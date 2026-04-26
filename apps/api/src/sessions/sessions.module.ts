import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { StrategyController } from './strategy.controller';
import { StrategyService } from './strategy.service';

@Module({
  imports: [AuthModule],
  controllers: [StrategyController],
  providers: [StrategyService],
  exports: [StrategyService],
})
export class SessionsModule {}
