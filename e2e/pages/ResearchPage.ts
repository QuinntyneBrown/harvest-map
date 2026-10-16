import type { Locator, Page } from "@playwright/test";

export class ResearchPage {
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly runResearch: Locator;
  readonly runTheFirstResearch: Locator;
  readonly emptyTitle: Locator;
  readonly skeleton: Locator;
  readonly loadError: Locator;
  readonly tryAgain: Locator;
  readonly runList: Locator;
  readonly findingsSection: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole("heading", { level: 1, name: "Research" });
    this.subtitle = page.locator(".page-header .subtitle");
    this.runResearch = page.getByRole("button", { name: "Run research", exact: true });
    this.runTheFirstResearch = page.getByRole("button", { name: "Run the first research" });
    this.emptyTitle = page.locator(".empty__title");
    this.skeleton = page.getByLabel("Loading runs");
    this.loadError = page.getByRole("heading", { name: "Couldn't load research runs" });
    this.tryAgain = page.getByRole("button", { name: "Try again" });
    this.runList = page.getByRole("region", { name: "Earlier runs" });
    this.findingsSection = page.getByRole("region", { name: "Findings to review" });
  }

  async open() {
    await this.page.goto("/research");
  }

  runRows() {
    return this.runList.getByTestId("run-row");
  }

  run(id: number) {
    return this.runRows().filter({ hasText: `#${id} · ` });
  }

  runTitle(id: number) {
    return this.run(id).locator(".run-row__title");
  }

  runMeta(id: number) {
    return this.run(id).locator(".text-caption");
  }

  runStatus(id: number) {
    return this.run(id).locator(".run-status");
  }

  findingCards() {
    return this.findingsSection.getByTestId("finding");
  }

  finding(statementStart: string) {
    return this.findingCards().filter({ hasText: statementStart });
  }

  findingStatement(statementStart: string) {
    return this.finding(statementStart).locator(".finding__claim");
  }

  findingMeta(statementStart: string) {
    return this.finding(statementStart).locator(".finding__meta");
  }

  findingDecision(statementStart: string) {
    return this.finding(statementStart).locator(".finding__decision");
  }

  findingError(statementStart: string) {
    return this.finding(statementStart).getByRole("alert");
  }

  findingButton(statementStart: string, name: "Accept" | "Edit" | "Reject" | "Undo") {
    return this.finding(statementStart).getByRole("button", { name, exact: true });
  }

  async accept(statementStart: string) {
    await this.findingButton(statementStart, "Accept").click();
  }

  async reject(statementStart: string) {
    await this.findingButton(statementStart, "Reject").click();
  }

  async edit(statementStart: string) {
    await this.findingButton(statementStart, "Edit").click();
  }

  async undo(statementStart: string) {
    await this.findingButton(statementStart, "Undo").click();
  }

  async retry() {
    await this.tryAgain.click();
  }
}
