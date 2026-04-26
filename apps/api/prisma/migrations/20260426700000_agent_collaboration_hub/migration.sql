-- ADR-0021: AI agent collaboration hub
-- registry / sessions / rooms / messages / digests / proposals

CREATE TABLE "agent_registrations" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "agent_key" TEXT NOT NULL,
  "name_i18n" JSONB NOT NULL,
  "operator_org" TEXT NOT NULL,
  "steward_user_id" UUID NOT NULL,
  "noncommercial_pledge" BOOLEAN NOT NULL DEFAULT false,
  "nonharm_pledge" BOOLEAN NOT NULL DEFAULT false,
  "plain_language_pledge" BOOLEAN NOT NULL DEFAULT false,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "capabilities" TEXT[] NOT NULL DEFAULT '{}',
  "working_locales" TEXT[] NOT NULL DEFAULT '{}',
  "field_regions" TEXT[] NOT NULL DEFAULT '{}',
  "homepage_url" TEXT,
  "public_key" TEXT NOT NULL,
  "manifest_hash" TEXT NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "paused_at" TIMESTAMP(3),
  "pause_reason" TEXT,
  "retired_at" TIMESTAMP(3),
  "harm_strikes" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_registrations_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_registrations_state_check"
    CHECK ("state" IN ('draft','review','active','paused','retired')),
  CONSTRAINT "agent_registrations_pledges_check"
    CHECK ("noncommercial_pledge" = true
           AND "nonharm_pledge" = true
           AND "plain_language_pledge" = true),
  CONSTRAINT "agent_registrations_pubkey_format_check"
    CHECK ("public_key" ~ '^[0-9a-f]{64}$'),
  CONSTRAINT "agent_registrations_strikes_nonneg_check"
    CHECK ("harm_strikes" >= 0)
);
CREATE UNIQUE INDEX "agent_registrations_tenant_key_key"
  ON "agent_registrations"("tenant_id", "agent_key");
CREATE INDEX "agent_registrations_tenant_state_idx"
  ON "agent_registrations"("tenant_id", "state");
CREATE INDEX "agent_registrations_sdg_idx"
  ON "agent_registrations" USING GIN ("sdg_focus");
ALTER TABLE "agent_registrations" ADD CONSTRAINT "agent_registrations_steward_fk"
  FOREIGN KEY ("steward_user_id") REFERENCES "users"("id");

CREATE TABLE "agent_sessions" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "agent_id" UUID NOT NULL,
  "started_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "last_heartbeat_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "ended_at" TIMESTAMP(3),
  "state" TEXT NOT NULL DEFAULT 'started',
  "current_task_i18n" JSONB,
  "events_emitted" INTEGER NOT NULL DEFAULT 0,
  "harm_strikes" INTEGER NOT NULL DEFAULT 0,
  CONSTRAINT "agent_sessions_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_sessions_state_check"
    CHECK ("state" IN ('started','idle','busy','ended','crashed'))
);
CREATE INDEX "agent_sessions_tenant_agent_idx"
  ON "agent_sessions"("tenant_id", "agent_id", "started_at");
CREATE INDEX "agent_sessions_state_heartbeat_idx"
  ON "agent_sessions"("state", "last_heartbeat_at");
ALTER TABLE "agent_sessions" ADD CONSTRAINT "agent_sessions_agent_id_fkey"
  FOREIGN KEY ("agent_id") REFERENCES "agent_registrations"("id");

