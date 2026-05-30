-- ADR-0019: AI BizPlan + multidisciplinary feasibility + expert matching

-- ============================================================
-- BizPlan + sections + source refs + feasibility
-- ============================================================

CREATE TABLE "biz_plans" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "track" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "applicable_regions" TEXT[] NOT NULL DEFAULT '{}',
  "period_months" INTEGER NOT NULL,
  "audience_label" TEXT,
  "state" TEXT NOT NULL DEFAULT 'drafting',
  "noncommercial_notice" BOOLEAN NOT NULL DEFAULT false,
  "ready_for_use_at" TIMESTAMP(3),
  "archived_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "biz_plans_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "biz_plans_track_check"
    CHECK ("track" IN ('business','policy','pledge','investment','oda','execution','management')),
  CONSTRAINT "biz_plans_state_check"
    CHECK ("state" IN ('drafting','ai_drafted','human_review','revising','ready_for_use','archived')),
  CONSTRAINT "biz_plans_noncommercial_check"
    CHECK ("noncommercial_notice" = true),
  CONSTRAINT "biz_plans_period_pos_check"
    CHECK ("period_months" > 0)
);
CREATE INDEX "biz_plans_tenant_state_idx"
  ON "biz_plans"("tenant_id", "state", "created_at");
CREATE INDEX "biz_plans_sdg_idx"
  ON "biz_plans" USING GIN ("sdg_focus");
CREATE INDEX "biz_plans_track_idx"
  ON "biz_plans"("track");

CREATE TABLE "biz_plan_sections" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plan_id" UUID NOT NULL,
  "position" INTEGER NOT NULL,
  "kind" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "plain_language_score" INTEGER,
  "ai_provenance" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "biz_plan_sections_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "biz_plan_sections_kind_check"
    CHECK ("kind" IN (
      'executive_summary','problem_statement','solution',
      'theory_of_change','beneficiaries','budget','timeline',
      'risk','monitoring','sustainability','partners'
    )),
  CONSTRAINT "biz_plan_sections_pls_range_check"
    CHECK ("plain_language_score" IS NULL
           OR ("plain_language_score" >= 0 AND "plain_language_score" <= 100))
);
CREATE UNIQUE INDEX "biz_plan_sections_plan_kind_key"
  ON "biz_plan_sections"("plan_id", "kind");
CREATE INDEX "biz_plan_sections_plan_idx"
  ON "biz_plan_sections"("plan_id");
ALTER TABLE "biz_plan_sections" ADD CONSTRAINT "biz_plan_sections_plan_id_fkey"
  FOREIGN KEY ("plan_id") REFERENCES "biz_plans"("id");

CREATE TABLE "biz_plan_source_refs" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "section_id" UUID NOT NULL,
  "position" INTEGER NOT NULL,
  "source_watch_item_id" UUID,
  "source_column_id" UUID,
  "source_patent_insight_id" UUID,
  "source_manuscript_id" UUID,
  "external_doi" TEXT,
  "external_url" TEXT,
  "rendered" TEXT NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "biz_plan_source_refs_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "biz_plan_source_refs_one_source_check"
    CHECK (
      (("source_watch_item_id" IS NOT NULL)::int
       + ("source_column_id" IS NOT NULL)::int
       + ("source_patent_insight_id" IS NOT NULL)::int
       + ("source_manuscript_id" IS NOT NULL)::int
       + ("external_doi" IS NOT NULL)::int
       + ("external_url" IS NOT NULL)::int) = 1
    )
);
CREATE UNIQUE INDEX "biz_plan_source_refs_section_position_key"
  ON "biz_plan_source_refs"("section_id", "position");
CREATE INDEX "biz_plan_source_refs_section_idx"
  ON "biz_plan_source_refs"("section_id");
ALTER TABLE "biz_plan_source_refs" ADD CONSTRAINT "biz_plan_source_refs_section_id_fkey"
  FOREIGN KEY ("section_id") REFERENCES "biz_plan_sections"("id");

