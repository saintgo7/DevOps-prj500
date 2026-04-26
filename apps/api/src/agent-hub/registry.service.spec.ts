import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { AgentRegistryService, type RegisterAgentInput } from './registry.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const STEWARD = '22222222-2222-2222-2222-222222222222';
const AGENT = '33333333-3333-3333-3333-333333333333';
const ACTOR = '44444444-4444-4444-4444-444444444444';
const SESSION = '55555555-5555-5555-5555-555555555555';

const VALID_PUBKEY = 'a'.repeat(64);

function input(overrides: Partial<RegisterAgentInput> = {}): RegisterAgentInput {
  return {
    tenantId: TENANT,
    agentKey: 'water-watch',
    nameI18n: { en: { name: 'Water watch agent' } },
    operatorOrg: 'NGO X',
    stewardUserId: STEWARD,
    noncommercialPledge: true,
    nonharmPledge: true,
    plainLanguagePledge: true,
    sdgFocus: ['SDG-6'],
    capabilities: ['monitor', 'summarise'],
    workingLocales: ['en', 'ko'],
    fieldRegions: ['BD'],
    publicKey: VALID_PUBKEY,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const agent = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: AGENT, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: AGENT, ...(data as object) }),
    ),
  };
  const session = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: SESSION, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: SESSION, ...(data as object) }),
    ),
  };
  return {
    agentRegistration: agent,
    agentSession: session,
  } as unknown as PrismaService;
}

describe('AgentRegistryService.canTransition', () => {
  it('allows draft → review', () => {
    expect(AgentRegistryService.canTransition('draft', 'review')).toBe(true);
  });
  it('forbids draft → active (must go via review)', () => {
    expect(AgentRegistryService.canTransition('draft', 'active')).toBe(false);
  });
  it('allows active ↔ paused', () => {
    expect(AgentRegistryService.canTransition('active', 'paused')).toBe(true);
    expect(AgentRegistryService.canTransition('paused', 'active')).toBe(true);
  });
  it('forbids retired → anything', () => {
    expect(AgentRegistryService.canTransition('retired', 'active')).toBe(false);
  });
});

describe('AgentRegistryService.register', () => {
  it('rejects without non-commercial pledge', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ noncommercialPledge: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects without non-harm pledge', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ nonharmPledge: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects without plain-language pledge', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ plainLanguagePledge: false }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects without steward', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ stewardUserId: '' }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects malformed agentKey', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ agentKey: 'A' }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('rejects malformed publicKey', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(svc.register(input({ publicKey: 'short' }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });
  it('creates a draft agent when valid', async () => {
    const prisma = prismaStub();
    const svc = new AgentRegistryService(prisma);
    await svc.register(input());
    expect(prisma.agentRegistration.create).toHaveBeenCalledOnce();
  });
});

describe('AgentRegistryService.transition', () => {
  it('rejects illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'draft',
    });
    const svc = new AgentRegistryService(prisma);
    await expect(svc.transition(TENANT, AGENT, 'active', ACTOR)).rejects.toBeInstanceOf(
      ConflictException,
    );
  });
  it('rejects pause without sufficient reason', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
    });
    const svc = new AgentRegistryService(prisma);
    await expect(
      svc.transition(TENANT, AGENT, 'paused', ACTOR, 'short'),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('approves with approvedAt + approvedBy on review → active', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'review',
    });
    const svc = new AgentRegistryService(prisma);
    await svc.transition(TENANT, AGENT, 'active', ACTOR);
    const call = (prisma.agentRegistration.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string; approvedAt: Date; approvedBy: string };
    };
    expect(call.data.state).toBe('active');
    expect(call.data.approvedAt).toBeInstanceOf(Date);
    expect(call.data.approvedBy).toBe(ACTOR);
  });
});

describe('AgentRegistryService.recordHarmStrike', () => {
  it('increments harmStrikes', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
      harmStrikes: 0,
    });
    const svc = new AgentRegistryService(prisma);
    await svc.recordHarmStrike(TENANT, AGENT);
    const call = (prisma.agentRegistration.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { harmStrikes: number; state?: string };
    };
    expect(call.data.harmStrikes).toBe(1);
    expect(call.data.state).toBeUndefined();
  });
  it('auto-pauses when crossing the threshold', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
      harmStrikes: 2,
    });
    const svc = new AgentRegistryService(prisma);
    await svc.recordHarmStrike(TENANT, AGENT);
    const call = (prisma.agentRegistration.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { harmStrikes: number; state?: string; pauseReason?: string };
    };
    expect(call.data.harmStrikes).toBe(3);
    expect(call.data.state).toBe('paused');
    expect(call.data.pauseReason).toMatch(/Auto-paused/);
  });
  it('does not auto-pause an already-paused agent', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'paused',
      harmStrikes: 5,
    });
    const svc = new AgentRegistryService(prisma);
    await svc.recordHarmStrike(TENANT, AGENT);
    const call = (prisma.agentRegistration.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state?: string };
    };
    expect(call.data.state).toBeUndefined();
  });
});

describe('AgentRegistryService.openSession', () => {
  it('rejects opening a session on a non-active agent', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'draft',
    });
    const svc = new AgentRegistryService(prisma);
    await expect(svc.openSession(TENANT, AGENT)).rejects.toBeInstanceOf(ConflictException);
  });
  it('opens a started session on an active agent', async () => {
    const prisma = prismaStub();
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
    });
    const svc = new AgentRegistryService(prisma);
    await svc.openSession(TENANT, AGENT, { en: 'monitoring water sensors' });
    expect(prisma.agentSession.create).toHaveBeenCalledOnce();
  });
});

describe('AgentRegistryService.heartbeat', () => {
  it('rejects unknown state', async () => {
    const svc = new AgentRegistryService(prismaStub());
    await expect(
      svc.heartbeat(TENANT, SESSION, 'whatever' as unknown as 'idle'),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects heartbeat on ended session', async () => {
    const prisma = prismaStub();
    (prisma.agentSession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'ended',
    });
    const svc = new AgentRegistryService(prisma);
    await expect(svc.heartbeat(TENANT, SESSION, 'idle')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });
  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.agentSession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new AgentRegistryService(prisma);
    await expect(svc.heartbeat(TENANT, SESSION, 'idle')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });
  it('updates heartbeat timestamp', async () => {
    const prisma = prismaStub();
    (prisma.agentSession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'idle',
    });
    const svc = new AgentRegistryService(prisma);
    await svc.heartbeat(TENANT, SESSION, 'busy', { en: 'rolling up sensor data' });
    expect(prisma.agentSession.update).toHaveBeenCalledOnce();
  });
});

describe('AgentRegistryService.endSession', () => {
  it('returns existing session when already ended', async () => {
    const prisma = prismaStub();
    (prisma.agentSession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'ended',
    });
    const svc = new AgentRegistryService(prisma);
    await svc.endSession(TENANT, SESSION);
    expect(prisma.agentSession.update).not.toHaveBeenCalled();
  });
  it('marks ended on first call', async () => {
    const prisma = prismaStub();
    (prisma.agentSession.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: SESSION,
      state: 'idle',
    });
    const svc = new AgentRegistryService(prisma);
    await svc.endSession(TENANT, SESSION);
    expect(prisma.agentSession.update).toHaveBeenCalledOnce();
  });
});
