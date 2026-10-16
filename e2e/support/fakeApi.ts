import type { Page, Route } from "@playwright/test";

type Reply = { status?: number; body?: unknown; delayMs?: number };

/** Fakes the Harvest Map JSON API with Playwright route interception. */
export class FakeApi {
  readonly requests: { method: string; path: string; body: unknown; query: URLSearchParams }[] = [];

  constructor(private readonly page: Page) {}

  async on(method: string, path: string, reply: Reply | ((body: unknown, url: URL) => Reply)) {
    await this.page.route(
      (url) => url.pathname === path,
      async (route: Route) => {
        const request = route.request();
        if (request.method() !== method) return route.fallback();
        const body = request.postData() ? request.postDataJSON() : null;
        const url = new URL(request.url());
        this.requests.push({ method, path, body, query: url.searchParams });
        const r = typeof reply === "function" ? reply(body, url) : reply;
        if (r.delayMs) await new Promise((resolve) => setTimeout(resolve, r.delayMs));
        await route.fulfill({
          status: r.status ?? 200,
          contentType: "application/json",
          body: JSON.stringify(r.body ?? {}),
        });
      },
    );
  }

  /** Never answers, so the page stays in its loading state. */
  async hang(method: string, path: string) {
    await this.page.route(
      (url) => url.pathname === path,
      (route) => (route.request().method() === method ? undefined : route.fallback()),
    );
  }

  sent(method: string, path: string) {
    return this.requests.filter((r) => r.method === method && r.path === path);
  }
}