CREATE TABLE "biz_plan_feasibility" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "plan_id" UUID NOT NULL,
  "feasibility_score" INTEGER NOT NULL,
  "outcome" TEXT NOT NULL,
  "review_mode" TEXT NOT NULL,
  "computed_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "biz_plan_feasibility_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "biz_plan_feasibility_score_range_check"
    CHECK ("feasibility_score" >= 0 AND "feasibility_score" <= 100),
  CONSTRAINT "biz_plan_feasibility_outcome_check"
    CHECK ("outcome" IN ('pass','fail')),
  CONSTRAINT "biz_plan_feasibility_review_mode_check"
    CHECK ("review_mode" IN ('deterministic-only','human-adjusted'))
);
CREATE UNIQUE INDEX "biz_plan_feasibility_plan_key" ON "biz_plan_feasibility"("plan_id");
CREATE INDEX "biz_plan_feasibility_tenant_plan_idx"
  ON "biz_plan_feasibility"("tenant_id", "plan_id");
ALTER TABLE "biz_plan_feasibility" ADD CONSTRAINT "biz_plan_feasibility_plan_id_fkey"
  FOREIGN KEY ("plan_id") REFERENCES "biz_plans"("id");

CREATE TABLE "feasibility_axis_scores" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "feasibility_id" UUID NOT NULL,
  "axis" TEXT NOT NULL,
  "score" INTEGER NOT NULL,
  "rationale" JSONB NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "feasibility_axis_scores_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "feasibility_axis_scores_axis_check"
    CHECK ("axis" IN ('impact','financial','technical','legal','ethical','evidence')),
  CONSTRAINT "feasibility_axis_scores_score_range_check"
    CHECK ("score" >= 0 AND "score" <= 100)
);
CREATE UNIQUE INDEX "feasibility_axis_scores_feas_axis_key"
  ON "feasibility_axis_scores"("feasibility_id", "axis");
CREATE INDEX "feasibility_axis_scores_feas_idx"
  ON "feasibility_axis_scores"("feasibility_id");
ALTER TABLE "feasibility_axis_scores" ADD CONSTRAINT "feasibility_axis_scores_feasibility_id_fkey"
  FOREIGN KEY ("feasibility_id") REFERENCES "biz_plan_feasibility"("id");

CREATE TABLE "feasibility_reviews" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "feasibility_id" UUID NOT NULL,
  "reviewer_id" UUID NOT NULL,
  "decision" TEXT NOT NULL,
  "domain_expert" BOOLEAN NOT NULL DEFAULT false,
  "comment" TEXT,
  "decided_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "feasibility_reviews_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "feasibility_reviews_decision_check"
    CHECK ("decision" IN ('approve','request_changes','reject'))
);
CREATE INDEX "feasibility_reviews_tenant_feas_idx"
  ON "feasibility_reviews"("tenant_id", "feasibility_id");
CREATE INDEX "feasibility_reviews_reviewer_idx"
  ON "feasibility_reviews"("reviewer_id");
ALTER TABLE "feasibility_reviews" ADD CONSTRAINT "feasibility_reviews_feasibility_id_fkey"
  FOREIGN KEY ("feasibility_id") REFERENCES "biz_plan_feasibility"("id");

-- ============================================================
-- Expert profiles + credentials + matches
-- ============================================================

CREATE TABLE "expert_profiles" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "headline_i18n" JSONB NOT NULL,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "working_locales" TEXT[] NOT NULL DEFAULT '{}',
  "field_regions" TEXT[] NOT NULL DEFAULT '{}',
  "availability" TEXT NOT NULL DEFAULT 'open',
  "visibility" TEXT NOT NULL DEFAULT 'platform-only',
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "expert_profiles_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "expert_profiles_availability_check"
    CHECK ("availability" IN ('open','busy','closed')),
  CONSTRAINT "expert_profiles_visibility_check"
    CHECK ("visibility" IN ('public','platform-only','private'))
);
CREATE UNIQUE INDEX "expert_profiles_user_key" ON "expert_profiles"("user_id");
CREATE INDEX "expert_profiles_tenant_avail_idx"
  ON "expert_profiles"("tenant_id", "availability");
CREATE INDEX "expert_profiles_sdg_idx"
  ON "expert_profiles" USING GIN ("sdg_focus");
CREATE INDEX "expert_profiles_regions_idx"
  ON "expert_profiles" USING GIN ("field_regions");

