import { describe, expect, it } from 'vitest';
import { StubScanner, pickScanner } from './scanner';

describe('Scanner', () => {
  it('StubScanner returns at least one finding for a source', async () => {
    const findings = await new StubScanner().scan({
      sourceId: 'src-1',
      url: 'https://example.org/news',
      feedUrl: null,
      kind: 'html',
      language: 'en',
      region: null,
      sdgFocus: ['SDG-13'],
    });
    expect(findings).toHaveLength(1);
    expect(findings[0]?.url).toBe('https://example.org/news');
    expect(findings[0]?.sdgFocus).toEqual(['SDG-13']);
  });

  it('pickScanner returns a scanner for any known kind', () => {
    expect(pickScanner('rss').kind).toBeDefined();
    expect(pickScanner('atom').kind).toBeDefined();
    expect(pickScanner('html').kind).toBeDefined();
    expect(pickScanner('github').kind).toBeDefined();
    expect(pickScanner('api').kind).toBeDefined();
  });
});
