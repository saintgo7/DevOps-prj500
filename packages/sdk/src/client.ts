export interface SdgiClientOptions {
  baseUrl: string;
  apiKey?: string;
  fetch?: typeof globalThis.fetch;
}

export interface HealthResponse {
  status: string;
  service: string;
  time: string;
}

export class SdgiClient {
  private readonly baseUrl: string;
  private readonly apiKey: string | undefined;
  private readonly fetchImpl: typeof globalThis.fetch;

  constructor(opts: SdgiClientOptions) {
    this.baseUrl = opts.baseUrl.replace(/\/$/, '');
    this.apiKey = opts.apiKey;
    this.fetchImpl = opts.fetch ?? globalThis.fetch;
  }

  async health(): Promise<HealthResponse> {
    const res = await this.fetchImpl(`${this.baseUrl}/v1/health`, {
      headers: this.headers(),
    });
    if (!res.ok) {
      throw new Error(`health failed: ${res.status}`);
    }
    return (await res.json()) as HealthResponse;
  }

  private headers(): Record<string, string> {
    const h: Record<string, string> = { 'content-type': 'application/json' };
    if (this.apiKey) h.authorization = `Bearer ${this.apiKey}`;
    return h;
  }
}
