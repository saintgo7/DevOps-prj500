import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
  IsIn,
  IsInt,
  IsObject,
  IsOptional,
  IsString,
  Max,
  Min,
  MinLength,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import {
  MakerService,
  type ArtifactKind,
  type MakerProjectState,
  type MakerTemplateKind,
} from './maker.service';

class CreateTemplateDto {
  @IsString()
  @IsIn(['static-site', 'next-app', 'pwa', 'mobile-rn', 'data-dashboard', 'sms-bot', 'whatsapp-bot'])
  kind!: MakerTemplateKind;
  @IsString() name!: string;
  @IsString() licenseSpdx!: string;
  @IsObject() descriptionI18n!: Record<string, { description: string; gettingStarted?: string }>;
  @IsString() sourceRef!: string;
}

class CreateProjectDto {
  @IsString() templateId!: string;
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; blurb?: string }>;
  @IsArray() sdgFocus!: string[];
  @IsOptional() @IsArray() targetRegions?: string[];
  @IsBoolean() noncommercialNotice!: boolean;
}

class ArtifactDto {
  @IsString() @IsIn(['repo', 'bundle', 'preview']) kind!: ArtifactKind;
  @IsString() ref!: string;
  @IsString() @MinLength(32) contentHash!: string;
  @IsOptional() @IsObject() aiProvenance?: { model: string; promptVersion: string; draftedAt: string };
  @IsOptional() @IsInt() @Min(0) @Max(100) readmeScore?: number;
}

class TransitionDto {
  @IsString()
  @IsIn(['scaffolding', 'building', 'review', 'live', 'archived', 'paused'])
  to!: MakerProjectState;
}

class PauseDto {
  @IsString() @MinLength(30) reason!: string;
}

@ApiTags('maker')
@Controller('maker')
export class MakerController {
  constructor(private readonly svc: MakerService) {}

  @Post('templates')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin', 'admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Register a maker template (super-admin / admin)' })
  async createTemplate(@Body() dto: CreateTemplateDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createTemplate({
      tenantId: auth.tenantId,
      kind: dto.kind,
      name: dto.name,
      licenseSpdx: dto.licenseSpdx,
      descriptionI18n: dto.descriptionI18n,
      sourceRef: dto.sourceRef,
    });
  }

  @Post('projects')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Start a maker project from a template' })
  async createProject(@Body() dto: CreateProjectDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createProject({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      templateId: dto.templateId,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      ...(dto.targetRegions !== undefined ? { targetRegions: dto.targetRegions } : {}),
      noncommercialNotice: dto.noncommercialNotice,
    });
  }

  @Post('projects/:id/artifacts')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Attach an artifact (repo / bundle / preview)' })
  async addArtifact(@Param('id') id: string, @Body() dto: ArtifactDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.addArtifact({
      tenantId: auth.tenantId,
      projectId: id,
      kind: dto.kind,
      ref: dto.ref,
      contentHash: dto.contentHash,
      ...(dto.aiProvenance !== undefined ? { aiProvenance: dto.aiProvenance } : {}),
      ...(dto.readmeScore !== undefined ? { readmeScore: dto.readmeScore } : {}),
    });
  }

  @Post('projects/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a project through its lifecycle (admin)' })
  async transition(@Param('id') id: string, @Body() dto: TransitionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transition(auth.tenantId, id, dto.to);
  }

  @Post('projects/:id/pause')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Pause a live project (super-admin)' })
  async pause(@Param('id') id: string, @Body() dto: PauseDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.pause(auth.tenantId, id, auth.userId, dto.reason);
  }
}
