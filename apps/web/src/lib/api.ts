export interface Goal {
  id: string;
  number: number;
  name: Record<string, string>;
  color: string;
  icon: string | null;
}

export interface ListResponse<T> {
  data: T[];
  meta: { count: number };
}

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:4000';

export async function fetchGoals(locale: string = 'ko'): Promise<Goal[]> {
  try {
    const res = await fetch(`${BASE_URL}/v1/catalog/goals`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const json = (await res.json()) as ListResponse<Goal>;
    return json.data;
  } catch {
    // Tolerate API not running (e.g. when only the web app is up locally)
    return [];
  }
}

export function localized(text: Record<string, string>, locale: string): string {
  return text[locale] ?? text.en ?? text.ko ?? Object.values(text)[0] ?? '';
}
