import { describe, expect, it } from 'vitest';
import { signWebhookBody, verifyWebhookSignature } from './webhook-signature';

const SECRET = 'partner-shared-secret-at-least-16-long';
const BODY = JSON.stringify({ id: 'col_1', event: 'column.published' });

describe('webhook-signature', () => {
  it('roundtrips a signed body', () => {
    const sig = signWebhookBody(SECRET, BODY);
    const v = verifyWebhookSignature(SECRET, BODY, sig);
    expect(v.ok).toBe(true);
  });

  it('rejects when the body is altered', () => {
    const sig = signWebhookBody(SECRET, BODY);
    const v = verifyWebhookSignature(SECRET, BODY + ' ', sig);
    expect(v.ok).toBe(false);
  });

  it('rejects when the secret differs', () => {
    const sig = signWebhookBody(SECRET, BODY);
    const v = verifyWebhookSignature('a-different-but-equally-long-secret', BODY, sig);
    expect(v.ok).toBe(false);
  });

  it('rejects an old timestamp (replay)', () => {
    const past = Math.floor(Date.now() / 1000) - 60 * 60; // 1h ago
    const sig = signWebhookBody(SECRET, BODY, past);
    const v = verifyWebhookSignature(SECRET, BODY, sig);
    expect(v.ok).toBe(false);
  });

  it('rejects malformed headers', () => {
    expect(verifyWebhookSignature(SECRET, BODY, '').ok).toBe(false);
    expect(verifyWebhookSignature(SECRET, BODY, 'foo=bar').ok).toBe(false);
    expect(verifyWebhookSignature(SECRET, BODY, 't=abc,v1=def').ok).toBe(false);
  });
});
