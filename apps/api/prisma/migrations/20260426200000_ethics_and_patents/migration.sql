-- ADR-0016: trend signals + patent insights + strategy sessions + super-admin role

-- Trend signals — metadata only, NEVER third-party content. Platform-level
-- rows have tenant_id IS NULL (no RLS for those).
CREATE TABLE "trend_signals" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID,
  "platform" TEXT NOT NULL,
  "locale" TEXT NOT NULL,
  "region" TEXT,
  "hour_of_day_utc" INTEGER NOT NULL,
  "metrics" JSONB NOT NULL,
  "window_start" TIMESTAMP(3) NOT NULL,
  "window_end" TIMESTAMP(3) NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "trend_signals_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "trend_signals_platform_locale_hour_idx"
  ON "trend_signals"("platform", "locale", "hour_of_day_utc");
CREATE INDEX "trend_signals_tenant_window_idx"
  ON "trend_signals"("tenant_id", "window_end");

-- Patent insights — one curated patent + SDG mapping
CREATE TABLE "patent_insights" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "patent_number" TEXT NOT NULL,
  "jurisdiction" TEXT NOT NULL,
  "source_url" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "filed_at" TIMESTAMP(3),
  "published_at" TIMESTAMP(3),
  "inventors" TEXT[] NOT NULL DEFAULT '{}',
  "assignee" TEXT,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "applicable_regions" TEXT[] NOT NULL DEFAULT '{}',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "retired_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "patent_insights_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "patent_insights_tenant_number_jurisdiction_key"
  ON "patent_insights"("tenant_id", "patent_number", "jurisdiction");
CREATE INDEX "patent_insights_tenant_state_idx"
  ON "patent_insights"("tenant_id", "state", "created_at");
CREATE INDEX "patent_insights_sdg_idx" ON "patent_insights" USING GIN ("sdg_focus");

-- Strategy sessions — invite-only; super-admin revokes immediately
CREATE TABLE "strategy_sessions" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "insight_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "applicable_regions" TEXT[] NOT NULL DEFAULT '{}',
  "noncommercial_notice" BOOLEAN NOT NULL DEFAULT false,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "revoked_at" TIMESTAMP(3),
  "revoked_by" UUID,
  "revoke_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "strategy_sessions_pkey" PRIMARY KEY ("id"),
  -- Hard rule: noncommercial_notice MUST be true. Trying to insert/update
  -- with false is rejected at the database layer too (defence in depth).
  CONSTRAINT "strategy_sessions_noncommercial_check"
    CHECK ("noncommercial_notice" = true)
);
CREATE INDEX "strategy_sessions_tenant_state_idx"
  ON "strategy_sessions"("tenant_id", "state", "created_at");
CREATE INDEX "strategy_sessions_insight_idx" ON "strategy_sessions"("insight_id");
ALTER TABLE "strategy_sessions" ADD CONSTRAINT "strategy_sessions_insight_id_fkey"
  FOREIGN KEY ("insight_id") REFERENCES "patent_insights"("id");

-- Per-person invite — token-bearing
CREATE TABLE "session_invites" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "session_id" UUID NOT NULL,
  "invited_by" UUID NOT NULL,
  "invitee_email" TEXT NOT NULL,
  "invitee_user_id" UUID,
  "share_right" TEXT NOT NULL DEFAULT 'view',
  "expires_at" TIMESTAMP(3) NOT NULL,
  "accepted_at" TIMESTAMP(3),
  "declined_at" TIMESTAMP(3),
  "revoked_at" TIMESTAMP(3),
  "consent_record" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "session_invites_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "session_invites_session_email_key"
  ON "session_invites"("session_id", "invitee_email");
CREATE INDEX "session_invites_tenant_session_idx"
  ON "session_invites"("tenant_id", "session_id");
CREATE INDEX "session_invites_expires_idx" ON "session_invites"("expires_at");
ALTER TABLE "session_invites" ADD CONSTRAINT "session_invites_session_id_fkey"
  FOREIGN KEY ("session_id") REFERENCES "strategy_sessions"("id");

-- Seed the super-admin role (above admin). Migration is idempotent so
-- re-runs do not duplicate. Existing admins are NOT auto-promoted.
INSERT INTO "roles" ("id", "key", "name") VALUES
  (gen_random_uuid(), 'super-admin', 'Super Administrator')
ON CONFLICT ("key") DO NOTHING;

-- RLS for the four new tenant-scoped tables. Trend signals with
-- tenant_id IS NULL stay readable across tenants (platform aggregates).
ALTER TABLE "trend_signals" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "patent_insights" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "strategy_sessions" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "session_invites" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "trend_signals"
  USING (tenant_id IS NULL OR tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "patent_insights"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "strategy_sessions"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "session_invites"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "trend_signals" FORCE ROW LEVEL SECURITY;
ALTER TABLE "patent_insights" FORCE ROW LEVEL SECURITY;
ALTER TABLE "strategy_sessions" FORCE ROW LEVEL SECURITY;
ALTER TABLE "session_invites" FORCE ROW LEVEL SECURITY;
