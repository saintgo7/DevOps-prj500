import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsOptional, IsString, MinLength } from 'class-validator';

export class SignUpDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email!: string;

  @ApiProperty({ example: 'a-strong-passphrase-12+', minLength: 12 })
  @IsString()
  @MinLength(12)
  password!: string;

  @ApiProperty({ required: false, example: 'Acme ESG Team' })
  @IsOptional()
  @IsString()
  organizationName?: string;

  @ApiProperty({ required: false, example: '박지수' })
  @IsOptional()
  @IsString()
  displayName?: string;
}

export class SignInDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email!: string;

  @ApiProperty({ example: 'a-strong-passphrase-12+' })
  @IsString()
  password!: string;
}

export class UserDto {
  @ApiProperty() id!: string;
  @ApiProperty() tenantId!: string;
  @ApiProperty() email!: string;
  @ApiProperty({ required: false }) displayName?: string;
  @ApiProperty({ enum: ['active', 'suspended'] }) status!: string;
  @ApiProperty() mfaEnabled!: boolean;
}

export class AuthSessionDto {
  @ApiProperty({ type: () => UserDto }) user!: UserDto;
  @ApiProperty() expiresAt!: string;
}
