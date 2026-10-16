import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { ResearchPage } from "./pages/ResearchPage";
import { ReviewFindingDialog } from "./pages/ReviewFindingDialog";
import { decided, findings, overview } from "./fixtures/research";

const PAT = "Pat Gelsinger moved";
const CREED = "Creed has 1 million";

async function openResearch(page: Page, list = findings) {
  const api = new FakeApi(page);
  await api.on("GET", "/api/research", { body: overview({ runs: overview().runs.slice(1), running: 0, findings: list }) });
  const research = new ResearchPage(page);
  await research.open();
  await expect(research.findingCards()).toHaveCount(list.length);
  return { api, research };
}

test.describe("L2-024 Review findings", () => {
  test("AC1: each finding shows statement, subject, source, confidence, low-confidence reason and actions", async ({ page }) => {
    // Given findings to review
    // When the section renders
    const { research } = await openResearch(page);
    // Then each shows its details and actions
    await expect(research.findingsSection).toContainText("Accept creates or updates the record · Reject keeps the source");
    await expect(research.findingStatement(PAT)).toHaveText(
      "Pat Gelsinger moved from chair to executive chair and head of technology at Gloo in April 2025.",
    );
    await expect(research.findingMeta(PAT)).toContainText("Pat Gelsinger");
    await expect(research.findingMeta(PAT)).toContainText("religionunplugged.com");
    await expect(research.findingMeta(PAT)).toContainText("Confidence 92%");
    await expect(research.findingMeta(PAT)).not.toContainText("Company claim");
    await expect(research.findingMeta(CREED)).toContainText("Confidence 41%");
    await expect(research.findingMeta(CREED)).toContainText("Company claim; no independent source.");
    for (const name of ["Accept", "Edit", "Reject"] as const) {
      await expect(research.findingButton(PAT, name)).toBeVisible();
    }
  });

  test("AC2: Accept applies at once, shows who accepted it with Undo, and updates the record", async ({ page }) => {
    // Given a pending finding and a slow server
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f1/accept", { delayMs: 1500, body: decided(findings[0], "Accepted") });
    // When the user selects Accept
    await research.accept(PAT);
    // Then the card shows the decision immediately, before the server answers
    await expect(research.findingDecision(PAT)).toHaveText("Accepted by Naomi Achterberg · Undo available for 30 s", { timeout: 1000 });
    await expect(research.findingButton(PAT, "Undo")).toBeVisible();
    await expect(research.findingButton(PAT, "Accept")).toHaveCount(0);
    // And the change is sent to create or update the record
    await expect.poll(() => api.sent("POST", "/api/findings/f1/accept").length).toBe(1);
    expect(api.sent("POST", "/api/findings/f1/accept")[0].body).toEqual({ fields: findings[0].fields });
    await expect(research.findingDecision(PAT)).toHaveText("Accepted by Naomi Achterberg · Undo available for 30 s");
  });

  test("AC2: a failed Accept puts the finding back and says so", async ({ page }) => {
    // Given the server refuses the Accept
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f1/accept", { status: 500 });
    // When the user selects Accept
    await research.accept(PAT);
    // Then the finding returns to pending with an error
    await expect(research.findingError(PAT)).toContainText("Couldn't save — Try again.");
    await expect(research.findingButton(PAT, "Accept")).toBeVisible();
  });

  test("AC3: Reject shows who rejected it with Undo", async ({ page }) => {
    // Given a pending finding
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f2/reject", { body: decided(findings[1], "Rejected") });
    // When the user selects Reject
    await research.reject(CREED);
    // Then the card shows the rejection and the source is kept
    await expect(research.findingDecision(CREED)).toHaveText("Rejected by Naomi Achterberg · Undo available for 30 s");
    await expect(research.findingButton(CREED, "Undo")).toBeVisible();
    await expect(research.findingMeta(CREED)).toContainText("creed.app");
    expect(api.sent("POST", "/api/findings/f2/reject")).toHaveLength(1);
  });

  test("AC4: Undo within 30 s returns the finding to pending", async ({ page }) => {
    // Given an accepted finding
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f1/accept", { body: decided(findings[0], "Accepted") });
    await api.on("POST", "/api/findings/f1/undo", { body: decided(findings[0], "Pending") });
    await research.accept(PAT);
    await expect(research.findingButton(PAT, "Undo")).toBeVisible();
    // When the user selects Undo
    await research.undo(PAT);
    // Then the effect is reversed and the finding is pending again
    await expect(research.findingButton(PAT, "Accept")).toBeVisible();
    await expect(research.findingDecision(PAT)).toHaveCount(0);
    expect(api.sent("POST", "/api/findings/f1/undo")).toHaveLength(1);
  });

  test("AC4: after 30 s Undo is no longer offered", async ({ page }) => {
    // Given an accepted finding
    await page.clock.install();
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f1/accept", { body: decided(findings[0], "Accepted") });
    await research.accept(PAT);
    await expect(research.findingButton(PAT, "Undo")).toBeVisible();
    // When 30 s pass
    await page.clock.fastForward(31_000);
    // Then Undo is gone
    await expect(research.findingButton(PAT, "Undo")).toHaveCount(0);
    await expect(research.findingDecision(PAT)).toHaveText("Accepted by Naomi Achterberg");
  });

  test("AC5: Edit opens the dialog with the record, statement, confidence, sources, status, fields and actions", async ({ page }) => {
    // Given a pending person finding
    const { research } = await openResearch(page);
    const dialog = new ReviewFindingDialog(page);
    // When the user selects Edit
    await research.edit(PAT);
    // Then the dialog shows what it updates and the editable change
    await expect(dialog.description).toHaveText("Updates Pat Gelsinger · Gloo");
    await expect(dialog.statement).toHaveText(findings[0].statement);
    await expect(dialog.meta).toHaveText(/Confidence 92%.*2 sources.*Verified/);
    await expect(dialog.role).toHaveValue("Executive Chair & Head of Technology");
    await expect(dialog.role).toBeFocused();
    await expect(dialog.since).toHaveValue("2025");
    await expect(dialog.organisation).toHaveValue("Gloo");
    await expect(dialog.sources).toHaveText(["Pat Gelsinger takes on bigger role at Gloo", "Gloo leadership"]);
    await expect(dialog.footerButtonNames()).toHaveText(["Reject", "Cancel", "Accept"]);
  });

  test("AC5: Accept from the dialog sends the edited values and decides the card", async ({ page }) => {
    // Given the dialog is open
    const { api, research } = await openResearch(page);
    await api.on("POST", "/api/findings/f1/accept", { delayMs: 500, body: decided(findings[0], "Accepted") });
    const dialog = new ReviewFindingDialog(page);
    await research.edit(PAT);
    await dialog.setRole("Executive Chair");
    // When the user selects Accept
    await dialog.submit();
    // Then the dialog is busy, then closes, and the card shows the decision
    await expect(dialog.accept).toHaveAttribute("aria-busy", "true");
    await expect(dialog.cancel).toBeDisabled();
    await expect(dialog.root).toBeHidden();
    await expect(research.findingDecision(PAT)).toHaveText("Accepted by Naomi Achterberg · Undo available for 30 s");
    expect(api.sent("POST", "/api/findings/f1/accept")[0].body).toEqual({
      fields: { role: "Executive Chair", since: "2025", organization: "Gloo" },
    });
  });

  test("AC6: an empty required field stops Accept at the error summary", async ({ page }) => {
    // Given the Role is empty
    const { api, research } = await openResearch(page);
    const dialog = new ReviewFindingDialog(page);
    await research.edit(PAT);
    await dialog.setRole("");
    // When Accept is attempted
    await dialog.submit();
    // Then the summary lists the problem
    await expect(dialog.errorSummary).toContainText("Fix 1 thing to save");
    await expect(dialog.errorSummary).toContainText("Enter a role");
    await expect(dialog.role).toHaveAttribute("aria-invalid", "true");
    await expect(dialog.roleError).toHaveText("Enter a role");
    expect(api.sent("POST", "/api/findings/f1/accept")).toHaveLength(0);
  });

  test("AC7: a failed request shows the failed state with retry and keeps the edits", async ({ page }) => {
    // Given the request fails once
    const { api, research } = await openResearch(page);
    let recovered = false;
    await api.on("POST", "/api/findings/f1/accept", () => (recovered ? { body: decided(findings[0], "Accepted") } : { status: 500 }));
    const dialog = new ReviewFindingDialog(page);
    await research.edit(PAT);
    await dialog.setRole("Executive Chair");
    // When it returns
    await dialog.submit();
    // Then the failed state shows and the edits are kept
    await expect(dialog.failedAlert).toContainText("Couldn't save");
    await expect(dialog.failedAlert).toContainText("Your edits are kept. Try again.");
    await expect(dialog.role).toHaveValue("Executive Chair");
    // And Accept retries
    recovered = true;
    await dialog.submit();
    await expect(dialog.root).toBeHidden();
  });

  test("AC7: the dialog scrolls inside when its content is taller than the viewport", async ({ page }) => {
    // Given a finding with many sources on a short screen
    await page.setViewportSize({ width: 900, height: 560 });
    const many = { ...findings[0], sources: Array.from({ length: 6 }, (_, i) => ({ ...findings[0].sources[0], title: `Source ${i + 1}` })) };
    const { research } = await openResearch(page, [many]);
    const dialog = new ReviewFindingDialog(page);
    // When the dialog opens
    await research.edit(PAT);
    // Then its body scrolls and the actions stay in view
    await expect(dialog.meta).toContainText("6 sources");
    expect(await dialog.scrollsInside()).toBe(true);
    await expect(dialog.accept).toBeInViewport();
  });

  test("Cancel closes the dialog without deciding", async ({ page }) => {
    const { api, research } = await openResearch(page);
    const dialog = new ReviewFindingDialog(page);
    await research.edit(PAT);
    await dialog.close();
    await expect(dialog.root).toBeHidden();
    await expect(research.findingButton(PAT, "Accept")).toBeVisible();
    expect(api.requests.filter((r) => r.method === "POST")).toHaveLength(0);
  });
});
