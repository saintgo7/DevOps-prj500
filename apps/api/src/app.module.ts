import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { APP_GUARD } from '@nestjs/core';
import { ThrottlerGuard, ThrottlerModule } from '@nestjs/throttler';
import { AgentHubModule } from './agent-hub/agent-hub.module';
import { AuditModule } from './audit/audit.module';
import { AuthModule } from './auth/auth.module';
import { BizPlanModule } from './bizplan/bizplan.module';
import { BooksModule } from './books/books.module';
import { CatalogModule } from './catalog/catalog.module';
import { ColumnsModule } from './columns/columns.module';
import { ExpertsModule } from './experts/experts.module';
import { ExtensibilityModule } from './extensibility/extensibility.module';
import { FeasibilityModule } from './feasibility/feasibility.module';
import { FundingModule } from './funding/funding.module';
import { ImpactModule } from './impact/impact.module';
import { MakerModule } from './maker/maker.module';
import { NeedsModule } from './needs/needs.module';
import { ResearchModule } from './research/research.module';
import { SessionsModule } from './sessions/sessions.module';
import { StoriesModule } from './stories/stories.module';
import { WatchModule } from './watch/watch.module';
import { HealthController } from './health/health.controller';
import { LocaleMiddleware } from './i18n/locale.middleware';
import { MonitoringModule } from './monitoring/monitoring.module';
import { ObservabilityModule } from './observability/observability.module';
import { RequestIdMiddleware } from './observability/request-id.middleware';
import { PrismaModule } from './prisma/prisma.module';
import { TenantContextMiddleware } from './tenant/tenant-context.middleware';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    ThrottlerModule.forRoot([
      { name: 'short', ttl: 1_000, limit: 20 },
      { name: 'long', ttl: 60_000, limit: 300 },
    ]),
    ObservabilityModule,
    PrismaModule,
    AgentHubModule,
    AuditModule,
    AuthModule,
    BizPlanModule,
    BooksModule,
    CatalogModule,
    ColumnsModule,
    ExpertsModule,
    ExtensibilityModule,
    FeasibilityModule,
    FundingModule,
    ImpactModule,
    MakerModule,
    MonitoringModule,
    NeedsModule,
    ResearchModule,
    SessionsModule,
    StoriesModule,
    WatchModule,
  ],
  controllers: [HealthController],
  providers: [{ provide: APP_GUARD, useClass: ThrottlerGuard }],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer
      .apply(RequestIdMiddleware, LocaleMiddleware, TenantContextMiddleware)
      .forRoutes('*');
  }
}
