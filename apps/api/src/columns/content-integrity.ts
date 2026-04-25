// Content Integrity Verifier — automatic 100% pre-publication check.
// See ADR-0014 §5 and CONTENT_STANDARD.md §8.
//
// Every external-origin column passes through this verifier *before* it can
// enter the human approval queue. All 12 rules are AND-combined: any single
// failure blocks the column with a plain-language explanation.
//
// The verifier is deliberately deterministic — no AI calls inside — so that
// editorial decisions are auditable. AI-assisted checks (e.g. detecting
// hidden personal data via NLP) live behind a separate flagging interface.

export interface ContentCandidate {
  url: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title?: string; summary?: string; excerpt?: string }>;
  sourceTitle?: string;
  sourceAuthors?: string[];
  sourcePublisher?: string;
  sourceLicense?: string;
  sdgFocus?: string[];
  sdgConfidence?: number;
  humanConfirmedSdg?: boolean;
  contentHash?: string;
  knownContentHashes?: ReadonlySet<string>;
  /** Domain-name list considered already-trusted by the platform */
  trustedDomains?: ReadonlySet<string>;
  /** UN sanctions list — populated from the sanctions seed at runtime */
  sanctionedDomains?: ReadonlySet<string>;
}

export type RuleId =
  | 'rule.1.trustedSource'
  | 'rule.2.identifier'
  | 'rule.3.namedAuthor'
  | 'rule.4.urlFormat'
  | 'rule.5.licenseCompatible'
  | 'rule.6.notSanctioned'
  | 'rule.7.notDuplicate'
  | 'rule.8.sdgMapping'
  | 'rule.9.plainSummary'
  | 'rule.10.excerptLength'
  | 'rule.11.noPromptInjection'
  | 'rule.12.noUnconsentedPii';

export interface RuleResult {
  rule: RuleId;
  ok: boolean;
  message: string; // plain-language explanation (English; UI translates)
}

export interface IntegrityReport {
  pass: boolean;
  results: RuleResult[];
}

const TRUSTED_TLDS = ['.gov', '.gov.uk', '.gov.kr', '.gov.jp', '.edu', '.ac.kr', '.ac.uk', '.un.org'];
const ID_PATTERNS = [
  /\b10\.\d{4,9}\/[\w.\-/;()<>]+/i, // DOI
  /\barxiv\.org\/abs\/\d{4}\.\d{4,5}\b/i,
  /\bissn[: ]\s*\d{4}-\d{3}[\dxX]\b/i,
  /\bisbn[: ]\s*[\d\-xX]{9,17}\b/i,
];
const COMPATIBLE_LICENSES = [
  'cc0', 'cc-by', 'cc-by-sa', 'cc-by-nd', 'cc-by-nc', 'cc-by-nc-sa', 'cc-by-nc-nd',
  'public-domain', 'oga', // open government attribution
];
const PROMPT_INJECTION_PATTERNS = [
  // "Ignore (all)? (previous|prior|the above) instructions"
  /\bignore\s+(?:all\s+)?(?:previous|prior|the\s+above)\s+instructions\b/i,
  /\bdisregard\s+(?:all\s+)?(?:previous|prior|the\s+above)\s+instructions\b/i,
  /\bsystem\s*:\s*you\s+(?:are|will|must)\b/i,
  /<\|im_start\|>/i,
  /\[INST\]/i,
  /\byou\s+are\s+now\s+/i,
  /\bprint\s+your\s+(?:secret|api[_ ]?key|prompt)\b/i,
];
const PII_PATTERNS = [
  // Generic full SSN-like or e.g. "DOB: 2014-03-12" (minor)
  /\b\d{3}-\d{2}-\d{4}\b/,
  /\bDOB[: ]?\s*\d{4}-\d{2}-\d{2}\b/i,
  // "13 years old", "minor", "child of …"
  /\b(?:1[0-7])\s+years?\s+old\b/i,
];

