import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import {
  BizPlanService,
  countSources,
  type CreatePlanInput,
  type SectionDraft,
  type SourceRefDraft,
} from './bizplan.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const PLAN = '33333333-3333-3333-3333-333333333333';
const SECTION = '44444444-4444-4444-4444-444444444444';
const FEAS = '55555555-5555-5555-5555-555555555555';
const REV1 = '66666666-6666-6666-6666-666666666666';
const REV2 = '77777777-7777-7777-7777-777777777777';

function planInput(overrides: Partial<CreatePlanInput> = {}): CreatePlanInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    track: 'business',
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '농촌 정수기 보급' } },
    sdgFocus: ['SDG-6'],
    applicableRegions: ['BD'],
    periodMonths: 24,
    noncommercialNotice: true,
    ...overrides,
  };
}

function section(overrides: Partial<SectionDraft> = {}): SectionDraft {
  return {
    position: 1,
    kind: 'problem_statement',
    bodyI18n: { ko: '벵골만 농촌 마을의 정수 시설 부족과 그로 인한 영향을 설명합니다.' },
    plainLanguageScore: 75,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const plan = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: PLAN, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const sec = {
    findFirst: vi.fn().mockResolvedValue(null),
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: SECTION, ...(data as object) }),
    ),
    update: vi.fn(),
  };
  const ref = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  const feas = {
    findFirst: vi.fn(),
  };
  const rev = {
    findMany: vi.fn().mockResolvedValue([]),
  };
  return {
    bizPlan: plan,
    bizPlanSection: sec,
    bizPlanSourceRef: ref,
    bizPlanFeasibility: feas,
    feasibilityReview: rev,
  } as unknown as PrismaService;
}

describe('countSources', () => {
  it('returns 0 with nothing set', () => {
    expect(countSources({ position: 1, rendered: 'x' })).toBe(0);
  });
  it('returns 1 with one source', () => {
    expect(
      countSources({ position: 1, rendered: 'x', sourceColumnId: 'col-1' }),
    ).toBe(1);
  });
  it('returns 2 with two sources', () => {
    expect(
      countSources({
        position: 1,
        rendered: 'x',
        sourceColumnId: 'col-1',
        externalDoi: '10.1000/x',
      }),
    ).toBe(2);
  });
});

