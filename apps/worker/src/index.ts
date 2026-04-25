import { Worker } from 'bullmq';
import IORedis from 'ioredis';
import pino from 'pino';

const logger = pino({ name: 'worker' });

const connection = new IORedis(process.env.REDIS_URL ?? 'redis://localhost:6379', {
  maxRetriesPerRequest: null,
});

const worker = new Worker(
  'sdgi-default',
  async (job) => {
    logger.info({ jobId: job.id, name: job.name }, 'processing job');
    return { ok: true };
  },
  { connection },
);

worker.on('failed', (job, err) => {
  logger.error({ jobId: job?.id, err: err.message }, 'job failed');
});

logger.info('worker started');
