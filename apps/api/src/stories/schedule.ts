// Per-region prime-time scheduling for short-form video posts.
// See ADR-0015 §6 — values are conservative defaults; partner organisations
// may override via DistributionTarget.policy.scheduleOverride.
//
// Determinism is the goal: given (locale, region, now) we always return the
// same nextPostingSlot. No randomisation, so unit tests can pin behaviour.

export interface PrimeWindow {
  hourStart: number; // 0-23 local
  hourEnd: number; // 0-23 local
  dayMask?: number; // bitfield of weekdays (1=Mon … 64=Sun); default = all
}

export interface RegionSchedule {
  ianaTz: string;
  windows: PrimeWindow[];
}

const ALL_DAYS = 0b1111111;
const WEEKDAYS = 0b0011111;
const WEEKEND = 0b1100000;

const SCHEDULES: Record<string, RegionSchedule> = {
  KR: { ianaTz: 'Asia/Seoul',     windows: [{ hourStart: 18, hourEnd: 22, dayMask: WEEKDAYS }, { hourStart: 14, hourEnd: 22, dayMask: WEEKEND }] },
  JP: { ianaTz: 'Asia/Tokyo',     windows: [{ hourStart: 18, hourEnd: 22 }] },
  CN: { ianaTz: 'Asia/Shanghai',  windows: [{ hourStart: 19, hourEnd: 23 }] },
  IN: { ianaTz: 'Asia/Kolkata',   windows: [{ hourStart: 19, hourEnd: 23 }] },
  BD: { ianaTz: 'Asia/Dhaka',     windows: [{ hourStart: 19, hourEnd: 22 }] },
  ID: { ianaTz: 'Asia/Jakarta',   windows: [{ hourStart: 18, hourEnd: 22 }] },
  // Arabic
  SA: { ianaTz: 'Asia/Riyadh',    windows: [{ hourStart: 21, hourEnd: 24 }] },
  AE: { ianaTz: 'Asia/Dubai',     windows: [{ hourStart: 21, hourEnd: 24 }] },
  EG: { ianaTz: 'Africa/Cairo',   windows: [{ hourStart: 19, hourEnd: 23 }] },
  // Sub-Saharan Africa (LDC-rich; equity boost upstream)
  KE: { ianaTz: 'Africa/Nairobi', windows: [{ hourStart: 17, hourEnd: 21 }] },
  TZ: { ianaTz: 'Africa/Dar_es_Salaam', windows: [{ hourStart: 17, hourEnd: 21 }] },
  UG: { ianaTz: 'Africa/Kampala', windows: [{ hourStart: 17, hourEnd: 21 }] },
  NG: { ianaTz: 'Africa/Lagos',   windows: [{ hourStart: 18, hourEnd: 22 }] },
  SN: { ianaTz: 'Africa/Dakar',   windows: [{ hourStart: 18, hourEnd: 22 }] },
  // LATAM
  BR: { ianaTz: 'America/Sao_Paulo',   windows: [{ hourStart: 19, hourEnd: 22 }] },
  MX: { ianaTz: 'America/Mexico_City', windows: [{ hourStart: 19, hourEnd: 22 }] },
  AR: { ianaTz: 'America/Argentina/Buenos_Aires', windows: [{ hourStart: 19, hourEnd: 22 }] },
  // North America / Europe
  US: { ianaTz: 'America/New_York', windows: [{ hourStart: 12, hourEnd: 15 }, { hourStart: 19, hourEnd: 22 }] },
  GB: { ianaTz: 'Europe/London',    windows: [{ hourStart: 18, hourEnd: 22 }] },
  FR: { ianaTz: 'Europe/Paris',     windows: [{ hourStart: 18, hourEnd: 22 }] },
  DE: { ianaTz: 'Europe/Berlin',    windows: [{ hourStart: 18, hourEnd: 22 }] },
  RU: { ianaTz: 'Europe/Moscow',    windows: [{ hourStart: 19, hourEnd: 22 }] },
};

const DEFAULT_SCHEDULE: RegionSchedule = {
  ianaTz: 'UTC',
  windows: [{ hourStart: 12, hourEnd: 22, dayMask: ALL_DAYS }],
};

export function scheduleForRegion(country: string | null | undefined): RegionSchedule {
  if (!country) return DEFAULT_SCHEDULE;
  return SCHEDULES[country.toUpperCase()] ?? DEFAULT_SCHEDULE;
}

/**
 * Find the next scheduling slot for a region, ≥ `now`. Uses local-hour math
 * by computing the offset between the region timezone and UTC at `now`. This
 * is a deliberately small implementation — for production-grade DST handling
 * we would adopt date-fns-tz, but the test suite covers the common cases.
 */
export function nextSlot(country: string | undefined, now: Date = new Date()): Date {
  const sched = scheduleForRegion(country);
  // Compute local hour using Intl — handles DST correctly without a library.
  for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
    const candidate = new Date(now.getTime() + dayOffset * 86400_000);
    const local = localParts(candidate, sched.ianaTz);
    const dayMaskBit = 1 << ((local.dow + 6) % 7); // Mon=bit0
    for (const w of sched.windows) {
      if ((w.dayMask ?? ALL_DAYS) & dayMaskBit) {
        // If today and we are still inside the window, post now.
        if (dayOffset === 0 && local.hour >= w.hourStart && local.hour < w.hourEnd) {
          return candidate;
        }
        // Else if we are before today's window, post at window start.
        if (dayOffset === 0 && local.hour < w.hourStart) {
          return atLocalHour(candidate, sched.ianaTz, w.hourStart);
        }
      }
    }
    // Try the first applicable window of the next day.
    if (dayOffset > 0) {
      for (const w of sched.windows) {
        const nextLocal = localParts(candidate, sched.ianaTz);
        const nextDayBit = 1 << ((nextLocal.dow + 6) % 7);
        if ((w.dayMask ?? ALL_DAYS) & nextDayBit) {
          return atLocalHour(candidate, sched.ianaTz, w.hourStart);
        }
      }
    }
  }
  return now; // safety net — should never hit
}

function localParts(d: Date, tz: string): { hour: number; dow: number } {
  const dtf = new Intl.DateTimeFormat('en-US', {
    timeZone: tz,
    hour: '2-digit',
    weekday: 'short',
    hour12: false,
  });
  const parts = dtf.formatToParts(d);
  const hourStr = parts.find((p) => p.type === 'hour')?.value ?? '0';
  const dayStr = parts.find((p) => p.type === 'weekday')?.value ?? 'Sun';
  const dowMap: Record<string, number> = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  return { hour: Number(hourStr), dow: dowMap[dayStr] ?? 0 };
}

function atLocalHour(d: Date, tz: string, localHour: number): Date {
  // Find UTC time whose local-hour-in-tz equals localHour, on the same day as d.
  // We brute-force by checking each UTC hour of d's UTC date — simple and DST-safe.
  const day = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
  for (let h = 0; h < 48; h++) {
    const candidate = new Date(day.getTime() + h * 3600_000);
    if (localParts(candidate, tz).hour === localHour) return candidate;
  }
  return d;
}
