import {
  Body,
  Controller,
  Param,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { IsArray, IsBoolean, IsObject, IsOptional, IsString, MinLength } from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import { StrategyService } from './strategy.service';

class CreateDto {
  @IsString() insightId!: string;
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; plan: string; riskNote?: string }>;
  @IsArray() sdgFocus!: string[];
  @IsOptional() @IsArray() applicableRegions?: string[];
  @IsBoolean() noncommercialNotice!: boolean;
}

class InviteDto {
  @IsString() inviteeEmail!: string;
  @IsOptional() @IsString() shareRight?: 'view' | 'discuss';
}

class AcceptDto {
  @IsString() @MinLength(20) agreedClause!: string;
}

class RevokeDto {
  @IsString() @MinLength(8) reason!: string;
}

@ApiTags('strategy-sessions')
@Controller('strategy-sessions')
export class StrategyController {
  constructor(private readonly svc: StrategyService) {}

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Create a strategy session draft (admin/reviewer; non-commercial obligation)',
  })
  async create(@Body() dto: CreateDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.create({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      insightId: dto.insightId,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      ...(dto.applicableRegions !== undefined ? { applicableRegions: dto.applicableRegions } : {}),
      noncommercialNotice: dto.noncommercialNotice,
    });
  }

  @Post(':id/approve')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Approve a draft session (admin)' })
  async approve(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.approve(auth.tenantId, id, auth.userId);
  }

  @Post(':id/invites')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Send an invite to one person — never auto-broadcast' })
  async invite(@Param('id') id: string, @Body() dto: InviteDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.invite({
      tenantId: auth.tenantId,
      sessionId: id,
      invitedBy: auth.userId,
      inviteeEmail: dto.inviteeEmail,
      ...(dto.shareRight !== undefined ? { shareRight: dto.shareRight } : {}),
    });
  }

  @Post('invites/:inviteId/accept')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Accept an invite — must include the non-commercial clause text',
  })
  async accept(
    @Param('inviteId') inviteId: string,
    @Body() dto: AcceptDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.accept(auth.tenantId, inviteId, dto.agreedClause);
  }

  @Post(':id/revoke')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Permanently revoke a session (super-admin only; reason is recorded forever)',
    description:
      'Only the super-admin role may revoke. All outstanding invites are invalidated in the same transaction. ' +
      'The reason is stored verbatim and cannot be edited later. See ADR-0016 §B.',
  })
  async revoke(
    @Param('id') id: string,
    @Body() dto: RevokeDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.revoke(auth.tenantId, id, auth.userId, dto.reason);
  }
}
