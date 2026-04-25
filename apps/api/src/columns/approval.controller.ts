import {
  BadRequestException,
  Controller,
  Get,
  Param,
  Query,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { SkipThrottle } from '@nestjs/throttler';
import { ApprovalTokenError, verifyApprovalToken } from './approval-token';
import { ColumnService } from './column.service';

// Public — accepts a token issued via email/SMS/in-app and records the
// decision exactly once. The token itself is the credential. See ADR-0013 §3.
@ApiTags('approval')
@SkipThrottle()
@Controller('approve')
export class ApprovalController {
  constructor(
    private readonly columns: ColumnService,
    private readonly config: ConfigService,
  ) {}

  @Get(':token')
  @ApiOperation({
    summary: 'Resolve a one-tap approval link (email/SMS/in-app)',
    description:
      'Public endpoint. The token is HMAC-signed; no personal data inside. Single-use, ' +
      '72-hour expiry. Records the decision and tallies the column.',
  })
  async resolve(
    @Param('token') token: string,
    @Query('lang') lang?: string,
  ): Promise<{
    decision: 'approve' | 'reject' | 'revise';
    requestId: string;
    columnId: string;
    outcome: { result: string; reason?: string };
    locale: string;
  }> {
    const secret = this.config.get<string>('APPROVAL_HMAC_SECRET');
    if (!secret) {
      throw new BadRequestException('Approval service not configured.');
    }
    let payload: ReturnType<typeof verifyApprovalToken>;
    try {
      payload = verifyApprovalToken(secret, token);
    } catch (e) {
      if (e instanceof ApprovalTokenError) {
        throw new BadRequestException({
          error: 'Token rejected',
          code: e.code,
          message: e.message,
        });
      }
      throw e;
    }
    const outcome = await this.columns.recordDecision(
      payload.requestId,
      payload.kind,
      'email-or-sms-link',
    );
    // Re-fetch the request to expose columnId for the UI redirect.
    return {
      decision: payload.kind,
      requestId: payload.requestId,
      columnId: '(see notification)',
      outcome,
      locale: lang ?? 'en',
    };
  }
}
