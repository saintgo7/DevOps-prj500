import { Controller, Get, Param, Query } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { ColumnService } from './column.service';

@ApiTags('columns')
@Controller('columns')
export class ColumnController {
  constructor(private readonly columns: ColumnService) {}

  @Get()
  @ApiOperation({
    summary: 'Recently published daily columns (public)',
    description:
      'Use ?origin=external for curated outside content, ?origin=internal for ' +
      'our own publications (ADR-0014 §4 — two-section UX).',
  })
  async listPublished(
    @Query('days') days?: string,
    @Query('locale') locale?: string,
    @Query('origin') origin?: 'external' | 'internal',
  ) {
    const since = days
      ? new Date(Date.now() - Number(days) * 86400 * 1000)
      : new Date(Date.now() - 30 * 86400 * 1000);
    const data = await this.columns.listPublished({
      since,
      ...(locale !== undefined ? { locale } : {}),
      ...(origin !== undefined ? { origin } : {}),
      take: 30,
    });
    return { data, meta: { count: data.length } };
  }

  @Get(':id')
  @ApiOperation({ summary: 'A single published daily column (public, JSON-LD)' })
  async one(@Param('id') id: string) {
    const c = await this.columns.getPublishedById(id);
    return {
      data: {
        ...c,
        '@context': 'https://schema.org',
        '@type': 'Article',
        license: 'https://creativecommons.org/licenses/by/4.0/',
      },
    };
  }
}
