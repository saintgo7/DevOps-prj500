import { describe, expect, it } from 'vitest';
import { countSources, validateCitations } from './citations';

const SELF = '11111111-1111-1111-1111-111111111111';
const OTHER = '22222222-2222-2222-2222-222222222222';

describe('countSources', () => {
  it('counts a single source', () => {
    expect(countSources({ position: 1, rendered: 'x', sourceColumnId: OTHER })).toBe(1);
  });
  it('counts zero when nothing is set', () => {
    expect(countSources({ position: 1, rendered: 'x' })).toBe(0);
  });
  it('counts two when both column and external doi are set', () => {
    expect(
      countSources({
        position: 1,
        rendered: 'x',
        sourceColumnId: OTHER,
        externalDoi: '10.1234/abcd',
      }),
    ).toBe(2);
  });
});

describe('validateCitations', () => {
  it('passes a clean citation list', () => {
    const out = validateCitations(
      [
        { position: 1, rendered: 'Smith, 2025', externalDoi: '10.1000/x' },
        { position: 2, rendered: 'Doe, 2024', sourceColumnId: OTHER },
      ],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(true);
  });

  it('rejects a citation with no source', () => {
    const out = validateCitations(
      [{ position: 1, rendered: 'Anon, n.d.' }],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(false);
    expect(out.errors[0]).toMatch(/exactly one source/);
  });

  it('rejects a citation with two sources', () => {
    const out = validateCitations(
      [
        {
          position: 1,
          rendered: 'duplicated',
          sourceColumnId: OTHER,
          externalDoi: '10.1000/y',
        },
      ],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(false);
  });

  it('rejects gaps in citation positions', () => {
    const out = validateCitations(
      [
        { position: 1, rendered: 'a', externalDoi: '10/a' },
        { position: 3, rendered: 'b', externalDoi: '10/b' },
      ],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(false);
    expect(out.errors.join(' ')).toMatch(/contiguous/);
  });

  it('rejects non-permanent external URLs', () => {
    const out = validateCitations(
      [{ position: 1, rendered: 'blog', externalUrl: 'https://random.example.com/post' }],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(false);
    expect(out.errors.join(' ')).toMatch(/permanent identifier/);
  });

  it('accepts an arxiv URL as permanent', () => {
    const out = validateCitations(
      [{ position: 1, rendered: 'preprint', externalUrl: 'https://arxiv.org/abs/2501.01234' }],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(true);
  });

  it('rejects when self-citations exceed 20% without override', () => {
    const out = validateCitations(
      [
        { position: 1, rendered: 'self-1', sourceManuscriptId: SELF },
        { position: 2, rendered: 'self-2', sourceManuscriptId: SELF },
        { position: 3, rendered: 'other', sourceColumnId: OTHER },
      ],
      { selfManuscriptId: SELF },
    );
    expect(out.ok).toBe(false);
    expect(out.errors.join(' ')).toMatch(/Self-citation/);
  });

  it('accepts excessive self-citations with an editor override', () => {
    const out = validateCitations(
      [
        { position: 1, rendered: 'self-1', sourceManuscriptId: SELF },
        { position: 2, rendered: 'self-2', sourceManuscriptId: SELF },
        { position: 3, rendered: 'other', sourceColumnId: OTHER },
      ],
      { selfManuscriptId: SELF, selfCiteOverrideReason: 'series follow-up' },
    );
    expect(out.ok).toBe(true);
  });
});
