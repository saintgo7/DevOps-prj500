import { PrismaClient } from '@prisma/client';
import { SDG_GOALS, SDG_TARGETS_SAMPLE, SDG_INDICATORS_SAMPLE } from './seed/sdg-goals';

const prisma = new PrismaClient();

async function main(): Promise<void> {
  // Roles (idempotent)
  const roles = [
    { key: 'admin', name: 'Administrator' },
    { key: 'reviewer', name: 'Reviewer' },
    { key: 'contributor', name: 'Contributor' },
    { key: 'viewer', name: 'Viewer' },
    { key: 'auditor', name: 'Auditor' },
  ];
  for (const r of roles) {
    await prisma.role.upsert({ where: { key: r.key }, update: { name: r.name }, create: r });
  }

  // SDG Goals (17)
  for (const g of SDG_GOALS) {
    await prisma.sdgGoal.upsert({
      where: { id: g.id },
      update: { number: g.number, color: g.color, nameI18n: g.nameI18n },
      create: { id: g.id, number: g.number, color: g.color, nameI18n: g.nameI18n },
    });
  }

  // Targets (sample subset)
  for (const t of SDG_TARGETS_SAMPLE) {
    await prisma.sdgTarget.upsert({
      where: { id: t.id },
      update: { goalId: t.goalId, type: t.type, textI18n: t.textI18n },
      create: { id: t.id, goalId: t.goalId, type: t.type, textI18n: t.textI18n },
    });
  }

  // Indicators (sample subset)
  for (const i of SDG_INDICATORS_SAMPLE) {
    await prisma.sdgIndicator.upsert({
      where: { id: i.id },
      update: {
        targetId: i.targetId,
        unit: i.unit,
        tier: i.tier,
        methodology: i.methodology ?? null,
      },
      create: {
        id: i.id,
        targetId: i.targetId,
        unit: i.unit,
        tier: i.tier,
        methodology: i.methodology ?? null,
      },
    });
  }

  console.log(
    `[seed] roles=${roles.length}, goals=${SDG_GOALS.length}, ` +
      `targets=${SDG_TARGETS_SAMPLE.length}, indicators=${SDG_INDICATORS_SAMPLE.length}`,
  );
}

main()
  .catch((e: unknown) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => {
    void prisma.$disconnect();
  });
