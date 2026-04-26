import { describe, expect, it, vi } from 'vitest';
import { BadRequestException, ConflictException, NotFoundException } from '@nestjs/common';
import type { PrismaService } from '../prisma/prisma.service';
import { MakerService, type CreateProjectInput } from './maker.service';

const TENANT = '11111111-1111-1111-1111-111111111111';
const OWNER = '22222222-2222-2222-2222-222222222222';
const TMPL = '33333333-3333-3333-3333-333333333333';
const PROJ = '44444444-4444-4444-4444-444444444444';
const ACTOR = '55555555-5555-5555-5555-555555555555';
const HASH = 'a'.repeat(64);

function project(overrides: Partial<CreateProjectInput> = {}): CreateProjectInput {
  return {
    tenantId: TENANT,
    ownerId: OWNER,
    templateId: TMPL,
    primaryLocale: 'ko',
    bodyI18n: { ko: { title: '농촌 정수기 모니터링 PWA' } },
    sdgFocus: ['SDG-6'],
    targetRegions: ['BD', 'TZ'],
    noncommercialNotice: true,
    ...overrides,
  };
}

function prismaStub(): PrismaService {
  const tmpl = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: TMPL, ...(data as object) })),
    findFirst: vi.fn().mockResolvedValue({ id: TMPL, active: true }),
  };
  const proj = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve({ id: PROJ, ...(data as object) })),
    findFirst: vi.fn(),
    update: vi.fn(),
  };
  const art = {
    create: vi.fn(({ data }: { data: unknown }) => Promise.resolve(data)),
    findMany: vi.fn().mockResolvedValue([]),
  };
  return {
    makerTemplate: tmpl,
    makerProject: proj,
    makerArtifact: art,
  } as unknown as PrismaService;
}

describe('MakerService.canTransition', () => {
  it('allows scaffolding → building', () => {
    expect(MakerService.canTransition('scaffolding', 'building')).toBe(true);
  });
  it('forbids archived → live', () => {
    expect(MakerService.canTransition('archived', 'live')).toBe(false);
  });
});

describe('MakerService.createTemplate', () => {
  it('rejects without an SPDX licence', async () => {
    const svc = new MakerService(prismaStub());
    await expect(
      svc.createTemplate({
        kind: 'next-app',
        name: 'starter',
        licenseSpdx: '',
        descriptionI18n: { en: { description: 'A starter.' } },
        sourceRef: 'https://example/starter',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('creates a global template (no tenantId) when valid', async () => {
    const prisma = prismaStub();
    const svc = new MakerService(prisma);
    await svc.createTemplate({
      kind: 'next-app',
      name: 'starter',
      licenseSpdx: 'MIT',
      descriptionI18n: { en: { description: 'A starter.' } },
      sourceRef: 'https://example/starter',
    });
    expect(prisma.makerTemplate.create).toHaveBeenCalledOnce();
  });
});

describe('MakerService.createProject', () => {
  it('rejects when noncommercialNotice is false', async () => {
    const svc = new MakerService(prismaStub());
    await expect(
      svc.createProject(project({ noncommercialNotice: false })),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects when template is missing', async () => {
    const prisma = prismaStub();
    (prisma.makerTemplate.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue(null);
    const svc = new MakerService(prisma);
    await expect(svc.createProject(project())).rejects.toBeInstanceOf(NotFoundException);
  });

  it('creates a scaffolding project when valid', async () => {
    const prisma = prismaStub();
    const svc = new MakerService(prisma);
    const out = await svc.createProject(project());
    expect(out).toBeDefined();
    expect(prisma.makerProject.create).toHaveBeenCalledOnce();
  });
});

describe('MakerService.addArtifact', () => {
  it('rejects a short content hash', async () => {
    const svc = new MakerService(prismaStub());
    await expect(
      svc.addArtifact({
        tenantId: TENANT,
        projectId: PROJ,
        kind: 'repo',
        ref: 'git://x',
        contentHash: 'too-short',
      }),
    ).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects adding to an archived project', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'archived',
    });
    const svc = new MakerService(prisma);
    await expect(
      svc.addArtifact({
        tenantId: TENANT,
        projectId: PROJ,
        kind: 'repo',
        ref: 'git://x',
        contentHash: HASH,
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('records an artifact when valid', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'building',
    });
    const svc = new MakerService(prisma);
    await svc.addArtifact({
      tenantId: TENANT,
      projectId: PROJ,
      kind: 'preview',
      ref: 'https://preview.example',
      contentHash: HASH,
      readmeScore: 75,
    });
    expect(prisma.makerArtifact.create).toHaveBeenCalledOnce();
  });
});

describe('MakerService.transition', () => {
  it('rejects an illegal transition', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'scaffolding',
      noncommercialNotice: true,
    });
    const svc = new MakerService(prisma);
    await expect(svc.transition(TENANT, PROJ, 'live')).rejects.toBeInstanceOf(ConflictException);
  });

  it('rejects live without artifacts', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'review',
      noncommercialNotice: true,
    });
    (prisma.makerArtifact.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([]);
    const svc = new MakerService(prisma);
    await expect(svc.transition(TENANT, PROJ, 'live')).rejects.toBeInstanceOf(BadRequestException);
  });

  it('rejects live when no artifact passes README ≥ 60', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'review',
      noncommercialNotice: true,
    });
    (prisma.makerArtifact.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { readmeScore: 30 },
      { readmeScore: null },
    ]);
    const svc = new MakerService(prisma);
    await expect(svc.transition(TENANT, PROJ, 'live')).rejects.toBeInstanceOf(BadRequestException);
  });

  it('goes live when at least one artifact passes README ≥ 60', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'review',
      noncommercialNotice: true,
    });
    (prisma.makerArtifact.findMany as ReturnType<typeof vi.fn>).mockResolvedValue([
      { readmeScore: 30 },
      { readmeScore: 80 },
    ]);
    (prisma.makerProject.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'live',
    });
    const svc = new MakerService(prisma);
    const out = (await svc.transition(TENANT, PROJ, 'live')) as { state: string };
    expect(out.state).toBe('live');
  });
});

describe('MakerService.pause', () => {
  it('rejects pausing a non-live project', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'building',
    });
    const svc = new MakerService(prisma);
    await expect(
      svc.pause(TENANT, PROJ, ACTOR, 'A long enough reason for pausing the live project here.'),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('pauses a live project', async () => {
    const prisma = prismaStub();
    (prisma.makerProject.findFirst as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'live',
    });
    (prisma.makerProject.update as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: PROJ,
      state: 'paused',
    });
    const svc = new MakerService(prisma);
    const out = (await svc.pause(
      TENANT,
      PROJ,
      ACTOR,
      'A long enough reason for pausing the live project here.',
    )) as { state: string };
    expect(out.state).toBe('paused');
  });
});
