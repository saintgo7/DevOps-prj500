import { describe, expect, it, vi } from 'vitest';
import { UnauthorizedException, type ExecutionContext } from '@nestjs/common';
import type { JwtService } from '@nestjs/jwt';
import { JwtAuthGuard, type AuthenticatedRequest } from './jwt-auth.guard';

function ctx(req: Partial<AuthenticatedRequest>): ExecutionContext {
  return {
    switchToHttp: () => ({ getRequest: <T>() => req as T }),
  } as unknown as ExecutionContext;
}

describe('JwtAuthGuard', () => {
  it('rejects when no token provided', async () => {
    const jwt = { verifyAsync: vi.fn() } as unknown as JwtService;
    const guard = new JwtAuthGuard(jwt);
    await expect(
      guard.canActivate(ctx({ header: () => undefined } as Partial<AuthenticatedRequest>)),
    ).rejects.toBeInstanceOf(UnauthorizedException);
  });

  it('extracts token from cookie and sets req.auth', async () => {
    const jwt = {
      verifyAsync: vi.fn().mockResolvedValue({ sub: 'u1', tid: 't1' }),
    } as unknown as JwtService;
    const guard = new JwtAuthGuard(jwt);
    const req = {
      cookies: { sdgi_session: 'cookie-token' },
      header: () => undefined,
    } as unknown as AuthenticatedRequest;
    await guard.canActivate(ctx(req));
    expect(req.auth).toEqual({ userId: 'u1', tenantId: 't1' });
    expect(jwt.verifyAsync).toHaveBeenCalledWith('cookie-token');
  });

  it('extracts token from Authorization header (Bearer)', async () => {
    const jwt = {
      verifyAsync: vi.fn().mockResolvedValue({ sub: 'u2', tid: 't2' }),
    } as unknown as JwtService;
    const guard = new JwtAuthGuard(jwt);
    const headers: Record<string, string> = { authorization: 'Bearer header-token' };
    const req = {
      header: (name: string) => headers[name.toLowerCase()],
    } as unknown as AuthenticatedRequest;
    await guard.canActivate(ctx(req));
    expect(req.auth).toEqual({ userId: 'u2', tenantId: 't2' });
  });

  it('rejects when JWT verification fails', async () => {
    const jwt = {
      verifyAsync: vi.fn().mockRejectedValue(new Error('expired')),
    } as unknown as JwtService;
    const guard = new JwtAuthGuard(jwt);
    const req = {
      cookies: { sdgi_session: 'bad' },
      header: () => undefined,
    } as unknown as AuthenticatedRequest;
    await expect(guard.canActivate(ctx(req))).rejects.toBeInstanceOf(UnauthorizedException);
  });
});
