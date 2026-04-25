import { describe, expect, it, vi } from 'vitest';
import { ForbiddenException, type ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { RolesGuard } from './roles.guard';
import type { PrismaService } from '../prisma/prisma.service';
import type { AuthenticatedRequest } from './jwt-auth.guard';

function ctx(req: Partial<AuthenticatedRequest>, required: string[] | undefined): ExecutionContext {
  const reflector = new Reflector();
  vi.spyOn(reflector, 'getAllAndOverride').mockReturnValue(required);
  return {
    _reflector: reflector,
    getHandler: () => () => undefined,
    getClass: () => class {},
    switchToHttp: () => ({ getRequest: <T>() => req as T }),
  } as unknown as ExecutionContext & { _reflector: Reflector };
}

function makePrisma(roleKeys: string[]): PrismaService {
  return {
    membership: {
      findMany: vi.fn().mockResolvedValue(
        roleKeys.map((key) => ({ role: { key } })),
      ),
    },
  } as unknown as PrismaService;
}

describe('RolesGuard', () => {
  it('passes through when no roles are required', async () => {
    const reflector = new Reflector();
    vi.spyOn(reflector, 'getAllAndOverride').mockReturnValue(undefined);
    const guard = new RolesGuard(reflector, makePrisma([]));
    const result = await guard.canActivate({
      getHandler: () => () => undefined,
      getClass: () => class {},
      switchToHttp: () =>
        ({
          getRequest: () => ({ auth: { userId: 'u', tenantId: 't' } }) as AuthenticatedRequest,
        }) as never,
    } as unknown as ExecutionContext);
    expect(result).toBe(true);
  });

  it('forbids when authentication context is missing', async () => {
    const reflector = new Reflector();
    vi.spyOn(reflector, 'getAllAndOverride').mockReturnValue(['admin']);
    const guard = new RolesGuard(reflector, makePrisma([]));
    await expect(
      guard.canActivate({
        getHandler: () => () => undefined,
        getClass: () => class {},
        switchToHttp: () => ({ getRequest: () => ({}) as AuthenticatedRequest }) as never,
      } as unknown as ExecutionContext),
    ).rejects.toBeInstanceOf(ForbiddenException);
  });

  it('allows when user has one of the required roles', async () => {
    const reflector = new Reflector();
    vi.spyOn(reflector, 'getAllAndOverride').mockReturnValue(['admin', 'reviewer']);
    const guard = new RolesGuard(reflector, makePrisma(['contributor', 'reviewer']));
    const result = await guard.canActivate({
      getHandler: () => () => undefined,
      getClass: () => class {},
      switchToHttp: () =>
        ({
          getRequest: () => ({ auth: { userId: 'u', tenantId: 't' } }) as AuthenticatedRequest,
        }) as never,
    } as unknown as ExecutionContext);
    expect(result).toBe(true);
  });

  it('forbids when user lacks all required roles', async () => {
    const reflector = new Reflector();
    vi.spyOn(reflector, 'getAllAndOverride').mockReturnValue(['admin']);
    const guard = new RolesGuard(reflector, makePrisma(['viewer']));
    await expect(
      guard.canActivate({
        getHandler: () => () => undefined,
        getClass: () => class {},
        switchToHttp: () =>
          ({
            getRequest: () =>
              ({ auth: { userId: 'u', tenantId: 't' } }) as AuthenticatedRequest,
          }) as never,
      } as unknown as ExecutionContext),
    ).rejects.toBeInstanceOf(ForbiddenException);
  });
});
