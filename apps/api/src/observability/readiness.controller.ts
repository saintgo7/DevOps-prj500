import { Controller, Get, ServiceUnavailableException } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { SkipThrottle } from '@nestjs/throttler';
import { PrismaService } from '../prisma/prisma.service';

@ApiTags('health')
@SkipThrottle()
@Controller('ready')
export class ReadinessController {
  constructor(private readonly prisma: PrismaService) {}

  @Get()
  @ApiOperation({
    summary: 'Readiness probe — verifies database connectivity',
  })
  async ready(): Promise<{
    status: 'ok';
    checks: { database: 'ok' };
    time: string;
  }> {
    try {
      await this.prisma.$queryRawUnsafe('SELECT 1');
    } catch {
      throw new ServiceUnavailableException({
        status: 'fail',
        checks: { database: 'fail' },
      });
    }
    return {
      status: 'ok',
      checks: { database: 'ok' },
      time: new Date().toISOString(),
    };
  }
}
