import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { ManuscriptsService, type CreateManuscriptInput } from './manuscripts.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const MS = '33333333-3333-3333-3333-333333333333';
const OTHER = '44444444-4444-4444-4444-444444444444';

function input(overrides: Partial<CreateManuscriptInput> = {}): CreateManuscriptInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    tier: 'nature',
    primaryLocale: 'ko',
    bodyI18n: {
      ko: { title: '저전력 정수기와 SDG 6', scientificAbstract: '본 논문은…' },
    },
    sdgFocus: ['SDG-6'],
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const manuscript = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: MS, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const citation = {
    deleteMany: vi.fn().mockResolvedValue({ count: 0 }),
    createMany: vi.fn().mockResolvedValue({ count: 0 }),
  };
  return {
    researchManuscript: manuscript,
    manuscriptCitation: citation,
    $transaction: vi.fn(async (fn: (tx: unknown) => Promise<unknown>) =>
      fn({ researchManuscript: manuscript, manuscriptCitation: citation }),
    ),
  } as unknown as PrismaService;
}

describe('ManuscriptsService.canTransition', () => {
  it('allows draft → internal_review', () => {
    expect(ManuscriptsService.canTransition('draft', 'internal_review')).toBe(true);
  });
  it('forbids draft → published', () => {
    expect(ManuscriptsService.canTransition('draft', 'published')).toBe(false);
  });
  it('forbids any transition out of withdrawn', () => {
    expect(ManuscriptsService.canTransition('withdrawn', 'draft')).toBe(false);
  });
  it('allows accepted → published', () => {
    expect(ManuscriptsService.canTransition('accepted', 'published')).toBe(true);
  });
});

describe('ManuscriptsService.create', () => {
  it('rejects an unsupported tier', async () => {
    const svc = new ManuscriptsService(prismaStub());
    await expect(
      // @ts-expect-error testing runtime guard
      svc.create(input({ tier: 'blog' })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects when primary locale body is missing', async () => {
    const svc = new ManuscriptsService(prismaStub());
    await expect(svc.create(input({ bodyI18n: {} }))).rejects.toBeInstanceOf(BadRequestException);
  });
  it('creates a draft manuscript when valid', async () => {
    const prisma = prismaStub();
    const svc = new ManuscriptsService(prisma);
    const out = await svc.create(input());
    expect(out).toBeDefined();
    expect(prisma.researchManuscript.create).toHaveBeenCalledOnce();
  });
});

describe('ManuscriptsService.transition', () => {
  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'draft',
    });
    const svc = new ManuscriptsService(prisma);
    await expect(svc.transition(TENANT, MS, 'published')).rejects.toBeInstanceOf(ConflictException);
  });
  it('errors with NotFound when manuscript missing', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new ManuscriptsService(prisma);
    await expect(svc.transition(TENANT, MS, 'internal_review')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });
});

describe('ManuscriptsService.publish', () => {
  it('rejects publishing when not accepted', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'draft',
      primaryLocale: 'ko',
    });
    const svc = new ManuscriptsService(prisma);
    await expect(
      svc.publish(TENANT, MS, {
        citations: [{ position: 1, rendered: 'a', externalDoi: '10/a' }],
        plainLanguageSummary: { en: 'x', ko: 'x' },
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects publishing without plain-language summary in primary locale', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'accepted',
      primaryLocale: 'ko',
    });
    const svc = new ManuscriptsService(prisma);
    await expect(
      svc.publish(TENANT, MS, {
        citations: [{ position: 1, rendered: 'a', externalDoi: '10/a' }],
        plainLanguageSummary: { en: 'only english here' },
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects publishing with bad citations', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'accepted',
      primaryLocale: 'ko',
    });
    const svc = new ManuscriptsService(prisma);
    await expect(
      svc.publish(TENANT, MS, {
        citations: [{ position: 1, rendered: '' }], // empty + no source
        plainLanguageSummary: { en: 'x', ko: 'x' },
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('publishes an accepted manuscript and freezes citations', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'accepted',
      primaryLocale: 'ko',
    });
    (prisma.researchManuscript.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'published',
    });
    const svc = new ManuscriptsService(prisma);
    const out = (await svc.publish(TENANT, MS, {
      citations: [
        { position: 1, rendered: 'A', externalDoi: '10/a' },
        { position: 2, rendered: 'B', sourceColumnId: OTHER },
      ],
      plainLanguageSummary: { en: 'plain en', ko: '평이한 한국어 요약' },
    })) as { state: string };
    expect(out.state).toBe('published');
    expect(prisma.manuscriptCitation.createMany).toHaveBeenCalled();
  });
});

describe('ManuscriptsService.withdraw', () => {
  it('rejects a short reason', async () => {
    const svc = new ManuscriptsService(prismaStub());
    await expect(svc.withdraw(TENANT, MS, 'oops')).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects a double-withdraw', async () => {
    const prisma = prismaStub();
    (prisma.researchManuscript.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MS,
      state: 'withdrawn',
    });
    const svc = new ManuscriptsService(prisma);
    await expect(
      svc.withdraw(TENANT, MS, 'reason long enough'),
    ).rejects.toBeInstanceOf(ConflictException);
  });
});
