// Expert profiles + credentials + matches (ADR-0019 §C).
//
// Hard rules enforced here:
//   - 'verified' credential kind requires verifiedBy + verifiedAt to be
//     provided; self-reporting as verified is rejected. The DB CHECK
//     enforces structural validity; this layer surfaces the error.
//   - Match suggestions never auto-message anyone. State only moves to
//     'engaged' once BOTH sides accept.
//   - Profiles default to 'platform-only' visibility; the user opts up
//     to 'public' or down to 'private'.
//   - Score = 0.4*domain + 0.2*locale + 0.2*region + 0.1*ldcBoost + 0.1*availability.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { LDC_REGIONS } from '../feasibility/scoring';

export type ExpertAvailability = 'open' | 'busy' | 'closed';
export type ExpertVisibility = 'public' | 'platform-only' | 'private';
export type CredentialKind =
  | 'orcid'
  | 'linkedin'
  | 'official_org'
  | 'community-vouched'
  | 'self-reported'
  | 'verified';
export type SubjectKind =
  | 'bizplan'
  | 'impact_study'
  | 'funding_proposal'
  | 'maker_project'
  | 'need_request';
export type MatchState =
  | 'suggested'
  | 'invited'
  | 'accepted'
  | 'engaged'
  | 'completed'
  | 'declined'
  | 'cancelled';

export interface CreateProfileInput {
  tenantId: string;
  userId: string;
  headlineI18n: Record<string, string>;
  sdgFocus?: string[];
  workingLocales?: string[];
  fieldRegions?: string[];
  availability?: ExpertAvailability;
  visibility?: ExpertVisibility;
}

export interface CredentialInput {
  tenantId: string;
  expertId: string;
  kind: CredentialKind;
  ref: string;
  /** Required if kind === 'verified'. */
  verifierId?: string;
}

export interface SubjectMatchInputs {
  /** SDG focus on the subject (BizPlan / Study / etc.). */
  sdgFocus: readonly string[];
  /** Locales the subject is published in / requires. */
  locales: readonly string[];
  /** Regions the subject applies to. */
  regions: readonly string[];
}

export interface ExpertScored {
  expertId: string;
  score: number;
  reasons: string[];
}

const ALLOWED: Record<MatchState, MatchState[]> = {
  suggested: ['invited', 'declined', 'cancelled'],
  invited: ['accepted', 'declined', 'cancelled'],
  accepted: ['engaged', 'cancelled'],
  engaged: ['completed', 'cancelled'],
  completed: [],
  declined: [],
  cancelled: [],
};

const W_DOMAIN = 0.4;
const W_LOCALE = 0.2;
const W_REGION = 0.2;
const W_LDC = 0.1;
const W_AVAIL = 0.1;

interface ExpertLike {
  id: string;
  sdgFocus: readonly string[];
  workingLocales: readonly string[];
  fieldRegions: readonly string[];
  availability: string;
}

/** Pure deterministic scorer — exported for unit tests. */
export function scoreExpertForSubject(
  expert: ExpertLike,
  subject: SubjectMatchInputs,
): ExpertScored {
  const reasons: string[] = [];

  const domainOverlap = expert.sdgFocus.filter((s) => subject.sdgFocus.includes(s)).length;
  const domain = subject.sdgFocus.length === 0
    ? 0
    : Math.min(100, (domainOverlap / subject.sdgFocus.length) * 100);
  reasons.push(`domain ${domain.toFixed(0)} (${domainOverlap}/${subject.sdgFocus.length} SDG overlap)`);

  const localeOverlap = expert.workingLocales.filter((l) => subject.locales.includes(l)).length;
  const locale = subject.locales.length === 0
    ? 50
    : Math.min(100, (localeOverlap / subject.locales.length) * 100);
  reasons.push(`locale ${locale.toFixed(0)} (${localeOverlap}/${subject.locales.length} locales)`);

  const regionOverlap = expert.fieldRegions.filter((r) => subject.regions.includes(r)).length;
  const region = subject.regions.length === 0
    ? 50
    : Math.min(100, (regionOverlap / subject.regions.length) * 100);
  reasons.push(`region ${region.toFixed(0)} (${regionOverlap}/${subject.regions.length} regions)`);

  const subjectInLdc = subject.regions.some((r) => LDC_REGIONS.has(r));
  const expertHasLdc = expert.fieldRegions.some((r) => LDC_REGIONS.has(r));
  const ldc = subjectInLdc && expertHasLdc ? 100 : 0;
  reasons.push(`ldc ${ldc} (subjectLDC=${subjectInLdc} expertLDC=${expertHasLdc})`);

  const avail = expert.availability === 'open' ? 100 : expert.availability === 'busy' ? 50 : 0;
  reasons.push(`availability ${avail} (${expert.availability})`);

  const score = Math.round(
    domain * W_DOMAIN + locale * W_LOCALE + region * W_REGION + ldc * W_LDC + avail * W_AVAIL,
  );
  return { expertId: expert.id, score, reasons };
}

