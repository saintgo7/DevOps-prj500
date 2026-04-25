import { describe, expect, it, vi } from 'vitest';
import { ConflictException, UnauthorizedException } from '@nestjs/common';
import argon2 from 'argon2';
import { AuthService } from './auth.service';
import type { PrismaService } from '../prisma/prisma.service';
import type { JwtService } from '@nestjs/jwt';

const TENANT_ID = 'b8c8a3a0-2c4f-4e9b-8b9a-1e2c3d4e5f60';
const USER_ID = 'd1d1d1d1-1111-2222-3333-444444444444';

interface FakeStore {
  users: Array<{
    id: string;
    tenantId: string;
    email: string;
    displayName: string | null;
    passwordHash: string | null;
    status: string;
    mfaEnabled: boolean;
  }>;
}

function makePrisma(store: FakeStore): PrismaService {
  return {
    user: {
      findFirst: vi.fn(({ where }: { where: { email: string } }) =>
        Promise.resolve(store.users.find((u) => u.email === where.email) ?? null),
      ),
      findUnique: vi.fn(({ where }: { where: { id: string } }) =>
        Promise.resolve(store.users.find((u) => u.id === where.id) ?? null),
      ),
    },
    role: {
      findUnique: vi.fn().mockResolvedValue({ id: 'role-admin', key: 'admin', name: 'Admin' }),
    },
    tenant: {
      create: vi.fn().mockResolvedValue({ id: TENANT_ID, name: 'Acme' }),
    },
    membership: {
      create: vi.fn().mockResolvedValue({}),
    },
    $transaction: vi.fn(async (fn: (tx: unknown) => Promise<unknown>) => {
      // Simulate Prisma's interactive transaction by passing a tx that mimics the
      // top-level client surface used in the AuthService.
      const tx = {
        tenant: { create: vi.fn().mockResolvedValue({ id: TENANT_ID, name: 'Acme' }) },
        user: {
          create: vi.fn(({ data }: { data: { email: string; displayName?: string; passwordHash: string } }) => {
            const created = {
              id: USER_ID,
              tenantId: TENANT_ID,
              email: data.email,
              displayName: data.displayName ?? null,
              passwordHash: data.passwordHash,
              status: 'active',
              mfaEnabled: false,
            };
            store.users.push(created);
            return Promise.resolve(created);
          }),
        },
        membership: { create: vi.fn().mockResolvedValue({}) },
      };
      return fn(tx);
    }),
  } as unknown as PrismaService;
}

function makeJwt(): JwtService {
  return {
    signAsync: vi.fn().mockResolvedValue('signed.jwt.token'),
    verifyAsync: vi.fn(),
  } as unknown as JwtService;
}

describe('AuthService', () => {
  it('signs up a new user, creates tenant, returns session', async () => {
    const store: FakeStore = { users: [] };
    const svc = new AuthService(makePrisma(store), makeJwt());
    const session = await svc.signUp({
      email: 'jisoo@example.com',
      password: 'a-strong-passphrase-12+',
      displayName: '박지수',
    });
    expect(session.user.email).toBe('jisoo@example.com');
    expect(session.user.tenantId).toBe(TENANT_ID);
    expect(session.token).toBe('signed.jwt.token');
    expect(store.users[0]?.passwordHash?.startsWith('$argon2')).toBe(true);
  });

  it('rejects signup when email already exists', async () => {
    const store: FakeStore = {
      users: [
        {
          id: USER_ID,
          tenantId: TENANT_ID,
          email: 'existing@example.com',
          displayName: null,
          passwordHash: 'irrelevant',
          status: 'active',
          mfaEnabled: false,
        },
      ],
    };
    const svc = new AuthService(makePrisma(store), makeJwt());
    await expect(
      svc.signUp({ email: 'existing@example.com', password: 'a-strong-passphrase-12+' }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('signs in with correct password', async () => {
    const passwordHash = await argon2.hash('a-strong-passphrase-12+', { type: argon2.argon2id });
    const store: FakeStore = {
      users: [
        {
          id: USER_ID,
          tenantId: TENANT_ID,
          email: 'jisoo@example.com',
          displayName: null,
          passwordHash,
          status: 'active',
          mfaEnabled: false,
        },
      ],
    };
    const svc = new AuthService(makePrisma(store), makeJwt());
    const session = await svc.signIn({
      email: 'jisoo@example.com',
      password: 'a-strong-passphrase-12+',
    });
    expect(session.user.id).toBe(USER_ID);
  });

  it('rejects signin with wrong password', async () => {
    const passwordHash = await argon2.hash('a-strong-passphrase-12+', { type: argon2.argon2id });
    const store: FakeStore = {
      users: [
        {
          id: USER_ID,
          tenantId: TENANT_ID,
          email: 'jisoo@example.com',
          displayName: null,
          passwordHash,
          status: 'active',
          mfaEnabled: false,
        },
      ],
    };
    const svc = new AuthService(makePrisma(store), makeJwt());
    await expect(
      svc.signIn({ email: 'jisoo@example.com', password: 'wrong-passphrase-12345' }),
    ).rejects.toBeInstanceOf(UnauthorizedException);
  });

  it('rejects signin with unknown email', async () => {
    const svc = new AuthService(makePrisma({ users: [] }), makeJwt());
    await expect(
      svc.signIn({ email: 'ghost@example.com', password: 'a-strong-passphrase-12+' }),
    ).rejects.toBeInstanceOf(UnauthorizedException);
  });
});
