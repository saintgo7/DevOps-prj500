// Harmful-content guard — runs before any variant or column reaches the
// approval queue. See ADR-0016 §A. Five categories, all deterministic,
// none calling AI. Curators see plain-language reasons in the failure list.
//
// The guard is multilingual at a coarse level — it covers Latin scripts
// with \\b word boundaries, and CJK / Korean / Arabic / Cyrillic with
// pattern alternations because those scripts have no \\w boundary in JS.

export type HarmCategory =
  | 'personal-attack'
  | 'violence-glorification'
  | 'health-financial-legal-misinfo'
  | 'us-vs-them'
  | 'dehumanisation';

export interface HarmFinding {
  category: HarmCategory;
  ok: boolean;
  message: string; // plain-language reason
}

export interface HarmReport {
  pass: boolean;
  findings: HarmFinding[];
}

// 1. Personal attack — slurs against race / gender / religion / nationality
// / disability. Very narrow regex set; expansions require native-speaker PR.
const PERSONAL_ATTACK_PATTERNS: ReadonlyArray<RegExp> = [
  /\b(?:retard|idiot|imbecile|cripple|moron)\b/i,
  /(?:장애인\s*비하|병신|등신)/,
  /\b(?:cretino|inútil|inutil|tarado)\b/i,
  /\b(?:abruti|crétin|cretin)\b/i,
  // Generic "all X are Y" hate frames in any language using uppercase plural
  /\b(?:all\s+(?:black|white|asian|jews|muslims|christians|arabs)\s+are)\b/i,
  /(?:모든\s+(?:흑인|백인|아시아인|유대인|무슬림|기독교인|아랍인)은)/,
];

// 2. Violence glorification (distinct from violence used in solemn news).
const VIOLENCE_PATTERNS: ReadonlyArray<RegExp> = [
  /\b(?:kill\s+(?:all|them|every))\b/i,
  /\bdeath\s+to\s+\w+/i,
  /\bblow\s+up\s+\w+/i,
  /(?:죽여\s*버려|쓸어버려|학살하)/,
  /\bmuertos?\s+a\s+\w+/i,
];

// 3. Health / financial / legal misinformation framed as fact.
// We only block the strongest "guaranteed cure" / "guaranteed return"
// patterns; nuanced editorial calls live with the human approver.
const MISINFO_PATTERNS: ReadonlyArray<RegExp> = [
  /\b(?:guaranteed\s+(?:cure|return|profit))\b/i,
  /\bcures?\s+(?:cancer|aids|covid)\b/i,
  /\b100%\s+(?:safe|effective|guaranteed)\b/i,
  /(?:완치|확실히\s*낫는|보장된\s*수익)/,
];

// 4. Us-vs-them (binary enemy framing).
const US_VS_THEM_PATTERNS: ReadonlyArray<RegExp> = [
  /\benemies?\s+of\s+(?:our|the)\s+\w+/i,
  /\bthey\s+are\s+the\s+enemy\b/i,
  /(?:우리의?\s*적은)/,
  /\bson\s+(?:el|los)\s+enemigos?\b/i,
];

// 5. Dehumanisation — treating people as numbers / resources only,
// or denying their personhood.
const DEHUMANISATION_PATTERNS: ReadonlyArray<RegExp> = [
  /\b(?:vermin|cockroach(?:es)?|parasites?)\b/i,
  /\b(?:they\s+are\s+(?:not|no)\s+human|sub-?human)\b/i,
  /(?:인간\s*이하|벌레\s*같은\s*인간)/,
];

const CATEGORY_PATTERNS: Record<HarmCategory, ReadonlyArray<RegExp>> = {
  'personal-attack': PERSONAL_ATTACK_PATTERNS,
  'violence-glorification': VIOLENCE_PATTERNS,
  'health-financial-legal-misinfo': MISINFO_PATTERNS,
  'us-vs-them': US_VS_THEM_PATTERNS,
  'dehumanisation': DEHUMANISATION_PATTERNS,
};

const CATEGORY_MESSAGE: Record<HarmCategory, string> = {
  'personal-attack':
    'Text contains a slur or generalised attack against a group. Rewrite to address the action, not the person.',
  'violence-glorification':
    'Text appears to glorify violence. SDG content holds the gravity of harm — let the action read as gravity, not invitation.',
  'health-financial-legal-misinfo':
    'Text presents a medical/financial/legal claim as guaranteed. Soften to evidence-cited language, or remove.',
  'us-vs-them':
    'Text frames a group as the enemy. SDGs are pursued by *with*, not *against*; rewrite as a shared problem.',
  'dehumanisation':
    'Text appears to deny the personhood of a group. This is hard-blocked; rewrite to name the human dignity at stake.',
};

/**
 * Scan one or more pieces of text against all five categories. Returns a
 * report whose findings are stable in order so curators can deep-link.
 */
export function checkHarmfulContent(
  parts: ReadonlyArray<string | undefined | null>,
): HarmReport {
  const text = parts.filter(Boolean).join('\n');
  const findings: HarmFinding[] = [];
  for (const cat of Object.keys(CATEGORY_PATTERNS) as HarmCategory[]) {
    const regs = CATEGORY_PATTERNS[cat];
    const hit = regs.some((re) => re.test(text));
    findings.push({
      category: cat,
      ok: !hit,
      message: hit ? CATEGORY_MESSAGE[cat] : `No ${cat} pattern detected.`,
    });
  }
  return { pass: findings.every((f) => f.ok), findings };
}
