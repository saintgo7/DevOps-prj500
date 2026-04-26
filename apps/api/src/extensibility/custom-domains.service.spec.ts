import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { CustomDomainsService } from './custom-domains.service';
import { EventsService } from './events.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const PLUGIN = '22222222-2222-2222-2222-222222222222';
const DOMAIN = '33333333-3333-3333-3333-333333333333';
const RECORD = '44444444-4444-4444-4444-444444444444';
const OWNER = '55555555-5555-5555-5555-555555555555';

function prismaStub(): PrismaService {
  const plugin = {
    findFirst: vi.fn(),
  };
  const domain = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: DOMAIN, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const record = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: RECORD, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: RECORD, ...(data as object) }),
    ),
    count: vi.fn().mockResolvedValue(0),
  };
  const workflow = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    findFirst: vi.fn(),
  };
  const event = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
  };
  return {
    pluginManifest: plugin,
    customDomain: domain,
    customRecord: record,
    customWorkflow: workflow,
    domainEvent: event,
  } as unknown as PrismaService;
}

function build(prisma: PrismaService): CustomDomainsService {
  return new CustomDomainsService(prisma, new EventsService(prisma));
}

const SCHEMA = {
  type: 'object',
  required: ['species'],
  properties: {
    species: { type: 'string', minLength: 1 },
    spotted: { type: 'integer', minimum: 0 },
    note: { type: 'string' },
  },
  additionalProperties: false,
};

describe('CustomDomainsService.createDomain', () => {
  it('rejects malformed domainKey', async () => {
    const prisma = prismaStub();
    const svc = build(prisma);
    await expect(
      svc.createDomain({
        tenantId: TENANT,
        pluginId: PLUGIN,
        domainKey: 'A',
        nameI18n: { en: { name: 'X' } },
        jsonSchema: SCHEMA,
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when plugin is not approved', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'draft',
    });
    const svc = build(prisma);
    await expect(
      svc.createDomain({
        tenantId: TENANT,
        pluginId: PLUGIN,
        domainKey: 'biodiv',
        nameI18n: { en: { name: 'X' } },
        jsonSchema: SCHEMA,
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('creates a draft domain when plugin is approved', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = build(prisma);
    await svc.createDomain({
      tenantId: TENANT,
      pluginId: PLUGIN,
      domainKey: 'biodiv',
      nameI18n: { en: { name: 'X' } },
      jsonSchema: SCHEMA,
    });
    expect(prisma.customDomain.create).toHaveBeenCalledOnce();
  });
});

describe('CustomDomainsService.transitionDomain', () => {
  it('rejects retire when records still exist', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'active',
    });
    (prisma.customRecord.count as ReturnType<typeof vi.fn>).mockResolvedValue(3);
    const svc = build(prisma);
    await expect(svc.transitionDomain(TENANT, DOMAIN, 'retired')).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('moves draft → active', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'draft',
    });
    (prisma.customDomain.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'active',
    });
    const svc = build(prisma);
    const out = (await svc.transitionDomain(TENANT, DOMAIN, 'active')) as { state: string };
    expect(out.state).toBe('active');
  });
});

describe('CustomDomainsService.upsertRecord', () => {
  it('rejects record on a non-active domain', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'draft',
      jsonSchema: SCHEMA,
      pluginId: PLUGIN,
      domainKey: 'biodiv',
      piiFields: [],
    });
    const svc = build(prisma);
    await expect(
      svc.upsertRecord({
        tenantId: TENANT,
        domainId: DOMAIN,
        ownerId: OWNER,
        payload: { species: 'panthera' },
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects payload that fails schema', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'active',
      jsonSchema: SCHEMA,
      pluginId: PLUGIN,
      domainKey: 'biodiv',
      piiFields: [],
    });
    const svc = build(prisma);
    await expect(
      svc.upsertRecord({
        tenantId: TENANT,
        domainId: DOMAIN,
        ownerId: OWNER,
        payload: { species: '' }, // minLength 1
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects payload blocked by harmful-content guard', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'active',
      jsonSchema: SCHEMA,
      pluginId: PLUGIN,
      domainKey: 'biodiv',
      piiFields: [],
    });
    const svc = build(prisma);
    await expect(
      svc.upsertRecord({
        tenantId: TENANT,
        domainId: DOMAIN,
        ownerId: OWNER,
        payload: { species: 'panthera', note: '모든 무슬림은 문제다 — 그것을 활용하자.' },
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a record and emits a domain event', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      state: 'active',
      jsonSchema: SCHEMA,
      pluginId: PLUGIN,
      domainKey: 'biodiv',
      piiFields: ['species'],
    });
    const svc = build(prisma);
    await svc.upsertRecord({
      tenantId: TENANT,
      domainId: DOMAIN,
      ownerId: OWNER,
      payload: { species: 'panthera', spotted: 3 },
    });
    expect(prisma.customRecord.create).toHaveBeenCalledOnce();
    expect(prisma.domainEvent.create).toHaveBeenCalledOnce();
    const evCall = (prisma.domainEvent.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { eventName: string };
    };
    expect(evCall.data.eventName).toBe('biodiv.created');
  });
});

