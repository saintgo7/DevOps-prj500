import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { FeasibilityController } from './feasibility.controller';
import { FeasibilityService } from './feasibility.service';

@Module({
  imports: [AuthModule],
  controllers: [FeasibilityController],
  providers: [FeasibilityService],
  exports: [FeasibilityService],
})
export class FeasibilityModule {}