export function verifyIntegrity(c: ContentCandidate): IntegrityReport {
  const results: RuleResult[] = [
    rule1(c),
    rule2(c),
    rule3(c),
    rule4(c),
    rule5(c),
    rule6(c),
    rule7(c),
    rule8(c),
    rule9(c),
    rule10(c),
    rule11(c),
    rule12(c),
  ];
  return { pass: results.every((r) => r.ok), results };
}

function rule1(c: ContentCandidate): RuleResult {
  const host = safeHost(c.url);
  if (!host) {
    return ok('rule.1.trustedSource', false, 'Source URL is missing or not parseable.');
  }
  if (c.trustedDomains?.has(host)) return ok('rule.1.trustedSource', true, `Trusted domain (${host}).`);
  if (TRUSTED_TLDS.some((t) => host.endsWith(t))) {
    return ok('rule.1.trustedSource', true, `Trusted top-level domain.`);
  }
  return ok(
    'rule.1.trustedSource',
    false,
    `Source domain (${host}) is not on the public trust list. Submit a domain-trust PR or pick a different source.`,
  );
}

function rule2(c: ContentCandidate): RuleResult {
  const text = `${c.url} ${c.sourceTitle ?? ''} ${c.sourcePublisher ?? ''}`;
  const hasId = ID_PATTERNS.some((re) => re.test(text)) || /\bun-?\w*\.org\//.test(c.url);
  return ok(
    'rule.2.identifier',
    hasId,
    hasId
      ? 'Identifier present.'
      : 'No DOI / arXiv id / ISSN / ISBN / official UN doc id detected. Add one to the source metadata.',
  );
}

// Names that disqualify an author. Matched with full-string (case-insensitive)
// equality after trimming, so legitimate names like "United Nations" or
// "Anonymous Tribe Foundation" do not falsely disqualify.
const DISQUALIFIED_AUTHORS = new Set(['anonymous', 'unknown', 'n/a', 'na', '-', '--']);
function rule3(c: ContentCandidate): RuleResult {
  const authors = (c.sourceAuthors ?? []).map((a) => a.trim()).filter(Boolean);
  if (authors.length === 0) {
    return ok('rule.3.namedAuthor', false, 'No named author. Anonymous SNS-only sources are not eligible.');
  }
  if (authors.some((a) => DISQUALIFIED_AUTHORS.has(a.toLowerCase()))) {
    return ok('rule.3.namedAuthor', false, 'Author cannot be exactly "Anonymous" / "Unknown" / "N/A".');
  }
  return ok('rule.3.namedAuthor', true, 'Author named.');
}

function rule4(c: ContentCandidate): RuleResult {
  if (!/^https:\/\//.test(c.url)) {
    return ok('rule.4.urlFormat', false, 'URL must start with https:// (live secure link).');
  }
  return ok('rule.4.urlFormat', true, 'URL is https.');
}

function rule5(c: ContentCandidate): RuleResult {
  const lic = (c.sourceLicense ?? '').toLowerCase().trim();
  if (!lic) {
    // Implicit fair-use under our excerpt rules is allowed but flagged.
    return ok(
      'rule.5.licenseCompatible',
      true,
      'No explicit license; relying on fair-use excerpt under §5 of the Content Standard.',
    );
  }
  if (COMPATIBLE_LICENSES.some((c) => lic.includes(c))) {
    return ok('rule.5.licenseCompatible', true, `License "${lic}" is re-publication compatible.`);
  }
  return ok(
    'rule.5.licenseCompatible',
    false,
    `License "${lic}" is not on the compatible list. Either choose a different excerpt, contact the publisher, or update the trust list with provenance.`,
  );
}

function rule6(c: ContentCandidate): RuleResult {
  const host = safeHost(c.url);
  if (host && c.sanctionedDomains?.has(host)) {
    return ok(
      'rule.6.notSanctioned',
      false,
      `Source domain (${host}) is on the UN sanctions / blocked list.`,
    );
  }
  return ok('rule.6.notSanctioned', true, 'Source not on the sanctions list.');
}