describe('CustomDomainsService.createWorkflow', () => {
  it('rejects when initialState is not in transitions', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
    });
    const svc = build(prisma);
    await expect(
      svc.createWorkflow({
        tenantId: TENANT,
        domainId: DOMAIN,
        workflowKey: 'lifecycle',
        transitions: { requested: ['approved'] },
        initialState: 'something-else',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects trigger emit names without a dot', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
    });
    const svc = build(prisma);
    await expect(
      svc.createWorkflow({
        tenantId: TENANT,
        domainId: DOMAIN,
        workflowKey: 'lifecycle',
        transitions: { requested: ['approved'] },
        initialState: 'requested',
        triggers: [{ on: 'approved', emit: 'invalidname' }],
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a workflow when valid', async () => {
    const prisma = prismaStub();
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
    });
    const svc = build(prisma);
    await svc.createWorkflow({
      tenantId: TENANT,
      domainId: DOMAIN,
      workflowKey: 'lifecycle',
      transitions: { requested: ['approved', 'denied'] },
      initialState: 'requested',
      terminalStates: ['approved', 'denied'],
      triggers: [{ on: 'approved', emit: 'reservation.approved' }],
    });
    expect(prisma.customWorkflow.create).toHaveBeenCalledOnce();
  });
});

describe('CustomDomainsService.runWorkflowTransition', () => {
  it('rejects when no active workflow exists', async () => {
    const prisma = prismaStub();
    (prisma.customRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: RECORD,
      domainId: DOMAIN,
      state: 'requested',
    });
    (prisma.customWorkflow.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = build(prisma);
    await expect(
      svc.runWorkflowTransition(TENANT, RECORD, 'lifecycle', 'approved'),
    ).rejects.toBeInstanceOf(NotFoundException);
  });

  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.customRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: RECORD,
      domainId: DOMAIN,
      state: 'requested',
    });
    (prisma.customWorkflow.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 'wf-1',
      workflowKey: 'lifecycle',
      transitions: { requested: ['approved'] },
      triggers: [],
      initialState: 'requested',
      terminalStates: [],
    });
    const svc = build(prisma);
    await expect(
      svc.runWorkflowTransition(TENANT, RECORD, 'lifecycle', 'returned'),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects transitioning out of a terminal state', async () => {
    const prisma = prismaStub();
    (prisma.customRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: RECORD,
      domainId: DOMAIN,
      state: 'denied',
    });
    (prisma.customWorkflow.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 'wf-1',
      workflowKey: 'lifecycle',
      transitions: { requested: ['approved', 'denied'] },
      triggers: [],
      initialState: 'requested',
      terminalStates: ['denied'],
    });
    const svc = build(prisma);
    await expect(
      svc.runWorkflowTransition(TENANT, RECORD, 'lifecycle', 'approved'),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('moves state and fires the matching trigger emit', async () => {
    const prisma = prismaStub();
    (prisma.customRecord.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: RECORD,
      domainId: DOMAIN,
      state: 'requested',
    });
    (prisma.customWorkflow.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 'wf-1',
      workflowKey: 'lifecycle',
      transitions: { requested: ['approved'] },
      triggers: [{ on: 'approved', emit: 'reservation.approved' }],
      initialState: 'requested',
      terminalStates: ['approved'],
    });
    (prisma.customDomain.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: DOMAIN,
      pluginId: PLUGIN,
    });
    const svc = build(prisma);
    await svc.runWorkflowTransition(TENANT, RECORD, 'lifecycle', 'approved');
    const evCall = (prisma.domainEvent.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { eventName: string };
    };
    expect(evCall.data.eventName).toBe('reservation.approved');
  });
});
