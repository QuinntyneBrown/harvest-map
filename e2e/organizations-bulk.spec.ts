import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { OrganizationsPage } from "./pages/OrganizationsPage";
import { ToastRegion } from "./pages/ToastRegion";
import { faithtech, gloo, kingdomCode, orgList, type OrgItem } from "./fixtures/organizations";

/** Serves the list from a mutable set, so archive and restore change what the list returns. */
async function open(page: Page) {
  const api = new FakeApi(page);
  const archived = new Set<string>();
  const all: OrgItem[] = [faithtech, gloo, kingdomCode];
  await api.on("GET", "/api/organizations", () => ({ body: orgList(all.filter((o) => !archived.has(o.id))) }));
  await api.on("POST", "/api/organizations/bulk/archive", (body) => {
    (body as { ids: string[] }).ids.forEach((id) => archived.add(id));
    return { body: { ok: true } };
  });
  await api.on("POST", "/api/organizations/bulk/restore", (body) => {
    (body as { ids: string[] }).ids.forEach((id) => archived.delete(id));
    return { body: { ok: true } };
  });
  const orgs = new OrganizationsPage(page);
  await orgs.open();
  await expect(orgs.cards()).toHaveCount(3);
  return { api, orgs, toasts: new ToastRegion(page) };
}

test.describe("L2-010 Archive and bulk actions", () => {
  test("AC1: Archive hides the organization and shows a toast with Undo", async ({ page }) => {
    // Given a selected organization
    const { api, orgs, toasts } = await open(page);
    await orgs.select("Kingdom Code");
    // When the user selects Archive
    await orgs.selectionButton("Archive").click();
    // Then it leaves the list and the toast offers Undo
    await expect(orgs.cards()).toHaveCount(2);
    await expect(orgs.card("Kingdom Code")).toHaveCount(0);
    await expect(toasts.toast("Kingdom Code archived")).toContainText("Hidden from lists and the map.");
    await expect(toasts.action("Kingdom Code archived", "Undo")).toBeVisible();
    await expect(orgs.selectionBar).toHaveCount(0);
    expect(api.sent("POST", "/api/organizations/bulk/archive")[0].body).toEqual({ ids: ["o3"] });
  });

  test("AC1: archiving several organizations says how many", async ({ page }) => {
    const { orgs, toasts } = await open(page);
    await orgs.select("FaithTech");
    await orgs.select("Gloo");
    await orgs.selectionButton("Archive").click();
    await expect(toasts.toast("2 organizations archived")).toContainText("Hidden from lists and the map.");
  });

  test("AC2: the toast disappears when its timer ends, unless hovered, which pauses the timer", async ({ page }) => {
    // Given an archive toast (the tests run the 8 s timer as 5 s)
    const { orgs, toasts } = await open(page);
    await orgs.select("Kingdom Code");
    await orgs.selectionButton("Archive").click();
    const toast = toasts.toast("Kingdom Code archived");
    await expect(toast).toBeVisible();
    // When the pointer comes to rest on it (the toast appeared under the pointer, so leave and enter again)
    await page.mouse.move(5, 5);
    await toast.hover();
    // Then its timer bar pauses, and it stays well past the timer
    await expect(toasts.timer("Kingdom Code archived")).toHaveCSS("animation-play-state", "paused");
    await page.waitForTimeout(5500);
    await expect(toast).toBeVisible();
    // And once the pointer leaves, the timer runs again and the toast goes
    await page.mouse.move(5, 5);
    await expect(toasts.timer("Kingdom Code archived")).toHaveCSS("animation-play-state", "running");
    await expect(toast).toHaveCount(0, { timeout: 8000 });
  });

  test("AC3: Undo restores the organization", async ({ page }) => {
    // Given an archived organization
    const { api, orgs, toasts } = await open(page);
    await orgs.select("Kingdom Code");
    await orgs.selectionButton("Archive").click();
    await expect(orgs.cards()).toHaveCount(2);
    // When the user selects Undo
    await toasts.action("Kingdom Code archived", "Undo").click();
    // Then it is back in the list
    await expect(orgs.cards()).toHaveCount(3);
    expect(api.sent("POST", "/api/organizations/bulk/restore")[0].body).toEqual({ ids: ["o3"] });
  });

  test("AC4: Tag adds a tag to every selected organization", async ({ page }) => {
    // Given two selected organizations
    const { api, orgs, toasts } = await open(page);
    await api.on("POST", "/api/organizations/bulk/tag", { body: { ok: true } });
    await orgs.select("FaithTech");
    await orgs.select("Gloo");
    // When the user adds the Moonshot tag
    await orgs.selectionButton("Tag").click();
    const dialog = orgs.tagDialog();
    await expect(dialog.root).toBeVisible();
    await dialog.tag.selectOption("Moonshot");
    await dialog.apply.click();
    // Then the change is saved for both and confirmed
    await expect(dialog.root).toBeHidden();
    expect(api.sent("POST", "/api/organizations/bulk/tag")[0].body).toEqual({ ids: ["o1", "o2"], tag: "Moonshot", mode: "add" });
    await expect(toasts.toast("Moonshot added to 2 organizations")).toBeVisible();
  });

  test("AC4: Tag can remove a tag", async ({ page }) => {
    const { api, orgs } = await open(page);
    await api.on("POST", "/api/organizations/bulk/tag", { body: { ok: true } });
    await orgs.select("FaithTech");
    await orgs.selectionButton("Tag").click();
    const dialog = orgs.tagDialog();
    await dialog.tag.selectOption("AI");
    await dialog.mode("Remove tag").check();
    await dialog.apply.click();
    expect(api.sent("POST", "/api/organizations/bulk/tag")[0].body).toEqual({ ids: ["o1"], tag: "AI", mode: "remove" });
  });

  test("a failed archive keeps the organizations and says so", async ({ page }) => {
    const { api, orgs, toasts } = await open(page);
    await api.on("POST", "/api/organizations/bulk/archive", { status: 500 });
    await orgs.select("Kingdom Code");
    await orgs.selectionButton("Archive").click();
    await expect(toasts.toast("Couldn't archive")).toBeVisible();
    await expect(orgs.cards()).toHaveCount(3);
  });
});
