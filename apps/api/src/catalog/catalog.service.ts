import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface GoalDto {
  id: string;
  number: number;
  name: Record<string, string>;
  color: string;
  icon: string | null;
}

export interface TargetDto {
  id: string;
  goalId: string;
  text: Record<string, string>;
  type: string;
}

export interface IndicatorDto {
  id: string;
  targetId: string;
  unit: string;
  methodology: string | null;
  tier: number;
}

@Injectable()
export class CatalogService {
  constructor(private readonly prisma: PrismaService) {}

  async listGoals(): Promise<GoalDto[]> {
    const goals = await this.prisma.sdgGoal.findMany({ orderBy: { number: 'asc' } });
    return goals.map((g) => ({
      id: g.id,
      number: g.number,
      name: g.nameI18n as Record<string, string>,
      color: g.color,
      icon: g.icon ?? null,
    }));
  }

  async getGoal(id: string): Promise<GoalDto> {
    const g = await this.prisma.sdgGoal.findUnique({ where: { id } });
    if (!g) throw new NotFoundException(`Goal not found: ${id}`);
    return {
      id: g.id,
      number: g.number,
      name: g.nameI18n as Record<string, string>,
      color: g.color,
      icon: g.icon ?? null,
    };
  }

  async listTargets(goalId?: string): Promise<TargetDto[]> {
    const targets = await this.prisma.sdgTarget.findMany({
      ...(goalId ? { where: { goalId } } : {}),
      orderBy: { id: 'asc' },
    });
    return targets.map((t) => ({
      id: t.id,
      goalId: t.goalId,
      text: t.textI18n as Record<string, string>,
      type: t.type,
    }));
  }

  async getIndicator(id: string): Promise<IndicatorDto> {
    const i = await this.prisma.sdgIndicator.findUnique({ where: { id } });
    if (!i) throw new NotFoundException(`Indicator not found: ${id}`);
    return {
      id: i.id,
      targetId: i.targetId,
      unit: i.unit,
      methodology: i.methodology ?? null,
      tier: i.tier,
    };
  }

  async listIndicators(targetId?: string): Promise<IndicatorDto[]> {
    const items = await this.prisma.sdgIndicator.findMany({
      ...(targetId ? { where: { targetId } } : {}),
      orderBy: { id: 'asc' },
    });
    return items.map((i) => ({
      id: i.id,
      targetId: i.targetId,
      unit: i.unit,
      methodology: i.methodology ?? null,
      tier: i.tier,
    }));
  }
}
