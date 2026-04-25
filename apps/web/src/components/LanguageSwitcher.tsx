'use client';

import { useTransition } from 'react';
import { useTranslations } from 'next-intl';
import { useParams } from 'next/navigation';
import { LOCALE_LABELS, type Locale } from '@/i18n/routing';
import { usePathname, useRouter } from '@/i18n/navigation';

export function LanguageSwitcher(): React.JSX.Element {
  const t = useTranslations('languageSwitcher');
  const router = useRouter();
  const pathname = usePathname();
  const params = useParams();
  const [isPending, startTransition] = useTransition();
  const currentLocale = (params.locale as Locale) ?? 'ko';

  function onChange(e: React.ChangeEvent<HTMLSelectElement>): void {
    const next = e.target.value as Locale;
    startTransition(() => {
      router.replace(pathname, { locale: next });
    });
  }

  return (
    <label
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        fontSize: 14,
        opacity: isPending ? 0.6 : 1,
      }}
    >
      <span className="visually-hidden" style={visuallyHidden}>
        {t('label')}
      </span>
      <span aria-hidden style={{ color: '#6b7280' }}>
        🌐
      </span>
      <select
        value={currentLocale}
        onChange={onChange}
        aria-label={t('label')}
        style={{
          padding: '4px 8px',
          border: '1px solid #d1d5db',
          borderRadius: 6,
          background: 'white',
          fontSize: 14,
          cursor: 'pointer',
        }}
      >
        {(Object.keys(LOCALE_LABELS) as Locale[]).map((loc) => (
          <option key={loc} value={loc}>
            {LOCALE_LABELS[loc]}
          </option>
        ))}
      </select>
    </label>
  );
}

const visuallyHidden: React.CSSProperties = {
  position: 'absolute',
  width: 1,
  height: 1,
  padding: 0,
  margin: -1,
  overflow: 'hidden',
  clip: 'rect(0,0,0,0)',
  whiteSpace: 'nowrap',
  border: 0,
};
