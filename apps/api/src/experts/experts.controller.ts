import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsIn,
  IsInt,
  IsObject,
  IsOptional,
  IsString,
  Min,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import {
  ExpertsService,
  type CredentialKind,
  type ExpertAvailability,
  type ExpertVisibility,
  type MatchState,
  type SubjectKind,
} from './experts.service';

class CreateProfileDto {
  @IsObject() headlineI18n!: Record<string, string>;
  @IsOptional() @IsArray() sdgFocus?: string[];
  @IsOptional() @IsArray() workingLocales?: string[];
  @IsOptional() @IsArray() fieldRegions?: string[];
  @IsOptional() @IsString() @IsIn(['open', 'busy', 'closed']) availability?: ExpertAvailability;
  @IsOptional() @IsString() @IsIn(['public', 'platform-only', 'private']) visibility?: ExpertVisibility;
}

class CredentialDto {
  @IsString()
  @IsIn(['orcid', 'linkedin', 'official_org', 'community-vouched', 'self-reported', 'verified'])
  kind!: CredentialKind;
  @IsString() ref!: string;
}

class SuggestDto {
  @IsString()
  @IsIn(['bizplan', 'impact_study', 'funding_proposal', 'maker_project', 'need_request'])
  subjectKind!: SubjectKind;
  @IsString() subjectId!: string;
  @IsArray() sdgFocus!: string[];
  @IsArray() locales!: string[];
  @IsArray() regions!: string[];
  @IsOptional() @IsInt() @Min(1) topN?: number;
}

class AcceptDto {
  @IsString() @IsIn(['expert', 'owner']) side!: 'expert' | 'owner';
}

class TransitionMatchDto {
  @IsString()
  @IsIn(['suggested', 'invited', 'accepted', 'engaged', 'completed', 'declined', 'cancelled'])
  to!: MatchState;
}

@ApiTags('experts')
@Controller('experts')
export class ExpertsController {
  constructor(private readonly svc: ExpertsService) {}

  @Post('profiles')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create or update your expert profile' })
  async createProfile(@Body() dto: CreateProfileDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createProfile({
      tenantId: auth.tenantId,
      userId: auth.userId,
      headlineI18n: dto.headlineI18n,
      ...(dto.sdgFocus !== undefined ? { sdgFocus: dto.sdgFocus } : {}),
      ...(dto.workingLocales !== undefined ? { workingLocales: dto.workingLocales } : {}),
      ...(dto.fieldRegions !== undefined ? { fieldRegions: dto.fieldRegions } : {}),
      ...(dto.availability !== undefined ? { availability: dto.availability } : {}),
      ...(dto.visibility !== undefined ? { visibility: dto.visibility } : {}),
    });
  }

  @Post('profiles/:id/credentials')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({
    summary: "Add a credential — 'verified' kind requires admin verifier and is granted server-side",
  })
  async addCredential(
    @Param('id') id: string,
    @Body() dto: CredentialDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    // 'verified' kind can only be granted by admins; the controller injects
    // the actor as verifier and the service rejects when missing.
    return this.svc.addCredential({
      tenantId: auth.tenantId,
      expertId: id,
      kind: dto.kind,
      ref: dto.ref,
      ...(dto.kind === 'verified' ? { verifierId: auth.userId } : {}),
    });
  }

  @Post('matches/suggest')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Suggest top-N expert matches for a subject (does NOT auto-message anyone)',
  })
  async suggest(@Body() dto: SuggestDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.suggestMatches(
      auth.tenantId,
      { kind: dto.subjectKind, id: dto.subjectId },
      { sdgFocus: dto.sdgFocus, locales: dto.locales, regions: dto.regions },
      dto.topN ?? 5,
    );
  }

  @Post('matches/:id/accept')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'One-sided accept — contact details unmask only after BOTH sides accept',
  })
  async accept(@Param('id') id: string, @Body() dto: AcceptDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.accept(auth.tenantId, id, dto.side);
  }

  @Post('matches/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a match through accepted → engaged → completed' })
  async transition(@Param('id') id: string, @Body() dto: TransitionMatchDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transitionMatch(auth.tenantId, id, dto.to);
  }
}
