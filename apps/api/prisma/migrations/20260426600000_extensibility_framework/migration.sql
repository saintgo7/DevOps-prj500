-- ADR-0020: extensibility framework — plugins / custom domains / events / capabilities / flags

CREATE TABLE "plugin_manifests" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plugin_key" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "version" TEXT NOT NULL,
  "author_email" TEXT NOT NULL,
  "homepage_url" TEXT,
  "owner_user_id" UUID NOT NULL,
  "requested_scopes" TEXT[] NOT NULL DEFAULT '{}',
  "noncommercial_pledge" BOOLEAN NOT NULL DEFAULT false,
  "plain_language_pledge" BOOLEAN NOT NULL DEFAULT false,
  "manifest_hash" TEXT NOT NULL,
  "governance_tier" TEXT NOT NULL DEFAULT 'standard',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "retired_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "plugin_manifests_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "plugin_manifests_state_check"
    CHECK ("state" IN ('draft','review','approved','paused','retired')),
  CONSTRAINT "plugin_manifests_governance_tier_check"
    CHECK ("governance_tier" IN ('standard','strict')),
  CONSTRAINT "plugin_manifests_noncommercial_check"
    CHECK ("noncommercial_pledge" = true),
  CONSTRAINT "plugin_manifests_plain_language_check"
    CHECK ("plain_language_pledge" = true)
);
CREATE UNIQUE INDEX "plugin_manifests_tenant_key_key"
  ON "plugin_manifests"("tenant_id", "plugin_key");
CREATE INDEX "plugin_manifests_tenant_state_idx"
  ON "plugin_manifests"("tenant_id", "state");

CREATE TABLE "custom_domains" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plugin_id" UUID NOT NULL,
  "domain_key" TEXT NOT NULL,
  "name_i18n" JSONB NOT NULL,
  "json_schema" JSONB NOT NULL,
  "links_to_core_kinds" TEXT[] NOT NULL DEFAULT '{}',
  "pii_fields" TEXT[] NOT NULL DEFAULT '{}',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "retired_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "custom_domains_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "custom_domains_state_check"
    CHECK ("state" IN ('draft','active','retired'))
);
CREATE UNIQUE INDEX "custom_domains_tenant_plugin_key_key"
  ON "custom_domains"("tenant_id", "plugin_id", "domain_key");
CREATE INDEX "custom_domains_tenant_state_idx"
  ON "custom_domains"("tenant_id", "state");
ALTER TABLE "custom_domains" ADD CONSTRAINT "custom_domains_plugin_id_fkey"
  FOREIGN KEY ("plugin_id") REFERENCES "plugin_manifests"("id");

CREATE TABLE "custom_records" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "domain_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "payload" JSONB NOT NULL,
  "state" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "custom_records_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "custom_records_tenant_domain_idx"
  ON "custom_records"("tenant_id", "domain_id", "created_at");
CREATE INDEX "custom_records_owner_idx"
  ON "custom_records"("owner_id");
CREATE INDEX "custom_records_payload_gin"
  ON "custom_records" USING GIN ("payload");
ALTER TABLE "custom_records" ADD CONSTRAINT "custom_records_domain_id_fkey"
  FOREIGN KEY ("domain_id") REFERENCES "custom_domains"("id");

CREATE TABLE "custom_workflows" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "domain_id" UUID NOT NULL,
  "workflow_key" TEXT NOT NULL,
  "transitions" JSONB NOT NULL,
  "triggers" JSONB NOT NULL DEFAULT '[]',
  "initial_state" TEXT NOT NULL,
  "terminal_states" TEXT[] NOT NULL DEFAULT '{}',
  "active" BOOLEAN NOT NULL DEFAULT true,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "custom_workflows_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "custom_workflows_tenant_domain_key_key"
  ON "custom_workflows"("tenant_id", "domain_id", "workflow_key");
CREATE INDEX "custom_workflows_tenant_domain_idx"
  ON "custom_workflows"("tenant_id", "domain_id");
ALTER TABLE "custom_workflows" ADD CONSTRAINT "custom_workflows_domain_id_fkey"
  FOREIGN KEY ("domain_id") REFERENCES "custom_domains"("id");

CREATE TABLE "domain_events" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "source" TEXT NOT NULL,
  "event_name" TEXT NOT NULL,
  "payload" JSONB NOT NULL,
  "correlation_id" TEXT,
  "occurred_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "domain_events_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "domain_events_tenant_event_idx"
  ON "domain_events"("tenant_id", "event_name", "occurred_at");
CREATE INDEX "domain_events_tenant_correlation_idx"
  ON "domain_events"("tenant_id", "correlation_id");
CREATE INDEX "domain_events_occurred_idx" ON "domain_events"("occurred_at");