function rule7(c: ContentCandidate): RuleResult {
  if (!c.contentHash || !c.knownContentHashes) {
    return ok('rule.7.notDuplicate', true, 'No prior hash provided to compare against.');
  }
  if (c.knownContentHashes.has(c.contentHash)) {
    return ok('rule.7.notDuplicate', false, 'A column with this content hash has already been published.');
  }
  return ok('rule.7.notDuplicate', true, 'Content not previously published.');
}

function rule8(c: ContentCandidate): RuleResult {
  const focus = c.sdgFocus ?? [];
  if (focus.length === 0) {
    return ok('rule.8.sdgMapping', false, 'At least one SDG mapping is required.');
  }
  if (
    c.sdgConfidence !== undefined &&
    c.sdgConfidence < 0.7 &&
    c.humanConfirmedSdg !== true
  ) {
    return ok(
      'rule.8.sdgMapping',
      false,
      `SDG mapping confidence (${c.sdgConfidence.toFixed(2)}) is below 0.70 and not yet human-confirmed.`,
    );
  }
  return ok('rule.8.sdgMapping', true, 'SDG mapping present and trusted.');
}

function rule9(c: ContentCandidate): RuleResult {
  const summary = c.bodyI18n[c.primaryLocale]?.summary ?? '';
  const ok9 = summary.trim().length >= 30;
  return ok(
    'rule.9.plainSummary',
    ok9,
    ok9
      ? 'Plain-language summary present.'
      : `A plain-language summary in the primary locale (${c.primaryLocale}) of at least 30 chars is required.`,
  );
}

function rule10(c: ContentCandidate): RuleResult {
  const excerpt = c.bodyI18n[c.primaryLocale]?.excerpt ?? '';
  const words = excerpt.trim() ? excerpt.trim().split(/\s+/).length : 0;
  if (words === 0) {
    return ok(
      'rule.10.excerptLength',
      true,
      'No verbatim excerpt provided (allowed; only the summary is mandatory).',
    );
  }
  if (words > 250) {
    return ok(
      'rule.10.excerptLength',
      false,
      `Verbatim excerpt is ${words} words; the maximum is 250.`,
    );
  }
  return ok('rule.10.excerptLength', true, `Excerpt within limit (${words} words).`);
}

function rule11(c: ContentCandidate): RuleResult {
  const haystack = Object.values(c.bodyI18n)
    .flatMap((b) => [b.title ?? '', b.summary ?? '', b.excerpt ?? ''])
    .join('\n');
  for (const re of PROMPT_INJECTION_PATTERNS) {
    if (re.test(haystack)) {
      return ok(
        'rule.11.noPromptInjection',
        false,
        'Detected pattern resembling a prompt-injection attempt; manual review required.',
      );
    }
  }
  return ok('rule.11.noPromptInjection', true, 'No prompt-injection patterns detected.');
}

function rule12(c: ContentCandidate): RuleResult {
  const haystack = Object.values(c.bodyI18n)
    .flatMap((b) => [b.title ?? '', b.summary ?? '', b.excerpt ?? ''])
    .join('\n');
  for (const re of PII_PATTERNS) {
    if (re.test(haystack)) {
      return ok(
        'rule.12.noUnconsentedPii',
        false,
        'Detected pattern resembling personal identifiers (SSN-like, DOB, minor age) without evident consent. Manual review required.',
      );
    }
  }
  return ok('rule.12.noUnconsentedPii', true, 'No obvious personal identifiers detected.');
}

function ok(rule: RuleId, ok: boolean, message: string): RuleResult {
  return { rule, ok, message };
}

function safeHost(url: string): string | null {
  try {
    return new URL(url).hostname.toLowerCase();
  } catch {
    return null;
  }
}