describe('BizPlanService.createPlan', () => {
  it('rejects when noncommercialNotice is false', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(svc.createPlan(planInput({ noncommercialNotice: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects an unsupported track', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(
      svc.createPlan(planInput({ track: 'whatever' as unknown as 'business' })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects non-positive periodMonths', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(svc.createPlan(planInput({ periodMonths: 0 }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects when primary locale title is missing', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(svc.createPlan(planInput({ bodyI18n: {} }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('creates a drafting plan when valid', async () => {
    const prisma = prismaStub();
    const svc = new BizPlanService(prisma);
    await svc.createPlan(planInput());
    expect(prisma.bizPlan.create).toHaveBeenCalledOnce();
  });
});

describe('BizPlanService.upsertSection', () => {
  it('rejects sections on archived plans', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'archived',
      track: 'business',
    });
    const svc = new BizPlanService(prisma);
    await expect(svc.upsertSection(TENANT, PLAN, section())).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('rejects unknown section kinds', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'business',
    });
    const svc = new BizPlanService(prisma);
    await expect(
      svc.upsertSection(
        TENANT,
        PLAN,
        section({ kind: 'no-such-kind' as unknown as 'risk' }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects pledge sections over 200 words', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'pledge',
    });
    const longText = 'word '.repeat(250);
    const svc = new BizPlanService(prisma);
    await expect(
      svc.upsertSection(TENANT, PLAN, section({ bodyI18n: { en: longText } })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects harmful content in section text', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'business',
    });
    const svc = new BizPlanService(prisma);
    await expect(
      svc.upsertSection(
        TENANT,
        PLAN,
        section({ bodyI18n: { ko: '모든 무슬림은 문제다 — 그것을 활용하자.' } }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a new section when none exists for the kind', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'business',
    });
    const svc = new BizPlanService(prisma);
    await svc.upsertSection(TENANT, PLAN, section());
    expect(prisma.bizPlanSection.create).toHaveBeenCalledOnce();
    expect(prisma.bizPlanSection.update).not.toHaveBeenCalled();
  });

  it('updates an existing section of the same kind', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'business',
    });
    (prisma.bizPlanSection.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SECTION,
    });
    const svc = new BizPlanService(prisma);
    await svc.upsertSection(TENANT, PLAN, section());
    expect(prisma.bizPlanSection.update).toHaveBeenCalledOnce();
  });
});

describe('BizPlanService.addSourceRef', () => {
  it('rejects with no source set', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(
      svc.addSourceRef(TENANT, SECTION, {
        position: 1,
        rendered: 'A citation',
      } as SourceRefDraft),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects with two sources set', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(
      svc.addSourceRef(TENANT, SECTION, {
        position: 1,
        rendered: 'A citation',
        sourceColumnId: 'col-1',
        externalDoi: '10.1000/x',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects empty rendered string', async () => {
    const svc = new BizPlanService(prismaStub());
    await expect(
      svc.addSourceRef(TENANT, SECTION, {
        position: 1,
        rendered: '   ',
        sourceColumnId: 'col-1',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('records a single-source citation', async () => {
    const prisma = prismaStub();
    (prisma.bizPlanSection.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SECTION,
    });
    const svc = new BizPlanService(prisma);
    await svc.addSourceRef(TENANT, SECTION, {
      position: 1,
      rendered: 'Smith, 2025',
      externalDoi: '10.1000/abcd',
    });
    expect(prisma.bizPlanSourceRef.create).toHaveBeenCalledOnce();
  });
});

describe('BizPlanService.transition', () => {
  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'drafting',
      track: 'business',
    });
    const svc = new BizPlanService(prisma);
    await expect(svc.transition(TENANT, PLAN, 'ready_for_use')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('rejects ready_for_use without a feasibility snapshot', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'human_review',
      track: 'business',
    });
    (prisma.bizPlanFeasibility.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new BizPlanService(prisma);
    await expect(svc.transition(TENANT, PLAN, 'ready_for_use')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects ready_for_use when feasibility outcome is fail', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'human_review',
      track: 'business',
    });
    (prisma.bizPlanFeasibility.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: FEAS,
      outcome: 'fail',
    });
    const svc = new BizPlanService(prisma);
    await expect(svc.transition(TENANT, PLAN, 'ready_for_use')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('ODA track needs ≥ 2 approvals incl. domain expert', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'human_review',
      track: 'oda',
    });
    (prisma.bizPlanFeasibility.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: FEAS,
      outcome: 'pass',
    });
    (prisma.feasibilityReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REV1, decision: 'approve', domainExpert: false },
    ]);
    const svc = new BizPlanService(prisma);
    await expect(svc.transition(TENANT, PLAN, 'ready_for_use')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('ODA track passes with 2 approvals incl. ≥1 domain expert', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'human_review',
      track: 'oda',
    });
    (prisma.bizPlanFeasibility.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: FEAS,
      outcome: 'pass',
    });
    (prisma.feasibilityReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REV1, decision: 'approve', domainExpert: true },
      { reviewerId: REV2, decision: 'approve', domainExpert: false },
    ]);
    (prisma.bizPlan.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'ready_for_use',
    });
    const svc = new BizPlanService(prisma);
    const out = (await svc.transition(TENANT, PLAN, 'ready_for_use')) as { state: string };
    expect(out.state).toBe('ready_for_use');
  });

  it('non-ODA track skips the 2-reviewer rule', async () => {
    const prisma = prismaStub();
    (prisma.bizPlan.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'human_review',
      track: 'business',
    });
    (prisma.bizPlanFeasibility.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: FEAS,
      outcome: 'pass',
    });
    (prisma.bizPlan.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLAN,
      state: 'ready_for_use',
    });
    const svc = new BizPlanService(prisma);
    const out = (await svc.transition(TENANT, PLAN, 'ready_for_use')) as { state: string };
    expect(out.state).toBe('ready_for_use');
  });
});
