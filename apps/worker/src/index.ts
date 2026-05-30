import { randomUUID } from 'node:crypto';
import { Queue, Worker } from 'bullmq';
import IORedis from 'ioredis';
import pino from 'pino';
import { pickScanner } from './scanners/scanner';

const baseLogger = pino({
  name: 'worker',
  level: process.env.LOG_LEVEL ?? 'info',
  base: {
    service: 'worker',
    env: process.env.NODE_ENV ?? 'development',
  },
  redact: {
    paths: ['data.password', 'data.passwordHash', 'data.token'],
    remove: true,
  },
});

const connection = new IORedis(process.env.REDIS_URL ?? 'redis://localhost:6379', {
  maxRetriesPerRequest: null,
});

const QUEUE = 'sdgi-default';
const queue = new Queue(QUEUE, { connection });

const worker = new Worker(
  QUEUE,
  async (job) => {
    const log = baseLogger.child({
      job_id: job.id,
      job_name: job.name,
      request_id: (job.data as { requestId?: string } | undefined)?.requestId ?? randomUUID(),
    });

    if (job.name === 'sdg-watch:scan-source') {
      // ADR-0012: scan a single source. Fanned-out by the weekly job.
      const data = job.data as {
        sourceId: string;
        url: string;
        feedUrl: string | null;
        kind: string;
        language: string;
        region: string | null;
        sdgFocus: string[];
      };
      const scanner = pickScanner(data.kind);
      const findings = await scanner.scan(data);
      log.info({ source_id: data.sourceId, count: findings.length }, 'source scanned');
      return { findings: findings.length };
    }

    if (job.name === 'sdg-watch:weekly-fanout') {
      // The recurring job — placeholder while service-to-service auth is set up.
      // Will eventually call api `GET /v1/watch/sources?active=true` and enqueue
      // one `sdg-watch:scan-source` job per source.
      log.info('weekly fan-out triggered');
      return { ok: true };
    }

    if (job.name === 'columns:generate-candidates') {
      // ADR-0013: every weekday morning, build candidate columns from the
      // most recently discovered watch items that pass CONTENT_STANDARD §8.
      // Today the worker only emits the schedule signal; api-side curator
      // tools then create drafts in their tenant scope.
      log.info('daily column candidate generation tick');
      return { ok: true };
    }

    if (job.name === 'stories:generate-daily') {
      // ADR-0015: each morning, fan out short-story variant generation for
      // yesterday's published columns. The fan-out itself is performed on
      // the api side under tenant context; this worker job is the schedule
      // anchor and (later) the trigger for service-to-service requests.
      log.info('daily short-story generation tick');
      return { ok: true };
    }

    if (job.name === 'stories:dispatch-post') {
      // Stub for outbound platform posting. Real platform integrations live
      // here (YouTube Data API v3, Meta Graph, TikTok, etc.). For now we
      // record the intent and exit successfully so retry policy is testable.
      const data = job.data as { postId: string; platform: string };
      log.info({ post_id: data.postId, platform: data.platform }, 'platform post dispatched (stub)');
      return { ok: true };
    }

    if (job.name === 'partner-webhook:dispatch') {
      // Outbound HMAC-signed webhook to a partner. Retries with exponential
      // backoff are handled by BullMQ's job options (set when enqueued).
      const data = job.data as {
        deliveryId: string;
        url: string;
        secret: string;
        body: string;
        event: string;
      };
      const { signWebhookBody } = await import('./signing/webhook');
      const sig = signWebhookBody(data.secret, data.body);
      const res = await fetch(data.url, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-sdgi-signature': sig,
          'x-sdgi-event': data.event,
          'x-sdgi-delivery': data.deliveryId,
          'user-agent': 'SDGI-Webhook/1.0 (+https://sdgi.app)',
        },
        body: data.body,
      });
      if (!res.ok) {
        throw new Error(`partner returned ${res.status}`);
      }
      log.info({ delivery_id: data.deliveryId, status: res.status }, 'webhook delivered');
      return { ok: true, status: res.status };
    }

    log.warn({ name: job.name }, 'unknown job; no-op');
    return { ok: true };
  },
  { connection },
);

// Register the recurring jobs once on startup. Idempotent — fixed jobIds.
async function registerSchedules(): Promise<void> {
  // Weekly watch fan-out — Mondays 06:00 UTC.
  await queue.add(
    'sdg-watch:weekly-fanout',
    {},
    {
      repeat: { pattern: '0 6 * * MON', tz: 'UTC' },
      jobId: 'sdg-watch:weekly-fanout',
      removeOnComplete: { count: 50 },
      removeOnFail: { count: 50 },
    },
  );
  baseLogger.info('weekly fan-out scheduled (Mon 06:00 UTC)');

  // Daily column candidate generation — weekdays 05:00 UTC.
  await queue.add(
    'columns:generate-candidates',
    {},
    {
      repeat: { pattern: '0 5 * * 1-5', tz: 'UTC' },
      jobId: 'columns:generate-candidates',
      removeOnComplete: { count: 50 },
      removeOnFail: { count: 50 },
    },
  );
  baseLogger.info('daily column candidate generation scheduled (Mon-Fri 05:00 UTC)');

  // Daily short-story variant generation — every day 06:30 UTC, after the
  // column candidate fan-out so newly-published columns have time to settle.
  await queue.add(
    'stories:generate-daily',
    {},
    {
      repeat: { pattern: '30 6 * * *', tz: 'UTC' },
      jobId: 'stories:generate-daily',
      removeOnComplete: { count: 50 },
      removeOnFail: { count: 50 },
    },
  );
  baseLogger.info('daily short-story variant generation scheduled (06:30 UTC)');
}

worker.on('failed', (job, err) => {
  baseLogger.error({ job_id: job?.id, err: err.message }, 'job failed');
});
worker.on('completed', (job) => {
  baseLogger.info({ job_id: job.id, name: job.name }, 'job completed');
});

baseLogger.info('worker started');
void registerSchedules().catch((err) => {
  baseLogger.error(
    { err: err instanceof Error ? err.message : String(err) },
    'schedule registration failed',
  );
});

async function shutdown(signal: string): Promise<void> {
  baseLogger.info({ signal }, 'shutting down');
  await worker.close();
  await queue.close();
  await connection.quit();
  process.exit(0);
}

process.on('SIGTERM', () => void shutdown('SIGTERM'));
process.on('SIGINT', () => void shutdown('SIGINT'));
