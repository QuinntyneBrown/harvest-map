import type { Locator, Page } from "@playwright/test";

export class RunResearchDialog {
  readonly root: Locator;
  readonly questionGroup: Locator;
  readonly lookForGroup: Locator;
  readonly depthGroup: Locator;
  readonly note: Locator;
  readonly customQuestion: Locator;
  readonly customQuestionError: Locator;
  readonly errorSummary: Locator;
  readonly failedAlert: Locator;
  readonly run: Locator;
  readonly cancel: Locator;

  constructor(private readonly page: Page) {
    this.root = page.getByRole("dialog", { name: "Ask the web" });
    this.questionGroup = this.root.getByRole("group", { name: "Question" });
    this.lookForGroup = this.root.getByRole("group", { name: "Look for" });
    this.depthGroup = this.root.getByRole("group", { name: "Depth" });
    this.note = this.root.locator(".text-caption", { hasText: "Findings need" });
    this.customQuestion = this.root.getByLabel("Your question");
    this.customQuestionError = this.root.locator("#rr-custom-error");
    this.errorSummary = this.root.locator(".form-summary");
    this.failedAlert = this.root.locator(".alert--danger:not(.form-summary)");
    this.run = this.root.getByRole("button", { name: "Run", exact: true });
    this.cancel = this.root.getByRole("button", { name: "Cancel" });
  }

  questionOptions() {
    return this.questionGroup.getByRole("radio");
  }

  questionOption(label: string) {
    return this.questionGroup.getByRole("radio", { name: label });
  }

  lookForOptions() {
    return this.lookForGroup.getByRole("checkbox");
  }

  lookFor(label: string) {
    return this.lookForGroup.getByRole("checkbox", { name: label });
  }

  depth(label: string) {
    return this.depthGroup.getByRole("radio", { name: new RegExp(`^${label}`) });
  }

  depthOptions() {
    return this.depthGroup.getByRole("radio");
  }

  async chooseQuestion(label: string) {
    await this.questionOption(label).check();
  }

  async chooseSomethingElse(text = "") {
    await this.questionOption("Something else").check();
    if (text) await this.customQuestion.fill(text);
  }

  async chooseDepth(label: string) {
    await this.depth(label).check();
  }

  async toggleLookFor(label: string) {
    await this.lookFor(label).click();
  }

  async submit() {
    await this.run.click();
  }

  async close() {
    await this.cancel.click();
  }

  async pressEscape() {
    await this.page.keyboard.press("Escape");
  }
}
