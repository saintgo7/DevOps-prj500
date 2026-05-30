import { createHmac, timingSafeEqual } from 'node:crypto';

// Outbound webhook signature header: X-SDGI-Signature
// Format:  t=<unix-seconds>,v1=<hex hmac_sha256(secret, `${t}.${rawBody}`)>
//
// Why the timestamp prefix: it makes replay attacks harder; partner side
// rejects deltas > 5 minutes. This mirrors the Stripe / GitHub convention.

const SCHEME = 'v1';

export function signWebhookBody(
  secret: string,
  body: string,
  timestamp: number = Math.floor(Date.now() / 1000),
): string {
  if (!secret) throw new Error('secret required to sign webhook');
  const signed = `${timestamp}.${body}`;
  const sig = createHmac('sha256', secret).update(signed).digest('hex');
  return `t=${timestamp},${SCHEME}=${sig}`;
}

export function verifyWebhookSignature(
  secret: string,
  body: string,
  header: string,
  toleranceSeconds = 5 * 60,
  now: Date = new Date(),
): { ok: true } | { ok: false; reason: string } {
  if (!header) return { ok: false, reason: 'missing signature header' };
  const parts = Object.fromEntries(
    header.split(',').map((p) => {
      const [k, v] = p.trim().split('=');
      return [k ?? '', v ?? ''];
    }),
  ) as Record<string, string>;
  const t = Number(parts['t']);
  const provided = parts[SCHEME];
  if (!Number.isFinite(t) || !provided) {
    return { ok: false, reason: 'malformed signature header' };
  }
  if (Math.abs(now.getTime() / 1000 - t) > toleranceSeconds) {
    return { ok: false, reason: 'timestamp outside tolerance window' };
  }
  const expected = createHmac('sha256', secret).update(`${t}.${body}`).digest('hex');
  const provBuf = Buffer.from(provided, 'hex');
  const expBuf = Buffer.from(expected, 'hex');
  if (provBuf.length !== expBuf.length || !timingSafeEqual(provBuf, expBuf)) {
    return { ok: false, reason: 'signature mismatch' };
  }
  return { ok: true };
}
