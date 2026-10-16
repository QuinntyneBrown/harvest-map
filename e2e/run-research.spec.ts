import { expect, test, type Page } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { QuestionsPage } from "./pages/QuestionsPage";
import { RunResearchDialog } from "./pages/RunResearchDialog";
import { answers, overview, QUESTIONS } from "./fixtures/questions";

async function openQuestions(page: Page, defaultDepth = "standard") {
  const api = new FakeApi(page);
  await api.on("GET", "/api/questions", { body: overview });
  for (const n of [1, 2, 3, 4, 5, 6]) await api.on("GET", `/api/questions/${n}`, { body: answers[n] });
  await api.on("GET", "/api/settings", { body: { defaultDepth } });
  const questions = new QuestionsPage(page);
  await questions.open();
  await expect(questions.questionMeta(6)).toBeVisible();
  return { api, questions, dialog: new RunResearchDialog(page) };
}

test.describe("L2-022 Run research dialog", () => {
  test("AC1 / L2-025 AC6: Ask the web opens the dialog with its choices, default depth and focus", async ({ page }) => {
    // Given the Questions page and a Settings default depth of Deep
    const { questions, dialog } = await openQuestions(page, "deep");
    // When the user selects Ask the web
    await questions.openAskTheWeb();
    // Then the dialog offers question, look for and depth, with the note
    await expect(dialog.root).toBeVisible();
    await expect(dialog.questionOptions()).toHaveCount(7);
    for (const q of QUESTIONS) await expect(dialog.questionOption(q)).toBeVisible();
    await expect(dialog.questionOption("Something else")).toBeVisible();
    await expect(dialog.lookForOptions()).toHaveCount(3);
    await expect(dialog.lookFor("Organisations")).toBeChecked();
    await expect(dialog.lookFor("LinkedIn profiles")).toBeChecked();
    await expect(dialog.depthOptions()).toHaveCount(3);
    await expect(dialog.depth("Quick")).toHaveAccessibleName("Quick about 1 minute");
    await expect(dialog.depth("Deep")).toBeChecked();
    await expect(dialog.note).toHaveText("Findings need two sources, or one trusted source, before they count as verified.");
    // And focus is on the checked question
    await expect(dialog.questionOption(QUESTIONS[0])).toBeChecked();
    await expect(dialog.questionOption(QUESTIONS[0])).toBeFocused();
  });

  test("AC5 / L2-025 AC5: Re-run opens the dialog with that question preselected", async ({ page }) => {
    // Given the Questions page
    const { questions, dialog } = await openQuestions(page);
    // When the user selects Re-run on question 4
    await questions.reRun(4);
    // Then that question is preselected and focused
    await expect(dialog.questionOption(QUESTIONS[3])).toBeChecked();
    await expect(dialog.questionOption(QUESTIONS[3])).toBeFocused();
    await expect(dialog.depth("Standard")).toBeChecked();
  });

  test("AC2: Something else with an empty question stops at the error summary", async ({ page }) => {
    // Given Something else with an empty text
    const { api, questions, dialog } = await openQuestions(page);
    await questions.openAskTheWeb();
    await dialog.chooseSomethingElse();
    // When the user selects Run
    await dialog.submit();
    // Then the summary lists the problem and the field shows the message
    await expect(dialog.errorSummary).toContainText("Fix 1 thing to save");
    await expect(dialog.errorSummary).toContainText("Write the question you want answered");
    await expect(dialog.errorSummary).toBeFocused();
    await expect(dialog.customQuestion).toHaveAttribute("aria-invalid", "true");
    await expect(dialog.customQuestionError).toHaveText("Write the question you want answered");
    expect(api.sent("POST", "/api/research/runs")).toHaveLength(0);
  });

  test("AC3: valid input shows busy, queues the run, closes and shows progress on Research", async ({ page }) => {
    // Given valid input
    const { api, questions, dialog } = await openQuestions(page);
    await api.on("POST", "/api/research/runs", { delayMs: 700, body: { ok: true, runId: 49 } });
    await api.on("GET", "/api/research", { body: { totalRuns: 0, running: 0, findingsToReview: 0, runs: [], findings: [] } });
    await questions.reRun(6);
    await dialog.chooseDepth("Quick");
    await dialog.toggleLookFor("Organisations");
    // When the user selects Run
    await dialog.submit();
    // Then the dialog is busy
    await expect(dialog.run).toHaveAttribute("aria-busy", "true");
    await expect(dialog.cancel).toBeDisabled();
    await expect(dialog.depth("Deep")).toBeDisabled();
    // And the run is queued, the dialog closes and the Research page shows
    await expect(dialog.root).toBeHidden();
    await expect(page).toHaveURL(/\/research$/);
    expect(api.sent("POST", "/api/research/runs")[0].body).toEqual({
      question: 6,
      customQuestion: null,
      lookFor: ["people", "linkedin"],
      depth: "quick",
    });
  });

  test("AC4: a failed request shows the failed state with retry and keeps the choices", async ({ page }) => {
    // Given the request fails once
    const { api, questions, dialog } = await openQuestions(page);
    let calls = 0;
    await api.on("POST", "/api/research/runs", () =>
      ++calls === 1
        ? { status: 503, body: { message: "Two sources are rate-limiting us. Try again in 2 minutes, or run Quick." } }
        : { body: { ok: true, runId: 49 } },
    );
    await api.on("GET", "/api/research", { body: { totalRuns: 0, running: 0, findingsToReview: 0, runs: [], findings: [] } });
    await questions.openAskTheWeb();
    await dialog.chooseSomethingElse("Who runs AI mentoring for teens in Lagos?");
    await dialog.chooseDepth("Deep");
    // When it returns
    await dialog.submit();
    // Then the failed state shows and the choices are kept
    await expect(dialog.failedAlert).toContainText("Couldn't start the run");
    await expect(dialog.failedAlert).toContainText("Two sources are rate-limiting us. Try again in 2 minutes, or run Quick.");
    await expect(dialog.customQuestion).toHaveValue("Who runs AI mentoring for teens in Lagos?");
    await expect(dialog.depth("Deep")).toBeChecked();
    await expect(dialog.run).toBeEnabled();
    // And Run retries
    await dialog.submit();
    await expect(dialog.root).toBeHidden();
    expect(api.sent("POST", "/api/research/runs")[1].body).toMatchObject({ question: null, customQuestion: "Who runs AI mentoring for teens in Lagos?" });
  });

  test("the shortcut R opens the dialog and Cancel or Escape closes it", async ({ page }) => {
    // Given the Questions page
    const { questions, dialog } = await openQuestions(page);
    // When the user presses R
    await questions.pressShortcut("r");
    // Then the dialog opens
    await expect(dialog.root).toBeVisible();
    // And Cancel closes it
    await dialog.close();
    await expect(dialog.root).toBeHidden();
    // And Escape closes it too
    await questions.openAskTheWeb();
    await dialog.pressEscape();
    await expect(dialog.root).toBeHidden();
  });
});
