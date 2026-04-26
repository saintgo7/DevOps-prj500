import { describe, expect, it } from 'vitest';
import { TONES, TONE_LIBRARY, closingFor, suggestTone } from './tones';

describe('tones', () => {
  it('lists the 5 canonical tones in stable order', () => {
    expect(TONES).toEqual(['playful', 'friend', 'solemn', 'instructive', 'reflective']);
  });

  it('every tone has a description and at least one closing', () => {
    for (const t of TONES) {
      const profile = TONE_LIBRARY[t];
      expect(profile.description.length).toBeGreaterThan(0);
      expect(Object.keys(profile.closingByLocale).length).toBeGreaterThanOrEqual(1);
    }
  });

  it('every tone has a Korean closing (operating market)', () => {
    for (const t of TONES) {
      expect(TONE_LIBRARY[t].closingByLocale.ko).toBeDefined();
    }
  });

  it('closingFor falls through to English for missing locale', () => {
    expect(closingFor('playful', 'bn' as never)).toBe(TONE_LIBRARY.playful.closingByLocale.en);
  });

  it('closingFor returns the locale value when present', () => {
    expect(closingFor('solemn', 'ko')).toBe(TONE_LIBRARY.solemn.closingByLocale.ko);
  });

  it('suggestTone routes children to playful and senior to reflective', () => {
    expect(suggestTone('children', 'standard')).toBe('playful');
    expect(suggestTone('senior', 'standard')).toBe('reflective');
  });

  it('suggestTone routes sensitive content to solemn regardless of tier', () => {
    expect(suggestTone('children', 'sensitive')).toBe('solemn');
    expect(suggestTone('teen', 'sensitive')).toBe('solemn');
    expect(suggestTone('adult', 'sensitive')).toBe('solemn');
    expect(suggestTone('senior', 'sensitive')).toBe('solemn');
  });

  it('every tone declares blocked registers', () => {
    for (const t of TONES) {
      expect(Array.isArray(TONE_LIBRARY[t].blockedRegisters)).toBe(true);
    }
  });
});
