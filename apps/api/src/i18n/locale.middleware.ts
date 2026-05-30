import { Injectable, NestMiddleware } from '@nestjs/common';
import type { NextFunction, Request, Response } from 'express';

// Kept in sync with apps/web/src/i18n/routing.ts. See ADR-0009.
export const SUPPORTED_LOCALES = [
  'en', 'zh', 'hi', 'es', 'ar', 'fr', 'bn', 'pt', 'ru', 'id', 'ja', 'ko', 'sw',
] as const;
export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];
export const DEFAULT_LOCALE: SupportedLocale = 'en';
export const RTL_LOCALES: ReadonlySet<SupportedLocale> = new Set(['ar']);

declare module 'express' {
  interface Request {
    locale?: SupportedLocale;
  }
}

/**
 * Picks the best locale for this request.
 * Order: ?lang= → Accept-Language q-weighted negotiation → DEFAULT_LOCALE.
 *
 * Equity matters here: if a user prefers ko, we honour that even if our
 * default is en. We never silently force English on Asian-language readers.
 */
@Injectable()
export class LocaleMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    const queryLang = typeof req.query.lang === 'string' ? req.query.lang : undefined;
    const accepted = req.header('accept-language') ?? '';
    req.locale = pickLocale(queryLang, accepted);
    res.setHeader('Content-Language', req.locale);
    next();
  }
}

export function pickLocale(
  queryLang: string | undefined,
  acceptLanguage: string,
): SupportedLocale {
  const fromQuery = normalize(queryLang);
  if (fromQuery && SUPPORTED_LOCALES.includes(fromQuery as SupportedLocale)) {
    return fromQuery as SupportedLocale;
  }

  const candidates = parseAcceptLanguage(acceptLanguage);
  for (const tag of candidates) {
    const norm = normalize(tag) as SupportedLocale;
    if (SUPPORTED_LOCALES.includes(norm)) return norm;
  }
  return DEFAULT_LOCALE;
}

/** "ko-KR" → "ko", "zh-Hans" / "zh-CN" → "zh" */
function normalize(tag: string | undefined): string | undefined {
  if (!tag) return undefined;
  const lower = tag.toLowerCase();
  const base = lower.split(/[-_]/)[0];
  if (!base) return undefined;
  if (base === 'cmn' || base === 'zh') return 'zh';
  return base;
}

interface ParsedTag {
  tag: string;
  q: number;
}

function parseAcceptLanguage(header: string): string[] {
  if (!header) return [];
  const tags: ParsedTag[] = header
    .split(',')
    .map((part) => {
      const [tagRaw, ...params] = part.trim().split(';');
      const qParam = params.find((p) => p.trim().startsWith('q='));
      const q = qParam ? Number(qParam.split('=')[1]) : 1;
      return { tag: (tagRaw ?? '').trim(), q: Number.isFinite(q) ? q : 1 };
    })
    .filter((t) => t.tag && t.q > 0)
    .sort((a, b) => b.q - a.q);
  return tags.map((t) => t.tag);
}
