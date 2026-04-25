import { z } from 'zod';

export const SdgGoalIdSchema = z
  .string()
  .regex(/^SDG-([1-9]|1[0-7])$/, 'Goal id must be SDG-1..SDG-17');
export type SdgGoalId = z.infer<typeof SdgGoalIdSchema>;

export const SdgTargetIdSchema = z
  .string()
  .regex(/^SDG-([1-9]|1[0-7])\.[a-z0-9]+$/i, 'Target id must be SDG-{goal}.{n}');
export type SdgTargetId = z.infer<typeof SdgTargetIdSchema>;

export const SdgIndicatorIdSchema = z
  .string()
  .regex(
    /^SDG-([1-9]|1[0-7])\.[a-z0-9]+\.[0-9]+$/i,
    'Indicator id must be SDG-{goal}.{target}.{n}',
  );
export type SdgIndicatorId = z.infer<typeof SdgIndicatorIdSchema>;

export const I18nTextSchema = z.record(z.string(), z.string());
export type I18nText = z.infer<typeof I18nTextSchema>;

export const SdgGoalSchema = z.object({
  id: SdgGoalIdSchema,
  number: z.number().int().min(1).max(17),
  name: I18nTextSchema,
  color: z.string().regex(/^#[0-9A-Fa-f]{6}$/),
});
export type SdgGoal = z.infer<typeof SdgGoalSchema>;

export const SdgTargetSchema = z.object({
  id: SdgTargetIdSchema,
  goalId: SdgGoalIdSchema,
  text: I18nTextSchema,
  type: z.enum(['outcome', 'means']),
});
export type SdgTarget = z.infer<typeof SdgTargetSchema>;

export const SdgIndicatorSchema = z.object({
  id: SdgIndicatorIdSchema,
  targetId: SdgTargetIdSchema,
  unit: z.string(),
  methodology: z.string().optional(),
  tier: z.union([z.literal(1), z.literal(2), z.literal(3)]),
});
export type SdgIndicator = z.infer<typeof SdgIndicatorSchema>;

export const ConfidenceSchema = z.number().min(0).max(1);
export type Confidence = z.infer<typeof ConfidenceSchema>;

export const VerificationStatusSchema = z.enum(['draft', 'reviewed', 'verified', 'audited']);
export type VerificationStatus = z.infer<typeof VerificationStatusSchema>;
