'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from '@/i18n/navigation';
import { apiBaseUrl } from '@/lib/api';

export default function SignUpPage(): React.JSX.Element {
  const t = useTranslations();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [organizationName, setOrganizationName] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent): Promise<void> {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch(`${apiBaseUrl}/v1/auth/signup`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          email,
          password,
          organizationName: organizationName || undefined,
          displayName: displayName || undefined,
        }),
      });
      if (!res.ok) {
        const body = (await res.json().catch(() => null)) as { message?: string } | null;
        throw new Error(body?.message ?? `${t('auth.signupFailed')} (${res.status})`);
      }
      router.push('/me');
    } catch (err) {
      setError(err instanceof Error ? err.message : t('auth.signupFailed'));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main style={pageStyle}>
      <h1>{t('auth.signUpTitle')}</h1>
      <p style={{ color: '#6b7280' }}>{t('auth.signUpHint')}</p>
      <form onSubmit={onSubmit} style={formStyle}>
        <Field label={t('auth.email')} required>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
            style={inputStyle}
          />
        </Field>
        <Field label={t('auth.passwordHint')} required>
          <input
            type="password"
            minLength={12}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            style={inputStyle}
          />
        </Field>
        <Field label={t('auth.organizationName')}>
          <input
            value={organizationName}
            onChange={(e) => setOrganizationName(e.target.value)}
            style={inputStyle}
          />
        </Field>
        <Field label={t('auth.displayName')}>
          <input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            style={inputStyle}
          />
        </Field>
        {error ? <p style={errorStyle}>{error}</p> : null}
        <button type="submit" disabled={submitting} style={buttonStyle}>
          {submitting ? t('auth.submitting') : t('common.signUp')}
        </button>
        <p style={{ fontSize: 14 }}>
          {t('auth.haveAccount')} <a href="signin">{t('common.signIn')}</a>
        </p>
      </form>
    </main>
  );
}

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}): React.JSX.Element {
  return (
    <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      <span style={{ fontWeight: 500, fontSize: 14 }}>
        {label}
        {required ? <span style={{ color: '#dc2626' }}> *</span> : null}
      </span>
      {children}
    </label>
  );
}

const pageStyle: React.CSSProperties = {
  padding: '2rem',
  maxWidth: 480,
  margin: '0 auto',
  fontFamily: 'system-ui, -apple-system, sans-serif',
};
const formStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 12,
  marginTop: 16,
};
const inputStyle: React.CSSProperties = {
  padding: '8px 10px',
  border: '1px solid #d1d5db',
  borderRadius: 6,
  fontSize: 14,
};
const buttonStyle: React.CSSProperties = {
  padding: '10px 16px',
  border: 'none',
  borderRadius: 6,
  background: '#0A6E5C',
  color: 'white',
  fontWeight: 600,
  cursor: 'pointer',
};
const errorStyle: React.CSSProperties = {
  padding: 8,
  background: '#fee2e2',
  color: '#991b1b',
  borderRadius: 6,
  fontSize: 14,
};
