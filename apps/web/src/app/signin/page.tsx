'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiBaseUrl } from '@/lib/api';

export default function SignInPage(): React.JSX.Element {
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
        throw new Error(body?.message ?? `Sign in failed (${res.status})`);
      }
      router.push('/me');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed');
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
      <h1>로그인 (Sign In)</h1>
      <form
        onSubmit={onSubmit}
        style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 16 }}
      >
        <label style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          <span style={{ fontWeight: 500, fontSize: 14 }}>이메일</span>
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
          <span style={{ fontWeight: 500, fontSize: 14 }}>비밀번호</span>
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
          {submitting ? '처리 중…' : '로그인'}
        </button>
        <p style={{ fontSize: 14 }}>
          계정이 없으신가요? <a href="/signup">가입</a>
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
