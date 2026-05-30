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
  defaultLocale: 'ko',
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

/**
 * Map an ISO-3166 alpha-2 country code to the most natural UI locale we
 * support. This is the *default suggestion only* — users always see the
 * language switcher and can override at any time. See ADR-0014.
 *
 * The country list is intentionally LDC-aware: Niger, Chad, Senegal etc.
 * map to French; Tanzania, Kenya, Uganda to Swahili; Bangladesh to Bengali.
 */
const COUNTRY_TO_LOCALE: Record<string, Locale> = {
  // East Asia (operating markets)
  KR: 'ko',
  JP: 'ja',
  CN: 'zh', TW: 'zh', HK: 'zh', MO: 'zh', SG: 'zh',
  // Arabic-speaking states (League of Arab States, 22)
  SA: 'ar', AE: 'ar', EG: 'ar', JO: 'ar', LB: 'ar', SY: 'ar', IQ: 'ar',
  KW: 'ar', QA: 'ar', BH: 'ar', OM: 'ar', YE: 'ar', PS: 'ar',
  DZ: 'ar', TN: 'ar', LY: 'ar', MA: 'ar', SD: 'ar', SO: 'ar',
  DJ: 'ar', KM: 'ar', MR: 'ar',
  // Francophone Africa (sub-Saharan LDC focus)
  SN: 'fr', ML: 'fr', BF: 'fr', NE: 'fr', BJ: 'fr', TG: 'fr',
  CI: 'fr', GN: 'fr', CM: 'fr', GA: 'fr', CG: 'fr', CD: 'fr',
  CF: 'fr', TD: 'fr', BI: 'fr', RW: 'fr', MG: 'fr',
  // Other Francophone
  FR: 'fr', BE: 'fr', CH: 'fr', LU: 'fr', MC: 'fr', CA: 'fr', HT: 'fr',
  // Swahili-speaking East Africa (EAC)
  KE: 'sw', TZ: 'sw', UG: 'sw',
  // Lusophone (Brazil + Lusophone Africa LDCs)
  PT: 'pt', BR: 'pt', AO: 'pt', MZ: 'pt', CV: 'pt',
  GW: 'pt', ST: 'pt', TL: 'pt',
  // Spanish-speaking (Spain + 20 LATAM)
  ES: 'es', MX: 'es', AR: 'es', CO: 'es', PE: 'es', VE: 'es',
  CL: 'es', EC: 'es', GT: 'es', CU: 'es', BO: 'es', DO: 'es',
  HN: 'es', PY: 'es', SV: 'es', NI: 'es', CR: 'es', PA: 'es',
  UY: 'es', PR: 'es', GQ: 'es',
  // South Asia
  IN: 'hi',
  BD: 'bn',
  // Russian / CIS
  RU: 'ru', BY: 'ru', KZ: 'ru', KG: 'ru', TJ: 'ru', UZ: 'ru', TM: 'ru',
  // Indonesia
  ID: 'id',
  // English-default English-speaking
  US: 'en', GB: 'en', AU: 'en', NZ: 'en', IE: 'en',
  ZA: 'en', NG: 'en', GH: 'en', PH: 'en',
};

/**
 * Pick the best UI locale for a given ISO-3166 alpha-2 country code.
 * Returns the platform default ('ko') when no mapping exists. The caller
 * is responsible for honouring user-chosen overrides first.
 */
export function countryToLocale(country: string | undefined | null): Locale {
  if (!country) return routing.defaultLocale;
  const upper = country.toUpperCase();
  return COUNTRY_TO_LOCALE[upper] ?? routing.defaultLocale;
}
