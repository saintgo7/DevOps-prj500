import { describe, expect, it } from 'vitest';
import { evaluateFeasibility, type PlanInputs } from './scoring';

function base(overrides: Partial<PlanInputs> = {}): PlanInputs {
  return {
    noncommercialNotice: true,
    sdgFocus: ['SDG-6', 'SDG-3'],
    applicableRegions: ['BD'],
    periodMonths: 24,
    budgetTotalMinor: 1_000_000,
    milestoneSumMinor: 1_000_000,
    trl: 7,
    harmfulContentBlocked: false,
    citedSourceSdgs: ['SDG-6', 'SDG-13'],
    citationSourceKinds: ['watch', 'column', 'manuscript', 'doi'],
    citationCount: 12,
    estimatedBeneficiaries: 5_000,
    ...overrides,
  };
}

describe('evaluateFeasibility — happy path', () => {
  it('passes a well-formed plan and returns 6 axes', () => {
    const r = evaluateFeasibility(base());
    expect(r.outcome).toBe('pass');
    expect(r.axes).toHaveLength(6);
    expect(r.feasibilityScore).toBeGreaterThanOrEqual(60);
  });
});

describe('legal axis', () => {
  it('returns 0 when noncommercialNotice is false', () => {
    const r = evaluateFeasibility(base({ noncommercialNotice: false }));
    const legal = r.axes.find((a) => a.axis === 'legal')!;
    expect(legal.score).toBe(0);
    expect(r.outcome).toBe('fail');
  });

  it('caps at 50 when no applicable regions are declared', () => {
    const r = evaluateFeasibility(base({ applicableRegions: [] }));
    const legal = r.axes.find((a) => a.axis === 'legal')!;
    expect(legal.score).toBeLessThanOrEqual(50);
  });
});

describe('financial axis', () => {
  it('returns 0 when budget is non-positive', () => {
    const r = evaluateFeasibility(base({ budgetTotalMinor: 0, milestoneSumMinor: 0 }));
    const fin = r.axes.find((a) => a.axis === 'financial')!;
    expect(fin.score).toBe(0);
    expect(r.outcome).toBe('fail');
  });

  it('caps at 30 when budget total ≠ milestone sum', () => {
    const r = evaluateFeasibility(
      base({ budgetTotalMinor: 1_000_000, milestoneSumMinor: 800_000 }),
    );
    const fin = r.axes.find((a) => a.axis === 'financial')!;
    expect(fin.score).toBeLessThanOrEqual(30);
  });

  it('caps at 40 when budget per beneficiary is implausibly low', () => {
    const r = evaluateFeasibility(
      base({ budgetTotalMinor: 100, milestoneSumMinor: 100, estimatedBeneficiaries: 100 }),
    );
    const fin = r.axes.find((a) => a.axis === 'financial')!;
    expect(fin.score).toBeLessThanOrEqual(40);
  });
});

describe('ethical axis', () => {
  it('returns 0 when harmful-content guard fired', () => {
    const r = evaluateFeasibility(base({ harmfulContentBlocked: true }));
    const eth = r.axes.find((a) => a.axis === 'ethical')!;
    expect(eth.score).toBe(0);
    expect(r.outcome).toBe('fail');
  });
});

describe('evidence axis', () => {
  it('returns 0 with zero citations', () => {
    const r = evaluateFeasibility(base({ citationCount: 0, citationSourceKinds: [] }));
    const ev = r.axes.find((a) => a.axis === 'evidence')!;
    expect(ev.score).toBe(0);
    expect(r.outcome).toBe('fail');
  });

  it('caps at 50 when every cited evidence is in our single SDG', () => {
    const r = evaluateFeasibility(
      base({
        sdgFocus: ['SDG-6'],
        citedSourceSdgs: ['SDG-6', 'SDG-6', 'SDG-6'],
        citationCount: 3,
        citationSourceKinds: ['watch', 'column', 'manuscript'],
      }),
    );
    const ev = r.axes.find((a) => a.axis === 'evidence')!;
    expect(ev.score).toBeLessThanOrEqual(50);
  });

  it('rewards diversity of source kinds', () => {
    const narrow = evaluateFeasibility(
      base({ citationSourceKinds: ['watch'], citationCount: 12 }),
    );
    const wide = evaluateFeasibility(
      base({
        citationSourceKinds: ['watch', 'column', 'patent', 'manuscript', 'doi', 'url'],
        citationCount: 12,
      }),
    );
    expect(wide.axes.find((a) => a.axis === 'evidence')!.score).toBeGreaterThan(
      narrow.axes.find((a) => a.axis === 'evidence')!.score,
    );
  });
});

describe('technical axis', () => {
  it('caps at 40 when TRL ≤ 2 and timeline ≤ 18 months', () => {
    const r = evaluateFeasibility(base({ trl: 2, periodMonths: 12 }));
    const tech = r.axes.find((a) => a.axis === 'technical')!;
    expect(tech.score).toBeLessThanOrEqual(40);
  });

  it('penalises out-of-range TRL', () => {
    const r = evaluateFeasibility(base({ trl: 12 }));
    const tech = r.axes.find((a) => a.axis === 'technical')!;
    expect(tech.score).toBeLessThanOrEqual(30);
  });
});

describe('impact axis', () => {
  it('rewards LDC region overlap', () => {
    const ldc = evaluateFeasibility(base({ applicableRegions: ['BD'] }));
    const non = evaluateFeasibility(base({ applicableRegions: ['KR'] }));
    expect(ldc.axes.find((a) => a.axis === 'impact')!.score).toBeGreaterThan(
      non.axes.find((a) => a.axis === 'impact')!.score,
    );
  });

  it('caps at 30 when SDG focus is empty', () => {
    const r = evaluateFeasibility(base({ sdgFocus: [] }));
    const imp = r.axes.find((a) => a.axis === 'impact')!;
    expect(imp.score).toBeLessThanOrEqual(30);
  });

  it('rewards multi-SDG focus over single', () => {
    const single = evaluateFeasibility(base({ sdgFocus: ['SDG-6'] }));
    const multi = evaluateFeasibility(base({ sdgFocus: ['SDG-6', 'SDG-13'] }));
    expect(multi.axes.find((a) => a.axis === 'impact')!.score).toBeGreaterThan(
      single.axes.find((a) => a.axis === 'impact')!.score,
    );
  });
});

describe('aggregate scoring', () => {
  it('marks outcome=fail when any single axis is below the floor', () => {
    const r = evaluateFeasibility(base({ noncommercialNotice: false }));
    expect(r.outcome).toBe('fail');
  });

  it('returns weighted aggregate within 0..100', () => {
    const r = evaluateFeasibility(base());
    expect(r.feasibilityScore).toBeGreaterThanOrEqual(0);
    expect(r.feasibilityScore).toBeLessThanOrEqual(100);
  });
});
