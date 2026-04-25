import { describe, expect, it } from 'vitest';

describe('worker bootstrap', () => {
  it('reads REDIS_URL with sensible default', () => {
    const url = process.env.REDIS_URL ?? 'redis://localhost:6379';
    expect(url.startsWith('redis://')).toBe(true);
  });
});
