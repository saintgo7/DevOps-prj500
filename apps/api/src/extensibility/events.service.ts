// Domain event log + subscription matching (ADR-0020 §E + §F).
//
// All emit() calls funnel through here. Payloads are PII-masked in place
// using the field list provided by the caller (typically taken from the
// CustomDomain.piiFields). Subscriptions matching the event pattern are
// looked up but NOT auto-delivered in this MVP — a follow-up worker
// drains the table and signs outgoing webhooks.

import { BadRequestException, Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { maskPii } from './pii-mask';

export interface EmitInput {
  tenantId: string;
  source: string;        // 'core.column' | 'plugin.<key>' | ...
  eventName: string;     // 'column.published' | 'biodiv-card.created' | ...
  payload: unknown;
  /** Field paths in payload to mask before persisting. */
  piiFields?: readonly string[];
  correlationId?: string;
}

/**
 * Returns true if a subscription pattern matches an event name.
 * Pattern grammar:
 *   '*'                 — match anything (single token wildcard)
 *   'core.*'            — prefix with one trailing wildcard
 *   '*.failed'          — suffix with one leading wildcard
 *   'core.column.published' — exact match
 *
 * No double-wildcards. Splits on '.'.
 */
export function patternMatches(pattern: string, eventName: string): boolean {
  if (pattern === '*' || pattern === eventName) return true;
  const pSeg = pattern.split('.');
  const eSeg = eventName.split('.');
  if (pSeg.length !== eSeg.length) return false;
  for (let i = 0; i < pSeg.length; i += 1) {
    if (pSeg[i] !== '*' && pSeg[i] !== eSeg[i]) return false;
  }
  return true;
}

@Injectable()
export class EventsService {
  constructor(private readonly prisma: PrismaService) {}

  async emit(input: EmitInput) {
    if (!input.eventName || !input.eventName.includes('.')) {
      throw new BadRequestException(
        'eventName must follow "<scope>.<verb>" form, e.g. "biodiv-card.created".',
      );
    }
    if (!input.source) {
      throw new BadRequestException('event source is required.');
    }
    const masked = maskPii(input.payload ?? {}, input.piiFields ?? []);
    return this.prisma.domainEvent.create({
      data: {
        tenantId: input.tenantId,
        source: input.source,
        eventName: input.eventName,
        payload: masked as unknown as Prisma.InputJsonValue,
        correlationId: input.correlationId ?? null,
      },
    });
  }

  /**
   * Find active subscriptions whose pattern matches the given event name.
   * Used by the (future) delivery worker; exposed here so other modules
   * can preview which plugins will see an event before it's emitted.
   */
  async matchingSubscriptions(tenantId: string, eventName: string) {
    const subs = await this.prisma.eventSubscription.findMany({
      where: { tenantId, active: true },
    });
    return subs.filter((s) => patternMatches(s.eventPattern, eventName));
  }
}
