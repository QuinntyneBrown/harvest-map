import type { Locator, Page } from "@playwright/test";

export class UnsavedChangesDialog {
  readonly root: Locator;
  readonly description: Locator;
  readonly discard: Locator;
  readonly keepEditing: Locator;

  constructor(page: Page, name: string) {
    this.root = page.getByRole("dialog", { name: `Discard changes to ${name}?` });
    this.description = this.root.locator("#dlg-desc");
    this.discard = this.root.getByRole("button", { name: "Discard" });
    this.keepEditing = this.root.getByRole("button", { name: "Keep editing" });
  }
}
