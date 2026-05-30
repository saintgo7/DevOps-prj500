// Agent registry — onboarding + lifecycle (ADR-0021 §A + §B).
//
// Stewards (humans) are mandatory. Three alignment pledges
// (noncommercial, nonharm, plain-language) are DB-enforced. State
// transitions follow an explicit allow-list. super-admin pause requires
// a permanent reason ≥ 30 chars.

import { createHash } from 'node:crypto';
import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type AgentState = 'draft' | 'review' | 'active' | 'paused' | 'retired';
export type SessionState = 'started' | 'idle' | 'busy' | 'ended' | 'crashed';

export interface RegisterAgentInput {
  tenantId: string;
  agentKey: string;
  nameI18n: Record<string, { name: string; blurb?: string }>;
  operatorOrg: string;
  stewardUserId: string;
  noncommercialPledge: boolean;
  nonharmPledge: boolean;
  plainLanguagePledge: boolean;
  sdgFocus?: string[];
  capabilities?: string[];
  workingLocales?: string[];
  fieldRegions?: string[];
  homepageUrl?: string;
  /** Ed25519 raw 32-byte hex public key. */
  publicKey: string;
}

const ALLOWED: Record<AgentState, AgentState[]> = {
  draft: ['review', 'retired'],
  review: ['draft', 'active', 'retired'],
  active: ['paused', 'retired'],
  paused: ['active', 'retired'],
  retired: [],
};

const HARM_AUTO_PAUSE_THRESHOLD = 3;
const KEY_PATTERN = /^[a-z0-9][a-z0-9-]{1,40}$/;
const ED25519_PUBKEY_PATTERN = /^[0-9a-f]{64}$/;

