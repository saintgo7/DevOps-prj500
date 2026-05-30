// Feasibility orchestrator (ADR-0019 §B). Wraps the pure scoring module
// with persistence + the human-review ledger. ODA / policy gates are
// enforced inside the BizPlan transition service; here we just compute
// and store the snapshot.

import {
  BadRequestException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { evaluateFeasibility, type PlanInputs } from './scoring';

@Injectable()
export class FeasibilityService {
  constructor(private readonly prisma: PrismaService) {}

  /**
   * Compute (or recompute) a feasibility snapshot for a plan. Replaces any
   * existing snapshot for the plan — the audit log preserves history. The
   * inputs come from the plan + its sections + its source refs; collecting
   * them is the controller's job (see controller).
   */
  async compute(
    tenantId: string,
    planId: string,
    inputs: PlanInputs,
    reviewMode: 'deterministic-only' | 'human-adjusted' = 'deterministic-only',
  ) {
    const plan = await this.prisma.bizPlan.findFirst({ where: { id: planId, tenantId } });
    if (!plan) throw new NotFoundException('Plan not found.');

    const result = evaluateFeasibility(inputs);

    return this.prisma.$transaction(async (tx) => {
      const existing = await tx.bizPlanFeasibility.findFirst({ where: { planId } });
      if (existing) {
        await tx.feasibilityAxisScore.deleteMany({ where: { feasibilityId: existing.id } });
        await tx.bizPlanFeasibility.delete({ where: { id: existing.id } });
      }
      const feas = await tx.bizPlanFeasibility.create({
        data: {
          tenantId,
          planId,
          feasibilityScore: result.feasibilityScore,
          outcome: result.outcome,
          reviewMode,
        },
      });
      await tx.feasibilityAxisScore.createMany({
        data: result.axes.map((a) => ({
          tenantId,
          feasibilityId: feas.id,
          axis: a.axis,
          score: a.score,
          rationale: a.rationale as unknown as Prisma.InputJsonValue,
        })),
      });
      return feas;
    });
  }

  /** Append-only review ledger entry. Reviewer cannot change a previous one. */
  async addReview(
    tenantId: string,
    feasibilityId: string,
    reviewerId: string,
    decision: 'approve' | 'request_changes' | 'reject',
    domainExpert: boolean,
    comment?: string,
  ) {
    if (!['approve', 'request_changes', 'reject'].includes(decision)) {
      throw new BadRequestException(`Unknown decision '${decision}'.`);
    }
    const feas = await this.prisma.bizPlanFeasibility.findFirst({
      where: { id: feasibilityId, tenantId },
    });
    if (!feas) throw new NotFoundException('Feasibility snapshot not found.');
    return this.prisma.feasibilityReview.create({
      data: {
        tenantId,
        feasibilityId,
        reviewerId,
        decision,
        domainExpert,
        comment: comment ?? null,
      },
    });
  }
}
