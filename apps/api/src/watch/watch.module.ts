import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { FeedController } from './feed.controller';
import { WatchController } from './watch.controller';
import { WatchService } from './watch.service';

@Module({
  imports: [AuthModule],
  controllers: [WatchController, FeedController],
  providers: [WatchService],
  exports: [WatchService],
})
export class WatchModule {}
