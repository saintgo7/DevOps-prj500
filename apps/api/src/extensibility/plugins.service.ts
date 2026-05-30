// Plugin lifecycle service (ADR-0020 §A + §F).
//
// Plugins move through draft -> review -> approved with admin governance
// (super-admin for governanceTier='strict'). super-admin can pause a live
// plugin at any time; the reason is permanent.
//
// Capability tokens are issued at approval time. The raw token is returned
// once and only once; thereafter we keep only its SHA-256 hash. The
// generated token is suitable for inclusion in an Authorization header
// of plugin->platform calls.

import { createHash, randomBytes } from 'node:crypto';
import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export type PluginState = 'draft' | 'review' | 'approved' | 'paused' | 'retired';

export interface CreateManifestInput {
  tenantId: string;
  ownerUserId: string;
  pluginKey: string;
  name: string;
  version: string;
  authorEmail: string;
  homepageUrl?: string;
  requestedScopes: string[];
  governanceTier?: 'standard' | 'strict';
  noncommercialPledge: boolean;
  plainLanguagePledge: boolean;
}

export interface IssuedToken {
  /** Raw token returned ONCE. Never persisted. */
  raw: string;
  /** Persisted token row id. */
  id: string;
  expiresAt: Date;
  grantedScopes: string[];
}

const ALLOWED: Record<PluginState, PluginState[]> = {
  draft: ['review', 'retired'],
  review: ['draft', 'approved', 'retired'],
  approved: ['paused', 'retired'],
  paused: ['approved', 'retired'],
  retired: [],
};

const NINETY_DAYS_MS = 90 * 24 * 60 * 60 * 1000;

