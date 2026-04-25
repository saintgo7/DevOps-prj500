import {
  Body,
  Controller,
  Get,
  HttpCode,
  Post,
  Req,
  Res,
  UseGuards,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import type { Request, Response } from 'express';
import { AuthService } from './auth.service';
import { AuthSessionDto, SignInDto, SignUpDto, UserDto } from './dto';
import { JwtAuthGuard, AuthenticatedRequest } from './jwt-auth.guard';

const COOKIE_NAME = 'sdgi_session';
const COOKIE_OPTS = {
  httpOnly: true,
  sameSite: 'lax' as const,
  secure: process.env.NODE_ENV === 'production',
  path: '/',
};

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(private readonly auth: AuthService) {}

  @Post('signup')
  @HttpCode(201)
  @ApiOperation({ summary: 'Create a new tenant + admin user' })
  @ApiResponse({ status: 201, type: AuthSessionDto })
  async signUp(@Body() dto: SignUpDto, @Res({ passthrough: true }) res: Response): Promise<AuthSessionDto> {
    const session = await this.auth.signUp(dto);
    res.cookie(COOKIE_NAME, session.token, {
      ...COOKIE_OPTS,
      expires: session.expiresAt,
    });
    return { user: session.user, expiresAt: session.expiresAt.toISOString() };
  }

  @Post('signin')
  @HttpCode(200)
  @ApiOperation({ summary: 'Sign in with email + password' })
  @ApiResponse({ status: 200, type: AuthSessionDto })
  async signIn(@Body() dto: SignInDto, @Res({ passthrough: true }) res: Response): Promise<AuthSessionDto> {
    const session = await this.auth.signIn(dto);
    res.cookie(COOKIE_NAME, session.token, {
      ...COOKIE_OPTS,
      expires: session.expiresAt,
    });
    return { user: session.user, expiresAt: session.expiresAt.toISOString() };
  }

  @Post('signout')
  @HttpCode(204)
  @ApiOperation({ summary: 'Clear the session cookie' })
  signOut(@Res({ passthrough: true }) res: Response): void {
    res.clearCookie(COOKIE_NAME, COOKIE_OPTS);
  }
}

@ApiTags('me')
@Controller('me')
export class MeController {
  constructor(private readonly auth: AuthService) {}

  @Get()
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Get the current user (cookie or Bearer token)' })
  @ApiResponse({ status: 200, type: UserDto })
  async me(@Req() req: Request): Promise<UserDto> {
    const auth = (req as AuthenticatedRequest).auth;
    if (!auth) throw new Error('JwtAuthGuard not applied');
    return this.auth.getMe(auth.userId);
  }
}
