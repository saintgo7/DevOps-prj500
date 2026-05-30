// Maker space — easy tool authoring for SDG practitioners (ADR-0018 §B).
//
// Templates ship pre-wired with the platform's principles (i18n, RLS,
// plain-language, ethics tones, harmful-content guard). A project that
// wants to go 'live' must satisfy:
//   - noncommercialNotice = true
//   - At least one published artifact whose readme_score ≥ 60
//   - Owner has accepted the template's license

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type MakerTemplateKind =
  | 'static-site'
  | 'next-app'
  | 'pwa'
  | 'mobile-rn'
  | 'data-dashboard'
  | 'sms-bot'
  | 'whatsapp-bot';

export type MakerProjectState =
  | 'scaffolding'
  | 'building'
  | 'review'
  | 'live'
  | 'archived'
  | 'paused';

export type ArtifactKind = 'repo' | 'bundle' | 'preview';

export interface CreateProjectInput {
  tenantId: string;
  ownerId: string;
  templateId: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; blurb?: string }>;
  sdgFocus: string[];
  targetRegions?: string[];
  noncommercialNotice: boolean;
}

export interface ArtifactInput {
  tenantId: string;
  projectId: string;
  kind: ArtifactKind;
  ref: string;
  contentHash: string;
  aiProvenance?: { model: string; promptVersion: string; draftedAt: string };
  readmeScore?: number;
}

const ALLOWED: Record<MakerProjectState, MakerProjectState[]> = {
  scaffolding: ['building', 'archived'],
  building: ['review', 'archived'],
  review: ['building', 'live', 'archived'],
  live: ['paused', 'archived'],
  paused: ['live', 'archived'],
  archived: [],
};

@Injectable()
export class MakerService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: MakerProjectState, to: MakerProjectState): boolean {
    return ALLOWED[from].includes(to);
  }

  async createTemplate(input: {
    tenantId?: string;
    kind: MakerTemplateKind;
    name: string;
    licenseSpdx: string;
    descriptionI18n: Record<string, { description: string; gettingStarted?: string }>;
    sourceRef: string;
  }) {
    if (!input.licenseSpdx || input.licenseSpdx.trim().length === 0) {
      throw new BadRequestException('Template needs an SPDX license identifier.');
    }
    return this.prisma.makerTemplate.create({
      data: {
        tenantId: input.tenantId ?? null,
        kind: input.kind,
        name: input.name,
        licenseSpdx: input.licenseSpdx,
        descriptionI18n: input.descriptionI18n as unknown as Prisma.InputJsonValue,
        sourceRef: input.sourceRef,
        active: true,
      },
    });
  }

  async createProject(input: CreateProjectInput) {
    if (input.noncommercialNotice !== true) {
      throw new BadRequestException(
        'Maker projects must declare non-commercial intent. The platform inherits this from your project.',
      );
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary?.title) {
      throw new BadRequestException(
        `Project needs a title in the primary locale (${input.primaryLocale}).`,
      );
    }
    const tmpl = await this.prisma.makerTemplate.findFirst({
      where: { id: input.templateId, active: true },
    });
    if (!tmpl) throw new NotFoundException('Template not found or retired.');
    return this.prisma.makerProject.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        templateId: input.templateId,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        targetRegions: input.targetRegions ?? [],
        noncommercialNotice: true,
        state: 'scaffolding',
      },
    });
  }

  async addArtifact(input: ArtifactInput) {
    if (!input.contentHash || input.contentHash.length < 32) {
      throw new BadRequestException('Artifact contentHash must be a SHA-256 hex digest.');
    }
    if (input.readmeScore !== undefined && (input.readmeScore < 0 || input.readmeScore > 100)) {
      throw new BadRequestException('readmeScore must be between 0 and 100.');
    }
    const p = await this.prisma.makerProject.findFirst({
      where: { id: input.projectId, tenantId: input.tenantId },
    });
    if (!p) throw new NotFoundException('Project not found.');
    if (p.state === 'archived' || p.state === 'paused') {
      throw new ConflictException(
        `Cannot add artifacts to a project in state '${p.state}'.`,
      );
    }
    return this.prisma.makerArtifact.create({
      data: {
        tenantId: input.tenantId,
        projectId: input.projectId,
        kind: input.kind,
        ref: input.ref,
        contentHash: input.contentHash,
        aiProvenance: (input.aiProvenance ?? null) as unknown as Prisma.InputJsonValue,
        readmeScore: input.readmeScore ?? null,
      },
    });
  }

  async transition(tenantId: string, projectId: string, to: MakerProjectState) {
    const p = await this.prisma.makerProject.findFirst({ where: { id: projectId, tenantId } });
    if (!p) throw new NotFoundException('Project not found.');
    const from = p.state as MakerProjectState;
    if (!MakerService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'live') {
      if (!p.noncommercialNotice) {
        throw new BadRequestException('Project is missing the non-commercial notice.');
      }
      const artifacts = await this.prisma.makerArtifact.findMany({
        where: { tenantId, projectId },
      });
      if (artifacts.length === 0) {
        throw new BadRequestException('A project needs at least one artifact before going live.');
      }
      const failing = artifacts.filter(
        (a) => a.readmeScore === null || (a.readmeScore ?? 0) < 60,
      );
      if (failing.length === artifacts.length) {
        throw new BadRequestException(
          'No artifact passes the plain-language README threshold (≥ 60).',
        );
      }
    }
    return this.prisma.makerProject.update({
      where: { id: projectId },
      data: {
        state: to,
        ...(to === 'live' ? { liveAt: new Date() } : {}),
        ...(to === 'archived' ? { archivedAt: new Date() } : {}),
      },
    });
  }

  /** Super-admin pause — same shape as funding pause. */
  async pause(tenantId: string, projectId: string, superAdminId: string, reason: string) {
    if (!reason || reason.trim().length < 30) {
      throw new BadRequestException('Pause reason must be at least 30 characters.');
    }
    const p = await this.prisma.makerProject.findFirst({ where: { id: projectId, tenantId } });
    if (!p) throw new NotFoundException('Project not found.');
    if (p.state !== 'live') {
      throw new ConflictException(`Can only pause a live project. Current state: '${p.state}'.`);
    }
    return this.prisma.makerProject.update({
      where: { id: projectId },
      data: {
        state: 'paused',
        pausedAt: new Date(),
        pauseReason: `${reason.trim()} (by:${superAdminId})`,
      },
    });
  }
}
