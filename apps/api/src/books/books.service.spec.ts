import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { BooksService, type ChapterDraft, type CreateBookInput } from './books.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const BOOK = '33333333-3333-3333-3333-333333333333';
const COLUMN = '44444444-4444-4444-4444-444444444444';
const MS = '55555555-5555-5555-5555-555555555555';

function bookInput(overrides: Partial<CreateBookInput> = {}): CreateBookInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '바람과 비, 그리고 우리의 손' } },
    sdgFocus: ['SDG-13'],
    ...overrides,
  };
}

function chapter(overrides: Partial<ChapterDraft> = {}): ChapterDraft {
  return {
    position: 1,
    headerI18n: { ko: { title: '서장' } },
    sourceColumnId: COLUMN,
    plainLanguageScore: 80,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const book = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: BOOK, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const chapterTable = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    findMany: vi.fn().mockResolvedValue([]),
  };
  return {
    bookProject: book,
    bookChapter: chapterTable,
  } as unknown as PrismaService;
}

describe('BooksService.create', () => {
  it('rejects without primary locale title', async () => {
    const svc = new BooksService(prismaStub());
    await expect(svc.create(bookInput({ bodyI18n: {} }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('creates a book with default license CC-BY-NC-SA-4.0', async () => {
    const prisma = prismaStub();
    const svc = new BooksService(prisma);
    await svc.create(bookInput());
    const call = (prisma.bookProject.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { license: string };
    };
    expect(call.data.license).toBe('CC-BY-NC-SA-4.0');
  });
});

describe('BooksService.addChapter', () => {
  it('rejects when no source is set', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'draft',
    });
    const svc = new BooksService(prisma);
    const noSource: ChapterDraft = {
      position: 1,
      headerI18n: { ko: { title: '서장' } },
      plainLanguageScore: 80,
    };
    await expect(svc.addChapter(TENANT, BOOK, noSource)).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects when two sources are set', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'draft',
    });
    const svc = new BooksService(prisma);
    await expect(
      svc.addChapter(
        TENANT,
        BOOK,
        chapter({ sourceColumnId: COLUMN, sourceManuscriptId: MS }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects custom-source chapter without a reason', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'draft',
    });
    const svc = new BooksService(prisma);
    const customNoReason: ChapterDraft = {
      position: 1,
      headerI18n: { ko: { title: '서장' } },
      sourceCustom: 'free text',
    };
    await expect(svc.addChapter(TENANT, BOOK, customNoReason)).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects adding chapters to a published book', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'published',
    });
    const svc = new BooksService(prisma);
    await expect(svc.addChapter(TENANT, BOOK, chapter())).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('accepts a chapter with one curated source', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'draft',
    });
    const svc = new BooksService(prisma);
    await svc.addChapter(TENANT, BOOK, chapter());
    expect(prisma.bookChapter.create).toHaveBeenCalledOnce();
  });
});

describe('BooksService.transition', () => {
  it('rejects publish when chapter plain-language score is below 60', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'review',
    });
    (prisma.bookChapter.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { position: 1, plainLanguageScore: 70 },
      { position: 2, plainLanguageScore: 40 },
    ]);
    const svc = new BooksService(prisma);
    await expect(svc.transition(TENANT, BOOK, 'published')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects publish when no chapters exist', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'review',
    });
    (prisma.bookChapter.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([]);
    const svc = new BooksService(prisma);
    await expect(svc.transition(TENANT, BOOK, 'published')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('publishes when every chapter scores >= 60', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'review',
    });
    (prisma.bookChapter.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { position: 1, plainLanguageScore: 80 },
      { position: 2, plainLanguageScore: 90 },
    ]);
    (prisma.bookProject.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'published',
    });
    const svc = new BooksService(prisma);
    const out = (await svc.transition(TENANT, BOOK, 'published')) as { state: string };
    expect(out.state).toBe('published');
  });

  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.bookProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: BOOK,
      state: 'draft',
    });
    const svc = new BooksService(prisma);
    await expect(svc.transition(TENANT, BOOK, 'published')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });
});
