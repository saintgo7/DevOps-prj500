// Book authoring — re-uses already-curated content (ADR-0017 §B).
//
// Hard rule: each chapter has exactly one source. The DB CHECK enforces the
// invariant; the service surfaces a friendly error before the round-trip.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type BookState = 'draft' | 'review' | 'published' | 'retired';

export interface CreateBookInput {
  tenantId: string;
  ownerId: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; subtitle?: string; blurb?: string }>;
  sdgFocus: string[];
  applicableRegions?: string[];
  license?: string;
}

export interface ChapterDraft {
  position: number;
  headerI18n: Record<string, { title: string; lead?: string }>;
  sourceColumnId?: string;
  sourceManuscriptId?: string;
  sourceShortStoryId?: string;
  sourceWatchDigestId?: string;
  sourceCustom?: string;
  sourceCustomReason?: string;
  plainLanguageScore?: number;
}

const ALLOWED_TRANSITIONS: Record<BookState, BookState[]> = {
  draft: ['review', 'retired'],
  review: ['draft', 'published', 'retired'],
  published: ['retired'],
  retired: [],
};

function countChapterSources(c: ChapterDraft): number {
  return (
    (c.sourceColumnId ? 1 : 0) +
    (c.sourceManuscriptId ? 1 : 0) +
    (c.sourceShortStoryId ? 1 : 0) +
    (c.sourceWatchDigestId ? 1 : 0) +
    (c.sourceCustom ? 1 : 0)
  );
}

@Injectable()
export class BooksService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: BookState, to: BookState): boolean {
    return ALLOWED_TRANSITIONS[from].includes(to);
  }

  async create(input: CreateBookInput) {
    if (!input.bodyI18n[input.primaryLocale]?.title) {
      throw new BadRequestException(
        `Book needs a title in the primary locale (${input.primaryLocale}).`,
      );
    }
    return this.prisma.bookProject.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        applicableRegions: input.applicableRegions ?? [],
        license: input.license ?? 'CC-BY-NC-SA-4.0',
        state: 'draft',
      },
    });
  }

  async addChapter(tenantId: string, bookId: string, draft: ChapterDraft) {
    const sources = countChapterSources(draft);
    if (sources !== 1) {
      throw new BadRequestException(
        `Each chapter must reference exactly one source — got ${sources}. ` +
          `Pick one of: source column / manuscript / short story / watch digest / custom.`,
      );
    }
    if (draft.sourceCustom && (!draft.sourceCustomReason || draft.sourceCustomReason.trim().length === 0)) {
      throw new BadRequestException(
        'Free-form chapters require a sourceCustomReason explaining why no curated source fit.',
      );
    }
    if (
      draft.plainLanguageScore !== undefined &&
      (draft.plainLanguageScore < 0 || draft.plainLanguageScore > 100)
    ) {
      throw new BadRequestException('plainLanguageScore must be between 0 and 100.');
    }
    const book = await this.prisma.bookProject.findFirst({
      where: { id: bookId, tenantId },
    });
    if (!book) throw new NotFoundException('Book not found.');
    if (book.state !== 'draft' && book.state !== 'review') {
      throw new ConflictException(
        `Cannot add chapters to a book in state '${book.state}'.`,
      );
    }
    return this.prisma.bookChapter.create({
      data: {
        tenantId,
        bookId,
        position: draft.position,
        headerI18n: draft.headerI18n as unknown as Prisma.InputJsonValue,
        sourceColumnId: draft.sourceColumnId ?? null,
        sourceManuscriptId: draft.sourceManuscriptId ?? null,
        sourceShortStoryId: draft.sourceShortStoryId ?? null,
        sourceWatchDigestId: draft.sourceWatchDigestId ?? null,
        sourceCustom: draft.sourceCustom ?? null,
        sourceCustomReason: draft.sourceCustomReason ?? null,
        plainLanguageScore: draft.plainLanguageScore ?? null,
      },
    });
  }

  async transition(tenantId: string, bookId: string, to: BookState) {
    const b = await this.prisma.bookProject.findFirst({
      where: { id: bookId, tenantId },
    });
    if (!b) throw new NotFoundException('Book not found.');
    const from = b.state as BookState;
    if (!BooksService.canTransition(from, to)) {
      throw new ConflictException(
        `Book is in state '${from}' — cannot transition to '${to}'.`,
      );
    }
    if (to === 'published') {
      // Plain-language gate: every chapter must score >= 60 (or be flagged as
      // pending). Chapters without a recorded score are blocked at publish.
      const chapters = await this.prisma.bookChapter.findMany({
        where: { tenantId, bookId },
      });
      if (chapters.length === 0) {
        throw new BadRequestException('Cannot publish a book with no chapters.');
      }
      const failing = chapters.filter(
        (c) => c.plainLanguageScore === null || (c.plainLanguageScore ?? 0) < 60,
      );
      if (failing.length > 0) {
        throw new BadRequestException({
          error: 'Some chapters have not passed the plain-language threshold (≥ 60).',
          chapters: failing.map((c) => ({ position: c.position, score: c.plainLanguageScore })),
        });
      }
    }
    return this.prisma.bookProject.update({
      where: { id: bookId },
      data: {
        state: to,
        ...(to === 'published' ? { publishedAt: new Date() } : {}),
      },
    });
  }
}
