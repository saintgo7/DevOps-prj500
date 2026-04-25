import type { Params } from 'nestjs-pino';

export const loggerParams: Params = {
  pinoHttp: {
    level: process.env.LOG_LEVEL ?? 'info',
    redact: {
      paths: [
        'req.headers.authorization',
        'req.headers.cookie',
        'req.body.password',
        'req.body.passwordHash',
        'res.headers["set-cookie"]',
      ],
      remove: true,
    },
    customProps: (req) => {
      const r = req as unknown as { tenantId?: string; requestId?: string };
      return {
        service: 'api',
        env: process.env.NODE_ENV ?? 'development',
        request_id: r.requestId,
        tenant_id: r.tenantId,
      };
    },
    serializers: {
      req(req) {
        return { method: req.method, url: req.url };
      },
      res(res) {
        return { statusCode: res.statusCode };
      },
    },
    autoLogging: {
      ignore: (req) => {
        const url = (req as { url?: string }).url ?? '';
        return url === '/v1/health' || url === '/v1/ready' || url === '/metrics';
      },
    },
  },
};
