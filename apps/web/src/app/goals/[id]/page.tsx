import Link from 'next/link';
import { notFound } from 'next/navigation';
import { SdgBadge } from '@sdgi/ui';
import { fetchGoal, fetchIndicators, fetchTargets, localized } from '@/lib/api';

export const dynamic = 'force-dynamic';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function GoalDetailPage({ params }: PageProps): Promise<React.JSX.Element> {
  const { id } = await params;
  const goal = await fetchGoal(id);
  if (!goal) notFound();

  const targets = await fetchTargets(goal.id);
  const targetIds = targets.map((t) => t.id);
  const allIndicators = (await Promise.all(targetIds.map((tid) => fetchIndicators(tid)))).flat();
  const indicatorsByTarget = new Map<string, typeof allIndicators>();
  for (const tid of targetIds) {
    indicatorsByTarget.set(
      tid,
      allIndicators.filter((i) => i.targetId === tid),
    );
  }

  return (
    <main
      style={{
        padding: '2rem',
        maxWidth: 900,
        margin: '0 auto',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <p>
        <Link href="/" style={{ color: '#6b7280' }}>
          ← 17 Goals
        </Link>
      </p>
      <header style={{ display: 'flex', alignItems: 'center', gap: 16, marginTop: 8 }}>
        <SdgBadge goal={goal.number} />
        <h1 style={{ margin: 0 }}>{localized(goal.name, 'ko')}</h1>
      </header>
      <p style={{ color: '#6b7280', marginTop: 8 }}>{localized(goal.name, 'en')}</p>

      <section aria-labelledby="targets-heading" style={{ marginTop: 32 }}>
        <h2 id="targets-heading">Targets ({targets.length})</h2>
        {targets.length === 0 ? (
          <p style={{ color: '#6b7280' }}>이 Goal에 대한 샘플 Target이 아직 시드되어 있지 않습니다.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, display: 'grid', gap: 16 }}>
            {targets.map((t) => {
              const indicators = indicatorsByTarget.get(t.id) ?? [];
              return (
                <li
                  key={t.id}
                  style={{
                    border: '1px solid #e5e7eb',
                    borderRadius: 8,
                    padding: 16,
                  }}
                >
                  <header style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
                    <strong>{t.id}</strong>
                    <small style={{ color: '#6b7280', textTransform: 'uppercase' }}>
                      {t.type}
                    </small>
                  </header>
                  <p style={{ margin: '8px 0 0' }}>{localized(t.text, 'ko')}</p>
                  <p style={{ margin: '4px 0 0', color: '#6b7280', fontSize: 14 }}>
                    {localized(t.text, 'en')}
                  </p>
                  {indicators.length > 0 ? (
                    <ul style={{ marginTop: 12, paddingLeft: 18, display: 'grid', gap: 4 }}>
                      {indicators.map((i) => (
                        <li key={i.id} style={{ fontSize: 14 }}>
                          <code>{i.id}</code> · {i.unit} · Tier {i.tier}
                          {i.methodology ? ` · ${i.methodology}` : null}
                        </li>
                      ))}
                    </ul>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </main>
  );
}
