// Ed25519 signature verification for agent-emitted messages (ADR-0021 §A).
//
// Each AgentRegistration declares a 32-byte Ed25519 public key (stored as
// hex). Every agent-sent AgentMessage must carry a hex-encoded Ed25519
// signature over the canonical `(roomId|originalLocale|originalText)`
// triple. We verify with Node's built-in webcrypto so no extra deps are
// pulled in.

import { createPublicKey, verify as nodeVerify } from 'node:crypto';

/** Build the canonical bytes that the agent should have signed. */
export function canonicalBytes(roomId: string, locale: string, text: string): Buffer {
  return Buffer.from(`${roomId}|${locale}|${text}`, 'utf8');
}

/** Hex → Buffer with strict format validation. */
export function hexToBuffer(hex: string, expectedLen: number): Buffer | null {
  if (hex.length !== expectedLen * 2) return null;
  if (!/^[0-9a-f]+$/i.test(hex)) return null;
  return Buffer.from(hex, 'hex');
}

/**
 * Verify an Ed25519 signature.
 *   publicKeyHex — 32-byte hex (raw key)
 *   signatureHex — 64-byte hex
 *   message      — bytes that were signed
 * Returns false on any malformed input or verification failure.
 */
export function verifyEd25519(
  publicKeyHex: string,
  signatureHex: string,
  message: Buffer,
): boolean {
  const pk = hexToBuffer(publicKeyHex, 32);
  const sig = hexToBuffer(signatureHex, 64);
  if (!pk || !sig) return false;

  // Wrap the raw 32-byte public key in DER so KeyObject can import it.
  // Ed25519 SPKI prefix: 30 2A 30 05 06 03 2B 65 70 03 21 00
  const SPKI_PREFIX = Buffer.from('302a300506032b6570032100', 'hex');
  const der = Buffer.concat([SPKI_PREFIX, pk]);
  let keyObject;
  try {
    keyObject = createPublicKey({ key: der, format: 'der', type: 'spki' });
  } catch {
    return false;
  }
  try {
    return nodeVerify(null, message, keyObject, sig);
  } catch {
    return false;
  }
}

export interface VerifyMessageInput {
  publicKeyHex: string;
  signatureHex: string;
  roomId: string;
  locale: string;
  text: string;
}

/** Convenience wrapper for verifying an agent message in one call. */
export function verifyAgentMessage(input: VerifyMessageInput): boolean {
  return verifyEd25519(
    input.publicKeyHex,
    input.signatureHex,
    canonicalBytes(input.roomId, input.locale, input.text),
  );
}
