import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { OrganizationsPage } from "./pages/OrganizationsPage";
import { faithtech, gloo, orgList, type OrgItem } from "./fixtures/organizations";

async function open(page: Page, items?: OrgItem[], over = {}) {
  const api = new FakeApi(page);
  await api.on("GET", "/api/organizations", { body: orgList(items, over) });
  const orgs = new OrganizationsPage(page);
  await orgs.open();
  return { api, orgs };
}

test.describe("L2-006 Organizations list", () => {
  test("AC1: header counts and cards with mark, name, meta, tags and status", async ({ page }) => {
    // Given organizations exist
    // When the page loads
    const { orgs } = await open(page);
    // Then the header counts and each card show their details
    await expect(orgs.heading).toBeVisible();
    await expect(orgs.subtitle).toHaveText("19 tracked · 12 verified · 7 unverified");
    await expect(orgs.cards()).toHaveCount(3);
    await expect(orgs.cardMark("FaithTech")).toHaveText("FT");
    await expect(orgs.cardMeta("FaithTech")).toHaveText("Community · Waterloo · 50+ cities");
    await expect(orgs.cardTags("FaithTech")).toHaveText(["AI", "Community", "Youth"]);
    await expect(orgs.cardStatus("FaithTech")).toHaveText("Verified");
    await expect(orgs.cardStatus("Kingdom Code")).toHaveText("Unverified");
    await expect(orgs.cardMeta("Kingdom Code")).toHaveText("Startup · London");
    await expect(orgs.cardLink("FaithTech")).toHaveAttribute("href", "/organizations/o1");
  });

  test("AC2: chips combine and show as pressed", async ({ page }) => {
    // Given the list
    const { api, orgs } = await open(page);
    // When the user toggles AI and Verified
    await orgs.toggleChip("AI");
    await orgs.toggleChip("Verified");
    // Then both are pressed and the list is requested with both filters
    await expect(orgs.chip("AI")).toHaveAttribute("aria-pressed", "true");
    await expect(orgs.chip("Verified")).toHaveAttribute("aria-pressed", "true");
    await expect(orgs.chip("Youth")).toHaveAttribute("aria-pressed", "false");
    await expect.poll(() => api.requests.at(-1)?.query.get("chips")).toBe("ai,verified");
  });

  test("AC3: sorting defaults to Impact and reorders on change", async ({ page }) => {
    // Given the list sorted by Impact
    const { api, orgs } = await open(page);
    await expect(orgs.cards()).toHaveCount(3);
    await expect(orgs.sort).toHaveValue("impact");
    expect(api.requests[0].query.get("sort")).toBe("impact");
    // When the user picks Name
    await orgs.sortBy("Name");
    // Then the list is requested by name
    await expect.poll(() => api.requests.at(-1)?.query.get("sort")).toBe("name");
  });

  test("AC4: search filters after 150 ms of idle typing", async ({ page }) => {
    // Given the list
    const { api, orgs } = await open(page);
    await expect(orgs.cards()).toHaveCount(3);
    const before = api.requests.length;
    // When the user types
    await orgs.searchFor("faith");
    // Then one request follows the pause, carrying the text
    await expect.poll(() => api.requests.at(-1)?.query.get("q")).toBe("faith");
    expect(api.requests.length).toBe(before + 1);
  });

  test("AC5: nothing matching shows the no-results state and Clear filters resets", async ({ page }) => {
    // Given a search that matches nothing
    const api = new FakeApi(page);
    await api.on("GET", "/api/organizations", (_b, url) => (url.searchParams.get("q") ? { body: orgList([]) } : { body: orgList() }));
    const orgs = new OrganizationsPage(page);
    await orgs.open();
    // When the user searches
    await orgs.searchFor("youth hackathon");
    // Then the no-results state offers Clear filters
    await expect(orgs.noResults).toBeVisible();
    await expect(page.getByText("No organisation matches “youth hackathon” with these filters.")).toBeVisible();
    await orgs.clearFilters.click();
    await expect(orgs.search).toHaveValue("");
    await expect(orgs.cards()).toHaveCount(3);
  });

  test("AC6: no organizations shows the empty state with New and Import", async ({ page }) => {
    const { orgs } = await open(page, [], { total: 0, verified: 0, unverified: 0 });
    await expect(orgs.subtitle).toHaveText("Nothing tracked yet");
    await expect(orgs.emptyTitle).toBeVisible();
    await expect(orgs.newButton.first()).toBeVisible();
    await expect(orgs.importButton).toBeVisible();
  });

  test("AC7: skeleton while loading", async ({ page }) => {
    const api = new FakeApi(page);
    await api.hang("GET", "/api/organizations");
    const orgs = new OrganizationsPage(page);
    await orgs.open();
    await expect(orgs.skeleton).toBeVisible();
  });

  test("AC7: load failure shows an error with Retry", async ({ page }) => {
    // Given the load fails once
    const api = new FakeApi(page);
    let recovered = false;
    await api.on("GET", "/api/organizations", () => (recovered ? { body: orgList() } : { status: 500 }));
    const orgs = new OrganizationsPage(page);
    await orgs.open();
    await expect(orgs.loadError).toBeVisible();
    // When the user selects Retry
    recovered = true;
    await orgs.retry.click();
    // Then the list loads
    await expect(orgs.cards()).toHaveCount(3);
  });

  test("AC8: long, right-to-left and non-Latin names wrap, a missing mark is an empty tile, Conflict shows", async ({ page }) => {
    // Given unusual records
    const long: OrgItem = {
      ...faithtech,
      id: "o4",
      name: "The International Association of Christian Technologists, Missionaries and Youth Workers of the Greater Waterloo Region",
      mark: null,
      status: "Conflict",
    };
    const arabic: OrgItem = { ...gloo, id: "o5", name: "منظمة الشباب المسيحي", mark: "م" };
    const { orgs } = await open(page, [long, arabic]);
    // Then the long name is fully visible and wraps, the mark tile is empty and Conflict shows
    await expect(orgs.card(long.name)).toBeVisible();
    await expect(orgs.cardMark(long.name)).toHaveText("");
    await expect(orgs.cardStatus(long.name)).toHaveText("Conflict");
    // And right-to-left text keeps its direction
    await expect(orgs.cardLink(arabic.name)).toHaveAttribute("dir", "auto");
    const box = await orgs.card(long.name).boundingBox();
    expect(box!.width).toBeLessThanOrEqual(page.viewportSize()!.width);
  });

  test("AC9: checking cards shows a selection bar with Tag, Export and Archive", async ({ page }) => {
    // Given the list
    const { orgs } = await open(page);
    await expect(orgs.selectionBar).toHaveCount(0);
    // When the user checks two cards
    await orgs.select("FaithTech");
    await orgs.select("Gloo");
    // Then the bar shows the count and actions
    await expect(orgs.selectionBar).toContainText("2 selected");
    await expect(orgs.selectionButton("Tag")).toBeVisible();
    await expect(orgs.selectionButton("Export 2")).toBeVisible();
    await expect(orgs.selectionButton("Archive")).toBeVisible();
  });
});
