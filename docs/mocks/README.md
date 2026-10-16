# Harvest Map mocks

Static HTML mocks for every page, dialog and notification of **Harvest Map**, in
every state. Harvest Map is a Chrome-only, responsive web app for collecting and
researching the organisations, people and moonshot problems around Christian
youth and AI, and for answering six standing questions:

1. Who is helping Christian youth, especially with AI?
2. Who is targeting moonshot problems?
3. Who is targeting the most impactful problem?
4. What are they doing?
5. Who are the key people?
6. Where are they on LinkedIn?

Open [index.html](index.html) from disk to browse the gallery. Every mock has a
mock bar at the bottom with its sibling states and a theme toggle.
`?theme=dark` forces dark, `?chrome=0` hides the mock bar and notes, and the
`t` key toggles the theme.

<!--
Cast and catalog (reuse these in every mock; today is Thu 16 Oct 2026)

Signed in:  Naomi Achterberg (NA), research lead, naomi@harvestmap.app
Team:       Tobias Mwangi (TM) researcher · Priya Raman (PR) researcher ·
            Elias Ferreira (EF) analyst · Hannah Okafor (HO) admin
Workspace:  Harvest Map · 14 organisations · 16 people · 9 problems · 48 runs

Organisations (real, public): FaithTech (Waterloo), Gloo (Boulder), OneHope
(Pompano Beach), illumiNations (alliance), Lausanne Movement, YouVersion
(Edmond), Creed, Fuller Youth Institute (Pasadena), American Bible Society
(Philadelphia), Indigitous (Singapore), Alpha International (London),
Dare 2 Share (Arvada), Barna Group (Ventura), Young Life (Colorado Springs).
Just-created example: Kingdom Code (London). Archived example: Kingdom Code.

People (real, public roles): James Kelly · Scott Beck · Pat Gelsinger ·
Rob Hoskins · Bob Hoskins · Mart Green · Michael Oh · Bobby Gruenewald ·
Adi Agrawal · Kara Powell · Jennifer Holloran · Simon Seow · Nicky Gumbel ·
Greg Stier · David Kinnaman · Newt Crenshaw. New-person example: Elise Varga.

Problems (ranked by impact = reach × severity × tractability):
94 Scripture in every language by 2033 · 91 God's Word for every child ·
88 Great Commission by 2050 · 83 AI that serves human flourishing ·
79 Gen Z loneliness and faith formation · 72 Every teen hears the gospel from
a friend · 64 Safe AI companions for young believers · 61 Young adults
engaging Scripture · 58 Digital evangelism at scale.

Research runs: #48 running (LinkedIn profiles, 62%) · #47 done (12 findings)
· #46 done · #45 failed (rate limited) · #44 done (scored 9 problems).
Reference codes: HM-4F2A (load failure), HM-9C21 (500).
-->

## What the product is

- **Field** (home): the six questions as cards with their current answer, the
  top three problems and the latest research runs, under a WebGPU particle
  field.
- **Organizations / People / Problems**: CRUD lists and detail pages. Every
  fact carries a verification status (Verified, Unverified, Conflict, Not
  found) because most records are written by research runs, not by hand.
- **Questions**: the six questions with answers that link to the records
  behind them, plus a Re-run action.
- **Research**: "Ask the web" runs with a live log; findings come back for
  review and only become records when a person accepts them.
- **Map**: a dot-matrix world map with organisation pins and a note on where
  the catalogue has gaps.
- **Search**, **Notifications**, **Settings**, sign-in flow and the five
  error pages (404, 403, 500, offline, unsupported browser).

## Design decisions

- **Whitespace first.** Topbar-only shell, 76 rem container, 64 px page
  margins on desktop, 96 px between sections, one primary action per screen,
  minimal copy (labels are nouns, buttons are verbs, numbers carry the story).
