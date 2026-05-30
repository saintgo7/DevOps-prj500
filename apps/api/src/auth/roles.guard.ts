import {
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PrismaService } from '../prisma/prisma.service';
import { ROLES_METADATA_KEY, type RoleKey } from './roles.decorator';
import type { AuthenticatedRequest } from './jwt-auth.guard';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(
    private readonly reflector: Reflector,
    private readonly prisma: PrismaService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const required = this.reflector.getAllAndOverride<RoleKey[] | undefined>(
      ROLES_METADATA_KEY,
      [context.getHandler(), context.getClass()],
    );
    if (!required || required.length === 0) return true;

    const req = context.switchToHttp().getRequest<AuthenticatedRequest>();
    const auth = req.auth;
    if (!auth) {
      // RolesGuard relies on JwtAuthGuard having run first. If it hasn't, fail closed.
      throw new ForbiddenException('Missing authentication context');
    }

    const memberships = await this.prisma.membership.findMany({
      where: { userId: auth.userId, tenantId: auth.tenantId },
      include: { role: true },
    });
    const userRoles = new Set(memberships.map((m) => m.role.key as RoleKey));
    const hasRole = required.some((r) => userRoles.has(r));
    if (!hasRole) {
      throw new ForbiddenException(
        `Requires one of: ${required.join(', ')}; user has: ${[...userRoles].join(', ') || 'none'}`,
      );
    }
    return true;
  }
}
