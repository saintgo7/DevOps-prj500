import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { AgentCollabService } from './collab.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const PROP = '22222222-2222-2222-2222-222222222222';
const PROPOSER = '33333333-3333-3333-3333-333333333333';
const RECIPIENT = '44444444-4444-4444-4444-444444444444';

function prismaStub(): PrismaService {
  const proposal = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: PROP, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: PROP, ...(data as object) }),
    ),
  };
  return { agentCollaborationProposal: proposal } as unknown as PrismaService;
}

describe('AgentCollabService.propose', () => {
  it('rejects without non-commercial notice', async () => {
    const svc = new AgentCollabService(prismaStub());
    await expect(
      svc.propose({
        tenantId: TENANT,
        proposerAgentId: PROPOSER,
        recipientAgentId: RECIPIENT,
        subjectI18n: { en: 'collab' },
        contextI18n: { en: 'why' },
        noncommercialNotice: false,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects two proposers', async () => {
    const svc = new AgentCollabService(prismaStub());
    await expect(
      svc.propose({
        tenantId: TENANT,
        proposerAgentId: PROPOSER,
        proposerUserId: PROPOSER,
        recipientAgentId: RECIPIENT,
        subjectI18n: { en: 'x' },
        contextI18n: { en: 'y' },
        noncommercialNotice: true,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects no recipient', async () => {
    const svc = new AgentCollabService(prismaStub());
    await expect(
      svc.propose({
        tenantId: TENANT,
        proposerAgentId: PROPOSER,
        subjectI18n: { en: 'x' },
        contextI18n: { en: 'y' },
        noncommercialNotice: true,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('rejects subject without en or ko', async () => {
    const svc = new AgentCollabService(prismaStub());
    await expect(
      svc.propose({
        tenantId: TENANT,
        proposerAgentId: PROPOSER,
        recipientAgentId: RECIPIENT,
        subjectI18n: { sw: 'pendekezo' },
        contextI18n: { sw: 'sababu' },
        noncommercialNotice: true,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });
  it('creates a suggested proposal when valid', async () => {
    const prisma = prismaStub();
    const svc = new AgentCollabService(prisma);
    await svc.propose({
      tenantId: TENANT,
      proposerAgentId: PROPOSER,
      recipientAgentId: RECIPIENT,
      subjectI18n: { ko: '협력 제안' },
      contextI18n: { ko: '같은 SDG 6 영역에서 데이터 공유 제안' },
      noncommercialNotice: true,
    });
    expect(prisma.agentCollaborationProposal.create).toHaveBeenCalledOnce();
  });
});

describe('AgentCollabService.accept', () => {
  it('rejects accept once cancelled', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'cancelled',
    });
    const svc = new AgentCollabService(prisma);
    await expect(svc.accept(TENANT, PROP, 'proposer')).rejects.toBeInstanceOf(ConflictException);
  });
  it('moves to recipient_review on first acceptance', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'suggested',
      proposerStewardAcceptedAt: null,
      recipientStewardAcceptedAt: null,
    });
    const svc = new AgentCollabService(prisma);
    await svc.accept(TENANT, PROP, 'recipient');
    const call = (prisma.agentCollaborationProposal.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string };
    };
    expect(call.data.state).toBe('recipient_review');
  });
  it('moves to accepted on second acceptance', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'recipient_review',
      proposerStewardAcceptedAt: null,
      recipientStewardAcceptedAt: new Date(),
    });
    const svc = new AgentCollabService(prisma);
    await svc.accept(TENANT, PROP, 'proposer');
    const call = (prisma.agentCollaborationProposal.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string };
    };
    expect(call.data.state).toBe('accepted');
  });
  it('rejects double acceptance from same side', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'recipient_review',
      proposerStewardAcceptedAt: new Date(),
      recipientStewardAcceptedAt: null,
    });
    const svc = new AgentCollabService(prisma);
    await expect(svc.accept(TENANT, PROP, 'proposer')).rejects.toBeInstanceOf(ConflictException);
  });
});

describe('AgentCollabService.decline', () => {
  it('rejects short reason', async () => {
    const svc = new AgentCollabService(prismaStub());
    await expect(svc.decline(TENANT, PROP, 'no')).rejects.toBeInstanceOf(BadRequestException);
  });
  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new AgentCollabService(prisma);
    await expect(
      svc.decline(TENANT, PROP, 'this is a long enough reason'),
    ).rejects.toBeInstanceOf(NotFoundException);
  });
  it('declines when reason valid and state allows', async () => {
    const prisma = prismaStub();
    (prisma.agentCollaborationProposal.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROP,
      state: 'recipient_review',
    });
    const svc = new AgentCollabService(prisma);
    await svc.decline(TENANT, PROP, 'overlap with another active project');
    const call = (prisma.agentCollaborationProposal.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { state: string };
    };
    expect(call.data.state).toBe('declined');
  });
});

describe('AgentCollabService.bothSidesAccepted', () => {
  it('false when missing one side', () => {
    expect(
      AgentCollabService.bothSidesAccepted({
        proposerStewardAcceptedAt: new Date(),
        recipientStewardAcceptedAt: null,
      }),
    ).toBe(false);
  });
  it('true when both sides accepted', () => {
    expect(
      AgentCollabService.bothSidesAccepted({
        proposerStewardAcceptedAt: new Date(),
        recipientStewardAcceptedAt: new Date(),
      }),
    ).toBe(true);
  });
});
