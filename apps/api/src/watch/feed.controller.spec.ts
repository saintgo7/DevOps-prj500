import { describe, expect, it } from 'vitest';
import { buildAtom } from './feed.controller';

describe('buildAtom', () => {
  it('produces a valid Atom skeleton with declared CC BY 4.0 rights', () => {
    const xml = buildAtom('Test feed', 'https://sdgi.app/feed/en/sdg.atom', []);
    expect(xml).toContain('<?xml version="1.0" encoding="utf-8"?>');
    expect(xml).toContain('<feed xmlns="http://www.w3.org/2005/Atom">');
    expect(xml).toContain('<title>Test feed</title>');
    expect(xml).toContain('Creative Commons Attribution 4.0');
    expect(xml).toContain('<link rel="self" href="https://sdgi.app/feed/en/sdg.atom" />');
  });

  it('renders entries with category tags for each SDG', () => {
    const xml = buildAtom('Test feed', 'https://sdgi.app/feed/en/sdg.atom', [
      {
        id: 'item-1',
        title: 'Climate finding',
        url: 'https://example.org/news/123',
        summary: 'About SDG 13',
        publishedAt: '2026-04-25T12:00:00Z',
        discoveredAt: '2026-04-25T12:00:00Z',
        sdgFocus: ['SDG-13', 'SDG-15'],
        source: { name: 'UN SDG News' },
      },
    ]);
    expect(xml).toContain('<title>Climate finding</title>');
    expect(xml).toContain('href="https://example.org/news/123"');
    expect(xml).toContain('<category term="SDG-13" />');
    expect(xml).toContain('<category term="SDG-15" />');
    expect(xml).toContain('<source><title>UN SDG News</title></source>');
  });

  it('escapes XML-special characters in title and summary', () => {
    const xml = buildAtom('Feed', 'https://sdgi.app/feed/en/sdg.atom', [
      {
        id: 'i',
        title: 'A & B <C>',
        url: 'https://example.org/?a=1&b=2',
        summary: '"quoted" & <tag>',
        publishedAt: null,
        discoveredAt: '2026-04-25T12:00:00Z',
        sdgFocus: [],
        source: { name: 'X' },
      },
    ]);
    expect(xml).not.toMatch(/title>A & B <C></);
    expect(xml).toContain('A &amp; B &lt;C&gt;');
    expect(xml).toContain('&quot;quoted&quot;');
  });
});
