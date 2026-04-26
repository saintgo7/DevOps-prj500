// Agent rooms + members + messages (ADR-0021 §C + §D).
//
// Hard rules:
//   - Membership row carries exactly one principal (agent XOR user).
//   - agent-only rooms reject user members.
//   - Archived rooms reject new messages.
//   - Every message body runs through the platform's harmful-content
//     guard. Failures are rejected AND record a harmStrike on the agent.
//   - Agent-sent messages must include a valid Ed25519 signature over
//     `(roomId|originalLocale|originalText)`.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { checkHarmfulContent } from '../tones/harmful-content';
import { verifyAgentMessage } from './agent-signature';
import { AgentRegistryService } from './registry.service';

export type RoomKind = 'agent-only' | 'mixed' | 'public-readable';
export type RoomState = 'active' | 'archived';
export type MemberRole = 'observer' | 'contributor' | 'moderator';
export type MessageKind = 'chat' | 'proposal' | 'observation' | 'data-handoff';

export interface CreateRoomInput {
  tenantId: string;
  createdBy: string;
  topicI18n: Record<string, string>;
  sdgFocus?: string[];
  kind?: RoomKind;
  publicReadable?: boolean;
  dailyDigestEnabled?: boolean;
}

export interface AddMemberInput {
  tenantId: string;
  roomId: string;
  agentId?: string;
  userId?: string;
  memberRole?: MemberRole;
}

export interface PostMessageInput {
  tenantId: string;
  roomId: string;
  /** Exactly one of senderAgentId / senderUserId must be set. */
  senderAgentId?: string;
  senderUserId?: string;
  originalText: string;
  originalLocale: string;
  kind?: MessageKind;
  /** Required when senderAgentId is set. */
  signature?: string;
}

@Injectable()
export class AgentRoomsService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly registry: AgentRegistryService,
  ) {}

  async createRoom(input: CreateRoomInput) {
    if (!input.topicI18n || Object.keys(input.topicI18n).length === 0) {
      throw new BadRequestException('Room needs a topic in at least one locale.');
    }
    const kind: RoomKind = input.kind ?? 'mixed';
    const publicReadable = input.publicReadable ?? false;
    if (publicReadable && kind !== 'public-readable') {
      throw new BadRequestException(
        "publicReadable=true is only allowed when kind='public-readable'.",
      );
    }
    return this.prisma.agentRoom.create({
      data: {
        tenantId: input.tenantId,
        createdBy: input.createdBy,
        topicI18n: input.topicI18n as unknown as Prisma.InputJsonValue,
        sdgFocus: input.sdgFocus ?? [],
        kind,
        publicReadable,
        state: 'active',
        dailyDigestEnabled: input.dailyDigestEnabled ?? false,
      },
    });
  }

  async archive(tenantId: string, roomId: string) {
    const r = await this.prisma.agentRoom.findFirst({ where: { id: roomId, tenantId } });
    if (!r) throw new NotFoundException('Room not found.');
    if (r.state === 'archived') return r;
    return this.prisma.agentRoom.update({
      where: { id: roomId },
      data: { state: 'archived', archivedAt: new Date() },
    });
  }

  async addMember(input: AddMemberInput) {
    const principalCount =
      (input.agentId ? 1 : 0) + (input.userId ? 1 : 0);
    if (principalCount !== 1) {
      throw new BadRequestException(
        'Membership requires exactly one principal — agentId XOR userId.',
      );
    }
    const room = await this.prisma.agentRoom.findFirst({
      where: { id: input.roomId, tenantId: input.tenantId },
    });
    if (!room) throw new NotFoundException('Room not found.');
    if (room.state !== 'active') {
      throw new ConflictException('Cannot add members to an archived room.');
    }
    if (room.kind === 'agent-only' && input.userId) {
      throw new BadRequestException(
        "agent-only rooms accept agent members only. Use kind='mixed' for humans.",
      );
    }
    return this.prisma.agentRoomMember.create({
      data: {
        tenantId: input.tenantId,
        roomId: input.roomId,
        agentId: input.agentId ?? null,
        userId: input.userId ?? null,
        memberRole: input.memberRole ?? 'contributor',
      },
    });
  }

  /**
   * Post a message into a room. Runs the harmful-content guard, verifies
   * the agent signature when sender is an agent, then persists. On guard
   * failure for an agent sender we increment the agent's harmStrikes (the
   * registry service will auto-pause if the threshold is crossed).
   */
  async postMessage(input: PostMessageInput) {
    const senderCount =
      (input.senderAgentId ? 1 : 0) + (input.senderUserId ? 1 : 0);
    if (senderCount !== 1) {
      throw new BadRequestException(
        'Message requires exactly one sender — senderAgentId XOR senderUserId.',
      );
    }
    if (!input.originalText || input.originalText.trim().length === 0) {
      throw new BadRequestException('Message text is empty.');
    }
    if (!input.originalLocale || input.originalLocale.trim().length === 0) {
      throw new BadRequestException('Message locale is required.');
    }

    const room = await this.prisma.agentRoom.findFirst({
      where: { id: input.roomId, tenantId: input.tenantId },
    });
    if (!room) throw new NotFoundException('Room not found.');
    if (room.state !== 'active') {
      throw new ConflictException('Cannot post to an archived room.');
    }

    // Verify agent signature.
    if (input.senderAgentId) {
      if (!input.signature) {
        throw new BadRequestException(
          'Agent-sent messages require an Ed25519 signature.',
        );
      }
      const agent = await this.prisma.agentRegistration.findFirst({
        where: { id: input.senderAgentId, tenantId: input.tenantId },
      });
      if (!agent) throw new NotFoundException('Sender agent not found.');
      if (agent.state !== 'active') {
        throw new ConflictException(
          `Sender agent is in state '${agent.state}' — cannot post.`,
        );
      }
      const ok = verifyAgentMessage({
        publicKeyHex: agent.publicKey,
        signatureHex: input.signature,
        roomId: input.roomId,
        locale: input.originalLocale,
        text: input.originalText,
      });
      if (!ok) {
        throw new BadRequestException(
          'Signature did not verify against the agent public key.',
        );
      }
    }

    // Run harmful-content guard.
    const harm = checkHarmfulContent([input.originalText]);
    if (!harm.pass) {
      if (input.senderAgentId) {
        await this.registry.recordHarmStrike(input.tenantId, input.senderAgentId);
      }
      throw new BadRequestException({
        error: 'Message blocked by the harmful-content guard.',
        items: harm.findings.filter((f) => !f.ok).map((f) => `${f.category}: ${f.message}`),
      });
    }

    return this.prisma.agentMessage.create({
      data: {
        tenantId: input.tenantId,
        roomId: input.roomId,
        senderAgentId: input.senderAgentId ?? null,
        senderUserId: input.senderUserId ?? null,
        originalText: input.originalText,
        originalLocale: input.originalLocale,
        kind: input.kind ?? 'chat',
        signature: input.signature ?? null,
        harmReport: { ok: true } as unknown as Prisma.InputJsonValue,
      },
    });
  }

  async listMessages(tenantId: string, roomId: string, since?: Date) {
    const where: Prisma.AgentMessageWhereInput = { tenantId, roomId };
    if (since) where.postedAt = { gte: since };
    return this.prisma.agentMessage.findMany({
      where,
      orderBy: { postedAt: 'asc' },
    });
  }
}
