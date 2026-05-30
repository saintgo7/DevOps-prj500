// Outbound webhook signing — kept identical in shape to
// apps/api/src/columns/webhook-signature.ts so the api can verify what the
// worker dispatched (and so partners can verify both).
import { createHmac } from 'node:crypto';

export function signWebhookBody(
  secret: string,
  body: string,
  timestamp: number = Math.floor(Date.now() / 1000),
): string {
  if (!secret) throw new Error('secret required to sign webhook');
  const sig = createHmac('sha256', secret).update(`${timestamp}.${body}`).digest('hex');
  return `t=${timestamp},v1=${sig}`;
}