@Injectable()
export class AgentRegistryService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: AgentState, to: AgentState): boolean {
    return ALLOWED[from].includes(to);
  }

  static computeManifestHash(input: RegisterAgentInput): string {
    const canonical = JSON.stringify({
      agentKey: input.agentKey,
      operatorOrg: input.operatorOrg,
      sdgFocus: [...(input.sdgFocus ?? [])].sort(),
      capabilities: [...(input.capabilities ?? [])].sort(),
      publicKey: input.publicKey,
    });
    return createHash('sha256').update(canonical).digest('hex');
  }

  async register(input: RegisterAgentInput) {
    if (input.noncommercialPledge !== true) {
      throw new BadRequestException(
        'Agent registration requires the non-commercial pledge.',
      );
    }
    if (input.nonharmPledge !== true) {
      throw new BadRequestException('Agent registration requires the non-harm pledge.');
    }
    if (input.plainLanguagePledge !== true) {
      throw new BadRequestException(
        'Agent registration requires the plain-language pledge.',
      );
    }
    if (!input.stewardUserId) {
      throw new BadRequestException(
        'Steward (a human user) is required for every agent.',
      );
    }
    if (!KEY_PATTERN.test(input.agentKey)) {
      throw new BadRequestException(
        'agentKey must be lowercase alphanumeric with dashes (2–41 chars).',
      );
    }
    if (!ED25519_PUBKEY_PATTERN.test(input.publicKey)) {
      throw new BadRequestException(
        'publicKey must be 32-byte Ed25519 hex (64 lowercase hex chars).',
      );
    }
    return this.prisma.agentRegistration.create({
      data: {
        tenantId: input.tenantId,
        agentKey: input.agentKey,
        nameI18n: input.nameI18n as unknown as Prisma.InputJsonValue,
        operatorOrg: input.operatorOrg,
        stewardUserId: input.stewardUserId,
        noncommercialPledge: true,
        nonharmPledge: true,
        plainLanguagePledge: true,
        sdgFocus: input.sdgFocus ?? [],
        capabilities: input.capabilities ?? [],
        workingLocales: input.workingLocales ?? [],
        fieldRegions: input.fieldRegions ?? [],
        homepageUrl: input.homepageUrl ?? null,
        publicKey: input.publicKey,
        manifestHash: AgentRegistryService.computeManifestHash(input),
        state: 'draft',
      },
    });
  }

  async transition(
    tenantId: string,
    agentId: string,
    to: AgentState,
    actorId: string,
    reason?: string,
  ) {
    const a = await this.prisma.agentRegistration.findFirst({
      where: { id: agentId, tenantId },
    });
    if (!a) throw new NotFoundException('Agent not found.');
    const from = a.state as AgentState;
    if (!AgentRegistryService.canTransition(from, to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'paused') {
      if (!reason || reason.trim().length < 30) {
        throw new BadRequestException(
          'Pause reason must be at least 30 characters — recorded forever.',
        );
      }
    }
    return this.prisma.agentRegistration.update({
      where: { id: agentId },
      data: {
        state: to,
        ...(to === 'active'
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
   * Increment the agent's lifetime harm strike count. When the count
   * crosses HARM_AUTO_PAUSE_THRESHOLD the agent is auto-paused. Returns
   * the resulting record.
   */
  async recordHarmStrike(tenantId: string, agentId: string) {
    const a = await this.prisma.agentRegistration.findFirst({
      where: { id: agentId, tenantId },
    });
    if (!a) throw new NotFoundException('Agent not found.');
    const next = a.harmStrikes + 1;
    const shouldAutoPause =
      a.state === 'active' && next >= HARM_AUTO_PAUSE_THRESHOLD;
    return this.prisma.agentRegistration.update({
      where: { id: agentId },
      data: {
        harmStrikes: next,
        ...(shouldAutoPause
          ? {
              state: 'paused',
              pausedAt: new Date(),
              pauseReason:
                `Auto-paused: harm-strike threshold reached (${next} ≥ ${HARM_AUTO_PAUSE_THRESHOLD}).`,
            }
          : {}),
      },
    });
  }

  /** Open a new monitoring session for an agent. Agent must be 'active'. */
  async openSession(tenantId: string, agentId: string, currentTaskI18n?: Record<string, string>) {
    const a = await this.prisma.agentRegistration.findFirst({
      where: { id: agentId, tenantId },
    });
    if (!a) throw new NotFoundException('Agent not found.');
    if (a.state !== 'active') {
      throw new ConflictException(
        `Sessions can only open on active agents. Current state: '${a.state}'.`,
      );
    }
    return this.prisma.agentSession.create({
      data: {
        tenantId,
        agentId,
        currentTaskI18n: (currentTaskI18n ?? null) as unknown as Prisma.InputJsonValue,
        state: 'started',
      },
    });
  }

  async heartbeat(
    tenantId: string,
    sessionId: string,
    state: SessionState = 'idle',
    currentTaskI18n?: Record<string, string>,
  ) {
    if (!['started', 'idle', 'busy', 'ended'].includes(state)) {
      throw new BadRequestException(`Unknown session state '${state}'.`);
    }
    const s = await this.prisma.agentSession.findFirst({
      where: { id: sessionId, tenantId },
    });
    if (!s) throw new NotFoundException('Session not found.');
    if (s.state === 'ended' || s.state === 'crashed') {
      throw new ConflictException(
        `Cannot heartbeat a session in state '${s.state}'.`,
      );
    }
    return this.prisma.agentSession.update({
      where: { id: sessionId },
      data: {
        state,
        lastHeartbeatAt: new Date(),
        ...(currentTaskI18n !== undefined
          ? { currentTaskI18n: currentTaskI18n as unknown as Prisma.InputJsonValue }
          : {}),
      },
    });
  }

  async endSession(tenantId: string, sessionId: string) {
    const s = await this.prisma.agentSession.findFirst({
      where: { id: sessionId, tenantId },
    });
    if (!s) throw new NotFoundException('Session not found.');
    if (s.state === 'ended' || s.state === 'crashed') return s;
    return this.prisma.agentSession.update({
      where: { id: sessionId },
      data: { state: 'ended', endedAt: new Date() },
    });
  }
}
