// Hashtag library per SDG × locale. See ADR-0015 §5.
//
// Curated lists are kept short and culturally-appropriate per locale.
// Anyone can submit a PR to add or refine entries; PRs touching this file
// must include a native-speaker reviewer.
//
// The composer combines:
//   - SDG-specific tags (per locale, with English fallback)
//   - LDC-visibility tags when applicable (#GlobalSouth #LDCs #Local2030)
//   - per-platform trim to the recommended count

// Locales we curate hashtags for. Mirrors apps/web/src/i18n/routing.ts but
// kept independent so changes to the web list do not silently change API
// behaviour without an explicit PR here.
export type Locale =
  | 'en' | 'zh' | 'hi' | 'es' | 'ar' | 'fr' | 'bn' | 'pt' | 'ru' | 'id' | 'ja' | 'ko' | 'sw';

export type Platform =
  | 'youtube_shorts'
  | 'instagram_reels'
  | 'tiktok'
  | 'x_video'
  | 'facebook_reels'
  | 'linkedin_video'
  | 'kakao_clip'
  | 'weibo_video';

const RECOMMENDED_COUNT: Record<Platform, number> = {
  youtube_shorts: 3,
  instagram_reels: 10,
  tiktok: 4,
  x_video: 2,
  facebook_reels: 8,
  linkedin_video: 5,
  kakao_clip: 5,
  weibo_video: 8,
};

// Subset of SDG-specific tags. The English column is always available as
// fallback when a locale entry is missing. Hand-curated; expand via PR.
type LocaleTags = Partial<Record<string, ReadonlyArray<string>>>;

const TAGS_BY_GOAL: Record<string, LocaleTags> = {
  'SDG-1': {
    en: ['#NoPoverty', '#SDG1', '#EndPoverty'],
    ko: ['#빈곤종식', '#SDG1', '#노포버티'],
    ja: ['#貧困をなくそう', '#SDG1'],
    zh: ['#无贫穷', '#SDG1'],
    es: ['#FinDeLaPobreza', '#ODS1', '#SinPobreza'],
    fr: ['#PasDePauvreté', '#ODD1'],
    ar: ['#القضاء_على_الفقر', '#SDG1'],
    sw: ['#KomeshaUmaskini', '#SDG1'],
    hi: ['#गरीबीउन्मूलन', '#SDG1'],
    bn: ['#দারিদ্র্যবিমোচন', '#SDG1'],
    pt: ['#ErradicarAPobreza', '#ODS1'],
    ru: ['#БезБедности', '#ЦУР1'],
    id: ['#TanpaKemiskinan', '#SDG1'],
  },
  'SDG-3': {
    en: ['#GoodHealth', '#SDG3', '#WellBeing'],
    ko: ['#건강과웰빙', '#SDG3'],
    ja: ['#すべての人に健康と福祉を', '#SDG3'],
    zh: ['#良好健康与福祉', '#SDG3'],
    es: ['#SaludYBienestar', '#ODS3'],
    fr: ['#SantéEtBienÊtre', '#ODD3'],
    ar: ['#الصحة_الجيدة', '#SDG3'],
    sw: ['#AfyaBora', '#SDG3'],
    hi: ['#अच्छास्वास्थ्य', '#SDG3'],
    bn: ['#সুস্বাস্থ্য', '#SDG3'],
    pt: ['#SaúdeEBemEstar', '#ODS3'],
    ru: ['#Здоровье', '#ЦУР3'],
    id: ['#KesehatanYangBaik', '#SDG3'],
  },
  'SDG-4': {
    en: ['#QualityEducation', '#SDG4', '#EducationForAll'],
    ko: ['#양질의교육', '#SDG4', '#모두를위한교육'],
    ja: ['#質の高い教育をみんなに', '#SDG4'],
    zh: ['#优质教育', '#SDG4'],
    es: ['#EducaciónDeCalidad', '#ODS4'],
    fr: ['#ÉducationDeQualité', '#ODD4'],
    ar: ['#التعليم_الجيد', '#SDG4'],
    sw: ['#ElimuBora', '#SDG4'],
    hi: ['#गुणवत्तापूर्णशिक्षा', '#SDG4'],
    bn: ['#মানসম্মতশিক্ষা', '#SDG4'],
    pt: ['#EducaçãoDeQualidade', '#ODS4'],
    ru: ['#КачественноеОбразование', '#ЦУР4'],
    id: ['#PendidikanBerkualitas', '#SDG4'],
  },
  'SDG-5': {
    en: ['#GenderEquality', '#SDG5'],
    ko: ['#성평등', '#SDG5'],
    es: ['#IgualdadDeGénero', '#ODS5'],
    fr: ['#ÉgalitéDesGenres', '#ODD5'],
    ar: ['#المساواة_بين_الجنسين', '#SDG5'],
    sw: ['#UsawaKijinsia', '#SDG5'],
  },
  'SDG-6': {
    en: ['#CleanWater', '#SDG6', '#WaterForAll'],
    ko: ['#깨끗한물', '#SDG6'],
    sw: ['#MajiSafi', '#SDG6'],
    fr: ['#EauPropre', '#ODD6'],
  },
  'SDG-13': {
    en: ['#ClimateAction', '#SDG13', '#ClimateCrisis'],
    ko: ['#기후행동', '#SDG13', '#기후위기', '#탄소중립'],
    ja: ['#気候変動', '#SDG13'],
    zh: ['#气候行动', '#SDG13'],
    es: ['#AcciónClimática', '#ODS13'],
    fr: ['#ActionClimat', '#ODD13'],
    ar: ['#العمل_المناخي', '#SDG13'],
    sw: ['#HatuaZaTabianchi', '#SDG13'],
    hi: ['#जलवायुकार्रवाई', '#SDG13'],
    bn: ['#জলবায়ুপদক্ষেপ', '#SDG13'],
    pt: ['#AçãoClimática', '#ODS13'],
    ru: ['#КлиматическоеДействие', '#ЦУР13'],
    id: ['#AksiIklim', '#SDG13'],
  },
  'SDG-17': {
    en: ['#Partnerships', '#SDG17', '#GlobalGoals'],
    ko: ['#파트너십', '#SDG17'],
    fr: ['#Partenariats', '#ODD17'],
    ar: ['#الشراكات', '#SDG17'],
    sw: ['#Ushirikiano', '#SDG17'],
  },
};

