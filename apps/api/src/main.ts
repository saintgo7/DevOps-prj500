import 'reflect-metadata';
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import cookieParser from 'cookie-parser';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule, {
    cors: { origin: process.env.WEB_ORIGIN ?? 'http://localhost:3000', credentials: true },
  });

  app.use(cookieParser());
  app.setGlobalPrefix('v1');
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
  console.log(`[api] listening on :${port}  •  docs at /docs`);
}

void bootstrap();
