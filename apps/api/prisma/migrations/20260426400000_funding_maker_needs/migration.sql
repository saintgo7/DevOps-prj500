-- ADR-0018: funding (crowdfunding/impact investment) + maker space + needs/offers/matching

-- ============================================================
-- Funding
-- ============================================================

CREATE TABLE "funding_proposals" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "region" TEXT NOT NULL,
  "funding_model" TEXT NOT NULL,
  "contribution_kinds" TEXT[] NOT NULL,
  "currency" TEXT NOT NULL DEFAULT 'USD',
  "soft_goal_minor" INTEGER NOT NULL,
  "hard_goal_minor" INTEGER NOT NULL,
  "raised_minor" INTEGER NOT NULL DEFAULT 0,
  "contributor_count" INTEGER NOT NULL DEFAULT 0,
  "ends_at" TIMESTAMP(3) NOT NULL,
  "noncommercial_notice" BOOLEAN NOT NULL DEFAULT false,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "cancelled_at" TIMESTAMP(3),
  "cancel_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "funding_proposals_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "funding_proposals_noncommercial_check"
    CHECK ("noncommercial_notice" = true),
  CONSTRAINT "funding_proposals_funding_model_check"
    CHECK ("funding_model" IN ('all-or-nothing','keep-it-all')),
  CONSTRAINT "funding_proposals_state_check"
    CHECK ("state" IN ('draft','review','live','funding_locked','completed',
                       'reported','cancelled','refunded','paused')),
  CONSTRAINT "funding_proposals_goal_order_check"
    CHECK ("soft_goal_minor" <= "hard_goal_minor"),
  CONSTRAINT "funding_proposals_goal_positive_check"
    CHECK ("soft_goal_minor" > 0 AND "hard_goal_minor" > 0),
  CONSTRAINT "funding_proposals_raised_nonneg_check"
    CHECK ("raised_minor" >= 0)
);
CREATE INDEX "funding_proposals_tenant_state_idx"
  ON "funding_proposals"("tenant_id", "state", "created_at");
CREATE INDEX "funding_proposals_sdg_idx"
  ON "funding_proposals" USING GIN ("sdg_focus");
CREATE INDEX "funding_proposals_region_idx"
  ON "funding_proposals"("region");

CREATE TABLE "funding_milestones" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposal_id" UUID NOT NULL,
  "position" INTEGER NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "amount_minor" INTEGER NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'pending',
  "evidence_url" TEXT,
  "evidence_hash" TEXT,
  "released_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "funding_milestones_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "funding_milestones_state_check"
    CHECK ("state" IN ('pending','evidence_submitted','released','rejected')),
  CONSTRAINT "funding_milestones_amount_pos_check"
    CHECK ("amount_minor" > 0)
);
CREATE UNIQUE INDEX "funding_milestones_proposal_position_key"
  ON "funding_milestones"("proposal_id", "position");
CREATE INDEX "funding_milestones_proposal_idx"
  ON "funding_milestones"("proposal_id");
ALTER TABLE "funding_milestones" ADD CONSTRAINT "funding_milestones_proposal_id_fkey"
  FOREIGN KEY ("proposal_id") REFERENCES "funding_proposals"("id");

CREATE TABLE "funding_contributions" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposal_id" UUID NOT NULL,
  "backer_user_id" UUID,
  "kind" TEXT NOT NULL,
  "amount_minor" INTEGER NOT NULL,
  "currency" TEXT NOT NULL,
  "visibility" TEXT NOT NULL DEFAULT 'private',
  "payment_provider_ref" TEXT,
  "state" TEXT NOT NULL DEFAULT 'pending',
  "refunded_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "funding_contributions_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "funding_contributions_kind_check"
    CHECK ("kind" IN ('donation','impact-investment','in-kind')),
  CONSTRAINT "funding_contributions_state_check"
    CHECK ("state" IN ('pending','collected','refunded','failed')),
  CONSTRAINT "funding_contributions_visibility_check"
    CHECK ("visibility" IN ('public','pseudonymous','private')),
  CONSTRAINT "funding_contributions_amount_pos_check"
    CHECK ("amount_minor" > 0)
);
CREATE INDEX "funding_contributions_tenant_proposal_idx"
  ON "funding_contributions"("tenant_id", "proposal_id");
