import { describe, expect, it } from 'vitest';
import { evaluateKAnonymity, floorFor } from './k-anonymity';

describe('floorFor', () => {
  it('returns 10 for ordinary studies', () => {
    expect(floorFor(false)).toBe(10);
  });
  it('returns 25 for sensitive studies', () => {
    expect(floorFor(true)).toBe(25);
  });
});

describe('evaluateKAnonymity', () => {
  it('throws when given a floor below 10', () => {
    expect(() => evaluateKAnonymity([{ id: 'a', cohortSize: 100 }], 5)).toThrow(/privacy regression/);
  });

  it('throws on a non-integer floor', () => {
    expect(() => evaluateKAnonymity([{ id: 'a', cohortSize: 100 }], 10.5)).toThrow(
      /privacy regression/,
    );
  });

  it('marks a clean release when every cohort meets the floor', () => {
    const r = evaluateKAnonymity(
      [
        { id: 'a', cohortSize: 12 },
        { id: 'b', cohortSize: 30 },
      ],
      10,
    );
    expect(r.ok).toBe(2);
    expect(r.suppressed).toBe(0);
    expect(r.cleanRelease).toBe(true);
  });

  it('marks small cohorts as suppressed and refuses clean release', () => {
    const r = evaluateKAnonymity(
      [
        { id: 'a', cohortSize: 5 },
        { id: 'b', cohortSize: 50 },
      ],
      10,
    );
    expect(r.suppressed).toBe(1);
    expect(r.cleanRelease).toBe(false);
    expect(r.details.find((d) => d.id === 'a')?.passed).toBe(false);
  });

  it('treats k=25 floor strictly for sensitive topics', () => {
    const r = evaluateKAnonymity(
      [
        { id: 'a', cohortSize: 12 }, // would pass at k=10 but not k=25
        { id: 'b', cohortSize: 30 },
      ],
      25,
    );
    expect(r.suppressed).toBe(1);
    expect(r.cleanRelease).toBe(false);
  });

  it('returns cleanRelease=false for an empty input', () => {
    const r = evaluateKAnonymity([], 10);
    expect(r.cleanRelease).toBe(false);
    expect(r.ok).toBe(0);
  });

  it('exactly meets the floor — passes', () => {
    const r = evaluateKAnonymity([{ id: 'a', cohortSize: 10 }], 10);
    expect(r.cleanRelease).toBe(true);
  });
});
