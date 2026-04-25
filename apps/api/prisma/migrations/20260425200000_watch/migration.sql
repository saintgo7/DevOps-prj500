-- Weekly Global SDG Watch (ADR-0012)

CREATE TABLE "watch_sources" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "name" TEXT NOT NULL,
  "url" TEXT NOT NULL,
  "feed_url" TEXT,
  "kind" TEXT NOT NULL,
  "category" TEXT NOT NULL,
  "language" TEXT NOT NULL DEFAULT 'en',
  "region" TEXT,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "active" BOOLEAN NOT NULL DEFAULT true,
  "last_scanned_at" TIMESTAMP(3),
  "failure_count" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "watch_sources_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "watch_sources_url_key" ON "watch_sources"("url");
CREATE INDEX "watch_sources_category_active_idx" ON "watch_sources"("category", "active");
CREATE INDEX "watch_sources_language_idx" ON "watch_sources"("language");

CREATE TABLE "watch_items" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "source_id" UUID NOT NULL,
  "url" TEXT NOT NULL,
  "title" TEXT NOT NULL,
  "summary" TEXT,
  "language" TEXT NOT NULL DEFAULT 'en',
  "published_at" TIMESTAMP(3),
  "discovered_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sdg_focus" TEXT[] NOT NULL DEFAULT '{}',
  "region" TEXT,
  "content_hash" TEXT NOT NULL,
  "i18n_summary" JSONB,
  CONSTRAINT "watch_items_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "watch_items_content_hash_key" ON "watch_items"("content_hash");
CREATE INDEX "watch_items_source_id_discovered_at_idx" ON "watch_items"("source_id", "discovered_at");
CREATE INDEX "watch_items_sdg_focus_idx" ON "watch_items" USING GIN ("sdg_focus");
ALTER TABLE "watch_items" ADD CONSTRAINT "watch_items_source_id_fkey" FOREIGN KEY ("source_id") REFERENCES "watch_sources"("id");

CREATE TABLE "watch_subscriptions" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "name" TEXT NOT NULL DEFAULT 'My weekly watch',
  "filter" JSONB NOT NULL,
  "digest_language" TEXT NOT NULL DEFAULT 'en',
  "active" BOOLEAN NOT NULL DEFAULT true,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "watch_subscriptions_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "watch_subscriptions_tenant_id_user_id_active_idx" ON "watch_subscriptions"("tenant_id", "user_id", "active");

CREATE TABLE "collaboration_interests" (
  "id" UUID NOT NULL DEFAULT gen_random_uuid(),
  "tenant_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "item_id" UUID NOT NULL,
  "note" TEXT,
  "intent" TEXT NOT NULL DEFAULT 'learn',
  "contact_consent" BOOLEAN NOT NULL DEFAULT false,
  "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "collaboration_interests_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "collaboration_interests_tenant_user_item_key"
  ON "collaboration_interests"("tenant_id", "user_id", "item_id");
CREATE INDEX "collaboration_interests_item_id_idx" ON "collaboration_interests"("item_id");
ALTER TABLE "collaboration_interests" ADD CONSTRAINT "collaboration_interests_item_id_fkey"
  FOREIGN KEY ("item_id") REFERENCES "watch_items"("id");

-- RLS: subscriptions and collaboration interests are personal — only the
-- owning tenant ever sees them. Sources and items are global (no RLS): they
-- benefit every tenant and feed public RSS/Atom anyway.
ALTER TABLE "watch_subscriptions" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "collaboration_interests" ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON "watch_subscriptions"
  USING (tenant_id::text = current_setting('app.tenant_id', true));
CREATE POLICY "tenant_isolation" ON "collaboration_interests"
  USING (tenant_id::text = current_setting('app.tenant_id', true));

ALTER TABLE "watch_subscriptions" FORCE ROW LEVEL SECURITY;
ALTER TABLE "collaboration_interests" FORCE ROW LEVEL SECURITY;
