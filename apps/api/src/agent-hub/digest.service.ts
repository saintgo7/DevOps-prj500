// Daily digest persistence + lifecycle (ADR-0021 §E).
//
// AI-drafted digests must pass a human-review gate before publish
// (ADR-0013 pattern). Validation enforces en + ko summaries and a 60+
// character minimum so we don't leak one-liner digests pretending to be
// a day's worth of work.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { bundle, validateSummary, type MessageInput } from './digest-composer';

export type DigestState = 'draft' | 'human_review' | 'published' | 'rejected';

export interface UpsertDigestInput {
  tenantId: string;
  roomId?: string;
  digestDate: Date;
  summaryI18n: Record<string, string>;
  sourceMessageIds: string[];
  aiProvenance?: {
    model: string;
    promptVersion: string;
    generatedAt: string;
    tokensIn?: number;
    tokensOut?: number;
  };
}

const ALLOWED: Record<DigestState, DigestState[]> = {
  draft: ['human_review', 'rejected'],
  human_review: ['published', 'rejected', 'draft'],
  published: [],
  rejected: ['draft'],
};

@Injectable()
export class AgentDigestService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: DigestState, to: DigestState): boolean {
    return ALLOWED[from].includes(to);
  }

  /** Build a deterministic bundle of one day's traffic. Useful as input to a downstream summariser. */
  bundleDay(messages: readonly MessageInput[]) {
    return bundle(messages);
  }

  /**
   * Create or replace the digest for (tenant, room?, date). If a non-published
   * digest already exists for that key, we update it; published digests are
   * immutable (use erratum / new date instead).
   */
  async upsertDraft(input: UpsertDigestInput) {
    if (input.sourceMessageIds.length === 0) {
      throw new BadRequestException(
        'Digest must reference at least one source message id.',
      );
    }
    const existing = await this.prisma.agentDailyDigest.findFirst({
      where: {
        tenantId: input.tenantId,
        roomId: input.roomId ?? null,
        digestDate: input.digestDate,
      },
    });
    if (existing && existing.state === 'published') {
      throw new ConflictException(
        'A published digest already exists for that day. Issue an erratum instead.',
      );
    }
    if (existing) {
      return this.prisma.agentDailyDigest.update({
        where: { id: existing.id },
        data: {
          summaryI18n: input.summaryI18n as unknown as Prisma.InputJsonValue,
          sourceMessageIds: input.sourceMessageIds,
          aiProvenance: (input.aiProvenance ?? null) as unknown as Prisma.InputJsonValue,
          state: 'draft',
        },
      });
    }
    return this.prisma.agentDailyDigest.create({
      data: {
        tenantId: input.tenantId,
        roomId: input.roomId ?? null,
        digestDate: input.digestDate,
        summaryI18n: input.summaryI18n as unknown as Prisma.InputJsonValue,
        sourceMessageIds: input.sourceMessageIds,
        aiProvenance: (input.aiProvenance ?? null) as unknown as Prisma.InputJsonValue,
        state: 'draft',
      },
    });
  }

  async transition(
    tenantId: string,
    digestId: string,
    to: DigestState,
    actorId: string,
  ) {
    const d = await this.prisma.agentDailyDigest.findFirst({
      where: { id: digestId, tenantId },
    });
    if (!d) throw new NotFoundException('Digest not found.');
    const from = d.state as DigestState;
    if (!AgentDigestService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'published') {
      const summary = d.summaryI18n as unknown as Record<string, string>;
      const check = validateSummary(summary);
      if (!check.ok) {
        throw new BadRequestException({
          error: 'Digest summary did not pass plain-language validation.',
          items: check.errors,
        });
      }
    }
    return this.prisma.agentDailyDigest.update({
      where: { id: digestId },
      data: {
        state: to,
        ...(to === 'published'
          ? {
              approvedAt: new Date(),
              approvedBy: actorId,
              publishedAt: new Date(),
            }
          : {}),
      },
    });
  }
}
