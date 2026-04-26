// AI-assisted BizPlan authoring (ADR-0019 §A).
//
// Hard rules enforced at the service layer:
//   - noncommercialNotice = true on creation; rejected otherwise.
//   - Track is immutable after creation.
//   - State transitions follow an explicit allow-list.
//   - Sections (other than executive_summary) require ≥ 1 source ref to
//     be considered AI-citable. The countSources guard mirrors ADR-0017.
//   - ready_for_use requires a passing feasibility snapshot AND the
//     track-specific reviewer count (oda/policy ≥ 2 incl. ≥1 domain expert).

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { checkHarmfulContent } from '../tones/harmful-content';

export type PlanTrack =
  | 'business'
  | 'policy'
  | 'pledge'
  | 'investment'
  | 'oda'
  | 'execution'
  | 'management';

export type PlanState =
  | 'drafting'
  | 'ai_drafted'
  | 'human_review'
  | 'revising'
  | 'ready_for_use'
  | 'archived';

export type SectionKind =
  | 'executive_summary'
  | 'problem_statement'
  | 'solution'
  | 'theory_of_change'
  | 'beneficiaries'
  | 'budget'
  | 'timeline'
  | 'risk'
  | 'monitoring'
  | 'sustainability'
  | 'partners';

export interface CreatePlanInput {
  tenantId: string;
  ownerId: string;
  track: PlanTrack;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; audience?: string; periodLabel?: string }>;
  sdgFocus: string[];
  applicableRegions?: string[];
  periodMonths: number;
  audienceLabel?: string;
  noncommercialNotice: boolean;
}

export interface SectionDraft {
  position: number;
  kind: SectionKind;
  bodyI18n: Record<string, string>;
  plainLanguageScore?: number;
  aiProvenance?: {
    model: string;
    promptVersion: string;
    generatedAt: string;
    tokensIn?: number;
    tokensOut?: number;
  };
}

export interface SourceRefDraft {
  position: number;
  rendered: string;
  sourceWatchItemId?: string;
  sourceColumnId?: string;
  sourcePatentInsightId?: string;
  sourceManuscriptId?: string;
  externalDoi?: string;
  externalUrl?: string;
}

export const TRACKS: ReadonlyArray<PlanTrack> = [
  'business',
  'policy',
  'pledge',
  'investment',
  'oda',
  'execution',
  'management',
];

export const SECTION_KINDS: ReadonlyArray<SectionKind> = [
  'executive_summary',
  'problem_statement',
  'solution',
  'theory_of_change',
  'beneficiaries',
  'budget',
  'timeline',
  'risk',
  'monitoring',
  'sustainability',
  'partners',
];

const ALLOWED: Record<PlanState, PlanState[]> = {
  drafting: ['ai_drafted', 'archived'],
  ai_drafted: ['human_review', 'revising', 'archived'],
  human_review: ['revising', 'ready_for_use', 'archived'],
  revising: ['human_review', 'archived'],
  ready_for_use: ['archived'],
  archived: [],
};

const TWO_REVIEWER_TRACKS: ReadonlyArray<PlanTrack> = ['oda', 'policy'];
const PLEDGE_SECTION_WORD_CAP = 200;

export function countSources(r: SourceRefDraft): number {
  return (
    (r.sourceWatchItemId ? 1 : 0) +
    (r.sourceColumnId ? 1 : 0) +
    (r.sourcePatentInsightId ? 1 : 0) +
    (r.sourceManuscriptId ? 1 : 0) +
    (r.externalDoi ? 1 : 0) +
    (r.externalUrl ? 1 : 0)
  );
}

