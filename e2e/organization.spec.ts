import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { OrganizationPage } from "./pages/OrganizationPage";
import { RunResearchDialog } from "./pages/RunResearchDialog";
import { faithtechDetail } from "./fixtures/organizations";

async function open(page: Page, detail: object = faithtechDetail) {
  const api = new FakeApi(page);
  await api.on("GET", "/api/organizations/o1", { body: detail });
  await api.on("GET", "/api/settings", { body: { defaultDepth: "standard" } });
  const org = new OrganizationPage(page);
  await org.open();
  return { api, org };
}

test.describe("L2-007 Organization detail", () => {
  test("AC1: name, status, summary, tags, actions, sections and details", async ({ page }) => {
    // Given an organization
    // When the page loads
    const { org } = await open(page);
    // Then the header, actions and sections show
    await expect(org.heading).toHaveText("FaithTech");
    await expect(org.status).toHaveText("Verified");
    await expect(org.subtitle).toHaveText("Global community of Christian technologists in 50+ cities and 20+ countries.");
    await expect(org.tags).toHaveText(["AI", "Community", "Youth"]);
    await expect(org.edit).toHaveAttribute("href", "/organizations/o1/edit");
    await expect(org.del).toBeVisible();
    await expect(org.research).toBeVisible();
    await expect(org.initiatives()).toHaveText(faithtechDetail.initiatives);
    await expect(org.sectionAction("People", "Add")).toBeVisible();
    await expect(org.sectionAction("Problems", "Link")).toBeVisible();
    await expect(org.sourceLinks()).toHaveText(["Canada's FaithTech aims to redeem technology", "What is redemptive technology?"]);
    await expect(org.sourceNotes().first()).toHaveText("ministrywatch.com · Verified Tue 14 Oct");
    await expect(org.sourceNotes().last()).toHaveText("letu.edu · Added Mon 13 Oct");
    await expect(org.fact("Type")).toHaveText("Community");
    await expect(org.fact("Founded")).toHaveText("2016");
    await expect(org.fact("Base")).toHaveText("Waterloo, Canada");
    await expect(org.fact("Reach")).toHaveText("50+ cities");
    await expect(org.fact("Website")).toContainText("faithtech.com");
    await expect(org.fact("Status")).toHaveText("Verified");
    await expect(org.activity()).toHaveText(["Today 12:04Run #48 looking for LinkedIn profiles"]);
  });

  test("AC2: people and problems open their pages", async ({ page }) => {
    const { org } = await open(page);
    await expect(org.personLinks().first()).toHaveAttribute("href", "/people/p1");
    await expect(org.problemLinks().first()).toHaveText("AI that serves human flourishing");
    await expect(org.section("Problems").getByRole("link", { name: "AI that serves human flourishing" })).toHaveAttribute("href", "/problems/pr4");
  });

  test("AC4: skeleton while loading", async ({ page }) => {
    const api = new FakeApi(page);
    await api.hang("GET", "/api/organizations/o1");
    const org = new OrganizationPage(page);
    await org.open();
    await expect(org.skeleton).toBeVisible();
  });

  test("AC4: an unknown id shows the not-found state", async ({ page }) => {
    const api = new FakeApi(page);
    await api.on("GET", "/api/organizations/o1", { status: 404, body: { message: "Not found" } });
    const org = new OrganizationPage(page);
    await org.open();
    await expect(org.notFound).toBeVisible();
  });

  test("AC4: a load failure shows an error with Retry", async ({ page }) => {
    const api = new FakeApi(page);
    let recovered = false;
    await api.on("GET", "/api/organizations/o1", () => (recovered ? { body: faithtechDetail } : { status: 500 }));
    const org = new OrganizationPage(page);
    await org.open();
    await expect(org.loadError).toBeVisible();
    recovered = true;
    await org.retry.click();
    await expect(org.heading).toHaveText("FaithTech");
  });

  test("AC5: empty sections prompt to add or research", async ({ page }) => {
    // Given an organization with nothing attached
    const { org } = await open(page, { ...faithtechDetail, initiatives: [], people: [], problems: [], sources: [], activity: [] });
    // Then each section shows a prompt
    await expect(org.section("What they're doing")).toContainText("Nothing recorded yet. Run research to find out.");
    await expect(org.section("People")).toContainText("No people yet. Add one, or run research.");
    await expect(org.section("Problems")).toContainText("No problems linked yet.");
    await expect(org.section("Sources")).toContainText("No sources yet. Run research to find some.");
  });

  test("AC6: an archived organization is read-only with only Restore", async ({ page }) => {
    const { org } = await open(page, { ...faithtechDetail, archived: { by: "Hannah Okafor", at: "Mon 13 Oct" } });
    await expect(org.archivedBanner).toContainText("Archived by Hannah Okafor · Mon 13 Oct");
    await expect(org.restore).toBeVisible();
    await expect(org.edit).toHaveCount(0);
    await expect(org.del).toHaveCount(0);
    await expect(org.research).toHaveCount(0);
    await expect(org.sectionAction("People", "Add")).toHaveCount(0);
    await expect(org.sectionAction("Problems", "Link")).toHaveCount(0);
  });

  test("AC7: Restore makes the organization editable again", async ({ page }) => {
    // Given an archived organization
    const { api, org } = await open(page, { ...faithtechDetail, archived: { by: "Hannah Okafor", at: "Mon 13 Oct" } });
    await api.on("POST", "/api/organizations/o1/restore", { body: { ok: true, organization: faithtechDetail } });
    // When the user selects Restore
    await org.restore.click();
    // Then the banner goes and the actions return
    await expect(org.archivedBanner).toHaveCount(0);
    await expect(org.edit).toBeVisible();
    await expect(org.restore).toHaveCount(0);
    expect(api.sent("POST", "/api/organizations/o1/restore")).toHaveLength(1);
  });

  test("AC8: Research opens Run research aimed at this organization", async ({ page }) => {
    const { org } = await open(page);
    await org.research.click();
    const dialog = new RunResearchDialog(page);
    await expect(dialog.root).toBeVisible();
    await expect(dialog.questionOption("Something else")).toBeChecked();
    await expect(dialog.customQuestion).toHaveValue("What is FaithTech doing?");
  });
});
