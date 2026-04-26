import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { AGE_TIERS, checkSafety, type AgeTier } from './age-tier';
import { composeHashtags } from './hashtags';
import type { Platform } from './platforms';

interface ColumnBody {
  title?: string;
  summary?: string;
  excerpt?: string;
}

export interface GenerateOptions {
  tenantId: string;
  columnId: string;
  /** Subset of supported locales to fan out — default = all from primaryLocale + en. */
  locales?: string[];
  /** Subset of age tiers — default = all four. */
  ageTiers?: AgeTier[];
}

export interface GeneratedVariantOutcome {
  variantId: string;
  locale: string;
  ageTier: AgeTier;
  blocked: boolean;
  reason?: string;
}

@Injectable()
export class StoryService {
  constructor(private readonly prisma: PrismaService) {}

  async generateFromColumn(opts: GenerateOptions): Promise<{
    storyId: string;
    variants: GeneratedVariantOutcome[];
  }> {
    const column = await this.prisma.column.findFirst({
      where: { id: opts.columnId, tenantId: opts.tenantId, state: 'published' },
    });
    if (!column) {
      throw new NotFoundException('Source column must be published before stories may be generated.');
    }

    const story = await this.prisma.shortStory.create({
      data: {
        tenantId: opts.tenantId,
        sourceColumnId: column.id,
        state: 'drafting',
        sdgFocus: column.sdgFocus,
      },
    });

    const body = column.bodyI18n as Record<string, ColumnBody>;
    const sourceLocales =
      opts.locales && opts.locales.length > 0
        ? opts.locales
        : Array.from(new Set([column.primaryLocale, 'en', ...Object.keys(body)]));
    const tiers = opts.ageTiers && opts.ageTiers.length > 0 ? opts.ageTiers : [...AGE_TIERS];

    const outcomes: GeneratedVariantOutcome[] = [];
    for (const locale of sourceLocales) {
      const localeBody = body[locale] ?? body[column.primaryLocale] ?? body.en;
      if (!localeBody?.summary) {
        outcomes.push({
          variantId: '',
          locale,
          ageTier: tiers[0]!,
          blocked: true,
          reason: `No source summary in '${locale}'.`,
        });
        continue;
      }
      for (const tier of tiers) {
        const draftCaption = formatCaptionDraft(localeBody, tier);
        const safety = checkSafety(draftCaption, tier);
        if (!safety.ok) {
          outcomes.push({
            variantId: '',
            locale,
            ageTier: tier,
            blocked: true,
            reason: safety.results.find((r) => !r.ok)?.message ?? 'Safety check failed.',
          });
          continue;
        }
        const hashtags = composeHashtags({
          goalIds: column.sdgFocus,
          locale: locale as Parameters<typeof composeHashtags>[0]['locale'],
          platform: 'instagram_reels' as Platform, // default; per-post recompute later
        });
        const storyboard = stubStoryboard(localeBody, tier, locale);
        const variant = await this.prisma.storyVariant.create({
          data: {
            tenantId: opts.tenantId,
            shortStoryId: story.id,
            locale,
            ageTier: tier,
            caption: draftCaption,
            hooks: extractHooks(localeBody),
            ctaText: 'sdgi.app',
            hashtags,
            storyboard: storyboard as unknown as Prisma.InputJsonValue,
            attribution: 'ai-assisted',
            state: 'draft',
            safetyReport: safety as unknown as Prisma.InputJsonValue,
          },
        });
        outcomes.push({ variantId: variant.id, locale, ageTier: tier, blocked: false });
      }
    }

    await this.prisma.shortStory.update({
      where: { id: story.id },
      data: { state: 'ready' },
    });

    return { storyId: story.id, variants: outcomes };
  }

  async approveVariant(tenantId: string, variantId: string): Promise<void> {
    const v = await this.prisma.storyVariant.findFirst({ where: { id: variantId, tenantId } });
    if (!v) throw new NotFoundException('Variant not found.');
    if (v.state !== 'draft' && v.state !== 'pending') {
      throw new BadRequestException(`Cannot approve a variant in state '${v.state}'.`);
    }
    await this.prisma.storyVariant.update({
      where: { id: variantId },
      data: { state: 'approved', approvedAt: new Date() },
    });
  }

  async listForStory(tenantId: string, storyId: string) {
    return this.prisma.storyVariant.findMany({
      where: { tenantId, shortStoryId: storyId },
      orderBy: [{ locale: 'asc' }, { ageTier: 'asc' }],
    });
  }
}

function formatCaptionDraft(body: ColumnBody, tier: AgeTier): string {
  const summary = body.summary ?? '';
  const trimmed = summary.length > 220 ? summary.slice(0, 217) + '…' : summary;
  // Simple tier-aware prefix. Real generation lives in apps/ai (Claude),
  // gated behind ColumnService approval and human variant review.
  switch (tier) {
    case 'children':
      return `함께 알아봐요 — ${trimmed}`;
    case 'teen':
      return `오늘 한 가지만 — ${trimmed}`;
    case 'senior':
      return `천천히 함께 — ${trimmed}`;
    case 'adult':
    default:
      return trimmed;
  }
}

function extractHooks(body: ColumnBody): string[] {
  const text = (body.title ?? body.summary ?? '').trim();
  if (!text) return [];
  const first = text.split(/[.!?。!?]/)[0]?.trim();
  return first ? [first] : [];
}

interface StoryboardStub {
  version: string;
  ageTier: AgeTier;
  locale: string;
  totalDurationSec: number;
  aspectRatio: '9:16';
  scenes: Array<{ index: number; durationSec: number; voiceover: string; caption: string; broll: string }>;
  watermark: string;
  attribution: string;
}

function stubStoryboard(body: ColumnBody, tier: AgeTier, locale: string): StoryboardStub {
  const summary = body.summary ?? '';
  const sentences = summary.split(/[.!?。!?]/).map((s) => s.trim()).filter(Boolean).slice(0, 4);
  const sceneDuration = tier === 'senior' ? 8 : tier === 'children' ? 6 : 5;
  return {
    version: '1.0',
    ageTier: tier,
    locale,
    totalDurationSec: sentences.length * sceneDuration,
    aspectRatio: '9:16',
    scenes: sentences.map((s, i) => ({
      index: i,
      durationSec: sceneDuration,
      voiceover: s,
      caption: s.length > 40 ? s.slice(0, 37) + '…' : s,
      broll: 'Respectful, no faces; abstract or symbolic imagery suitable for ' + tier,
    })),
    watermark: 'AI-assisted • Source-attributed',
    attribution: body.title ?? 'See source column',
  };
}
