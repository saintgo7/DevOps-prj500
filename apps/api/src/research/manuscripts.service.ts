// Research manuscripts — Nature-tier and SSCI-tier authoring (ADR-0017 §A).
//
// State machine (append-only):
//   draft → internal_review → external_peer_review → revise_requested
//                                                   → accepted → published
//                                                              → withdrawn

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { validateCitations, type CitationDraft } from './citations';

export type ManuscriptTier = 'nature' | 'ssci';
export type ManuscriptState =
  | 'draft'
  | 'internal_review'
  | 'external_peer_review'
  | 'revise_requested'
  | 'accepted'
  | 'published'
  | 'withdrawn';

export interface CreateManuscriptInput {
  tenantId: string;
  ownerId: string;
  tier: ManuscriptTier;
  primaryLocale: string;
  /** { en: { title, scientificAbstract }, ko: ..., ... } */
  bodyI18n: Record<string, { title: string; scientificAbstract: string }>;
  sdgFocus: string[];
  applicableRegions?: string[];
}

export interface PublishOptions {
  citations: CitationDraft[];
  /** { en: '...', ko: '...', sw?: '...' } — primaryLocale + 'en' required. */
  plainLanguageSummary: Record<string, string>;
  selfCiteOverrideReason?: string;
}

const ALLOWED_TRANSITIONS: Record<ManuscriptState, ManuscriptState[]> = {
  draft: ['internal_review', 'withdrawn'],
  internal_review: ['external_peer_review', 'revise_requested', 'withdrawn'],
  external_peer_review: ['accepted', 'revise_requested', 'withdrawn'],
  revise_requested: ['internal_review', 'external_peer_review', 'withdrawn'],
  accepted: ['published', 'withdrawn'],
  published: ['withdrawn'],
  withdrawn: [],
};

@Injectable()
export class ManuscriptsService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: ManuscriptState, to: ManuscriptState): boolean {
    return ALLOWED_TRANSITIONS[from].includes(to);
  }

  async create(input: CreateManuscriptInput) {
    if (input.tier !== 'nature' && input.tier !== 'ssci') {
      throw new BadRequestException(`Unsupported manuscript tier '${input.tier}'.`);
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary || !primary.title || !primary.scientificAbstract) {
      throw new BadRequestException(
        `Manuscript needs a title + scientific abstract in the primary locale (${input.primaryLocale}).`,
      );
    }
    return this.prisma.researchManuscript.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        tier: input.tier,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        applicableRegions: input.applicableRegions ?? [],
        state: 'draft',
      },
    });
  }

  async transition(tenantId: string, manuscriptId: string, to: ManuscriptState) {
    const m = await this.prisma.researchManuscript.findFirst({
      where: { id: manuscriptId, tenantId },
    });
    if (!m) throw new NotFoundException('Manuscript not found.');
    const from = m.state as ManuscriptState;
    if (!ManuscriptsService.canTransition(from, to)) {
      throw new ConflictException(
        `Manuscript is in state '${from}' — cannot transition to '${to}'.`,
      );
    }
    return this.prisma.researchManuscript.update({
      where: { id: manuscriptId },
      data: { state: to },
    });
  }

  async withdraw(tenantId: string, manuscriptId: string, reason: string) {
    if (!reason || reason.trim().length < 8) {
      throw new BadRequestException(
        'Withdraw reason must be at least 8 characters — it is recorded in the audit log forever.',
      );
    }
    const m = await this.prisma.researchManuscript.findFirst({
      where: { id: manuscriptId, tenantId },
    });
    if (!m) throw new NotFoundException('Manuscript not found.');
    if (m.state === 'withdrawn') {
      throw new ConflictException('Manuscript is already withdrawn.');
    }
    return this.prisma.researchManuscript.update({
      where: { id: manuscriptId },
      data: { state: 'withdrawn', withdrawnAt: new Date(), withdrawReason: reason.trim() },
    });
  }

  /**
   * Move a manuscript from 'accepted' to 'published'. Freezes the citation
   * list onto the manuscript so the chain is tamper-resistant afterwards.
   * Plain-language summary is mandatory at this gate (ADR-0017 §A.4).
   */
  async publish(tenantId: string, manuscriptId: string, opts: PublishOptions) {
    const m = await this.prisma.researchManuscript.findFirst({
      where: { id: manuscriptId, tenantId },
    });
    if (!m) throw new NotFoundException('Manuscript not found.');
    if (m.state !== 'accepted') {
      throw new ConflictException(
        `Cannot publish a manuscript in state '${m.state}'. Only 'accepted' manuscripts may publish.`,
      );
    }

    // Plain-language summary required: English + primary locale at minimum.
    const langs = Object.keys(opts.plainLanguageSummary).filter(
      (k) => (opts.plainLanguageSummary[k] ?? '').trim().length > 0,
    );
    if (!langs.includes('en') || !langs.includes(m.primaryLocale)) {
      throw new BadRequestException(
        `Plain-language summary must include both 'en' and the primary locale '${m.primaryLocale}'.`,
      );
    }

    const check = validateCitations(opts.citations, {
      selfManuscriptId: manuscriptId,
      ...(opts.selfCiteOverrideReason !== undefined
        ? { selfCiteOverrideReason: opts.selfCiteOverrideReason }
        : {}),
    });
    if (!check.ok) {
      throw new BadRequestException({
        error: 'Citation list failed validation.',
        items: check.errors,
      });
    }

    return this.prisma.$transaction(async (tx) => {
      // Replace citations atomically — manuscript belongs to one tenant so
      // the deleteMany scope is safe.
      await tx.manuscriptCitation.deleteMany({ where: { manuscriptId } });
      await tx.manuscriptCitation.createMany({
        data: opts.citations.map((c) => ({
          tenantId,
          manuscriptId,
          position: c.position,
          rendered: c.rendered,
          sourceColumnId: c.sourceColumnId ?? null,
          sourceManuscriptId: c.sourceManuscriptId ?? null,
          sourcePatentInsightId: c.sourcePatentInsightId ?? null,
          sourceWatchItemId: c.sourceWatchItemId ?? null,
          externalDoi: c.externalDoi ?? null,
          externalUrl: c.externalUrl ?? null,
        })),
      });
      return tx.researchManuscript.update({
        where: { id: manuscriptId },
        data: {
          state: 'published',
          publishedAt: new Date(),
          plainLanguageSummary: opts.plainLanguageSummary as unknown as Prisma.InputJsonValue,
          frozenCitations: opts.citations as unknown as Prisma.InputJsonValue,
        },
      });
    });
  }
}