@Injectable()
export class ExpertsService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: MatchState, to: MatchState): boolean {
    return ALLOWED[from].includes(to);
  }

  async createProfile(input: CreateProfileInput) {
    if (!input.headlineI18n || Object.keys(input.headlineI18n).length === 0) {
      throw new BadRequestException('Profile needs a headline in at least one locale.');
    }
    if (input.availability && !['open', 'busy', 'closed'].includes(input.availability)) {
      throw new BadRequestException(`Unknown availability '${input.availability}'.`);
    }
    if (
      input.visibility &&
      !['public', 'platform-only', 'private'].includes(input.visibility)
    ) {
      throw new BadRequestException(`Unknown visibility '${input.visibility}'.`);
    }
    return this.prisma.expertProfile.create({
      data: {
        tenantId: input.tenantId,
        userId: input.userId,
        headlineI18n: input.headlineI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus ?? [],
        workingLocales: input.workingLocales ?? [],
        fieldRegions: input.fieldRegions ?? [],
        availability: input.availability ?? 'open',
        visibility: input.visibility ?? 'platform-only',
      },
    });
  }

  async addCredential(input: CredentialInput) {
    if (input.kind === 'verified' && !input.verifierId) {
      throw new BadRequestException(
        "'verified' credentials must be granted by an admin verifier — verifierId required.",
      );
    }
    if (!input.ref || input.ref.trim().length === 0) {
      throw new BadRequestException('Credential ref is required.');
    }
    const expert = await this.prisma.expertProfile.findFirst({
      where: { id: input.expertId, tenantId: input.tenantId },
    });
    if (!expert) throw new NotFoundException('Expert profile not found.');
    return this.prisma.expertCredential.create({
      data: {
        tenantId: input.tenantId,
        expertId: input.expertId,
        kind: input.kind,
        ref: input.ref.trim(),
        verifiedBy: input.kind === 'verified' ? input.verifierId! : null,
        verifiedAt: input.kind === 'verified' ? new Date() : null,
      },
    });
  }

  /**
   * Suggest matches for a subject. The caller passes the SubjectMatchInputs;
   * we score every open/busy expert in the tenant and persist the top N.
   * Closed-availability experts are excluded entirely.
   */
  async suggestMatches(
    tenantId: string,
    subject: { kind: SubjectKind; id: string },
    inputs: SubjectMatchInputs,
    topN = 5,
  ) {
    const experts = await this.prisma.expertProfile.findMany({
      where: { tenantId, availability: { in: ['open', 'busy'] } },
    });
    if (experts.length === 0) return [];
    const scored = experts
      .map((e) =>
        scoreExpertForSubject(
          {
            id: e.id,
            sdgFocus: e.sdgFocus,
            workingLocales: e.workingLocales,
            fieldRegions: e.fieldRegions,
            availability: e.availability,
          },
          inputs,
        ),
      )
      .sort((a, b) => b.score - a.score)
      .slice(0, topN);

    const created: Array<{ id: string }> = [];
    for (const s of scored) {
      // Skip if this expert × subject pair already exists.
      const existing = await this.prisma.expertMatch.findFirst({
        where: {
          tenantId,
          expertId: s.expertId,
          subjectKind: subject.kind,
          subjectId: subject.id,
        },
      });
      if (existing) continue;
      const m = await this.prisma.expertMatch.create({
        data: {
          tenantId,
          expertId: s.expertId,
          subjectKind: subject.kind,
          subjectId: subject.id,
          matchScore: s.score,
          state: 'suggested',
        },
      });
      created.push({ id: m.id });
    }
    return created;
  }

  /**
   * One-sided acceptance. Both expert and subject owner must hit accept
   * before the match transitions to 'accepted' (and contact details may be
   * unmasked at the API layer).
   */
  async accept(tenantId: string, matchId: string, side: 'expert' | 'owner') {
    const m = await this.prisma.expertMatch.findFirst({ where: { id: matchId, tenantId } });
    if (!m) throw new NotFoundException('Match not found.');
    if (m.state !== 'suggested' && m.state !== 'invited') {
      throw new ConflictException(
        `Cannot accept a match in state '${m.state}'.`,
      );
    }
    const data: Record<string, unknown> = { state: 'invited' };
    if (side === 'expert') {
      if (m.expertAcceptedAt) throw new ConflictException('Expert already accepted.');
      data.expertAcceptedAt = new Date();
      if (m.ownerAcceptedAt) data.state = 'accepted';
    } else {
      if (m.ownerAcceptedAt) throw new ConflictException('Owner already accepted.');
      data.ownerAcceptedAt = new Date();
      if (m.expertAcceptedAt) data.state = 'accepted';
    }
    return this.prisma.expertMatch.update({
      where: { id: matchId },
      data: data as unknown as Prisma.ExpertMatchUpdateInput,
    });
  }

  async transitionMatch(tenantId: string, matchId: string, to: MatchState) {
    const m = await this.prisma.expertMatch.findFirst({ where: { id: matchId, tenantId } });
    if (!m) throw new NotFoundException('Match not found.');
    if (!ExpertsService.canTransition(m.state as MatchState, to)) {
      throw new ConflictException(`Cannot transition match '${m.state}' → '${to}'.`);
    }
    return this.prisma.expertMatch.update({
      where: { id: matchId },
      data: { state: to },
    });
  }

  /**
   * Mask contact information until BOTH sides have accepted. Consumers
   * should call this before returning expert profiles attached to a match.
   */
  static maskIfNotAccepted<T extends { email?: string | null; phoneE164?: string | null }>(
    profile: T,
    matchAccepted: boolean,
  ): T {
    if (matchAccepted) return profile;
    return {
      ...profile,
      ...(profile.email !== undefined ? { email: null } : {}),
      ...(profile.phoneE164 !== undefined ? { phoneE164: null } : {}),
    };
  }
}
