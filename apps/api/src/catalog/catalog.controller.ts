import { Controller, Get, Param, Query } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { CatalogService, GoalDto, IndicatorDto, TargetDto } from './catalog.service';

@ApiTags('catalog')
@Controller('catalog')
export class CatalogController {
  constructor(private readonly catalog: CatalogService) {}

  @Get('goals')
  @ApiOperation({ summary: 'List all 17 SDG goals' })
  async listGoals(): Promise<{ data: GoalDto[]; meta: { count: number } }> {
    const data = await this.catalog.listGoals();
    return { data, meta: { count: data.length } };
  }

  @Get('goals/:id')
  @ApiOperation({ summary: 'Get a single goal (e.g. SDG-13)' })
  async getGoal(@Param('id') id: string): Promise<{ data: GoalDto }> {
    return { data: await this.catalog.getGoal(id) };
  }

  @Get('targets')
  @ApiOperation({ summary: 'List targets, optionally filtered by goal' })
  async listTargets(
    @Query('goal') goal?: string,
  ): Promise<{ data: TargetDto[]; meta: { count: number } }> {
    const data = await this.catalog.listTargets(goal);
    return { data, meta: { count: data.length } };
  }

  @Get('indicators')
  @ApiOperation({ summary: 'List indicators, optionally filtered by target' })
  async listIndicators(
    @Query('target') target?: string,
  ): Promise<{ data: IndicatorDto[]; meta: { count: number } }> {
    const data = await this.catalog.listIndicators(target);
    return { data, meta: { count: data.length } };
  }

  @Get('indicators/:id')
  @ApiOperation({ summary: 'Get a single indicator (e.g. SDG-13.2.2)' })
  async getIndicator(@Param('id') id: string): Promise<{ data: IndicatorDto }> {
    return { data: await this.catalog.getIndicator(id) };
  }
}
