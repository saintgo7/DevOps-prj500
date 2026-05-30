import { Body, Controller, Get, Param, Post, Query, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
  IsDateString,
  IsIn,
  IsObject,
  IsOptional,
  IsString,
  MinLength,
} from 'class-validator';
import type { Request } from 'express';
import { JwtAuthGuard, type AuthenticatedRequest } from '../auth/jwt-auth.guard';
import { Roles } from '../auth/roles.decorator';
import { RolesGuard } from '../auth/roles.guard';
import {
  AgentCollabService,
  type ProposalState,
} from './collab.service';
import { AgentDigestService, type DigestState } from './digest.service';
import {
  AgentRegistryService,
  type AgentState,
  type SessionState,
} from './registry.service';
import { AgentRoomsService, type MemberRole, type MessageKind, type RoomKind } from './rooms.service';

class RegisterAgentDto {
  @IsString() agentKey!: string;
  @IsObject() nameI18n!: Record<string, { name: string; blurb?: string }>;
  @IsString() operatorOrg!: string;
  @IsString() stewardUserId!: string;
  @IsBoolean() noncommercialPledge!: boolean;
  @IsBoolean() nonharmPledge!: boolean;
  @IsBoolean() plainLanguagePledge!: boolean;
  @IsOptional() @IsArray() sdgFocus?: string[];
  @IsOptional() @IsArray() capabilities?: string[];
  @IsOptional() @IsArray() workingLocales?: string[];
  @IsOptional() @IsArray() fieldRegions?: string[];
  @IsOptional() @IsString() homepageUrl?: string;
  @IsString() publicKey!: string;
}

class TransitionAgentDto {
  @IsString() @IsIn(['draft', 'review', 'active', 'paused', 'retired']) to!: AgentState;
  @IsOptional() @IsString() @MinLength(30) reason?: string;
}

class OpenSessionDto {
  @IsOptional() @IsObject() currentTaskI18n?: Record<string, string>;
}

class HeartbeatDto {
  @IsString() @IsIn(['started', 'idle', 'busy', 'ended']) state!: SessionState;
  @IsOptional() @IsObject() currentTaskI18n?: Record<string, string>;
}

class CreateRoomDto {
  @IsObject() topicI18n!: Record<string, string>;
  @IsOptional() @IsArray() sdgFocus?: string[];
  @IsOptional() @IsString() @IsIn(['agent-only', 'mixed', 'public-readable']) kind?: RoomKind;
  @IsOptional() @IsBoolean() publicReadable?: boolean;
  @IsOptional() @IsBoolean() dailyDigestEnabled?: boolean;
}

class AddMemberDto {
  @IsOptional() @IsString() agentId?: string;
  @IsOptional() @IsString() userId?: string;
  @IsOptional() @IsString() @IsIn(['observer', 'contributor', 'moderator'])
  memberRole?: MemberRole;
}

class PostMessageDto {
  @IsOptional() @IsString() senderAgentId?: string;
  @IsString() originalText!: string;
  @IsString() originalLocale!: string;
  @IsOptional() @IsString() @IsIn(['chat', 'proposal', 'observation', 'data-handoff'])
  kind?: MessageKind;
  @IsOptional() @IsString() signature?: string;
}

class UpsertDigestDto {
  @IsOptional() @IsString() roomId?: string;
  @IsDateString() digestDate!: string;
  @IsObject() summaryI18n!: Record<string, string>;
  @IsArray() sourceMessageIds!: string[];
  @IsOptional() @IsObject() aiProvenance?: {
    model: string;
    promptVersion: string;
    generatedAt: string;
    tokensIn?: number;
    tokensOut?: number;
  };
}

class TransitionDigestDto {
  @IsString() @IsIn(['draft', 'human_review', 'published', 'rejected']) to!: DigestState;
}

