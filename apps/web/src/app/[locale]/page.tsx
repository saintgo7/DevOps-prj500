import { getTranslations, setRequestLocale } from 'next-intl/server';
import { SdgBadge } from '@sdgi/ui';
import { Link } from '@/i18n/navigation';
import { LanguageSwitcher } from '@/components/LanguageSwitcher';
import { fetchGoals, localized, type Goal } from '@/lib/api';

export const dynamic = 'force-dynamic';

export default async function HomePage(props: {
  params: Promise<{ locale: string }>;
}): Promise<React.JSX.Element> {
  const { locale } = await props.params;
  setRequestLocale(locale);
  const t = await getTranslations();
  const goals: Goal[] = await fetchGoals(locale);

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
          <h1 style={{ margin: 0 }}>{t('common.appName')}</h1>
          <p style={{ color: '#4b5563', marginTop: 4 }}>{t('common.tagline')}</p>
        </div>
        <nav
          style={{
            display: 'flex',
            gap: 8,
            alignItems: 'center',
            flexWrap: 'wrap',
          }}
        >
          <LanguageSwitcher />
          <Link href="/signin" style={navLink}>
            {t('common.signIn')}
          </Link>
          <Link
            href="/signup"
            style={{ ...navLink, background: '#0A6E5C', color: 'white' }}
          >
            {t('common.signUp')}
          </Link>
          <Link href="/me" style={navLink}>
            {t('common.myProfile')}
          </Link>
        </nav>
      </header>

      <section aria-labelledby="goals-heading">
        <h2 id="goals-heading">{t('home.goalsHeading')}</h2>
        {goals.length === 0 ? (
          <p style={{ color: '#6b7280' }}>
            {t('home.apiOffline', { dev: 'pnpm dev', compose: 'make up' })}
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
                  href={`/goals/${encodeURIComponent(g.id)}` as never}
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
                  <span style={{ fontWeight: 500 }}>{localized(g.name, locale)}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer style={{ marginTop: '2rem', color: '#9ca3af', fontSize: 12 }}>
        {t('home.footerDocs')}:{' '}
        <a href="https://github.com/saintgo7/devops-prj500/tree/main/docs">/docs</a>
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
