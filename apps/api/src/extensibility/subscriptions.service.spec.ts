import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { SubscriptionsService } from './subscriptions.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const PLUGIN = '22222222-2222-2222-2222-222222222222';
const SUB = '33333333-3333-3333-3333-333333333333';

function prismaStub(): PrismaService {
  const plugin = {
    findFirst: vi.fn(),
  };
  const sub = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: SUB, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  return { pluginManifest: plugin, eventSubscription: sub } as unknown as PrismaService;
}

describe('SubscriptionsService.create', () => {
  it('rejects malformed event pattern', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new SubscriptionsService(prisma);
    await expect(
      svc.create({
        tenantId: TENANT,
        pluginId: PLUGIN,
        eventPattern: '#$%',
        deliveryKind: 'inproc',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects webhook delivery without URL', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new SubscriptionsService(prisma);
    await expect(
      svc.create({
        tenantId: TENANT,
        pluginId: PLUGIN,
        eventPattern: 'core.*',
        deliveryKind: 'webhook',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects inproc with a webhookUrl set', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new SubscriptionsService(prisma);
    await expect(
      svc.create({
        tenantId: TENANT,
        pluginId: PLUGIN,
        eventPattern: 'core.*',
        deliveryKind: 'inproc',
        webhookUrl: 'https://example.com/hook',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when plugin is not approved', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'draft',
    });
    const svc = new SubscriptionsService(prisma);
    await expect(
      svc.create({
        tenantId: TENANT,
        pluginId: PLUGIN,
        eventPattern: 'core.*',
        deliveryKind: 'inproc',
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('issues a webhook secret ONCE and persists only the hash', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new SubscriptionsService(prisma);
    const out = await svc.create({
      tenantId: TENANT,
      pluginId: PLUGIN,
      eventPattern: 'core.*',
      deliveryKind: 'webhook',
      webhookUrl: 'https://example.com/hook',
    });
    expect(out.webhookSecret?.startsWith('sdgi_whsec_')).toBe(true);
    const call = (prisma.eventSubscription.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { webhookSecretHash: string };
    };
    expect(call.data.webhookSecretHash).toMatch(/^[a-f0-9]{64}$/);
    expect(call.data.webhookSecretHash).not.toBe(out.webhookSecret);
  });

  it('omits webhookSecret on inproc subscriptions', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new SubscriptionsService(prisma);
    const out = await svc.create({
      tenantId: TENANT,
      pluginId: PLUGIN,
      eventPattern: 'core.*',
      deliveryKind: 'inproc',
    });
    expect(out.webhookSecret).toBeUndefined();
  });
});

describe('SubscriptionsService.recordFailure', () => {
  it('increments failureCount', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SUB,
      active: true,
      failureCount: 1,
    });
    const svc = new SubscriptionsService(prisma);
    await svc.recordFailure(TENANT, SUB);
    const call = (prisma.eventSubscription.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { failureCount: number; active: boolean };
    };
    expect(call.data.failureCount).toBe(2);
    expect(call.data.active).toBe(true);
  });

  it('auto-deactivates after threshold', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SUB,
      active: true,
      failureCount: 4, // 5th failure trips the switch
    });
    const svc = new SubscriptionsService(prisma);
    await svc.recordFailure(TENANT, SUB);
    const call = (prisma.eventSubscription.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { failureCount: number; active: boolean };
    };
    expect(call.data.failureCount).toBe(5);
    expect(call.data.active).toBe(false);
  });

  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new SubscriptionsService(prisma);
    await expect(svc.recordFailure(TENANT, SUB)).rejects.toBeInstanceOf(NotFoundException);
  });
});

describe('SubscriptionsService.recordSuccess', () => {
  it('resets failureCount and stamps lastDeliveredAt', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SUB,
      active: true,
      failureCount: 3,
    });
    const svc = new SubscriptionsService(prisma);
    await svc.recordSuccess(TENANT, SUB);
    const call = (prisma.eventSubscription.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { failureCount: number; lastDeliveredAt: Date };
    };
    expect(call.data.failureCount).toBe(0);
    expect(call.data.lastDeliveredAt).toBeInstanceOf(Date);
  });
});

describe('SubscriptionsService.reactivate', () => {
  it('returns existing subscription if already active', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SUB,
      active: true,
    });
    const svc = new SubscriptionsService(prisma);
    await svc.reactivate(TENANT, SUB);
    expect(prisma.eventSubscription.update).not.toHaveBeenCalled();
  });

  it('flips active back on and resets failureCount', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SUB,
      active: false,
      failureCount: 5,
    });
    const svc = new SubscriptionsService(prisma);
    await svc.reactivate(TENANT, SUB);
    const call = (prisma.eventSubscription.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { active: boolean; failureCount: number };
    };
    expect(call.data.active).toBe(true);
    expect(call.data.failureCount).toBe(0);
  });
});