class ProposeCollabDto {
  @IsOptional() @IsString() proposerAgentId?: string;
  @IsOptional() @IsString() proposerUserId?: string;
  @IsOptional() @IsString() recipientAgentId?: string;
  @IsOptional() @IsString() recipientUserId?: string;
  @IsObject() subjectI18n!: Record<string, string>;
  @IsObject() contextI18n!: Record<string, string>;
  @IsBoolean() noncommercialNotice!: boolean;
}

class AcceptCollabDto {
  @IsString() @IsIn(['proposer', 'recipient']) side!: 'proposer' | 'recipient';
}

class TransitionCollabDto {
  @IsString()
  @IsIn(['suggested', 'recipient_review', 'accepted', 'engaged', 'completed', 'declined', 'cancelled'])
  to!: ProposalState;
}

class DeclineCollabDto {
  @IsString() @MinLength(10) reason!: string;
}

@ApiTags('agent-hub')
@Controller('agent-hub')
export class AgentHubController {
  constructor(
    private readonly registry: AgentRegistryService,
    private readonly rooms: AgentRoomsService,
    private readonly digests: AgentDigestService,
    private readonly collab: AgentCollabService,
  ) {}

  // ===== Registry =====

  @Post('agents')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Register an AI agent. Steward (a human) is mandatory; alignment pledges DB-enforced.',
  })
  async registerAgent(@Body() dto: RegisterAgentDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.registry.register({
      tenantId: auth.tenantId,
      agentKey: dto.agentKey,
      nameI18n: dto.nameI18n,
      operatorOrg: dto.operatorOrg,
      stewardUserId: dto.stewardUserId,
      noncommercialPledge: dto.noncommercialPledge,
      nonharmPledge: dto.nonharmPledge,
      plainLanguagePledge: dto.plainLanguagePledge,
      ...(dto.sdgFocus !== undefined ? { sdgFocus: dto.sdgFocus } : {}),
      ...(dto.capabilities !== undefined ? { capabilities: dto.capabilities } : {}),
      ...(dto.workingLocales !== undefined ? { workingLocales: dto.workingLocales } : {}),
      ...(dto.fieldRegions !== undefined ? { fieldRegions: dto.fieldRegions } : {}),
      ...(dto.homepageUrl !== undefined ? { homepageUrl: dto.homepageUrl } : {}),
      publicKey: dto.publicKey,
    });
  }

  @Post('agents/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'super-admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Move an agent through its lifecycle. Pause requires super-admin reason.',
  })
  async transitionAgent(
    @Param('id') id: string,
    @Body() dto: TransitionAgentDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.registry.transition(auth.tenantId, id, dto.to, auth.userId, dto.reason);
  }

  @Post('agents/:id/sessions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Open a monitoring session for an active agent' })
  async openSession(
    @Param('id') id: string,
    @Body() dto: OpenSessionDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.registry.openSession(auth.tenantId, id, dto.currentTaskI18n);
  }

  @Post('sessions/:id/heartbeat')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Heartbeat for an open session' })
  async heartbeat(
    @Param('id') id: string,
    @Body() dto: HeartbeatDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.registry.heartbeat(auth.tenantId, id, dto.state, dto.currentTaskI18n);
  }

  @Post('sessions/:id/end')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'End a session' })
  async endSession(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.registry.endSession(auth.tenantId, id);
  }

  // ===== Rooms =====

  @Post('rooms')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a collaboration room' })
  async createRoom(@Body() dto: CreateRoomDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.rooms.createRoom({
      tenantId: auth.tenantId,
      createdBy: auth.userId,
      topicI18n: dto.topicI18n,
      ...(dto.sdgFocus !== undefined ? { sdgFocus: dto.sdgFocus } : {}),
      ...(dto.kind !== undefined ? { kind: dto.kind } : {}),
      ...(dto.publicReadable !== undefined ? { publicReadable: dto.publicReadable } : {}),
      ...(dto.dailyDigestEnabled !== undefined ? { dailyDigestEnabled: dto.dailyDigestEnabled } : {}),
    });
  }

  @Post('rooms/:id/archive')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Archive a room (admin)' })
  async archiveRoom(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.rooms.archive(auth.tenantId, id);
  }

  @Post('rooms/:id/members')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Add a room member (agent XOR user)' })
  async addMember(
    @Param('id') id: string,
    @Body() dto: AddMemberDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.rooms.addMember({
      tenantId: auth.tenantId,
      roomId: id,
      ...(dto.agentId !== undefined ? { agentId: dto.agentId } : {}),
      ...(dto.userId !== undefined ? { userId: dto.userId } : {}),
      ...(dto.memberRole !== undefined ? { memberRole: dto.memberRole } : {}),
    });
  }

  @Post('rooms/:id/messages')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Post a message. Agent senders must include an Ed25519 signature.',
  })
  async postMessage(
    @Param('id') id: string,
    @Body() dto: PostMessageDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.rooms.postMessage({
      tenantId: auth.tenantId,
      roomId: id,
      ...(dto.senderAgentId !== undefined
        ? { senderAgentId: dto.senderAgentId }
        : { senderUserId: auth.userId }),
      originalText: dto.originalText,
      originalLocale: dto.originalLocale,
      ...(dto.kind !== undefined ? { kind: dto.kind } : {}),
      ...(dto.signature !== undefined ? { signature: dto.signature } : {}),
    });
  }

  @Get('rooms/:id/messages')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'List messages in a room (since query param optional)' })
  async listMessages(
    @Param('id') id: string,
    @Query('since') since: string | undefined,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.rooms.listMessages(auth.tenantId, id, since ? new Date(since) : undefined);
  }

  // ===== Digests =====

  @Post('digests')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Upsert a daily digest draft (AI-drafted output enters here)' })
  async upsertDigest(@Body() dto: UpsertDigestDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.digests.upsertDraft({
      tenantId: auth.tenantId,
      ...(dto.roomId !== undefined ? { roomId: dto.roomId } : {}),
      digestDate: new Date(dto.digestDate),
      summaryI18n: dto.summaryI18n,
      sourceMessageIds: dto.sourceMessageIds,
      ...(dto.aiProvenance !== undefined ? { aiProvenance: dto.aiProvenance } : {}),
    });
  }

  @Post('digests/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a digest through draft → human_review → published' })
  async transitionDigest(
    @Param('id') id: string,
    @Body() dto: TransitionDigestDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.digests.transition(auth.tenantId, id, dto.to, auth.userId);
  }

  // ===== Collaboration proposals =====

  @Post('collab/proposals')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Propose collaboration with an agent. Contact stays masked until both stewards accept.',
  })
  async propose(@Body() dto: ProposeCollabDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.collab.propose({
      tenantId: auth.tenantId,
      ...(dto.proposerAgentId !== undefined ? { proposerAgentId: dto.proposerAgentId } : {}),
      ...(dto.proposerUserId !== undefined ? { proposerUserId: dto.proposerUserId } : {}),
      ...(dto.recipientAgentId !== undefined ? { recipientAgentId: dto.recipientAgentId } : {}),
      ...(dto.recipientUserId !== undefined ? { recipientUserId: dto.recipientUserId } : {}),
      subjectI18n: dto.subjectI18n,
      contextI18n: dto.contextI18n,
      noncommercialNotice: dto.noncommercialNotice,
    });
  }

  @Post('collab/proposals/:id/accept')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'One-sided steward acceptance. Both sides must accept before contact unmasks.',
  })
  async acceptProposal(
    @Param('id') id: string,
    @Body() dto: AcceptCollabDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.collab.accept(auth.tenantId, id, dto.side);
  }

  @Post('collab/proposals/:id/decline')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Decline a proposal with a recorded reason' })
  async declineProposal(
    @Param('id') id: string,
    @Body() dto: DeclineCollabDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.collab.decline(auth.tenantId, id, dto.reason);
  }

  @Post('collab/proposals/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a proposal through accepted → engaged → completed' })
  async transitionProposal(
    @Param('id') id: string,
    @Body() dto: TransitionCollabDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.collab.transition(auth.tenantId, id, dto.to);
  }
}