// Always-on tags suggested when the source comes from an LDC, to amplify
// global-south voices (per ADR-0015 §7 equity weight).
const LDC_BOOST_TAGS: Record<Locale, ReadonlyArray<string>> = {
  en: ['#GlobalSouth', '#LDCs', '#Local2030'],
  ko: ['#글로벌사우스', '#LDC', '#Local2030'],
  ja: ['#グローバルサウス', '#LDC', '#Local2030'],
  zh: ['#全球南方', '#LDC', '#Local2030'],
  es: ['#SurGlobal', '#PMA', '#Local2030'],
  fr: ['#SudGlobal', '#PMA', '#Local2030'],
  ar: ['#الجنوب_العالمي', '#أقل_البلدان_نمواً', '#Local2030'],
  sw: ['#KusiniMwaUlimwengu', '#NchiZilizoendeleaKidogoZaidi', '#Local2030'],
  hi: ['#वैश्विकदक्षिण', '#LDC', '#Local2030'],
  bn: ['#বৈশ্বিকদক্ষিণ', '#LDC', '#Local2030'],
  pt: ['#SulGlobal', '#PMD', '#Local2030'],
  ru: ['#ГлобальныйЮг', '#НРС', '#Local2030'],
  id: ['#GlobalSelatan', '#LDC', '#Local2030'],
};

export interface ComposeOptions {
  goalIds: ReadonlyArray<string>;
  locale: Locale;
  platform: Platform;
  isLdcOrigin?: boolean;
}

/**
 * Compose a final hashtag list for one (sdg × locale × platform) post.
 * - Pulls SDG-specific tags from TAGS_BY_GOAL with English fallback.
 * - Optionally appends the LDC-boost set.
 * - De-duplicates while preserving insertion order.
 * - Trims to the platform's recommended count (or all when 0).
 */
export function composeHashtags(opts: ComposeOptions): string[] {
  const out: string[] = [];
  for (const goal of opts.goalIds) {
    const byLocale = TAGS_BY_GOAL[goal] ?? {};
    const localTags = byLocale[opts.locale] ?? byLocale.en ?? [];
    for (const t of localTags) if (!out.includes(t)) out.push(t);
  }
  if (opts.isLdcOrigin) {
    const boosts = LDC_BOOST_TAGS[opts.locale] ?? LDC_BOOST_TAGS.en ?? [];
    for (const t of boosts) if (!out.includes(t)) out.push(t);
  }
  const cap = RECOMMENDED_COUNT[opts.platform];
  return cap > 0 ? out.slice(0, cap) : out;
}

export function platformCap(platform: Platform): number {
  return RECOMMENDED_COUNT[platform];
}
