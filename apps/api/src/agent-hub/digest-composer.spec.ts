import { describe, expect, it } from 'vitest';
import { bundle, validateSummary, type MessageInput } from './digest-composer';

function msg(overrides: Partial<MessageInput> = {}): MessageInput {
  return {
    id: 'm-1',
    postedAt: new Date('2026-04-26T10:00:00Z'),
    senderAgentId: null,
    senderUserId: null,
    originalText: 'hello',
    originalLocale: 'en',
    kind: 'chat',
    ...overrides,
  };
}

describe('bundle', () => {
  it('counts total and byKind', () => {
    const r = bundle([
      msg({ id: 'a', kind: 'chat' }),
      msg({ id: 'b', kind: 'chat' }),
      msg({ id: 'c', kind: 'proposal' }),
    ]);
    expect(r.total).toBe(3);
    expect(r.byKind.chat).toBe(2);
    expect(r.byKind.proposal).toBe(1);
  });

  it('captures distinct agent and human senders', () => {
    const r = bundle([
      msg({ id: 'a', senderAgentId: 'agent-1' }),
      msg({ id: 'b', senderAgentId: 'agent-1' }),
      msg({ id: 'c', senderUserId: 'user-1' }),
    ]);
    expect(r.agentSenders).toEqual(['agent-1']);
    expect(r.userSenders).toEqual(['user-1']);
  });

  it('lists locales seen in the day', () => {
    const r = bundle([
      msg({ id: 'a', originalLocale: 'ko' }),
      msg({ id: 'b', originalLocale: 'en' }),
      msg({ id: 'c', originalLocale: 'ko' }),
    ]);
    expect(r.locales).toEqual(['en', 'ko']);
  });

  it('prioritises proposals / observations / handoffs over chat in excerpts', () => {
    const r = bundle([
      msg({ id: 'chat-old', kind: 'chat', postedAt: new Date('2026-04-26T09:00:00Z') }),
      msg({ id: 'observation', kind: 'observation', postedAt: new Date('2026-04-26T08:00:00Z') }),
      msg({ id: 'proposal', kind: 'proposal', postedAt: new Date('2026-04-26T07:00:00Z') }),
    ]);
    const ids = r.topExcerpts.map((e) => e.id);
    expect(ids[0]).toBe('proposal');
    expect(ids[1]).toBe('observation');
    expect(ids[2]).toBe('chat-old');
  });

  it('caps excerpts at 10 and truncates long previews', () => {
    const longText = 'x'.repeat(500);
    const many = Array.from({ length: 25 }, (_, i) =>
      msg({ id: `m-${i}`, originalText: longText, kind: 'chat' }),
    );
    const r = bundle(many);
    expect(r.topExcerpts).toHaveLength(10);
    for (const e of r.topExcerpts) {
      expect(e.preview.length).toBeLessThanOrEqual(240);
      expect(e.preview.endsWith('…')).toBe(true);
    }
  });

  it('handles empty message list', () => {
    const r = bundle([]);
    expect(r.total).toBe(0);
    expect(r.topExcerpts).toEqual([]);
    expect(r.locales).toEqual([]);
  });
});

describe('validateSummary', () => {
  it('requires en + ko summaries', () => {
    expect(validateSummary({ en: 'a'.repeat(70) }).ok).toBe(false);
    expect(validateSummary({ ko: 'a'.repeat(70) }).ok).toBe(false);
  });

  it('rejects too-short summaries', () => {
    const r = validateSummary({ en: 'short', ko: 'a'.repeat(70) });
    expect(r.ok).toBe(false);
  });

  it('accepts valid bilingual digests', () => {
    const r = validateSummary({ en: 'a'.repeat(70), ko: 'b'.repeat(70) });
    expect(r.ok).toBe(true);
  });

  it('allows extra locales beyond en+ko', () => {
    const r = validateSummary({
      en: 'a'.repeat(70),
      ko: 'b'.repeat(70),
      sw: 'c'.repeat(70),
    });
    expect(r.ok).toBe(true);
  });
});
