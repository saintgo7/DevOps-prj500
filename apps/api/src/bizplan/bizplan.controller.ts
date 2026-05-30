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
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import {
  BizPlanService,
  SECTION_KINDS,
  TRACKS,
  type PlanState,
  type PlanTrack,
  type SectionKind,
} from './bizplan.service';

class CreatePlanDto {
  @IsString() @IsIn([...TRACKS]) track!: PlanTrack;
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; audience?: string; periodLabel?: string }>;
  @IsArray() sdgFocus!: string[];
  @IsOptional() @IsArray() applicableRegions?: string[];
  @IsInt() @Min(1) periodMonths!: number;
  @IsOptional() @IsString() audienceLabel?: string;
  @IsBoolean() noncommercialNotice!: boolean;
}

class SectionDto {
  @IsInt() @Min(1) position!: number;
  @IsString() @IsIn([...SECTION_KINDS]) kind!: SectionKind;
  @IsObject() bodyI18n!: Record<string, string>;
  @IsOptional() @IsInt() @Min(0) @Max(100) plainLanguageScore?: number;
  @IsOptional() @IsObject() aiProvenance?: {
    model: string;
    promptVersion: string;
    generatedAt: string;
    tokensIn?: number;
    tokensOut?: number;
  };
}

class SourceRefDto {
  @IsInt() @Min(1) position!: number;
  @IsString() rendered!: string;
  @IsOptional() @IsString() sourceWatchItemId?: string;
  @IsOptional() @IsString() sourceColumnId?: string;
  @IsOptional() @IsString() sourcePatentInsightId?: string;
  @IsOptional() @IsString() sourceManuscriptId?: string;
  @IsOptional() @IsString() externalDoi?: string;
  @IsOptional() @IsString() externalUrl?: string;
}

class TransitionDto {
  @IsString()
  @IsIn(['drafting', 'ai_drafted', 'human_review', 'revising', 'ready_for_use', 'archived'])
  to!: PlanState;
}

@ApiTags('bizplan')
@Controller('bizplan')
export class BizPlanController {
  constructor(private readonly svc: BizPlanService) {}

  @Post('plans')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a BizPlan draft (non-commercial obligation)' })
  async create(@Body() dto: CreatePlanDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createPlan({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      track: dto.track,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      ...(dto.applicableRegions !== undefined ? { applicableRegions: dto.applicableRegions } : {}),
      periodMonths: dto.periodMonths,
      ...(dto.audienceLabel !== undefined ? { audienceLabel: dto.audienceLabel } : {}),
      noncommercialNotice: dto.noncommercialNotice,
    });
  }

  @Post('plans/:id/sections')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Upsert a section (AI-assisted or human-authored)' })
  async upsertSection(@Param('id') id: string, @Body() dto: SectionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.upsertSection(auth.tenantId, id, {
      position: dto.position,
      kind: dto.kind,
      bodyI18n: dto.bodyI18n,
      ...(dto.plainLanguageScore !== undefined ? { plainLanguageScore: dto.plainLanguageScore } : {}),
      ...(dto.aiProvenance !== undefined ? { aiProvenance: dto.aiProvenance } : {}),
    });
  }

  @Post('sections/:id/source-refs')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Attach a citation (exactly one source per ref)' })
  async addSourceRef(@Param('id') id: string, @Body() dto: SourceRefDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.addSourceRef(auth.tenantId, id, {
      position: dto.position,
      rendered: dto.rendered,
      ...(dto.sourceWatchItemId !== undefined ? { sourceWatchItemId: dto.sourceWatchItemId } : {}),
      ...(dto.sourceColumnId !== undefined ? { sourceColumnId: dto.sourceColumnId } : {}),
      ...(dto.sourcePatentInsightId !== undefined ? { sourcePatentInsightId: dto.sourcePatentInsightId } : {}),
      ...(dto.sourceManuscriptId !== undefined ? { sourceManuscriptId: dto.sourceManuscriptId } : {}),
      ...(dto.externalDoi !== undefined ? { externalDoi: dto.externalDoi } : {}),
      ...(dto.externalUrl !== undefined ? { externalUrl: dto.externalUrl } : {}),
    });
  }

  @Post('plans/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a plan through its lifecycle' })
  async transition(@Param('id') id: string, @Body() dto: TransitionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transition(auth.tenantId, id, dto.to);
  }
}
