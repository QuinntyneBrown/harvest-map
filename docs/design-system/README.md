# Harvest Map design system

Extracted from [docs/mocks](../mocks/README.md) on 16 Oct 2026. Open [index.html](index.html) locally.

Regenerate everything with `python docs/design-system/tools/build.py`; the HTML is generated, so edit `tools/` or the mock assets, not the pages.

## Foundations

| Page | Covers |
|---|---|
| [Color](foundations/color.html) | Ramps, roles, status, live contrast pairs |
| [Typography](foundations/typography.html) | Roles, scale, measure |
| [Spacing](foundations/spacing.html) | 4px scale, inside vs between |
| [Layout](foundations/layout.html) | Grid, margins, templates |
| [Elevation](foundations/elevation.html) | Shadows, surfaces, z-order |
| [Shape](foundations/shape.html) | Radii, borders |
| [Motion](foundations/motion.html) | Durations, easing, reduced motion |
| [Iconography](foundations/iconography.html) | Icon sheet, sizes |
| [Theming](foundations/theming.html) | Light/dark, tiers, tokens.json |
| [Responsive](foundations/responsive.html) | Breakpoint behaviour, touch |
| [Accessibility](foundations/accessibility.html) | WCAG 2.2 AA commitments |
| [Content](foundations/content.html) | Voice, numbers, microcopy |

## Components

| Component | Group | Source mocks |
|---|---|---|
| [Button](components/button.html) | Actions | `pages/field/default`, `pages/organizations/default`, `dialogs/delete-organization/default` |
| [Link](components/link.html) | Actions | `pages/organization/default`, `pages/people/default` |
| [Menu](components/menu.html) | Actions | `pages/organization/default` |
| [Command palette](components/command-palette.html) | Actions | `dialogs/command-palette/default`, `dialogs/command-palette/no-results` |
| [Text field](components/text-field.html) | Inputs | `pages/organization-edit/default`, `pages/organization-edit/invalid`, `pages/sign-in/default` |
| [Textarea](components/textarea.html) | Inputs | `pages/organization-edit/default`, `pages/settings/invalid` |
| [Select](components/select.html) | Inputs | `pages/organization-edit/default`, `pages/settings/default` |
| [Checkbox](components/checkbox.html) | Inputs | `dialogs/run-research/default`, `pages/organizations/selected` |
| [Radio group](components/radio-group.html) | Inputs | `dialogs/run-research/default`, `pages/people/default`, `dialogs/link-problem/invalid` |
| [Switch](components/switch.html) | Inputs | `pages/settings/default` |
| [File upload](components/file-upload.html) | Inputs | `dialogs/import-csv/default`, `dialogs/import-csv/failed` |
| [Form field](components/form-field.html) | Inputs | `pages/organization-edit/invalid`, `pages/person-edit/invalid` |
| [Form layout](components/form-layout.html) | Inputs | `pages/organization-edit/invalid`, `pages/organization-edit/submitting`, `pages/settings/success` |
| [Top bar](components/top-bar.html) | Navigation | `pages/field/default`, `pages/organizations/default` |
| [Sidebar navigation](components/sidebar-navigation.html) | Navigation | `dialogs/nav-sheet/default` |
| [Tabs](components/tabs.html) | Navigation | `pages/organization/default` |
| [Breadcrumb](components/breadcrumb.html) | Navigation | `pages/organization/default`, `pages/organization-edit/default` |
| [Pagination](components/pagination.html) | Navigation | `pages/organizations/long`, `pages/people/long` |
| [Skip link](components/skip-link.html) | Navigation | `pages/field/default` |
| [Card](components/card.html) | Containers | `pages/organizations/default`, `pages/settings/default` |
| [Entity card](components/entity-card.html) | Data display | `pages/organizations/default`, `pages/organizations/edge`, `pages/people/default` |
| [Question card](components/question-card.html) | Data display | `pages/field/default`, `pages/field/empty` |
| [Dialog](components/dialog.html) | Containers | `dialogs/delete-organization/default`, `dialogs/run-research/default`, `dialogs/review-finding/scroll` |
| [Drawer](components/drawer.html) | Containers | `dialogs/nav-sheet/default` |
| [Popover](components/popover.html) | Containers | `pages/map/default` |
| [Tooltip](components/tooltip.html) | Containers | `pages/field/default` |
| [Divider](components/divider.html) | Containers | `pages/organization/default` |
| [Layout primitives](components/layout.html) | Containers | `pages/field/default` |
| [Table](components/table.html) | Data display | `dialogs/import-csv/default` |
| [List](components/list.html) | Data display | `pages/notifications/default`, `pages/research/running` |
| [Facts list](components/description-list.html) | Data display | `pages/organization/default`, `pages/person/default` |
| [Avatar](components/avatar.html) | Data display | `pages/people/default` |
| [Badge](components/badge.html) | Data display | `pages/people/default`, `pages/field/default` |
| [Chip](components/chip.html) | Data display | `pages/organizations/default`, `pages/organizations/no-results` |
| [Tag](components/tag.html) | Data display | `pages/organizations/default`, `pages/organizations/edge` |
| [Status indicator](components/status.html) | Data display | `pages/organizations/default`, `pages/research/default` |
| [Score ring](components/score-ring.html) | Data display | `pages/problems/default`, `pages/problem/default` |
| [Finding](components/finding.html) | Data display | `pages/research/review`, `dialogs/review-finding/default` |
| [Timeline](components/timeline.html) | Data display | `pages/organization/default`, `pages/problem/default` |
| [Map](components/map.html) | Data display | `pages/map/default` |
| [Toast](components/toast.html) | Feedback | `notifications/toast/success`, `notifications/toast/stacked` |
| [Alert and banner](components/alert.html) | Feedback | `notifications/research-banner/info`, `notifications/offline-banner/warning`, `notifications/inline-alert/warning` |
| [Inline message](components/inline-message.html) | Feedback | `pages/settings/success`, `pages/organization-edit/invalid` |
| [Progress](components/progress.html) | Feedback | `pages/research/running`, `dialogs/import-csv/busy` |
| [Spinner](components/spinner.html) | Feedback | `dialogs/command-palette/busy`, `pages/sign-in/success` |
| [Skeleton](components/skeleton.html) | Feedback | `pages/organizations/loading`, `pages/field/loading` |
| [Empty state](components/empty-state.html) | Feedback | `pages/organizations/empty`, `pages/organizations/no-results`, `pages/organizations/error` |
| [Error page](components/error-page.html) | Feedback | `pages/not-found/default`, `pages/server-error/default`, `pages/unsupported-browser/default` |
| [Selection bar](components/selection-bar.html) | Feedback | `pages/organizations/selected` |
| [Hero field](components/hero-field.html) | Feedback | `pages/field/default` |