CREATE INDEX "funding_contributions_backer_idx"
  ON "funding_contributions"("backer_user_id");
CREATE INDEX "funding_contributions_state_idx"
  ON "funding_contributions"("state");
ALTER TABLE "funding_contributions" ADD CONSTRAINT "funding_contributions_proposal_id_fkey"
  FOREIGN KEY ("proposal_id") REFERENCES "funding_proposals"("id");

CREATE TABLE "funding_reports" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposal_id" UUID NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "impact_study_id" UUID,
  "published_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "funding_reports_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "funding_reports_tenant_proposal_idx"
  ON "funding_reports"("tenant_id", "proposal_id");
ALTER TABLE "funding_reports" ADD CONSTRAINT "funding_reports_proposal_id_fkey"
  FOREIGN KEY ("proposal_id") REFERENCES "funding_proposals"("id");

CREATE TABLE "funding_flags" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposal_id" UUID NOT NULL,
  "reporter_id" UUID NOT NULL,
  "category" TEXT NOT NULL,
  "reason" TEXT NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "funding_flags_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "funding_flags_category_check"
    CHECK ("category" IN ('fraud','commercial','harm','misinformation','other'))
);
CREATE INDEX "funding_flags_tenant_proposal_idx"
  ON "funding_flags"("tenant_id", "proposal_id");
ALTER TABLE "funding_flags" ADD CONSTRAINT "funding_flags_proposal_id_fkey"
  FOREIGN KEY ("proposal_id") REFERENCES "funding_proposals"("id");

-- ============================================================
-- Maker space
-- ============================================================

CREATE TABLE "maker_templates" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID,
  "kind" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "license_spdx" TEXT NOT NULL,
  "description_i18n" JSONB NOT NULL,
  "source_ref" TEXT NOT NULL,
  "active" BOOLEAN NOT NULL DEFAULT true,
  "retired_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "maker_templates_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "maker_templates_kind_check"
    CHECK ("kind" IN ('static-site','next-app','pwa','mobile-rn',
                      'data-dashboard','sms-bot','whatsapp-bot'))
);
CREATE INDEX "maker_templates_kind_active_idx"
  ON "maker_templates"("kind", "active");

CREATE TABLE "maker_projects" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "template_id" UUID NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "target_regions" TEXT[] NOT NULL DEFAULT '{}',
  "state" TEXT NOT NULL DEFAULT 'scaffolding',
  "noncommercial_notice" BOOLEAN NOT NULL DEFAULT false,
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "live_at" TIMESTAMP(3),
  "archived_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "maker_projects_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "maker_projects_state_check"
    CHECK ("state" IN ('scaffolding','building','review','live','archived','paused'))
);
CREATE INDEX "maker_projects_tenant_state_idx"
  ON "maker_projects"("tenant_id", "state", "created_at");
CREATE INDEX "maker_projects_sdg_idx"
  ON "maker_projects" USING GIN ("sdg_focus");
ALTER TABLE "maker_projects" ADD CONSTRAINT "maker_projects_template_id_fkey"
  FOREIGN KEY ("template_id") REFERENCES "maker_templates"("id");

CREATE TABLE "maker_contributors" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "project_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "role" TEXT NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "maker_contributors_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "maker_contributors_role_check"
    CHECK ("role" IN ('maintainer','editor','translator','tester'))
);
CREATE UNIQUE INDEX "maker_contributors_project_user_role_key"
  ON "maker_contributors"("project_id", "user_id", "role");
CREATE INDEX "maker_contributors_project_idx"
  ON "maker_contributors"("project_id");
ALTER TABLE "maker_contributors" ADD CONSTRAINT "maker_contributors_project_id_fkey"
  FOREIGN KEY ("project_id") REFERENCES "maker_projects"("id");

