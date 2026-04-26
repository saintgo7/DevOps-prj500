-- ADR-0017: research authoring + book authoring + impact verification

-- ============================================================
-- Research manuscripts
-- ============================================================

CREATE TABLE "research_manuscripts" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "tier" TEXT NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "plain_language_summary" JSONB,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "applicable_regions" TEXT[] NOT NULL DEFAULT '{}',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "submitted_at" TIMESTAMP(3),
  "accepted_at" TIMESTAMP(3),
  "published_at" TIMESTAMP(3),
  "withdrawn_at" TIMESTAMP(3),
  "withdraw_reason" TEXT,
  "doi" TEXT,
  "frozen_citations" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "research_manuscripts_pkey" PRIMARY KEY ("id"),
  -- Tier guard: only the two tiers we currently support ship into the data.
  CONSTRAINT "research_manuscripts_tier_check"
    CHECK ("tier" IN ('nature','ssci')),
  -- State machine guard. Service must move through allowed transitions; the
  -- DB only enforces that no garbage state ever lands.
  CONSTRAINT "research_manuscripts_state_check"
    CHECK ("state" IN ('draft','internal_review','external_peer_review',
                       'revise_requested','accepted','published','withdrawn'))
);
CREATE INDEX "research_manuscripts_tenant_state_idx"
  ON "research_manuscripts"("tenant_id", "state", "created_at");
CREATE INDEX "research_manuscripts_sdg_idx"
  ON "research_manuscripts" USING GIN ("sdg_focus");

CREATE TABLE "manuscript_coauthors" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "manuscript_id" UUID NOT NULL,
  "display_name" TEXT NOT NULL,
  "orcid" TEXT,
  "contact_email" TEXT,
  "affiliation" TEXT,
  "credit_roles" TEXT[] NOT NULL DEFAULT '{}',
  "ldc_affiliated" BOOLEAN NOT NULL DEFAULT false,
  "position" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "manuscript_coauthors_pkey" PRIMARY KEY ("id"),
  -- Either ORCID or (contact_email AND affiliation) must be present so we
  -- can reach the author for corrections / errata.
  CONSTRAINT "manuscript_coauthors_contact_check"
    CHECK ("orcid" IS NOT NULL
           OR ("contact_email" IS NOT NULL AND "affiliation" IS NOT NULL))
);
CREATE UNIQUE INDEX "manuscript_coauthors_manuscript_position_key"
  ON "manuscript_coauthors"("manuscript_id", "position");
CREATE INDEX "manuscript_coauthors_manuscript_idx"
  ON "manuscript_coauthors"("manuscript_id");
ALTER TABLE "manuscript_coauthors" ADD CONSTRAINT "manuscript_coauthors_manuscript_id_fkey"
  FOREIGN KEY ("manuscript_id") REFERENCES "research_manuscripts"("id");

CREATE TABLE "manuscript_citations" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "manuscript_id" UUID NOT NULL,
  "position" INTEGER NOT NULL,
  "source_column_id" UUID,
  "source_manuscript_id" UUID,
  "source_patent_insight_id" UUID,
  "source_watch_item_id" UUID,
  "external_doi" TEXT,
  "external_url" TEXT,
  "rendered" TEXT NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "manuscript_citations_pkey" PRIMARY KEY ("id"),
  -- Exactly one source selector must be set. This guarantees a citation
  -- always points at exactly one canonical thing — no ambiguity, no orphans.
  CONSTRAINT "manuscript_citations_one_source_check"
    CHECK (
      (("source_column_id" IS NOT NULL)::int
       + ("source_manuscript_id" IS NOT NULL)::int
       + ("source_patent_insight_id" IS NOT NULL)::int
       + ("source_watch_item_id" IS NOT NULL)::int
       + ("external_doi" IS NOT NULL)::int
       + ("external_url" IS NOT NULL)::int) = 1
    )
);
CREATE UNIQUE INDEX "manuscript_citations_manuscript_position_key"
  ON "manuscript_citations"("manuscript_id", "position");
CREATE INDEX "manuscript_citations_manuscript_idx"
  ON "manuscript_citations"("manuscript_id");
ALTER TABLE "manuscript_citations" ADD CONSTRAINT "manuscript_citations_manuscript_id_fkey"
  FOREIGN KEY ("manuscript_id") REFERENCES "research_manuscripts"("id");

-- ============================================================
-- Books
-- ============================================================

CREATE TABLE "book_projects" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "applicable_regions" TEXT[] NOT NULL DEFAULT '{}',
  "license" TEXT NOT NULL DEFAULT 'CC-BY-NC-SA-4.0',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "published_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "book_projects_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "book_projects_state_check"
    CHECK ("state" IN ('draft','review','published','retired'))
);
CREATE INDEX "book_projects_tenant_state_idx"
  ON "book_projects"("tenant_id", "state", "created_at");

