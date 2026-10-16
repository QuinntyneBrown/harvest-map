import type { Locator, Page } from "@playwright/test";

export class ToastRegion {
  constructor(private readonly page: Page) {}

  toasts(): Locator {
    return this.page.getByTestId("toast");
  }

  toast(title: string): Locator {
    return this.toasts().filter({ hasText: title });
  }

  action(title: string, label: string): Locator {
    return this.toast(title).getByRole("button", { name: label, exact: true });
  }

  timer(title: string): Locator {
    return this.toast(title).locator(".toast__progress");
  }

  dismiss(title: string): Locator {
    return this.toast(title).getByRole("button", { name: "Dismiss" });
  }
}
