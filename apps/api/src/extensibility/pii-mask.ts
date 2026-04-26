// PII masking for custom-record payloads (ADR-0020 §B).
//
// CustomDomain.piiFields lists either a top-level key or a JSONPath-like
// expression ('user.contact.email') of fields that must be masked before
// any AI invocation or external disclosure.
//
// This module is pure — no Prisma, no IO. It only knows how to walk a
// payload and replace flagged fields with the platform's mask token.

export const PII_MASK = '[redacted]';

export interface MaskOptions {
  /** Leave the first N characters of strings visible (e.g. for emails). */
  showPrefix?: number;
}

function maskValue(value: unknown, opts: MaskOptions): unknown {
  if (typeof value === 'string') {
    const n = opts.showPrefix ?? 0;
    if (n > 0 && value.length > n) {
      return value.slice(0, n) + '***';
    }
    return PII_MASK;
  }
  if (Array.isArray(value)) {
    return value.map(() => PII_MASK);
  }
  if (typeof value === 'object' && value !== null) {
    return PII_MASK;
  }
  // numbers / booleans / null become the string mask token so a downstream
  // AI prompt can't infer the value type either.
  return PII_MASK;
}

function setByPath(
  target: Record<string, unknown>,
  path: string,
  apply: (existing: unknown) => unknown,
): void {
  const segments = path.split('.').filter(Boolean);
  if (segments.length === 0) return;
  let cursor: Record<string, unknown> = target;
  for (let i = 0; i < segments.length - 1; i += 1) {
    const seg = segments[i] as string;
    const next = cursor[seg];
    if (typeof next !== 'object' || next === null || Array.isArray(next)) return;
    cursor = next as Record<string, unknown>;
  }
  const last = segments[segments.length - 1] as string;
  if (Object.prototype.hasOwnProperty.call(cursor, last)) {
    cursor[last] = apply(cursor[last]);
  }
}

/**
 * Returns a deep copy of the payload with the listed fields masked.
 * Unknown paths are silently ignored (they describe future shapes).
 *
 * The original payload is NOT mutated.
 */
export function maskPii(
  payload: unknown,
  piiFields: readonly string[],
  opts: MaskOptions = {},
): unknown {
  if (!piiFields || piiFields.length === 0) return structuredClone(payload);
  if (typeof payload !== 'object' || payload === null) return structuredClone(payload);

  const copy = structuredClone(payload) as Record<string, unknown>;
  for (const field of piiFields) {
    setByPath(copy, field, (existing) => maskValue(existing, opts));
  }
  return copy;
}
