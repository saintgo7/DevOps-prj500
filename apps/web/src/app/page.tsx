import Link from 'next/link';
import { SdgBadge } from '@sdgi/ui';
import { fetchGoals, localized, type Goal } from '@/lib/api';

export const dynamic = 'force-dynamic';

export default async function HomePage(): Promise<React.JSX.Element> {
  const goals: Goal[] = await fetchGoals();

  return (
    <main
      style={{
        padding: '2rem',
        maxWidth: 1100,
        margin: '0 auto',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <header
        style={{
          marginBottom: '2rem',
          display: 'flex',
          alignItems: 'baseline',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: 16,
        }}
      >
        <div>
          <h1 style={{ margin: 0 }}>SDG Impact Cloud</h1>
          <p style={{ color: '#4b5563', marginTop: 4 }}>
            UN 지속가능발전목표(SDGs) 기반 임팩트 측정·보고 SaaS
          </p>
        </div>
        <nav style={{ display: 'flex', gap: 8 }}>
          <Link href="/signin" style={navLink}>
            로그인
          </Link>
          <Link href="/signup" style={{ ...navLink, background: '#0A6E5C', color: 'white' }}>
            가입
          </Link>
          <Link href="/me" style={navLink}>
            내 프로필
          </Link>
        </nav>
      </header>

      <section aria-labelledby="goals-heading">
        <h2 id="goals-heading">17개 지속가능발전목표</h2>
        {goals.length === 0 ? (
          <p style={{ color: '#6b7280' }}>
            카탈로그 API에 연결되지 않았습니다. <code>pnpm dev</code> 또는 <code>make up</code>로
            로컬 환경을 기동하세요.
          </p>
        ) : (
          <ul
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
              gap: 12,
              listStyle: 'none',
              padding: 0,
            }}
          >
            {goals.map((g) => (
              <li key={g.id}>
                <Link
                  href={{ pathname: `/goals/${encodeURIComponent(g.id)}` }}
                  style={{
                    border: '1px solid #e5e7eb',
                    borderRadius: 8,
                    padding: 12,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    textDecoration: 'none',
                    color: 'inherit',
                  }}
                >
                  <SdgBadge goal={g.number} />
                  <span style={{ fontWeight: 500 }}>{localized(g.name, 'ko')}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer style={{ marginTop: '2rem', color: '#9ca3af', fontSize: 12 }}>
        문서: <a href="https://github.com/saintgo7/devops-prj500/tree/main/docs">/docs</a>
      </footer>
    </main>
  );
}

const navLink: React.CSSProperties = {
  padding: '6px 12px',
  border: '1px solid #d1d5db',
  borderRadius: 6,
  textDecoration: 'none',
  color: '#111827',
  fontSize: 14,
};
