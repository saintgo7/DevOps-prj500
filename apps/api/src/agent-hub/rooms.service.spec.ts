import { describe, expect, it, vi } from 'vitest';
import { generateKeyPairSync, sign as nodeSign } from 'node:crypto';
import { BadRequestException, ConflictException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { AgentRegistryService } from './registry.service';
import { AgentRoomsService, type CreateRoomInput, type PostMessageInput } from './rooms.service';
import { canonicalBytes } from './agent-signature';

const TENANT = '11111111-1111-1111-1111-111111111111';
const CREATOR = '22222222-2222-2222-2222-222222222222';
const AGENT = '33333333-3333-3333-3333-333333333333';
const ROOM = '44444444-4444-4444-4444-444444444444';

function genAgentKey() {
  const { publicKey, privateKey } = generateKeyPairSync('ed25519');
  const der = publicKey.export({ format: 'der', type: 'spki' });
  const rawPub = Buffer.from(der.subarray(12)).toString('hex');
  return { rawPub, privateKey };
}

function prismaStub(): PrismaService {
  const room = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: ROOM, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: ROOM, ...(data as object) }),
    ),
  };
  const member = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  const message = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    findMany: vi.fn().mockResolvedValue([]),
  };
  const agent = {
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  return {
    agentRoom: room,
    agentRoomMember: member,
    agentMessage: message,
    agentRegistration: agent,
  } as unknown as PrismaService;
}

function build(prisma: PrismaService): AgentRoomsService {
  return new AgentRoomsService(prisma, new AgentRegistryService(prisma));
}

