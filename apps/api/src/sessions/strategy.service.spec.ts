import { describe, expect, it, vi } from 'vitest';
import {
  BadRequestException,
  ConflictException,
  ForbiddenException,
  NotFoundException,
} from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { StrategyService, type CreateSessionInput } from './strategy.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const INSIGHT = '33333333-3333-3333-3333-333333333333';
const SUPER = '44444444-4444-4444-4444-444444444444';
const SESSION = '55555555-5555-5555-5555-555555555555';
const INVITE = '66666666-6666-6666-6666-666666666666';

function input(overrides: Partial<CreateSessionInput> = {}): CreateSessionInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    insightId: INSIGHT,
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '저렴한 정수 필터', plan: '시범 적용 계획.', riskNote: '없음.' } },
    sdgFocus: ['SDG-6'],
    noncommercialNotice: true,
    ...overrides,
  };
}

function approvedInsightPrisma(): PrismaService {
  const strategySession = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: SESSION, ...(data as object) })),
    findFirst: vi.fn(),
    update: vi.fn().mockResolvedValue({ id: SESSION }),
  };
  const sessionInvite = {
    create: vi.fn(),
    findFirst: vi.fn(),
    update: vi.fn(),
    updateMany: vi.fn().mockResolvedValue({ count: 0 }),
  };
  return {
    patentInsight: {
      findFirst: vi.fn().mockResolvedValue({ id: INSIGHT, state: 'approved' }),
    },
    strategySession,
    sessionInvite,
    // The mocked transaction passes a tx that proxies through to the
    // top-level mocks so calls inside the transaction body are observable
    // (the revoke test below asserts updateMany was invoked).
    $transaction: vi.fn(async (fn: (tx: unknown) => Promise<unknown>) =>
      fn({ strategySession, sessionInvite }),
    ),
  } as unknown as PrismaService;
}

describe('StrategyService.create', () => {
  it('rejects when noncommercialNotice is false', async () => {
    const svc = new StrategyService(approvedInsightPrisma());
    await expect(svc.create(input({ noncommercialNotice: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects when the body contains harmful content', async () => {
    const svc = new StrategyService(approvedInsightPrisma());
    await expect(
      svc.create(
        input({
          bodyI18n: {
            ko: { title: '계획', plan: '모든 무슬림은 문제다 — 그것을 활용하자.' },
          },
        }),
      ),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when the patent insight does not exist', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.patentInsight.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new StrategyService(prisma);
    await expect(svc.create(input())).rejects.toBeInstanceOf(NotFoundException);
  });

  it('rejects when the insight is still in draft', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.patentInsight.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: INSIGHT,
      state: 'draft',
    });
    const svc = new StrategyService(prisma);
    await expect(svc.create(input())).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a draft session when all rules pass', async () => {
    const prisma = approvedInsightPrisma();
    const svc = new StrategyService(prisma);
    const out = await svc.create(input());
    expect(out).toBeDefined();
    expect(prisma.strategySession.create).toHaveBeenCalledOnce();
  });
});

describe('StrategyService.approve', () => {
  it('moves draft → invited and stamps approver', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.strategySession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'draft',
      noncommercialNotice: true,
    });
    (prisma.strategySession.update as ReturnType<typeof vi.fn>).mockImplementation(
      ({ data }: { data: unknown }) => Promise.resolve({ id: SESSION, ...(data as object) }),
    );
    const svc = new StrategyService(prisma);
    const out = (await svc.approve(TENANT, SESSION, SUPER)) as { state: string };
    expect(out.state).toBe('invited');
  });

  it('rejects approving a session that is not in draft', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.strategySession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'invited',
      noncommercialNotice: true,
    });
    const svc = new StrategyService(prisma);
    await expect(svc.approve(TENANT, SESSION, SUPER)).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects approving a session missing the non-commercial notice', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.strategySession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'draft',
      noncommercialNotice: false, // would be unusual given DB CHECK, but test defence
    });
    const svc = new StrategyService(prisma);
    await expect(svc.approve(TENANT, SESSION, SUPER)).rejects.toBeInstanceOf(ForbiddenException);
  });
});

describe('StrategyService.revoke', () => {
  it('rejects an empty or short reason', async () => {
    const svc = new StrategyService(approvedInsightPrisma());
    await expect(svc.revoke(TENANT, SESSION, SUPER, '')).rejects.toBeInstanceOf(BadRequestException);
    await expect(svc.revoke(TENANT, SESSION, SUPER, 'short')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('blocks re-revoking an already-revoked session', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.strategySession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'revoked',
    });
    const svc = new StrategyService(prisma);
    await expect(
      svc.revoke(TENANT, SESSION, SUPER, 'duplicate revoke attempt'),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('on revoke, sets state=revoked AND invalidates all outstanding invites', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.strategySession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'invited',
    });
    const svc = new StrategyService(prisma);
    await svc.revoke(TENANT, SESSION, SUPER, 'Concerns about commercial misuse.');
    expect(prisma.strategySession.update).toHaveBeenCalledWith(
      expect.objectContaining({ data: expect.objectContaining({ state: 'revoked' }) }),
    );
    expect(prisma.sessionInvite.updateMany).toHaveBeenCalled();
  });
});

describe('StrategyService.accept', () => {
  it('refuses acceptance without the non-commercial clause text', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.sessionInvite.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: INVITE,
      acceptedAt: null,
      declinedAt: null,
      revokedAt: null,
      expiresAt: new Date(Date.now() + 86400_000),
    });
    const svc = new StrategyService(prisma);
    await expect(svc.accept(TENANT, INVITE, 'I agree to use this stuff.')).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('accepts when the clause includes "non-commercial"', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.sessionInvite.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: INVITE,
      acceptedAt: null,
      declinedAt: null,
      revokedAt: null,
      expiresAt: new Date(Date.now() + 86400_000),
    });
    (prisma.sessionInvite.update as ReturnType<typeof vi.fn>).mockResolvedValue({ id: INVITE });
    const svc = new StrategyService(prisma);
    await expect(
      svc.accept(TENANT, INVITE, 'I agree to non-commercial use only for SDG implementation.'),
    ).resolves.toBeDefined();
  });

  it('refuses acceptance after the invite has expired', async () => {
    const prisma = approvedInsightPrisma();
    (prisma.sessionInvite.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: INVITE,
      acceptedAt: null,
      declinedAt: null,
      revokedAt: null,
      expiresAt: new Date(Date.now() - 86400_000),
    });
    const svc = new StrategyService(prisma);
    await expect(
      svc.accept(TENANT, INVITE, 'I agree to non-commercial use only.'),
    ).rejects.toBeInstanceOf(ConflictException);
  });
});
