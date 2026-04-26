// Event subscription management (ADR-0020 §F).
//
// A subscription says "deliver events matching this pattern via this channel".
// Webhook deliveries are HMAC-SHA256 signed (ADR-0013 partner pattern). The
// raw secret is shown ONCE on creation and never persisted — we keep only
// its SHA-256 hash. A delivery worker (out of MVP scope) drains the
// domain_events table and calls the webhook with a signature header.

import { createHash, randomBytes } from 'node:crypto';
import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface CreateSubscriptionInput {
  tenantId: string;
  pluginId: string;
  eventPattern: string;
  deliveryKind: 'inproc' | 'webhook';
  webhookUrl?: string;
}

export interface IssuedSubscription {
  id: string;
  /** Raw webhook secret returned ONCE; only present for webhook subscriptions. */
  webhookSecret?: string;
}

const PATTERN_RE = /^[a-z0-9*][a-z0-9*.-]{1,80}$/i;
const FAILURE_THRESHOLD = 5;

@Injectable()
export class SubscriptionsService {
  constructor(private readonly prisma: PrismaService) {}

  async create(input: CreateSubscriptionInput): Promise<IssuedSubscription> {
    if (!PATTERN_RE.test(input.eventPattern)) {
      throw new BadRequestException('eventPattern has unsupported characters.');
    }
    if (input.deliveryKind === 'webhook') {
      if (!input.webhookUrl) {
        throw new BadRequestException('webhook subscription needs webhookUrl.');
      }
      if (!/^https?:\/\//.test(input.webhookUrl)) {
        throw new BadRequestException('webhookUrl must be http(s).');
      }
    } else if (input.webhookUrl) {
      throw new BadRequestException('inproc subscription must not carry a webhookUrl.');
    }
    const plugin = await this.prisma.pluginManifest.findFirst({
      where: { id: input.pluginId, tenantId: input.tenantId },
    });
    if (!plugin) throw new NotFoundException('Plugin manifest not found.');
    if (plugin.state !== 'approved') {
      throw new ConflictException(
        `Subscriptions only accepted on approved plugins. Current state: '${plugin.state}'.`,
      );
    }

    let webhookSecret: string | undefined;
    let webhookSecretHash: string | null = null;
    if (input.deliveryKind === 'webhook') {
      webhookSecret = `sdgi_whsec_${randomBytes(32).toString('base64url')}`;
      webhookSecretHash = createHash('sha256').update(webhookSecret).digest('hex');
    }

    const created = await this.prisma.eventSubscription.create({
      data: {
        tenantId: input.tenantId,
        pluginId: input.pluginId,
        eventPattern: input.eventPattern,
        deliveryKind: input.deliveryKind,
        webhookUrl: input.deliveryKind === 'webhook' ? input.webhookUrl! : null,
        webhookSecretHash,
        active: true,
      },
    });
    const issued: IssuedSubscription = { id: created.id };
    if (webhookSecret !== undefined) {
      issued.webhookSecret = webhookSecret;
    }
    return issued;
  }

  /**
   * Mark a delivery as failed. After FAILURE_THRESHOLD consecutive
   * failures the subscription is auto-deactivated; a super-admin must
   * explicitly reactivate it.
   */
  async recordFailure(tenantId: string, subscriptionId: string) {
    const sub = await this.prisma.eventSubscription.findFirst({
      where: { id: subscriptionId, tenantId },
    });
    if (!sub) throw new NotFoundException('Subscription not found.');
    const next = sub.failureCount + 1;
    return this.prisma.eventSubscription.update({
      where: { id: subscriptionId },
      data: {
        failureCount: next,
        active: next < FAILURE_THRESHOLD ? sub.active : false,
      },
    });
  }

  async recordSuccess(tenantId: string, subscriptionId: string) {
    const sub = await this.prisma.eventSubscription.findFirst({
      where: { id: subscriptionId, tenantId },
    });
    if (!sub) throw new NotFoundException('Subscription not found.');
    return this.prisma.eventSubscription.update({
      where: { id: subscriptionId },
      data: { failureCount: 0, lastDeliveredAt: new Date() },
    });
  }

  /** Super-admin re-enables a subscription that was auto-deactivated. */
  async reactivate(tenantId: string, subscriptionId: string) {
    const sub = await this.prisma.eventSubscription.findFirst({
      where: { id: subscriptionId, tenantId },
    });
    if (!sub) throw new NotFoundException('Subscription not found.');
    if (sub.active) return sub;
    return this.prisma.eventSubscription.update({
      where: { id: subscriptionId },
      data: { active: true, failureCount: 0 },
    });
  }
}
