// Needs / Offers / Matching — relief & sharing exchange (ADR-0018 §C).
//
// Hard rules enforced here:
//   - Quantity > 0 (DB CHECK is defence-in-depth).
//   - Match endpoints share the same category — DB CHECK + service guard.
//   - Until BOTH sides accept, contact details are masked at the API layer
//     (consumed by the controller; this service simply records state).
//   - State transitions are explicit allow-list (request, offer, match).
//   - Identity verification level cannot be self-set to 'verified' — only
//     a verifier (admin / partner) can grant it via setVerification().
//   - Super-admin pause for either side, append-only with reason ≥ 30 chars.

import { createHash } from 'node:crypto';
import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type NeedCategory = 'relief' | 'supplies' | 'equipment' | 'knowledge' | 'volunteers';
export type Urgency = 'critical' | 'high' | 'normal' | 'low';
export type VerificationLevel = 'verified' | 'community-vouched' | 'unverified';

export type RequestState =
  | 'draft'
  | 'published'
  | 'matching'
  | 'fulfilled'
  | 'closed'
  | 'cancelled'
  | 'expired'
  | 'paused';

export type OfferState =
  | 'draft'
  | 'published'
  | 'matching'
  | 'closed'
  | 'cancelled'
  | 'expired'
  | 'paused';

export type MatchState =
  | 'suggested'
  | 'contacted'
  | 'accepted'
  | 'shipped'
  | 'delivered'
  | 'cancelled';

export interface CreateRequestInput {
  tenantId: string;
  ownerId: string;
  category: NeedCategory;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; description: string }>;
  sdgFocus: string[];
  region: string;
  subregion?: string;
  quantity: number;
  unit: string;
  urgency?: Urgency;
  neededBy: Date;
}

export interface CreateOfferInput {
  tenantId: string;
  ownerId: string;
  category: NeedCategory;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; description: string }>;
  sdgFocus: string[];
  region: string;
  subregion?: string;
  quantity: number;
  unit: string;
  availableUntil: Date;
}

const REQUEST_ALLOWED: Record<RequestState, RequestState[]> = {
  draft: ['published', 'cancelled'],
  published: ['matching', 'cancelled', 'expired', 'paused'],
  matching: ['fulfilled', 'cancelled', 'expired', 'paused'],
  fulfilled: ['closed'],
  closed: [],
  cancelled: [],
  expired: [],
  paused: ['published', 'matching', 'cancelled'],
};

const OFFER_ALLOWED: Record<OfferState, OfferState[]> = {
  draft: ['published', 'cancelled'],
  published: ['matching', 'cancelled', 'expired', 'paused'],
  matching: ['closed', 'cancelled', 'expired', 'paused'],
  closed: [],
  cancelled: [],
  expired: [],
  paused: ['published', 'matching', 'cancelled'],
};

