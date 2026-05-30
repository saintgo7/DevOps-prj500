import { Module } from '@nestjs/common';
import { ApprovalController } from './approval.controller';
import { ColumnController } from './column.controller';
import { ColumnService } from './column.service';

@Module({
  controllers: [ColumnController, ApprovalController],
  providers: [ColumnService],
  exports: [ColumnService],
})
export class ColumnsModule {}