@Injectable()
export class BizPlanService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: PlanState, to: PlanState): boolean {
    return ALLOWED[from].includes(to);
  }

  async createPlan(input: CreatePlanInput) {
    if (input.noncommercialNotice !== true) {
      throw new BadRequestException(
        'BizPlans must declare non-commercial use. Toggle the notice and submit again.',
      );
    }
    if (!TRACKS.includes(input.track)) {
      throw new BadRequestException(`Unsupported track '${input.track}'.`);
    }
    if (input.periodMonths <= 0) {
      throw new BadRequestException('periodMonths must be > 0.');
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary?.title) {
      throw new BadRequestException(
        `Plan body needs a title in primary locale (${input.primaryLocale}).`,
      );
    }
    return this.prisma.bizPlan.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        track: input.track,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        applicableRegions: input.applicableRegions ?? [],
        periodMonths: input.periodMonths,
        audienceLabel: input.audienceLabel ?? null,
        noncommercialNotice: true,
        state: 'drafting',
      },
    });
  }

  async upsertSection(
    tenantId: string,
    planId: string,
    draft: SectionDraft,
  ) {
    const plan = await this.prisma.bizPlan.findFirst({ where: { id: planId, tenantId } });
    if (!plan) throw new NotFoundException('Plan not found.');
    if (plan.state === 'archived' || plan.state === 'ready_for_use') {
      throw new ConflictException(
        `Cannot edit sections of a plan in state '${plan.state}'.`,
      );
    }
    if (!SECTION_KINDS.includes(draft.kind)) {
      throw new BadRequestException(`Unknown section kind '${draft.kind}'.`);
    }
    if (
      draft.plainLanguageScore !== undefined &&
      (draft.plainLanguageScore < 0 || draft.plainLanguageScore > 100)
    ) {
      throw new BadRequestException('plainLanguageScore must be between 0 and 100.');
    }
    // Track-specific guard: pledge sections are short and plain-language.
    if (plan.track === 'pledge') {
      const overLimit = Object.values(draft.bodyI18n).some(
        (text) => text.split(/\s+/).filter(Boolean).length > PLEDGE_SECTION_WORD_CAP,
      );
      if (overLimit) {
        throw new BadRequestException(
          `Pledge sections must be ≤ ${PLEDGE_SECTION_WORD_CAP} words.`,
        );
      }
    }
    // Harmful-content guard runs on every section text variant.
    const harm = checkHarmfulContent(Object.values(draft.bodyI18n));
    if (!harm.pass) {
      throw new BadRequestException({
        error: 'Section text blocked by the harmful-content guard.',
        items: harm.findings.filter((f) => !f.ok).map((f) => `${f.category}: ${f.message}`),
      });
    }

    const existing = await this.prisma.bizPlanSection.findFirst({
      where: { planId, kind: draft.kind },
    });
    if (existing) {
      return this.prisma.bizPlanSection.update({
        where: { id: existing.id },
        data: {
          position: draft.position,
          bodyI18n: draft.bodyI18n as unknown as Prisma.InputJsonValue,
          plainLanguageScore: draft.plainLanguageScore ?? null,
          aiProvenance: (draft.aiProvenance ?? null) as unknown as Prisma.InputJsonValue,
        },
      });
    }
    return this.prisma.bizPlanSection.create({
      data: {
        tenantId,
        planId,
        position: draft.position,
        kind: draft.kind,
        bodyI18n: draft.bodyI18n as unknown as Prisma.InputJsonValue,
        plainLanguageScore: draft.plainLanguageScore ?? null,
        aiProvenance: (draft.aiProvenance ?? null) as unknown as Prisma.InputJsonValue,
      },
    });
  }

  async addSourceRef(
    tenantId: string,
    sectionId: string,
    draft: SourceRefDraft,
  ) {
    if (countSources(draft) !== 1) {
      throw new BadRequestException(
        'Source ref must point at exactly one source — got ' + countSources(draft),
      );
    }
    if (!draft.rendered || draft.rendered.trim().length === 0) {
      throw new BadRequestException('Source ref needs a rendered citation string.');
    }
    const section = await this.prisma.bizPlanSection.findFirst({
      where: { id: sectionId, tenantId },
    });
    if (!section) throw new NotFoundException('Section not found.');
    return this.prisma.bizPlanSourceRef.create({
      data: {
        tenantId,
        sectionId,
        position: draft.position,
        sourceWatchItemId: draft.sourceWatchItemId ?? null,
        sourceColumnId: draft.sourceColumnId ?? null,
        sourcePatentInsightId: draft.sourcePatentInsightId ?? null,
        sourceManuscriptId: draft.sourceManuscriptId ?? null,
        externalDoi: draft.externalDoi ?? null,
        externalUrl: draft.externalUrl ?? null,
        rendered: draft.rendered.trim(),
      },
    });
  }

  /**
   * Move state with structural checks. ready_for_use requires:
   *   - a feasibility row with outcome='pass'
   *   - track-specific reviewer count (oda/policy ≥ 2 incl. ≥1 domain expert)
   */
  async transition(tenantId: string, planId: string, to: PlanState) {
    const plan = await this.prisma.bizPlan.findFirst({ where: { id: planId, tenantId } });
    if (!plan) throw new NotFoundException('Plan not found.');
    const from = plan.state as PlanState;
    if (!BizPlanService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'ready_for_use') {
      const fea = await this.prisma.bizPlanFeasibility.findFirst({
        where: { planId, tenantId },
      });
      if (!fea) {
        throw new BadRequestException(
          'Plan needs a feasibility snapshot before going ready_for_use.',
        );
      }
      if (fea.outcome !== 'pass') {
        throw new BadRequestException(
          `Feasibility outcome is '${fea.outcome}' — every axis must score ≥ 40.`,
        );
      }
      if (TWO_REVIEWER_TRACKS.includes(plan.track as PlanTrack)) {
        const reviews = await this.prisma.feasibilityReview.findMany({
          where: { feasibilityId: fea.id, decision: 'approve' },
        });
        if (reviews.length < 2) {
          throw new ConflictException(
            `Track '${plan.track}' needs at least 2 'approve' reviews — got ${reviews.length}.`,
          );
        }
        if (!reviews.some((r) => r.domainExpert)) {
          throw new ConflictException(
            `Track '${plan.track}' needs at least one approving reviewer flagged as a domain expert.`,
          );
        }
      }
    }
    return this.prisma.bizPlan.update({
      where: { id: planId },
      data: {
        state: to,
        ...(to === 'ready_for_use' ? { readyForUseAt: new Date() } : {}),
        ...(to === 'archived' ? { archivedAt: new Date() } : {}),
      },
    });
  }
}
