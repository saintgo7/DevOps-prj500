import { describe, expect, it } from 'vitest';
import { validatePayload, type JsonSchema } from './schema-validate';

describe('validatePayload — type', () => {
  it('accepts a matching primitive', () => {
    expect(validatePayload('hello', { type: 'string' }).ok).toBe(true);
    expect(validatePayload(42, { type: 'number' }).ok).toBe(true);
    expect(validatePayload(42, { type: 'integer' }).ok).toBe(true);
    expect(validatePayload(true, { type: 'boolean' }).ok).toBe(true);
    expect(validatePayload(null, { type: 'null' }).ok).toBe(true);
  });

  it('rejects type mismatch', () => {
    const r = validatePayload(42, { type: 'string' });
    expect(r.ok).toBe(false);
    expect(r.errors[0]?.message).toMatch(/expected type 'string'/);
  });

  it('treats integers as a subset of number', () => {
    expect(validatePayload(7, { type: 'number' }).ok).toBe(true);
    expect(validatePayload(7.5, { type: 'integer' }).ok).toBe(false);
  });
});

describe('validatePayload — string constraints', () => {
  it('enforces minLength / maxLength', () => {
    const schema: JsonSchema = { type: 'string', minLength: 2, maxLength: 5 };
    expect(validatePayload('a', schema).ok).toBe(false);
    expect(validatePayload('abc', schema).ok).toBe(true);
    expect(validatePayload('toolong', schema).ok).toBe(false);
  });

  it('enforces a regex pattern', () => {
    const schema: JsonSchema = { type: 'string', pattern: '^[A-Z]{3}$' };
    expect(validatePayload('ABC', schema).ok).toBe(true);
    expect(validatePayload('abc', schema).ok).toBe(false);
  });
});

describe('validatePayload — number constraints', () => {
  it('enforces minimum / maximum', () => {
    const schema: JsonSchema = { type: 'integer', minimum: 1, maximum: 10 };
    expect(validatePayload(0, schema).ok).toBe(false);
    expect(validatePayload(5, schema).ok).toBe(true);
    expect(validatePayload(11, schema).ok).toBe(false);
  });
});

describe('validatePayload — enum', () => {
  it('accepts only listed values', () => {
    const schema: JsonSchema = { type: 'string', enum: ['low', 'medium', 'high'] };
    expect(validatePayload('low', schema).ok).toBe(true);
    expect(validatePayload('extreme', schema).ok).toBe(false);
  });
});

describe('validatePayload — object', () => {
  const schema: JsonSchema = {
    type: 'object',
    required: ['name'],
    properties: {
      name: { type: 'string', minLength: 1 },
      age: { type: 'integer', minimum: 0 },
    },
    additionalProperties: false,
  };

  it('accepts a well-formed object', () => {
    expect(validatePayload({ name: 'A', age: 1 }, schema).ok).toBe(true);
  });

  it('rejects missing required key', () => {
    const r = validatePayload({ age: 1 }, schema);
    expect(r.ok).toBe(false);
    expect(r.errors.some((e) => e.path === 'name')).toBe(true);
  });

  it('rejects unknown properties when additionalProperties is false', () => {
    const r = validatePayload({ name: 'A', extra: 'x' }, schema);
    expect(r.ok).toBe(false);
  });

  it('walks into known property schemas', () => {
    const r = validatePayload({ name: '', age: 1 }, schema);
    expect(r.ok).toBe(false);
    expect(r.errors.some((e) => e.path === 'name')).toBe(true);
  });
});

describe('validatePayload — array', () => {
  it('walks each item with the items schema', () => {
    const schema: JsonSchema = {
      type: 'array',
      items: { type: 'integer', minimum: 0 },
    };
    expect(validatePayload([1, 2, 3], schema).ok).toBe(true);
    const r = validatePayload([1, -1, 3], schema);
    expect(r.ok).toBe(false);
    expect(r.errors[0]?.path).toContain('[1]');
  });
});
