-- Identity & Tenancy
CREATE TABLE "tenants" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "name" TEXT NOT NULL,
  "region" TEXT NOT NULL DEFAULT 'kr',
  "plan" TEXT NOT NULL DEFAULT 'starter',
  "status" TEXT NOT NULL DEFAULT 'active',
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "tenants_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "users" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "email" TEXT NOT NULL,
  "display_name" TEXT,
  "auth_provider" TEXT NOT NULL DEFAULT 'local',
  "mfa_enabled" BOOLEAN NOT NULL DEFAULT false,
  "status" TEXT NOT NULL DEFAULT 'active',
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "users_tenant_id_email_key" ON "users"("tenant_id", "email");
CREATE INDEX "users_tenant_id_status_idx" ON "users"("tenant_id", "status");

CREATE TABLE "roles" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "key" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  CONSTRAINT "roles_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "roles_key_key" ON "roles"("key");

CREATE TABLE "memberships" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "role_id" UUID NOT NULL,
  CONSTRAINT "memberships_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "memberships_tenant_id_user_id_role_id_key" ON "memberships"("tenant_id", "user_id", "role_id");

CREATE TABLE "audit_events" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID,
  "actor_id" UUID,
  "action" TEXT NOT NULL,
  "resource_type" TEXT NOT NULL,
  "resource_id" TEXT,
  "before" JSONB,
  "after" JSONB,
  "occurred_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "audit_events_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "audit_events_tenant_id_occurred_at_idx" ON "audit_events"("tenant_id", "occurred_at");
CREATE INDEX "audit_events_resource_type_resource_id_idx" ON "audit_events"("resource_type", "resource_id");

ALTER TABLE "users" ADD CONSTRAINT "users_tenant_id_fkey" FOREIGN KEY ("tenant_id") REFERENCES "tenants"("id");
ALTER TABLE "memberships" ADD CONSTRAINT "memberships_tenant_id_fkey" FOREIGN KEY ("tenant_id") REFERENCES "tenants"("id");
ALTER TABLE "memberships" ADD CONSTRAINT "memberships_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id");
ALTER TABLE "memberships" ADD CONSTRAINT "memberships_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "roles"("id");
ALTER TABLE "audit_events" ADD CONSTRAINT "audit_events_tenant_id_fkey" FOREIGN KEY ("tenant_id") REFERENCES "tenants"("id");
ALTER TABLE "audit_events" ADD CONSTRAINT "audit_events_actor_id_fkey" FOREIGN KEY ("actor_id") REFERENCES "users"("id");

-- SDG catalog (global)
CREATE TABLE "sdg_goals" (
  "id" TEXT NOT NULL,
  "number" INTEGER NOT NULL,
  "name_i18n" JSONB NOT NULL,
  "color" TEXT NOT NULL,
  "icon" TEXT,
  CONSTRAINT "sdg_goals_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "sdg_goals_number_key" ON "sdg_goals"("number");

CREATE TABLE "sdg_targets" (
  "id" TEXT NOT NULL,
  "goal_id" TEXT NOT NULL,
  "text_i18n" JSONB NOT NULL,
  "type" TEXT NOT NULL DEFAULT 'outcome',
  CONSTRAINT "sdg_targets_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "sdg_targets_goal_id_idx" ON "sdg_targets"("goal_id");
ALTER TABLE "sdg_targets" ADD CONSTRAINT "sdg_targets_goal_id_fkey" FOREIGN KEY ("goal_id") REFERENCES "sdg_goals"("id");

CREATE TABLE "sdg_indicators" (
  "id" TEXT NOT NULL,
  "target_id" TEXT NOT NULL,
  "unit" TEXT NOT NULL,
  "methodology" TEXT,
  "tier" INTEGER NOT NULL,
  CONSTRAINT "sdg_indicators_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "sdg_indicators_target_id_idx" ON "sdg_indicators"("target_id");
ALTER TABLE "sdg_indicators" ADD CONSTRAINT "sdg_indicators_target_id_fkey" FOREIGN KEY ("target_id") REFERENCES "sdg_targets"("id");

-- Row-Level Security: enforce tenant isolation on all tenant-scoped tables.
-- Application sets `app.tenant_id` via SET LOCAL per request.
ALTER TABLE "users" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "memberships" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "audit_events" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "users"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

CREATE POLICY "tenant_isolation" ON "memberships"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

CREATE POLICY "tenant_isolation" ON "audit_events"
  USING (tenant_id IS NULL OR tenant_id::text = current_setting('app.tenant_id', true));

-- Bypass policy when no tenant context is set (e.g. system jobs, migrations).
-- We force RLS so even table owners obey the policy unless they bypass via role.
ALTER TABLE "users" FORCE ROW LEVEL SECURITY;
ALTER TABLE "memberships" FORCE ROW LEVEL SECURITY;
ALTER TABLE "audit_events" FORCE ROW LEVEL SECURITY;
