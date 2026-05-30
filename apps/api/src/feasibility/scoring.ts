// Deterministic 6-axis feasibility scoring (ADR-0019 §B).
//
// Each axis is 0..100. The aggregate is a weighted average. Pass requires
// every axis ≥ 40; ODA / policy tracks additionally require human review
// (handled at the service layer — this module is pure).
//
// The deterministic guards encode editorial standards we never want to
// silently relax. If you change a guard you must add a test for it AND
// document the change in the next ADR.

export type FeasibilityAxis =
  | 'impact'
  | 'financial'
  | 'technical'
  | 'legal'
  | 'ethical'
  | 'evidence';

export interface PlanInputs {
  /** Hard rule: must be true for legal axis to score above zero. */
  noncommercialNotice: boolean;
  /** SDG focus tags on the plan. */
  sdgFocus: readonly string[];
  /** ISO-3166 region tags; LDC codes get an impact bonus. */
  applicableRegions: readonly string[];
  /** Months of project duration. */
  periodMonths: number;
  /** Sum of all section budgets, in currency minor units. */
  budgetTotalMinor: number;
  /** Sum of milestone amounts, in currency minor units. */
  milestoneSumMinor: number;
  /** Technology readiness level (1..9) of the central solution. */
  trl: number;
  /** True if the harmful-content guard rejected any section text. */
  harmfulContentBlocked: boolean;
  /** SDG codes present in cited sources — used to detect cited-too-narrowly. */
  citedSourceSdgs: readonly string[];
  /** Citation source kinds — used for evidence diversity. */
  citationSourceKinds: ReadonlyArray<
    'watch' | 'column' | 'patent' | 'manuscript' | 'doi' | 'url'
  >;
  /** Total number of citations (across all sections). */
  citationCount: number;
  /** Estimated beneficiaries reached. */
  estimatedBeneficiaries: number;
}

export interface AxisRationale {
  rules: string[];
  passed: boolean;
}

export interface AxisResult {
  axis: FeasibilityAxis;
  score: number;
  rationale: AxisRationale;
}

export interface FeasibilityResult {
  axes: AxisResult[];
  /** Weighted aggregate (0..100). */
  feasibilityScore: number;
  /** 'pass' if every axis ≥ 40, otherwise 'fail'. */
  outcome: 'pass' | 'fail';
}

const AXIS_WEIGHTS: Record<FeasibilityAxis, number> = {
  impact: 0.25,
  financial: 0.2,
  technical: 0.15,
  legal: 0.15,
  ethical: 0.15,
  evidence: 0.1,
};

const PASS_FLOOR = 40;

// Stable sample list — keep small. Real ETL replaces this in ADR-0009 follow-up.
export const LDC_REGIONS = new Set([
  'AF', 'AO', 'BD', 'BF', 'BI', 'BJ', 'BT', 'CD', 'CF', 'CG',
  'DJ', 'ER', 'ET', 'GM', 'GN', 'GW', 'HT', 'KH', 'KI', 'KM',
  'LA', 'LR', 'LS', 'MG', 'ML', 'MM', 'MR', 'MW', 'MZ', 'NE',
  'NP', 'RW', 'SB', 'SD', 'SL', 'SO', 'SS', 'ST', 'TD', 'TG',
  'TL', 'TV', 'TZ', 'UG', 'YE', 'ZM',
]);

function clamp(n: number): number {
  return Math.max(0, Math.min(100, Math.round(n)));
}

function impactAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  let score = 0;
  // Beneficiaries: log-scaled. 100 → 30; 1k → 50; 10k → 70; 100k → 90.
  if (p.estimatedBeneficiaries > 0) {
    score += Math.min(60, 10 * Math.log10(Math.max(10, p.estimatedBeneficiaries)));
    rules.push(
      `Beneficiaries ${p.estimatedBeneficiaries} → +${Math.min(60, 10 * Math.log10(Math.max(10, p.estimatedBeneficiaries))).toFixed(0)}`,
    );
  } else {
    rules.push('No beneficiaries declared → 0 base.');
  }
  // Duration sustainability: 18m+ adds 10.
  if (p.periodMonths >= 18) {
    score += 10;
    rules.push(`Duration ${p.periodMonths}m ≥ 18m → +10`);
  }
  // LDC overlap: any LDC region adds 15.
  const ldcMatch = p.applicableRegions.some((r) => LDC_REGIONS.has(r));
  if (ldcMatch) {
    score += 15;
    rules.push('LDC region present → +15');
  }
  // SDG focus: at least 1, missing → cap at 30.
  if (p.sdgFocus.length === 0) {
    score = Math.min(score, 30);
    rules.push('No SDG focus → cap 30');
  } else if (p.sdgFocus.length >= 2) {
    score += 5;
    rules.push('Multi-SDG focus → +5');
  }
  return {
    axis: 'impact',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

function financialAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  let score = 60; // baseline assumes a coherent plan
  if (p.budgetTotalMinor <= 0) {
    rules.push('Budget total ≤ 0 → cap 0');
    return { axis: 'financial', score: 0, rationale: { rules, passed: false } };
  }
  let cap = 100;
  if (p.milestoneSumMinor !== p.budgetTotalMinor) {
    cap = Math.min(cap, 30);
    rules.push(
      `Budget (${p.budgetTotalMinor}) ≠ milestone sum (${p.milestoneSumMinor}) → cap 30`,
    );
  } else {
    rules.push('Budget = milestone sum');
    score += 10;
  }
  if (p.estimatedBeneficiaries > 0) {
    const perPerson = p.budgetTotalMinor / p.estimatedBeneficiaries;
    if (perPerson < 100) {
      cap = Math.min(cap, 40);
      rules.push(`Budget/beneficiary < 100 minor units → cap 40 (likely under-funded)`);
    } else if (perPerson > 10_000_000) {
      cap = Math.min(cap, 40);
      rules.push(`Budget/beneficiary > 10M minor units → cap 40 (likely over-budgeted)`);
    } else {
      rules.push(`Budget/beneficiary ${Math.round(perPerson)} minor units → in range`);
      score += 5;
    }
  }
  // Apply caps last so additive bonuses cannot defeat a structural cap.
  score = Math.min(score, cap);
  return {
    axis: 'financial',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

function technicalAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  let score = 50;
  if (p.trl <= 0 || p.trl > 9) {
    rules.push(`TRL ${p.trl} out of range (1..9) → cap 30`);
    score = Math.min(score, 30);
  } else {
    rules.push(`TRL ${p.trl}`);
    score = 30 + p.trl * 5; // TRL 1 → 35, TRL 9 → 75
  }
  if (p.trl <= 2 && p.periodMonths <= 18) {
    score = Math.min(score, 40);
    rules.push('TRL ≤ 2 with ≤ 18m timeline → cap 40 (deployment risk)');
  }
  return {
    axis: 'technical',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

function legalAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  if (!p.noncommercialNotice) {
    rules.push('Non-commercial notice missing → 0');
    return { axis: 'legal', score: 0, rationale: { rules, passed: false } };
  }
  rules.push('Non-commercial notice present');
  let score = 70;
  if (p.applicableRegions.length === 0) {
    score = Math.min(score, 50);
    rules.push('No applicable regions declared → cap 50 (regulatory ambiguity)');
  } else {
    score += 5;
    rules.push(`Applicable regions: ${p.applicableRegions.join(', ')}`);
  }
  return {
    axis: 'legal',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

function ethicalAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  if (p.harmfulContentBlocked) {
    rules.push('Harmful-content guard blocked at least one section → 0');
    return { axis: 'ethical', score: 0, rationale: { rules, passed: false } };
  }
  rules.push('Harmful-content guard passed all sections');
  let score = 75;
  // Working in conflict-affected regions raises ethical caution; we don't
  // penalise but record the rule for transparency.
  const conflictRegions = ['YE', 'SD', 'SS', 'AF', 'SY'];
  const conflictHit = p.applicableRegions.some((r) => conflictRegions.includes(r));
  if (conflictHit) {
    rules.push('Conflict-affected region — extra caution recommended');
    score -= 5;
  }
  return {
    axis: 'ethical',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

function evidenceAxis(p: PlanInputs): AxisResult {
  const rules: string[] = [];
  if (p.citationCount === 0) {
    rules.push('No citations → 0');
    return { axis: 'evidence', score: 0, rationale: { rules, passed: false } };
  }
  let score = 30;
  rules.push(`${p.citationCount} citations → +30 base`);
  // Diversity: distinct source kinds.
  const kinds = new Set(p.citationSourceKinds);
  score += Math.min(30, kinds.size * 6);
  rules.push(`${kinds.size} distinct source kinds → +${Math.min(30, kinds.size * 6)}`);
  // Cross-SDG cited evidence: if every cited source is in the plan's sole SDG
  // we cap the score (avoid echo-chamber evidence).
  if (p.sdgFocus.length === 1) {
    const onlyOurSdg = p.citedSourceSdgs.every((s) => s === p.sdgFocus[0]);
    if (onlyOurSdg) {
      score = Math.min(score, 50);
      rules.push('All cited evidence in our single SDG → cap 50 (narrow view)');
    }
  }
  return {
    axis: 'evidence',
    score: clamp(score),
    rationale: { rules, passed: clamp(score) >= PASS_FLOOR },
  };
}

export function evaluateFeasibility(p: PlanInputs): FeasibilityResult {
  const axes: AxisResult[] = [
    impactAxis(p),
    financialAxis(p),
    technicalAxis(p),
    legalAxis(p),
    ethicalAxis(p),
    evidenceAxis(p),
  ];
  const aggregate = axes.reduce(
    (acc, a) => acc + a.score * AXIS_WEIGHTS[a.axis],
    0,
  );
  const allPass = axes.every((a) => a.rationale.passed);
  return {
    axes,
    feasibilityScore: clamp(aggregate),
    outcome: allPass ? 'pass' : 'fail',
  };
}
