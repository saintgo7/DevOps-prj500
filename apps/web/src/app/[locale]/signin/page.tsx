'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/navigation';
import { apiBaseUrl } from '@/lib/api';

export default function SignInPage(): React.JSX.Element {
  const t = useTranslations();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent): Promise<void> {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch(`${apiBaseUrl}/v1/auth/signin`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const body = (await res.json().catch(() => null)) as { message?: string } | null;
        throw new Error(body?.message ?? `${t('auth.signinFailed')} (${res.status})`);
      }
      router.push('/me');
    } catch (err) {
      setError(err instanceof Error ? err.message : t('auth.signinFailed'));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main
      style={{
        padding: '2rem',
        maxWidth: 420,
        margin: '0 auto',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <h1>{t('auth.signInTitle')}</h1>
      <form
        onSubmit={onSubmit}
        style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 16 }}
      >
        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontWeight: 500, fontSize: 14 }}>{t('auth.email')}</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            style={inputStyle}
          />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontWeight: 500, fontSize: 14 }}>{t('auth.password')}</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            style={inputStyle}
          />
        </label>
        {error ? (
          <p
            style={{
              padding: 8,
              background: '#fee2e2',
              color: '#991b1b',
              borderRadius: 6,
              fontSize: 14,
            }}
          >
            {error}
          </p>
        ) : null}
        <button
          type="submit"
          disabled={submitting}
          style={{
            padding: '10px 16px',
            border: 'none',
            borderRadius: 6,
            background: '#0A6E5C',
            color: 'white',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          {submitting ? t('auth.submitting') : t('common.signIn')}
        </button>
        <p style={{ fontSize: 14 }}>
          {t('auth.noAccount')} <a href="signup">{t('common.signUp')}</a>
        </p>
      </form>
    </main>
  );
}

const inputStyle: React.CSSProperties = {
  padding: '8px 10px',
  border: '1px solid #d1d5db',
  borderRadius: 6,
  fontSize: 14,
};
