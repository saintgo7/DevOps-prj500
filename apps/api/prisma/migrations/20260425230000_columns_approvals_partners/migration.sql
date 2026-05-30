-- Daily Columns + Multi-channel Approval + Partners (ADR-0013)

CREATE TABLE "columns" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "author_id" UUID,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'en',
  "source_url" TEXT NOT NULL,
  "source_title" TEXT,
  "source_authors" TEXT[] NOT NULL DEFAULT '{}',
  "source_publisher" TEXT,
  "source_license" TEXT,
  "source_published_at" TIMESTAMP(3),
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "sdg_confidence" DOUBLE PRECISION,
  "sensitivity" TEXT NOT NULL DEFAULT 'standard',
  "standard_version" TEXT NOT NULL DEFAULT 'v0.1',
  "ai_provenance" JSONB,
  "submitted_at" TIMESTAMP(3),
  "published_at" TIMESTAMP(3),
  "revoked_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "columns_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "columns_tenant_state_created_idx" ON "columns"("tenant_id", "state", "created_at");
CREATE INDEX "columns_state_published_idx" ON "columns"("state", "published_at");
CREATE INDEX "columns_sdg_focus_idx" ON "columns" USING GIN ("sdg_focus");

CREATE TABLE "column_approvers" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "channels" TEXT[] NOT NULL DEFAULT '{"email","inapp"}',
  "phone_e164" TEXT,
  "sensitive_ok" BOOLEAN NOT NULL DEFAULT false,
  "active" BOOLEAN NOT NULL DEFAULT true,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "column_approvers_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "column_approvers_tenant_user_key" ON "column_approvers"("tenant_id", "user_id");
CREATE INDEX "column_approvers_tenant_active_idx" ON "column_approvers"("tenant_id", "active");

CREATE TABLE "approval_requests" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "column_id" UUID NOT NULL,
  "approver_id" UUID NOT NULL,
  "channel" TEXT NOT NULL,
  "expires_at" TIMESTAMP(3) NOT NULL,
  "decision" TEXT,
  "decided_at" TIMESTAMP(3),
  "decided_via" TEXT,
  "reason_note" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "approval_requests_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "approval_requests_tenant_column_idx" ON "approval_requests"("tenant_id", "column_id");
CREATE INDEX "approval_requests_approver_decision_idx" ON "approval_requests"("approver_id", "decision");
CREATE INDEX "approval_requests_expires_idx" ON "approval_requests"("expires_at");
ALTER TABLE "approval_requests" ADD CONSTRAINT "approval_requests_column_id_fkey"
  FOREIGN KEY ("column_id") REFERENCES "columns"("id");

CREATE TABLE "partner_organizations" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "name" TEXT NOT NULL,
  "homepage_url" TEXT,
  "contact_email" TEXT NOT NULL,
  "hmac_secret" TEXT NOT NULL,
  "scopes" TEXT[] NOT NULL DEFAULT '{}',
  "active" BOOLEAN NOT NULL DEFAULT true,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "partner_organizations_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "partner_webhooks" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "partner_id" UUID NOT NULL,
  "url" TEXT NOT NULL,
  "events" TEXT[] NOT NULL DEFAULT '{"column.published"}',
  "active" BOOLEAN NOT NULL DEFAULT true,
  "last_status" INTEGER,
  "last_delivered_at" TIMESTAMP(3),
  "failure_count" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "partner_webhooks_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "partner_webhooks_partner_active_idx" ON "partner_webhooks"("partner_id", "active");
ALTER TABLE "partner_webhooks" ADD CONSTRAINT "partner_webhooks_partner_id_fkey"
  FOREIGN KEY ("partner_id") REFERENCES "partner_organizations"("id");

-- RLS: drafts/pending/rejected are tenant-scoped. Published columns are
-- additionally readable through the public feed (separate, no-auth route).
-- Approvers and approval requests are tenant-scoped.
-- Partners and partner webhooks are platform-level (not tenant-scoped) and
-- managed by platform admins; RLS not applied here.
ALTER TABLE "columns" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "column_approvers" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "approval_requests" ENABLE ROW LEVEL SECURITY;

-- For columns, the tenant policy lets tenant members see all states; a
-- separate "public_published" policy allows reads of published columns
-- without tenant context (used by the public feed handler).
CREATE POLICY "tenant_isolation" ON "columns"
  USING (
    tenant_id::text = current_setting('app.tenant_id', true)
    OR (state = 'published' AND current_setting('app.tenant_id', true) = '')
  );
CREATE POLICY "tenant_isolation" ON "column_approvers"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "approval_requests"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "columns" FORCE ROW LEVEL SECURITY;
ALTER TABLE "column_approvers" FORCE ROW LEVEL SECURITY;
ALTER TABLE "approval_requests" FORCE ROW LEVEL SECURITY;