CREATE TABLE "book_chapters" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "book_id" UUID NOT NULL,
  "position" INTEGER NOT NULL,
  "header_i18n" JSONB NOT NULL,
  "source_column_id" UUID,
  "source_manuscript_id" UUID,
  "source_short_story_id" UUID,
  "source_watch_digest_id" UUID,
  "source_custom" TEXT,
  "source_custom_reason" TEXT,
  "plain_language_score" INTEGER,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "book_chapters_pkey" PRIMARY KEY ("id"),
  -- Exactly one source per chapter — re-use is the rule, free-form is the
  -- exception, and the exception always carries an editor's reason.
  CONSTRAINT "book_chapters_one_source_check"
    CHECK (
      (("source_column_id" IS NOT NULL)::int
       + ("source_manuscript_id" IS NOT NULL)::int
       + ("source_short_story_id" IS NOT NULL)::int
       + ("source_watch_digest_id" IS NOT NULL)::int
       + ("source_custom" IS NOT NULL)::int) = 1
    ),
  CONSTRAINT "book_chapters_custom_reason_check"
    CHECK ("source_custom" IS NULL OR "source_custom_reason" IS NOT NULL),
  CONSTRAINT "book_chapters_pls_range_check"
    CHECK ("plain_language_score" IS NULL
           OR ("plain_language_score" >= 0 AND "plain_language_score" <= 100))
);
CREATE UNIQUE INDEX "book_chapters_book_position_key"
  ON "book_chapters"("book_id", "position");
CREATE INDEX "book_chapters_book_idx"
  ON "book_chapters"("book_id");
ALTER TABLE "book_chapters" ADD CONSTRAINT "book_chapters_book_id_fkey"
  FOREIGN KEY ("book_id") REFERENCES "book_projects"("id");
ALTER TABLE "book_chapters" ADD CONSTRAINT "book_chapters_manuscript_fk"
  FOREIGN KEY ("source_manuscript_id") REFERENCES "research_manuscripts"("id");

-- ============================================================
-- Impact verification with consent + k-anonymity floor
-- ============================================================

CREATE TABLE "impact_consent_records" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "scope" JSONB NOT NULL,
  "level" TEXT NOT NULL DEFAULT 'aggregate-only',
  "consent_version" TEXT NOT NULL,
  "agreed_clause_hash" TEXT NOT NULL,
  "expires_at" TIMESTAMP(3) NOT NULL,
  "revoked_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "impact_consent_records_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "impact_consent_records_level_check"
    CHECK ("level" IN ('aggregate-only','longitudinal'))
);
CREATE UNIQUE INDEX "impact_consent_records_tenant_user_version_key"
  ON "impact_consent_records"("tenant_id", "user_id", "consent_version");
CREATE INDEX "impact_consent_records_tenant_user_idx"
  ON "impact_consent_records"("tenant_id", "user_id");
CREATE INDEX "impact_consent_records_expires_idx"
  ON "impact_consent_records"("expires_at");
CREATE INDEX "impact_consent_records_revoked_idx"
  ON "impact_consent_records"("revoked_at");

CREATE TABLE "impact_studies" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "title" TEXT NOT NULL,
  "hypothesis" TEXT NOT NULL,
  "method" TEXT NOT NULL,
  "k_anonymity_floor" INTEGER NOT NULL DEFAULT 10,
  "sensitive_topic" BOOLEAN NOT NULL DEFAULT false,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "regions" TEXT[] NOT NULL DEFAULT '{}',
  "topic_tags" TEXT[] NOT NULL DEFAULT '{}',
  "window_start" TIMESTAMP(3) NOT NULL,
  "window_end" TIMESTAMP(3) NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "enrolled_count" INTEGER NOT NULL DEFAULT 0,
  "published_at" TIMESTAMP(3),
  "retired_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "impact_studies_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "impact_studies_state_check"
    CHECK ("state" IN ('draft','enrolling','analysing','review','published','retired')),
  -- Floor must always be at least 10. Sensitive studies bump to 25 at the
  -- service layer; the DB ensures no one can lower below 10 by mistake.
  CONSTRAINT "impact_studies_k_floor_check"
    CHECK ("k_anonymity_floor" >= 10),
  CONSTRAINT "impact_studies_window_check"
    CHECK ("window_end" > "window_start")
);
CREATE INDEX "impact_studies_tenant_state_idx"
  ON "impact_studies"("tenant_id", "state", "created_at");
CREATE INDEX "impact_studies_sdg_idx"
  ON "impact_studies" USING GIN ("sdg_focus");

