import 'reflect-metadata';
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import cookieParser from 'cookie-parser';
import helmet from 'helmet';
import { Logger } from 'nestjs-pino';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule, {
    cors: { origin: process.env.WEB_ORIGIN ?? 'http://localhost:3000', credentials: true },
    bufferLogs: true,
  });
  app.useLogger(app.get(Logger));

  app.use(
    helmet({
      ...(process.env.NODE_ENV === 'production' ? {} : { contentSecurityPolicy: false }),
      crossOriginResourcePolicy: { policy: 'cross-origin' },
    }),
  );
  app.use(cookieParser());
  // Public Atom/RSS feeds and one-tap approval links live at the root URL
  // (not under /v1) so feed readers and email/SMS recipients can reach them.
  // See ADR-0012 (feeds) and ADR-0013 (approve).
  app.setGlobalPrefix('v1', {
    exclude: ['metrics', 'feed/(.*)', 'approve/(.*)'],
  });
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  // OpenAPI / Swagger
  const config = new DocumentBuilder()
    .setTitle('SDG Impact Cloud API')
    .setDescription('Multi-tenant SaaS for SDG-based impact measurement and reporting.')
    .setVersion('0.1.0')
    .addBearerAuth()
    .addCookieAuth('sdgi_session')
    .addTag('auth', 'Authentication & sessions')
    .addTag('me', 'Current user')
    .addTag('catalog', 'UN SDG catalog (goals / targets / indicators)')
    .addTag('health', 'Liveness / readiness')
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document, { useGlobalPrefix: false });

  const port = Number(process.env.PORT ?? 4000);
  await app.listen(port);
  app
    .get(Logger)
    .log(
      `[api] listening on :${port} • docs=/docs metrics=/metrics ready=/v1/ready`,
      'Bootstrap',
    );
}

void bootstrap();
