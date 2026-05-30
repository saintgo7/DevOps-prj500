// Subscriber/liker opt-in for impact verification (ADR-0017 §C.1).
//
// We never assume "subscribe = consent". Inclusion in any impact study
// requires an explicit, scoped, time-bound, revocable consent record.

import { createHash } from 'node:crypto';
import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type ConsentLevel = 'aggregate-only' | 'longitudinal';

export interface ConsentScope {
  sdgFocus?: string[];
  regions?: string[];
  topicTags?: string[];
}

export interface RecordConsentInput {
  tenantId: string;
  userId: string;
  scope: ConsentScope;
  level: ConsentLevel;
  /** Version tag of the displayed consent text — e.g. 'v1.2'. */
  consentVersion: string;
  /** Exact text the user saw and agreed to. We hash it; the raw is not stored. */
  agreedClauseText: string;
  /** ms since epoch. Defaults to 12 months from now. */
  expiresAt?: Date;
}

const TWELVE_MONTHS_MS = 365 * 24 * 60 * 60 * 1000;

@Injectable()
export class ConsentService {
  constructor(private readonly prisma: PrismaService) {}

  /**
   * Record a consent. Idempotent on (tenantId, userId, consentVersion) —
   * if the user re-agrees to the same version we keep the original timestamp
   * and just refresh `expiresAt`.
   */
  async record(input: RecordConsentInput) {
    if (input.level !== 'aggregate-only' && input.level !== 'longitudinal') {
      throw new BadRequestException(`Unsupported consent level '${input.level}'.`);
    }
    if (!input.consentVersion || input.consentVersion.trim().length === 0) {
      throw new BadRequestException('consentVersion is required.');
    }
    if (!input.agreedClauseText || input.agreedClauseText.trim().length < 30) {
      throw new BadRequestException(
        'Agreed clause text is too short — pass the full clause the user saw.',
      );
    }

    const expiresAt = input.expiresAt ?? new Date(Date.now() + TWELVE_MONTHS_MS);
    const agreedClauseHash = createHash('sha256')
      .update(input.agreedClauseText)
      .digest('hex');

    const existing = await this.prisma.impactConsentRecord.findFirst({
      where: {
        tenantId: input.tenantId,
        userId: input.userId,
        consentVersion: input.consentVersion,
      },
    });
    if (existing) {
      if (existing.agreedClauseHash !== agreedClauseHash) {
        throw new ConflictException(
          'This consent version already exists with different text. Bump consentVersion and re-record.',
        );
      }
      return this.prisma.impactConsentRecord.update({
        where: { id: existing.id },
        data: { expiresAt, revokedAt: null },
      });
    }

    return this.prisma.impactConsentRecord.create({
      data: {
        tenantId: input.tenantId,
        userId: input.userId,
        scope: (input.scope ?? {}) as unknown as Prisma.InputJsonValue,
        level: input.level,
        consentVersion: input.consentVersion,
        agreedClauseHash,
        expiresAt,
      },
    });
  }

  /** Revoke a single consent record. Idempotent on already-revoked rows. */
  async revoke(tenantId: string, recordId: string) {
    const r = await this.prisma.impactConsentRecord.findFirst({
      where: { id: recordId, tenantId },
    });
    if (!r) throw new NotFoundException('Consent record not found.');
    if (r.revokedAt) {
      // Already revoked: return as-is without an update so audit trail
      // shows a single revocation event.
      return r;
    }
    return this.prisma.impactConsentRecord.update({
      where: { id: recordId },
      data: { revokedAt: new Date() },
    });
  }

  /**
   * Pure helper: does this consent record cover the given study scope right
   * now? Used by the study service before counting an enrollee.
   */
  static covers(
    record: {
      scope: ConsentScope | null;
      level: ConsentLevel | string;
      expiresAt: Date;
      revokedAt: Date | null;
    },
    study: { sdgFocus: readonly string[]; regions: readonly string[]; topicTags: readonly string[] },
    now: Date = new Date(),
  ): boolean {
    if (record.revokedAt && record.revokedAt.getTime() <= now.getTime()) return false;
    if (record.expiresAt.getTime() < now.getTime()) return false;
    const scope = record.scope ?? {};
    const sdgOk =
      !scope.sdgFocus ||
      scope.sdgFocus.length === 0 ||
      study.sdgFocus.some((s) => scope.sdgFocus!.includes(s));
    const regionOk =
      !scope.regions ||
      scope.regions.length === 0 ||
      study.regions.some((r) => scope.regions!.includes(r));
    const topicOk =
      !scope.topicTags ||
      scope.topicTags.length === 0 ||
      study.topicTags.some((t) => scope.topicTags!.includes(t));
    return sdgOk && regionOk && topicOk;
  }
}
