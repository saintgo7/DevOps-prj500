import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { PluginsService, type CreateManifestInput } from './plugins.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const PLUGIN = '33333333-3333-3333-3333-333333333333';
const ACTOR = '44444444-4444-4444-4444-444444444444';
const TOKEN = '55555555-5555-5555-5555-555555555555';

function manifestInput(overrides: Partial<CreateManifestInput> = {}): CreateManifestInput {
  return {
    tenantId: TENANT,
    ownerUserId: OWNER,
    pluginKey: 'biodiv-monitor',
    name: 'Biodiversity monitor',
    version: '0.1.0',
    authorEmail: 'maintainer@example.com',
    requestedScopes: ['custom-domain.write', 'event.subscribe'],
    governanceTier: 'standard',
    noncommercialPledge: true,
    plainLanguagePledge: true,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const manifest = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: PLUGIN, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const token = {
    create: vi.fn(({ data }: { data: unknown }) =>
      Promise.resolve({ id: TOKEN, ...(data as object) }),
    ),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  return {
    pluginManifest: manifest,
    capabilityToken: token,
  } as unknown as PrismaService;
}

describe('PluginsService.canTransition', () => {
  it('allows draft → review', () => {
    expect(PluginsService.canTransition('draft', 'review')).toBe(true);
  });
  it('forbids retired → anything', () => {
    expect(PluginsService.canTransition('retired', 'approved')).toBe(false);
  });
  it('allows approved ↔ paused', () => {
    expect(PluginsService.canTransition('approved', 'paused')).toBe(true);
    expect(PluginsService.canTransition('paused', 'approved')).toBe(true);
  });
});

describe('PluginsService.computeManifestHash', () => {
  it('is stable across scope ordering', () => {
    const a = PluginsService.computeManifestHash(
      manifestInput({ requestedScopes: ['a', 'b'] }),
    );
    const b = PluginsService.computeManifestHash(
      manifestInput({ requestedScopes: ['b', 'a'] }),
    );
    expect(a).toBe(b);
  });

  it('changes when version changes', () => {
    const a = PluginsService.computeManifestHash(manifestInput({ version: '0.1.0' }));
    const b = PluginsService.computeManifestHash(manifestInput({ version: '0.2.0' }));
    expect(a).not.toBe(b);
  });
});

describe('PluginsService.createManifest', () => {
  it('rejects without non-commercial pledge', async () => {
    const svc = new PluginsService(prismaStub());
    await expect(
      svc.createManifest(manifestInput({ noncommercialPledge: false })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects without plain-language pledge', async () => {
    const svc = new PluginsService(prismaStub());
    await expect(
      svc.createManifest(manifestInput({ plainLanguagePledge: false })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects malformed pluginKey', async () => {
    const svc = new PluginsService(prismaStub());
    await expect(svc.createManifest(manifestInput({ pluginKey: 'A' }))).rejects.toBeInstanceOf(
      BadRequestException,
    );
    await expect(
      svc.createManifest(manifestInput({ pluginKey: 'has space' })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects non-semver version', async () => {
    const svc = new PluginsService(prismaStub());
    await expect(
      svc.createManifest(manifestInput({ version: 'next' })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a draft manifest with computed hash', async () => {
    const prisma = prismaStub();
    const svc = new PluginsService(prisma);
    await svc.createManifest(manifestInput());
    const call = (prisma.pluginManifest.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { manifestHash: string; state: string };
    };
    expect(call.data.manifestHash).toMatch(/^[a-f0-9]{64}$/);
    expect(call.data.state).toBe('draft');
  });
});

describe('PluginsService.transition', () => {
  it('rejects illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'draft',
    });
    const svc = new PluginsService(prisma);
    await expect(svc.transition(TENANT, PLUGIN, 'approved', ACTOR)).rejects.toBeInstanceOf(
      ConflictException,
    );
  });

  it('rejects pause without sufficient reason', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new PluginsService(prisma);
    await expect(
      svc.transition(TENANT, PLUGIN, 'paused', ACTOR, 'short'),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('moves review → approved with approvedAt + approvedBy', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'review',
    });
    (prisma.pluginManifest.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new PluginsService(prisma);
    await svc.transition(TENANT, PLUGIN, 'approved', ACTOR);
    const call = (prisma.pluginManifest.update as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { approvedAt: Date; approvedBy: string };
    };
    expect(call.data.approvedAt).toBeInstanceOf(Date);
    expect(call.data.approvedBy).toBe(ACTOR);
  });
});

describe('PluginsService.issueToken', () => {
  it('rejects when plugin is not approved', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'draft',
      requestedScopes: ['event.subscribe'],
    });
    const svc = new PluginsService(prisma);
    await expect(
      svc.issueToken(TENANT, PLUGIN, ['event.subscribe']),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects scope outside the manifest requested set', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
      requestedScopes: ['event.subscribe'],
    });
    const svc = new PluginsService(prisma);
    await expect(
      svc.issueToken(TENANT, PLUGIN, ['custom-domain.delete']),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('issues a raw token, persists only the hash', async () => {
    const prisma = prismaStub();
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
      requestedScopes: ['event.subscribe'],
    });
    const svc = new PluginsService(prisma);
    const issued = await svc.issueToken(TENANT, PLUGIN, ['event.subscribe']);
    expect(issued.raw.startsWith('sdgi_pat_')).toBe(true);
    const call = (prisma.capabilityToken.create as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as {
      data: { tokenHash: string };
    };
    expect(call.data.tokenHash).toMatch(/^[a-f0-9]{64}$/);
    expect(call.data.tokenHash).not.toBe(issued.raw);
  });
});

describe('PluginsService.resolveToken', () => {
  it('returns null on unknown raw', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new PluginsService(prisma);
    const out = await svc.resolveToken('sdgi_pat_nope');
    expect(out).toBeNull();
  });

  it('returns null on revoked token', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      tenantId: TENANT,
      pluginId: PLUGIN,
      grantedScopes: ['event.subscribe'],
      revokedAt: new Date(Date.now() - 1000),
      expiresAt: new Date(Date.now() + 1_000_000),
    });
    const svc = new PluginsService(prisma);
    expect(await svc.resolveToken('sdgi_pat_x')).toBeNull();
  });

  it('returns null on expired token', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      tenantId: TENANT,
      pluginId: PLUGIN,
      grantedScopes: ['event.subscribe'],
      revokedAt: null,
      expiresAt: new Date(Date.now() - 1000),
    });
    const svc = new PluginsService(prisma);
    expect(await svc.resolveToken('sdgi_pat_x')).toBeNull();
  });

  it('returns null when plugin is paused', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      tenantId: TENANT,
      pluginId: PLUGIN,
      grantedScopes: ['event.subscribe'],
      revokedAt: null,
      expiresAt: new Date(Date.now() + 1_000_000),
    });
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'paused',
    });
    const svc = new PluginsService(prisma);
    expect(await svc.resolveToken('sdgi_pat_x')).toBeNull();
  });

  it('returns scope info on a healthy approved plugin', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      tenantId: TENANT,
      pluginId: PLUGIN,
      grantedScopes: ['event.subscribe'],
      revokedAt: null,
      expiresAt: new Date(Date.now() + 1_000_000),
    });
    (prisma.pluginManifest.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PLUGIN,
      state: 'approved',
    });
    const svc = new PluginsService(prisma);
    const out = await svc.resolveToken('sdgi_pat_x');
    expect(out).toEqual({
      tenantId: TENANT,
      pluginId: PLUGIN,
      grantedScopes: ['event.subscribe'],
    });
  });
});

describe('PluginsService.revokeToken', () => {
  it('NotFound when missing', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new PluginsService(prisma);
    await expect(svc.revokeToken(TENANT, TOKEN)).rejects.toBeInstanceOf(NotFoundException);
  });

  it('is idempotent on already-revoked tokens', async () => {
    const prisma = prismaStub();
    (prisma.capabilityToken.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: TOKEN,
      revokedAt: new Date(Date.now() - 1000),
    });
    const svc = new PluginsService(prisma);
    await svc.revokeToken(TENANT, TOKEN);
    expect(prisma.capabilityToken.update).not.toHaveBeenCalled();
  });
});
