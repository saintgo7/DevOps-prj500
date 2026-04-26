import { describe, expect, it } from 'vitest';
import { AGE_TIERS, checkSafety, estimateGrade, tierProfile, type AgeTier } from './age-tier';

describe('age-tier', () => {
  it('lists exactly four tiers in stable order', () => {
    expect(AGE_TIERS).toEqual(['children', 'teen', 'adult', 'senior']);
  });

  it('has stricter sentence limit for children than for adult', () => {
    expect(tierProfile('children').maxSentenceWords).toBeLessThan(tierProfile('adult').maxSentenceWords);
  });

  it('senior pace is slower than adult pace', () => {
    expect(tierProfile('senior').paceMultiplier).toBeGreaterThan(tierProfile('adult').paceMultiplier);
  });

  describe('checkSafety — children tier', () => {
    const tier: AgeTier = 'children';
    it('blocks english violence words', () => {
      const r = checkSafety('A sad story about war and weapons.', tier);
      expect(r.ok).toBe(false);
      expect(r.results.find((x) => x.rule === 'forbidden-pattern')?.ok).toBe(false);
    });

    it('blocks korean violence words', () => {
      expect(checkSafety('이 이야기는 죽음에 관한 것입니다.', tier).ok).toBe(false);
    });

    it('blocks spanish violence words', () => {
      expect(checkSafety('La historia trata sobre la guerra.', tier).ok).toBe(false);
    });

    it('blocks french violence words', () => {
      expect(checkSafety('L\'histoire parle de la guerre.', tier).ok).toBe(false);
    });

    it('blocks chinese violence words', () => {
      expect(checkSafety('这是关于战争的故事。', tier).ok).toBe(false);
    });

    it('blocks japanese violence words', () => {
      expect(checkSafety('これは戦争についての物語です。', tier).ok).toBe(false);
    });

    it('blocks PII patterns (SSN-like)', () => {
      expect(checkSafety('Call 123-45-6789 today.', tier).ok).toBe(false);
    });

    it('passes a wholesome short caption', () => {
      const r = checkSafety('Plant one tree. Water it. Watch it grow.', tier);
      expect(r.ok).toBe(true);
    });
  });

  describe('checkSafety — adult tier', () => {
    it('does not block words that the children tier blocks (e.g. war in history context)', () => {
      const r = checkSafety('The 2014 conflict caused a humanitarian crisis.', 'adult');
      expect(r.ok).toBe(true);
    });
  });

  describe('checkSafety — sentence length', () => {
    it('rejects a children-tier sentence longer than 12 words', () => {
      const long = 'one two three four five six seven eight nine ten eleven twelve thirteen.';
      const r = checkSafety(long, 'children');
      expect(r.results.find((x) => x.rule === 'sentence-length')?.ok).toBe(false);
    });

    it('accepts the same sentence at the adult tier (cap is 25)', () => {
      const ok = 'one two three four five six seven eight nine ten eleven twelve thirteen.';
      expect(checkSafety(ok, 'adult').results.find((x) => x.rule === 'sentence-length')?.ok).toBe(true);
    });
  });

  describe('checkSafety — overall length', () => {
    it('rejects a 60-second-of-words script for the senior tier (slower pace pushes it over the cap)', () => {
      // 150 words at children pace 1.2 = 180 (under 200). At senior 1.5 = 225 (over 200).
      const words = Array.from({ length: 150 }, () => 'word').join(' ');
      const text = words + '.';
      expect(checkSafety(text, 'senior').results.find((x) => x.rule === 'overall-length')?.ok).toBe(false);
    });

    it('accepts the same script at the adult tier', () => {
      const words = Array.from({ length: 150 }, () => 'word').join(' ');
      const text = words + '.';
      expect(checkSafety(text, 'adult').results.find((x) => x.rule === 'overall-length')?.ok).toBe(true);
    });
  });

  describe('estimateGrade', () => {
    it('returns a number for short English text', () => {
      const g = estimateGrade('The quick brown fox jumps over the lazy dog.');
      expect(typeof g).toBe('number');
    });
    it('returns 0 for empty text', () => {
      expect(estimateGrade('')).toBe(0);
    });
  });
});
