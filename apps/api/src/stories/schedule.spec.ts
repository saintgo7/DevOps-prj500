import { describe, expect, it } from 'vitest';
import { nextSlot, scheduleForRegion } from './schedule';

describe('schedule', () => {
  it('returns a per-region timezone for known countries', () => {
    expect(scheduleForRegion('KR').ianaTz).toBe('Asia/Seoul');
    expect(scheduleForRegion('KE').ianaTz).toBe('Africa/Nairobi');
    expect(scheduleForRegion('AR').ianaTz).toBe('America/Argentina/Buenos_Aires');
  });

  it('falls back to UTC for unknown countries', () => {
    expect(scheduleForRegion('XX').ianaTz).toBe('UTC');
    expect(scheduleForRegion(null).ianaTz).toBe('UTC');
    expect(scheduleForRegion(undefined).ianaTz).toBe('UTC');
  });

  it('returns a Date in the future or now', () => {
    const now = new Date('2026-04-26T03:00:00Z'); // pinned for determinism
    const slot = nextSlot('KR', now);
    expect(slot.getTime()).toBeGreaterThanOrEqual(now.getTime());
  });

  it('returns now when current time is inside a prime window (KR Mon 19:30 KST)', () => {
    // 19:30 KST = 10:30 UTC on the same day
    const inWindow = new Date('2026-04-27T10:30:00Z');
    const slot = nextSlot('KR', inWindow);
    expect(slot.getTime()).toBe(inWindow.getTime());
  });

  it('schedules at window start when current time is before window (KR Mon 09:00 KST)', () => {
    // 09:00 KST = 00:00 UTC; KR weekday window starts 18:00 KST = 09:00 UTC
    const before = new Date('2026-04-27T00:00:00Z');
    const slot = nextSlot('KR', before);
    // Local hour should be 18
    const local = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Seoul', hour: '2-digit', hour12: false }).format(slot);
    expect(Number(local)).toBe(18);
  });

  it('handles Ramadan-style late-evening Arabic window (SA 21-24)', () => {
    const slot = nextSlot('SA', new Date('2026-04-26T05:00:00Z'));
    const localHour = Number(
      new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Riyadh', hour: '2-digit', hour12: false }).format(slot),
    );
    expect(localHour).toBeGreaterThanOrEqual(21);
  });
});