CREATE TABLE "maker_artifacts" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "project_id" UUID NOT NULL,
  "kind" TEXT NOT NULL,
  "ref" TEXT NOT NULL,
  "content_hash" TEXT NOT NULL,
  "ai_provenance" JSONB,
  "readme_score" INTEGER,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "maker_artifacts_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "maker_artifacts_kind_check"
    CHECK ("kind" IN ('repo','bundle','preview')),
  CONSTRAINT "maker_artifacts_score_range_check"
    CHECK ("readme_score" IS NULL
           OR ("readme_score" >= 0 AND "readme_score" <= 100))
);
CREATE INDEX "maker_artifacts_project_idx"
  ON "maker_artifacts"("project_id");
ALTER TABLE "maker_artifacts" ADD CONSTRAINT "maker_artifacts_project_id_fkey"
  FOREIGN KEY ("project_id") REFERENCES "maker_projects"("id");

-- ============================================================
-- Needs / Offers / Match
-- ============================================================

CREATE TABLE "need_requests" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "category" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "region" TEXT NOT NULL,
  "subregion" TEXT,
  "quantity" INTEGER NOT NULL,
  "unit" TEXT NOT NULL,
  "urgency" TEXT NOT NULL DEFAULT 'normal',
  "needed_by" TIMESTAMP(3) NOT NULL,
  "verification_level" TEXT NOT NULL DEFAULT 'unverified',
  "verified_by" UUID,
  "verified_at" TIMESTAMP(3),
  "state" TEXT NOT NULL DEFAULT 'draft',
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "closed_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "need_requests_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "need_requests_category_check"
    CHECK ("category" IN ('relief','supplies','equipment','knowledge','volunteers')),
  CONSTRAINT "need_requests_urgency_check"
    CHECK ("urgency" IN ('critical','high','normal','low')),
  CONSTRAINT "need_requests_state_check"
    CHECK ("state" IN ('draft','published','matching','fulfilled','closed',
                       'cancelled','expired','paused')),
  CONSTRAINT "need_requests_verification_check"
    CHECK ("verification_level" IN ('verified','community-vouched','unverified')),
  CONSTRAINT "need_requests_quantity_pos_check"
    CHECK ("quantity" > 0)
);
CREATE INDEX "need_requests_tenant_state_idx"
  ON "need_requests"("tenant_id", "state", "created_at");
CREATE INDEX "need_requests_category_region_urgency_idx"
  ON "need_requests"("category", "region", "urgency");
CREATE INDEX "need_requests_sdg_idx"
  ON "need_requests" USING GIN ("sdg_focus");

CREATE TABLE "offer_listings" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "category" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "region" TEXT NOT NULL,
  "subregion" TEXT,
  "quantity" INTEGER NOT NULL,
  "unit" TEXT NOT NULL,
  "available_until" TIMESTAMP(3) NOT NULL,
  "verification_level" TEXT NOT NULL DEFAULT 'unverified',
  "verified_by" UUID,
  "verified_at" TIMESTAMP(3),
  "state" TEXT NOT NULL DEFAULT 'draft',
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "offer_listings_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "offer_listings_category_check"
    CHECK ("category" IN ('relief','supplies','equipment','knowledge','volunteers')),
  CONSTRAINT "offer_listings_state_check"
    CHECK ("state" IN ('draft','published','matching','closed','cancelled',
                       'expired','paused')),
  CONSTRAINT "offer_listings_verification_check"
    CHECK ("verification_level" IN ('verified','community-vouched','unverified')),
  CONSTRAINT "offer_listings_quantity_pos_check"
    CHECK ("quantity" > 0)
);
CREATE INDEX "offer_listings_tenant_state_idx"
  ON "offer_listings"("tenant_id", "state", "created_at");
CREATE INDEX "offer_listings_category_region_idx"
  ON "offer_listings"("category", "region");
CREATE INDEX "offer_listings_sdg_idx"
  ON "offer_listings" USING GIN ("sdg_focus");

