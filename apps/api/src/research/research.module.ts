import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { ManuscriptsController } from './manuscripts.controller';
import { ManuscriptsService } from './manuscripts.service';

@Module({
  imports: [AuthModule],
  controllers: [ManuscriptsController],
  providers: [ManuscriptsService],
  exports: [ManuscriptsService],
})
export class ResearchModule {}
