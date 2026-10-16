import { expect, test } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { orgList } from "./fixtures/organizations";
import { NavigationShell } from "./pages/NavigationShell";

async function open(page: import("@playwright/test").Page) {
  const api = new FakeApi(page);
  await api.on("GET", "/api/organizations", { body: orgList() });
  const nav = new NavigationShell(page);
  await page.goto("/organizations");
  await expect(page.getByRole("heading", { level: 1, name: "Organizations" })).toBeVisible();
  return nav;
}

test.describe("L2-030 Navigation shell", () => {
  test("AC1: at 768 px and wider the header shows the links and marks the current page", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    const nav = await open(page);
    await expect(nav.menuButton).toBeHidden();
    await expect(nav.headerLinks).toHaveText(["Field", "Orgs", "People", "Problems", "Questions", "Research", "Map"]);
    await expect(nav.headerLink("Orgs")).toHaveAttribute("aria-current", "page");
  });

  test("AC2: below 768 px the links move into a navigation sheet opened from a menu button", async ({ page }) => {
    // Given a phone-width viewport
    await page.setViewportSize({ width: 390, height: 800 });
    const nav = await open(page);
    await expect(nav.headerLinks.first()).toBeHidden();
    // When the user opens the menu
    await nav.menuButton.click();
    // Then the sheet lists the same links, an Account group and the user
    await expect(nav.sheet).toBeVisible();
    await expect(nav.sheetLinks).toHaveText(["Field", "Organizations", "People", "Problems", "Questions", "Research", "Map", "Settings", "Notifications"]);
    await expect(nav.sheetLink("Organizations")).toHaveAttribute("aria-current", "page");
    await expect(nav.sheet).toContainText("Account");
    await expect(nav.sheet).toContainText("Naomi Achterberg");
  });

  test("AC2: Escape closes the sheet and returns focus to the menu button", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 800 });
    const nav = await open(page);
    await nav.menuButton.click();
    await page.keyboard.press("Escape");
    await expect(nav.sheet).toBeHidden();
    await expect(nav.menuButton).toBeFocused();
  });

  test("AC2: choosing a link closes the sheet and opens the page", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 800 });
    const nav = await open(page);
    await nav.menuButton.click();
    await nav.sheetLink("Research").click();
    await expect(page).toHaveURL(/\/research$/);
    await expect(nav.sheet).toBeHidden();
  });

  test("AC3: Skip to content is the first focusable element and moves focus to the main content", async ({ page }) => {
    const nav = await open(page);
    await page.keyboard.press("Tab");
    await expect(nav.skipLink).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/#main$/);
  });
});
