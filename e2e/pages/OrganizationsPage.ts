import type { Locator, Page } from "@playwright/test";

type Chip = "AI" | "Youth" | "Moonshot" | "Verified";

export class OrganizationsPage {
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly search: Locator;
  readonly sort: Locator;
  readonly newButton: Locator;
  readonly importButton: Locator;
  readonly skeleton: Locator;
  readonly loadError: Locator;
  readonly retry: Locator;
  readonly emptyTitle: Locator;
  readonly noResults: Locator;
  readonly clearFilters: Locator;
  readonly selectionBar: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole("heading", { level: 1, name: "Organizations" });
    this.subtitle = page.locator(".page-header .subtitle");
    this.search = page.getByRole("searchbox", { name: "Search organisations" });
    this.sort = page.getByLabel("Sort organisations");
    this.newButton = page.getByRole("link", { name: "New", exact: true });
    this.importButton = page.getByRole("button", { name: "Import", exact: true });
    this.skeleton = page.getByLabel("Loading organizations");
    this.loadError = page.getByRole("heading", { name: "Couldn't load organizations" });
    this.retry = page.getByRole("button", { name: "Retry" });
    this.emptyTitle = page.getByRole("heading", { name: "No organisations yet" });
    this.noResults = page.getByRole("heading", { name: "Nothing matches" });
    this.clearFilters = page.getByRole("button", { name: "Clear filters" });
    this.selectionBar = page.getByRole("region", { name: /organisations selected/ });
  }

  async open(query = "") {
    await this.page.goto(`/organizations${query}`);
  }

  cards() {
    return this.page.getByTestId("org-card");
  }

  card(name: string) {
    return this.cards().filter({ has: this.page.getByRole("link", { name, exact: true }) });
  }

  cardLink(name: string) {
    return this.card(name).getByRole("link", { name, exact: true });
  }

  cardMeta(name: string) {
    return this.card(name).locator(".org-card__meta");
  }

  cardTags(name: string) {
    return this.card(name).locator(".tag");
  }

  cardStatus(name: string) {
    return this.card(name).locator(".verify");
  }

  cardMark(name: string) {
    return this.card(name).locator(".mark");
  }

  chip(name: Chip) {
    return this.page.getByRole("button", { name, exact: true });
  }

  async toggleChip(name: Chip) {
    await this.chip(name).click();
  }

  async sortBy(option: "Impact" | "Name" | "Updated") {
    await this.sort.selectOption({ label: option });
  }

  async searchFor(text: string) {
    await this.search.fill(text);
  }

  checkbox(name: string) {
    return this.page.getByRole("checkbox", { name: `Select ${name}` });
  }

  async select(name: string) {
    await this.checkbox(name).check();
  }

  selectionButton(name: string | RegExp) {
    return this.selectionBar.getByRole("button", { name });
  }

  tagDialog() {
    return new BulkTagDialog(this.page);
  }
}

export class BulkTagDialog {
  readonly root: Locator;
  readonly tag: Locator;
  readonly apply: Locator;

  constructor(private readonly page: Page) {
    this.root = page.getByRole("dialog", { name: /^Tag \d+ organi[sz]ations?$/ });
    this.tag = this.root.getByLabel("Tag", { exact: true });
    this.apply = this.root.getByRole("button", { name: "Apply" });
  }

  mode(label: "Add tag" | "Remove tag") {
    return this.root.getByRole("radio", { name: label });
  }
}
