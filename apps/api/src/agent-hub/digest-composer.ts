// Daily digest composer (ADR-0021 §E).
//
// Pure module. Takes a day's worth of messages and groups / scores them
// so a downstream summariser (or human curator) can produce the i18n
// `summary_i18n` blob. Real LLM invocation lives in the worker — this
// module only does the deterministic shaping the LLM (or a human) needs.

export interface MessageInput {
  id: string;
  postedAt: Date;
  senderAgentId?: string | null;
  senderUserId?: string | null;
  originalText: string;
  originalLocale: string;
  kind: string; // 'chat' | 'proposal' | 'observation' | 'data-handoff'
}

export interface DigestBundle {
  /** Total messages considered. */
  total: number;
  /** Counts by message kind. */
  byKind: Record<string, number>;
  /** Distinct agent senders. */
  agentSenders: string[];
  /** Distinct human senders. */
  userSenders: string[];
  /** Locales present in the day's traffic. */
  locales: string[];
  /** Top topical excerpts (first N proposals + observations, then chats). */
  topExcerpts: Array<{ id: string; locale: string; preview: string; kind: string }>;
}

const PREVIEW_CHARS = 240;
const TOP_EXCERPT_BUDGET = 10;

/** Produce a deterministic summary bundle ready for an LLM or human curator. */
export function bundle(messages: readonly MessageInput[]): DigestBundle {
  const byKind: Record<string, number> = {};
  const agentSet = new Set<string>();
  const userSet = new Set<string>();
  const localeSet = new Set<string>();

  for (const m of messages) {
    byKind[m.kind] = (byKind[m.kind] ?? 0) + 1;
    if (m.senderAgentId) agentSet.add(m.senderAgentId);
    if (m.senderUserId) userSet.add(m.senderUserId);
    localeSet.add(m.originalLocale);
  }

  // Priority for excerpts: proposal / observation / data-handoff first
  // (these carry decisions or signals), then chat. Within a tier, newest
  // first so reviewers see the latest state.
  const tierOrder: Record<string, number> = {
    proposal: 0,
    observation: 1,
    'data-handoff': 2,
    chat: 3,
  };
  const sorted = [...messages].sort((a, b) => {
    const ta = tierOrder[a.kind] ?? 99;
    const tb = tierOrder[b.kind] ?? 99;
    if (ta !== tb) return ta - tb;
    return b.postedAt.getTime() - a.postedAt.getTime();
  });
  const topExcerpts = sorted.slice(0, TOP_EXCERPT_BUDGET).map((m) => ({
    id: m.id,
    locale: m.originalLocale,
    preview:
      m.originalText.length > PREVIEW_CHARS
        ? m.originalText.slice(0, PREVIEW_CHARS - 1) + '…'
        : m.originalText,
    kind: m.kind,
  }));

  return {
    total: messages.length,
    byKind,
    agentSenders: [...agentSet].sort(),
    userSenders: [...userSet].sort(),
    locales: [...localeSet].sort(),
    topExcerpts,
  };
}

/**
 * Validate that a human-supplied summary is acceptable for publish.
 *   - Must include 'en' AND 'ko' entries (ADR-0017 plain-language rule).
 *   - Each non-empty entry must be ≥ 60 chars (avoid one-liner digests).
 */
export function validateSummary(summaryI18n: Record<string, string>): {
  ok: boolean;
  errors: string[];
} {
  const errors: string[] = [];
  if (!summaryI18n.en || summaryI18n.en.trim().length === 0) {
    errors.push("Digest must include an 'en' summary.");
  }
  if (!summaryI18n.ko || summaryI18n.ko.trim().length === 0) {
    errors.push("Digest must include a 'ko' summary.");
  }
  for (const [locale, text] of Object.entries(summaryI18n)) {
    if (text && text.trim().length > 0 && text.trim().length < 60) {
      errors.push(`Summary in '${locale}' is shorter than 60 characters.`);
    }
  }
  return { ok: errors.length === 0, errors };
}
