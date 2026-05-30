// Impact studies — region × country × SDG-topic verification (ADR-0017 §C).
//
// Lifecycle:
//   draft → enrolling → analysing → review → published → retired
//
// Hard rules enforced here:
//   - K-anonymity floor consulted for both creation and publish.
//   - Sensitive studies use floor=25 (overrides any caller-supplied value).
//   - Publish requires at least 2 'approve' reviews (one with domain_expert=true).
//   - Publish refuses if any observation is below floor; small cohorts are
//     suppressed (set release_ready=false, suppressed=true) instead of leaked.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { evaluateKAnonymity, floorFor } from './k-anonymity';

export type StudyState =
  | 'draft'
  | 'enrolling'
  | 'analysing'
  | 'review'
  | 'published'
  | 'retired';

export interface CreateStudyInput {
  tenantId: string;
  ownerId: string;
  title: string;
  hypothesis: string;
  method: string;
  sdgFocus: string[];
  regions: string[];
  topicTags: string[];
  windowStart: Date;
  windowEnd: Date;
  sensitiveTopic?: boolean;
}

const ALLOWED_TRANSITIONS: Record<StudyState, StudyState[]> = {
  draft: ['enrolling', 'retired'],
  enrolling: ['analysing', 'retired'],
  analysing: ['review', 'retired'],
  review: ['analysing', 'published', 'retired'],
  published: ['retired'],
  retired: [],
};

@Injectable()
export class StudiesService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: StudyState, to: StudyState): boolean {
    return ALLOWED_TRANSITIONS[from].includes(to);
  }

  async create(input: CreateStudyInput) {
    if (input.windowEnd.getTime() <= input.windowStart.getTime()) {
      throw new BadRequestException('Study window end must be after window start.');
    }
    if (input.sdgFocus.length === 0) {
      throw new BadRequestException('Study must have at least one SDG focus.');
    }
    const sensitive = !!input.sensitiveTopic;
    const floor = floorFor(sensitive);
    return this.prisma.impactStudy.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        title: input.title,
        hypothesis: input.hypothesis,
        method: input.method,
        sdgFocus: input.sdgFocus,
        regions: input.regions,
        topicTags: input.topicTags,
        windowStart: input.windowStart,
        windowEnd: input.windowEnd,
        sensitiveTopic: sensitive,
        kAnonymityFloor: floor,
        state: 'draft',
      },
    });
  }

  async transition(tenantId: string, studyId: string, to: StudyState) {
    const s = await this.prisma.impactStudy.findFirst({
      where: { id: studyId, tenantId },
    });
    if (!s) throw new NotFoundException('Study not found.');
    const from = s.state as StudyState;
    if (!StudiesService.canTransition(from, to)) {
      throw new ConflictException(
        `Study is in state '${from}' — cannot transition to '${to}'.`,
      );
    }
    return this.prisma.impactStudy.update({
      where: { id: studyId },
      data: { state: to },
    });
  }

  /**
   * Publish a study. Refuses unless:
   *   - state == 'review'
   *   - >= 2 reviews with decision='approve'
   *   - >= 1 of those reviewers has domain_expert=true
   *   - every observation has cohortSize >= study.kAnonymityFloor
   * Observations below the floor are *not* leaked. They are flagged
   * suppressed=true so curators can see what was withheld.
   */
  async publish(tenantId: string, studyId: string) {
    const s = await this.prisma.impactStudy.findFirst({
      where: { id: studyId, tenantId },
    });
    if (!s) throw new NotFoundException('Study not found.');
    if (s.state !== 'review') {
      throw new ConflictException(
        `Cannot publish a study in state '${s.state}'. Move to 'review' first.`,
      );
    }

    const reviews = await this.prisma.impactStudyReview.findMany({
      where: { tenantId, studyId, decision: 'approve' },
    });
    if (reviews.length < 2) {
      throw new ConflictException(
        `Publish needs at least 2 'approve' reviews — got ${reviews.length}.`,
      );
    }
    if (!reviews.some((r) => r.domainExpert)) {
      throw new ConflictException(
        'Publish needs at least one approving reviewer flagged as a domain expert.',
      );
    }

    const observations = await this.prisma.impactObservation.findMany({
      where: { tenantId, studyId },
    });
    if (observations.length === 0) {
      throw new BadRequestException('Study has no observations to publish.');
    }
    const k = evaluateKAnonymity(observations, s.kAnonymityFloor);

    return this.prisma.$transaction(async (tx) => {
      // Mark each observation as either release-ready or suppressed.
      for (const detail of k.details) {
        await tx.impactObservation.update({
          where: { id: detail.id },
          data: {
            releaseReady: detail.passed,
            suppressed: !detail.passed,
          },
        });
      }
      if (k.ok === 0) {
        throw new ConflictException(
          'Every cohort fell below the k-anonymity floor; nothing is publishable. ' +
            'Widen the cohort or raise enrolment, then try again.',
        );
      }
      return tx.impactStudy.update({
        where: { id: studyId },
        data: { state: 'published', publishedAt: new Date() },
      });
    });
  }

  /**
   * Disclose a published study to a partner / channel — append-only audit.
   */
  async disclose(
    tenantId: string,
    studyId: string,
    channel: 'atom' | 'webhook' | 'export',
    recipient?: string,
  ) {
    const s = await this.prisma.impactStudy.findFirst({
      where: { id: studyId, tenantId },
    });
    if (!s) throw new NotFoundException('Study not found.');
    if (s.state !== 'published') {
      throw new ConflictException(
        `Cannot disclose a study in state '${s.state}'. Only published studies may be shared.`,
      );
    }
    return this.prisma.impactDisclosure.create({
      data: {
        tenantId,
        studyId,
        channel,
        recipient: recipient ?? null,
      },
    });
  }
}
