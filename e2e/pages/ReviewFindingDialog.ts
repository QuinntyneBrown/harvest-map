import type { Locator, Page } from "@playwright/test";

export class ReviewFindingDialog {
  readonly root: Locator;
  readonly description: Locator;
  readonly statement: Locator;
  readonly meta: Locator;
  readonly role: Locator;
  readonly since: Locator;
  readonly organisation: Locator;
  readonly roleError: Locator;
  readonly sources: Locator;
  readonly errorSummary: Locator;
  readonly failedAlert: Locator;
  readonly accept: Locator;
  readonly reject: Locator;
  readonly cancel: Locator;
  private readonly body: Locator;

  constructor(private readonly page: Page) {
    this.root = page.getByRole("dialog", { name: "Review finding" });
    this.description = this.root.locator("#dlg-desc");
    this.statement = this.root.locator("blockquote");
    this.meta = this.root.locator(".finding__meta");
    this.role = this.root.getByLabel("Role");
    this.since = this.root.getByLabel("Since");
    this.organisation = this.root.getByLabel("Organisation");
    this.roleError = this.root.locator("#rf-role-error");
    this.sources = this.root.getByRole("region", { name: "Sources" }).getByRole("link");
    this.errorSummary = this.root.locator(".form-summary");
    this.failedAlert = this.root.locator(".alert--danger:not(.form-summary)");
    this.accept = this.root.getByRole("button", { name: "Accept", exact: true });
    this.reject = this.root.getByRole("button", { name: "Reject", exact: true });
    this.cancel = this.root.getByRole("button", { name: "Cancel" });
    this.body = this.root.locator(".dialog__body");
  }

  footerButtonNames() {
    return this.root.locator(".dialog__footer button");
  }

  async setRole(value: string) {
    await this.role.fill(value);
  }

  async submit() {
    await this.accept.click();
  }

  async close() {
    await this.cancel.click();
  }

  /** True when the body scrolls inside the dialog while the footer stays in view. */
  async scrollsInside() {
    return this.body.evaluate((el) => el.scrollHeight > el.clientHeight && getComputedStyle(el).overflowY === "auto");
  }
}