CREATE TABLE "need_matches" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "request_id" UUID NOT NULL,
  "offer_id" UUID NOT NULL,
  "category" TEXT NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'suggested',
  "requester_accepted_at" TIMESTAMP(3),
  "provider_accepted_at" TIMESTAMP(3),
  "cancelled_at" TIMESTAMP(3),
  "cancel_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "need_matches_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "need_matches_state_check"
    CHECK ("state" IN ('suggested','contacted','accepted','shipped',
                       'delivered','cancelled')),
  CONSTRAINT "need_matches_category_check"
    CHECK ("category" IN ('relief','supplies','equipment','knowledge','volunteers'))
);
CREATE UNIQUE INDEX "need_matches_request_offer_key"
  ON "need_matches"("request_id", "offer_id");
CREATE INDEX "need_matches_tenant_state_idx"
  ON "need_matches"("tenant_id", "state");
ALTER TABLE "need_matches" ADD CONSTRAINT "need_matches_request_id_fkey"
  FOREIGN KEY ("request_id") REFERENCES "need_requests"("id");
ALTER TABLE "need_matches" ADD CONSTRAINT "need_matches_offer_id_fkey"
  FOREIGN KEY ("offer_id") REFERENCES "offer_listings"("id");

CREATE TABLE "need_fulfillments" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "match_id" UUID NOT NULL,
  "tracking_ref" TEXT,
  "evidence_hashes" TEXT[] NOT NULL DEFAULT '{}',
  "requester_signed_at" TIMESTAMP(3),
  "provider_signed_at" TIMESTAMP(3),
  "agreed_clause_hash" TEXT NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "need_fulfillments_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "need_fulfillments_match_key" ON "need_fulfillments"("match_id");
CREATE INDEX "need_fulfillments_tenant_idx" ON "need_fulfillments"("tenant_id");
ALTER TABLE "need_fulfillments" ADD CONSTRAINT "need_fulfillments_match_id_fkey"
  FOREIGN KEY ("match_id") REFERENCES "need_matches"("id");

-- ============================================================
-- RLS — every new table tenant-bound and FORCE-isolated.
-- maker_templates allows NULL tenant_id for global platform templates.
-- ============================================================

ALTER TABLE "funding_proposals"     ENABLE ROW LEVEL SECURITY;
ALTER TABLE "funding_milestones"    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "funding_contributions" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "funding_reports"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "funding_flags"         ENABLE ROW LEVEL SECURITY;
ALTER TABLE "maker_templates"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "maker_projects"        ENABLE ROW LEVEL SECURITY;
ALTER TABLE "maker_contributors"    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "maker_artifacts"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "need_requests"         ENABLE ROW LEVEL SECURITY;
ALTER TABLE "offer_listings"        ENABLE ROW LEVEL SECURITY;
ALTER TABLE "need_matches"          ENABLE ROW LEVEL SECURITY;
ALTER TABLE "need_fulfillments"     ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "funding_proposals"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "funding_milestones"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "funding_contributions"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "funding_reports"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "funding_flags"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "maker_templates"
  USING (tenant_id IS NULL OR tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "maker_projects"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "maker_contributors"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "maker_artifacts"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "need_requests"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "offer_listings"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "need_matches"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "need_fulfillments"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "funding_proposals"     FORCE ROW LEVEL SECURITY;
ALTER TABLE "funding_milestones"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "funding_contributions" FORCE ROW LEVEL SECURITY;
ALTER TABLE "funding_reports"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "funding_flags"         FORCE ROW LEVEL SECURITY;
ALTER TABLE "maker_templates"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "maker_projects"        FORCE ROW LEVEL SECURITY;
ALTER TABLE "maker_contributors"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "maker_artifacts"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "need_requests"         FORCE ROW LEVEL SECURITY;
ALTER TABLE "offer_listings"        FORCE ROW LEVEL SECURITY;
ALTER TABLE "need_matches"          FORCE ROW LEVEL SECURITY;
ALTER TABLE "need_fulfillments"     FORCE ROW LEVEL SECURITY;
