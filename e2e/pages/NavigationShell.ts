import type { Locator, Page } from "@playwright/test";

export class NavigationShell {
  readonly menuButton: Locator;
  readonly headerLinks: Locator;
  readonly sheet: Locator;
  readonly sheetLinks: Locator;
  readonly skipLink: Locator;

  constructor(private readonly page: Page) {
    this.menuButton = page.getByRole("button", { name: "Open navigation" });
    this.headerLinks = page.locator("header.topbar nav.topbar__nav").getByRole("link");
    this.sheet = page.getByRole("dialog", { name: "Harvest Map" });
    this.sheetLinks = this.sheet.getByRole("link");
    this.skipLink = page.getByRole("link", { name: "Skip to content" });
  }

  headerLink(name: string) {
    return this.headerLinks.filter({ hasText: new RegExp(`^${name}$`) });
  }

  sheetLink(name: string) {
    return this.sheet.getByRole("link", { name, exact: true });
  }
}
