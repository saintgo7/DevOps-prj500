import { describe, expect, it } from 'vitest';
import { checkHarmfulContent } from './harmful-content';

describe('harmful-content', () => {
  it('passes a wholesome SDG line', () => {
    const r = checkHarmfulContent(['Plant one tree. Water it. Watch it grow.']);
    expect(r.pass).toBe(true);
    expect(r.findings).toHaveLength(5);
  });

  it('blocks personal-attack slurs in English', () => {
    const r = checkHarmfulContent(['What an idiot policy.']);
    expect(r.pass).toBe(false);
    expect(r.findings.find((f) => f.category === 'personal-attack')?.ok).toBe(false);
  });

  it('blocks Korean personal attacks (병신)', () => {
    const r = checkHarmfulContent(['이건 진짜 병신 같은 정책이야.']);
    expect(r.pass).toBe(false);
  });

  it('blocks "all X are Y" hate frames', () => {
    const r = checkHarmfulContent(['All muslims are problematic.']);
    expect(r.pass).toBe(false);
  });

  it('blocks Korean blanket-group hate frames', () => {
    const r = checkHarmfulContent(['모든 무슬림은 문제다.']);
    expect(r.pass).toBe(false);
  });

  it('blocks violence glorification ("kill them all", "death to ...")', () => {
    expect(checkHarmfulContent(['Just kill them all.']).pass).toBe(false);
    expect(checkHarmfulContent(['Death to the deniers!']).pass).toBe(false);
  });

  it('blocks "guaranteed cure" health misinformation', () => {
    expect(checkHarmfulContent(['This product guaranteed cure for all chronic disease.']).pass).toBe(false);
  });

  it('blocks "100% safe" / "guaranteed return" pattern', () => {
    expect(checkHarmfulContent(['The investment offers a guaranteed return of 30% annually.']).pass).toBe(false);
  });

  it('blocks Korean health misinformation (완치)', () => {
    expect(checkHarmfulContent(['이 제품은 암을 완치시킵니다.']).pass).toBe(false);
  });

  it('blocks us-vs-them framing', () => {
    expect(checkHarmfulContent(['They are the enemy of our way of life.']).pass).toBe(false);
  });

  it('blocks dehumanising vocabulary', () => {
    expect(checkHarmfulContent(['Those people are vermin.']).pass).toBe(false);
    expect(checkHarmfulContent(['They are not human.']).pass).toBe(false);
    expect(checkHarmfulContent(['인간 이하의 존재들이다.']).pass).toBe(false);
  });

  it('combines multiple parts when scanning', () => {
    const r = checkHarmfulContent([
      'Headline 1 — fine.',
      'Headline 2 — also fine.',
      'And buried later: kill them all.',
    ]);
    expect(r.pass).toBe(false);
  });

  it('returns one finding per category in stable order', () => {
    const r = checkHarmfulContent(['fine']);
    const cats = r.findings.map((f) => f.category);
    expect(cats).toEqual([
      'personal-attack',
      'violence-glorification',
      'health-financial-legal-misinfo',
      'us-vs-them',
      'dehumanisation',
    ]);
  });

  it('plain-language messages do not embed jargon', () => {
    const r = checkHarmfulContent(['Just kill them all.']);
    const violenceMsg = r.findings.find((f) => f.category === 'violence-glorification')?.message;
    expect(violenceMsg).toMatch(/violence/i);
    expect(violenceMsg).not.toMatch(/regex|pattern/i);
  });
});
