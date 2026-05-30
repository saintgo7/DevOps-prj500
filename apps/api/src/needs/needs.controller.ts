import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
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
  NeedsService,
  type MatchState,
  type NeedCategory,
  type OfferState,
  type RequestState,
  type Urgency,
  type VerificationLevel,
} from './needs.service';

const CATEGORIES: NeedCategory[] = ['relief', 'supplies', 'equipment', 'knowledge', 'volunteers'];

class CreateRequestDto {
  @IsString() @IsIn(CATEGORIES) category!: NeedCategory;
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; description: string }>;
  @IsArray() sdgFocus!: string[];
  @IsString() region!: string;
  @IsOptional() @IsString() subregion?: string;
  @IsInt() @Min(1) quantity!: number;
  @IsString() unit!: string;
  @IsOptional() @IsString() @IsIn(['critical', 'high', 'normal', 'low']) urgency?: Urgency;
  @IsDateString() neededBy!: string;
}

class CreateOfferDto {
  @IsString() @IsIn(CATEGORIES) category!: NeedCategory;
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; description: string }>;
  @IsArray() sdgFocus!: string[];
  @IsString() region!: string;
  @IsOptional() @IsString() subregion?: string;
  @IsInt() @Min(1) quantity!: number;
  @IsString() unit!: string;
  @IsDateString() availableUntil!: string;
}

class TransitionRequestDto {
  @IsString()
  @IsIn(['draft', 'published', 'matching', 'fulfilled', 'closed', 'cancelled', 'expired', 'paused'])
  to!: RequestState;
}

class TransitionOfferDto {
  @IsString()
  @IsIn(['draft', 'published', 'matching', 'closed', 'cancelled', 'expired', 'paused'])
  to!: OfferState;
}

class TransitionMatchDto {
  @IsString()
  @IsIn(['suggested', 'contacted', 'accepted', 'shipped', 'delivered', 'cancelled'])
  to!: MatchState;
}

class SuggestMatchDto {
  @IsString() requestId!: string;
  @IsString() offerId!: string;
}

class AcceptDto {
  @IsString() @IsIn(['requester', 'provider']) side!: 'requester' | 'provider';
}

class SignDto {
  @IsString() @IsIn(['requester', 'provider']) side!: 'requester' | 'provider';
  @IsString() @MinLength(30) agreedClauseText!: string;
  @IsOptional() @IsString() trackingRef?: string;
  @IsOptional() @IsArray() evidenceHashes?: string[];
}

class VerificationDto {
  @IsString() @IsIn(['verified', 'community-vouched', 'unverified'])
  level!: VerificationLevel;
}

@ApiTags('needs')
@Controller('needs')
export class NeedsController {
  constructor(private readonly svc: NeedsService) {}

  @Post('requests')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a need request (admin/reviewer/contributor)' })
  async createRequest(@Body() dto: CreateRequestDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createRequest({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      category: dto.category,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      region: dto.region,
      ...(dto.subregion !== undefined ? { subregion: dto.subregion } : {}),
      quantity: dto.quantity,
      unit: dto.unit,
      ...(dto.urgency !== undefined ? { urgency: dto.urgency } : {}),
      neededBy: new Date(dto.neededBy),
    });
  }

  @Post('offers')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create an offer listing' })
  async createOffer(@Body() dto: CreateOfferDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.createOffer({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      category: dto.category,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      region: dto.region,
      ...(dto.subregion !== undefined ? { subregion: dto.subregion } : {}),
      quantity: dto.quantity,
      unit: dto.unit,
      availableUntil: new Date(dto.availableUntil),
    });
  }

  @Post('requests/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a request through its lifecycle' })
  async transitionRequest(
    @Param('id') id: string,
    @Body() dto: TransitionRequestDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transitionRequest(auth.tenantId, id, dto.to);
  }

  @Post('offers/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move an offer through its lifecycle' })
  async transitionOffer(
    @Param('id') id: string,
    @Body() dto: TransitionOfferDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transitionOffer(auth.tenantId, id, dto.to);
  }

  @Post('matches')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Suggest a match between a request and an offer (does NOT auto-message anyone)',
  })
  async suggestMatch(@Body() dto: SuggestMatchDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.suggestMatch(auth.tenantId, dto.requestId, dto.offerId);
  }

  @Post('matches/:id/accept')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'One-sided accept; contact details unmask only after BOTH sides accept',
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
  @ApiOperation({ summary: 'Move a match through accepted → shipped → delivered' })
  async transitionMatch(
    @Param('id') id: string,
    @Body() dto: TransitionMatchDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transitionMatch(auth.tenantId, id, dto.to);
  }

  @Post('matches/:id/sign')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Two-party signed fulfilment record' })
  async sign(@Param('id') id: string, @Body() dto: SignDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.sign(
      auth.tenantId,
      id,
      dto.side,
      dto.agreedClauseText,
      dto.trackingRef,
      dto.evidenceHashes,
    );
  }

  @Post('requests/:id/verification')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Set requester verification level (admin only)' })
  async setVerification(
    @Param('id') id: string,
    @Body() dto: VerificationDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.setRequestVerification(auth.tenantId, id, dto.level, auth.userId);
  }
}
