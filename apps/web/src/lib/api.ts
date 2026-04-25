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

export interface AuthSession {
  user: {
    id: string;
    tenantId: string;
    email: string;
    displayName?: string;
    status: string;
    mfaEnabled: boolean;
  };
  expiresAt: string;
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

export async function fetchGoals(): Promise<Goal[]> {
  const json = await safeJson<ListResponse<Goal>>(
    fetch(`${BASE_URL}/v1/catalog/goals`, { next: { revalidate: 60 } }),
  );
  return json?.data ?? [];
}

export async function fetchGoal(id: string): Promise<Goal | null> {
  const json = await safeJson<ItemResponse<Goal>>(
    fetch(`${BASE_URL}/v1/catalog/goals/${encodeURIComponent(id)}`, {
      next: { revalidate: 60 },
    }),
  );
  return json?.data ?? null;
}

export async function fetchTargets(goalId?: string): Promise<Target[]> {
  const url = new URL(`${BASE_URL}/v1/catalog/targets`);
  if (goalId) url.searchParams.set('goal', goalId);
  const json = await safeJson<ListResponse<Target>>(
    fetch(url.toString(), { next: { revalidate: 60 } }),
  );
  return json?.data ?? [];
}

export async function fetchIndicators(targetId?: string): Promise<Indicator[]> {
  const url = new URL(`${BASE_URL}/v1/catalog/indicators`);
  if (targetId) url.searchParams.set('target', targetId);
  const json = await safeJson<ListResponse<Indicator>>(
    fetch(url.toString(), { next: { revalidate: 60 } }),
  );
  return json?.data ?? [];
}

export function localized(text: Record<string, string>, locale: string): string {
  return text[locale] ?? text.en ?? text.ko ?? Object.values(text)[0] ?? '';
}

export const apiBaseUrl = BASE_URL;
