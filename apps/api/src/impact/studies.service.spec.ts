import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { StudiesService, type CreateStudyInput } from './studies.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const STUDY = '33333333-3333-3333-3333-333333333333';
const REVIEWER1 = '44444444-4444-4444-4444-444444444444';
const REVIEWER2 = '55555555-5555-5555-5555-555555555555';

function input(overrides: Partial<CreateStudyInput> = {}): CreateStudyInput {
  const start = new Date('2026-01-01T00:00:00Z');
  const end = new Date('2026-04-01T00:00:00Z');
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    title: 'Water access in BD subdistricts',
    hypothesis: 'Filter availability correlates with reported diarrhea drop.',
    method: 'rate',
    sdgFocus: ['SDG-6'],
    regions: ['BD'],
    topicTags: ['water'],
    windowStart: start,
    windowEnd: end,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const study = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: STUDY, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const review = {
    findMany: vi.fn().mockResolvedValue([]),
  };
  const obs = {
    findMany: vi.fn().mockResolvedValue([]),
    update: vi.fn(),
  };
  const disclosure = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  return {
    impactStudy: study,
    impactStudyReview: review,
    impactObservation: obs,
    impactDisclosure: disclosure,
    $transaction: vi.fn(async (fn: (tx: unknown) => Promise<unknown>) =>
      fn({
        impactStudy: study,
        impactStudyReview: review,
        impactObservation: obs,
      }),
    ),
  } as unknown as PrismaService;
}

describe('StudiesService.create', () => {
  it('rejects when window is empty / inverted', async () => {
    const svc = new StudiesService(prismaStub());
    const start = new Date('2026-04-01');
    const end = new Date('2026-01-01');
    await expect(svc.create(input({ windowStart: start, windowEnd: end }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects when sdgFocus is empty', async () => {
    const svc = new StudiesService(prismaStub());
    await expect(svc.create(input({ sdgFocus: [] }))).rejects.toBeInstanceOf(BadRequestException);
  });

  it('uses k=10 floor for ordinary studies', async () => {
    const prisma = prismaStub();
    const svc = new StudiesService(prisma);
    await svc.create(input());
    const call = (prisma.impactStudy.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { kAnonymityFloor: number };
    };
    expect(call.data.kAnonymityFloor).toBe(10);
  });

  it('forces k=25 floor for sensitive topics', async () => {
    const prisma = prismaStub();
    const svc = new StudiesService(prisma);
    await svc.create(input({ sensitiveTopic: true }));
    const call = (prisma.impactStudy.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { kAnonymityFloor: number };
    };
    expect(call.data.kAnonymityFloor).toBe(25);
  });
});

describe('StudiesService.transition', () => {
  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'draft',
    });
    const svc = new StudiesService(prisma);
    await expect(svc.transition(TENANT, STUDY, 'published')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });
});

describe('StudiesService.publish', () => {
  it('rejects publishing when not in review state', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'analysing',
      kAnonymityFloor: 10,
    });
    const svc = new StudiesService(prisma);
    await expect(svc.publish(TENANT, STUDY)).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects publishing without 2 approvals', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'review',
      kAnonymityFloor: 10,
    });
    (prisma.impactStudyReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REVIEWER1, decision: 'approve', domainExpert: true },
    ]);
    const svc = new StudiesService(prisma);
    await expect(svc.publish(TENANT, STUDY)).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects publishing without a domain-expert approver', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'review',
      kAnonymityFloor: 10,
    });
    (prisma.impactStudyReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REVIEWER1, decision: 'approve', domainExpert: false },
      { reviewerId: REVIEWER2, decision: 'approve', domainExpert: false },
    ]);
    const svc = new StudiesService(prisma);
    await expect(svc.publish(TENANT, STUDY)).rejects.toBeInstanceOf(ConflictException);
  });

  it('refuses publish when every cohort is below the floor', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'review',
      kAnonymityFloor: 10,
    });
    (prisma.impactStudyReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REVIEWER1, decision: 'approve', domainExpert: true },
      { reviewerId: REVIEWER2, decision: 'approve', domainExpert: false },
    ]);
    (prisma.impactObservation.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { id: 'o1', cohortSize: 4 },
      { id: 'o2', cohortSize: 7 },
    ]);
    const svc = new StudiesService(prisma);
    await expect(svc.publish(TENANT, STUDY)).rejects.toBeInstanceOf(ConflictException);
  });

  it('publishes a study and suppresses small cohorts', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'review',
      kAnonymityFloor: 10,
    });
    (prisma.impactStudyReview.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { reviewerId: REVIEWER1, decision: 'approve', domainExpert: true },
      { reviewerId: REVIEWER2, decision: 'approve', domainExpert: false },
    ]);
    (prisma.impactObservation.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { id: 'o-big', cohortSize: 20 },
      { id: 'o-small', cohortSize: 4 },
    ]);
    (prisma.impactStudy.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'published',
    });
    const svc = new StudiesService(prisma);
    const out = (await svc.publish(TENANT, STUDY)) as { state: string };
    expect(out.state).toBe('published');
    // Both observations get an update — one release-ready, one suppressed.
    expect(prisma.impactObservation.update).toHaveBeenCalledTimes(2);
    const calls = (prisma.impactObservation.update as ReturnType<typeof vi.fn>).mock.calls as Array<
      [{ where: { id: string }; data: { releaseReady: boolean; suppressed: boolean } }]
    >;
    const big = calls.find((c) => c[0].where.id === 'o-big');
    const small = calls.find((c) => c[0].where.id === 'o-small');
    expect(big?.[0].data).toEqual({ releaseReady: true, suppressed: false });
    expect(small?.[0].data).toEqual({ releaseReady: false, suppressed: true });
  });
});

describe('StudiesService.disclose', () => {
  it('rejects disclosure of an unpublished study', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'review',
    });
    const svc = new StudiesService(prisma);
    await expect(svc.disclose(TENANT, STUDY, 'atom')).rejects.toBeInstanceOf(ConflictException);
  });

  it('errors with NotFound when study is missing', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new StudiesService(prisma);
    await expect(svc.disclose(TENANT, STUDY, 'atom')).rejects.toBeInstanceOf(NotFoundException);
  });

  it('records a disclosure for a published study', async () => {
    const prisma = prismaStub();
    (prisma.impactStudy.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: STUDY,
      state: 'published',
    });
    const svc = new StudiesService(prisma);
    await svc.disclose(TENANT, STUDY, 'webhook', 'partner-foo');
    expect(prisma.impactDisclosure.create).toHaveBeenCalledOnce();
  });
});
