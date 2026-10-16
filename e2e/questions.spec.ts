import { expect, test } from "@playwright/test";
import { FakeApi } from "./support/fakeApi";
import { QuestionsPage } from "./pages/QuestionsPage";
import { answers, emptyOverview, overview, QUESTIONS } from "./fixtures/questions";

async function fakeAnswers(api: FakeApi) {
  for (const n of [1, 2, 3, 4, 5, 6]) await api.on("GET", `/api/questions/${n}`, { body: answers[n] });
}

test.describe("L2-025 Core questions page", () => {
  test("AC1: header counts and six questions with number, status, sources and Re-run", async ({ page }) => {
    // Given the catalogue
    const api = new FakeApi(page);
    await api.on("GET", "/api/questions", { body: overview });
    await fakeAnswers(api);
    const questions = new QuestionsPage(page);
    // When the page loads
    await questions.open();
    // Then the header and each of the six questions show
    await expect(questions.heading).toBeVisible();
    await expect(questions.subtitle).toHaveText("6 questions · 4 answered · 2 partial");
    await expect(questions.questionTitles()).toHaveText(QUESTIONS);
    await expect(questions.questionMeta(1)).toHaveText("01 · Answered · 23 sources");
    await expect(questions.questionMeta(4)).toHaveText("04 · Partial · 38 sources");
    for (const n of [1, 2, 3, 4, 5, 6]) await expect(questions.reRunButton(n)).toBeVisible();
    await expect(questions.askTheWeb).toBeVisible();
  });

  test("AC2: each question lists its top answers as links with details", async ({ page }) => {
    // Given computed answers
    const api = new FakeApi(page);
    await api.on("GET", "/api/questions", { body: overview });
    await fakeAnswers(api);
    const questions = new QuestionsPage(page);
    // When the page loads
    await questions.open();
    // Then problems list by score with their leading organization, people with role and organization,
    // and LinkedIn reports who is still missing a link
    await expect(questions.answerLinks(3)).toHaveText([
      "Scripture in every language by 2033",
      "God's Word for every child",
      "Great Commission by 2050",
    ]);
    await expect(questions.answerDetails(3).first()).toHaveText("Score 94 · illumiNations");
    await expect(questions.answerLinks(3).first()).toHaveAttribute("href", "/problems/p1");
    await expect(questions.answerDetails(5).first()).toHaveText("Executive Chair & Head of Technology · Gloo");
    await expect(questions.answerLinks(6).last()).toHaveText("8 more without LinkedIn");
  });

  test("AC3: only the question whose answer fails shows Couldn't load this answer with Retry", async ({ page }) => {
    // Given question 6's answer fails to load once
    const api = new FakeApi(page);
    await api.on("GET", "/api/questions", { body: overview });
    for (const n of [1, 2, 3, 4, 5]) await api.on("GET", `/api/questions/${n}`, { body: answers[n] });
    let recovered = false;
    await api.on("GET", "/api/questions/6", () => (recovered ? { body: answers[6] } : { status: 504 }));
    const questions = new QuestionsPage(page);
    // When rendered
    await questions.open();
    // Then only that question shows the error
    await expect(questions.answerError(6)).toContainText("Couldn't load this answer");
    await expect(questions.answerError(6)).toContainText("The findings service didn't answer in time.");
    await expect(questions.answerError(5)).toHaveCount(0);
    await expect(questions.answerLinks(5)).toHaveCount(3);
    // And Retry loads it
    recovered = true;
    await questions.retryAnswer(6);
    await expect(questions.answerLinks(6)).toHaveCount(3);
  });

  test("AC4: skeleton while the page loads", async ({ page }) => {
    // Given the page is loading
    const api = new FakeApi(page);
    await api.hang("GET", "/api/questions");
    const questions = new QuestionsPage(page);
    // When it renders
    await questions.open();
    // Then the skeleton shows
    await expect(questions.skeleton).toBeVisible();
  });

  test("AC4: empty catalogue shows the empty prompt with Ask the web", async ({ page }) => {
    // Given no data
    const api = new FakeApi(page);
    await api.on("GET", "/api/questions", { body: emptyOverview });
    const questions = new QuestionsPage(page);
    // When the page renders
    await questions.open();
    // Then the empty prompt shows
    await expect(questions.subtitle).toHaveText("Nothing answered yet");
    await expect(questions.askTheWeb).toBeVisible();
    await expect(questions.questionMeta(3)).toHaveText("03 · Open · 0 sources");
    await expect(questions.question(3).getByText("Run research to answer this")).toBeVisible();
  });

  test("AC4: page load failure shows the error with retry", async ({ page }) => {
    // Given the page fails to load once
    const api = new FakeApi(page);
    let recovered = false;
    await api.on("GET", "/api/questions", () => (recovered ? { body: overview } : { status: 500 }));
    await fakeAnswers(api);
    const questions = new QuestionsPage(page);
    // When it renders
    await questions.open();
    // Then the error with retry shows, and retry recovers
    await expect(questions.pageError).toBeVisible();
    await expect(questions.pageErrorText).toHaveText(
      "The request timed out. Try again, or share reference HM-4F2A with support.",
    );
    recovered = true;
    await questions.retryPage();
    await expect(questions.subtitle).toHaveText("6 questions · 4 answered · 2 partial");
  });
});
