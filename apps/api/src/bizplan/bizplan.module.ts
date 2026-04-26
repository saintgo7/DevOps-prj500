import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { BizPlanController } from './bizplan.controller';
import { BizPlanService } from './bizplan.service';

@Module({
  imports: [AuthModule],
  controllers: [BizPlanController],
  providers: [BizPlanService],
  exports: [BizPlanService],
})
export class BizPlanModule {}
