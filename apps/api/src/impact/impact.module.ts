import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { ConsentService } from './consent.service';
import { ImpactController } from './impact.controller';
import { StudiesService } from './studies.service';

@Module({
  imports: [AuthModule],
  controllers: [ImpactController],
  providers: [ConsentService, StudiesService],
  exports: [ConsentService, StudiesService],
})
export class ImpactModule {}