CREATE TABLE "expert_credentials" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "expert_id" UUID NOT NULL,
  "kind" TEXT NOT NULL,
  "ref" TEXT NOT NULL,
  "verified_by" UUID,
  "verified_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "expert_credentials_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "expert_credentials_kind_check"
    CHECK ("kind" IN ('orcid','linkedin','official_org','community-vouched','self-reported','verified')),
  -- Hard rule: 'verified' kind requires verified_by + verified_at to be set.
  -- Self-reporting as 'verified' is rejected at the database layer.
  CONSTRAINT "expert_credentials_verified_requires_verifier_check"
    CHECK ("kind" <> 'verified'
           OR ("verified_by" IS NOT NULL AND "verified_at" IS NOT NULL))
);
CREATE UNIQUE INDEX "expert_credentials_expert_kind_ref_key"
  ON "expert_credentials"("expert_id", "kind", "ref");
CREATE INDEX "expert_credentials_expert_idx"
  ON "expert_credentials"("expert_id");
ALTER TABLE "expert_credentials" ADD CONSTRAINT "expert_credentials_expert_id_fkey"
  FOREIGN KEY ("expert_id") REFERENCES "expert_profiles"("id");

CREATE TABLE "expert_matches" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "expert_id" UUID NOT NULL,
  "subject_kind" TEXT NOT NULL,
  "subject_id" UUID NOT NULL,
  "match_score" INTEGER NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'suggested',
  "expert_accepted_at" TIMESTAMP(3),
  "owner_accepted_at" TIMESTAMP(3),
  "declined_reason" TEXT,
  "cancel_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "expert_matches_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "expert_matches_subject_kind_check"
    CHECK ("subject_kind" IN ('bizplan','impact_study','funding_proposal','maker_project','need_request')),
  CONSTRAINT "expert_matches_state_check"
    CHECK ("state" IN ('suggested','invited','accepted','engaged','completed','declined','cancelled')),
  CONSTRAINT "expert_matches_score_range_check"
    CHECK ("match_score" >= 0 AND "match_score" <= 100)
);
CREATE UNIQUE INDEX "expert_matches_expert_subject_key"
  ON "expert_matches"("expert_id", "subject_kind", "subject_id");
CREATE INDEX "expert_matches_tenant_state_idx"
  ON "expert_matches"("tenant_id", "state");
CREATE INDEX "expert_matches_subject_idx"
  ON "expert_matches"("subject_kind", "subject_id");
ALTER TABLE "expert_matches" ADD CONSTRAINT "expert_matches_expert_id_fkey"
  FOREIGN KEY ("expert_id") REFERENCES "expert_profiles"("id");
-- Note: bizplan FK is enforced at the Prisma layer (expert_matches_bizplan_fk)
-- because subject_id is polymorphic.

-- ============================================================
-- RLS — every new table tenant-bound and FORCE-isolated.
-- ============================================================

ALTER TABLE "biz_plans"               ENABLE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_sections"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_source_refs"    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_feasibility"    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "feasibility_axis_scores" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "feasibility_reviews"     ENABLE ROW LEVEL SECURITY;
ALTER TABLE "expert_profiles"         ENABLE ROW LEVEL SECURITY;
ALTER TABLE "expert_credentials"      ENABLE ROW LEVEL SECURITY;
ALTER TABLE "expert_matches"          ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "biz_plans"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "biz_plan_sections"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "biz_plan_source_refs"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "biz_plan_feasibility"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "feasibility_axis_scores"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "feasibility_reviews"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "expert_profiles"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "expert_credentials"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "expert_matches"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "biz_plans"               FORCE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_sections"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_source_refs"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "biz_plan_feasibility"    FORCE ROW LEVEL SECURITY;
ALTER TABLE "feasibility_axis_scores" FORCE ROW LEVEL SECURITY;
ALTER TABLE "feasibility_reviews"     FORCE ROW LEVEL SECURITY;
ALTER TABLE "expert_profiles"         FORCE ROW LEVEL SECURITY;
ALTER TABLE "expert_credentials"      FORCE ROW LEVEL SECURITY;
ALTER TABLE "expert_matches"          FORCE ROW LEVEL SECURITY;
