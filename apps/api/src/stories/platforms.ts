// Per-platform constraints for short-form video. See ADR-0015 §4.
//
// Used by the storyboard generator and the distribution validator. Values
// are defaults for *recommended* publication — platform hard limits may be
// higher (e.g. TikTok caption can be 2,200 chars but TikTok-recommended
// hooks live in the first ~80). We stay on the conservative side.

import type { Platform } from './hashtags';
export type { Platform } from './hashtags';

export interface PlatformSpec {
  maxDurationSec: number;
  maxCaptionChars: number;
  recommendedAspect: '9:16' | '16:9' | '1:1';
  // First-N seconds to land the hook. Different from total duration.
  hookWindowSec: number;
  // Whether the platform exposes a public link to the post that we can
  // record in DistributionPost.externalUrl.
  publicUrl: boolean;
  // True if scheduling is supported via official API.
  supportsScheduling: boolean;
}

const SPECS: Record<Platform, PlatformSpec> = {
  youtube_shorts: { maxDurationSec: 60, maxCaptionChars: 100, recommendedAspect: '9:16', hookWindowSec: 3, publicUrl: true, supportsScheduling: true },
  instagram_reels: { maxDurationSec: 90, maxCaptionChars: 2200, recommendedAspect: '9:16', hookWindowSec: 3, publicUrl: true, supportsScheduling: true },
  tiktok: { maxDurationSec: 180, maxCaptionChars: 2200, recommendedAspect: '9:16', hookWindowSec: 3, publicUrl: true, supportsScheduling: true },
  x_video: { maxDurationSec: 140, maxCaptionChars: 280, recommendedAspect: '16:9', hookWindowSec: 4, publicUrl: true, supportsScheduling: false },
  facebook_reels: { maxDurationSec: 90, maxCaptionChars: 2200, recommendedAspect: '9:16', hookWindowSec: 3, publicUrl: true, supportsScheduling: true },
  linkedin_video: { maxDurationSec: 600, maxCaptionChars: 3000, recommendedAspect: '9:16', hookWindowSec: 5, publicUrl: true, supportsScheduling: true },
  kakao_clip: { maxDurationSec: 60, maxCaptionChars: 1000, recommendedAspect: '9:16', hookWindowSec: 3, publicUrl: true, supportsScheduling: false },
  weibo_video: { maxDurationSec: 600, maxCaptionChars: 2000, recommendedAspect: '9:16', hookWindowSec: 4, publicUrl: true, supportsScheduling: true },
};

export function specFor(p: Platform): PlatformSpec {
  return SPECS[p];
}

export const ALL_PLATFORMS: ReadonlyArray<Platform> = Object.keys(SPECS) as Platform[];

/**
 * Validate that a (caption, durationSec, aspectRatio) tuple is within
 * the platform's recommended constraints. Returns the list of violations
 * in plain language so curators can fix them.
 */
export function validateForPlatform(
  p: Platform,
  caption: string,
  durationSec: number,
  aspect?: string,
): string[] {
  const spec = SPECS[p];
  const v: string[] = [];
  if (caption.length > spec.maxCaptionChars) {
    v.push(`Caption is ${caption.length} chars; ${p} caps at ${spec.maxCaptionChars}.`);
  }
  if (durationSec > spec.maxDurationSec) {
    v.push(`Video is ${durationSec}s; ${p} caps at ${spec.maxDurationSec}s.`);
  }
  if (aspect && aspect !== spec.recommendedAspect) {
    v.push(`Aspect ratio ${aspect} is not the ${p} recommendation (${spec.recommendedAspect}).`);
  }
  return v;
}
