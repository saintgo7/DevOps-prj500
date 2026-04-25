import {
  Body,
  Controller,
  Get,
  Post,
  Query,
  Req,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiQuery,
  ApiTags,
} from '@nestjs/swagger';
import { IsArray, IsOptional, IsString } from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { WatchService, type WatchItemDto } from './watch.service';

class CreateSubscriptionDto {
  @IsOptional() @IsString() name?: string;
  @IsOptional() @IsString() digestLanguage?: string;
  @IsOptional() @IsArray() sdgFocus?: string[];
  @IsOptional() @IsArray() categories?: string[];
  @IsOptional() @IsArray() languages?: string[];
  @IsOptional() @IsArray() regions?: string[];
}

class ExpressInterestDto {
  @IsString() itemId!: string;
  @IsOptional() @IsString() intent?: string; // 'learn' | 'partner' | 'fund' | 'volunteer'
  @IsOptional() @IsString() note?: string;
  @IsOptional() contactConsent?: boolean;
}

@ApiTags('watch')
@Controller('watch')
export class WatchController {
  constructor(private readonly watch: WatchService) {}

  @Get('items')
  @ApiOperation({
    summary: 'Find this week’s findings filtered by SDG, language, region',
  })
  @ApiQuery({ name: 'sdg', required: false, isArray: true })
  @ApiQuery({ name: 'lang', required: false, isArray: true })
  @ApiQuery({ name: 'region', required: false, isArray: true })
  @ApiQuery({ name: 'category', required: false, isArray: true })
  async items(
    @Query('sdg') sdg?: string | string[],
    @Query('lang') lang?: string | string[],
    @Query('region') region?: string | string[],
    @Query('category') category?: string | string[],
    @Query('days') days?: string,
  ): Promise<{ data: WatchItemDto[]; meta: { count: number } }> {
    const since = days
      ? new Date(Date.now() - Number(days) * 86400 * 1000)
      : new Date(Date.now() - 7 * 86400 * 1000);
    const data = await this.watch.listRecentItems({
      sdgFocus: toArray(sdg),
      languages: toArray(lang),
      regions: toArray(region),
      categories: toArray(category),
      since,
      take: 100,
    });
    return { data, meta: { count: data.length } };
  }

  @Get('sources')
  @ApiOperation({ summary: 'List the public weekly-watch sources' })
  async sources() {
    const data = await this.watch.listSources({ active: true });
    return { data, meta: { count: data.length } };
  }

  @Post('subscriptions')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Save a personal weekly digest filter' })
  async createSubscription(@Body() dto: CreateSubscriptionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.watch.createSubscription({
      tenantId: auth.tenantId,
      userId: auth.userId,
      ...(dto.name !== undefined ? { name: dto.name } : {}),
      filter: {
        ...(dto.sdgFocus ? { sdgFocus: dto.sdgFocus } : {}),
        ...(dto.categories ? { categories: dto.categories } : {}),
        ...(dto.languages ? { languages: dto.languages } : {}),
        ...(dto.regions ? { regions: dto.regions } : {}),
      },
      ...(dto.digestLanguage !== undefined
        ? { digestLanguage: dto.digestLanguage }
        : {}),
    });
  }

  @Get('subscriptions')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'List my saved weekly digest filters' })
  async listSubscriptions(@Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const data = await this.watch.listSubscriptions(auth.tenantId, auth.userId);
    return { data, meta: { count: data.length } };
  }

  @Post('interests')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: "Record private interest in a finding (does NOT auto-notify anyone)",
    description:
      'Per ADR-0012, expressing interest is private. Reaching out to the source ' +
      'or other interested users requires a separate explicit action.',
  })
  async expressInterest(@Body() dto: ExpressInterestDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.watch.expressInterest({
      tenantId: auth.tenantId,
      userId: auth.userId,
      itemId: dto.itemId,
      ...(dto.intent !== undefined ? { intent: dto.intent } : {}),
      ...(dto.note !== undefined ? { note: dto.note } : {}),
      ...(dto.contactConsent !== undefined
        ? { contactConsent: dto.contactConsent }
        : {}),
    });
  }
}

function toArray(v: string | string[] | undefined): string[] | undefined {
  if (!v) return undefined;
  if (Array.isArray(v)) return v;
  return v.split(',').map((s) => s.trim()).filter(Boolean);
}
