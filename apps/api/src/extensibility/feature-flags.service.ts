// Per-tenant feature flags (ADR-0020 §F).
//
// Setting `enabled=false` on a plugin's flag is the platform's *final
// kill switch*. The audience JSON allows partial rollout — { userIds:
// [...], roles: [...] } — but the master switch overrides everything.

import {
  BadRequestException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export interface FlagAudience {
  userIds?: string[];
  roles?: string[];
}

export interface SetFlagInput {
  tenantId: string;
  flagKey: string;
  enabled: boolean;
  audience?: FlagAudience;
  updatedBy: string;
}

const FLAG_KEY_PATTERN = /^[a-z0-9][a-z0-9.-]{1,80}$/;

@Injectable()
export class FeatureFlagsService {
  constructor(private readonly prisma: PrismaService) {}

  async set(input: SetFlagInput) {
    if (!FLAG_KEY_PATTERN.test(input.flagKey)) {
      throw new BadRequestException(
        'flagKey must be lowercase alphanumeric with dots/dashes (2–81 chars).',
      );
    }
    const existing = await this.prisma.featureFlag.findFirst({
      where: { tenantId: input.tenantId, flagKey: input.flagKey },
    });
    if (existing) {
      return this.prisma.featureFlag.update({
        where: { id: existing.id },
        data: {
          enabled: input.enabled,
          audience: (input.audience ?? null) as unknown as Prisma.InputJsonValue,
          updatedBy: input.updatedBy,
        },
      });
    }
    return this.prisma.featureFlag.create({
      data: {
        tenantId: input.tenantId,
        flagKey: input.flagKey,
        enabled: input.enabled,
        audience: (input.audience ?? null) as unknown as Prisma.InputJsonValue,
        updatedBy: input.updatedBy,
      },
    });
  }

  /**
   * Resolve a flag for a specific user. Returns true if the master switch
   * is on AND (no audience restriction OR audience matches the user).
   */
  static evaluate(
    flag: { enabled: boolean; audience: FlagAudience | null } | null,
    user: { userId: string; roles: readonly string[] },
  ): boolean {
    if (!flag) return false;
    if (!flag.enabled) return false;
    const audience = flag.audience ?? null;
    if (!audience) return true;
    const userIds = audience.userIds ?? [];
    const roles = audience.roles ?? [];
    if (userIds.length === 0 && roles.length === 0) return true;
    if (userIds.includes(user.userId)) return true;
    if (user.roles.some((r) => roles.includes(r))) return true;
    return false;
  }

  async resolve(tenantId: string, flagKey: string, user: { userId: string; roles: readonly string[] }): Promise<boolean> {
    const flag = await this.prisma.featureFlag.findFirst({
      where: { tenantId, flagKey },
    });
    return FeatureFlagsService.evaluate(
      flag ? { enabled: flag.enabled, audience: flag.audience as FlagAudience | null } : null,
      user,
    );
  }

  async get(tenantId: string, flagKey: string) {
    const flag = await this.prisma.featureFlag.findFirst({
      where: { tenantId, flagKey },
    });
    if (!flag) throw new NotFoundException('Feature flag not set.');
    return flag;
  }
}