CREATE TABLE "impact_observations" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "study_id" UUID NOT NULL,
  "cohort_key" JSONB NOT NULL,
  "cohort_size" INTEGER NOT NULL,
  "metric" JSONB NOT NULL,
  "release_ready" BOOLEAN NOT NULL DEFAULT false,
  "suppressed" BOOLEAN NOT NULL DEFAULT false,
  "observed_at" TIMESTAMP(3) NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "impact_observations_pkey" PRIMARY KEY ("id"),
  -- Cohort size never drops below 1 in storage. The k-anonymity *publish*
  -- gate (>= study.k_anonymity_floor) is enforced in the service layer
  -- because it is dynamic per study; here we stop only structurally invalid
  -- rows.
  CONSTRAINT "impact_observations_cohort_size_check"
    CHECK ("cohort_size" >= 1),
  -- An observation cannot be both release_ready AND suppressed.
  CONSTRAINT "impact_observations_release_xor_suppress_check"
    CHECK (NOT ("release_ready" AND "suppressed"))
);
CREATE INDEX "impact_observations_tenant_study_idx"
  ON "impact_observations"("tenant_id", "study_id", "observed_at");
ALTER TABLE "impact_observations" ADD CONSTRAINT "impact_observations_study_id_fkey"
  FOREIGN KEY ("study_id") REFERENCES "impact_studies"("id");

CREATE TABLE "impact_study_reviews" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "study_id" UUID NOT NULL,
  "reviewer_id" UUID NOT NULL,
  "decision" TEXT NOT NULL,
  "domain_expert" BOOLEAN NOT NULL DEFAULT false,
  "comment" TEXT,
  "decided_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "impact_study_reviews_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "impact_study_reviews_decision_check"
    CHECK ("decision" IN ('approve','reject','request_changes'))
);
CREATE INDEX "impact_study_reviews_tenant_study_idx"
  ON "impact_study_reviews"("tenant_id", "study_id");
CREATE INDEX "impact_study_reviews_reviewer_idx"
  ON "impact_study_reviews"("reviewer_id");
ALTER TABLE "impact_study_reviews" ADD CONSTRAINT "impact_study_reviews_study_id_fkey"
  FOREIGN KEY ("study_id") REFERENCES "impact_studies"("id");

CREATE TABLE "impact_disclosures" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "study_id" UUID NOT NULL,
  "channel" TEXT NOT NULL,
  "recipient" TEXT,
  "disclosed_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "impact_disclosures_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "impact_disclosures_channel_check"
    CHECK ("channel" IN ('atom','webhook','export'))
);
CREATE INDEX "impact_disclosures_tenant_study_idx"
  ON "impact_disclosures"("tenant_id", "study_id");
CREATE INDEX "impact_disclosures_disclosed_idx"
  ON "impact_disclosures"("disclosed_at");
ALTER TABLE "impact_disclosures" ADD CONSTRAINT "impact_disclosures_study_id_fkey"
  FOREIGN KEY ("study_id") REFERENCES "impact_studies"("id");

-- ============================================================
-- RLS — every new table is tenant-bound and FORCE-isolated.
-- ============================================================

ALTER TABLE "research_manuscripts" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "manuscript_coauthors" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "manuscript_citations" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "book_projects"        ENABLE ROW LEVEL SECURITY;
ALTER TABLE "book_chapters"        ENABLE ROW LEVEL SECURITY;
ALTER TABLE "impact_consent_records" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "impact_studies"       ENABLE ROW LEVEL SECURITY;
ALTER TABLE "impact_observations"  ENABLE ROW LEVEL SECURITY;
ALTER TABLE "impact_study_reviews" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "impact_disclosures"   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "research_manuscripts"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "manuscript_coauthors"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "manuscript_citations"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "book_projects"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "book_chapters"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "impact_consent_records"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "impact_studies"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "impact_observations"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "impact_study_reviews"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "impact_disclosures"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "research_manuscripts" FORCE ROW LEVEL SECURITY;
ALTER TABLE "manuscript_coauthors" FORCE ROW LEVEL SECURITY;
ALTER TABLE "manuscript_citations" FORCE ROW LEVEL SECURITY;
ALTER TABLE "book_projects"        FORCE ROW LEVEL SECURITY;
ALTER TABLE "book_chapters"        FORCE ROW LEVEL SECURITY;
ALTER TABLE "impact_consent_records" FORCE ROW LEVEL SECURITY;
ALTER TABLE "impact_studies"       FORCE ROW LEVEL SECURITY;
ALTER TABLE "impact_observations"  FORCE ROW LEVEL SECURITY;
ALTER TABLE "impact_study_reviews" FORCE ROW LEVEL SECURITY;
ALTER TABLE "impact_disclosures"   FORCE ROW LEVEL SECURITY;
