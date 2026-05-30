import { Body, Controller, Delete, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
  IsDateString,
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
import { ConsentService, type ConsentLevel, type ConsentScope } from './consent.service';
import { StudiesService, type StudyState } from './studies.service';

class ConsentDto {
  @IsObject() scope!: ConsentScope;
  @IsString() @IsIn(['aggregate-only', 'longitudinal']) level!: ConsentLevel;
  @IsString() @MinLength(1) consentVersion!: string;
  @IsString() @MinLength(30) agreedClauseText!: string;
}

class CreateStudyDto {
  @IsString() title!: string;
  @IsString() hypothesis!: string;
  @IsString() method!: string;
  @IsArray() sdgFocus!: string[];
  @IsArray() regions!: string[];
  @IsArray() topicTags!: string[];
  @IsDateString() windowStart!: string;
  @IsDateString() windowEnd!: string;
  @IsOptional() @IsBoolean() sensitiveTopic?: boolean;
}

class TransitionStudyDto {
  @IsString()
  @IsIn(['draft', 'enrolling', 'analysing', 'review', 'published', 'retired'])
  to!: StudyState;
}

class DiscloseDto {
  @IsString() @IsIn(['atom', 'webhook', 'export']) channel!: 'atom' | 'webhook' | 'export';
  @IsOptional() @IsString() recipient?: string;
}

@ApiTags('impact')
@Controller('impact')
export class ImpactController {
  constructor(
    private readonly consent: ConsentService,
    private readonly studies: StudiesService,
  ) {}

  @Post('consent')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary:
      'Opt in to inclusion in SDG impact studies (any signed-in user; revocable any time)',
  })
  async optIn(@Body() dto: ConsentDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.consent.record({
      tenantId: auth.tenantId,
      userId: auth.userId,
      scope: dto.scope,
      level: dto.level,
      consentVersion: dto.consentVersion,
      agreedClauseText: dto.agreedClauseText,
    });
  }

  @Delete('consent/:id')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Revoke a consent record (the user themselves)' })
  async revoke(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.consent.revoke(auth.tenantId, id);
  }

  @Post('studies')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create an impact study (admin/reviewer)' })
  async createStudy(@Body() dto: CreateStudyDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.studies.create({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      title: dto.title,
      hypothesis: dto.hypothesis,
      method: dto.method,
      sdgFocus: dto.sdgFocus,
      regions: dto.regions,
      topicTags: dto.topicTags,
      windowStart: new Date(dto.windowStart),
      windowEnd: new Date(dto.windowEnd),
      ...(dto.sensitiveTopic !== undefined ? { sensitiveTopic: dto.sensitiveTopic } : {}),
    });
  }

  @Post('studies/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a study through its lifecycle' })
  async transitionStudy(
    @Param('id') id: string,
    @Body() dto: TransitionStudyDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.studies.transition(auth.tenantId, id, dto.to);
  }

  @Post('studies/:id/publish')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Publish a study (admin) — needs 2 approvals incl. one domain expert',
    description:
      'Publish runs the k-anonymity floor against every observation. Cohorts below the ' +
      'floor are suppressed (release_ready=false) — they are NOT leaked. ' +
      'See ADR-0017 §C.',
  })
  async publishStudy(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.studies.publish(auth.tenantId, id);
  }

  @Post('studies/:id/disclose')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Record an external disclosure of a published study (admin)' })
  async disclose(
    @Param('id') id: string,
    @Body() dto: DiscloseDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.studies.disclose(auth.tenantId, id, dto.channel, dto.recipient);
  }
}
