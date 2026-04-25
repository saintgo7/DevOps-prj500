import { Injectable, Logger } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export interface AuditWriteInput {
  tenantId: string | null;
  actorId: string | null;
  action: string;
  resourceType: string;
  resourceId?: string | null;
  before?: unknown;
  after?: unknown;
}

@Injectable()
export class AuditService {
  private readonly logger = new Logger(AuditService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Append an audit event. Failures are swallowed (logged) so that the
   * primary request is never broken by audit-log issues — but in production
   * we still surface them to observability.
   */
  async record(event: AuditWriteInput): Promise<void> {
    try {
      await this.prisma.auditEvent.create({
        data: {
          tenantId: event.tenantId,
          actorId: event.actorId,
          action: event.action,
          resourceType: event.resourceType,
          resourceId: event.resourceId ?? null,
          before:
            event.before === undefined
              ? Prisma.JsonNull
              : (event.before as Prisma.InputJsonValue),
          after:
            event.after === undefined
              ? Prisma.JsonNull
              : (event.after as Prisma.InputJsonValue),
        },
      });
    } catch (err) {
      this.logger.error(
        `audit write failed: action=${event.action} resource=${event.resourceType}`,
        err instanceof Error ? err.stack : String(err),
      );
    }
  }
}
