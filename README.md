# Harvest Map

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Harvest Map is a responsive web app for mapping organizations that serve Christian youth. It focuses on groups that help young people with the changes AI is bringing, with loneliness, and with the search for meaning.

Users create, read, update and delete records about organizations and their key people. The app also runs web research to help answer these questions:

- Which organizations worldwide are helping Christian youth, especially with AI-driven change, loneliness and a sense of meaning?
- Which organizations are taking on huge moonshot problems?
- Who is working on the most impactful problem, and what are they doing about it?
- Who are the key people in these organizations, and what are their LinkedIn profiles?

## Contents

- [Features](#features)
- [Getting started](#getting-started)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [Security](#security)
- [Support](#support)
- [Code of conduct](#code-of-conduct)
- [License](#license)

## Features

- **Organization directory:** collect, create, read, update and delete records of organizations that serve Christian youth worldwide.
- **Map view:** see where organizations are located and what they work on.
- **Key people:** record leaders and key staff, with links to their LinkedIn profiles.
- **Problem focus:** tag organizations by the problems they address, including AI-driven change, loneliness, meaning and moonshot problems.
- **Impact comparison:** compare who is working on the most impactful problems and what they are doing.
- **Web research:** run web research to find new organizations and fill in or update records.
- **Responsive and accessible:** works on phones, tablets and desktops.

## Getting started

### Prerequisites

- [Node.js](https://nodejs.org/) 20 LTS or later
- npm 10 or later
- Git

### Installation

```bash
git clone https://github.com/QuinntyneBrown/harvest-map.git
cd harvest-map
npm install
```

### Run locally

Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` (research runs search the web through Claude). Then start PostgreSQL, create the tables, seed the signed-in user and the problem catalogue, and start the app:

```bash
docker compose up -d
npm run db:migrate
npm run db:seed            # add -- --demo for a few sample organizations and people
npm run dev
```

Then open <http://localhost:3000/questions> in your browser.

## Usage

| Task | Command |
| --- | --- |
| Start the development server | `npm run dev` |
| Create a production build | `npm run build` |
| Serve the production build | `npm run start` |
| Lint the code | `npm run lint` |
| Run the end-to-end tests | `npm run test:e2e` |

## Project structure

```
harvest-map/
├── docs/
│   ├── specs/              # L1 and L2 requirements
│   ├── detailed-designs/   # Per-feature designs
│   ├── mocks/              # Static HTML mocks
│   └── design-system/      # Design tokens and component pages
├── public/                 # Static assets
├── src/
│   ├── app/                # Next.js App Router routes and API route handlers
│   ├── components/         # Shared UI components
│   ├── features/           # Feature-specific UI, hooks and server logic
│   └── lib/                # Shared helpers, API client and validation
└── tests/
    ├── e2e/                # Playwright specs
    └── pages/              # Page objects, one per screen
```

## Development

Harvest Map is built with [Next.js](https://nextjs.org/) (App Router) and [React](https://react.dev/).

Work follows a requirements-first, test-first process:

1. Each production behavior change starts with a requirement in `docs/specs/`, a detailed design in `docs/detailed-designs/`, and a mock in `docs/mocks/`.
2. Each change is built in small slices using acceptance test-driven development (ATDD).
3. Frontend tests use [Playwright](https://playwright.dev/) with the Page Object Model. They run in Chromium only, with every API response faked through route interception.

Coding agents should read [AGENTS.md](AGENTS.md) before making changes.

## Contributing

Contributions are welcome. Before you open an issue or a pull request, please read [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

To report a security vulnerability, follow the steps in [SECURITY.md](SECURITY.md). Please don't report vulnerabilities in public issues.

## Support

For help, questions or feature requests, see [SUPPORT.md](SUPPORT.md).

## Code of conduct

This project has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md). By taking part, you agree to follow its terms.

## License

Licensed under the [MIT License](LICENSE).