## Patterns

| Pattern | Covers |
|---|---|
| [Forms](patterns/forms.html) | One column in a 44rem card; validate on submit, then on input; summary first. |
| [Feedback & loading](patterns/feedback-and-loading.html) | Every action answers within 100ms; skeletons for pages, busy buttons for actions, progress for runs. |
| [Empty & error states](patterns/empty-and-error-states.html) | Teach on first run, help on no-results, recover on errors. Chrome stays. |
| [Navigation & page structure](patterns/navigation.html) | Top bar, page header with numbers, breadcrumbs on details, ⌘K everywhere. |
| [Dialogs & overlays](patterns/dialogs-and-overlays.html) | Dialog for decisions, drawer for navigation, popover for previews, page for long forms. |
| [Data tables & lists](patterns/data-lists.html) | Entity cards for records, tables for comparisons; filters as chips; 25 per page. |
| [Notifications](patterns/notifications.html) | Toast for what you did, banner for what is happening, centre for what happened while away. |
| [Content & tone](patterns/content-and-tone.html) | Minimal text: nouns, verbs and numbers. See the content foundation for the library. |
| [Research & review](patterns/research-review.html) | Ask the web → live run → findings → accept/edit/reject → records. Nothing unverified becomes fact. |

## Tokens

- `tokens/tokens.css`: source of truth (primitives, semantic, light and dark).
- `tokens/tokens.json`: DTCG export.
- `tokens/contrast-pairs.json`: every checked pair.
- `assets/components.css`: component library (generated from the mocks' `ui.css` + `harvest.css`).

## Drift found in the mocks

| Mock | Issue | Resolution |
|---|---|---|
| `assets/ui.css` | Spinner, pulse, shimmer and pin ripple used raw durations (0.8s, 1.4s, 1.6s, 2.4s, 24s, 40ms) | Added --duration-loop-fast/-loop/-loop-slow/-ambient and --stagger; shimmer 1.4s unified to 1.6s |
| `assets/ui.css` | Badge height 22px and dots 6px/10px off the 4px grid | Snapped to --size-badge (24px) and --size-dot (8px) |
| `assets/ui.css` | Tab indicator radius 2px literal | Uses --radius-xs |
| `assets/harvest.css` | Moonshot tag background used color-mix(), which cannot be contrast-checked | Uses --color-warning-bg |
| `assets/harvest.css` | Hero mask gradient used the colour keyword black | Uses currentColor (mask is alpha-only) |
| `pages/*/loading` | Skeleton widths fixed at 12–20rem overflowed 360px | Percent widths; fixed in mocks |
| `pages/field/default` | WebGPU canvas had no intrinsic size and rendered 300×150 | Explicit width/height in .field-canvas |
| `pages/map/default` | External SVG mask blocked by CORS under file:// | Data-URI mask in world-dots.css |
| `all pages` | Top-bar tooltips widened the page at 360px | visibility-hidden tooltips anchored right |
| `pages/settings/default` | Switches lacked role="switch" | Documented on the switch page; fix in product code |
| `pages/person-edit/default` | Organisation select lists every organisation | Open: replace with a searchable picker at scale |
| `pages/organization/default` | Danger text on a ghost button set with an inline colour | Open: add btn--ghost-danger when building the product |
| `several mocks` | Inline style gaps and grid-template overrides | All map to space tokens; entity row variants documented |

## Verification

```
check_contrast.py: 118 passed, 0 failed, 0 unresolved
check_design_system.py: 72 pages (50 components, 9 patterns), 0 errors, 0 warnings
check_mocks.py: 42 screens, 176 mocks, 0 errors, 0 warnings
Screenshots reviewed (16 Oct 2026): index, button, entity card, dialog, color at 360 and 1280 px, light and dark; no page overflows 360 px.

```

## Relationship to the mocks

The mocks stay the source: `tools/build_css.py` reads `docs/mocks/assets/tokens.css`, `ui.css` and `harvest.css` and writes this system's tokens and components. Fix a value in the mock assets, then rebuild both.
