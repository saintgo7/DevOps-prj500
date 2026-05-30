import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { NeedsController } from './needs.controller';
import { NeedsService } from './needs.service';

@Module({
  imports: [AuthModule],
  controllers: [NeedsController],
  providers: [NeedsService],
  exports: [NeedsService],
})
export class NeedsModule {}
