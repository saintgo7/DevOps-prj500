import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
  IsIn,
  IsInt,
  IsOptional,
  IsString,
  Min,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import { FeasibilityService } from './feasibility.service';
import type { PlanInputs } from './scoring';

class ComputeDto {
  @IsBoolean() noncommercialNotice!: boolean;
  @IsArray() sdgFocus!: string[];
  @IsArray() applicableRegions!: string[];
  @IsInt() @Min(1) periodMonths!: number;
  @IsInt() @Min(0) budgetTotalMinor!: number;
  @IsInt() @Min(0) milestoneSumMinor!: number;
  @IsInt() trl!: number;
  @IsBoolean() harmfulContentBlocked!: boolean;
  @IsArray() citedSourceSdgs!: string[];
  @IsArray() citationSourceKinds!: Array<'watch' | 'column' | 'patent' | 'manuscript' | 'doi' | 'url'>;
  @IsInt() @Min(0) citationCount!: number;
  @IsInt() @Min(0) estimatedBeneficiaries!: number;
  @IsOptional() @IsString() @IsIn(['deterministic-only', 'human-adjusted'])
  reviewMode?: 'deterministic-only' | 'human-adjusted';
}

class ReviewDto {
  @IsString() @IsIn(['approve', 'request_changes', 'reject'])
  decision!: 'approve' | 'request_changes' | 'reject';
  @IsBoolean() domainExpert!: boolean;
  @IsOptional() @IsString() comment?: string;
}

@ApiTags('feasibility')
@Controller('feasibility')
export class FeasibilityController {
  constructor(private readonly svc: FeasibilityService) {}

  @Post('plans/:planId/compute')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Compute (or recompute) the 6-axis feasibility snapshot for a plan',
  })
  async compute(@Param('planId') planId: string, @Body() dto: ComputeDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const inputs: PlanInputs = {
      noncommercialNotice: dto.noncommercialNotice,
      sdgFocus: dto.sdgFocus,
      applicableRegions: dto.applicableRegions,
      periodMonths: dto.periodMonths,
      budgetTotalMinor: dto.budgetTotalMinor,
      milestoneSumMinor: dto.milestoneSumMinor,
      trl: dto.trl,
      harmfulContentBlocked: dto.harmfulContentBlocked,
      citedSourceSdgs: dto.citedSourceSdgs,
      citationSourceKinds: dto.citationSourceKinds,
      citationCount: dto.citationCount,
      estimatedBeneficiaries: dto.estimatedBeneficiaries,
    };
    return this.svc.compute(auth.tenantId, planId, inputs, dto.reviewMode ?? 'deterministic-only');
  }

  @Post(':feasibilityId/reviews')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Append a human review (append-only ledger)' })
  async addReview(
    @Param('feasibilityId') feasibilityId: string,
    @Body() dto: ReviewDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.addReview(
      auth.tenantId,
      feasibilityId,
      auth.userId,
      dto.decision,
      dto.domainExpert,
      dto.comment,
    );
  }
}
