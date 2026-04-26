import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { CustomDomainsService } from './custom-domains.service';
import { EventsService } from './events.service';
import { ExtensibilityController } from './extensibility.controller';
import { FeatureFlagsService } from './feature-flags.service';
import { PluginsService } from './plugins.service';
import { SubscriptionsService } from './subscriptions.service';

@Module({
  imports: [AuthModule],
  controllers: [ExtensibilityController],
  providers: [
    PluginsService,
    EventsService,
    CustomDomainsService,
    SubscriptionsService,
    FeatureFlagsService,
  ],
  exports: [
    PluginsService,
    EventsService,
    CustomDomainsService,
    SubscriptionsService,
    FeatureFlagsService,
  ],
})
export class ExtensibilityModule {}
