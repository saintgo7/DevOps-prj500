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

    log.warn({ name: job.name }, 'unknown job; no-op');
    return { ok: true };
  },
  { connection },
);

// Register the recurring weekly job once on startup.
// Mondays 06:00 UTC. Idempotent — using a fixed jobId.
async function registerSchedules(): Promise<void> {
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
