import { describe, expect, it, vi } from 'vitest';
import type { NextFunction, Request, Response } from 'express';
import { RequestIdMiddleware } from './request-id.middleware';

function makeReq(header: string | undefined): Request {
  return {
    header(name: string): string | undefined {
      return name.toLowerCase() === 'x-request-id' ? header : undefined;
    },
  } as unknown as Request;
}

function makeRes(): Response & { _headers: Record<string, string> } {
  const headers: Record<string, string> = {};
  return {
    _headers: headers,
    setHeader(name: string, value: string): void {
      headers[name.toLowerCase()] = value;
    },
  } as unknown as Response & { _headers: Record<string, string> };
}

describe('RequestIdMiddleware', () => {
  it('generates a UUID when no header is sent', () => {
    const req = makeReq(undefined);
    const res = makeRes();
    new RequestIdMiddleware().use(req, res, vi.fn() as unknown as NextFunction);
    expect(req.requestId).toMatch(/[0-9a-f-]{36}/i);
    expect(res._headers['x-request-id']).toBe(req.requestId);
  });

  it('reuses incoming request id when valid', () => {
    const req = makeReq('req-abcd-1234-5678');
    const res = makeRes();
    new RequestIdMiddleware().use(req, res, vi.fn() as unknown as NextFunction);
    expect(req.requestId).toBe('req-abcd-1234-5678');
  });

  it('rejects malicious header by generating fresh id', () => {
    const req = makeReq('a b c');
    const res = makeRes();
    new RequestIdMiddleware().use(req, res, vi.fn() as unknown as NextFunction);
    expect(req.requestId).not.toBe('a b c');
    expect(req.requestId).toMatch(/[0-9a-f-]{36}/i);
  });
});
