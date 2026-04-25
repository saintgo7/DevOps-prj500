import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { CatalogModule } from './catalog/catalog.module';
import { HealthController } from './health/health.controller';
import { PrismaModule } from './prisma/prisma.module';
import { TenantContextMiddleware } from './tenant/tenant-context.middleware';

@Module({
  imports: [PrismaModule, CatalogModule],
  controllers: [HealthController],
  providers: [],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(TenantContextMiddleware).forRoutes('*');
  }
}
