import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import {
  ExpertsService,
  scoreExpertForSubject,
  type CreateProfileInput,
} from './experts.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const USER = '22222222-2222-2222-2222-222222222222';
const EXPERT = '33333333-3333-3333-3333-333333333333';
const VERIFIER = '44444444-4444-4444-4444-444444444444';
const MATCH = '55555555-5555-5555-5555-555555555555';
const SUBJECT = '66666666-6666-6666-6666-666666666666';

function profileInput(overrides: Partial<CreateProfileInput> = {}): CreateProfileInput {
  return {
    tenantId: TENANT,
    userId: USER,
    headlineI18n: { ko: '저전력 정수 시스템 엔지니어' },
    sdgFocus: ['SDG-6', 'SDG-13'],
    workingLocales: ['ko', 'en'],
    fieldRegions: ['BD', 'KE'],
    availability: 'open',
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const profile = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: EXPERT, ...(data as object) })),
    findFirst: vi.fn(),
    findMany: vi.fn().mockResolvedValue([]),
  };
  const cred = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  const match = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: MATCH, ...(data as object) }),
    ),
    findFirst: vi.fn().mockResolvedValue(null),
    update: vi.fn(),
  };
  return {
    expertProfile: profile,
    expertCredential: cred,
    expertMatch: match,
  } as unknown as PrismaService;
}

describe('scoreExpertForSubject', () => {
  it('rewards full domain overlap', () => {
    const r = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(r.score).toBeGreaterThanOrEqual(80);
  });

  it('penalises closed availability', () => {
    const open = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    const closed = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'closed',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(closed.score).toBeLessThan(open.score);
  });

  it('rewards LDC subject + LDC field experience', () => {
    const ldc = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    const non = scoreExpertForSubject(
      {
        id: 'e2',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['KR'],
        availability: 'open',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['KR'] },
    );
    expect(ldc.score).toBeGreaterThan(non.score);
  });

  it('returns reasons array', () => {
    const r = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(r.reasons.length).toBe(5);
  });

  it('handles empty subject scope without throwing', () => {
    const r = scoreExpertForSubject(
      {
        id: 'e1',
        sdgFocus: [],
        workingLocales: [],
        fieldRegions: [],
        availability: 'open',
      },
      { sdgFocus: [], locales: [], regions: [] },
    );
    expect(r.score).toBeGreaterThanOrEqual(0);
  });
});

