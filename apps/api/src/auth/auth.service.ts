import {
  ConflictException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import argon2 from 'argon2';
import { PrismaService } from '../prisma/prisma.service';
import type { SignInDto, SignUpDto, UserDto } from './dto';

const SESSION_TTL_SECONDS = 60 * 60 * 8; // 8 hours

export interface IssuedSession {
  user: UserDto;
  token: string;
  expiresAt: Date;
}

@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly jwt: JwtService,
  ) {}

  async signUp(dto: SignUpDto): Promise<IssuedSession> {
    const existing = await this.prisma.user.findFirst({ where: { email: dto.email } });
    if (existing) throw new ConflictException('Email already registered');

    const adminRole = await this.prisma.role.findUnique({ where: { key: 'admin' } });
    if (!adminRole) {
      // Roles are seeded — this is a setup error, not user error.
      throw new Error('Role "admin" not seeded. Run prisma db seed.');
    }

    const tenantName = dto.organizationName ?? `${dto.email.split('@')[1] ?? 'workspace'}`;
    const passwordHash = await argon2.hash(dto.password, { type: argon2.argon2id });

    const user = await this.prisma.$transaction(async (tx) => {
      const tenant = await tx.tenant.create({ data: { name: tenantName } });
      const created = await tx.user.create({
        data: {
          tenantId: tenant.id,
          email: dto.email,
          ...(dto.displayName !== undefined ? { displayName: dto.displayName } : {}),
          passwordHash,
          authProvider: 'local',
        },
      });
      await tx.membership.create({
        data: { tenantId: tenant.id, userId: created.id, roleId: adminRole.id },
      });
      return created;
    });

    return this.issueSession(user);
  }

  async signIn(dto: SignInDto): Promise<IssuedSession> {
    const user = await this.prisma.user.findFirst({ where: { email: dto.email } });
    if (!user || !user.passwordHash) {
      throw new UnauthorizedException('Invalid credentials');
    }
    const ok = await argon2.verify(user.passwordHash, dto.password);
    if (!ok) throw new UnauthorizedException('Invalid credentials');
    if (user.status !== 'active') throw new UnauthorizedException('Account inactive');
    return this.issueSession(user);
  }

  async getMe(userId: string): Promise<UserDto> {
    const user = await this.prisma.user.findUnique({ where: { id: userId } });
    if (!user) throw new UnauthorizedException('Session invalid');
    return this.toDto(user);
  }

  private async issueSession(user: {
    id: string;
    tenantId: string;
    email: string;
    displayName: string | null;
    status: string;
    mfaEnabled: boolean;
  }): Promise<IssuedSession> {
    const token = await this.jwt.signAsync(
      { sub: user.id, tid: user.tenantId },
      { expiresIn: SESSION_TTL_SECONDS },
    );
    return {
      user: this.toDto(user),
      token,
      expiresAt: new Date(Date.now() + SESSION_TTL_SECONDS * 1000),
    };
  }

  private toDto(user: {
    id: string;
    tenantId: string;
    email: string;
    displayName: string | null;
    status: string;
    mfaEnabled: boolean;
  }): UserDto {
    return {
      id: user.id,
      tenantId: user.tenantId,
      email: user.email,
      ...(user.displayName !== null ? { displayName: user.displayName } : {}),
      status: user.status,
      mfaEnabled: user.mfaEnabled,
    };
  }
}
