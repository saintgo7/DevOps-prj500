import { Controller, Get, Header, Param, Query, Res } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { SkipThrottle } from '@nestjs/throttler';
import type { Response } from 'express';
import { WatchService } from './watch.service';

const SITE = process.env.SITE_URL ?? 'https://sdgi.app';

@ApiTags('feed')
@SkipThrottle()
@Controller('feed')
export class FeedController {
  constructor(private readonly watch: WatchService) {}

  /**
   * Public Atom feed of recent SDG findings, optionally filtered by goal.
   * Anyone may resyndicate this — see ADR-0012 §"Public RSS/Atom feed".
   * No authentication. CC BY 4.0 (declared in <rights>).
   */
  @Get(':locale/sdg/:goalId.atom')
  @Header('Content-Type', 'application/atom+xml; charset=utf-8')
  @Header('Cache-Control', 'public, max-age=1800')
  @ApiOperation({
    summary: 'Public Atom feed of weekly SDG findings (filterable by goal)',
  })
  async sdgGoalFeed(
    @Param('locale') locale: string,
    @Param('goalId') goalId: string,
    @Query('lang') lang: string | undefined,
    @Res() res: Response,
  ): Promise<void> {
    const items = await this.watch.listRecentItems({
      sdgFocus: [goalId],
      languages: lang ? [lang] : undefined,
      since: new Date(Date.now() - 14 * 86400 * 1000),
      take: 50,
    });
    const feedTitle = `SDG Impact Cloud — ${goalId} weekly findings (${locale})`;
    const feedUrl = `${SITE}/feed/${encodeURIComponent(locale)}/sdg/${encodeURIComponent(goalId)}.atom`;
    res.send(buildAtom(feedTitle, feedUrl, items));
  }

  @Get(':locale/sdg.atom')
  @Header('Content-Type', 'application/atom+xml; charset=utf-8')
  @Header('Cache-Control', 'public, max-age=1800')
  @ApiOperation({ summary: 'Public Atom feed of all weekly SDG findings' })
  async sdgFeed(
    @Param('locale') locale: string,
    @Query('lang') lang: string | undefined,
    @Res() res: Response,
  ): Promise<void> {
    const items = await this.watch.listRecentItems({
      languages: lang ? [lang] : undefined,
      since: new Date(Date.now() - 7 * 86400 * 1000),
      take: 50,
    });
    const feedTitle = `SDG Impact Cloud — weekly findings (${locale})`;
    const feedUrl = `${SITE}/feed/${encodeURIComponent(locale)}/sdg.atom`;
    res.send(buildAtom(feedTitle, feedUrl, items));
  }
}

interface FeedEntry {
  id: string;
  title: string;
  url: string;
  summary: string | null;
  publishedAt: string | null;
  discoveredAt: string;
  sdgFocus: string[];
  source: { name: string };
}

export function buildAtom(title: string, selfUrl: string, items: FeedEntry[]): string {
  const updated =
    items[0]?.discoveredAt ?? items[0]?.publishedAt ?? new Date().toISOString();
  const entries = items.map(renderEntry).join('\n');
  return `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>${esc(title)}</title>
  <link rel="self" href="${esc(selfUrl)}" />
  <link rel="alternate" href="${esc(SITE)}" />
  <id>${esc(selfUrl)}</id>
  <updated>${esc(updated)}</updated>
  <author><name>SDG Impact Cloud community</name></author>
  <rights>Creative Commons Attribution 4.0 International (CC BY 4.0). See ${esc(SITE)}/PRINCIPLES.md</rights>
  <generator uri="${esc(SITE)}">SDG Impact Cloud</generator>
${entries}
</feed>`;
}

function renderEntry(item: FeedEntry): string {
  const summary = item.summary ?? '';
  const tags = item.sdgFocus
    .map((s) => `  <category term="${esc(s)}" />`)
    .join('\n');
  const published = item.publishedAt ?? item.discoveredAt;
  return `<entry>
  <id>${esc(item.url)}#${esc(item.id)}</id>
  <title>${esc(item.title)}</title>
  <link rel="alternate" href="${esc(item.url)}" />
  <published>${esc(published)}</published>
  <updated>${esc(item.discoveredAt)}</updated>
  <source><title>${esc(item.source.name)}</title></source>
  <summary type="text">${esc(summary)}</summary>
${tags}
</entry>`;
}

function esc(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
