import { SetMetadata } from '@nestjs/common';

export const ROLES_METADATA_KEY = 'sdgi:required_roles';
export type RoleKey = 'admin' | 'reviewer' | 'contributor' | 'viewer' | 'auditor';

/**
 * Mark a route as requiring at least one of the listed roles.
 * Use together with `RolesGuard`. Implies `JwtAuthGuard`.
 */
export const Roles = (...roles: RoleKey[]): MethodDecorator & ClassDecorator =>
  SetMetadata(ROLES_METADATA_KEY, roles);
