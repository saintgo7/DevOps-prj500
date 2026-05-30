-- ADR-0014: origin field, integrity report, research proposals, expert outreach, chat

-- Origin field (default 'external' so existing rows are classified as curated)
ALTER TABLE "columns" ADD COLUMN "origin" TEXT NOT NULL DEFAULT 'external';
ALTER TABLE "columns" ALTER COLUMN "primary_locale" SET DEFAULT 'ko';
ALTER TABLE "columns" ADD COLUMN "integrity_report" JSONB;
CREATE INDEX "columns_origin_state_idx" ON "columns"("origin", "state");

-- Research proposals (RLS-bound)
CREATE TABLE "research_proposals" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "owner_id" UUID NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "body_i18n" JSONB NOT NULL,
  "primary_locale" TEXT NOT NULL DEFAULT 'ko',
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "inspired_by_item_ids" TEXT[] NOT NULL DEFAULT '{}',
  "inspired_by_column_ids" TEXT[] NOT NULL DEFAULT '{}',
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "research_proposals_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "research_proposals_tenant_state_idx" ON "research_proposals"("tenant_id", "state", "created_at");
CREATE INDEX "research_proposals_owner_idx" ON "research_proposals"("owner_id");

-- Expert outreach drafts (RLS-bound). Stays "draft" until human explicitly sends.
CREATE TABLE "expert_outreaches" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposal_id" UUID NOT NULL,
  "expert_name" TEXT NOT NULL,
  "expert_org" TEXT,
  "expert_email" TEXT,
  "draft_message" TEXT NOT NULL,
  "draft_locale" TEXT NOT NULL DEFAULT 'en',
  "state" TEXT NOT NULL DEFAULT 'draft',
  "sent_at" TIMESTAMP(3),
  "consent_record" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "expert_outreaches_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "expert_outreaches_tenant_proposal_idx" ON "expert_outreaches"("tenant_id", "proposal_id");
CREATE INDEX "expert_outreaches_state_idx" ON "expert_outreaches"("state");
ALTER TABLE "expert_outreaches" ADD CONSTRAINT "expert_outreaches_proposal_id_fkey"
  FOREIGN KEY ("proposal_id") REFERENCES "research_proposals"("id");

-- Chat (RLS-bound)
CREATE TABLE "conversations" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "topic" TEXT,
  "members" JSONB NOT NULL,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "archived_at" TIMESTAMP(3),
  CONSTRAINT "conversations_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "conversations_tenant_idx" ON "conversations"("tenant_id", "created_at");

CREATE TABLE "messages" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "conversation_id" UUID NOT NULL,
  "author_id" UUID NOT NULL,
  "original_text" TEXT NOT NULL,
  "original_locale" TEXT NOT NULL,
  "translations" JSONB,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "messages_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "messages_conversation_idx" ON "messages"("tenant_id", "conversation_id", "created_at");
ALTER TABLE "messages" ADD CONSTRAINT "messages_conversation_id_fkey"
  FOREIGN KEY ("conversation_id") REFERENCES "conversations"("id");

-- RLS for new tables
ALTER TABLE "research_proposals" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "expert_outreaches" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "conversations" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "messages" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "research_proposals"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "expert_outreaches"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "conversations"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "messages"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "research_proposals" FORCE ROW LEVEL SECURITY;
ALTER TABLE "expert_outreaches" FORCE ROW LEVEL SECURITY;
ALTER TABLE "conversations" FORCE ROW LEVEL SECURITY;
ALTER TABLE "messages" FORCE ROW LEVEL SECURITY;
