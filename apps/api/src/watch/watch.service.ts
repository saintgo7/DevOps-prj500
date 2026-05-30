import { Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export interface ItemFilter {
  sdgFocus?: string[] | undefined;
  categories?: string[] | undefined;
  languages?: string[] | undefined;
  regions?: string[] | undefined;
}

export interface WatchItemDto {
  id: string;
  title: string;
  url: string;
  summary: string | null;
  language: string;
  publishedAt: string | null;
  discoveredAt: string;
  sdgFocus: string[];
  region: string | null;
  source: { id: string; name: string; category: string };
}

@Injectable()
export class WatchService {
  constructor(private readonly prisma: PrismaService) {}

  async listSources(filter: { category?: string; active?: boolean } = {}) {
    return this.prisma.watchSource.findMany({
      where: {
        ...(filter.category ? { category: filter.category } : {}),
        ...(filter.active !== undefined ? { active: filter.active } : {}),
      },
      orderBy: { name: 'asc' },
    });
  }

  async listRecentItems(
    filter: ItemFilter & { since?: Date; take?: number } = {},
  ): Promise<WatchItemDto[]> {
    const where: Prisma.WatchItemWhereInput = {
      ...(filter.since ? { discoveredAt: { gte: filter.since } } : {}),
      ...(filter.sdgFocus && filter.sdgFocus.length > 0
        ? { sdgFocus: { hasSome: filter.sdgFocus } }
        : {}),
      ...(filter.languages && filter.languages.length > 0
        ? { language: { in: filter.languages } }
        : {}),
      ...(filter.regions && filter.regions.length > 0
        ? { region: { in: filter.regions } }
        : {}),
      ...(filter.categories && filter.categories.length > 0
        ? { source: { category: { in: filter.categories } } }
        : {}),
    };

    const items = await this.prisma.watchItem.findMany({
      where,
      orderBy: { discoveredAt: 'desc' },
      take: filter.take ?? 50,
      include: { source: true },
    });

    return items.map((i) => ({
      id: i.id,
      title: i.title,
      url: i.url,
      summary: i.summary,
      language: i.language,
      publishedAt: i.publishedAt?.toISOString() ?? null,
      discoveredAt: i.discoveredAt.toISOString(),
      sdgFocus: i.sdgFocus,
      region: i.region,
      source: { id: i.source.id, name: i.source.name, category: i.source.category },
    }));
  }

  async createSubscription(input: {
    tenantId: string;
    userId: string;
    name?: string;
    filter: ItemFilter;
    digestLanguage?: string;
  }) {
    return this.prisma.watchSubscription.create({
      data: {
        tenantId: input.tenantId,
        userId: input.userId,
        ...(input.name ? { name: input.name } : {}),
        filter: input.filter as Prisma.InputJsonValue,
        ...(input.digestLanguage ? { digestLanguage: input.digestLanguage } : {}),
      },
    });
  }

  async listSubscriptions(tenantId: string, userId: string) {
    return this.prisma.watchSubscription.findMany({
      where: { tenantId, userId, active: true },
      orderBy: { createdAt: 'desc' },
    });
  }

  /**
   * Records a private interest. Per ADR-0012 §"Collaboration workflow",
   * this DOES NOT auto-broadcast to anyone. Reaching out requires a
   * separate explicit human action with content review.
   */
  async expressInterest(input: {
    tenantId: string;
    userId: string;
    itemId: string;
    intent?: string;
    note?: string;
    contactConsent?: boolean;
  }) {
    return this.prisma.collaborationInterest.upsert({
      where: {
        tenantId_userId_itemId: {
          tenantId: input.tenantId,
          userId: input.userId,
          itemId: input.itemId,
        },
      },
      update: {
        intent: input.intent ?? 'learn',
        ...(input.note !== undefined ? { note: input.note } : {}),
        ...(input.contactConsent !== undefined
          ? { contactConsent: input.contactConsent }
          : {}),
      },
      create: {
        tenantId: input.tenantId,
        userId: input.userId,
        itemId: input.itemId,
        intent: input.intent ?? 'learn',
        ...(input.note !== undefined ? { note: input.note } : {}),
        ...(input.contactConsent !== undefined
          ? { contactConsent: input.contactConsent }
          : {}),
      },
    });
  }
}
