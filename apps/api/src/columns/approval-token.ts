import { createHmac, timingSafeEqual } from 'node:crypto';

// Approval token format (see ADR-0013 §3):
//   token = base64url(payload) + "." + base64url(hmac_sha256(secret, payload))
//   payload = JSON({ v: 1, kind: 'approve'|'reject'|'revise', requestId, exp })
//
// The token is delivered via email/SMS one-tap links. It contains NO personal
// data and is single-use (the DB row's decided_at field guards re-use). The
// token expires at `exp` (Unix seconds). Verification is constant-time.

export type ApprovalKind = 'approve' | 'reject' | 'revise';

export interface ApprovalPayload {
  v: 1;
  kind: ApprovalKind;
  requestId: string;
  exp: number; // unix seconds
}

const ENCODE_VERSION = 1;
const TTL_SECONDS = 72 * 60 * 60; // 72 hours

export class ApprovalTokenError extends Error {
  constructor(
    message: string,
    public readonly code:
      | 'malformed'
      | 'bad_signature'
      | 'expired'
      | 'wrong_version',
  ) {
    super(message);
  }
}

export function issueApprovalToken(
  secret: string,
  kind: ApprovalKind,
  requestId: string,
  now: Date = new Date(),
): { token: string; payload: ApprovalPayload } {
  if (!secret || secret.length < 16) {
    throw new Error('approval secret must be set and at least 16 chars');
  }
  const payload: ApprovalPayload = {
    v: ENCODE_VERSION,
    kind,
    requestId,
    exp: Math.floor(now.getTime() / 1000) + TTL_SECONDS,
  };
  const payloadJson = JSON.stringify(payload);
  const payloadB64 = base64url(Buffer.from(payloadJson, 'utf8'));
  const sig = sign(secret, payloadB64);
  return { token: `${payloadB64}.${sig}`, payload };
}

export function verifyApprovalToken(
  secret: string,
  token: string,
  now: Date = new Date(),
): ApprovalPayload {
  if (!secret) throw new ApprovalTokenError('secret missing', 'bad_signature');
  const dot = token.indexOf('.');
  if (dot <= 0 || dot === token.length - 1) {
    throw new ApprovalTokenError('token has no signature', 'malformed');
  }
  const payloadB64 = token.slice(0, dot);
  const sig = token.slice(dot + 1);
  const expected = sign(secret, payloadB64);
  if (!safeEqual(sig, expected)) {
    throw new ApprovalTokenError('signature mismatch', 'bad_signature');
  }
  let payload: ApprovalPayload;
  try {
    payload = JSON.parse(
      Buffer.from(payloadB64.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8'),
    ) as ApprovalPayload;
  } catch {
    throw new ApprovalTokenError('payload not JSON', 'malformed');
  }
  if (payload.v !== ENCODE_VERSION) {
    throw new ApprovalTokenError(`unsupported token version ${payload.v}`, 'wrong_version');
  }
  if (typeof payload.exp !== 'number' || payload.exp * 1000 < now.getTime()) {
    throw new ApprovalTokenError('token expired', 'expired');
  }
  if (
    typeof payload.requestId !== 'string' ||
    !['approve', 'reject', 'revise'].includes(payload.kind)
  ) {
    throw new ApprovalTokenError('payload fields invalid', 'malformed');
  }
  return payload;
}

function sign(secret: string, data: string): string {
  return base64url(createHmac('sha256', secret).update(data).digest());
}

function base64url(buf: Buffer): string {
  return buf.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function safeEqual(a: string, b: string): boolean {
  const aBuf = Buffer.from(a, 'utf8');
  const bBuf = Buffer.from(b, 'utf8');
  if (aBuf.length !== bBuf.length) return false;
  return timingSafeEqual(aBuf, bBuf);
}
