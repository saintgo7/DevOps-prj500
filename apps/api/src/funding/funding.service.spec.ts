import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { FundingService, type CreateProposalInput } from './funding.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const PROP = '33333333-3333-3333-3333-333333333333';
const ACTOR = '44444444-4444-4444-4444-444444444444';
const BACKER = '55555555-5555-5555-5555-555555555555';
const CONTRIB = '66666666-6666-6666-6666-666666666666';

function input(overrides: Partial<CreateProposalInput> = {}): CreateProposalInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    primaryLocale: 'ko',
    bodyI18n: {
      ko: {
        title: '저전력 정수기 100대',
        summary: '벵골 만 농촌 마을 100가구에 무동력 정수기 보급.',
        plan: '현지 NGO와 함께 6개월간 설치·교육·점검을 실시.',
      },
    },
    sdgFocus: ['SDG-6'],
    region: 'BD',
    fundingModel: 'all-or-nothing',
    contributionKinds: ['donation'],
    softGoalMinor: 500_000,
    hardGoalMinor: 1_000_000,
    endsAt: new Date(Date.now() + 30 * 86400_000),
    noncommercialNotice: true,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const proposal = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: PROP, ...(data as object) })),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const milestone = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    count: vi.fn().mockResolvedValue(0),
  };
  const contribution = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: CONTRIB, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const flag = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  return {
    fundingProposal: proposal,
    fundingMilestone: milestone,
    fundingContribution: contribution,
    fundingFlag: flag,
    $transaction: vi.fn(async (fn: (tx: unknown) => Promise<unknown>) =>
      fn({
        fundingProposal: proposal,
        fundingMilestone: milestone,
        fundingContribution: contribution,
      }),
    ),
  } as unknown as PrismaService;
}

