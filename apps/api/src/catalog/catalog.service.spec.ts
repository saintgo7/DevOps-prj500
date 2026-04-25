import { describe, expect, it, vi } from 'vitest';
import { NotFoundException } from '@nestjs/common';
import { CatalogService } from './catalog.service';
import type { PrismaService } from '../prisma/prisma.service';

function makePrismaMock(): PrismaService {
  return {
    sdgGoal: {
      findMany: vi.fn().mockResolvedValue([
        { id: 'SDG-1', number: 1, color: '#E5243B', icon: null, nameI18n: { en: 'No Poverty' } },
        { id: 'SDG-13', number: 13, color: '#3F7E44', icon: null, nameI18n: { en: 'Climate Action' } },
      ]),
      findUnique: vi.fn(({ where }: { where: { id: string } }) =>
        where.id === 'SDG-13'
          ? Promise.resolve({
              id: 'SDG-13',
              number: 13,
              color: '#3F7E44',
              icon: null,
              nameI18n: { en: 'Climate Action' },
            })
          : Promise.resolve(null),
      ),
    },
    sdgTarget: {
      findMany: vi.fn().mockResolvedValue([
        { id: 'SDG-13.2', goalId: 'SDG-13', textI18n: { en: 'Integrate climate' }, type: 'outcome' },
      ]),
    },
    sdgIndicator: {
      findUnique: vi.fn(({ where }: { where: { id: string } }) =>
        where.id === 'SDG-13.2.2'
          ? Promise.resolve({
              id: 'SDG-13.2.2',
              targetId: 'SDG-13.2',
              unit: 'tCO2eq',
              methodology: null,
              tier: 1,
            })
          : Promise.resolve(null),
      ),
      findMany: vi.fn().mockResolvedValue([]),
    },
  } as unknown as PrismaService;
}

describe('CatalogService', () => {
  it('returns all goals ordered', async () => {
    const svc = new CatalogService(makePrismaMock());
    const goals = await svc.listGoals();
    expect(goals).toHaveLength(2);
    expect(goals[0]?.id).toBe('SDG-1');
    expect(goals[1]?.color).toBe('#3F7E44');
  });

  it('returns a single goal by id', async () => {
    const svc = new CatalogService(makePrismaMock());
    const goal = await svc.getGoal('SDG-13');
    expect(goal.number).toBe(13);
    expect(goal.name.en).toBe('Climate Action');
  });

  it('throws NotFound for unknown goal id', async () => {
    const svc = new CatalogService(makePrismaMock());
    await expect(svc.getGoal('SDG-99')).rejects.toBeInstanceOf(NotFoundException);
  });

  it('lists targets filtered by goal', async () => {
    const svc = new CatalogService(makePrismaMock());
    const targets = await svc.listTargets('SDG-13');
    expect(targets).toHaveLength(1);
    expect(targets[0]?.goalId).toBe('SDG-13');
  });

  it('returns indicator detail with unit', async () => {
    const svc = new CatalogService(makePrismaMock());
    const indicator = await svc.getIndicator('SDG-13.2.2');
    expect(indicator.unit).toBe('tCO2eq');
    expect(indicator.tier).toBe(1);
  });

  it('throws for unknown indicator', async () => {
    const svc = new CatalogService(makePrismaMock());
    await expect(svc.getIndicator('SDG-99.9.9')).rejects.toBeInstanceOf(NotFoundException);
  });
});