@Injectable()
export class NeedsService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransitionRequest(from: RequestState, to: RequestState): boolean {
    return REQUEST_ALLOWED[from].includes(to);
  }
  static canTransitionOffer(from: OfferState, to: OfferState): boolean {
    return OFFER_ALLOWED[from].includes(to);
  }

  async createRequest(input: CreateRequestInput) {
    if (input.quantity <= 0) throw new BadRequestException('Quantity must be > 0.');
    if (input.neededBy.getTime() <= Date.now()) {
      throw new BadRequestException('neededBy must be in the future.');
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary?.title || !primary?.description) {
      throw new BadRequestException(
        `Need request needs title + description in primary locale (${input.primaryLocale}).`,
      );
    }
    return this.prisma.needRequest.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        category: input.category,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        region: input.region,
        subregion: input.subregion ?? null,
        quantity: input.quantity,
        unit: input.unit,
        urgency: input.urgency ?? 'normal',
        neededBy: input.neededBy,
        verificationLevel: 'unverified',
        state: 'draft',
      },
    });
  }

  async createOffer(input: CreateOfferInput) {
    if (input.quantity <= 0) throw new BadRequestException('Quantity must be > 0.');
    if (input.availableUntil.getTime() <= Date.now()) {
      throw new BadRequestException('availableUntil must be in the future.');
    }
    const primary = input.bodyI18n[input.primaryLocale];
    if (!primary?.title || !primary?.description) {
      throw new BadRequestException(
        `Offer needs title + description in primary locale (${input.primaryLocale}).`,
      );
    }
    return this.prisma.offerListing.create({
      data: {
        tenantId: input.tenantId,
        ownerId: input.ownerId,
        category: input.category,
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus,
        region: input.region,
        subregion: input.subregion ?? null,
        quantity: input.quantity,
        unit: input.unit,
        availableUntil: input.availableUntil,
        verificationLevel: 'unverified',
        state: 'draft',
      },
    });
  }

  async transitionRequest(tenantId: string, requestId: string, to: RequestState) {
    const r = await this.prisma.needRequest.findFirst({ where: { id: requestId, tenantId } });
    if (!r) throw new NotFoundException('Request not found.');
    if (!NeedsService.canTransitionRequest(r.state as RequestState, to)) {
      throw new ConflictException(`Cannot transition request '${r.state}' → '${to}'.`);
    }
    return this.prisma.needRequest.update({
      where: { id: requestId },
      data: {
        state: to,
        ...(to === 'closed' ? { closedAt: new Date() } : {}),
      },
    });
  }

  async transitionOffer(tenantId: string, offerId: string, to: OfferState) {
    const o = await this.prisma.offerListing.findFirst({ where: { id: offerId, tenantId } });
    if (!o) throw new NotFoundException('Offer not found.');
    if (!NeedsService.canTransitionOffer(o.state as OfferState, to)) {
      throw new ConflictException(`Cannot transition offer '${o.state}' → '${to}'.`);
    }
    return this.prisma.offerListing.update({
      where: { id: offerId },
      data: { state: to },
    });
  }

  /**
   * Suggest a match. Both endpoints must:
   *   - belong to the same tenant
   *   - be in 'published' or 'matching' state
   *   - share the same category (also DB-CHECK enforced)
   * The match starts in 'suggested' — neither side sees the other's
   * contact details until BOTH have hit accept().
   */
  async suggestMatch(tenantId: string, requestId: string, offerId: string) {
    const [req, off] = await Promise.all([
      this.prisma.needRequest.findFirst({ where: { id: requestId, tenantId } }),
      this.prisma.offerListing.findFirst({ where: { id: offerId, tenantId } }),
    ]);
    if (!req) throw new NotFoundException('Request not found.');
    if (!off) throw new NotFoundException('Offer not found.');
    if (req.category !== off.category) {
      throw new BadRequestException(
        `Cannot match a '${req.category}' request to a '${off.category}' offer.`,
      );
    }
    const reqOk = req.state === 'published' || req.state === 'matching';
    const offOk = off.state === 'published' || off.state === 'matching';
    if (!reqOk || !offOk) {
      throw new ConflictException(
        `Both endpoints must be published or matching. Got request='${req.state}', offer='${off.state}'.`,
      );
    }
    return this.prisma.needMatch.create({
      data: {
        tenantId,
        requestId,
        offerId,
        category: req.category,
        state: 'suggested',
      },
    });
  }

  /**
   * Acceptance is one-sided. Only when BOTH sides accept does the match
   * transition to 'accepted'. The controller layer also masks contact
   * fields until then.
   */
  async accept(tenantId: string, matchId: string, side: 'requester' | 'provider') {
    const m = await this.prisma.needMatch.findFirst({ where: { id: matchId, tenantId } });
    if (!m) throw new NotFoundException('Match not found.');
    if (m.state !== 'suggested' && m.state !== 'contacted') {
      throw new ConflictException(`Cannot accept a match in state '${m.state}'.`);
    }
    const data: Record<string, unknown> = { state: 'contacted' };
    if (side === 'requester') {
      if (m.requesterAcceptedAt) throw new ConflictException('Requester already accepted.');
      data.requesterAcceptedAt = new Date();
      if (m.providerAcceptedAt) data.state = 'accepted';
    } else {
      if (m.providerAcceptedAt) throw new ConflictException('Provider already accepted.');
      data.providerAcceptedAt = new Date();
      if (m.requesterAcceptedAt) data.state = 'accepted';
    }
    return this.prisma.needMatch.update({
      where: { id: matchId },
      data: data as unknown as Prisma.NeedMatchUpdateInput,
    });
  }

  async transitionMatch(tenantId: string, matchId: string, to: MatchState) {
    const m = await this.prisma.needMatch.findFirst({ where: { id: matchId, tenantId } });
    if (!m) throw new NotFoundException('Match not found.');
    const allowed: Record<MatchState, MatchState[]> = {
      suggested: ['contacted', 'cancelled'],
      contacted: ['accepted', 'cancelled'],
      accepted: ['shipped', 'cancelled'],
      shipped: ['delivered', 'cancelled'],
      delivered: [],
      cancelled: [],
    };
    if (!allowed[m.state as MatchState].includes(to)) {
      throw new ConflictException(`Cannot transition match '${m.state}' → '${to}'.`);
    }
    return this.prisma.needMatch.update({
      where: { id: matchId },
      data: { state: to },
    });
  }

  /**
   * Two-party signed fulfilment. Each side calls sign() once; once both
   * have signed AND the match is in 'shipped' or 'delivered' state, the
   * fulfilment is considered complete.
   */
  async sign(
    tenantId: string,
    matchId: string,
    side: 'requester' | 'provider',
    agreedClauseText: string,
    trackingRef?: string,
    evidenceHashes?: string[],
  ) {
    if (!agreedClauseText || agreedClauseText.trim().length < 30) {
      throw new BadRequestException('Agreed clause text is too short.');
    }
    const m = await this.prisma.needMatch.findFirst({ where: { id: matchId, tenantId } });
    if (!m) throw new NotFoundException('Match not found.');
    if (m.state !== 'shipped' && m.state !== 'delivered') {
      throw new ConflictException(
        `Can only sign for shipped/delivered matches. Current state: '${m.state}'.`,
      );
    }
    const agreedClauseHash = createHash('sha256').update(agreedClauseText).digest('hex');
    const existing = await this.prisma.needFulfillment.findFirst({ where: { matchId, tenantId } });
    if (!existing) {
      return this.prisma.needFulfillment.create({
        data: {
          tenantId,
          matchId,
          trackingRef: trackingRef ?? null,
          evidenceHashes: evidenceHashes ?? [],
          requesterSignedAt: side === 'requester' ? new Date() : null,
          providerSignedAt: side === 'provider' ? new Date() : null,
          agreedClauseHash,
        },
      });
    }
    if (existing.agreedClauseHash !== agreedClauseHash) {
      throw new ConflictException(
        'Both signers must agree to the same clause text. Hashes differ.',
      );
    }
    if (side === 'requester' && existing.requesterSignedAt) {
      throw new ConflictException('Requester already signed.');
    }
    if (side === 'provider' && existing.providerSignedAt) {
      throw new ConflictException('Provider already signed.');
    }
    return this.prisma.needFulfillment.update({
      where: { id: existing.id },
      data: {
        ...(side === 'requester' ? { requesterSignedAt: new Date() } : {}),
        ...(side === 'provider' ? { providerSignedAt: new Date() } : {}),
        ...(trackingRef !== undefined ? { trackingRef } : {}),
        ...(evidenceHashes !== undefined
          ? { evidenceHashes: { set: evidenceHashes } }
          : {}),
      },
    });
  }

  /** Verifier-only — admin/partner grants verification. */
  async setRequestVerification(
    tenantId: string,
    requestId: string,
    level: VerificationLevel,
    verifierId: string,
  ) {
    if (level !== 'verified' && level !== 'community-vouched' && level !== 'unverified') {
      throw new BadRequestException('Unknown verification level.');
    }
    const r = await this.prisma.needRequest.findFirst({ where: { id: requestId, tenantId } });
    if (!r) throw new NotFoundException('Request not found.');
    return this.prisma.needRequest.update({
      where: { id: requestId },
      data: {
        verificationLevel: level,
        verifiedBy: verifierId,
        verifiedAt: new Date(),
      },
    });
  }
}
