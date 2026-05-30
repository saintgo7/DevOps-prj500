import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
  IsDateString,
  IsIn,
  IsInt,
  IsObject,
  IsOptional,
  IsString,
  Min,
  MinLength,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import {
  FundingService,
  type ContributionKind,
  type ContributionVisibility,
  type FundingModel,
  type FundingState,
} from './funding.service';

class CreateProposalDto {
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; summary: string; plan: string; budget?: string }>;
  @IsArray() sdgFocus!: string[];
  @IsString() region!: string;
  @IsString() @IsIn(['all-or-nothing', 'keep-it-all']) fundingModel!: FundingModel;
  @IsArray() contributionKinds!: ContributionKind[];
  @IsOptional() @IsString() currency?: string;
  @IsInt() @Min(1) softGoalMinor!: number;
  @IsInt() @Min(1) hardGoalMinor!: number;
  @IsDateString() endsAt!: string;
  @IsBoolean() noncommercialNotice!: boolean;
}

class MilestoneDto {
  @IsInt() @Min(1) position!: number;
  @IsString() title!: string;
  @IsString() description!: string;
  @IsInt() @Min(1) amountMinor!: number;
}

class TransitionDto {
  @IsString()
  @IsIn([
    'draft',
    'review',
    'live',
    'funding_locked',
    'completed',
    'reported',
    'cancelled',
    'refunded',
    'paused',
  ])
  to!: FundingState;
}

class ContributeDto {
  @IsOptional() @IsString() backerUserId?: string;
  @IsString() @IsIn(['donation', 'impact-investment', 'in-kind']) kind!: ContributionKind;
  @IsInt() @Min(1) amountMinor!: number;
  @IsString() currency!: string;
  @IsOptional() @IsString() @IsIn(['public', 'pseudonymous', 'private']) visibility?: ContributionVisibility;
  @IsOptional() @IsString() paymentProviderRef?: string;
}

class PauseDto {
  @IsString() @MinLength(30) reason!: string;
}

class FlagDto {
  @IsString() @IsIn(['fraud', 'commercial', 'harm', 'misinformation', 'other'])
  category!: 'fraud' | 'commercial' | 'harm' | 'misinformation' | 'other';
  @IsString() @MinLength(30) reason!: string;
}

@ApiTags('funding')
@Controller('funding/proposals')
export class FundingController {
  constructor(private readonly svc: FundingService) {}

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Create a funding proposal draft (admin/reviewer/contributor; non-commercial obligation)',
  })
  async create(@Body() dto: CreateProposalDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createProposal({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      region: dto.region,
      fundingModel: dto.fundingModel,
      contributionKinds: dto.contributionKinds,
      ...(dto.currency !== undefined ? { currency: dto.currency } : {}),
      softGoalMinor: dto.softGoalMinor,
      hardGoalMinor: dto.hardGoalMinor,
      endsAt: new Date(dto.endsAt),
      noncommercialNotice: dto.noncommercialNotice,
    });
  }

  @Post(':id/milestones')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Add a milestone (only allowed in draft/review)' })
  async addMilestone(@Param('id') id: string, @Body() dto: MilestoneDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.addMilestone(auth.tenantId, id, {
      position: dto.position,
      title: dto.title,
      description: dto.description,
      amountMinor: dto.amountMinor,
    });
  }

  @Post(':id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a proposal through its lifecycle (admin)' })
  async transition(@Param('id') id: string, @Body() dto: TransitionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transition(auth.tenantId, id, dto.to, auth.userId);
  }

  @Post(':id/contributions')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Record a pending contribution; payment partner webhook flips to collected',
  })
  async contribute(@Param('id') id: string, @Body() dto: ContributeDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.contribute({
      tenantId: auth.tenantId,
      proposalId: id,
      backerUserId: dto.backerUserId ?? auth.userId,
      kind: dto.kind,
      amountMinor: dto.amountMinor,
      currency: dto.currency,
      ...(dto.visibility !== undefined ? { visibility: dto.visibility } : {}),
      ...(dto.paymentProviderRef !== undefined ? { paymentProviderRef: dto.paymentProviderRef } : {}),
    });
  }

  @Post(':id/pause')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Pause a live proposal (super-admin only; reason recorded forever)',
  })
  async pause(@Param('id') id: string, @Body() dto: PauseDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.pause(auth.tenantId, id, auth.userId, dto.reason);
  }

  @Post(':id/flags')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Flag a proposal — drives super-admin review' })
  async flag(@Param('id') id: string, @Body() dto: FlagDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.flag(auth.tenantId, id, auth.userId, dto.category, dto.reason);
  }
}
