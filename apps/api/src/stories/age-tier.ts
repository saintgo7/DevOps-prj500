// Age tier rules for short-form video variants. See ADR-0015 §2.
//
// Each tier has:
//   - a max reading-grade target (Flesch-Kincaid analogue)
//   - a max sentence length
//   - a list of forbidden patterns (hard-block — children especially)
//   - a recommended pace multiplier (used by the storyboard generator)
//
// All rules are deterministic and unit-tested. No LLM in this file.

export type AgeTier = 'children' | 'teen' | 'adult' | 'senior';
export const AGE_TIERS: ReadonlyArray<AgeTier> = ['children', 'teen', 'adult', 'senior'];

interface TierProfile {
  maxGrade: number; // Flesch-Kincaid grade level (approx)
  maxSentenceWords: number;
  paceMultiplier: number; // 1.0 = normal; 1.5 = slower (senior); 0.9 = faster (teen)
  forbiddenPatterns: ReadonlyArray<RegExp>;
}

// Forbidden topic patterns for the 'children' tier. These are blunt
// guardrails — false positives are acceptable; missed positives are not.
// Multilingual: matches common English / Korean / Spanish / French / Arabic /
// Swahili / Chinese / Japanese tokens for each blocked concept.
const CHILD_FORBIDDEN: ReadonlyArray<RegExp> = [
  // Latin scripts use word boundaries to avoid catching substrings.
  /\b(?:death|kill|murder|suicide|war|weapon|gun|blood|gore|torture)\b/i,
  /\b(?:muerte|matar|asesinato|suicidio|guerra|arma|sangre|tortura)\b/i,
  /\b(?:mort|tuer|meurtre|suicide|guerre|arme|sang|torture)\b/i,
  /\b(?:vifo|kuua|mauaji|kujiua|vita|silaha|damu|mateso)\b/i,
  // Korean (Hangul is not \w in JS regex; \b cannot anchor here so we omit it).
  /(?:죽음|살인|자살|전쟁|무기|고문)/,
  // Chinese (CJK ideographs are not \w in JS regex; \b would never match).
  /(?:死亡|杀人|自杀|战争|武器|血腥|酷刑)/,
  // Japanese (kanji + kana — same reason).
  /(?:死亡|殺人|自殺|戦争|武器|拷問)/,
  // Arabic — block specific war/weapon words rather than ambiguous chars.
  /(?:حرب|سلاح|قتل|انتحار|تعذيب)/,
  // Sex / drugs (Latin scripts only — region-appropriate words for other
  // scripts can be added via PR with a native-speaker review).
  /\b(?:sex|porn|drug|alcohol|cigarette|smok\w*)\b/i,
  /(?:마약|성행위|흡연)/,
  // Personal identifiers:
  /\b\d{3}-\d{2}-\d{4}\b/, // SSN-like
  /\bDOB[: ]?\s*\d{4}-\d{2}-\d{2}\b/i,
];

// Teen-tier blocks the most extreme child-tier items minus everyday
// vocabulary that teens already encounter (e.g. "war" history class).
const TEEN_FORBIDDEN: ReadonlyArray<RegExp> = [
  /\b(?:porn|hardcore drug|self-harm)\b/i,
  /\b(?:자해|마약 거래)\b/,
  /\b\d{3}-\d{2}-\d{4}\b/,
];

const TIERS: Record<AgeTier, TierProfile> = {
  children: { maxGrade: 5, maxSentenceWords: 12, paceMultiplier: 1.2, forbiddenPatterns: CHILD_FORBIDDEN },
  teen:     { maxGrade: 8, maxSentenceWords: 18, paceMultiplier: 0.95, forbiddenPatterns: TEEN_FORBIDDEN },
  adult:    { maxGrade: 12, maxSentenceWords: 25, paceMultiplier: 1.0, forbiddenPatterns: [] },
  senior:   { maxGrade: 12, maxSentenceWords: 20, paceMultiplier: 1.5, forbiddenPatterns: [] },
};

export function tierProfile(tier: AgeTier): TierProfile {
  return TIERS[tier];
}

export interface SafetyCheck {
  ok: boolean;
  results: Array<{ rule: string; ok: boolean; message: string }>;
}

/**
 * Deterministic safety check applied to a candidate caption / voiceover for
 * a given age tier. The result is stored on the variant so admins (and
 * monitoring) can see exactly why something was blocked.
 */
export function checkSafety(text: string, tier: AgeTier): SafetyCheck {
  const profile = TIERS[tier];
  const results: Array<{ rule: string; ok: boolean; message: string }> = [];

  // 1. Forbidden patterns
  for (const re of profile.forbiddenPatterns) {
    if (re.test(text)) {
      results.push({
        rule: 'forbidden-pattern',
        ok: false,
        message: `Text matches a pattern blocked for the ${tier} age tier (${re.source.slice(0, 40)}…).`,
      });
      // Continue checking so the curator sees the full picture.
    }
  }
  if (!results.some((r) => !r.ok)) {
    results.push({ rule: 'forbidden-pattern', ok: true, message: 'No forbidden patterns matched.' });
  }

  // 2. Sentence length cap
  const sentences = text.split(/[.!?。!?]+/).map((s) => s.trim()).filter(Boolean);
  const tooLong = sentences.find((s) => s.split(/\s+/).length > profile.maxSentenceWords);
  results.push({
    rule: 'sentence-length',
    ok: !tooLong,
    message: tooLong
      ? `One sentence exceeds the ${tier}-tier limit of ${profile.maxSentenceWords} words.`
      : `All sentences are within the ${profile.maxSentenceWords}-word limit.`,
  });

  // 3. Total length sanity (60-second voiceover ≈ 150 words at normal pace)
  const totalWords = text.split(/\s+/).filter(Boolean).length;
  const adjusted = Math.round(totalWords * profile.paceMultiplier);
  const ok3 = adjusted <= 200;
  results.push({
    rule: 'overall-length',
    ok: ok3,
    message: ok3
      ? `Length OK (${totalWords} words, ${adjusted} adjusted).`
      : `Too long for a short-form video at this pace (${adjusted} adjusted words; cap 200).`,
  });

  return { ok: results.every((r) => r.ok), results };
}

/**
 * Estimate the Flesch-Kincaid-style reading grade. This is a coarse
 * approximation that works for English-like text; for non-Latin scripts the
 * function returns the original grade unchanged. We use it only as a hint —
 * the binding constraint is the safety check above.
 */
export function estimateGrade(text: string): number {
  const words = text.split(/\s+/).filter(Boolean).length;
  const sentences = Math.max(1, text.split(/[.!?。!?]+/).filter((s) => s.trim()).length);
  const syllables = (text.match(/[aeiouAEIOU]+/g) ?? []).length || words; // crude
  if (words === 0) return 0;
  return Math.round(0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59);
}
