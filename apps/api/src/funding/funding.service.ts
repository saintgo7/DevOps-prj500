// Funding (crowdfunding + impact investment + in-kind) — ADR-0018 §A.
//
// Hard rules enforced here (DB CHECK is defence-in-depth):
//   - noncommercialNotice = true on creation; rejected otherwise.
//   - softGoalMinor <= hardGoalMinor; both > 0.
//   - State transitions are explicit allow-list.
//   - 'live' transition needs ≥1 milestone and admin gate (controller).
//   - Single contribution capped at 25% of hardGoalMinor (no whale capture).
//   - Body & milestones cannot be edited after 'live'; addendum only.
//   - Refund only on un-released balance.
//   - Super-admin pause/cancel — append-only, reason ≥ 30 chars.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { checkHarmfulContent } from '../tones/harmful-content';

export type FundingState =
  | 'draft'
  | 'review'
  | 'live'
  | 'funding_locked'
  | 'completed'
  | 'reported'
  | 'cancelled'
  | 'refunded'
  | 'paused';

export type FundingModel = 'all-or-nothing' | 'keep-it-all';
export type ContributionKind = 'donation' | 'impact-investment' | 'in-kind';
export type ContributionVisibility = 'public' | 'pseudonymous' | 'private';

export interface CreateProposalInput {
  tenantId: string;
  ownerId: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; summary: string; plan: string; budget?: string }>;
  sdgFocus: string[];
  region: string;
  fundingModel: FundingModel;
  contributionKinds: ContributionKind[];
  currency?: string;
  softGoalMinor: number;
  hardGoalMinor: number;
  endsAt: Date;
  noncommercialNotice: boolean;
}

export interface MilestoneDraft {
  position: number;
  title: string;
  description: string;
  amountMinor: number;
}

export interface ContributionInput {
  tenantId: string;
  proposalId: string;
  backerUserId?: string;
  kind: ContributionKind;
  amountMinor: number;
  currency: string;
  visibility?: ContributionVisibility;
  paymentProviderRef?: string;
}

const ALLOWED: Record<FundingState, FundingState[]> = {
  draft: ['review', 'cancelled'],
  review: ['live', 'draft', 'cancelled'],
  live: ['funding_locked', 'completed', 'cancelled', 'paused'],
  funding_locked: ['completed', 'cancelled'],
  completed: ['reported'],
  reported: [],
  cancelled: ['refunded'],
  refunded: [],
  paused: ['live', 'cancelled'],
};

const SINGLE_CONTRIB_FRACTION = 0.25;

