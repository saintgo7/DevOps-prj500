import {
  Body,
  Controller,
  Get,
  Param,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { IsArray, IsOptional, IsString } from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import { StoryService } from './story.service';

class GenerateDto {
  @IsString() columnId!: string;
  @IsOptional() @IsArray() locales?: string[];
  @IsOptional() @IsArray() ageTiers?: ('children' | 'teen' | 'adult' | 'senior')[];
}

@ApiTags('stories')
@Controller('stories')
export class StoryController {
  constructor(private readonly stories: StoryService) {}

  @Post('generate')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Generate variants of a short-form story from a published column',
    description:
      'Fan out across locales × age tiers. Each variant lands in state=draft ' +
      'and must be approved by a human (POST /v1/stories/variants/:id/approve) ' +
      'before any distribution post can be created. See ADR-0015.',
  })
  async generate(@Body() dto: GenerateDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.stories.generateFromColumn({
      tenantId: auth.tenantId,
      columnId: dto.columnId,
      ...(dto.locales !== undefined ? { locales: dto.locales } : {}),
      ...(dto.ageTiers !== undefined ? { ageTiers: dto.ageTiers } : {}),
    });
  }

  @Post('variants/:id/approve')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Approve a variant for distribution' })
  async approveVariant(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    await this.stories.approveVariant(auth.tenantId, id);
    return { ok: true };
  }

  @Get(':storyId/variants')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'List all variants of a story for the current tenant' })
  async listVariants(@Param('storyId') storyId: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const data = await this.stories.listForStory(auth.tenantId, storyId);
    return { data, meta: { count: data.length } };
  }
}
