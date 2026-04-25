import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';
import type { Request, Response } from 'express';
import { httpRequestDuration } from './metrics.controller';

@Injectable()
export class MetricsInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const http = context.switchToHttp();
    const req = http.getRequest<Request>();
    const res = http.getResponse<Response>();
    const start = process.hrtime.bigint();

    const route = req.route?.path ?? req.path;

    return next.handle().pipe(
      tap({
        next: () => recordDuration(start, req.method, route, res.statusCode),
        error: () => recordDuration(start, req.method, route, res.statusCode || 500),
      }),
    );
  }
}

function recordDuration(start: bigint, method: string, route: string, status: number): void {
  const elapsedNs = Number(process.hrtime.bigint() - start);
  httpRequestDuration
    .labels({ method, route, status: String(status) })
    .observe(elapsedNs / 1e9);
}
