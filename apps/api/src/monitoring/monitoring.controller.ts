import { Controller, Get, Query, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import { AuditService } from '../audit/audit.service';
import { MonitoringService, type MonitoringSnapshot } from './monitoring.service';

// Admin-only: a holistic view across content integrity, approvals, partners,
// research, outreach, and the watch pipeline. Every snapshot read is itself
// recorded in the audit log — see ADR-0014 §"Equity / trust / dignity".
@ApiTags('monitoring')
@Controller('monitoring')
export class MonitoringController {
  constructor(
    private readonly monitoring: MonitoringService,
    private readonly audit: AuditService,
  ) {}

  @Get('snapshot')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Admin-only monitoring snapshot (audit-logged on every read)',
    description:
      'Returns publication counts, approval timing, partner delivery health, ' +
      'research/outreach queues, watch-pipeline status, and the integrity-rule ' +
      'failure histogram. Reading this endpoint records an audit event.',
  })
  async snapshot(
    @Req() req: Request,
    @Query('days') daysParam?: string,
  ): Promise<MonitoringSnapshot> {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const days = Math.max(1, Math.min(180, Number(daysParam) || 30));
    const snap = await this.monitoring.snapshot(auth.tenantId, days);
    await this.audit.record({
      tenantId: auth.tenantId,
      actorId: auth.userId,
      action: 'monitoring.snapshot.read',
      resourceType: 'monitoring',
      resourceId: 'snapshot',
      after: { windowDays: days, generatedAt: snap.generatedAt },
    });
    return snap;
  }
}
