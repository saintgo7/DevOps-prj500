import { Controller, Get, Param, Query } from '@nestjs/common';
import { CatalogService, GoalDto, IndicatorDto, TargetDto } from './catalog.service';

@Controller('catalog')
export class CatalogController {
  constructor(private readonly catalog: CatalogService) {}

  @Get('goals')
  async listGoals(): Promise<{ data: GoalDto[]; meta: { count: number } }> {
    const data = await this.catalog.listGoals();
    return { data, meta: { count: data.length } };
  }

  @Get('goals/:id')
  async getGoal(@Param('id') id: string): Promise<{ data: GoalDto }> {
    return { data: await this.catalog.getGoal(id) };
  }

  @Get('targets')
  async listTargets(
    @Query('goal') goal?: string,
  ): Promise<{ data: TargetDto[]; meta: { count: number } }> {
    const data = await this.catalog.listTargets(goal);
    return { data, meta: { count: data.length } };
  }

  @Get('indicators')
  async listIndicators(
    @Query('target') target?: string,
  ): Promise<{ data: IndicatorDto[]; meta: { count: number } }> {
    const data = await this.catalog.listIndicators(target);
    return { data, meta: { count: data.length } };
  }

  @Get('indicators/:id')
  async getIndicator(@Param('id') id: string): Promise<{ data: IndicatorDto }> {
    return { data: await this.catalog.getIndicator(id) };
  }
}
