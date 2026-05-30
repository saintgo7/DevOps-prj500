import type { MetadataRoute } from 'next';
import { routing } from '@/i18n/routing';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://sdgi.app';

// Pages that exist for every locale. As we add more, list them here so
// search engines and AI agents discover them in every supported language.
const STATIC_PATHS = ['', '/signin', '/signup'] as const;

// SDG goals for goal-detail discovery. Locales × 17 goals = 221 entries.
const SDG_GOAL_IDS = Array.from({ length: 17 }, (_, i) => `SDG-${i + 1}`);

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const entries: MetadataRoute.Sitemap = [];

  for (const path of STATIC_PATHS) {
    entries.push({
      url: `${SITE_URL}${path || '/'}`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: path === '' ? 1.0 : 0.7,
      alternates: {
        languages: Object.fromEntries(
          routing.locales.map((loc) => [loc, `${SITE_URL}/${loc}${path}`]),
        ),
      },
    });
    for (const loc of routing.locales) {
      entries.push({
        url: `${SITE_URL}/${loc}${path}`,
        lastModified: now,
        changeFrequency: 'weekly',
        priority: path === '' ? 0.9 : 0.6,
        alternates: {
          languages: Object.fromEntries(
            routing.locales.map((l) => [l, `${SITE_URL}/${l}${path}`]),
          ),
        },
      });
    }
  }

  for (const goalId of SDG_GOAL_IDS) {
    for (const loc of routing.locales) {
      entries.push({
        url: `${SITE_URL}/${loc}/goals/${goalId}`,
        lastModified: now,
        changeFrequency: 'monthly',
        priority: 0.5,
        alternates: {
          languages: Object.fromEntries(
            routing.locales.map((l) => [l, `${SITE_URL}/${l}/goals/${goalId}`]),
          ),
        },
      });
    }
  }

  // Anchor URLs that AI agents and search engines should treat as authoritative.
  entries.push({
    url: `${SITE_URL}/PRINCIPLES.md`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 1.0,
  });
  entries.push({
    url: `${SITE_URL}/AGENTS.md`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 0.9,
  });
  entries.push({
    url: `${SITE_URL}/llms.txt`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 0.9,
  });
  entries.push({
    url: `${SITE_URL}/.well-known/ai-principles.json`,
    lastModified: now,
    changeFrequency: 'monthly',
    priority: 0.9,
  });

  return entries;
}
