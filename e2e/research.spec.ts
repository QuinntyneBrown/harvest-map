import { expect, test } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { ResearchPage } from "./pages/ResearchPage";
import { RunResearchDialog } from "./pages/RunResearchDialog";
import { overview, runs } from "./fixtures/research";

test.describe("L2-023 Research page (minimal)", () => {
  test("AC1: header counts, Earlier runs with number, title, start, person, findings and status, and Run research", async ({ page }) => {
    // Given runs exist
    const api = new FakeApi(page);
    await api.on("GET", "/api/research", { body: overview({ findings: [] }) });
    await api.on("GET", "/api/settings", { body: { defaultDepth: "standard" } });
    const research = new ResearchPage(page);
    // When the page loads
    await research.open();
    // Then the header, the run list and Run research show
    await expect(research.heading).toBeVisible();
    await expect(research.subtitle).toHaveText("48 runs · 1 running · 2 findings to review");
    await expect(research.runRows()).toHaveCount(3);
    await expect(research.runTitle(48)).toHaveText("#48 · Find LinkedIn profiles for 8 people");
    await expect(research.runMeta(48)).toHaveText("12:04 · Naomi Achterberg · 5 findings");
    await expect(research.runStatus(48)).toHaveText("Running");
    await expect(research.runStatus(47)).toHaveText("Done");
    await expect(research.runStatus(45)).toHaveText("Failed");
    await expect(research.run(45)).toContainText("Rate limited by 2 sources");
    // And Run research opens the dialog
    await research.runResearch.click();
    await expect(new RunResearchDialog(page).root).toBeVisible();
  });

  test("AC3: new runs and findings appear without reload while a run is in progress", async ({ page }) => {
    // Given a run in progress with no findings yet
    const api = new FakeApi(page);
    let itemCompleted = false;
    await api.on("GET", "/api/research", () =>
      itemCompleted
        ? { body: overview({ runs: [{ ...runs[0], status: "Done", findingCount: 6 }, ...runs.slice(1)], running: 0 }) }
        : { body: overview({ findings: [], findingsToReview: 0 }) },
    );
    const research = new ResearchPage(page);
    await research.open();
    await expect(research.runStatus(48)).toHaveText("Running");
    // When the run completes an item
    itemCompleted = true;
    // Then its findings appear in the review list without reload
    await expect(research.runStatus(48)).toHaveText("Done", { timeout: 10_000 });
    await expect(research.findingCards()).toHaveCount(2);
    await expect(research.subtitle).toHaveText("48 runs · 0 running · 2 findings to review");
  });

  test("AC6: no runs shows No runs yet with Run the first research", async ({ page }) => {
    // Given no runs exist
    const api = new FakeApi(page);
    await api.on("GET", "/api/research", { body: overview({ totalRuns: 0, running: 0, findingsToReview: 0, runs: [], findings: [] }) });
    await api.on("GET", "/api/settings", { body: { defaultDepth: "standard" } });
    const research = new ResearchPage(page);
    // When the page loads
    await research.open();
    // Then the empty state shows
    await expect(research.subtitle).toHaveText("No runs yet");
    await expect(research.emptyTitle).toHaveText("Ask the web");
    await research.runTheFirstResearch.click();
    await expect(new RunResearchDialog(page).root).toBeVisible();
  });

  test("AC7: skeleton while loading", async ({ page }) => {
    const api = new FakeApi(page);
    await api.hang("GET", "/api/research");
    const research = new ResearchPage(page);
    await research.open();
    await expect(research.skeleton).toBeVisible();
  });

  test("AC7: load failure shows the error with retry", async ({ page }) => {
    // Given the load fails once
    const api = new FakeApi(page);
    let recovered = false;
    await api.on("GET", "/api/research", () => (recovered ? { body: overview() } : { status: 500 }));
    const research = new ResearchPage(page);
    // When the page renders
    await research.open();
    // Then the error with retry shows, and retry recovers
    await expect(research.loadError).toBeVisible();
    recovered = true;
    await research.retry();
    await expect(research.runRows()).toHaveCount(3);
  });

  test("L2-022 AC3: a queued run shows on the Research page", async ({ page }) => {
    // Given the Research page and a run that will be queued
    const api = new FakeApi(page);
    let queued = false;
    await api.on("GET", "/api/research", () => ({
      body: queued
        ? overview({ runs: [{ id: 49, title: "Who are the key people?", startedLabel: "12:30", person: "Naomi Achterberg", findingCount: 0, status: "Queued", failureReason: null }, ...runs], findings: [] })
        : overview({ findings: [] }),
    }));
    await api.on("GET", "/api/settings", { body: { defaultDepth: "standard" } });
    await api.on("POST", "/api/research/runs", () => {
      queued = true;
      return { body: { ok: true, runId: 49 } };
    });
    const research = new ResearchPage(page);
    const dialog = new RunResearchDialog(page);
    await research.open();
    // When the user runs research from the page
    await research.runResearch.click();
    await dialog.chooseQuestion("Who are the key people?");
    await dialog.submit();
    // Then the queued run appears
    await expect(research.runStatus(49)).toHaveText("Queued");
  });
});