- **Warm neutrals and an ember accent.** Light accent is ember-700 (5.2:1 on
  white); dark accent is ember-300 on stone-900 (11:1). All colours, sizes and
  durations live in `assets/tokens.css`.
- **Chrome only, on purpose.** The mocks use features that only Chrome 125+
  ships: WebGPU (`assets/field.js`), cross-document view transitions
  (`@view-transition`), `@starting-style` entrances, scroll-driven animations
  (`animation-timeline: view()`), CSS anchor positioning for the map popover
  (`position-anchor`, `position-area`), `scroll-state()` container queries for
  the topbar shadow, `field-sizing: content` textareas, `interpolate-size`
  accordions, `linear()` spring easing, `@property`-animated score rings,
  `color-mix()` in oklch. `pages/unsupported-browser` explains the policy;
  detection is feature-based, not user-agent based.
- **Micro-animations with purpose.** Cards rise 40 ms apart on entry, lift on
  hover with a spring, score rings fill from 0, pins pulse on a stagger, the
  hero field drifts. Everything stops under `prefers-reduced-motion`.
- **WebGPU field.** `assets/field.js` runs a compute pass that drifts 4,000
  grains with value noise and a render pass that draws them as soft points,
  tinted from the accent token. Without WebGPU the canvas gets
  `data-gpu="off"` and a slow CSS gradient takes over (that is what the
  screenshot sweep captures, since the headless shell has no GPU).
- **LinkedIn links.** A person shows a LinkedIn link only when one is stored,
  added by research or the person edit form; otherwise "No LinkedIn yet".

## Files

```
docs/mocks/
  README.md, index.html, manifest.json
  assets/tokens.css      design tokens (light + dark)
  assets/ui.css          starter component kit (unchanged from the skill)
  assets/harvest.css     Harvest Map components and Chrome-only behaviour
  assets/mock.css/.js    mock bar and theme switch (not product UI)
  assets/field.js        WebGPU field
  assets/world-dots.svg  dot-matrix world map (served) and world-dots.css (data URI for file://)
  tools/                 generator: data.py (cast), build.py (manifest + shell), pages.py, dialogs.py, notifications.py
  pages/, dialogs/, notifications/
```

The HTML is generated. Change a renderer or the manifest, then:

```sh
python docs/mocks/tools/build.py
python .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks --write
python .claude/skills/writing-html-mocks/scripts/screenshot_mocks.py docs/mocks
```

Screenshots land in `docs/mocks/.cache/mocks/` (do not commit) with a contact
sheet at `.cache/mocks/index.html`. Two things to know when reading them: the
sweep captures 150 ms after load, so dialogs and cards are sometimes caught
mid-entrance (slightly transparent); and the headless shell has no GPU, so the
hero shows the CSS fallback rather than the WebGPU field. Open the mock in
Chrome to see both settled.

## Open questions and assumptions

- No `docs/specs` exist yet, so there are no requirement IDs. The screen list
  comes from the request; `writing-requirements` can backfill IDs into
  `manifest.json` later.
- Harvest Map is assumed invite-only (no sign-up page). Workspace members are
  invited by an admin.
- "Impact" is modelled as reach × severity × tractability on a 0–100 scale,
  set by a research run and editable by hand. The formula is a placeholder for
  the team to agree.
- Organisation and people facts come from public sources checked on
  16 Oct 2026; items the product shows as *Unverified* are exactly the ones
  that could not be confirmed from a primary source (Creed's user numbers,
  Indigitous' founder, Dare 2 Share's founder, Young Life's president, Mart
  Green's current title, Jennifer Holloran's title). Verify before reusing
  the catalogue as data.
- Cookie consent is not applicable: the app is an internal tool with no
  third-party cookies. Billing, plan limits and trial states do not exist.
- The home page is called "Field"; rename if the team prefers "Home".
- The map uses an equirectangular dot grid; organisations without a single
  home (alliances, movements) are listed below it instead of being pinned.

