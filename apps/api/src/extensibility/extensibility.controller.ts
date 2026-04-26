import { Body, Controller, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import {
  IsArray,
  IsBoolean,
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
  CustomDomainsService,
  type CreateDomainInput,
  type CreateWorkflowInput,
  type DomainState,
} from './custom-domains.service';
import { FeatureFlagsService, type FlagAudience } from './feature-flags.service';
import { PluginsService, type PluginState } from './plugins.service';
import { SubscriptionsService } from './subscriptions.service';

class CreateManifestDto {
  @IsString() pluginKey!: string;
  @IsString() name!: string;
  @IsString() version!: string;
  @IsString() authorEmail!: string;
  @IsOptional() @IsString() homepageUrl?: string;
  @IsArray() requestedScopes!: string[];
  @IsOptional() @IsString() @IsIn(['standard', 'strict']) governanceTier?: 'standard' | 'strict';
  @IsBoolean() noncommercialPledge!: boolean;
  @IsBoolean() plainLanguagePledge!: boolean;
}

class TransitionManifestDto {
  @IsString() @IsIn(['draft', 'review', 'approved', 'paused', 'retired']) to!: PluginState;
  @IsOptional() @IsString() @MinLength(30) reason?: string;
}

class IssueTokenDto {
  @IsArray() grantedScopes!: string[];
  @IsOptional() ttlMs?: number;
}

class CreateDomainDto {
  @IsString() pluginId!: string;
  @IsString() domainKey!: string;
  @IsObject() nameI18n!: Record<string, { name: string; description?: string }>;
  @IsObject() jsonSchema!: object;
  @IsOptional() @IsArray() linksToCoreKinds?: string[];
  @IsOptional() @IsArray() piiFields?: string[];
}

class TransitionDomainDto {
  @IsString() @IsIn(['draft', 'active', 'retired']) to!: DomainState;
}

class UpsertRecordDto {
  @IsString() domainId!: string;
  @IsOptional() @IsString() recordId?: string;
  @IsObject() payload!: Record<string, unknown>;
  @IsOptional() @IsString() state?: string;
}

class CreateWorkflowDto {
  @IsString() domainId!: string;
  @IsString() workflowKey!: string;
  @IsObject() transitions!: Record<string, string[]>;
  @IsOptional() @IsArray() triggers?: Array<{ on: string; emit: string }>;
  @IsString() initialState!: string;
  @IsOptional() @IsArray() terminalStates?: string[];
}

class RunTransitionDto {
  @IsString() recordId!: string;
  @IsString() workflowKey!: string;
  @IsString() to!: string;
}

class CreateSubscriptionDto {
  @IsString() pluginId!: string;
  @IsString() eventPattern!: string;
  @IsString() @IsIn(['inproc', 'webhook']) deliveryKind!: 'inproc' | 'webhook';
  @IsOptional() @IsString() webhookUrl?: string;
}

class SetFlagDto {
  @IsString() flagKey!: string;
  @IsBoolean() enabled!: boolean;
  @IsOptional() @IsObject() audience?: FlagAudience;
}

@ApiTags('extensibility')
@Controller('extensibility')
export class ExtensibilityController {
  constructor(
    private readonly plugins: PluginsService,
    private readonly domains: CustomDomainsService,
    private readonly subs: SubscriptionsService,
    private readonly flags: FeatureFlagsService,
  ) {}

  @Post('plugins')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Register a plugin manifest (admin)' })
  async createManifest(@Body() dto: CreateManifestDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.plugins.createManifest({
      tenantId: auth.tenantId,
      ownerUserId: auth.userId,
      pluginKey: dto.pluginKey,
      name: dto.name,
      version: dto.version,
      authorEmail: dto.authorEmail,
      ...(dto.homepageUrl !== undefined ? { homepageUrl: dto.homepageUrl } : {}),
      requestedScopes: dto.requestedScopes,
      ...(dto.governanceTier !== undefined ? { governanceTier: dto.governanceTier } : {}),
      noncommercialPledge: dto.noncommercialPledge,
      plainLanguagePledge: dto.plainLanguagePledge,
    });
  }

  @Post('plugins/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'super-admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Move a plugin through its lifecycle (admin; super-admin for pause/retire)',
  })
  async transitionManifest(
    @Param('id') id: string,
    @Body() dto: TransitionManifestDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.plugins.transition(auth.tenantId, id, dto.to, auth.userId, dto.reason);
  }

  @Post('plugins/:id/tokens')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Issue a capability token. Raw value returned ONCE — cannot be retrieved later.',
  })
  async issueToken(@Param('id') id: string, @Body() dto: IssueTokenDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.plugins.issueToken(auth.tenantId, id, dto.grantedScopes, dto.ttlMs);
  }

  @Post('plugins/tokens/:tokenId/revoke')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'super-admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Revoke a capability token' })
  async revokeToken(@Param('tokenId') tokenId: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.plugins.revokeToken(auth.tenantId, tokenId);
  }

  @Post('domains')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Declare a custom domain attached to an approved plugin' })
  async createDomain(@Body() dto: CreateDomainDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const input: CreateDomainInput = {
      tenantId: auth.tenantId,
      pluginId: dto.pluginId,
      domainKey: dto.domainKey,
      nameI18n: dto.nameI18n,
      jsonSchema: dto.jsonSchema,
      ...(dto.linksToCoreKinds !== undefined ? { linksToCoreKinds: dto.linksToCoreKinds } : {}),
      ...(dto.piiFields !== undefined ? { piiFields: dto.piiFields } : {}),
    };
    return this.domains.createDomain(input);
  }

  @Post('domains/:id/transition')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Move a custom domain through draft → active → retired' })
  async transitionDomain(
    @Param('id') id: string,
    @Body() dto: TransitionDomainDto,
    @Req() req: Request,
  ) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.domains.transitionDomain(auth.tenantId, id, dto.to);
  }

  @Post('records')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Upsert a custom record (validated against the domain schema)' })
  async upsertRecord(@Body() dto: UpsertRecordDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.domains.upsertRecord({
      tenantId: auth.tenantId,
      ownerId: auth.userId,
      domainId: dto.domainId,
      ...(dto.recordId !== undefined ? { recordId: dto.recordId } : {}),
      payload: dto.payload,
      ...(dto.state !== undefined ? { state: dto.state } : {}),
    });
  }

  @Post('workflows')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Define a state machine over a custom domain' })
  async createWorkflow(@Body() dto: CreateWorkflowDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    const input: CreateWorkflowInput = {
      tenantId: auth.tenantId,
      domainId: dto.domainId,
      workflowKey: dto.workflowKey,
      transitions: dto.transitions,
      ...(dto.triggers !== undefined ? { triggers: dto.triggers } : {}),
      initialState: dto.initialState,
      ...(dto.terminalStates !== undefined ? { terminalStates: dto.terminalStates } : {}),
    };
    return this.domains.createWorkflow(input);
  }

  @Post('workflows/run')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin', 'reviewer', 'contributor')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Run a workflow transition on one record' })
  async runTransition(@Body() dto: RunTransitionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.domains.runWorkflowTransition(
      auth.tenantId,
      dto.recordId,
      dto.workflowKey,
      dto.to,
    );
  }

  @Post('subscriptions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Subscribe to events. Webhook secret is returned ONCE on creation.',
  })
  async createSubscription(@Body() dto: CreateSubscriptionDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.subs.create({
      tenantId: auth.tenantId,
      pluginId: dto.pluginId,
      eventPattern: dto.eventPattern,
      deliveryKind: dto.deliveryKind,
      ...(dto.webhookUrl !== undefined ? { webhookUrl: dto.webhookUrl } : {}),
    });
  }

  @Post('subscriptions/:id/reactivate')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Reactivate an auto-deactivated subscription (super-admin)' })
  async reactivateSubscription(@Param('id') id: string, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.subs.reactivate(auth.tenantId, id);
  }

  @Post('flags')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('super-admin')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Set a feature flag (super-admin only — final kill switch)' })
  async setFlag(@Body() dto: SetFlagDto, @Req() req: Request) {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.flags.set({
      tenantId: auth.tenantId,
      flagKey: dto.flagKey,
      enabled: dto.enabled,
      ...(dto.audience !== undefined ? { audience: dto.audience } : {}),
      updatedBy: auth.userId,
    });
  }
}
