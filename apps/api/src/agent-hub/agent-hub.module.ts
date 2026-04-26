import { Module } from '@nestjs/common';
import { AuthModule } from '../auth/auth.module';
import { AgentHubController } from './agent-hub.controller';
import { AgentCollabService } from './collab.service';
import { AgentDigestService } from './digest.service';
import { AgentRegistryService } from './registry.service';
import { AgentRoomsService } from './rooms.service';

@Module({
  imports: [AuthModule],
  controllers: [AgentHubController],
  providers: [
    AgentRegistryService,
    AgentRoomsService,
    AgentDigestService,
    AgentCollabService,
  ],
  exports: [
    AgentRegistryService,
    AgentRoomsService,
    AgentDigestService,
    AgentCollabService,
  ],
})
export class AgentHubModule {}
