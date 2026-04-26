// Privacy floor for impact-verification observations (ADR-0017 §C.2).
//
// The principle:
//   No external release contains a cohort smaller than the study's floor.
//   Default floor = 10 (the DB CHECK enforces a minimum of 10).
//   Sensitive studies bump the floor to 25 — handled at study creation time.
//
// This module is pure. The DB CHECK enforces structural validity at the
// storage layer (cohort_size >= 1, release_ready XOR suppressed). We enforce
// the *publish-time* floor here.

export interface KAnonymityCheck {
  /** Number of observations that pass the floor. */
  ok: number;
  /** Number that fall below and must be suppressed. */
  suppressed: number;
  /** True if the study is safe to release as-is (every observation passes). */
  cleanRelease: boolean;
  /** Human-readable detail per observation. */
  details: Array<{ id: string; cohortSize: number; passed: boolean }>;
}

export interface ObservationLike {
  id: string;
  cohortSize: number;
}

export function evaluateKAnonymity(
  observations: readonly ObservationLike[],
  floor: number,
): KAnonymityCheck {
  if (!Number.isInteger(floor) || floor < 10) {
    throw new Error(
      `K-anonymity floor must be an integer ≥ 10. Received ${floor}. ` +
        `Refusing to evaluate — this would be a privacy regression.`,
    );
  }
  let ok = 0;
  let suppressed = 0;
  const details = observations.map((o) => {
    const passed = o.cohortSize >= floor;
    if (passed) ok += 1;
    else suppressed += 1;
    return { id: o.id, cohortSize: o.cohortSize, passed };
  });
  return { ok, suppressed, cleanRelease: suppressed === 0 && ok > 0, details };
}

/**
 * Returns the floor to use for a study. Sensitive topics push to 25.
 * This is the *single* source of truth for floor computation; both the
 * service layer (study creation) and the publish-time gate consult it.
 */
export function floorFor(sensitiveTopic: boolean): number {
  return sensitiveTopic ? 25 : 10;
}
