// Custom domain + record + workflow services (ADR-0020 §B + §C + §D).

import {
  BadRequestException,
  ConflictException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { checkHarmfulContent } from '../tones/harmful-content';
import { EventsService } from './events.service';
import { validatePayload, type JsonSchema } from './schema-validate';

export type DomainState = 'draft' | 'active' | 'retired';

export interface CreateDomainInput {
  tenantId: string;
  pluginId: string;
  domainKey: string;
  nameI18n: Record<string, { name: string; description?: string }>;
  jsonSchema: JsonSchema;
  linksToCoreKinds?: string[];
  piiFields?: string[];
}

export interface UpsertRecordInput {
  tenantId: string;
  domainId: string;
  ownerId: string;
  /** When updating, the existing record id. */
  recordId?: string;
  payload: Record<string, unknown>;
  /** Optional starting state; ignored when a workflow is attached and a record already exists. */
  state?: string;
}

export interface CreateWorkflowInput {
  tenantId: string;
  domainId: string;
  workflowKey: string;
  /** { 'requested': ['approved','denied'], ... } */
  transitions: Record<string, string[]>;
  /** [{ on: 'approved', emit: 'reservation.approved' }, ...] */
  triggers?: Array<{ on: string; emit: string }>;
  initialState: string;
  terminalStates?: string[];
}

const DOMAIN_KEY_PATTERN = /^[a-z0-9][a-z0-9-]{1,40}$/;

@Injectable()
export class CustomDomainsService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly events: EventsService,
  ) {}

  async createDomain(input: CreateDomainInput) {
    if (!DOMAIN_KEY_PATTERN.test(input.domainKey)) {
      throw new BadRequestException(
        'domainKey must be lowercase alphanumeric with dashes (2–41 chars).',
      );
    }
    if (!input.jsonSchema || typeof input.jsonSchema !== 'object') {
      throw new BadRequestException('jsonSchema is required.');
    }
    // Sanity check: plugin must be approved.
    const plugin = await this.prisma.pluginManifest.findFirst({
      where: { id: input.pluginId, tenantId: input.tenantId },
    });
    if (!plugin) throw new NotFoundException('Plugin manifest not found.');
    if (plugin.state !== 'approved') {
      throw new ConflictException(
        `Domains may only be declared by approved plugins. Current plugin state: '${plugin.state}'.`,
      );
    }
    return this.prisma.customDomain.create({
      data: {
        tenantId: input.tenantId,
        pluginId: input.pluginId,
        domainKey: input.domainKey,
        nameI18n: input.nameI18n as unknown as Prisma.InputJsonValue,
        jsonSchema: input.jsonSchema as unknown as Prisma.InputJsonValue,
        linksToCoreKinds: input.linksToCoreKinds ?? [],
        piiFields: input.piiFields ?? [],
        state: 'draft',
      },
    });
  }

  async transitionDomain(tenantId: string, domainId: string, to: DomainState) {
    const d = await this.prisma.customDomain.findFirst({
      where: { id: domainId, tenantId },
    });
    if (!d) throw new NotFoundException('Custom domain not found.');
    const from = d.state as DomainState;
    const allowed: Record<DomainState, DomainState[]> = {
      draft: ['active', 'retired'],
      active: ['retired'],
      retired: [],
    };
    if (!allowed[from].includes(to)) {
      throw new ConflictException(`Cannot transition '${from}' → '${to}'.`);
    }
    if (to === 'retired') {
      const live = await this.prisma.customRecord.count({
        where: { tenantId, domainId },
      });
      if (live > 0) {
        throw new ConflictException(
          `Cannot retire a domain with ${live} active records — archive them first.`,
        );
      }
    }
    return this.prisma.customDomain.update({
      where: { id: domainId },
      data: { state: to, ...(to === 'retired' ? { retiredAt: new Date() } : {}) },
    });
  }

  /**
   * Create or update a CustomRecord. Validates payload against the
   * domain's JSON Schema, runs the harmful-content guard on stringy
   * fields, then emits 'record.created' or 'record.updated'.
   */
  async upsertRecord(input: UpsertRecordInput) {
    const domain = await this.prisma.customDomain.findFirst({
      where: { id: input.domainId, tenantId: input.tenantId },
    });
    if (!domain) throw new NotFoundException('Custom domain not found.');
    if (domain.state !== 'active') {
      throw new ConflictException(
        `Cannot write records to a domain in state '${domain.state}'.`,
      );
    }
    const schema = domain.jsonSchema as unknown as JsonSchema;
    const result = validatePayload(input.payload, schema);
    if (!result.ok) {
      throw new BadRequestException({
        error: 'Payload failed schema validation.',
        items: result.errors.map((e) => `${e.path}: ${e.message}`),
      });
    }
    // Run harmful-content guard on every string in the payload (shallow walk).
    const stringValues: string[] = [];
    const walk = (v: unknown): void => {
      if (typeof v === 'string') stringValues.push(v);
      else if (Array.isArray(v)) v.forEach(walk);
      else if (typeof v === 'object' && v !== null) {
        for (const child of Object.values(v as Record<string, unknown>)) walk(child);
      }
    };
    walk(input.payload);
    const harm = checkHarmfulContent(stringValues);
    if (!harm.pass) {
      throw new BadRequestException({
        error: 'Record blocked by the harmful-content guard.',
        items: harm.findings.filter((f) => !f.ok).map((f) => `${f.category}: ${f.message}`),
      });
    }

    let record;
    if (input.recordId) {
      const existing = await this.prisma.customRecord.findFirst({
        where: { id: input.recordId, tenantId: input.tenantId, domainId: input.domainId },
      });
      if (!existing) throw new NotFoundException('Record not found.');
      record = await this.prisma.customRecord.update({
        where: { id: existing.id },
        data: {
          payload: input.payload as unknown as Prisma.InputJsonValue,
          ...(input.state !== undefined ? { state: input.state } : {}),
        },
      });
    } else {
      record = await this.prisma.customRecord.create({
        data: {
          tenantId: input.tenantId,
          domainId: input.domainId,
          ownerId: input.ownerId,
          payload: input.payload as unknown as Prisma.InputJsonValue,
          state: input.state ?? null,
        },
      });
    }

    // Emit a domain event with PII masked using the domain's piiFields.
    await this.events.emit({
      tenantId: input.tenantId,
      source: `plugin.${domain.pluginId}`,
      eventName: input.recordId
        ? `${domain.domainKey}.updated`
        : `${domain.domainKey}.created`,
      payload: { recordId: record.id, payload: input.payload },
      piiFields: (domain.piiFields ?? []).map((f) => `payload.${f}`),
    });

    return record;
  }

  async createWorkflow(input: CreateWorkflowInput) {
    if (!input.workflowKey || input.workflowKey.trim().length === 0) {
      throw new BadRequestException('workflowKey is required.');
    }
    if (!input.transitions || typeof input.transitions !== 'object') {
      throw new BadRequestException('transitions map is required.');
    }
    if (!input.initialState) {
      throw new BadRequestException('initialState is required.');
    }
    // Every state mentioned (left or right) must form a closed graph.
    const knownStates = new Set<string>(Object.keys(input.transitions));
    for (const tos of Object.values(input.transitions)) {
      for (const t of tos) knownStates.add(t);
    }
    if (!knownStates.has(input.initialState)) {
      throw new BadRequestException(
        `initialState '${input.initialState}' is not present in the transitions map.`,
      );
    }
    for (const term of input.terminalStates ?? []) {
      if (!knownStates.has(term)) {
        throw new BadRequestException(
          `terminalState '${term}' is not present in the transitions map.`,
        );
      }
    }
    // Trigger emit names must match the platform pattern '<scope>.<verb>'.
    for (const tr of input.triggers ?? []) {
      if (!tr.emit.includes('.')) {
        throw new BadRequestException(
          `Trigger emit '${tr.emit}' must follow '<scope>.<verb>' form.`,
        );
      }
    }

    const domain = await this.prisma.customDomain.findFirst({
      where: { id: input.domainId, tenantId: input.tenantId },
    });
    if (!domain) throw new NotFoundException('Custom domain not found.');

    return this.prisma.customWorkflow.create({
      data: {
        tenantId: input.tenantId,
        domainId: input.domainId,
        workflowKey: input.workflowKey,
        transitions: input.transitions as unknown as Prisma.InputJsonValue,
        triggers: (input.triggers ?? []) as unknown as Prisma.InputJsonValue,
        initialState: input.initialState,
        terminalStates: input.terminalStates ?? [],
        active: true,
      },
    });
  }

  /**
   * Run a workflow transition on a record. Looks up the active workflow
   * for the record's domain, validates the requested transition, updates
   * the record state, and emits any matching trigger events.
   */
  async runWorkflowTransition(
    tenantId: string,
    recordId: string,
    workflowKey: string,
    to: string,
  ) {
    const record = await this.prisma.customRecord.findFirst({
      where: { id: recordId, tenantId },
    });
    if (!record) throw new NotFoundException('Record not found.');
    const wf = await this.prisma.customWorkflow.findFirst({
      where: { tenantId, domainId: record.domainId, workflowKey, active: true },
    });
    if (!wf) throw new NotFoundException('Active workflow not found for that domain.');

    const transitions = wf.transitions as unknown as Record<string, string[]>;
    const from = record.state ?? wf.initialState;
    if ((wf.terminalStates ?? []).includes(from)) {
      throw new ConflictException(
        `Record is in terminal state '${from}'; no further transitions are allowed.`,
      );
    }
    const allowed = transitions[from] ?? [];
    if (!allowed.includes(to)) {
      throw new ConflictException(
        `Workflow forbids transition '${from}' → '${to}'.`,
      );
    }

    const updated = await this.prisma.customRecord.update({
      where: { id: recordId },
      data: { state: to },
    });

    // Fire any trigger that matches the new state.
    const triggers = (wf.triggers as unknown as Array<{ on: string; emit: string }>) ?? [];
    const domain = await this.prisma.customDomain.findFirst({
      where: { id: record.domainId, tenantId },
    });
    for (const tr of triggers.filter((t) => t.on === to)) {
      await this.events.emit({
        tenantId,
        source: `plugin.${domain?.pluginId ?? 'unknown'}`,
        eventName: tr.emit,
        payload: { recordId, from, to },
      });
    }
    return updated;
  }
}
