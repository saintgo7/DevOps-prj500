export interface Goal {
  id: string;
  number: number;
  name: Record<string, string>;
  color: string;
  icon: string | null;
}

export interface Target {
  id: string;
  goalId: string;
  text: Record<string, string>;
  type: string;
}

export interface Indicator {
  id: string;
  targetId: string;
  unit: string;
  methodology: string | null;
  tier: number;
}

export interface ListResponse<T> {
  data: T[];
  meta: { count: number };
}

export interface ItemResponse<T> {
  data: T;
}

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:4000';

async function safeJson<T>(promise: Promise<Response>): Promise<T | null> {
  try {
    const res = await promise;
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

function localeHeaders(locale: string): Record<string, string> {
  // Map web locale to BCP-47 Accept-Language. Server respects q-weighted fallback.
  const fallbackChain: Record<string, string> = {
    ko: 'ko, en;q=0.7, ja;q=0.5, zh;q=0.3',
    en: 'en, ko;q=0.5, ja;q=0.4, zh;q=0.3',
    ja: 'ja, en;q=0.7, ko;q=0.4, zh;q=0.3',
    zh: 'zh, en;q=0.7, ja;q=0.4, ko;q=0.3',
  };
  return {
    'Accept-Language': fallbackChain[locale] ?? fallbackChain.ko ?? 'en',
  };
}

export async function fetchGoals(locale: string): Promise<Goal[]> {
  const json = await safeJson<ListResponse<Goal>>(
    fetch(`${BASE_URL}/v1/catalog/goals`, {
      headers: localeHeaders(locale),
      next: { revalidate: 60 },
    }),
  );
  return json?.data ?? [];
}

export async function fetchGoal(id: string, locale: string): Promise<Goal | null> {
  const json = await safeJson<ItemResponse<Goal>>(
    fetch(`${BASE_URL}/v1/catalog/goals/${encodeURIComponent(id)}`, {
      headers: localeHeaders(locale),
      next: { revalidate: 60 },
    }),
  );
  return json?.data ?? null;
}

export async function fetchTargets(goalId: string, locale: string): Promise<Target[]> {
  const url = new URL(`${BASE_URL}/v1/catalog/targets`);
  url.searchParams.set('goal', goalId);
  const json = await safeJson<ListResponse<Target>>(
    fetch(url.toString(), { headers: localeHeaders(locale), next: { revalidate: 60 } }),
  );
  return json?.data ?? [];
}

export async function fetchIndicators(targetId: string, locale: string): Promise<Indicator[]> {
  const url = new URL(`${BASE_URL}/v1/catalog/indicators`);
  url.searchParams.set('target', targetId);
  const json = await safeJson<ListResponse<Indicator>>(
    fetch(url.toString(), { headers: localeHeaders(locale), next: { revalidate: 60 } }),
  );
  return json?.data ?? [];
}

/**
 * Pick the localized string from an i18n JSONB blob with smart fallback.
 * Order: requested → en → ko → ja → zh → first available.
 */
export function localized(text: Record<string, string>, locale: string): string {
  return (
    text[locale] ??
    text.en ??
    text.ko ??
    text.ja ??
    text.zh ??
    Object.values(text)[0] ??
    ''
  );
}

export const apiBaseUrl = BASE_URL;
