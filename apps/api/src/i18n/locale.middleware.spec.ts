import { describe, expect, it } from 'vitest';
import { pickLocale, DEFAULT_LOCALE } from './locale.middleware';

describe('pickLocale', () => {
  it('honours ?lang= query param', () => {
    expect(pickLocale('ja', 'en-US')).toBe('ja');
    expect(pickLocale('zh-CN', '')).toBe('zh');
  });

  it('falls back to Accept-Language q-weighted negotiation', () => {
    expect(pickLocale(undefined, 'ko-KR,en;q=0.7')).toBe('ko');
    expect(pickLocale(undefined, 'th;q=1, ja;q=0.9')).toBe('ja');
    expect(pickLocale(undefined, 'zh-Hans-CN, en;q=0.8')).toBe('zh');
  });

  it('ignores unknown languages and uses default', () => {
    expect(pickLocale(undefined, 'xx;q=1')).toBe(DEFAULT_LOCALE);
    expect(pickLocale('klingon', '')).toBe(DEFAULT_LOCALE);
  });

  it('treats higher q-value as preferred', () => {
    // Mixed with a non-supported high-q value, picks the next supported.
    expect(pickLocale(undefined, 'th;q=1, ko;q=0.4, ja;q=0.6')).toBe('ja');
  });

  it('respects equity: never silently downgrades to English when user prefers ko', () => {
    // Even if our default is 'en', user-preferred 'ko' wins.
    expect(pickLocale(undefined, 'ko')).toBe('ko');
  });

  it('honours LDC-priority languages (sw, fr, ar, pt, bn)', () => {
    expect(pickLocale(undefined, 'sw-KE')).toBe('sw');
    expect(pickLocale(undefined, 'ar-EG')).toBe('ar');
    expect(pickLocale(undefined, 'fr-SN')).toBe('fr');
    expect(pickLocale(undefined, 'pt-AO')).toBe('pt');
    expect(pickLocale(undefined, 'bn-BD')).toBe('bn');
  });

  it('handles top-10 global languages', () => {
    expect(pickLocale(undefined, 'hi-IN')).toBe('hi');
    expect(pickLocale(undefined, 'es-MX')).toBe('es');
    expect(pickLocale(undefined, 'ru-RU')).toBe('ru');
    expect(pickLocale(undefined, 'id-ID')).toBe('id');
  });
});
