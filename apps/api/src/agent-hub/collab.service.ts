// Agent collaboration proposals (ADR-0021 §F).
//
// Mirrors the contact-masking pattern used by NeedMatch (ADR-0018) and
// ExpertMatch (ADR-0019). Until both stewards have hit accept, contact
// fields are excluded at the API layer.

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';

export type ProposalState =
  | 'suggested'
  | 'recipient_review'
  | 'accepted'
  | 'engaged'
  | 'completed'
  | 'declined'
  | 'cancelled';

export interface ProposeInput {
  tenantId: string;
  /** Exactly one of proposer{AgentId,UserId}. */
  proposerAgentId?: string;
  proposerUserId?: string;
  /** Exactly one of recipient{AgentId,UserId}. */
  recipientAgentId?: string;
  recipientUserId?: string;
  subjectI18n: Record<string, string>;
  contextI18n: Record<string, string>;
  noncommercialNotice: boolean;
}

const ALLOWED: Record<ProposalState, ProposalState[]> = {
  suggested: ['recipient_review', 'cancelled'],
  recipient_review: ['accepted', 'declined', 'cancelled'],
  accepted: ['engaged', 'cancelled'],
  engaged: ['completed', 'cancelled'],
  completed: [],
  declined: [],
  cancelled: [],
};

@Injectable()
export class AgentCollabService {
  constructor(private readonly prisma: PrismaService) {}

  static canTransition(from: ProposalState, to: ProposalState): boolean {
    return ALLOWED[from].includes(to);
  }

  async propose(input: ProposeInput) {
    if (input.noncommercialNotice !== true) {
      throw new BadRequestException(
        'Collaboration proposal must declare non-commercial use.',
      );
    }
    const proposerCount =
      (input.proposerAgentId ? 1 : 0) + (input.proposerUserId ? 1 : 0);
    if (proposerCount !== 1) {
      throw new BadRequestException(
        'Proposal needs exactly one proposer — proposerAgentId XOR proposerUserId.',
      );
    }
    const recipientCount =
      (input.recipientAgentId ? 1 : 0) + (input.recipientUserId ? 1 : 0);
    if (recipientCount !== 1) {
      throw new BadRequestException(
        'Proposal needs exactly one recipient — recipientAgentId XOR recipientUserId.',
      );
    }
    if (!input.subjectI18n.en && !input.subjectI18n.ko) {
      throw new BadRequestException(
        'Subject must include at least an English or Korean entry.',
      );
    }
    return this.prisma.agentCollaborationProposal.create({
      data: {
        tenantId: input.tenantId,
        proposerAgentId: input.proposerAgentId ?? null,
        proposerUserId: input.proposerUserId ?? null,
        recipientAgentId: input.recipientAgentId ?? null,
        recipientUserId: input.recipientUserId ?? null,
        subjectI18n: input.subjectI18n as unknown as Prisma.InputJsonValue,
        contextI18n: input.contextI18n as unknown as Prisma.InputJsonValue,
        noncommercialNotice: true,
        state: 'suggested',
      },
    });
  }

  async transition(tenantId: string, proposalId: string, to: ProposalState) {
    const p = await this.prisma.agentCollaborationProposal.findFirst({
      where: { id: proposalId, tenantId },
    });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (!AgentCollabService.canTransition(p.state as ProposalState, to)) {
      throw new ConflictException(`Cannot transition '${p.state}' → '${to}'.`);
    }
    return this.prisma.agentCollaborationProposal.update({
      where: { id: proposalId },
      data: { state: to },
    });
  }

  /**
   * One-sided steward acceptance. State stays 'recipient_review' (or the
   * receiver moves it there) until BOTH sides have accepted, at which
   * point it advances to 'accepted'.
   */
  async accept(tenantId: string, proposalId: string, side: 'proposer' | 'recipient') {
    const p = await this.prisma.agentCollaborationProposal.findFirst({
      where: { id: proposalId, tenantId },
    });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (p.state !== 'suggested' && p.state !== 'recipient_review') {
      throw new ConflictException(
        `Cannot accept a proposal in state '${p.state}'.`,
      );
    }
    const data: Record<string, unknown> = { state: 'recipient_review' };
    if (side === 'proposer') {
      if (p.proposerStewardAcceptedAt) {
        throw new ConflictException('Proposer steward already accepted.');
      }
      data.proposerStewardAcceptedAt = new Date();
      if (p.recipientStewardAcceptedAt) data.state = 'accepted';
    } else {
      if (p.recipientStewardAcceptedAt) {
        throw new ConflictException('Recipient steward already accepted.');
      }
      data.recipientStewardAcceptedAt = new Date();
      if (p.proposerStewardAcceptedAt) data.state = 'accepted';
    }
    return this.prisma.agentCollaborationProposal.update({
      where: { id: proposalId },
      data: data as unknown as Prisma.AgentCollaborationProposalUpdateInput,
    });
  }

  async decline(tenantId: string, proposalId: string, reason: string) {
    if (!reason || reason.trim().length < 10) {
      throw new BadRequestException('Decline reason must be at least 10 characters.');
    }
    const p = await this.prisma.agentCollaborationProposal.findFirst({
      where: { id: proposalId, tenantId },
    });
    if (!p) throw new NotFoundException('Proposal not found.');
    if (!AgentCollabService.canTransition(p.state as ProposalState, 'declined')) {
      throw new ConflictException(
        `Cannot decline a proposal in state '${p.state}'.`,
      );
    }
    return this.prisma.agentCollaborationProposal.update({
      where: { id: proposalId },
      data: { state: 'declined', declinedReason: reason.trim() },
    });
  }

  /**
   * Returns true when both stewards have accepted (and so contact
   * details may be unmasked at the API layer). Used by callers that
   * decide whether to reveal contact info on the response.
   */
  static bothSidesAccepted(p: {
    proposerStewardAcceptedAt: Date | null;
    recipientStewardAcceptedAt: Date | null;
  }): boolean {
    return Boolean(p.proposerStewardAcceptedAt && p.recipientStewardAcceptedAt);
  }
}
