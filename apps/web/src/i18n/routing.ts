/**
 * Supported UI locales — chosen to maximise SDG-relevant population reach.
 *
 * Selection rationale (Ethnologue 2025 + UN LDC list 2025):
 * - Top-10 by total speakers cover ~60% of humanity.
 * - 'sw' (Swahili) covers East African Community (8 countries, 200M+ speakers,
 *   majority LDC).
 * - 'ar' brings RTL support and 22 Arab states including LDCs (Sudan, Yemen,
 *   Somalia, Comoros, Mauritania, Djibouti).
 * - 'fr' is the working language of 14 of the 32 sub-Saharan African LDCs.
 *
 * Adding a locale = (1) a JSON file in `messages/`, (2) update this list,
 * (3) confirm RTL/font fallback in `LocaleConfig`.
 */
import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  locales: [
    'en', // English — 1.53B
    'zh', // 普通话 — 1.18B
    'hi', // हिन्दी — 609M
    'es', // Español — 558M
    'ar', // العربية — 335M (RTL)
    'fr', // Français — 312M (sub-Saharan LDCs)
    'bn', // বাংলা — 284M
    'pt', // Português — 266M (Lusophone Africa: Angola, Mozambique LDCs)
    'ru', // Русский — 253M
    'id', // Bahasa Indonesia — 252M
    'ja', // 日本語 — 125M
    'ko', // 한국어 — 80M
    'sw', // Kiswahili — 200M+ EAC
  ] as const,
  defaultLocale: 'en',
  localeDetection: true,
  localePrefix: 'always',
});

export type Locale = (typeof routing.locales)[number];

export const LOCALE_LABELS: Record<Locale, string> = {
  en: 'English',
  zh: '简体中文',
  hi: 'हिन्दी',
  es: 'Español',
  ar: 'العربية',
  fr: 'Français',
  bn: 'বাংলা',
  pt: 'Português',
  ru: 'Русский',
  id: 'Bahasa Indonesia',
  ja: '日本語',
  ko: '한국어',
  sw: 'Kiswahili',
};

/** Locales that render right-to-left. */
export const RTL_LOCALES: ReadonlySet<Locale> = new Set(['ar']);

export function dir(locale: Locale): 'ltr' | 'rtl' {
  return RTL_LOCALES.has(locale) ? 'rtl' : 'ltr';
}