-- Enforce append-only semantics. UPDATE / DELETE on domain_events are
-- rejected at the database level — not even the application can mutate
-- a recorded event. To "fix" a wrong event you emit a corrective one.
CREATE OR REPLACE FUNCTION reject_domain_events_mutation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'domain_events is append-only — UPDATE / DELETE rejected.';
END;
$$;
CREATE TRIGGER domain_events_no_update
  BEFORE UPDATE ON "domain_events"
  FOR EACH ROW EXECUTE FUNCTION reject_domain_events_mutation();
CREATE TRIGGER domain_events_no_delete
  BEFORE DELETE ON "domain_events"
  FOR EACH ROW EXECUTE FUNCTION reject_domain_events_mutation();

CREATE TABLE "event_subscriptions" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plugin_id" UUID NOT NULL,
  "event_pattern" TEXT NOT NULL,
  "delivery_kind" TEXT NOT NULL,
  "webhook_url" TEXT,
  "webhook_secret_hash" TEXT,
  "active" BOOLEAN NOT NULL DEFAULT true,
  "failure_count" INTEGER NOT NULL DEFAULT 0,
  "last_delivered_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "event_subscriptions_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "event_subscriptions_delivery_kind_check"
    CHECK ("delivery_kind" IN ('inproc','webhook')),
  -- A webhook subscription must carry a URL AND a secret hash. inproc
  -- subscriptions must NOT carry a webhook URL.
  CONSTRAINT "event_subscriptions_webhook_fields_check"
    CHECK (
      ("delivery_kind" = 'webhook' AND "webhook_url" IS NOT NULL AND "webhook_secret_hash" IS NOT NULL)
      OR
      ("delivery_kind" = 'inproc' AND "webhook_url" IS NULL AND "webhook_secret_hash" IS NULL)
    )
);
CREATE INDEX "event_subscriptions_tenant_pattern_idx"
  ON "event_subscriptions"("tenant_id", "event_pattern");
CREATE INDEX "event_subscriptions_plugin_active_idx"
  ON "event_subscriptions"("plugin_id", "active");
ALTER TABLE "event_subscriptions" ADD CONSTRAINT "event_subscriptions_plugin_id_fkey"
  FOREIGN KEY ("plugin_id") REFERENCES "plugin_manifests"("id");

CREATE TABLE "capability_tokens" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plugin_id" UUID NOT NULL,
  "granted_scopes" TEXT[] NOT NULL,
  "token_hash" TEXT NOT NULL,
  "expires_at" TIMESTAMP(3) NOT NULL,
  "revoked_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "capability_tokens_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "capability_tokens_token_hash_key" ON "capability_tokens"("token_hash");
CREATE INDEX "capability_tokens_tenant_plugin_idx"
  ON "capability_tokens"("tenant_id", "plugin_id");
CREATE INDEX "capability_tokens_expires_idx" ON "capability_tokens"("expires_at");
ALTER TABLE "capability_tokens" ADD CONSTRAINT "capability_tokens_plugin_id_fkey"
  FOREIGN KEY ("plugin_id") REFERENCES "plugin_manifests"("id");

CREATE TABLE "feature_flags" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "flag_key" TEXT NOT NULL,
  "enabled" BOOLEAN NOT NULL DEFAULT false,
  "audience" JSONB,
  "updated_by" UUID NOT NULL,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "feature_flags_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "feature_flags_tenant_flag_key" ON "feature_flags"("tenant_id", "flag_key");
CREATE INDEX "feature_flags_tenant_enabled_idx"
  ON "feature_flags"("tenant_id", "enabled");

-- ============================================================
-- RLS — every new table tenant-bound and FORCE-isolated.
-- ============================================================

ALTER TABLE "plugin_manifests"     ENABLE ROW LEVEL SECURITY;
ALTER TABLE "custom_domains"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "custom_records"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "custom_workflows"     ENABLE ROW LEVEL SECURITY;
ALTER TABLE "domain_events"        ENABLE ROW LEVEL SECURITY;
ALTER TABLE "event_subscriptions"  ENABLE ROW LEVEL SECURITY;
ALTER TABLE "capability_tokens"    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "feature_flags"        ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "plugin_manifests"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "custom_domains"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "custom_records"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "custom_workflows"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "domain_events"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "event_subscriptions"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "capability_tokens"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "feature_flags"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "plugin_manifests"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "custom_domains"      FORCE ROW LEVEL SECURITY;
ALTER TABLE "custom_records"      FORCE ROW LEVEL SECURITY;
ALTER TABLE "custom_workflows"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "domain_events"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "event_subscriptions" FORCE ROW LEVEL SECURITY;
ALTER TABLE "capability_tokens"   FORCE ROW LEVEL SECURITY;
ALTER TABLE "feature_flags"       FORCE ROW LEVEL SECURITY;
