import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { ConsentService, type ConsentLevel } from './consent.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const USER = '22222222-2222-2222-2222-222222222222';
const REC = '33333333-3333-3333-3333-333333333333';

const FULL_CLAUSE =
  'I agree to anonymous, aggregate-only inclusion of my engagement signals in SDG impact studies.';

function prismaStub(): PrismaService {
  const consent = {
    findFirst: vi.fn(),
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: REC, ...(data as object) }),
    ),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: REC, ...(data as object) }),
    ),
  };
  return { impactConsentRecord: consent } as unknown as PrismaService;
}

describe('ConsentService.record', () => {
  it('rejects an unsupported level', async () => {
    const svc = new ConsentService(prismaStub());
    await expect(
      svc.record({
        tenantId: TENANT,
        userId: USER,
        scope: {},
        level: 'whatever' as unknown as ConsentLevel,
        consentVersion: 'v1',
        agreedClauseText: FULL_CLAUSE,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects missing consentVersion', async () => {
    const svc = new ConsentService(prismaStub());
    await expect(
      svc.record({
        tenantId: TENANT,
        userId: USER,
        scope: {},
        level: 'aggregate-only',
        consentVersion: '',
        agreedClauseText: FULL_CLAUSE,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects truncated agreed clause', async () => {
    const svc = new ConsentService(prismaStub());
    await expect(
      svc.record({
        tenantId: TENANT,
        userId: USER,
        scope: {},
        level: 'aggregate-only',
        consentVersion: 'v1',
        agreedClauseText: 'too short',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a fresh consent when none exists', async () => {
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new ConsentService(prisma);
    await svc.record({
      tenantId: TENANT,
      userId: USER,
      scope: { sdgFocus: ['SDG-6'] },
      level: 'aggregate-only',
      consentVersion: 'v1',
      agreedClauseText: FULL_CLAUSE,
    });
    expect(prisma.impactConsentRecord.create).toHaveBeenCalledOnce();
  });

  it('rejects re-recording the same version with different text', async () => {
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REC,
      agreedClauseHash:
        '93b54df59e6d9bfdc6c92e35a2d5089cf42a8e8b61afa68f3fc8bd6a06d4ca8d', // contrived; hashes will not match FULL_CLAUSE
    });
    const svc = new ConsentService(prisma);
    await expect(
      svc.record({
        tenantId: TENANT,
        userId: USER,
        scope: {},
        level: 'aggregate-only',
        consentVersion: 'v1',
        agreedClauseText: FULL_CLAUSE,
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('refreshes expiry on idempotent re-agreement (same hash)', async () => {
    const { createHash } = await import('node:crypto');
    const sameHash = createHash('sha256').update(FULL_CLAUSE).digest('hex');
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REC,
      agreedClauseHash: sameHash,
    });
    const svc = new ConsentService(prisma);
    await svc.record({
      tenantId: TENANT,
      userId: USER,
      scope: {},
      level: 'aggregate-only',
      consentVersion: 'v1',
      agreedClauseText: FULL_CLAUSE,
    });
    expect(prisma.impactConsentRecord.update).toHaveBeenCalledOnce();
    expect(prisma.impactConsentRecord.create).not.toHaveBeenCalled();
  });
});

describe('ConsentService.revoke', () => {
  it('errors with NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new ConsentService(prisma);
    await expect(svc.revoke(TENANT, REC)).rejects.toBeInstanceOf(NotFoundException);
  });

  it('is idempotent on already-revoked records', async () => {
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REC,
      revokedAt: new Date(Date.now() - 1000),
    });
    const svc = new ConsentService(prisma);
    await svc.revoke(TENANT, REC);
    expect(prisma.impactConsentRecord.update).not.toHaveBeenCalled();
  });

  it('sets revokedAt when first revoking', async () => {
    const prisma = prismaStub();
    (prisma.impactConsentRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: REC,
      revokedAt: null,
    });
    const svc = new ConsentService(prisma);
    await svc.revoke(TENANT, REC);
    expect(prisma.impactConsentRecord.update).toHaveBeenCalledOnce();
  });
});

describe('ConsentService.covers', () => {
  const study = { sdgFocus: ['SDG-6'], regions: ['BD'], topicTags: ['water'] };

  it('returns false for an expired record', () => {
    expect(
      ConsentService.covers(
        {
          scope: {},
          level: 'aggregate-only',
          expiresAt: new Date(Date.now() - 1000),
          revokedAt: null,
        },
        study,
      ),
    ).toBe(false);
  });

  it('returns false for a revoked record', () => {
    expect(
      ConsentService.covers(
        {
          scope: {},
          level: 'aggregate-only',
          expiresAt: new Date(Date.now() + 86400_000),
          revokedAt: new Date(Date.now() - 1000),
        },
        study,
      ),
    ).toBe(false);
  });

  it('returns true when scope is empty (covers everything in user consent)', () => {
    expect(
      ConsentService.covers(
        {
          scope: {},
          level: 'aggregate-only',
          expiresAt: new Date(Date.now() + 86400_000),
          revokedAt: null,
        },
        study,
      ),
    ).toBe(true);
  });

  it('returns false when sdg scope does not overlap', () => {
    expect(
      ConsentService.covers(
        {
          scope: { sdgFocus: ['SDG-13'] },
          level: 'aggregate-only',
          expiresAt: new Date(Date.now() + 86400_000),
          revokedAt: null,
        },
        study,
      ),
    ).toBe(false);
  });
});
