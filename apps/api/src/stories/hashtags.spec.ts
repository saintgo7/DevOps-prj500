import { describe, expect, it } from 'vitest';
import { composeHashtags, platformCap } from './hashtags';

describe('hashtags', () => {
  it('returns Korean tags for SDG-13 in ko', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-13'],
      locale: 'ko',
      platform: 'instagram_reels',
    });
    expect(tags).toContain('#기후행동');
    expect(tags).toContain('#SDG13');
  });

  it('falls back to English when a locale has no entries for a goal', () => {
    // Indonesian has no SDG-17 in our seed → English fallback expected.
    const tags = composeHashtags({
      goalIds: ['SDG-17'],
      locale: 'id',
      platform: 'tiktok',
    });
    expect(tags).toContain('#Partnerships');
  });

  it('appends LDC-boost tags when isLdcOrigin is true', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-13'],
      locale: 'sw',
      platform: 'instagram_reels',
      isLdcOrigin: true,
    });
    expect(tags.some((t) => t.includes('Local2030'))).toBe(true);
  });

  it('omits LDC-boost tags by default', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-13'],
      locale: 'en',
      platform: 'instagram_reels',
    });
    expect(tags.includes('#GlobalSouth')).toBe(false);
  });

  it('trims to the platform recommended count', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-13', 'SDG-17'],
      locale: 'en',
      platform: 'youtube_shorts', // cap 3
      isLdcOrigin: true,
    });
    expect(tags.length).toBeLessThanOrEqual(platformCap('youtube_shorts'));
  });

  it('de-duplicates tags across goals', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-3', 'SDG-3'],
      locale: 'en',
      platform: 'facebook_reels',
    });
    const unique = new Set(tags);
    expect(unique.size).toBe(tags.length);
  });

  it('handles unknown goals gracefully (returns empty array)', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-NOTHING'],
      locale: 'en',
      platform: 'tiktok',
    });
    expect(Array.isArray(tags)).toBe(true);
    expect(tags.length).toBe(0);
  });

  it('preserves insertion order of goals', () => {
    const tags = composeHashtags({
      goalIds: ['SDG-13', 'SDG-1'],
      locale: 'en',
      platform: 'facebook_reels',
    });
    expect(tags.indexOf('#ClimateAction')).toBeLessThan(tags.indexOf('#NoPoverty'));
  });
});
