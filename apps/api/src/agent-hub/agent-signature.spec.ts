import { describe, expect, it } from 'vitest';
import { generateKeyPairSync, sign as nodeSign } from 'node:crypto';
import {
  canonicalBytes,
  hexToBuffer,
  verifyAgentMessage,
  verifyEd25519,
} from './agent-signature';

function genEd25519() {
  const { publicKey, privateKey } = generateKeyPairSync('ed25519');
  // Extract the raw 32-byte public key from SPKI DER
  const der = publicKey.export({ format: 'der', type: 'spki' });
  // SPKI ed25519 prefix is 12 bytes
  const rawPub = Buffer.from(der.subarray(12)).toString('hex');
  return { rawPub, privateKey };
}

describe('hexToBuffer', () => {
  it('returns null on length mismatch', () => {
    expect(hexToBuffer('abcd', 32)).toBeNull();
  });
  it('returns null on non-hex characters', () => {
    expect(hexToBuffer('z'.repeat(64), 32)).toBeNull();
  });
  it('parses valid 32-byte hex', () => {
    const buf = hexToBuffer('a'.repeat(64), 32);
    expect(buf?.length).toBe(32);
  });
});

describe('canonicalBytes', () => {
  it('joins fields with pipes in order', () => {
    expect(canonicalBytes('r', 'ko', '안녕').toString('utf8')).toBe('r|ko|안녕');
  });
});

describe('verifyEd25519', () => {
  it('verifies a real signature produced by Node crypto', () => {
    const { rawPub, privateKey } = genEd25519();
    const msg = canonicalBytes('room-1', 'en', 'hello');
    const sig = nodeSign(null, msg, privateKey).toString('hex');
    expect(verifyEd25519(rawPub, sig, msg)).toBe(true);
  });

  it('rejects when the message is tampered', () => {
    const { rawPub, privateKey } = genEd25519();
    const msg = canonicalBytes('room-1', 'en', 'hello');
    const sig = nodeSign(null, msg, privateKey).toString('hex');
    const tampered = canonicalBytes('room-1', 'en', 'goodbye');
    expect(verifyEd25519(rawPub, sig, tampered)).toBe(false);
  });

  it('rejects malformed public key', () => {
    expect(verifyEd25519('zz', 'a'.repeat(128), Buffer.from('x'))).toBe(false);
  });

  it('rejects malformed signature', () => {
    const { rawPub } = genEd25519();
    expect(verifyEd25519(rawPub, 'short', Buffer.from('x'))).toBe(false);
  });
});

describe('verifyAgentMessage', () => {
  it('end-to-end happy path', () => {
    const { rawPub, privateKey } = genEd25519();
    const text = '오늘의 발견을 공유합니다';
    const roomId = 'room-id-1';
    const locale = 'ko';
    const sig = nodeSign(null, canonicalBytes(roomId, locale, text), privateKey).toString('hex');
    expect(
      verifyAgentMessage({
        publicKeyHex: rawPub,
        signatureHex: sig,
        roomId,
        locale,
        text,
      }),
    ).toBe(true);
  });

  it('rejects sig from a different key', () => {
    const a = genEd25519();
    const b = genEd25519();
    const text = 'msg';
    const sigA = nodeSign(null, canonicalBytes('r', 'en', text), a.privateKey).toString('hex');
    expect(
      verifyAgentMessage({
        publicKeyHex: b.rawPub,
        signatureHex: sigA,
        roomId: 'r',
        locale: 'en',
        text,
      }),
    ).toBe(false);
  });
});
