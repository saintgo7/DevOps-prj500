-- ADR-0015: short-form video stories + multilingual variants + distribution

CREATE TABLE "short_stories" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "source_column_id" UUID NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'drafting',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "region" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "short_stories_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "short_stories_tenant_state_idx" ON "short_stories"("tenant_id", "state", "created_at");
CREATE INDEX "short_stories_source_idx" ON "short_stories"("source_column_id");
CREATE INDEX "short_stories_sdg_idx" ON "short_stories" USING GIN ("sdg_focus");

CREATE TABLE "story_variants" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "short_story_id" UUID NOT NULL,
  "locale" TEXT NOT NULL,
  "age_tier" TEXT NOT NULL,
  "caption" TEXT NOT NULL,
  "hooks" TEXT[] NOT NULL DEFAULT '{}',
  "cta_text" TEXT,
  "hashtags" TEXT[] NOT NULL DEFAULT '{}',
  "storyboard" JSONB NOT NULL,
  "attribution" TEXT NOT NULL DEFAULT 'ai-assisted',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "safety_report" JSONB,
  "approved_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "story_variants_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "story_variants_story_locale_age_key"
  ON "story_variants"("short_story_id", "locale", "age_tier");
CREATE INDEX "story_variants_tenant_state_idx" ON "story_variants"("tenant_id", "state", "created_at");
ALTER TABLE "story_variants" ADD CONSTRAINT "story_variants_short_story_id_fkey"
  FOREIGN KEY ("short_story_id") REFERENCES "short_stories"("id");

CREATE TABLE "distribution_targets" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "platform" TEXT NOT NULL,
  "account_handle" TEXT NOT NULL,
  "credential_ref" TEXT,
  "active" BOOLEAN NOT NULL DEFAULT true,
  "policy" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "distribution_targets_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "distribution_targets_tenant_platform_handle_key"
  ON "distribution_targets"("tenant_id", "platform", "account_handle");
CREATE INDEX "distribution_targets_tenant_active_idx" ON "distribution_targets"("tenant_id", "active");

CREATE TABLE "distribution_posts" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "variant_id" UUID NOT NULL,
  "target_id" UUID NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'ready',
  "scheduled_for" TIMESTAMP(3),
  "posted_at" TIMESTAMP(3),
  "retracted_at" TIMESTAMP(3),
  "external_post_id" TEXT,
  "external_url" TEXT,
  "metrics" JSONB,
  "metrics_updated_at" TIMESTAMP(3),
  "last_error" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "distribution_posts_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "distribution_posts_variant_target_key"
  ON "distribution_posts"("variant_id", "target_id");
CREATE INDEX "distribution_posts_tenant_state_idx"
  ON "distribution_posts"("tenant_id", "state", "scheduled_for");
ALTER TABLE "distribution_posts" ADD CONSTRAINT "distribution_posts_variant_id_fkey"
  FOREIGN KEY ("variant_id") REFERENCES "story_variants"("id");
ALTER TABLE "distribution_posts" ADD CONSTRAINT "distribution_posts_target_id_fkey"
  FOREIGN KEY ("target_id") REFERENCES "distribution_targets"("id");

-- All four tables tenant-scoped — RLS for isolation.
ALTER TABLE "short_stories" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "story_variants" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "distribution_targets" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "distribution_posts" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "short_stories"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "story_variants"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "distribution_targets"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "distribution_posts"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "short_stories" FORCE ROW LEVEL SECURITY;
ALTER TABLE "story_variants" FORCE ROW LEVEL SECURITY;
ALTER TABLE "distribution_targets" FORCE ROW LEVEL SECURITY;
ALTER TABLE "distribution_posts" FORCE ROW LEVEL SECURITY;
