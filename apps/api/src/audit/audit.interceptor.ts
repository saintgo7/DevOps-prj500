import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';
import type { Request } from 'express';
import { AuditService } from './audit.service';
import type { AuthenticatedRequest } from '../auth/jwt-auth.guard';

const MUTATING_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);
const SKIP_PATHS = ['/v1/auth/signin', '/v1/auth/signup', '/v1/auth/signout'];

/**
 * Records an audit event for every successful mutation. We log only metadata
 * (method, path, ids) — payloads may include secrets/PII and are filtered
 * out at this layer. Per-resource audit (with before/after diffs) is added
 * inside individual services using `AuditService.record` directly.
 */
@Injectable()
export class AuditInterceptor implements NestInterceptor {
  constructor(private readonly audit: AuditService) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const req = context.switchToHttp().getRequest<Request & AuthenticatedRequest>();
    const method = req.method.toUpperCase();
    const path = req.path;
    const shouldRecord =
      MUTATING_METHODS.has(method) && !SKIP_PATHS.some((p) => path.startsWith(p));

    return next.handle().pipe(
      tap(() => {
        if (!shouldRecord) return;
        void this.audit.record({
          tenantId: req.auth?.tenantId ?? req.tenantId ?? null,
          actorId: req.auth?.userId ?? null,
          action: `${method} ${path}`,
          resourceType: deriveResourceType(path),
        });
      }),
    );
  }
}

function deriveResourceType(path: string): string {
  // /v1/activities/abc/data-points → "activities"
  const parts = path.split('/').filter(Boolean);
  if (parts[0] === 'v1' && parts[1]) return parts[1];
  return parts[0] ?? 'unknown';
}