CREATE TABLE "agent_rooms" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "topic_i18n" JSONB NOT NULL,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "kind" TEXT NOT NULL DEFAULT 'mixed',
  "public_readable" BOOLEAN NOT NULL DEFAULT false,
  "created_by" UUID NOT NULL,
  "state" TEXT NOT NULL DEFAULT 'active',
  "archived_at" TIMESTAMP(3),
  "daily_digest_enabled" BOOLEAN NOT NULL DEFAULT false,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_rooms_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_rooms_kind_check"
    CHECK ("kind" IN ('agent-only','mixed','public-readable')),
  CONSTRAINT "agent_rooms_state_check"
    CHECK ("state" IN ('active','archived')),
  -- 'public-readable' implies the flag; non-public rooms must keep it false.
  CONSTRAINT "agent_rooms_public_readable_check"
    CHECK ((NOT "public_readable") OR "kind" = 'public-readable')
);
CREATE INDEX "agent_rooms_tenant_state_idx"
  ON "agent_rooms"("tenant_id", "state", "created_at");
CREATE INDEX "agent_rooms_sdg_idx"
  ON "agent_rooms" USING GIN ("sdg_focus");

CREATE TABLE "agent_room_members" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "room_id" UUID NOT NULL,
  "agent_id" UUID,
  "user_id" UUID,
  "member_role" TEXT NOT NULL DEFAULT 'contributor',
  "joined_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_room_members_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_room_members_role_check"
    CHECK ("member_role" IN ('observer','contributor','moderator')),
  -- Exactly one principal: either an agent or a human user.
  CONSTRAINT "agent_room_members_one_principal_check"
    CHECK (
      (("agent_id" IS NOT NULL)::int + ("user_id" IS NOT NULL)::int) = 1
    )
);
CREATE INDEX "agent_room_members_tenant_room_idx"
  ON "agent_room_members"("tenant_id", "room_id");
CREATE INDEX "agent_room_members_agent_idx" ON "agent_room_members"("agent_id");
CREATE INDEX "agent_room_members_user_idx" ON "agent_room_members"("user_id");
ALTER TABLE "agent_room_members" ADD CONSTRAINT "agent_room_members_room_id_fkey"
  FOREIGN KEY ("room_id") REFERENCES "agent_rooms"("id");
ALTER TABLE "agent_room_members" ADD CONSTRAINT "agent_room_members_agent_id_fkey"
  FOREIGN KEY ("agent_id") REFERENCES "agent_registrations"("id");

CREATE TABLE "agent_messages" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "room_id" UUID NOT NULL,
  "sender_agent_id" UUID,
  "sender_user_id" UUID,
  "original_text" TEXT NOT NULL,
  "original_locale" TEXT NOT NULL,
  "translations" JSONB,
  "kind" TEXT NOT NULL DEFAULT 'chat',
  "signature" TEXT,
  "harm_report" JSONB,
  "posted_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_messages_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_messages_kind_check"
    CHECK ("kind" IN ('chat','proposal','observation','data-handoff')),
  CONSTRAINT "agent_messages_one_sender_check"
    CHECK (
      (("sender_agent_id" IS NOT NULL)::int + ("sender_user_id" IS NOT NULL)::int) = 1
    ),
  -- Agent senders must carry a signature.
  CONSTRAINT "agent_messages_agent_signature_check"
    CHECK ("sender_agent_id" IS NULL OR "signature" IS NOT NULL)
);
CREATE INDEX "agent_messages_tenant_room_posted_idx"
  ON "agent_messages"("tenant_id", "room_id", "posted_at");
CREATE INDEX "agent_messages_sender_agent_idx" ON "agent_messages"("sender_agent_id");
CREATE INDEX "agent_messages_sender_user_idx" ON "agent_messages"("sender_user_id");
ALTER TABLE "agent_messages" ADD CONSTRAINT "agent_messages_room_id_fkey"
  FOREIGN KEY ("room_id") REFERENCES "agent_rooms"("id");
ALTER TABLE "agent_messages" ADD CONSTRAINT "agent_messages_sender_agent_id_fkey"
  FOREIGN KEY ("sender_agent_id") REFERENCES "agent_registrations"("id");

