#!/usr/bin/env python3
"""Build the Harvest Map design system docs.

    python docs/design-system/tools/build.py

Runs build_css.py (tokens.css, components.css), extends contrast-pairs.json,
then writes every foundation, component and pattern page, index.html and README.md.
Afterwards run the skill's check_contrast.py, tokens_to_json.py and check_design_system.py.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
subprocess.run([sys.executable, str(HERE / "build_css.py")], check=True)

import components  # noqa: E402
import foundations  # noqa: E402
import patterns  # noqa: E402
MOCK_COUNT = (lambda m: f"{sum(len(s['states']) for s in m['screens'])} mocks, {len(m['screens'])} screens")(json.loads((HERE.parents[1] / "mocks" / "manifest.json").read_text(encoding="utf-8")))
from shell import COMPONENTS, DATE, FOUNDATIONS, PATTERNS, PRODUCT, ROOT, page  # noqa: E402

EXTRA_PAIRS = [
    ("--color-fg-muted", "--color-bg-subtle", 4.5, "default tag text"),
    ("--color-fg-accent", "--color-accent-subtle", 4.5, "AI tag, mark initials, avatar"),
    ("--color-warning-fg", "--color-warning-bg", 4.5, "Moonshot tag"),
    ("--color-success-fg", "--color-bg-canvas", 4.5, "Verified status on page"),
    ("--color-warning-fg", "--color-bg-canvas", 4.5, "Unverified status on page"),
    ("--color-danger-fg", "--color-bg-canvas", 4.5, "Conflict status on page"),
    ("--color-fg-muted", "--color-bg-surface-sunken", 4.5, "kbd text"),
    ("--color-accent", "--color-bg-subtle-hover", 3, "score ring fill vs track"),
    ("--color-warning-icon", "--color-bg-surface", 3, "rank-1 ring, unverified pin"),
    ("--color-fg-inverse", "--color-bg-inverse", 4.5, "selection bar, toast"),
    ("--color-border-inverse", "--color-bg-inverse", 3, "selection bar button edge"),
]


def extend_pairs() -> None:
    path = ROOT / "tokens" / "contrast-pairs.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    have = {(p["fg"], p["bg"]) for p in data["pairs"]}
    for fg, bg, m, note in EXTRA_PAIRS:
        if (fg, bg) not in have:
            data["pairs"].append({"fg": fg, "bg": bg, "min": m, "note": f"Harvest Map: {note}"})
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


DRIFT = [
    ("assets/ui.css", "Spinner, pulse, shimmer and pin ripple used raw durations (0.8s, 1.4s, 1.6s, 2.4s, 24s, 40ms)", "Added --duration-loop-fast/-loop/-loop-slow/-ambient and --stagger; shimmer 1.4s unified to 1.6s"),
    ("assets/ui.css", "Badge height 22px and dots 6px/10px off the 4px grid", "Snapped to --size-badge (24px) and --size-dot (8px)"),
    ("assets/ui.css", "Tab indicator radius 2px literal", "Uses --radius-xs"),
    ("assets/harvest.css", "Moonshot tag background used color-mix(), which cannot be contrast-checked", "Uses --color-warning-bg"),
    ("assets/harvest.css", "Hero mask gradient used the colour keyword black", "Uses currentColor (mask is alpha-only)"),
    ("pages/*/loading", "Skeleton widths fixed at 12–20rem overflowed 360px", "Percent widths; fixed in mocks"),
    ("pages/field/default", "WebGPU canvas had no intrinsic size and rendered 300×150", "Explicit width/height in .field-canvas"),
    ("pages/map/default", "External SVG mask blocked by CORS under file://", "Data-URI mask in world-dots.css"),
    ("all pages", "Top-bar tooltips widened the page at 360px", "visibility-hidden tooltips anchored right"),
    ("pages/settings/default", "Switches lacked role=\"switch\"", "Documented on the switch page; fix in product code"),
    ("pages/person-edit/default", "Organisation select lists every organisation", "Open: replace with a searchable picker at scale"),
    ("pages/organization/default", "Danger text on a ghost button set with an inline colour", "Open: add btn--ghost-danger when building the product"),
    ("several mocks", "Inline style gaps and grid-template overrides", "All map to space tokens; entity row variants documented"),
]


def index() -> None:
    def cards(folder, entries):
        return '<div class="ds-cards">' + "".join(f'<a class="ds-card" href="{folder}/{pid}.html"><b>{label}</b><span>{folder[:-1].title()}</span></a>' for pid, label in entries) + "</div>"
    comps = [(c, n) for c, n, _ in COMPONENTS]
    start = '<div class="ds-cards">' + "".join(f'<a class="ds-card" href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in [
        ("foundations/color.html", "Color", "Stone and ember, both themes"), ("foundations/typography.html", "Typography", "Big numbers, little text"),
        ("foundations/layout.html", "Layout", "Top bar, wide margins"), ("components/button.html", "Button", "Every variant and state"),
        ("components/form-field.html", "Form field", "Label, help, error"), ("components/dialog.html", "Dialog", "Sheets on phones")]) + "</div>"
    sections = [
        ("start", "Start here", start, None),
        ("foundations", "Foundations", cards("foundations", FOUNDATIONS), None),
        ("components", "Components", cards("components", comps), None),
        ("patterns", "Patterns", cards("patterns", PATTERNS), None),
        ("how", "How to use", "<ol><li>Link <code>tokens/tokens.css</code> then <code>assets/components.css</code>.</li><li>Use the class names on each component page.</li><li>Generate platform constants from <code>tokens/tokens.json</code> (DTCG).</li><li>Chrome 125+ only, by design.</li></ol>", None),
        ("provenance", "Provenance", f'<p>Extracted from <a href="../mocks/index.html">docs/mocks</a> ({MOCK_COUNT}) on {DATE}. Regenerate with <code>python docs/design-system/tools/build.py</code>.</p>', None),
    ]
    page("index.html", f"{PRODUCT} design system", "Design system", "The visual and interaction language of Harvest Map: whitespace first, minimal text, Chrome-native motion and a WebGPU field.", sections,
         meta=f'<span class="ds-pill ds-pill--ok">WCAG 2.2 AA</span><span class="ds-pill">{len(FOUNDATIONS)} foundations</span><span class="ds-pill">{len(COMPONENTS)} components</span><span class="ds-pill">{len(PATTERNS)} patterns</span>')


def readme(contrast: str, structure: str) -> None:
    lines = [f"# {PRODUCT} design system", "", f"Extracted from [docs/mocks](../mocks/README.md) on {DATE}. Open [index.html](index.html) locally.", "",
             "Regenerate everything with `python docs/design-system/tools/build.py`; the HTML is generated, so edit `tools/` or the mock assets, not the pages.", "",
             "## Foundations", "", "| Page | Covers |", "|---|---|"]
    covers = {"color": "Ramps, roles, status, live contrast pairs", "typography": "Roles, scale, measure", "spacing": "4px scale, inside vs between", "layout": "Grid, margins, templates",
              "elevation": "Shadows, surfaces, z-order", "shape": "Radii, borders", "motion": "Durations, easing, reduced motion", "iconography": "Icon sheet, sizes",
              "theming": "Light/dark, tiers, tokens.json", "responsive": "Breakpoint behaviour, touch", "accessibility": "WCAG 2.2 AA commitments", "content": "Voice, numbers, microcopy"}
    lines += [f"| [{label}](foundations/{pid}.html) | {covers[pid]} |" for pid, label in FOUNDATIONS]
    lines += ["", "## Components", "", "| Component | Group | Source mocks |", "|---|---|---|"]
    by_id = {s["id"]: s for s in components.SPECS}
    for cid, name, group in COMPONENTS:
        lines.append(f"| [{name}](components/{cid}.html) | {group} | " + ", ".join(f"`{s}`" for s in by_id[cid]["sources"][:3]) + " |")
    lines += ["", "## Patterns", "", "| Pattern | Covers |", "|---|---|"]
    lines += [f"| [{p['title']}](patterns/{p['pid']}.html) | {p['lead']} |" for p in patterns.P]
    lines += ["", "## Tokens", "", "- `tokens/tokens.css`: source of truth (primitives, semantic, light and dark).", "- `tokens/tokens.json`: DTCG export.", "- `tokens/contrast-pairs.json`: every checked pair.", "- `assets/components.css`: component library (generated from the mocks' `ui.css` + `harvest.css`).", "",
              "## Drift found in the mocks", "", "| Mock | Issue | Resolution |", "|---|---|---|"]
    lines += [f"| `{m}` | {i} | {r} |" for m, i, r in DRIFT]
    lines += ["", "## Verification", "", "```", contrast.strip(), structure.strip(), "```", ""]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    extend_pairs()
    components.build()
    foundations.build()
    patterns.build()
    index()
    readme("(run tools/verify.sh to fill)", "")
    print(f"{len(FOUNDATIONS)} foundations, {len(COMPONENTS)} components, {len(PATTERNS)} patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
