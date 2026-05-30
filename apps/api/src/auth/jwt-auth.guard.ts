import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import type { Request } from 'express';

export interface AuthenticatedRequest extends Request {
  auth?: { userId: string; tenantId: string };
}

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private readonly jwt: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const req = context.switchToHttp().getRequest<AuthenticatedRequest>();
    const token = this.extractToken(req);
    if (!token) throw new UnauthorizedException('Missing session');
    try {
      const payload = await this.jwt.verifyAsync<{ sub: string; tid: string }>(token);
      req.auth = { userId: payload.sub, tenantId: payload.tid };
      // Also expose tenantId so the existing TenantContextMiddleware-based flow works.
      (req as Request).tenantId = payload.tid;
      return true;
    } catch {
      throw new UnauthorizedException('Session invalid or expired');
    }
  }

  private extractToken(req: AuthenticatedRequest): string | undefined {
    const cookies = (req as unknown as { cookies?: Record<string, string> }).cookies;
    if (cookies?.['sdgi_session']) return cookies['sdgi_session'];
    const auth = req.header('authorization');
    if (auth?.startsWith('Bearer ')) return auth.slice(7);
    return undefined;
  }
}
