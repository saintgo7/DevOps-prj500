import { describe, expect, it } from 'vitest';
import { maskPii, PII_MASK } from './pii-mask';

describe('maskPii', () => {
  it('returns a clone when piiFields is empty', () => {
    const input = { name: 'A', age: 1 };
    const out = maskPii(input, []);
    expect(out).toEqual(input);
    expect(out).not.toBe(input);
  });

  it('masks a top-level field', () => {
    const out = maskPii({ name: 'Alice', age: 30 }, ['name']) as Record<string, unknown>;
    expect(out.name).toBe(PII_MASK);
    expect(out.age).toBe(30);
  });

  it('masks a nested field via dot path', () => {
    const out = maskPii(
      { user: { contact: { email: 'a@example.com' }, age: 30 } },
      ['user.contact.email'],
    ) as { user: { contact: { email: string }; age: number } };
    expect(out.user.contact.email).toBe(PII_MASK);
    expect(out.user.age).toBe(30);
  });

  it('ignores paths that do not exist', () => {
    const input = { name: 'A' };
    const out = maskPii(input, ['user.contact.email']);
    expect(out).toEqual(input);
  });

  it('does not mutate the original payload', () => {
    const input = { name: 'Alice', email: 'a@example.com' };
    maskPii(input, ['name', 'email']);
    expect(input.name).toBe('Alice');
    expect(input.email).toBe('a@example.com');
  });

  it('partially reveals strings when showPrefix is set', () => {
    const out = maskPii({ email: 'alice@example.com' }, ['email'], { showPrefix: 3 }) as {
      email: string;
    };
    expect(out.email.startsWith('ali')).toBe(true);
    expect(out.email.endsWith('***')).toBe(true);
  });

  it('masks arrays as a list of mask tokens', () => {
    const out = maskPii({ phones: ['+1', '+2', '+3'] }, ['phones']) as { phones: string[] };
    expect(out.phones).toEqual([PII_MASK, PII_MASK, PII_MASK]);
  });

  it('masks objects entirely', () => {
    const out = maskPii({ contact: { email: 'a@b', phone: '+1' } }, ['contact']) as {
      contact: unknown;
    };
    expect(out.contact).toBe(PII_MASK);
  });

  it('handles non-object payloads as no-op', () => {
    expect(maskPii('hello', ['anything'])).toBe('hello');
    expect(maskPii(42, ['anything'])).toBe(42);
    expect(maskPii(null, ['anything'])).toBe(null);
  });
});
