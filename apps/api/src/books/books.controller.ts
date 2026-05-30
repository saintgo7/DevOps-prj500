import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
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
import { BooksService, type BookState } from './books.service';

class CreateBookDto {
  @IsString() primaryLocale!: string;
  @IsObject() bodyI18n!: Record<string, { title: string; subtitle?: string; blurb?: string }>;
  @IsArray() sdgFocus!: string[];
  @IsOptional() @IsArray() applicableRegions?: string[];
  @IsOptional() @IsString() license?: string;
}

class ChapterDto {
  @IsInt() @Min(1) position!: number;
  @IsObject() headerI18n!: Record<string, { title: string; lead?: string }>;
  @IsOptional() @IsString() sourceColumnId?: string;
  @IsOptional() @IsString() sourceManuscriptId?: string;
  @IsOptional() @IsString() sourceShortStoryId?: string;
  @IsOptional() @IsString() sourceWatchDigestId?: string;
  @IsOptional() @IsString() sourceCustom?: string;
  @IsOptional() @IsString() sourceCustomReason?: string;
  @IsOptional() @IsInt() @Min(0) @Max(100) plainLanguageScore?: number;
}

class TransitionBookDto {
  @IsString()
  @IsIn(['draft', 'review', 'published', 'retired'])
  to!: BookState;
}

@ApiTags('books')
@Controller('books')
export class BooksController {
  constructor(private readonly svc: BooksService) {}

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a book project (admin/reviewer)' })
  async create(@Body() dto: CreateBookDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.create({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      primaryLocale: dto.primaryLocale,
      bodyI18n: dto.bodyI18n,
      sdgFocus: dto.sdgFocus,
      ...(dto.applicableRegions !== undefined ? { applicableRegions: dto.applicableRegions } : {}),
      ...(dto.license !== undefined ? { license: dto.license } : {}),
    });
  }

  @Post(':id/chapters')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Add a chapter — exactly one source per chapter' })
  async addChapter(
    @Param('id') id: string,
    @Body() dto: ChapterDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.addChapter(auth.tenantId, id, {
      position: dto.position,
      headerI18n: dto.headerI18n,
      ...(dto.sourceColumnId !== undefined ? { sourceColumnId: dto.sourceColumnId } : {}),
      ...(dto.sourceManuscriptId !== undefined ? { sourceManuscriptId: dto.sourceManuscriptId } : {}),
      ...(dto.sourceShortStoryId !== undefined ? { sourceShortStoryId: dto.sourceShortStoryId } : {}),
      ...(dto.sourceWatchDigestId !== undefined ? { sourceWatchDigestId: dto.sourceWatchDigestId } : {}),
      ...(dto.sourceCustom !== undefined ? { sourceCustom: dto.sourceCustom } : {}),
      ...(dto.sourceCustomReason !== undefined ? { sourceCustomReason: dto.sourceCustomReason } : {}),
      ...(dto.plainLanguageScore !== undefined ? { plainLanguageScore: dto.plainLanguageScore } : {}),
    });
  }

  @Post(':id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a book through draft → review → published' })
  async transition(
    @Param('id') id: string,
    @Body() dto: TransitionBookDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.svc.transition(auth.tenantId, id, dto.to);
  }
}
