import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsIn,
  IsObject,
  IsOptional,
  IsString,
  MinLength,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import { ManuscriptsService, type ManuscriptState } from './manuscripts.service';

class CreateDto {
  @IsString() @IsIn(['nature', 'ssci']) tier!: 'nature' | 'ssci';
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; scientificAbstract: string }>;
  @IsArray() sdgFocus!: string[];
  @IsOptional() @IsArray() applicableRegions?: string[];
}

class TransitionDto {
  @IsString()
  @IsIn([
    'draft',
    'internal_review',
    'external_peer_review',
    'revise_requested',
    'accepted',
    'published',
    'withdrawn',
  ])
  to!: ManuscriptState;
}

class WithdrawDto {
  @IsString() @MinLength(8) reason!: string;
}

class PublishDto {
  @IsArray() citations!: Array<{
    position: number;
    rendered: string;
    sourceColumnId?: string;
    sourceManuscriptId?: string;
    sourcePatentInsightId?: string;
    sourceWatchItemId?: string;
    externalDoi?: string;
    externalUrl?: string;
  }>;
  @IsObject() plainLanguageSummary!: Record<string, string>;
  @IsOptional() @IsString() selfCiteOverrideReason?: string;
}

@ApiTags('research-manuscripts')
@Controller('research/manuscripts')
export class ManuscriptsController {
  constructor(private readonly svc: ManuscriptsService) {}

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a manuscript draft (admin/reviewer/contributor)' })
  async create(@Body() dto: CreateDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.create({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      tier: dto.tier,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      ...(dto.applicableRegions !== undefined ? { applicableRegions: dto.applicableRegions } : {}),
    });
  }

  @Post(':id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a manuscript through its review lifecycle' })
  async transition(
    @Param('id') id: string,
    @Body() dto: TransitionDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transition(auth.tenantId, id, dto.to);
  }

  @Post(':id/publish')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Publish an accepted manuscript (admin) — citations are frozen at this point',
  })
  async publish(
    @Param('id') id: string,
    @Body() dto: PublishDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.publish(auth.tenantId, id, {
      citations: dto.citations,
      plainLanguageSummary: dto.plainLanguageSummary,
      ...(dto.selfCiteOverrideReason !== undefined
        ? { selfCiteOverrideReason: dto.selfCiteOverrideReason }
        : {}),
    });
  }

  @Post(':id/withdraw')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'super-admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Withdraw a manuscript (admin / super-admin)' })
  async withdraw(
    @Param('id') id: string,
    @Body() dto: WithdrawDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.withdraw(auth.tenantId, id, dto.reason);
  }
}
