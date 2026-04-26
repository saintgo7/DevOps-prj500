import { describe, expect, it, vi } from 'vitest';
import { BadRequestException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { EventsService, patternMatches } from './events.service';

const TENANT = '11111111-1111-1111-1111-111111111111';

function prismaStub(): PrismaService {
  const evt = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: 'e-1', ...(data as object) })),
  };
  const sub = {
    findMany: vi.fn().mockResolvedValue([]),
  };
  return { domainEvent: evt, eventSubscription: sub } as unknown as PrismaService;
}

describe('patternMatches', () => {
  it('exact match', () => {
    expect(patternMatches('core.column.published', 'core.column.published')).toBe(true);
  });
  it('global wildcard', () => {
    expect(patternMatches('*', 'anything.here')).toBe(true);
  });
  it('prefix wildcard', () => {
    expect(patternMatches('core.*', 'core.published')).toBe(true);
    expect(patternMatches('core.*', 'plugin.published')).toBe(false);
  });
  it('suffix wildcard', () => {
    expect(patternMatches('*.failed', 'webhook.failed')).toBe(true);
    expect(patternMatches('*.failed', 'webhook.delivered')).toBe(false);
  });
  it('different segment count rejects', () => {
    expect(patternMatches('core.*', 'core.column.published')).toBe(false);
  });
});

describe('EventsService.emit', () => {
  it('rejects missing source', async () => {
    const svc = new EventsService(prismaStub());
    await expect(
      svc.emit({ tenantId: TENANT, source: '', eventName: 'a.b', payload: {} }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects an eventName without a dot', async () => {
    const svc = new EventsService(prismaStub());
    await expect(
      svc.emit({ tenantId: TENANT, source: 'core', eventName: 'created', payload: {} }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('persists the event with payload masked by piiFields', async () => {
    const prisma = prismaStub();
    const svc = new EventsService(prisma);
    await svc.emit({
      tenantId: TENANT,
      source: 'plugin.biodiv',
      eventName: 'biodiv-card.created',
      payload: { name: 'Alice', species: 'panthera' },
      piiFields: ['name'],
    });
    const call = (prisma.domainEvent.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { payload: { name: string; species: string } };
    };
    expect(call.data.payload.name).not.toBe('Alice');
    expect(call.data.payload.species).toBe('panthera');
  });
});

describe('EventsService.matchingSubscriptions', () => {
  it('returns only matching subscriptions', async () => {
    const prisma = prismaStub();
    (prisma.eventSubscription.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { id: 's-1', eventPattern: 'core.*' },
      { id: 's-2', eventPattern: '*.published' },
      { id: 's-3', eventPattern: 'plugin.biodiv.*' },
    ]);
    const svc = new EventsService(prisma);
    const out = await svc.matchingSubscriptions(TENANT, 'core.published');
    const ids = out.map((s) => s.id);
    expect(ids).toContain('s-1');
    expect(ids).toContain('s-2');
    expect(ids).not.toContain('s-3');
  });
});
