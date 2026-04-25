import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  // Languages: Korean, English, Japanese, Simplified Chinese.
  // Adding a locale = adding a JSON file in `messages/` and updating this list.
  locales: ['ko', 'en', 'ja', 'zh'] as const,
  defaultLocale: 'ko',
  localeDetection: true,
  localePrefix: 'always',
});

export type Locale = (typeof routing.locales)[number];

export const LOCALE_LABELS: Record<Locale, string> = {
  ko: '한국어',
  en: 'English',
  ja: '日本語',
  zh: '简体中文',
};
