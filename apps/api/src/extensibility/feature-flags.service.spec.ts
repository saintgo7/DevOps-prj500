import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { FeatureFlagsService } from './feature-flags.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const ACTOR = '22222222-2222-2222-2222-222222222222';
const FLAG = '33333333-3333-3333-3333-333333333333';

function prismaStub(): PrismaService {
  const flag = {
    findFirst: vi.fn(),
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: FLAG, ...(data as object) })),
    update: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: FLAG, ...(data as object) })),
  };
  return { featureFlag: flag } as unknown as PrismaService;
}

describe('FeatureFlagsService.evaluate', () => {
  it('returns false when flag is null', () => {
    expect(FeatureFlagsService.evaluate(null, { userId: 'u', roles: [] })).toBe(false);
  });

  it('returns false when master switch is off', () => {
    expect(
      FeatureFlagsService.evaluate(
        { enabled: false, audience: null },
        { userId: 'u', roles: [] },
      ),
    ).toBe(false);
  });

  it('returns true when enabled and no audience set', () => {
    expect(
      FeatureFlagsService.evaluate(
        { enabled: true, audience: null },
        { userId: 'u', roles: [] },
      ),
    ).toBe(true);
  });

  it('returns true when user matches userIds', () => {
    expect(
      FeatureFlagsService.evaluate(
        { enabled: true, audience: { userIds: ['u-1'] } },
        { userId: 'u-1', roles: [] },
      ),
    ).toBe(true);
  });

  it('returns true when user role matches roles', () => {
    expect(
      FeatureFlagsService.evaluate(
        { enabled: true, audience: { roles: ['admin'] } },
        { userId: 'u-1', roles: ['admin'] },
      ),
    ).toBe(true);
  });

  it('returns false when neither user nor role match', () => {
    expect(
      FeatureFlagsService.evaluate(
        { enabled: true, audience: { userIds: ['u-2'], roles: ['admin'] } },
        { userId: 'u-1', roles: ['contributor'] },
      ),
    ).toBe(false);
  });
});

describe('FeatureFlagsService.set', () => {
  it('rejects malformed flagKey', async () => {
    const svc = new FeatureFlagsService(prismaStub());
    await expect(
      svc.set({ tenantId: TENANT, flagKey: 'A', enabled: true, updatedBy: ACTOR }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a fresh flag when none exists', async () => {
    const prisma = prismaStub();
    (prisma.featureFlag.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new FeatureFlagsService(prisma);
    await svc.set({ tenantId: TENANT, flagKey: 'plugin.biodiv', enabled: true, updatedBy: ACTOR });
    expect(prisma.featureFlag.create).toHaveBeenCalledOnce();
  });

  it('updates an existing flag in place', async () => {
    const prisma = prismaStub();
    (prisma.featureFlag.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({ id: FLAG });
    const svc = new FeatureFlagsService(prisma);
    await svc.set({ tenantId: TENANT, flagKey: 'plugin.biodiv', enabled: false, updatedBy: ACTOR });
    expect(prisma.featureFlag.update).toHaveBeenCalledOnce();
  });
});

describe('FeatureFlagsService.get', () => {
  it('throws NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.featureFlag.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new FeatureFlagsService(prisma);
    await expect(svc.get(TENANT, 'plugin.biodiv')).rejects.toBeInstanceOf(NotFoundException);
  });
});
