import type { Locator, Page } from "@playwright/test";

export class OrganizationFormPage {
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly name: Locator;
  readonly type: Locator;
  readonly founded: Locator;
  readonly city: Locator;
  readonly country: Locator;
  readonly website: Locator;
  readonly summary: Locator;
  readonly save: Locator;
  readonly cancel: Locator;
  readonly errorSummary: Locator;
  readonly failedAlert: Locator;
  readonly skeleton: Locator;
  readonly loadError: Locator;
  readonly tryAgain: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole("heading", { level: 1 });
    this.subtitle = page.locator(".page-header .subtitle");
    this.name = page.getByLabel("Name");
    this.type = page.getByLabel("Type");
    this.founded = page.getByLabel("Founded");
    this.city = page.getByLabel("City");
    this.country = page.getByLabel("Country");
    this.website = page.getByLabel("Website");
    this.summary = page.getByLabel("Summary");
    this.save = page.getByRole("button", { name: "Save", exact: true });
    this.cancel = page.getByRole("button", { name: "Cancel", exact: true });
    this.errorSummary = page.locator(".form-summary");
    this.failedAlert = page.locator(".alert--danger:not(.form-summary)");
    this.skeleton = page.getByLabel("Loading form");
    this.loadError = page.getByRole("heading", { name: "Couldn't load the form" });
    this.tryAgain = page.getByRole("button", { name: "Try again" });
  }

  async openEdit(id = "o1") {
    await this.page.goto(`/organizations/${id}/edit`);
  }

  async openNew() {
    await this.page.goto("/organizations/new");
  }

  tag(name: string) {
    return this.page.getByRole("group", { name: "Tags" }).getByRole("checkbox", { name });
  }

  fieldError(id: string) {
    return this.page.locator(`#${id}-error`);
  }

  summaryItem(text: string) {
    return this.errorSummary.getByRole("link", { name: text });
  }
}
