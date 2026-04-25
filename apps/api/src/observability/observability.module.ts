import { Global, Module } from '@nestjs/common';
import { APP_INTERCEPTOR } from '@nestjs/core';
import { LoggerModule } from 'nestjs-pino';
import { loggerParams } from './logger.config';
import { MetricsController } from './metrics.controller';
import { MetricsInterceptor } from './metrics.interceptor';
import { ReadinessController } from './readiness.controller';
import { RequestIdMiddleware } from './request-id.middleware';

@Global()
@Module({
  imports: [LoggerModule.forRoot(loggerParams)],
  controllers: [MetricsController, ReadinessController],
  providers: [
    RequestIdMiddleware,
    { provide: APP_INTERCEPTOR, useClass: MetricsInterceptor },
  ],
  exports: [LoggerModule, RequestIdMiddleware],
})
export class ObservabilityModule {}
