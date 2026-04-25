import { createHmac } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import {
  ApprovalTokenError,
  issueApprovalToken,
  verifyApprovalToken,
} from './approval-token';

const SECRET = 'a-test-secret-at-least-16-chars-long';
const REQUEST_ID = 'req_01HZABCDEFGHJKMNPQRSTV';

describe('approval-token', () => {
  it('round-trips approve / reject / revise kinds', () => {
    for (const kind of ['approve', 'reject', 'revise'] as const) {
      const { token, payload } = issueApprovalToken(SECRET, kind, REQUEST_ID);
      const verified = verifyApprovalToken(SECRET, token);
      expect(verified.kind).toBe(kind);
      expect(verified.requestId).toBe(REQUEST_ID);
      expect(verified.v).toBe(1);
      expect(verified.exp).toBe(payload.exp);
    }
  });

  it('rejects a tampered payload (signature mismatch)', () => {
    const { token } = issueApprovalToken(SECRET, 'approve', REQUEST_ID);
    const [head, sig] = token.split('.');
    expect(head).toBeDefined();
    expect(sig).toBeDefined();
    // Flip a single character in the head — signature must no longer match.
    const tampered =
      (head as string).slice(0, -1) +
      ((head as string).slice(-1) === 'A' ? 'B' : 'A') +
      '.' +
      sig;
    expect(() => verifyApprovalToken(SECRET, tampered)).toThrow(ApprovalTokenError);
  });

  it('rejects a token signed with a different secret', () => {
    const { token } = issueApprovalToken(SECRET, 'approve', REQUEST_ID);
    expect(() => verifyApprovalToken('a-totally-different-secret-1234', token)).toThrow(
      ApprovalTokenError,
    );
  });

  it('rejects an expired token', () => {
    const longAgo = new Date(Date.now() - 72 * 60 * 60 * 1000 - 60_000); // 72h+1m ago
    const { token } = issueApprovalToken(SECRET, 'approve', REQUEST_ID, longAgo);
    try {
      verifyApprovalToken(SECRET, token);
      throw new Error('should have thrown');
    } catch (e) {
      expect(e).toBeInstanceOf(ApprovalTokenError);
      expect((e as ApprovalTokenError).code).toBe('expired');
    }
  });

  it('rejects malformed tokens', () => {
    expect(() => verifyApprovalToken(SECRET, 'no-dot-here')).toThrow(ApprovalTokenError);
    expect(() => verifyApprovalToken(SECRET, '.')).toThrow(ApprovalTokenError);
    expect(() => verifyApprovalToken(SECRET, 'abc.')).toThrow(ApprovalTokenError);
  });

  it('rejects an unsupported token version', () => {
    // Hand-craft a v=2 payload, sign it correctly — verify should still reject
    // because the version is unknown to this code path.
    const v2payload = Buffer.from(
      JSON.stringify({ v: 2, kind: 'approve', requestId: REQUEST_ID, exp: 9999999999 }),
      'utf8',
    )
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
    // Re-use issue's signing path: forge by signing v2payload under SECRET via
    // the same algorithm. Tests assert that the verifier rejects on version
    // even when the signature is valid.
    const sig = createHmac('sha256', SECRET).update(v2payload).digest();
    const sigB64 = sig
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
    const token = `${v2payload}.${sigB64}`;
    try {
      verifyApprovalToken(SECRET, token);
      throw new Error('should have thrown');
    } catch (e) {
      expect(e).toBeInstanceOf(ApprovalTokenError);
      expect((e as ApprovalTokenError).code).toBe('wrong_version');
    }
  });

  it('does not embed any personal data in the token', () => {
    const { token } = issueApprovalToken(SECRET, 'approve', REQUEST_ID);
    const head = token.split('.')[0] as string;
    const decoded = Buffer.from(
      head.replace(/-/g, '+').replace(/_/g, '/'),
      'base64',
    ).toString('utf8');
    // Sanity: the payload should not contain any obviously-personal fields.
    expect(decoded).not.toMatch(/email|phone|name/i);
  });
});