describe('ExpertsService.createProfile', () => {
  it('rejects without a headline', async () => {
    const svc = new ExpertsService(prismaStub());
    await expect(svc.createProfile(profileInput({ headlineI18n: {} }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects unknown availability', async () => {
    const svc = new ExpertsService(prismaStub());
    await expect(
      svc.createProfile(
        profileInput({ availability: 'whatever' as unknown as 'open' }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a profile with platform-only default visibility', async () => {
    const prisma = prismaStub();
    const svc = new ExpertsService(prisma);
    await svc.createProfile(profileInput());
    const call = (prisma.expertProfile.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { visibility: string };
    };
    expect(call.data.visibility).toBe('platform-only');
  });
});

describe('ExpertsService.addCredential', () => {
  it('rejects self-reporting as verified', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: EXPERT });
    const svc = new ExpertsService(prisma);
    await expect(
      svc.addCredential({
        tenantId: TENANT,
        expertId: EXPERT,
        kind: 'verified',
        ref: 'orcid:0000-0000-0000-0000',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('records a verified credential when verifier is set', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: EXPERT });
    const svc = new ExpertsService(prisma);
    await svc.addCredential({
      tenantId: TENANT,
      expertId: EXPERT,
      kind: 'verified',
      ref: 'orcid:0000-0000-0000-0000',
      verifierId: VERIFIER,
    });
    const call = (prisma.expertCredential.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { kind: string; verifiedBy: string; verifiedAt: Date };
    };
    expect(call.data.verifiedBy).toBe(VERIFIER);
    expect(call.data.verifiedAt).toBeInstanceOf(Date);
  });

  it('rejects empty ref', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: EXPERT });
    const svc = new ExpertsService(prisma);
    await expect(
      svc.addCredential({
        tenantId: TENANT,
        expertId: EXPERT,
        kind: 'orcid',
        ref: '   ',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('errors with NotFound when expert profile is missing', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new ExpertsService(prisma);
    await expect(
      svc.addCredential({
        tenantId: TENANT,
        expertId: EXPERT,
        kind: 'orcid',
        ref: '0000-0000-0000-0000',
      }),
    ).rejects.toBeInstanceOf(NotFoundException);
  });
});

describe('ExpertsService.suggestMatches', () => {
  it('returns empty when no experts exist', async () => {
    const prisma = prismaStub();
    const svc = new ExpertsService(prisma);
    const out = await svc.suggestMatches(
      TENANT,
      { kind: 'bizplan', id: SUBJECT },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(out).toEqual([]);
  });

  it('skips closed-availability experts', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      {
        id: EXPERT,
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
    ]);
    const svc = new ExpertsService(prisma);
    await svc.suggestMatches(
      TENANT,
      { kind: 'bizplan', id: SUBJECT },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    // closed-availability experts are filtered at the DB query level — we
    // verify findMany was scoped to open/busy.
    const call = (prisma.expertProfile.findMany as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      where: { availability: { in: string[] } };
    };
    expect(call.where.availability.in).toEqual(['open', 'busy']);
  });

  it('does not duplicate an existing match', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      {
        id: EXPERT,
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
    ]);
    (prisma.expertMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: MATCH });
    const svc = new ExpertsService(prisma);
    const out = await svc.suggestMatches(
      TENANT,
      { kind: 'bizplan', id: SUBJECT },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(out).toEqual([]);
    expect(prisma.expertMatch.create).not.toHaveBeenCalled();
  });

  it('creates a suggestion for each new candidate', async () => {
    const prisma = prismaStub();
    (prisma.expertProfile.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      {
        id: EXPERT,
        sdgFocus: ['SDG-6'],
        workingLocales: ['en'],
        fieldRegions: ['BD'],
        availability: 'open',
      },
    ]);
    const svc = new ExpertsService(prisma);
    const out = await svc.suggestMatches(
      TENANT,
      { kind: 'bizplan', id: SUBJECT },
      { sdgFocus: ['SDG-6'], locales: ['en'], regions: ['BD'] },
    );
    expect(out).toHaveLength(1);
    expect(prisma.expertMatch.create).toHaveBeenCalledOnce();
  });
});

describe('ExpertsService.accept', () => {
  it('moves to invited on first one-sided accept', async () => {
    const prisma = prismaStub();
    (prisma.expertMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'suggested',
      expertAcceptedAt: null,
      ownerAcceptedAt: null,
    });
    const svc = new ExpertsService(prisma);
    await svc.accept(TENANT, MATCH, 'expert');
    const call = (prisma.expertMatch.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string; expertAcceptedAt?: Date };
    };
    expect(call.data.state).toBe('invited');
  });

  it('moves to accepted when both sides have accepted', async () => {
    const prisma = prismaStub();
    (prisma.expertMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'invited',
      expertAcceptedAt: null,
      ownerAcceptedAt: new Date(),
    });
    const svc = new ExpertsService(prisma);
    await svc.accept(TENANT, MATCH, 'expert');
    const call = (prisma.expertMatch.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string };
    };
    expect(call.data.state).toBe('accepted');
  });

  it('rejects double-accept from the same side', async () => {
    const prisma = prismaStub();
    (prisma.expertMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'invited',
      expertAcceptedAt: new Date(),
      ownerAcceptedAt: null,
    });
    const svc = new ExpertsService(prisma);
    await expect(svc.accept(TENANT, MATCH, 'expert')).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects accept once cancelled or completed', async () => {
    const prisma = prismaStub();
    (prisma.expertMatch.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: MATCH,
      state: 'cancelled',
    });
    const svc = new ExpertsService(prisma);
    await expect(svc.accept(TENANT, MATCH, 'expert')).rejects.toBeInstanceOf(ConflictException);
  });
});

describe('ExpertsService.maskIfNotAccepted', () => {
  it('masks contact when not accepted', () => {
    const out = ExpertsService.maskIfNotAccepted(
      { email: 'e@example.com', phoneE164: '+10000000000' },
      false,
    );
    expect(out.email).toBeNull();
    expect(out.phoneE164).toBeNull();
  });

  it('passes through when accepted', () => {
    const out = ExpertsService.maskIfNotAccepted(
      { email: 'e@example.com', phoneE164: '+10000000000' },
      true,
    );
    expect(out.email).toBe('e@example.com');
    expect(out.phoneE164).toBe('+10000000000');
  });
});
