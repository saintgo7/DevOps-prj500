import { Injectable, NestMiddleware } from '@nestjs/common';
import { randomUUID } from 'node:crypto';
import type { NextFunction, Request, Response } from 'express';

declare module 'express' {
  interface Request {
    requestId?: string;
  }
}

const HEADER = 'x-request-id';
const REQUEST_ID_RE = /^[A-Za-z0-9_.-]{8,128}$/;

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    const incoming = req.header(HEADER);
    const id = incoming && REQUEST_ID_RE.test(incoming) ? incoming : randomUUID();
    req.requestId = id;
    res.setHeader(HEADER, id);
    next();
  }
}