## Next step

Run `extracting-design-systems` to turn these mocks into `docs/design-system/`.

## Coverage

<!-- coverage:start -->

Legend: ✅ mock exists · ➖ not applicable (reason in manifest) · ❌ missing

### Pages

| Screen | default | loading | empty | error | invalid | submitting | success | partial | no-results | long | selected | edge | read-only | running | review | read | Requirements |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sign in (`sign-in`) | [✅](pages/sign-in/default.html) | ➖ | ➖ | [✅](pages/sign-in/error.html) | [✅](pages/sign-in/invalid.html) | [✅](pages/sign-in/submitting.html) | [✅](pages/sign-in/success.html) |  |  |  |  |  |  |  |  |  |  |
| Forgot password (`forgot-password`) | [✅](pages/forgot-password/default.html) | ➖ | ➖ | [✅](pages/forgot-password/error.html) | [✅](pages/forgot-password/invalid.html) | [✅](pages/forgot-password/submitting.html) | [✅](pages/forgot-password/success.html) |  |  |  |  |  |  |  |  |  |  |
| Reset password (`reset-password`) | [✅](pages/reset-password/default.html) | [✅](pages/reset-password/loading.html) | ➖ | [✅](pages/reset-password/error.html) | [✅](pages/reset-password/invalid.html) | [✅](pages/reset-password/submitting.html) | [✅](pages/reset-password/success.html) |  |  |  |  |  |  |  |  |  |  |
| Field (`field`) | [✅](pages/field/default.html) | [✅](pages/field/loading.html) | [✅](pages/field/empty.html) | [✅](pages/field/error.html) |  |  |  | [✅](pages/field/partial.html) |  |  |  |  |  |  |  |  |  |
| Organizations (`organizations`) | [✅](pages/organizations/default.html) | [✅](pages/organizations/loading.html) | [✅](pages/organizations/empty.html) | [✅](pages/organizations/error.html) |  |  |  |  | [✅](pages/organizations/no-results.html) | [✅](pages/organizations/long.html) | [✅](pages/organizations/selected.html) | [✅](pages/organizations/edge.html) |  |  |  |  |  |
| Organization (`organization`) | [✅](pages/organization/default.html) | [✅](pages/organization/loading.html) | [✅](pages/organization/empty.html) | [✅](pages/organization/error.html) |  |  |  |  |  |  |  | [✅](pages/organization/edge.html) | [✅](pages/organization/read-only.html) |  |  |  |  |
| Edit organization (`organization-edit`) | [✅](pages/organization-edit/default.html) | [✅](pages/organization-edit/loading.html) | ➖ | [✅](pages/organization-edit/error.html) | [✅](pages/organization-edit/invalid.html) | [✅](pages/organization-edit/submitting.html) | [✅](pages/organization-edit/success.html) |  |  |  |  |  |  |  |  |  |  |
| People (`people`) | [✅](pages/people/default.html) | [✅](pages/people/loading.html) | [✅](pages/people/empty.html) | [✅](pages/people/error.html) |  |  |  |  | [✅](pages/people/no-results.html) | [✅](pages/people/long.html) |  |  |  |  |  |  |  |
| Person (`person`) | [✅](pages/person/default.html) | [✅](pages/person/loading.html) | [✅](pages/person/empty.html) | [✅](pages/person/error.html) |  |  |  |  |  |  |  | [✅](pages/person/edge.html) |  |  |  |  |  |
| Edit person (`person-edit`) | [✅](pages/person-edit/default.html) | [✅](pages/person-edit/loading.html) | ➖ | [✅](pages/person-edit/error.html) | [✅](pages/person-edit/invalid.html) | [✅](pages/person-edit/submitting.html) | [✅](pages/person-edit/success.html) |  |  |  |  |  |  |  |  |  |  |
| Problems (`problems`) | [✅](pages/problems/default.html) | [✅](pages/problems/loading.html) | [✅](pages/problems/empty.html) | [✅](pages/problems/error.html) |  |  |  |  | [✅](pages/problems/no-results.html) |  |  |  |  |  |  |  |  |
| Problem (`problem`) | [✅](pages/problem/default.html) | [✅](pages/problem/loading.html) | [✅](pages/problem/empty.html) | [✅](pages/problem/error.html) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Edit problem (`problem-edit`) | [✅](pages/problem-edit/default.html) | [✅](pages/problem-edit/loading.html) | ➖ | [✅](pages/problem-edit/error.html) | [✅](pages/problem-edit/invalid.html) | [✅](pages/problem-edit/submitting.html) | [✅](pages/problem-edit/success.html) |  |  |  |  |  |  |  |  |  |  |
| Questions (`questions`) | [✅](pages/questions/default.html) | [✅](pages/questions/loading.html) | [✅](pages/questions/empty.html) | [✅](pages/questions/error.html) |  |  |  | [✅](pages/questions/partial.html) |  |  |  |  |  |  |  |  |  |
| Research (`research`) | [✅](pages/research/default.html) | [✅](pages/research/loading.html) | [✅](pages/research/empty.html) | [✅](pages/research/error.html) |  |  |  |  |  |  |  |  |  | [✅](pages/research/running.html) | [✅](pages/research/review.html) |  |  |
| Map (`map`) | [✅](pages/map/default.html) | [✅](pages/map/loading.html) | [✅](pages/map/empty.html) | [✅](pages/map/error.html) |  |  |  |  | [✅](pages/map/no-results.html) |  |  |  |  |  |  |  |  |
| Search (`search`) | [✅](pages/search/default.html) | [✅](pages/search/loading.html) | [✅](pages/search/empty.html) | [✅](pages/search/error.html) |  |  |  |  | [✅](pages/search/no-results.html) |  |  |  |  |  |  |  |  |
| Notifications (`notifications`) | [✅](pages/notifications/default.html) | [✅](pages/notifications/loading.html) | [✅](pages/notifications/empty.html) | [✅](pages/notifications/error.html) |  |  |  |  |  |  |  |  |  |  |  | [✅](pages/notifications/read.html) |  |
| Settings (`settings`) | [✅](pages/settings/default.html) | [✅](pages/settings/loading.html) | ➖ | [✅](pages/settings/error.html) | [✅](pages/settings/invalid.html) | [✅](pages/settings/submitting.html) | [✅](pages/settings/success.html) |  |  |  |  |  |  |  |  |  |  |
| Not found (`not-found`) | [✅](pages/not-found/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Forbidden (`forbidden`) | [✅](pages/forbidden/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Something went wrong (`server-error`) | [✅](pages/server-error/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Offline (`offline`) | [✅](pages/offline/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Unsupported browser (`unsupported-browser`) | [✅](pages/unsupported-browser/default.html) | ➖ | ➖ | ➖ |  |  |  |  |  |  |  |  |  |  |  |  |  |

### Dialogs

| Screen | default | busy | invalid | no-results | failed | success | scroll | Requirements |
|---|---|---|---|---|---|---|---|---|
| Navigation (`nav-sheet`) | [✅](dialogs/nav-sheet/default.html) | ➖ | ➖ |  |  |  |  |  |
| Command palette (`command-palette`) | [✅](dialogs/command-palette/default.html) | [✅](dialogs/command-palette/busy.html) | ➖ | [✅](dialogs/command-palette/no-results.html) |  |  |  |  |
| Delete organization (`delete-organization`) | [✅](dialogs/delete-organization/default.html) | [✅](dialogs/delete-organization/busy.html) | [✅](dialogs/delete-organization/invalid.html) |  | [✅](dialogs/delete-organization/failed.html) |  |  |  |
| Delete person (`delete-person`) | [✅](dialogs/delete-person/default.html) | [✅](dialogs/delete-person/busy.html) | ➖ |  | [✅](dialogs/delete-person/failed.html) |  |  |  |
| Delete problem (`delete-problem`) | [✅](dialogs/delete-problem/default.html) | [✅](dialogs/delete-problem/busy.html) | ➖ |  | [✅](dialogs/delete-problem/failed.html) |  |  |  |
| Add person (`add-person`) | [✅](dialogs/add-person/default.html) | [✅](dialogs/add-person/busy.html) | [✅](dialogs/add-person/invalid.html) |  | [✅](dialogs/add-person/failed.html) | [✅](dialogs/add-person/success.html) |  |  |
| Link problem (`link-problem`) | [✅](dialogs/link-problem/default.html) | [✅](dialogs/link-problem/busy.html) | [✅](dialogs/link-problem/invalid.html) |  | [✅](dialogs/link-problem/failed.html) |  |  |  |
| Run research (`run-research`) | [✅](dialogs/run-research/default.html) | [✅](dialogs/run-research/busy.html) | [✅](dialogs/run-research/invalid.html) |  | [✅](dialogs/run-research/failed.html) |  |  |  |
| Review finding (`review-finding`) | [✅](dialogs/review-finding/default.html) | [✅](dialogs/review-finding/busy.html) | [✅](dialogs/review-finding/invalid.html) |  | [✅](dialogs/review-finding/failed.html) |  | [✅](dialogs/review-finding/scroll.html) |  |
| Import CSV (`import-csv`) | [✅](dialogs/import-csv/default.html) | [✅](dialogs/import-csv/busy.html) | [✅](dialogs/import-csv/invalid.html) |  | [✅](dialogs/import-csv/failed.html) | [✅](dialogs/import-csv/success.html) |  |  |
| Export (`export`) | [✅](dialogs/export/default.html) | [✅](dialogs/export/busy.html) | ➖ |  | [✅](dialogs/export/failed.html) |  |  |  |
| Sign out (`sign-out`) | [✅](dialogs/sign-out/default.html) | [✅](dialogs/sign-out/busy.html) | ➖ |  | [✅](dialogs/sign-out/failed.html) |  |  |  |
| Unsaved changes (`unsaved-changes`) | [✅](dialogs/unsaved-changes/default.html) | ➖ | ➖ |  |  |  |  |  |
| Keyboard shortcuts (`keyboard-shortcuts`) | [✅](dialogs/keyboard-shortcuts/default.html) | ➖ | ➖ |  |  |  |  |  |

### Notifications

| Screen | info | success | warning | danger | with-action | stacked | persistent | Requirements |
|---|---|---|---|---|---|---|---|---|
| Toast (`toast`) | [✅](notifications/toast/info.html) | [✅](notifications/toast/success.html) | [✅](notifications/toast/warning.html) | [✅](notifications/toast/danger.html) | [✅](notifications/toast/with-action.html) | [✅](notifications/toast/stacked.html) |  |  |
| Research banner (`research-banner`) | [✅](notifications/research-banner/info.html) | [✅](notifications/research-banner/success.html) | [✅](notifications/research-banner/warning.html) | [✅](notifications/research-banner/danger.html) |  |  | [✅](notifications/research-banner/persistent.html) |  |
| Offline banner (`offline-banner`) | [✅](notifications/offline-banner/info.html) | [✅](notifications/offline-banner/success.html) | [✅](notifications/offline-banner/warning.html) | [✅](notifications/offline-banner/danger.html) |  |  | [✅](notifications/offline-banner/persistent.html) |  |
| Inline alert (`inline-alert`) | [✅](notifications/inline-alert/info.html) | [✅](notifications/inline-alert/success.html) | [✅](notifications/inline-alert/warning.html) | [✅](notifications/inline-alert/danger.html) | [✅](notifications/inline-alert/with-action.html) |  |  |  |

<!-- coverage:end -->