CREATE TABLE "agent_daily_digests" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "room_id" UUID,
  "digest_date" DATE NOT NULL,
  "summary_i18n" JSONB NOT NULL,
  "source_message_ids" TEXT[] NOT NULL DEFAULT '{}',
  "ai_provenance" JSONB,
  "state" TEXT NOT NULL DEFAULT 'draft',
  "approved_at" TIMESTAMP(3),
  "approved_by" UUID,
  "published_at" TIMESTAMP(3),
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_daily_digests_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_daily_digests_state_check"
    CHECK ("state" IN ('draft','human_review','published','rejected'))
);
CREATE UNIQUE INDEX "agent_daily_digests_tenant_room_date_key"
  ON "agent_daily_digests"("tenant_id", "room_id", "digest_date");
CREATE INDEX "agent_daily_digests_tenant_state_idx"
  ON "agent_daily_digests"("tenant_id", "state", "digest_date");
ALTER TABLE "agent_daily_digests" ADD CONSTRAINT "agent_daily_digests_room_id_fkey"
  FOREIGN KEY ("room_id") REFERENCES "agent_rooms"("id");

CREATE TABLE "agent_collaboration_proposals" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "proposer_agent_id" UUID,
  "proposer_user_id" UUID,
  "recipient_agent_id" UUID,
  "recipient_user_id" UUID,
  "subject_i18n" JSONB NOT NULL,
  "context_i18n" JSONB NOT NULL,
  "noncommercial_notice" BOOLEAN NOT NULL DEFAULT false,
  "state" TEXT NOT NULL DEFAULT 'suggested',
  "proposer_steward_accepted_at" TIMESTAMP(3),
  "recipient_steward_accepted_at" TIMESTAMP(3),
  "declined_reason" TEXT,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "agent_collaboration_proposals_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "agent_collaboration_proposals_state_check"
    CHECK ("state" IN ('suggested','recipient_review','accepted',
                       'engaged','completed','declined','cancelled')),
  CONSTRAINT "agent_collaboration_proposals_noncommercial_check"
    CHECK ("noncommercial_notice" = true),
  CONSTRAINT "agent_collaboration_proposals_one_proposer_check"
    CHECK (
      (("proposer_agent_id" IS NOT NULL)::int + ("proposer_user_id" IS NOT NULL)::int) = 1
    ),
  CONSTRAINT "agent_collaboration_proposals_one_recipient_check"
    CHECK (
      (("recipient_agent_id" IS NOT NULL)::int + ("recipient_user_id" IS NOT NULL)::int) = 1
    )
);
CREATE INDEX "agent_collab_proposals_tenant_state_idx"
  ON "agent_collaboration_proposals"("tenant_id", "state");
CREATE INDEX "agent_collab_proposals_recipient_agent_idx"
  ON "agent_collaboration_proposals"("recipient_agent_id");
CREATE INDEX "agent_collab_proposals_proposer_agent_idx"
  ON "agent_collaboration_proposals"("proposer_agent_id");
ALTER TABLE "agent_collaboration_proposals" ADD CONSTRAINT "agent_collab_proposals_proposer_agent_fk"
  FOREIGN KEY ("proposer_agent_id") REFERENCES "agent_registrations"("id");
ALTER TABLE "agent_collaboration_proposals" ADD CONSTRAINT "agent_collab_proposals_recipient_agent_fk"
  FOREIGN KEY ("recipient_agent_id") REFERENCES "agent_registrations"("id");

-- ============================================================
-- RLS — every new table tenant-bound and FORCE-isolated.
-- ============================================================

ALTER TABLE "agent_registrations"            ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_sessions"                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_rooms"                    ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_room_members"             ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_messages"                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_daily_digests"            ENABLE ROW LEVEL SECURITY;
ALTER TABLE "agent_collaboration_proposals"  ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "agent_registrations"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_sessions"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_rooms"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_room_members"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_messages"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_daily_digests"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "agent_collaboration_proposals"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "agent_registrations"            FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_sessions"                 FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_rooms"                    FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_room_members"             FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_messages"                 FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_daily_digests"            FORCE ROW LEVEL SECURITY;
ALTER TABLE "agent_collaboration_proposals"  FORCE ROW LEVEL SECURITY;
