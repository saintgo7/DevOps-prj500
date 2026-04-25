import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';
import { Observable, from, mergeMap, of } from 'rxjs';
import type { Request } from 'express';
import { PrismaService } from '../prisma/prisma.service';

/**
 * For each HTTP request, set Postgres session var `app.tenant_id`
 * inside a transaction so RLS policies select the correct tenant rows.
 *
 * Future: switch to Prisma transactional context once stable for our use.
 * For now this interceptor is wired only on routes that touch RLS tables.
 */
@Injectable()
export class PrismaTenantInterceptor implements NestInterceptor {
  constructor(private readonly prisma: PrismaService) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const req = context.switchToHttp().getRequest<Request>();
    const tenantId = req.tenantId;
    if (!tenantId) {
      return next.handle();
    }
    return from(
      this.prisma.$executeRawUnsafe(`SELECT set_config('app.tenant_id', $1, true)`, tenantId),
    ).pipe(mergeMap(() => next.handle() ?? of(undefined)));
  }
}