@Injectable()
export class PluginsService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: PluginState, to: PluginState): boolean {
    return ALLOWED[from].includes(to);
  }

  /**
   * Compute the canonical SHA-256 of a manifest's significant fields. Used
   * to detect tampering between create / approve / runtime.
   */
  static computeManifestHash(input: CreateManifestInput): string {
    const canonical = JSON.stringify({
      pluginKey: input.pluginKey,
      name: input.name,
      version: input.version,
      authorEmail: input.authorEmail,
      requestedScopes: [...input.requestedScopes].sort(),
      governanceTier: input.governanceTier ?? 'standard',
    });
    return createHash('sha256').update(canonical).digest('hex');
  }

  async createManifest(input: CreateManifestInput) {
    if (input.noncommercialPledge !== true) {
      throw new BadRequestException(
        'Plugin manifest must accept the non-commercial pledge.',
      );
    }
    if (input.plainLanguagePledge !== true) {
      throw new BadRequestException(
        'Plugin manifest must accept the plain-language pledge.',
      );
    }
    if (!/^[a-z0-9][a-z0-9-]{1,40}$/.test(input.pluginKey)) {
      throw new BadRequestException(
        'pluginKey must be lowercase alphanumeric with dashes (2–41 chars).',
      );
    }
    if (!/^\d+\.\d+\.\d+$/.test(input.version)) {
      throw new BadRequestException('version must be semver "MAJOR.MINOR.PATCH".');
    }
    return this.prisma.pluginManifest.create({
      data: {
        tenantId: input.tenantId,
        ownerUserId: input.ownerUserId,
        pluginKey: input.pluginKey,
        name: input.name,
        version: input.version,
        authorEmail: input.authorEmail,
        homepageUrl: input.homepageUrl ?? null,
        requestedScopes: input.requestedScopes,
        governanceTier: input.governanceTier ?? 'standard',
        noncommercialPledge: true,
        plainLanguagePledge: true,
        manifestHash: PluginsService.computeManifestHash(input),
        state: 'draft',
      },
    });
  }

  async transition(
    tenantId: string,
    pluginId: string,
    to: PluginState,
    actorId: string,
    /** Required when to='paused' or to='retired'. */
    reason?: string,
  ) {
    const m = await this.prisma.pluginManifest.findFirst({
      where: { id: pluginId, tenantId },
    });
    if (!m) throw new NotFoundException('Plugin manifest not found.');
    const from = m.state as PluginState;
    if (!PluginsService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'paused') {
      if (!reason || reason.trim().length < 30) {
        throw new BadRequestException(
          'Pause reason must be at least 30 characters — recorded forever.',
        );
      }
    }
    return this.prisma.pluginManifest.update({
      where: { id: pluginId },
      data: {
        state: to,
        ...(to === 'approved'
          ? { approvedAt: new Date(), approvedBy: actorId, pausedAt: null, pauseReason: null }
          : {}),
        ...(to === 'paused'
          ? { pausedAt: new Date(), pauseReason: `${reason!.trim()} (by:${actorId})` }
          : {}),
        ...(to === 'retired' ? { retiredAt: new Date() } : {}),
      },
    });
  }

  /**
   * Issue a scoped capability token. The plugin must be 'approved'. The
   * granted scope set must be a (possibly proper) subset of the manifest's
   * requestedScopes.
   */
  async issueToken(
    tenantId: string,
    pluginId: string,
    grantedScopes: string[],
    ttlMs: number = NINETY_DAYS_MS,
  ): Promise<IssuedToken> {
    const m = await this.prisma.pluginManifest.findFirst({
      where: { id: pluginId, tenantId },
    });
    if (!m) throw new NotFoundException('Plugin manifest not found.');
    if (m.state !== 'approved') {
      throw new ConflictException(
        `Tokens can only be issued for approved plugins. Current state: '${m.state}'.`,
      );
    }
    const requested = new Set(m.requestedScopes);
    for (const scope of grantedScopes) {
      if (!requested.has(scope)) {
        throw new BadRequestException(
          `Granted scope '${scope}' was not in the manifest's requestedScopes.`,
        );
      }
    }
    if (ttlMs <= 0 || ttlMs > 365 * 24 * 60 * 60 * 1000) {
      throw new BadRequestException('Token TTL must be between 1 ms and 365 days.');
    }
    // 256-bit random; encoded base64url. Prefix identifies the platform.
    const raw = `sdgi_pat_${randomBytes(32).toString('base64url')}`;
    const tokenHash = createHash('sha256').update(raw).digest('hex');
    const expiresAt = new Date(Date.now() + ttlMs);
    const created = await this.prisma.capabilityToken.create({
      data: {
        tenantId,
        pluginId,
        grantedScopes,
        tokenHash,
        expiresAt,
      },
    });
    return { raw, id: created.id, expiresAt, grantedScopes };
  }

  async revokeToken(tenantId: string, tokenId: string) {
    const t = await this.prisma.capabilityToken.findFirst({
      where: { id: tokenId, tenantId },
    });
    if (!t) throw new NotFoundException('Token not found.');
    if (t.revokedAt) return t;
    return this.prisma.capabilityToken.update({
      where: { id: tokenId },
      data: { revokedAt: new Date() },
    });
  }

  /**
   * Returns the plugin id for a presented raw token if (and only if) the
   * token is valid AND the plugin is approved. Returns null otherwise.
   * Caller still has to check that the requested capability is in
   * grantedScopes.
   */
  async resolveToken(
    raw: string,
  ): Promise<{ tenantId: string; pluginId: string; grantedScopes: string[] } | null> {
    const tokenHash = createHash('sha256').update(raw).digest('hex');
    const t = await this.prisma.capabilityToken.findFirst({
      where: { tokenHash },
    });
    if (!t) return null;
    if (t.revokedAt) return null;
    if (t.expiresAt.getTime() < Date.now()) return null;
    const m = await this.prisma.pluginManifest.findFirst({
      where: { id: t.pluginId, tenantId: t.tenantId },
    });
    if (!m || m.state !== 'approved') return null;
    return { tenantId: t.tenantId, pluginId: t.pluginId, grantedScopes: t.grantedScopes };
  }
}
