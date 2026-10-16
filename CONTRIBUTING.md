# Contributing to Harvest Map

Thank you for your interest in Harvest Map. This guide explains how to report issues, suggest changes and submit pull requests.

By taking part in this project, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Reporting issues

- Search the [existing issues](https://github.com/QuinntyneBrown/harvest-map/issues) before you open a new one.
- For a bug, include the steps to reproduce it, what you expected to happen and what happened instead. Add your browser and operating system.
- For a feature request, describe the problem you want to solve, not only the solution.
- Report security vulnerabilities as described in [SECURITY.md](SECURITY.md), not in a public issue.

## Development workflow

1. Fork the repository and create a branch from `main`:

   ```bash
   git checkout -b feature/short-description
   ```

2. Install dependencies and start the app:

   ```bash
   npm install
   npm run dev
   ```

3. Make your change, following the process below.
4. Run the checks:

   ```bash
   npm run lint
   npm run test:e2e
   ```

5. Push your branch and open a pull request against `main`.

## Process for production changes

Every new feature or change to production behavior needs these three things before any code is written:

- a requirement in `docs/specs/`
- a detailed design in `docs/detailed-designs/`
- a mock in `docs/mocks/`

Changes that only touch documentation, the design system, mocks or tests don't need them.

Implementation follows acceptance test-driven development (ATDD):

1. Split the work into small, reviewable slices.
2. For each slice, write Given-When-Then acceptance criteria.
3. Write the acceptance test and run it. Confirm it fails for the expected reason.
4. Write only the code needed to make that test pass.
5. Refactor with the tests green, then run the regression checks before you start the next slice.

## Testing guidelines

- Write frontend tests with [Playwright](https://playwright.dev/) using the Page Object Model. Use one page object per screen. Page objects own the selectors; tests only state intent.
- Fake every API response with Playwright route interception. Frontend tests must not need the backend running.
- Run tests in Chromium only.
- Test behavior, not the shape of the codebase. Don't add tests for structure, naming or banned APIs.
- Don't weaken a test to make it pass.

## Coding guidelines

- Keep changes small and focused on the task. Don't add features, abstractions or dependencies that the change doesn't need.
- Don't refactor code that isn't part of your change.
- Match the style of the code around your change.
- Meet [WCAG 2.2](https://www.w3.org/TR/WCAG22/) level AA accessibility.

See [AGENTS.md](AGENTS.md) for the full set of project rules.

## Commit messages

- Use the imperative mood in the subject line, for example "Add organization search".
- Keep the subject line to about 50 characters, and wrap the body at 72.
- Explain what changed and why in the body when it isn't obvious.

## Pull requests

- Link the issue your pull request addresses.
- Describe what changed and how you tested it.
- Include screenshots for UI changes.
- Make sure all checks pass before you ask for a review.
- Keep each pull request to one logical change.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
