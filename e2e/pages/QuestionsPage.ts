import type { Locator, Page } from "@playwright/test";

export class QuestionsPage {
  readonly heading: Locator;
  readonly subtitle: Locator;
  readonly askTheWeb: Locator;
  readonly skeleton: Locator;
  readonly pageError: Locator;
  readonly pageErrorText: Locator;
  readonly tryAgain: Locator;

  constructor(private readonly page: Page) {
    this.heading = page.getByRole("heading", { level: 1, name: "Questions" });
    this.subtitle = page.locator(".page-header .subtitle");
    this.askTheWeb = page.getByRole("button", { name: "Ask the web" });
    this.skeleton = page.getByLabel("Loading questions");
    this.pageError = page.getByRole("heading", { name: "Couldn't load the answers" });
    this.pageErrorText = page.locator(".empty--error .empty__text");
    this.tryAgain = page.getByRole("button", { name: "Try again" });
  }

  async open() {
    await this.page.goto("/questions");
  }

  question(number: number) {
    return this.page.locator(`#q${number}`);
  }

  questionTitles() {
    return this.page.locator(".answer__q");
  }

  questionMeta(number: number) {
    return this.question(number).locator(".q-card__n");
  }

  reRunButton(number: number) {
    return this.question(number).getByRole("button", { name: "Re-run" });
  }

  answerLinks(number: number) {
    return this.question(number).locator(".answer__list").getByRole("link");
  }

  answerDetails(number: number) {
    return this.question(number).locator(".answer__list .text-caption");
  }

  answerError(number: number) {
    return this.question(number).getByRole("alert");
  }

  async retryAnswer(number: number) {
    await this.question(number).getByRole("button", { name: "Retry" }).click();
  }

  async reRun(number: number) {
    await this.reRunButton(number).click();
  }

  async openAskTheWeb() {
    await this.askTheWeb.click();
  }

  async retryPage() {
    await this.tryAgain.click();
  }

  async pressShortcut(key: string) {
    await this.page.keyboard.press(key);
  }
}
