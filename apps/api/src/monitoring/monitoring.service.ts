import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface MonitoringSnapshot {
  generatedAt: string;
  windowDays: number;
  columns: {
    publishedExternal: number;
    publishedInternal: number;
    pending: number;
    rejected: number;
    revoked: number;
  };
  approvals: {
    pendingRequests: number;
    expiredUnusedRequests: number;
    avgDecisionMinutes: number | null;
  };
  partners: {
    activeWebhooks: number;
    last24hFailures: number;
  };
  research: {
    drafts: number;
    inReview: number;
    approved: number;
  };
  outreach: {
    drafts: number;
    sent: number;
    declined: number;
  };
  watch: {
    activeSources: number;
    itemsLastWindow: number;
  };
  /** Eligibility-rule failure histogram of the most recent N candidates. */
  integrityRuleFailureHistogram: Record<string, number>;
}

@Injectable()
export class MonitoringService {
  constructor(private readonly prisma: PrismaService) {}

  async snapshot(tenantId: string, windowDays = 30): Promise<MonitoringSnapshot> {
    const since = new Date(Date.now() - windowDays * 86400 * 1000);

    const [
      publishedExternal,
      publishedInternal,
      pending,
      rejected,
      revoked,
      pendingRequests,
      expired,
      decided,
      activeWebhooks,
      partnerFailures,
      researchDraft,
      researchReview,
      researchApproved,
      outreachDraft,
      outreachSent,
      outreachDeclined,
      activeSources,
      watchItems,
      recentColumnsForHistogram,
    ] = await Promise.all([
      this.prisma.column.count({
        where: { tenantId, state: 'published', origin: 'external', publishedAt: { gte: since } },
      }),
      this.prisma.column.count({
        where: { tenantId, state: 'published', origin: 'internal', publishedAt: { gte: since } },
      }),
      this.prisma.column.count({ where: { tenantId, state: 'pending' } }),
      this.prisma.column.count({
        where: { tenantId, state: 'rejected', createdAt: { gte: since } },
      }),
      this.prisma.column.count({
        where: { tenantId, state: 'revoked', revokedAt: { gte: since } },
      }),
      this.prisma.approvalRequest.count({
        where: { tenantId, decision: null, expiresAt: { gt: new Date() } },
      }),
      this.prisma.approvalRequest.count({
        where: { tenantId, decision: null, expiresAt: { lte: new Date() } },
      }),
      this.prisma.approvalRequest.findMany({
        where: { tenantId, decidedAt: { not: null }, createdAt: { gte: since } },
        select: { createdAt: true, decidedAt: true },
      }),
      this.prisma.partnerWebhook.count({ where: { active: true } }),
      this.prisma.partnerWebhook.count({
        where: {
          active: true,
          lastDeliveredAt: { gte: new Date(Date.now() - 86400 * 1000) },
          lastStatus: { gte: 400 },
        },
      }),
      this.prisma.researchProposal.count({ where: { tenantId, state: 'draft' } }),
      this.prisma.researchProposal.count({ where: { tenantId, state: 'review' } }),
      this.prisma.researchProposal.count({ where: { tenantId, state: 'approved' } }),
      this.prisma.expertOutreach.count({ where: { tenantId, state: 'draft' } }),
      this.prisma.expertOutreach.count({ where: { tenantId, state: 'sent' } }),
      this.prisma.expertOutreach.count({ where: { tenantId, state: 'declined' } }),
      this.prisma.watchSource.count({ where: { active: true } }),
      this.prisma.watchItem.count({ where: { discoveredAt: { gte: since } } }),
      this.prisma.column.findMany({
        where: { tenantId, createdAt: { gte: since } },
        select: { integrityReport: true },
        take: 200,
      }),
    ]);

    // Average minutes-to-decision (decidedAt - createdAt) over the window.
    const decidedDurations = decided
      .filter((d) => d.decidedAt)
      .map((d) => (d.decidedAt!.getTime() - d.createdAt.getTime()) / 60_000);
    const avgDecisionMinutes =
      decidedDurations.length > 0
        ? Math.round(
            decidedDurations.reduce((a, b) => a + b, 0) / decidedDurations.length,
          )
        : null;

    // Build the rule-failure histogram from recent column integrity reports.
    const histogram: Record<string, number> = {};
    for (const c of recentColumnsForHistogram) {
      const report = c.integrityReport as
        | { results?: { rule: string; ok: boolean }[] }
        | null;
      if (!report?.results) continue;
      for (const r of report.results) {
        if (!r.ok) histogram[r.rule] = (histogram[r.rule] ?? 0) + 1;
      }
    }

    return {
      generatedAt: new Date().toISOString(),
      windowDays,
      columns: {
        publishedExternal,
        publishedInternal,
        pending,
        rejected,
        revoked,
      },
      approvals: {
        pendingRequests,
        expiredUnusedRequests: expired,
        avgDecisionMinutes,
      },
      partners: {
        activeWebhooks,
        last24hFailures: partnerFailures,
      },
      research: {
        drafts: researchDraft,
        inReview: researchReview,
        approved: researchApproved,
      },
      outreach: {
        drafts: outreachDraft,
        sent: outreachSent,
        declined: outreachDeclined,
      },
      watch: {
        activeSources,
        itemsLastWindow: watchItems,
      },
      integrityRuleFailureHistogram: histogram,
    };
  }
}
