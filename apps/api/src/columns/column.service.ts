import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { tally, type RequestRecord, type Sensitivity } from './approval-tally';

export interface ColumnDraftInput {
  tenantId: string;
  authorId?: string;
  primaryLocale: string;
  bodyI18n: Record<string, { title: string; summary: string; excerpt?: string }>;
  sourceUrl: string;
  sourceTitle?: string;
  sourceAuthors?: string[];
  sourcePublisher?: string;
  sourceLicense?: string;
  sdgFocus: string[];
  sdgConfidence?: number;
  sensitivity?: Sensitivity;
  aiProvenance?: { model: string; promptVersion: string; draftedAt: string };
}

@Injectable()
export class ColumnService {
  constructor(private readonly prisma: PrismaService) {}

  // Eligibility check per CONTENT_STANDARD.md §8 — surfaced in plain words.
  static eligibilityErrors(input: ColumnDraftInput): string[] {
    const errors: string[] = [];
    if (!input.sourceUrl) errors.push('A source URL is required.');
    if ((input.sdgFocus ?? []).length === 0) {
      errors.push('At least one SDG mapping is required.');
    }
    if (input.sdgConfidence !== undefined && input.sdgConfidence < 0.7) {
      errors.push('SDG mapping confidence below 0.70 needs human confirmation.');
    }
    const primaryBody = input.bodyI18n[input.primaryLocale];
    if (!primaryBody) {
      errors.push(`A summary in the primary locale (${input.primaryLocale}) is required.`);
    } else {
      if (!primaryBody.title) errors.push('Title is missing.');
      if (!primaryBody.summary) errors.push('Plain-language summary is missing.');
      if (primaryBody.excerpt && primaryBody.excerpt.split(/\s+/).length > 250) {
        errors.push('Original-text excerpt must be 250 words or fewer.');
      }
    }
    return errors;
  }

  async createDraft(input: ColumnDraftInput) {
    const errors = ColumnService.eligibilityErrors(input);
    if (errors.length > 0) {
      throw new BadRequestException({
        error: 'Column draft does not meet the content standard.',
        items: errors,
      });
    }
    return this.prisma.column.create({
      data: {
        tenantId: input.tenantId,
        ...(input.authorId !== undefined ? { authorId: input.authorId } : {}),
        state: 'draft',
        primaryLocale: input.primaryLocale,
        bodyI18n: input.bodyI18n as Prisma.InputJsonValue,
        sourceUrl: input.sourceUrl,
        ...(input.sourceTitle !== undefined ? { sourceTitle: input.sourceTitle } : {}),
        sourceAuthors: input.sourceAuthors ?? [],
        ...(input.sourcePublisher !== undefined ? { sourcePublisher: input.sourcePublisher } : {}),
        ...(input.sourceLicense !== undefined ? { sourceLicense: input.sourceLicense } : {}),
        sdgFocus: input.sdgFocus,
        ...(input.sdgConfidence !== undefined ? { sdgConfidence: input.sdgConfidence } : {}),
        sensitivity: input.sensitivity ?? 'standard',
        ...(input.aiProvenance !== undefined
          ? { aiProvenance: input.aiProvenance as unknown as Prisma.InputJsonValue }
          : {}),
      },
    });
  }

  async submitForApproval(tenantId: string, columnId: string, approverIds: string[]) {
    if (approverIds.length === 0) {
      throw new BadRequestException('At least one approver is required.');
    }
    const column = await this.prisma.column.findFirst({
      where: { id: columnId, tenantId },
    });
    if (!column) throw new NotFoundException('Column not found.');
    if (column.state !== 'draft') {
      throw new ConflictException(`Cannot submit a column in state '${column.state}'.`);
    }
    const expiresAt = new Date(Date.now() + 72 * 60 * 60 * 1000);

    return this.prisma.$transaction(async (tx) => {
      await tx.column.update({
        where: { id: columnId },
        data: { state: 'pending', submittedAt: new Date() },
      });
      await tx.approvalRequest.createMany({
        data: approverIds.map((approverId) => ({
          tenantId,
          columnId,
          approverId,
          channel: 'email',
          expiresAt,
        })),
      });
      return tx.approvalRequest.findMany({
        where: { tenantId, columnId },
      });
    });
  }

  async recordDecision(
    requestId: string,
    decision: 'approve' | 'reject' | 'revise',
    decidedVia: string,
    reason?: string,
  ) {
    const req = await this.prisma.approvalRequest.findUnique({
      where: { id: requestId },
    });
    if (!req) throw new NotFoundException('Approval request not found.');
    if (req.decision) {
      throw new ConflictException('This approval request has already been decided.');
    }
    if (req.expiresAt.getTime() < Date.now()) {
      throw new ConflictException('This approval request has expired.');
    }
    await this.prisma.approvalRequest.update({
      where: { id: requestId },
      data: {
        decision,
        decidedAt: new Date(),
        decidedVia,
        ...(reason !== undefined ? { reasonNote: reason } : {}),
      },
    });
    return this.tallyAndAdvance(req.tenantId, req.columnId);
  }

  async tallyAndAdvance(tenantId: string, columnId: string) {
    const column = await this.prisma.column.findFirst({
      where: { id: columnId, tenantId },
    });
    if (!column) throw new NotFoundException('Column not found.');
    const requests = await this.prisma.approvalRequest.findMany({
      where: { columnId },
    });
    const approverIds = requests.map((r) => r.approverId);
    const approvers = await this.prisma.columnApprover.findMany({
      where: { id: { in: approverIds } },
    });
    const sensitiveOkById = new Map(approvers.map((a) => [a.id, a.sensitiveOk]));

    const records: RequestRecord[] = requests.map((r) => ({
      decision: r.decision as RequestRecord['decision'],
      approverIsSensitiveOk: sensitiveOkById.get(r.approverId) ?? false,
    }));
    const outcome = tally(column.sensitivity as Sensitivity, records);

    if (outcome.result === 'publish' && column.state !== 'published') {
      await this.prisma.column.update({
        where: { id: columnId },
        data: { state: 'published', publishedAt: new Date() },
      });
    } else if (outcome.result === 'reject' && column.state !== 'rejected') {
      await this.prisma.column.update({
        where: { id: columnId },
        data: { state: 'rejected' },
      });
    } else if (outcome.result === 'revise' && column.state !== 'draft') {
      await this.prisma.column.update({
        where: { id: columnId },
        data: { state: 'draft' },
      });
    }
    return outcome;
  }

  async listPublished(filter: { since?: Date; locale?: string; take?: number } = {}) {
    return this.prisma.column.findMany({
      where: {
        state: 'published',
        ...(filter.since ? { publishedAt: { gte: filter.since } } : {}),
      },
      orderBy: { publishedAt: 'desc' },
      take: filter.take ?? 30,
    });
  }

  async getPublishedById(id: string) {
    const c = await this.prisma.column.findFirst({
      where: { id, state: 'published' },
    });
    if (!c) throw new NotFoundException('Column not found or not published.');
    return c;
  }
}
