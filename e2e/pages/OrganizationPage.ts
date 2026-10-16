import type { Locator, Page } from "@playwright/test";

export class OrganizationPage {
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly status: Locator;
  readonly tags: Locator;
  readonly edit: Locator;
  readonly del: Locator;
  readonly research: Locator;
  readonly restore: Locator;
  readonly archivedBanner: Locator;
  readonly skeleton: Locator;
  readonly notFound: Locator;
  readonly loadError: Locator;
  readonly retry: Locator;
  readonly facts: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole("heading", { level: 1 });
    this.subtitle = page.locator(".page-header .subtitle");
    this.status = page.locator(".page-header .verify");
    this.tags = page.locator(".page-header .tag");
    this.edit = page.getByRole("link", { name: "Edit", exact: true });
    this.del = page.getByRole("button", { name: "Delete", exact: true });
    this.research = page.getByRole("button", { name: "Research", exact: true });
    this.restore = page.getByRole("button", { name: "Restore", exact: true });
    this.archivedBanner = page.getByRole("status").filter({ hasText: "Read-only until restored." });
    this.skeleton = page.getByLabel("Loading organization");
    this.notFound = page.getByRole("heading", { name: "Nothing grows here" });
    this.loadError = page.getByRole("heading", { name: "Couldn't load this organization" });
    this.retry = page.getByRole("button", { name: "Retry" });
    this.facts = page.locator(".facts .fact");
  }

  async open(id = "o1") {
    await this.page.goto(`/organizations/${id}`);
  }

  section(title: string) {
    return this.page.locator("section").filter({ has: this.page.getByRole("heading", { name: title, exact: true }) });
  }

  sectionAction(title: string, name: string) {
    return this.section(title).getByRole("button", { name, exact: true });
  }

  initiatives() {
    return this.section("What they're doing").locator("li");
  }

  personLinks() {
    return this.section("People").getByRole("link").filter({ hasNotText: "LinkedIn" });
  }

  problemLinks() {
    return this.section("Problems").locator(".org-card__name");
  }

  sourceLinks() {
    return this.section("Sources").locator(".source a");
  }

  sourceNotes() {
    return this.section("Sources").locator(".source__host");
  }

  fact(label: string) {
    return this.facts.filter({ has: this.page.locator("dt", { hasText: label }) }).locator("dd");
  }

  activity() {
    return this.section("Activity").locator("li");
  }

  prompt(title: string) {
    return this.section(title).locator(".empty__text, .text-muted").first();
  }
}
