import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { AgentDigestService } from './digest.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const DIGEST = '22222222-2222-2222-2222-222222222222';
const ACTOR = '33333333-3333-3333-3333-333333333333';

function prismaStub(): PrismaService {
  const digest = {
    findFirst: vi.fn(),
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: DIGEST, ...(data as object) }),
    ),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: DIGEST, ...(data as object) }),
    ),
  };
  return { agentDailyDigest: digest } as unknown as PrismaService;
}

describe('AgentDigestService.canTransition', () => {
  it('allows draft → human_review', () => {
    expect(AgentDigestService.canTransition('draft', 'human_review')).toBe(true);
  });
  it('forbids draft → published (must go via review)', () => {
    expect(AgentDigestService.canTransition('draft', 'published')).toBe(false);
  });
  it('forbids any transition out of published', () => {
    expect(AgentDigestService.canTransition('published', 'draft')).toBe(false);
  });
});

describe('AgentDigestService.upsertDraft', () => {
  it('rejects when no source messages are listed', async () => {
    const svc = new AgentDigestService(prismaStub());
    await expect(
      svc.upsertDraft({
        tenantId: TENANT,
        digestDate: new Date('2026-04-26'),
        summaryI18n: { en: 'a'.repeat(70), ko: 'b'.repeat(70) },
        sourceMessageIds: [],
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects upsert when a published digest already exists', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DIGEST,
      state: 'published',
    });
    const svc = new AgentDigestService(prisma);
    await expect(
      svc.upsertDraft({
        tenantId: TENANT,
        digestDate: new Date('2026-04-26'),
        summaryI18n: { en: 'a'.repeat(70), ko: 'b'.repeat(70) },
        sourceMessageIds: ['m-1'],
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });
  it('creates a draft when nothing exists', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new AgentDigestService(prisma);
    await svc.upsertDraft({
      tenantId: TENANT,
      digestDate: new Date('2026-04-26'),
      summaryI18n: { en: 'a'.repeat(70), ko: 'b'.repeat(70) },
      sourceMessageIds: ['m-1', 'm-2'],
    });
    expect(prisma.agentDailyDigest.create).toHaveBeenCalledOnce();
  });
  it('updates an existing non-published digest', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DIGEST,
      state: 'human_review',
    });
    const svc = new AgentDigestService(prisma);
    await svc.upsertDraft({
      tenantId: TENANT,
      digestDate: new Date('2026-04-26'),
      summaryI18n: { en: 'a'.repeat(70), ko: 'b'.repeat(70) },
      sourceMessageIds: ['m-1'],
    });
    expect(prisma.agentDailyDigest.update).toHaveBeenCalledOnce();
  });
});

describe('AgentDigestService.transition', () => {
  it('rejects illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DIGEST,
      state: 'draft',
    });
    const svc = new AgentDigestService(prisma);
    await expect(svc.transition(TENANT, DIGEST, 'published', ACTOR)).rejects.toBeInstanceOf(
      ConflictException,
    );
  });
  it('rejects publish without en+ko summary', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DIGEST,
      state: 'human_review',
      summaryI18n: { en: 'a'.repeat(70) }, // missing ko
    });
    const svc = new AgentDigestService(prisma);
    await expect(svc.transition(TENANT, DIGEST, 'published', ACTOR)).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('publishes with approvedAt + approvedBy when valid', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DIGEST,
      state: 'human_review',
      summaryI18n: { en: 'a'.repeat(70), ko: 'b'.repeat(70) },
    });
    const svc = new AgentDigestService(prisma);
    await svc.transition(TENANT, DIGEST, 'published', ACTOR);
    const call = (prisma.agentDailyDigest.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string; approvedAt: Date; approvedBy: string };
    };
    expect(call.data.state).toBe('published');
    expect(call.data.approvedAt).toBeInstanceOf(Date);
    expect(call.data.approvedBy).toBe(ACTOR);
  });
  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.agentDailyDigest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new AgentDigestService(prisma);
    await expect(svc.transition(TENANT, DIGEST, 'human_review', ACTOR)).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });
});
