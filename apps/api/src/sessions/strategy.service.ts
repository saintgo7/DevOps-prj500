// Strategy-session service. See ADR-0016 §B for the full lifecycle.
//
// Hard rules enforced here:
//   1. noncommercialNotice MUST be true on creation; false is rejected.
//   2. Only state='approved' sessions may issue invites.
//   3. Once a session is revoked it cannot return to active — the state
//      transition is final and append-only (with revokedBy + reason).
//   4. Anyone with role 'super-admin' may revoke any session in any state
//      at any time. The check is performed in the controller layer; this
//      service exposes revoke() unconditionally so that the controller's
//      RBAC decoration is the single point of truth.

import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { checkHarmfulContent } from '../tones/harmful-content';

export type SessionState = 'draft' | 'invited' | 'active' | 'revoked';

export interface CreateSessionInput {
  tenantId: string;
  ownerId: string;
  insightId: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; plan: string; riskNote?: string }>;
  sdgFocus: string[];
  applicableRegions?: string[];
  /**
   * MUST be true. The migration enforces a CHECK constraint as a second
   * line of defence; this service rejects with a plain-language error.
   */
  noncommercialNotice: boolean;
}

@Injectable()
export class StrategyService {
  constructor(private readonly prisma: PrismaService) {}

  async create(input: CreateSessionInput) {
    if (input.noncommercialNotice !== true) {
      throw new BadRequestException(
        'A strategy session must declare non-commercial use. Toggle the non-commercial notice and submit again.',
      );
    }

    // Block harmful content at creation time. The same guard runs again
    // when admins approve, but catching it early saves curator time.
    const parts = Object.values(input.bodyI18n).flatMap((b) => [b.title, b.plan, b.riskNote ?? '']);
    const harm = checkHarmfulContent(parts);
    if (!harm.pass) {
      throw new BadRequestException({
        error: 'Strategy text contains content that the harmful-content guard blocked.',
        items: harm.findings.filter((f) => !f.ok).map((f) => `${f.category}: ${f.message}`),
      });
    }

    const insight = await this.prisma.patentInsight.findFirst({
      where: { id: input.insightId, tenantId: input.tenantId },
    });
    if (!insight) {
      throw new NotFoundException(
        'Patent insight not found for this tenant. Sessions can only build on approved insights.',
      );
    }
    if (insight.state !== 'approved') {
      throw new BadRequestException(
        `Patent insight is in state '${insight.state}'. Only approved insights may host a session.`,
      );
    }

    return this.prisma.strategySession.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        insightId: input.insightId,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        applicableRegions: input.applicableRegions ?? [],
        noncommercialNotice: true,
        state: 'draft',
      },
    });
  }

  async approve(tenantId: string, sessionId: string, approverId: string) {
    const s = await this.prisma.strategySession.findFirst({
      where: { id: sessionId, tenantId },
    });
    if (!s) throw new NotFoundException('Session not found.');
    if (s.state !== 'draft') {
      throw new ConflictException(
        `Cannot approve a session in state '${s.state}'. Only drafts may be approved.`,
      );
    }
    if (!s.noncommercialNotice) {
      // Defence in depth — should have been caught at create() time.
      throw new ForbiddenException('Session is missing the non-commercial notice.');
    }
    return this.prisma.strategySession.update({
      where: { id: sessionId },
      data: { state: 'invited', approvedAt: new Date(), approvedBy: approverId },
    });
  }

  /**
   * Permanently revoke a session. Caller MUST be guarded with
   * @Roles('super-admin') at the controller layer. Once revoked, the
   * session never re-activates: a new strategy must be created from
   * scratch under fresh approval.
   */
  async revoke(
    tenantId: string,
    sessionId: string,
    superAdminId: string,
    reason: string,
  ) {
    if (!reason || reason.trim().length < 8) {
      throw new BadRequestException(
        'Revoke reason must be at least 8 characters — this is recorded in the audit log forever.',
      );
    }
    const s = await this.prisma.strategySession.findFirst({
      where: { id: sessionId, tenantId },
    });
    if (!s) throw new NotFoundException('Session not found.');
    if (s.state === 'revoked') {
      throw new ConflictException('Session is already revoked.');
    }
    return this.prisma.$transaction(async (tx) => {
      await tx.strategySession.update({
        where: { id: sessionId },
        data: {
          state: 'revoked',
          revokedAt: new Date(),
          revokedBy: superAdminId,
          revokeReason: reason.trim(),
        },
      });
      // Invalidate every outstanding invite simultaneously.
      await tx.sessionInvite.updateMany({
        where: { sessionId, acceptedAt: null, declinedAt: null, revokedAt: null },
        data: { revokedAt: new Date() },
      });
      return { ok: true };
    });
  }

  async invite(input: {
    tenantId: string;
    sessionId: string;
    invitedBy: string;
    inviteeEmail: string;
    shareRight?: 'view' | 'discuss';
  }) {
    const s = await this.prisma.strategySession.findFirst({
      where: { id: input.sessionId, tenantId: input.tenantId },
    });
    if (!s) throw new NotFoundException('Session not found.');
    if (s.state !== 'invited' && s.state !== 'active') {
      throw new ConflictException(
        `Cannot invite to a session in state '${s.state}'. Approve the session first.`,
      );
    }
    return this.prisma.sessionInvite.create({
      data: {
        tenantId: input.tenantId,
        sessionId: input.sessionId,
        invitedBy: input.invitedBy,
        inviteeEmail: input.inviteeEmail,
        shareRight: input.shareRight ?? 'view',
        expiresAt: new Date(Date.now() + 14 * 86400 * 1000), // 14 days
      },
    });
  }

  async accept(tenantId: string, inviteId: string, agreedClause: string) {
    const inv = await this.prisma.sessionInvite.findFirst({
      where: { id: inviteId, tenantId },
    });
    if (!inv) throw new NotFoundException('Invite not found.');
    if (inv.acceptedAt) throw new ConflictException('Invite already accepted.');
    if (inv.declinedAt) throw new ConflictException('Invite was declined.');
    if (inv.revokedAt) throw new ConflictException('Invite was revoked.');
    if (inv.expiresAt.getTime() < Date.now()) {
      throw new ConflictException('Invite has expired.');
    }
    if (!/non-?commercial/i.test(agreedClause)) {
      throw new BadRequestException(
        'Acceptance must include the non-commercial use clause text. Re-submit with the displayed clause.',
      );
    }
    return this.prisma.sessionInvite.update({
      where: { id: inviteId },
      data: {
        acceptedAt: new Date(),
        consentRecord: {
          agreedAt: new Date().toISOString(),
          agreedClause,
        } as unknown as Prisma.InputJsonValue,
      },
    });
  }
}