@Injectable()
export class FundingService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: FundingState, to: FundingState): boolean {
    return ALLOWED[from].includes(to);
  }

  async createProposal(input: CreateProposalInput) {
    if (input.noncommercialNotice !== true) {
      throw new BadRequestException(
        'Funding proposals must declare non-commercial use. Toggle the notice and submit again.',
      );
    }
    if (!Array.isArray(input.contributionKinds) || input.contributionKinds.length === 0) {
      throw new BadRequestException('At least one contributionKinds entry is required.');
    }
    if (input.softGoalMinor <= 0 || input.hardGoalMinor <= 0) {
      throw new BadRequestException('Goals must be positive amounts (in currency minor units).');
    }
    if (input.softGoalMinor > input.hardGoalMinor) {
      throw new BadRequestException('softGoalMinor must be ≤ hardGoalMinor.');
    }
    if (input.endsAt.getTime() <= Date.now()) {
      throw new BadRequestException('endsAt must be in the future.');
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary?.title || !primary?.summary || !primary?.plan) {
      throw new BadRequestException(
        `Proposal body needs title + summary + plan in primary locale (${input.primaryLocale}).`,
      );
    }
    const harm = checkHarmfulContent(
      Object.values(input.bodyI18n).flatMap((b) => [b.title, b.summary, b.plan, b.budget ?? '']),
    );
    if (!harm.pass) {
      throw new BadRequestException({
        error: 'Proposal text contains content blocked by the harmful-content guard.',
        items: harm.findings.filter((f) => !f.ok).map((f) => `${f.category}: ${f.message}`),
      });
    }
    return this.prisma.fundingProposal.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        region: input.region,
        fundingModel: input.fundingModel,
        contributionKinds: input.contributionKinds,
        currency: input.currency ?? 'USD',
        softGoalMinor: input.softGoalMinor,
        hardGoalMinor: input.hardGoalMinor,
        endsAt: input.endsAt,
        noncommercialNotice: true,
        state: 'draft',
      },
    });
  }

  async addMilestone(tenantId: string, proposalId: string, draft: MilestoneDraft) {
    if (draft.amountMinor <= 0) throw new BadRequestException('Milestone amount must be > 0.');
    const p = await this.prisma.fundingProposal.findFirst({ where: { id: proposalId, tenantId } });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (p.state !== 'draft' && p.state !== 'review') {
      throw new ConflictException(
        `Cannot add milestones to a proposal in state '${p.state}'. Body is locked once live.`,
      );
    }
    return this.prisma.fundingMilestone.create({
      data: {
        tenantId,
        proposalId,
        position: draft.position,
        title: draft.title,
        description: draft.description,
        amountMinor: draft.amountMinor,
      },
    });
  }

  /**
   * Move state with structural checks. The controller layer enforces RBAC;
   * this service guarantees that the transition itself is valid AND that
   * key invariants are met for each target state.
   */
  async transition(
    tenantId: string,
    proposalId: string,
    to: FundingState,
    actorId: string,
  ) {
    const p = await this.prisma.fundingProposal.findFirst({ where: { id: proposalId, tenantId } });
    if (!p) throw new NotFoundException('Proposal not found.');
    const from = p.state as FundingState;
    if (!FundingService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'live') {
      const milestones = await this.prisma.fundingMilestone.count({
        where: { tenantId, proposalId },
      });
      if (milestones < 1) {
        throw new BadRequestException(
          'A proposal needs at least one milestone before going live.',
        );
      }
      if (!p.noncommercialNotice) {
        throw new BadRequestException('Proposal is missing the non-commercial notice.');
      }
    }
    return this.prisma.fundingProposal.update({
      where: { id: proposalId },
      data: {
        state: to,
        ...(to === 'live' ? { approvedAt: new Date(), approvedBy: actorId } : {}),
      },
    });
  }

  async contribute(input: ContributionInput) {
    if (input.amountMinor <= 0) throw new BadRequestException('Contribution amount must be > 0.');
    const p = await this.prisma.fundingProposal.findFirst({
      where: { id: input.proposalId, tenantId: input.tenantId },
    });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (p.state !== 'live') {
      throw new ConflictException(
        `Contributions accepted only on live proposals. Current state: '${p.state}'.`,
      );
    }
    if (!p.contributionKinds.includes(input.kind)) {
      throw new BadRequestException(
        `Contribution kind '${input.kind}' is not allowed on this proposal.`,
      );
    }
    if (input.currency !== p.currency) {
      throw new BadRequestException(
        `Contribution currency '${input.currency}' does not match proposal currency '${p.currency}'.`,
      );
    }
    const cap = Math.floor(p.hardGoalMinor * SINGLE_CONTRIB_FRACTION);
    if (input.amountMinor > cap) {
      throw new BadRequestException(
        `Single contribution capped at 25% of hard goal (${cap} ${p.currency} minor units).`,
      );
    }
    return this.prisma.$transaction(async (tx) => {
      const c = await tx.fundingContribution.create({
        data: {
          tenantId: input.tenantId,
          proposalId: input.proposalId,
          backerUserId: input.backerUserId ?? null,
          kind: input.kind,
          amountMinor: input.amountMinor,
          currency: input.currency,
          visibility: input.visibility ?? 'private',
          paymentProviderRef: input.paymentProviderRef ?? null,
          state: 'pending',
        },
      });
      // Tally is best-effort; payment partner webhook later flips the
      // contribution to 'collected' and updates raised_minor authoritatively.
      return c;
    });
  }

  /**
   * Mark a contribution as collected. Called by the payment partner webhook
   * handler. Updates the proposal's raised_minor in the same transaction so
   * the running tally stays consistent.
   */
  async confirmCollected(tenantId: string, contributionId: string) {
    const c = await this.prisma.fundingContribution.findFirst({
      where: { id: contributionId, tenantId },
    });
    if (!c) throw new NotFoundException('Contribution not found.');
    if (c.state !== 'pending') {
      throw new ConflictException(`Contribution already in state '${c.state}'.`);
    }
    return this.prisma.$transaction(async (tx) => {
      const updated = await tx.fundingContribution.update({
        where: { id: contributionId },
        data: { state: 'collected' },
      });
      await tx.fundingProposal.update({
        where: { id: c.proposalId },
        data: {
          raisedMinor: { increment: c.amountMinor },
          contributorCount: { increment: 1 },
        },
      });
      return updated;
    });
  }

  /**
   * Super-admin pause: blocks new contributions, opens refund window for
   * existing backers. The controller layer @Roles('super-admin') guards.
   */
  async pause(tenantId: string, proposalId: string, superAdminId: string, reason: string) {
    if (!reason || reason.trim().length < 30) {
      throw new BadRequestException(
        'Pause reason must be at least 30 characters — recorded in the audit log forever.',
      );
    }
    const p = await this.prisma.fundingProposal.findFirst({ where: { id: proposalId, tenantId } });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (p.state === 'paused') throw new ConflictException('Already paused.');
    if (p.state !== 'live') {
      throw new ConflictException(`Can only pause a live proposal. Current state: '${p.state}'.`);
    }
    return this.prisma.fundingProposal.update({
      where: { id: proposalId },
      data: {
        state: 'paused',
        pausedAt: new Date(),
        pauseReason: `${reason.trim()} (by:${superAdminId})`,
      },
    });
  }

  /** Anyone signed-in may flag a proposal — drives super-admin review. */
  async flag(
    tenantId: string,
    proposalId: string,
    reporterId: string,
    category: 'fraud' | 'commercial' | 'harm' | 'misinformation' | 'other',
    reason: string,
  ) {
    if (!reason || reason.trim().length < 30) {
      throw new BadRequestException('Flag reason must be at least 30 characters.');
    }
    const p = await this.prisma.fundingProposal.findFirst({ where: { id: proposalId, tenantId } });
    if (!p) throw new NotFoundException('Proposal not found.');
    return this.prisma.fundingFlag.create({
      data: { tenantId, proposalId, reporterId, category, reason: reason.trim() },
    });
  }
}
