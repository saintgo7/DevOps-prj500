import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  @Get()
  check(): { status: 'ok'; service: 'api'; time: string } {
    return { status: 'ok', service: 'api', time: new Date().toISOString() };
  }
}