describe('AgentRoomsService.createRoom', () => {
  it('rejects empty topic', async () => {
    const svc = build(prismaStub());
    await expect(
      svc.createRoom({ tenantId: TENANT, createdBy: CREATOR, topicI18n: {} } as CreateRoomInput),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects publicReadable=true on non public-readable kind', async () => {
    const svc = build(prismaStub());
    await expect(
      svc.createRoom({
        tenantId: TENANT,
        createdBy: CREATOR,
        topicI18n: { en: 'water' },
        kind: 'mixed',
        publicReadable: true,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('creates a default mixed room', async () => {
    const prisma = prismaStub();
    const svc = build(prisma);
    await svc.createRoom({
      tenantId: TENANT,
      createdBy: CREATOR,
      topicI18n: { en: 'water access' },
    });
    const call = (prisma.agentRoom.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { kind: string; state: string };
    };
    expect(call.data.kind).toBe('mixed');
    expect(call.data.state).toBe('active');
  });
});

describe('AgentRoomsService.archive', () => {
  it('returns existing room when already archived', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'archived',
    });
    const svc = build(prisma);
    await svc.archive(TENANT, ROOM);
    expect(prisma.agentRoom.update).not.toHaveBeenCalled();
  });
  it('archives an active room', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    const svc = build(prisma);
    await svc.archive(TENANT, ROOM);
    expect(prisma.agentRoom.update).toHaveBeenCalledOnce();
  });
});

describe('AgentRoomsService.addMember', () => {
  it('rejects when neither principal is set', async () => {
    const svc = build(prismaStub());
    await expect(
      svc.addMember({ tenantId: TENANT, roomId: ROOM }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects when both principals are set', async () => {
    const svc = build(prismaStub());
    await expect(
      svc.addMember({ tenantId: TENANT, roomId: ROOM, agentId: AGENT, userId: CREATOR }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects user member in agent-only room', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
      kind: 'agent-only',
    });
    const svc = build(prisma);
    await expect(
      svc.addMember({ tenantId: TENANT, roomId: ROOM, userId: CREATOR }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects on archived room', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'archived',
      kind: 'mixed',
    });
    const svc = build(prisma);
    await expect(
      svc.addMember({ tenantId: TENANT, roomId: ROOM, userId: CREATOR }),
    ).rejects.toBeInstanceOf(ConflictException);
  });
  it('adds a member to an active mixed room', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
      kind: 'mixed',
    });
    const svc = build(prisma);
    await svc.addMember({ tenantId: TENANT, roomId: ROOM, userId: CREATOR });
    expect(prisma.agentRoomMember.create).toHaveBeenCalledOnce();
  });
});

describe('AgentRoomsService.postMessage', () => {
  function baseInput(overrides: Partial<PostMessageInput> = {}): PostMessageInput {
    return {
      tenantId: TENANT,
      roomId: ROOM,
      senderUserId: CREATOR,
      originalText: '오늘의 발견을 공유합니다',
      originalLocale: 'ko',
      kind: 'chat',
      ...overrides,
    };
  }

  it('rejects when neither sender is set', async () => {
    const svc = build(prismaStub());
    await expect(
      svc.postMessage({
        tenantId: TENANT,
        roomId: ROOM,
        originalText: 'x',
        originalLocale: 'en',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects empty text', async () => {
    const svc = build(prismaStub());
    await expect(svc.postMessage(baseInput({ originalText: '' }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
  });

  it('rejects on archived room', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'archived',
    });
    const svc = build(prisma);
    await expect(svc.postMessage(baseInput())).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects harmful content from a human sender', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    const svc = build(prisma);
    await expect(
      svc.postMessage(baseInput({ originalText: '모든 무슬림은 문제다 — 그것을 활용하자.' })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects an agent message without a signature', async () => {
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    const svc = build(prisma);
    const agentNoSig: PostMessageInput = {
      tenantId: TENANT,
      roomId: ROOM,
      senderAgentId: AGENT,
      originalText: '오늘의 발견을 공유합니다',
      originalLocale: 'ko',
      kind: 'chat',
    };
    await expect(svc.postMessage(agentNoSig)).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects an agent message with a bogus signature', async () => {
    const { rawPub } = genAgentKey();
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
      publicKey: rawPub,
    });
    const svc = build(prisma);
    const bogus: PostMessageInput = {
      tenantId: TENANT,
      roomId: ROOM,
      senderAgentId: AGENT,
      originalText: '오늘의 발견을 공유합니다',
      originalLocale: 'ko',
      kind: 'chat',
      signature: '0'.repeat(128),
    };
    await expect(svc.postMessage(bogus)).rejects.toBeInstanceOf(BadRequestException);
  });

  it('accepts a valid agent message and persists harmReport=ok', async () => {
    const { rawPub, privateKey } = genAgentKey();
    const text = '오늘의 발견을 공유합니다';
    const sig = nodeSign(null, canonicalBytes(ROOM, 'ko', text), privateKey).toString('hex');
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
      publicKey: rawPub,
    });
    const svc = build(prisma);
    await svc.postMessage({
      tenantId: TENANT,
      roomId: ROOM,
      senderAgentId: AGENT,
      originalText: text,
      originalLocale: 'ko',
      kind: 'chat',
      signature: sig,
    });
    expect(prisma.agentMessage.create).toHaveBeenCalledOnce();
  });

  it('records a harm strike when an agent sends harmful content', async () => {
    const { rawPub, privateKey } = genAgentKey();
    const text = '모든 무슬림은 문제다 — 그것을 활용하자.';
    const sig = nodeSign(null, canonicalBytes(ROOM, 'ko', text), privateKey).toString('hex');
    const prisma = prismaStub();
    (prisma.agentRoom.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: ROOM,
      state: 'active',
    });
    // Two findFirst calls — the agent lookup happens for both signature
    // verify and harm-strike recording. Always return the same active agent.
    (prisma.agentRegistration.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: AGENT,
      state: 'active',
      publicKey: rawPub,
      harmStrikes: 0,
    });
    const svc = build(prisma);
    await expect(
      svc.postMessage({
        tenantId: TENANT,
        roomId: ROOM,
        senderAgentId: AGENT,
        originalText: text,
        originalLocale: 'ko',
        kind: 'chat',
        signature: sig,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
    expect(prisma.agentRegistration.update).toHaveBeenCalledOnce();
  });
});
