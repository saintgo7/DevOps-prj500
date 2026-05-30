import { describe, expect, it, vi } from 'vitest';
import type { NextFunction, Request, Response } from 'express';
import { TenantContextMiddleware } from './tenant-context.middleware';

function makeReq(headers: Record<string, string>): Request {
  return {
    header(name: string): string | undefined {
      return headers[name.toLowerCase()];
    },
  } as unknown as Request;
}

describe('TenantContextMiddleware', () => {
  it('sets tenantId when header is a valid UUID', () => {
    const middleware = new TenantContextMiddleware();
    const valid = 'b8c8a3a0-2c4f-4e9b-8b9a-1e2c3d4e5f60';
    const req = makeReq({ 'x-tenant-id': valid });
    const next = vi.fn() as unknown as NextFunction;
    middleware.use(req, {} as Response, next);
    expect(req.tenantId).toBe(valid);
    expect(next).toHaveBeenCalledOnce();
  });

  it('does not set tenantId when header is missing', () => {
    const middleware = new TenantContextMiddleware();
    const req = makeReq({});
    const next = vi.fn() as unknown as NextFunction;
    middleware.use(req, {} as Response, next);
    expect(req.tenantId).toBeUndefined();
    expect(next).toHaveBeenCalledOnce();
  });

  it('does not set tenantId when header is not a UUID', () => {
    const middleware = new TenantContextMiddleware();
    const req = makeReq({ 'x-tenant-id': 'not-a-uuid' });
    const next = vi.fn() as unknown as NextFunction;
    middleware.use(req, {} as Response, next);
    expect(req.tenantId).toBeUndefined();
    expect(next).toHaveBeenCalledOnce();
  });
});
