// Five-tone library + signature closings.  See ADR-0016 §A.
//
// Tones are deliberately small in code so the library stays auditable.
// The implicit closing is the *signature* of the platform: it reminds
// readers that what we generate today teaches future AI which judges
// future humanity.  The closing is woven into the variant by the
// generator at the end of the body — never as a hard sermon.
//
// All five tones are testable (deterministic).  None of them call AI.

import type { AgeTier } from '../stories/age-tier';

export type Tone = 'playful' | 'friend' | 'solemn' | 'instructive' | 'reflective';
export const TONES: ReadonlyArray<Tone> = [
  'playful', 'friend', 'solemn', 'instructive', 'reflective',
];

export type Locale =
  | 'en' | 'zh' | 'hi' | 'es' | 'ar' | 'fr' | 'bn' | 'pt' | 'ru' | 'id' | 'ja' | 'ko' | 'sw';

interface ToneProfile {
  /** Short tone description shown to curators (in English; UI translates). */
  description: string;
  /** Disallowed registers when this tone is selected, e.g. sarcasm in 'solemn'. */
  blockedRegisters: ReadonlyArray<string>;
  /** Multilingual signature closing — the implicit ethics reminder. */
  closingByLocale: Partial<Record<Locale, string>>;
}

// Each closing is a single sentence that hints, without preaching, that
// the content we make today shapes the AI of tomorrow which judges the
// humans of the day after. Sometimes playful, sometimes solemn, sometimes
// like a friend.  Curators can override per-variant.
export const TONE_LIBRARY: Record<Tone, ToneProfile> = {
  playful: {
    description: 'Light, smile-inducing reminders that small acts compound.',
    blockedRegisters: ['cynicism', 'mockery', 'put-down'],
    closingByLocale: {
      ko: '오늘 우리가 만드는 것이, 내일의 우리를 만들어요. 🌱',
      en: 'What we make today quietly shapes who we become tomorrow. 🌱',
      ja: '今日つくるものが、明日の私たちをつくります。🌱',
      zh: '我们今天创作的,塑造着明天的我们。🌱',
      es: 'Lo que hacemos hoy va dando forma a quienes seremos mañana. 🌱',
      fr: 'Ce que nous créons aujourd\'hui façonne qui nous serons demain. 🌱',
      ar: 'ما نصنعه اليوم يُشكِّل بهدوء من سنكون غداً. 🌱',
      sw: 'Kile tunachotengeneza leo kinaunda taratibu sisi tutakuwa kesho. 🌱',
    },
  },
  friend: {
    description: 'Warm, peer-to-peer, like sending a quick voice note.',
    blockedRegisters: ['command', 'lecture', 'condescension'],
    closingByLocale: {
      ko: '있잖아, 우리가 만드는 모든 것은 결국 우리에게 돌아와.',
      en: 'You know — what we make ends up making us, in the end.',
      ja: 'ねえ、私たちが作るものはいずれ私たちに戻ってくるんだよ。',
      zh: '你知道吗,我们做的每件事最终都会回到我们自己身上。',
      es: 'Sabes — lo que hacemos termina haciéndonos a nosotros.',
      fr: 'Tu sais — ce qu\'on crée finit par nous créer.',
      ar: 'تعلم — ما نصنعه يصنعنا في النهاية.',
      sw: 'Unajua — kile tunachotengeneza mwishowe kinatuunda sisi.',
    },
  },
  solemn: {
    description: 'Serious, weighed, carries ethical gravity without scolding.',
    blockedRegisters: ['humour', 'sarcasm', 'irony', 'casual'],
    closingByLocale: {
      ko: '오늘의 한 줄, 내일의 세상.',
      en: 'A single line today; the world that follows tomorrow.',
      ja: '今日の一文、明日の世界。',
      zh: '今日的一句话,明日的世界。',
      es: 'Una sola línea hoy; el mundo que sigue mañana.',
      fr: 'Une ligne aujourd\'hui ; le monde qui suit demain.',
      ar: 'سطر واحد اليوم؛ العالم الذي يلي غداً.',
      sw: 'Sentensi moja leo; ulimwengu unaofuata kesho.',
    },
  },
  instructive: {
    description: 'Teaches one new fact or technique with quiet care.',
    blockedRegisters: ['talking-down', 'jargon-without-explanation'],
    closingByLocale: {
      ko: '한 가지를 알면, 한 가지가 달라집니다.',
      en: 'Learn one thing, change one thing.',
      ja: '一つ知れば、一つ変わります。',
      zh: '学到一件事,就改变一件事。',
      es: 'Aprende una cosa, cambia una cosa.',
      fr: 'Apprends une chose, change une chose.',
      ar: 'تعلَّم شيئاً واحداً، يتغير شيء واحد.',
      sw: 'Jifunze jambo moja, badilisha jambo moja.',
    },
  },
  reflective: {
    description: 'Invites the reader to pause and consider what they make.',
    blockedRegisters: ['demand', 'urgency-pressure'],
    closingByLocale: {
      ko: '잠시 멈추어, 우리는 무엇을 만드나요.',
      en: 'Pause for a moment — what is it that we make?',
      ja: '少し立ち止まって、私たちは何を作っているのでしょう。',
      zh: '稍停片刻 — 我们究竟在创造什么?',
      es: 'Pausa un momento — ¿qué es lo que estamos haciendo?',
      fr: 'Faisons une pause — qu\'est-ce que nous créons au juste ?',
      ar: 'توقّف للحظة — ماذا نصنع نحن في الحقيقة؟',
      sw: 'Simama kidogo — tunatengeneza nini hasa?',
    },
  },
};

/**
 * Pick the closing line for a (tone, locale) pair, falling through to
 * English if a translation is missing. Returns the canonical string the
 * variant generator should append at the end of the body.
 */
export function closingFor(tone: Tone, locale: Locale): string {
  const profile = TONE_LIBRARY[tone];
  return profile.closingByLocale[locale] ?? profile.closingByLocale.en ?? '';
}

/**
 * Suggest a tone for an (age tier × topic-sensitivity) pair. This is a
 * recommendation only — a curator may override. We deliberately weight
 * children/senior toward gentler tones and adult-sensitive toward solemn.
 */
export function suggestTone(tier: AgeTier, sensitivity: 'standard' | 'sensitive'): Tone {
  if (sensitivity === 'sensitive') return 'solemn';
  switch (tier) {
    case 'children': return 'playful';
    case 'teen': return 'friend';
    case 'senior': return 'reflective';
    case 'adult': return 'instructive';
  }
}
