import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { MakerController } from './maker.controller';
import { MakerService } from './maker.service';

@Module({
  imports: [AuthModule],
  controllers: [MakerController],
  providers: [MakerService],
  exports: [MakerService],
})
export class MakerModule {}
