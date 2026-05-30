import { describe, expect, it, vi } from 'vitest';
import { of, lastValueFrom, type Observable } from 'rxjs';
import type { CallHandler, ExecutionContext } from '@nestjs/common';
import { AuditInterceptor } from './audit.interceptor';
import type { AuditService } from './audit.service';

function makeContext(method: string, path: string, auth?: { userId: string; tenantId: string }): ExecutionContext {
  return {
    switchToHttp: () => ({
      getRequest: () => ({
        method,
        path,
        auth,
      }),
    }),
  } as unknown as ExecutionContext;
}

function makeNext(): CallHandler {
  return {
    handle: (): Observable<unknown> => of({ ok: true }),
  };
}

describe('AuditInterceptor', () => {
  it('records on POST /v1/activities', async () => {
    const audit = { record: vi.fn().mockResolvedValue(undefined) } as unknown as AuditService;
    const interceptor = new AuditInterceptor(audit);
    const ctx = makeContext('POST', '/v1/activities', { userId: 'u', tenantId: 't' });
    await lastValueFrom(interceptor.intercept(ctx, makeNext()));
    expect(audit.record).toHaveBeenCalledOnce();
    const call = (audit.record as unknown as { mock: { calls: unknown[][] } }).mock.calls[0]?.[0] as {
      action: string;
      resourceType: string;
      tenantId: string | null;
      actorId: string | null;
    };
    expect(call.action).toBe('POST /v1/activities');
    expect(call.resourceType).toBe('activities');
    expect(call.tenantId).toBe('t');
    expect(call.actorId).toBe('u');
  });

  it('does not record GETs', async () => {
    const audit = { record: vi.fn() } as unknown as AuditService;
    const interceptor = new AuditInterceptor(audit);
    await lastValueFrom(
      interceptor.intercept(makeContext('GET', '/v1/catalog/goals'), makeNext()),
    );
    expect(audit.record).not.toHaveBeenCalled();
  });

  it('skips signin/signup/signout', async () => {
    const audit = { record: vi.fn() } as unknown as AuditService;
    const interceptor = new AuditInterceptor(audit);
    await lastValueFrom(interceptor.intercept(makeContext('POST', '/v1/auth/signin'), makeNext()));
    await lastValueFrom(interceptor.intercept(makeContext('POST', '/v1/auth/signup'), makeNext()));
    expect(audit.record).not.toHaveBeenCalled();
  });
});