describe('FundingService.createProposal', () => {
  it('rejects when noncommercialNotice is false', async () => {
    const svc = new FundingService(prismaStub());
    await expect(svc.createProposal(input({ noncommercialNotice: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects soft > hard goals', async () => {
    const svc = new FundingService(prismaStub());
    await expect(
      svc.createProposal(input({ softGoalMinor: 9_999_999 })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects past endsAt', async () => {
    const svc = new FundingService(prismaStub());
    await expect(
      svc.createProposal(input({ endsAt: new Date(Date.now() - 86400_000) })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when contributionKinds is empty', async () => {
    const svc = new FundingService(prismaStub());
    await expect(
      svc.createProposal(input({ contributionKinds: [] })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects harmful body content', async () => {
    const svc = new FundingService(prismaStub());
    await expect(
      svc.createProposal(
        input({
          bodyI18n: {
            ko: {
              title: '계획',
              summary: '모든 무슬림은 문제다 — 그것을 활용하자.',
              plan: '진행',
            },
          },
        }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a draft when valid', async () => {
    const prisma = prismaStub();
    const svc = new FundingService(prisma);
    const out = await svc.createProposal(input());
    expect(out).toBeDefined();
    expect(prisma.fundingProposal.create).toHaveBeenCalledOnce();
  });
});

describe('FundingService.transition', () => {
  it('rejects illegal transitions', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'draft',
      noncommercialNotice: true,
    });
    const svc = new FundingService(prisma);
    await expect(svc.transition(TENANT, PROP, 'completed', ACTOR)).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('rejects going live without milestones', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'review',
      noncommercialNotice: true,
    });
    (prisma.fundingMilestone.count as ReturnType<typeof vi.fn>).mockResolvedValue(0);
    const svc = new FundingService(prisma);
    await expect(svc.transition(TENANT, PROP, 'live', ACTOR)).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('goes live when milestones exist and notice is set', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'review',
      noncommercialNotice: true,
    });
    (prisma.fundingMilestone.count as ReturnType<typeof vi.fn>).mockResolvedValue(2);
    (prisma.fundingProposal.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
    });
    const svc = new FundingService(prisma);
    const out = (await svc.transition(TENANT, PROP, 'live', ACTOR)) as { state: string };
    expect(out.state).toBe('live');
  });
});

describe('FundingService.contribute', () => {
  it('rejects contribution to a non-live proposal', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'draft',
      contributionKinds: ['donation'],
      currency: 'USD',
      hardGoalMinor: 100_000,
    });
    const svc = new FundingService(prisma);
    await expect(
      svc.contribute({
        tenantId: TENANT,
        proposalId: PROP,
        backerUserId: BACKER,
        kind: 'donation',
        amountMinor: 1000,
        currency: 'USD',
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects mismatched currency', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
      contributionKinds: ['donation'],
      currency: 'USD',
      hardGoalMinor: 100_000,
    });
    const svc = new FundingService(prisma);
    await expect(
      svc.contribute({
        tenantId: TENANT,
        proposalId: PROP,
        kind: 'donation',
        amountMinor: 1000,
        currency: 'KRW',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects a contribution above the 25% single-contributor cap', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
      contributionKinds: ['donation'],
      currency: 'USD',
      hardGoalMinor: 100_000,
    });
    const svc = new FundingService(prisma);
    await expect(
      svc.contribute({
        tenantId: TENANT,
        proposalId: PROP,
        kind: 'donation',
        amountMinor: 30_000, // > 25%
        currency: 'USD',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects a contribution kind not allowed by the proposal', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
      contributionKinds: ['donation'],
      currency: 'USD',
      hardGoalMinor: 100_000,
    });
    const svc = new FundingService(prisma);
    await expect(
      svc.contribute({
        tenantId: TENANT,
        proposalId: PROP,
        kind: 'impact-investment',
        amountMinor: 1000,
        currency: 'USD',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('records a valid pending contribution', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
      contributionKinds: ['donation'],
      currency: 'USD',
      hardGoalMinor: 100_000,
    });
    const svc = new FundingService(prisma);
    await svc.contribute({
      tenantId: TENANT,
      proposalId: PROP,
      kind: 'donation',
      amountMinor: 1000,
      currency: 'USD',
    });
    expect(prisma.fundingContribution.create).toHaveBeenCalledOnce();
  });
});

describe('FundingService.confirmCollected', () => {
  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.fundingContribution.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new FundingService(prisma);
    await expect(svc.confirmCollected(TENANT, CONTRIB)).rejects.toBeInstanceOf(NotFoundException);
  });

  it('rejects double-collect', async () => {
    const prisma = prismaStub();
    (prisma.fundingContribution.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: CONTRIB,
      proposalId: PROP,
      amountMinor: 1000,
      state: 'collected',
    });
    const svc = new FundingService(prisma);
    await expect(svc.confirmCollected(TENANT, CONTRIB)).rejects.toBeInstanceOf(ConflictException);
  });

  it('flips pending → collected and bumps tally', async () => {
    const prisma = prismaStub();
    (prisma.fundingContribution.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: CONTRIB,
      proposalId: PROP,
      amountMinor: 1000,
      state: 'pending',
    });
    (prisma.fundingContribution.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: CONTRIB,
      state: 'collected',
    });
    const svc = new FundingService(prisma);
    await svc.confirmCollected(TENANT, CONTRIB);
    expect(prisma.fundingContribution.update).toHaveBeenCalledOnce();
    expect(prisma.fundingProposal.update).toHaveBeenCalledOnce();
  });
});

describe('FundingService.pause', () => {
  it('rejects a short reason', async () => {
    const svc = new FundingService(prismaStub());
    await expect(svc.pause(TENANT, PROP, ACTOR, 'too short')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects pausing a non-live proposal', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'draft',
    });
    const svc = new FundingService(prisma);
    await expect(
      svc.pause(TENANT, PROP, ACTOR, 'A long enough reason for pausing the live proposal here.'),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('pauses a live proposal', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
    });
    (prisma.fundingProposal.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'paused',
    });
    const svc = new FundingService(prisma);
    const out = (await svc.pause(
      TENANT,
      PROP,
      ACTOR,
      'A long enough reason for pausing the live proposal here.',
    )) as { state: string };
    expect(out.state).toBe('paused');
  });
});

describe('FundingService.flag', () => {
  it('rejects a short reason', async () => {
    const svc = new FundingService(prismaStub());
    await expect(svc.flag(TENANT, PROP, BACKER, 'fraud', 'short')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('records a flag', async () => {
    const prisma = prismaStub();
    (prisma.fundingProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'live',
    });
    const svc = new FundingService(prisma);
    await svc.flag(
      TENANT,
      PROP,
      BACKER,
      'fraud',
      'Looks like a duplicate of an off-platform scam — see linked discussion.',
    );
    expect(prisma.fundingFlag.create).toHaveBeenCalledOnce();
  });
});
