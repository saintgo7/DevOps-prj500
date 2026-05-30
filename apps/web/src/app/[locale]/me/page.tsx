'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/navigation';
import { apiBaseUrl } from '@/lib/api';

interface MeResponse {
  id: string;
  tenantId: string;
  email: string;
  displayName?: string;
  status: string;
  mfaEnabled: boolean;
}

export default function MePage(): React.JSX.Element {
  const t = useTranslations();
  const router = useRouter();
  const [me, setMe] = useState<MeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load(): Promise<void> {
      try {
        const res = await fetch(`${apiBaseUrl}/v1/me`, { credentials: 'include' });
        if (res.status === 401) {
          if (!cancelled) router.push('/signin');
          return;
        }
        if (!res.ok) throw new Error(t('me.loadFailed'));
        const body = (await res.json()) as MeResponse;
        if (!cancelled) setMe(body);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : t('me.loadFailed'));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, [router, t]);

  async function signOut(): Promise<void> {
    await fetch(`${apiBaseUrl}/v1/auth/signout`, {
      method: 'POST',
      credentials: 'include',
    });
    router.push('/signin');
  }

  return (
    <main
      style={{
        padding: '2rem',
        maxWidth: 720,
        margin: '0 auto',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <h1>{t('me.title')}</h1>
      {loading ? (
        <p>{t('common.loading')}</p>
      ) : error ? (
        <p style={{ color: '#dc2626' }}>{error}</p>
      ) : me ? (
        <dl style={{ display: 'grid', gridTemplateColumns: '160px 1fr', gap: 8, marginTop: 16 }}>
          <dt style={{ color: '#6b7280' }}>{t('me.email')}</dt>
          <dd>{me.email}</dd>
          <dt style={{ color: '#6b7280' }}>{t('me.name')}</dt>
          <dd>{me.displayName ?? '—'}</dd>
          <dt style={{ color: '#6b7280' }}>{t('me.status')}</dt>
          <dd>{me.status}</dd>
          <dt style={{ color: '#6b7280' }}>{t('me.mfa')}</dt>
          <dd>{me.mfaEnabled ? t('me.mfaActive') : t('me.mfaInactive')}</dd>
          <dt style={{ color: '#6b7280' }}>{t('me.tenantId')}</dt>
          <dd>
            <code>{me.tenantId}</code>
          </dd>
          <dt style={{ color: '#6b7280' }}>{t('me.userId')}</dt>
          <dd>
            <code>{me.id}</code>
          </dd>
        </dl>
      ) : null}
      <div style={{ marginTop: 24, display: 'flex', gap: 8 }}>
        <button
          type="button"
          onClick={signOut}
          style={{
            padding: '8px 14px',
            border: '1px solid #d1d5db',
            borderRadius: 6,
            background: 'white',
            cursor: 'pointer',
          }}
        >
          {t('common.signOut')}
        </button>
        <a
          href="../"
          style={{
            padding: '8px 14px',
            border: '1px solid #d1d5db',
            borderRadius: 6,
            textDecoration: 'none',
            color: '#111827',
          }}
        >
          {t('common.home')}
        </a>
      </div>
    </main>
  );
}
