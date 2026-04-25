import { randomUUID } from 'node:crypto';
import { Worker } from 'bullmq';
import IORedis from 'ioredis';
import pino from 'pino';

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

const worker = new Worker(
  'sdgi-default',
  async (job) => {
    const log = baseLogger.child({
      job_id: job.id,
      job_name: job.name,
      request_id: (job.data as { requestId?: string } | undefined)?.requestId ?? randomUUID(),
    });
    log.info('processing job');
    return { ok: true };
  },
  { connection },
);

worker.on('failed', (job, err) => {
  baseLogger.error({ job_id: job?.id, err: err.message }, 'job failed');
});

worker.on('completed', (job) => {
  baseLogger.info({ job_id: job.id, name: job.name }, 'job completed');
});

baseLogger.info('worker started');

async function shutdown(signal: string): Promise<void> {
  baseLogger.info({ signal }, 'shutting down');
  await worker.close();
  await connection.quit();
  process.exit(0);
}

process.on('SIGTERM', () => void shutdown('SIGTERM'));
process.on('SIGINT', () => void shutdown('SIGINT'));
