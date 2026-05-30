import { describe, expect, it } from 'vitest';
import { ALL_PLATFORMS, specFor, validateForPlatform } from './platforms';

describe('platforms', () => {
  it('lists all 8 supported platforms', () => {
    expect(ALL_PLATFORMS).toHaveLength(8);
    expect(ALL_PLATFORMS).toContain('youtube_shorts');
    expect(ALL_PLATFORMS).toContain('tiktok');
    expect(ALL_PLATFORMS).toContain('kakao_clip');
    expect(ALL_PLATFORMS).toContain('weibo_video');
  });

  it('youtube_shorts caption is short (≤100)', () => {
    expect(specFor('youtube_shorts').maxCaptionChars).toBe(100);
  });

  it('linkedin_video allows longest video (≥10 minutes)', () => {
    expect(specFor('linkedin_video').maxDurationSec).toBeGreaterThanOrEqual(600);
  });

  it('returns no violations for a 9:16 60-sec 80-char post on youtube_shorts', () => {
    const v = validateForPlatform('youtube_shorts', 'a'.repeat(80), 60, '9:16');
    expect(v).toEqual([]);
  });

  it('flags an over-length caption', () => {
    const v = validateForPlatform('x_video', 'a'.repeat(500), 30, '16:9');
    expect(v.some((m) => m.includes('Caption'))).toBe(true);
  });

  it('flags an over-length video', () => {
    const v = validateForPlatform('youtube_shorts', 'short caption', 120, '9:16');
    expect(v.some((m) => m.includes('caps at 60s'))).toBe(true);
  });

  it('flags wrong aspect ratio', () => {
    const v = validateForPlatform('instagram_reels', 'short', 30, '16:9');
    expect(v.some((m) => m.includes('Aspect'))).toBe(true);
  });
});
