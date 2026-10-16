"""Foundation pages. Every token in tokens.css appears on exactly one of them."""
from __future__ import annotations

import re

from shell import ICONS, ROOT, example, icon, page, pair, table, token_table, ul

TOKENS_CSS = (ROOT / "tokens" / "tokens.css").read_text(encoding="utf-8")
ROOT_BLOCK = TOKENS_CSS[TOKENS_CSS.index(":root {"):TOKENS_CSS.index("color-scheme: light;")]
ALL = list(dict.fromkeys(re.findall(r"(--[\w-]+)\s*:", ROOT_BLOCK)))


def pick(*prefixes: str) -> list[str]:
    return [t for t in ALL if t.startswith(prefixes)]


def tok_rows(tokens: list[str], usage: dict[str, str] | None = None) -> str:
    usage = usage or {}
    return token_table([(usage.get(t, t.removeprefix("--").replace("-", " ")), t) for t in tokens])


def sec(sid, title, body):
    return (sid, title, body, None)


# ---------------------------------------------------------------- color
def color():
    ramps = ""
    for hue in ["gray", "ember", "green", "amber", "red"]:
        steps = [t for t in ALL if t.startswith(f"--palette-{hue}-")]
        ramps += f"<h3>{hue.title()}</h3><div class=\"ds-ramp\">" + "".join(f'<span style="--swatch: var({t});" data-step="{t.rsplit("-", 1)[1]}"></span>' for t in steps) + "</div>"
    roles = pick("--color-")
    sw = "".join(f'<div class="ds-swatch"><div class="ds-swatch__chip" style="--swatch: var({t});"></div><div class="ds-swatch__body"><span class="ds-swatch__name">{t}</span><span class="ds-swatch__value" data-token="{t}"></span></div></div>' for t in roles if not t.startswith(("--color-info", "--color-success", "--color-warning", "--color-danger")))
    status = "".join(f'<div class="alert alert--{s}" role="status">{icon(s)}<div class="alert__body"><div class="alert__title">{s.title()}</div><div>Text on {s} background.</div></div></div>' for s in ["info", "success", "warning", "danger"])
    import json
    pairs = json.loads((ROOT / "tokens" / "contrast-pairs.json").read_text(encoding="utf-8"))["pairs"]
    pair_html = "".join(pair(p.get("note", ""), p["fg"], p["bg"], p["min"]) for p in pairs if p["fg"].startswith("--") and p["bg"].startswith("--"))
    both = ('<div class="ds-themes">' + "".join(f'<div data-theme="{th}"><div class="ds-swatches">' + "".join(f'<div class="ds-swatch"><div class="ds-swatch__chip" style="--swatch: var({t});"></div><div class="ds-swatch__body"><span class="ds-swatch__name">{t}</span><span class="ds-swatch__value" data-token="{t}"></span></div></div>' for t in ["--color-bg-canvas", "--color-bg-surface", "--color-accent", "--color-fg-default"]) + "</div></div>" for th in ["light", "dark"]) + "</div>")
    page("foundations/color.html", "Color", "Foundation", "Warm stone neutrals and one ember accent. Every pair passes WCAG 2.2 AA in both themes.", [
        sec("overview", "Overview", "<p>Colour is quiet so content and whitespace lead. One accent (ember) marks the primary action, current navigation and highlights. Status colours always come with an icon and a word.</p>" + both),
        sec("primitives", "Primitive ramps", "<p>Raw values. Only semantic tokens reference them.</p>" + ramps),
        sec("roles", "Semantic roles", f'<div class="ds-swatches">{sw}</div>'),
        sec("status", "Status colours", f'<div class="stack">{status}</div>'),
        sec("usage", "Usage", ul(["Accent is ember-700 on light (5.2:1 on white), ember-300 on dark.", "Never use a primitive in a component.", "AI tags use accent-subtle; Moonshot tags use warning-bg.", "Gold (warning-icon) is reserved for rank 1."])),
        sec("accessibility", "Contrast pairs", "<p>Live ratios for every pair in <code>tokens/contrast-pairs.json</code>, in the current theme. Toggle the theme to check dark.</p>" + pair_html),
        sec("brand-theme", "Adding a brand theme", "<p>Add a <code>[data-theme=\"&lt;name&gt;\"]</code> block overriding <code>--color-accent*</code> and <code>--color-fg-accent</code>, add pairs, run <code>check_contrast.py</code>.</p>"),
        sec("tokens", "Tokens", tok_rows(pick("--palette-", "--color-", "--shadow-color"))),
    ])


def typography():
    roles = ["--text-display", "--text-h1", "--text-h2", "--text-h3", "--text-h4", "--text-body-lg", "--text-body", "--text-body-sm", "--text-label", "--text-caption", "--text-overline", "--text-code"]
    spec = "".join(f'<div class="ds-specimen"><span style="font: var({t});">The field is ripe</span><span class="ds-specimen__meta">{t} · <span data-token="{t}"></span></span></div>' for t in roles)
    page("foundations/typography.html", "Typography", "Foundation", "Inter (Segoe UI Variable fallback), nine sizes, tight display, 16px body. Minimal text, big numbers.", [
        sec("overview", "Overview", "<p>Headings are bold and tight; numbers carry the story (tabular, h2 size on question cards). Copy is short. Headings use <code>text-wrap: balance</code>, paragraphs <code>pretty</code>.</p>"),
        sec("roles", "Roles", spec),
        sec("scale", "Size scale", '<div class="ds-scale">' + "".join(f'<div class="ds-scale__row"><code>{t}</code><span data-token="{t}"></span><span style="font-size: var({t});">Aa</span></div>' for t in pick("--font-size-")) + "</div>"),
        sec("usage", "Usage", ul(["Body is 16px; nothing below 12px.", "Display (48px) only for the Field hero and error codes.", "Line length capped at --layout-measure (65ch).", "Numbers: tabular-nums, thousands separators."])),
        sec("accessibility", "Accessibility", ul(["All sizes in rem; reflows at 200% zoom.", "Text spacing overrides (1.4.12) do not clip: no fixed heights on text containers."])),
        sec("tokens", "Tokens", tok_rows(pick("--font-", "--line-height-", "--letter-spacing-", "--text-"))),
    ])


def spacing():
    page("foundations/spacing.html", "Spacing", "Foundation", "A 4px scale used generously: 64px between sections, 96px around the page.", [
        sec("overview", "Overview", "<p>Whitespace is the brand. Related things sit 8–12px apart; unrelated sections 64px.</p>"),
        sec("scale", "Scale", '<div class="ds-scale">' + "".join(f'<div class="ds-scale__row"><code>{t}</code><span data-token="{t}"></span><span class="ds-scale__bar" style="--size: var({t});"></span></div>' for t in pick("--space-")) + "</div>"),
        sec("usage", "Inside vs between", table(["Context", "Token"], [["Icon to label", "--space-1/2"], ["Inside chips and badges", "--space-2"], ["Field parts", "--space-1"], ["Between fields", "--space-6"], ["Card padding", "--space-6 / --space-8"], ["Between cards", "--space-3 (lists) / --space-6 (grids)"], ["Header to content", "--space-12"], ["Between sections", "--space-16"], ["Page top/bottom", "--space-16 / --space-24"]])),
        sec("tokens", "Tokens", tok_rows(pick("--space-"))),
    ])


def layout():
    page("foundations/layout.html", "Layout", "Foundation", "Top-bar shell, 76rem container, 4/8/12 columns, wide margins.", [
        sec("overview", "Overview", "<p>No sidebar: the top bar carries navigation, the page gets the width. Detail pages split 2:1 with an aside from 1024px.</p>"),
        sec("grid", "Grid", '<div class="ds-grid-demo">' + "".join(f"<span>{i}</span>" for i in range(1, 13)) + "</div>" + table(["Breakpoint", "Columns", "Gutter", "Margin"], [["0–767", "4", "16px", "20px"], ["768–1023", "8", "24px", "40px"], ["≥ 1024", "12", "32px", "64px"]])),
        sec("templates", "Page templates", ul(["<b>Shell</b>: top bar + <code>main.container.app-main</code>.", "<b>List</b>: header, toolbar, entity list, pagination.", "<b>Detail</b>: breadcrumb, header with mark, <code>.detail</code> 2:1 grid.", "<b>Form</b>: 44rem card.", "<b>Auth</b>: centred 26rem card, no top bar.", "<b>Hero</b>: Field page with the WebGPU field."])),
        sec("usage", "Usage", ul(["Use .container for every page.", "Never scroll the page sideways; tables and maps contain their own overflow."])),
        sec("tokens", "Tokens", tok_rows(pick("--layout-"))),
    ])


def elevation():
    shadows = '<div class="ds-shadow-grid">' + "".join(f'<div style="--shadow: var({t});">{t}</div>' for t in ["--shadow-1", "--shadow-2", "--shadow-3", "--shadow-4"]) + "</div>"
    page("foundations/elevation.html", "Elevation", "Foundation", "Four shadows and a z-order scale. Cards barely float; dialogs clearly do.", [
        sec("overview", "Overview", "<p>Flat by default. Hover lifts cards from level 1 to 2. Menus 3, dialogs 4.</p>" + shadows),
        sec("surfaces", "Surfaces", table(["Surface", "Token", "Use"], [["Canvas", "--color-bg-canvas", "Page"], ["Surface", "--color-bg-surface", "Cards, inputs"], ["Raised", "--color-bg-surface-raised", "Dialogs, menus"], ["Sunken", "--color-bg-surface-sunken", "Table headers, read-only, kbd"], ["Inverse", "--color-bg-inverse", "Toasts, tooltips, selection bar"]])),
        sec("z", "Z-order", table(["Layer", "Token"], [[t.removeprefix("--z-"), f"<code>{t}</code>"] for t in pick("--z-")])),
        sec("usage", "Usage", ul(["Dark theme: raised surfaces get lighter; shadows get darker and larger.", "Never set a raw z-index."])),
        sec("tokens", "Tokens", tok_rows(pick("--shadow-1", "--shadow-2", "--shadow-3", "--shadow-4", "--shadow-focus", "--z-"))),
    ])


def shape():
    page("foundations/shape.html", "Shape", "Foundation", "Soft, generous corners: 12px controls, 20px cards, 28px sheets.", [
        sec("overview", "Overview", '<div class="ds-scale" style="flex-direction:row;flex-wrap:wrap;gap:var(--space-6);">' + "".join(f'<div><div class="ds-scale__box" style="--size: var({t});"></div><code>{t}</code></div>' for t in pick("--radius-")) + "</div>"),
        sec("usage", "Usage", table(["Element", "Radius"], [["Checkbox", "xs"], ["Badge, tag, tooltip", "sm"], ["Button, input, menu", "md"], ["Card, dialog, table wrap", "lg"], ["Sheet, map", "xl"], ["Avatar, chip, pill", "full"]])),
        sec("tokens", "Tokens", tok_rows(pick("--radius-", "--border-width-"))),
    ])


def motion():
    demos = "".join(f'<div class="ds-motion-demo" style="--demo-duration: var({d}); --demo-ease: var(--ease-standard);"><button class="btn" type="button" data-motion-run>Replay {d}</button><span class="dot" aria-hidden="true"></span></div>' for d in ["--duration-fast", "--duration-base", "--duration-slow", "--duration-deliberate"])
    eases = "".join(f'<div class="ds-motion-demo" style="--demo-duration: var(--duration-deliberate); --demo-ease: var({e});"><button class="btn" type="button" data-motion-run>Replay {e}</button><span class="dot" aria-hidden="true"></span></div>' for e in ["--ease-standard", "--ease-enter", "--ease-exit", "--ease-spring", "--ease-spring-linear"])
    page("foundations/motion.html", "Motion", "Foundation", "Micro-animations that explain: rise, lift, press, fill, pulse. Chrome-native: @starting-style, scroll-driven, view transitions, linear() springs.", [
        sec("overview", "Overview", ul(["<b>Rise</b>: lists enter 40ms apart with <code>@starting-style</code>.", "<b>Reveal</b>: lower sections fade up with <code>animation-timeline: view()</code>.", "<b>Lift</b>: cards rise 2px on hover with a <code>linear()</code> spring.", "<b>Press</b>: buttons and chips scale down.", "<b>Fill</b>: score rings animate a registered <code>@property</code>.", "<b>Morph</b>: page titles carry <code>view-transition-name</code> across pages.", "<b>Ambient</b>: the WebGPU field drifts."])),
        sec("durations", "Durations", demos),
        sec("easing", "Easing", eases),
        sec("usage", "Choreography", ul(["Hover 120ms, reveal 200ms, dialogs 320ms, score fill 500ms.", "Loops (spinner, pulse, ripple) have their own tokens.", "No animation over 500ms except loops and the ambient field."])),
        sec("accessibility", "Reduced motion", "<p>Under <code>prefers-reduced-motion</code> every duration token becomes 0.01ms, <code>--stagger</code> becomes 0, scroll reveals and pin ripples are removed and the WebGPU field draws one still frame.</p>"),
        sec("tokens", "Tokens", tok_rows(pick("--duration-", "--ease-", "--stagger"))),
    ])


def iconography():
    sheet = "".join(f'<div class="ds-swatch" style="display:grid;place-items:center;padding:var(--space-4);gap:var(--space-2);">{icon(n, "icon icon--lg")}<code>{n}</code></div>' for n in sorted(ICONS))
    page("foundations/iconography.html", "Iconography", "Foundation", "Inline SVG on a 24-unit grid, 2px round strokes, currentColor. The wheat mark is the brand.", [
        sec("overview", "Overview", "<p>Icons support labels; they rarely replace them. Every icon is <code>aria-hidden</code>; icon-only controls carry <code>aria-label</code>.</p>"),
        sec("set", "Icon set", f'<div class="ds-swatches">{sheet}</div>'),
        sec("sizes", "Sizes", example(f'{icon("wheat", "icon icon--sm")}{icon("wheat")}{icon("wheat", "icon icon--lg")}', "16 / 20 / 24px.")),
        sec("usage", "Usage", ul(["One meaning per icon across the product.", "Sparkle = research; flask = runs; wheat = brand."])),
        sec("tokens", "Tokens", tok_rows(pick("--size-"))),
    ])


def theming():
    page("foundations/theming.html", "Theming", "Foundation", "Light and dark from one token file; OS preference by default, forced with data-theme.", [
        sec("overview", "Overview", ul(["Light on <code>:root</code>; dark on <code>[data-theme=\"dark\"]</code> and under <code>prefers-color-scheme: dark</code> unless forced light.", "<code>color-scheme</code> set per theme so native controls follow.", "<code>prefers-contrast: more</code> strengthens borders and muted text; <code>forced-colors</code> hands rings to system colours."])),
        sec("tiers", "Token tiers", table(["Tier", "Example", "Who reads it"], [["Primitive", "<code>--palette-ember-700</code>", "Semantic tokens only"], ["Semantic", "<code>--color-accent</code>", "Components and pages"], ["Component", "<code>--btn-bg</code>", "One component"]])),
        sec("adding", "Adding a theme", "<p>Copy the dark block, rename it, change semantic tokens only, add pairs to <code>contrast-pairs.json</code>, run the checker.</p>"),
        sec("json", "tokens.json", "<p><code>tokens/tokens.json</code> is the DTCG export (aliases as <code>{group.token}</code>, dark under <code>$extensions</code>). Regenerate with <code>tokens_to_json.py</code>.</p>"),
        sec("usage", "Do and don't", ul(["Do override semantic tokens in a theme.", "Don't write colours in components.", "Don't invert light to get dark: build dark from roles."])),
        sec("tokens", "Tokens", tok_rows(pick("--target-", "--focus-ring-", "--control-height-"))),
    ])


def responsive():
    page("foundations/responsive.html", "Responsive", "Foundation", "Mobile-first; tested at 360, 768 and 1280px with no horizontal page scroll.", [
        sec("overview", "Overview", ul(["Base styles are for 360px.", "48rem adds inline nav and wider gutters; 64rem adds the full brand, 2:1 detail grids and 64px margins.", "Phones: dialogs become bottom sheets, entity cards wrap, map popovers dock below."])),
        sec("components", "Per component", table(["Component", "< 768px", "≥ 1024px"], [["Top bar", "Menu button + drawer", "Full nav + brand"], ["Entity card", "Wraps; status under name", "Grid row"], ["Dialog", "Bottom sheet", "Centred"], ["Detail", "Aside below", "2:1 with aside"], ["Toasts", "Full width", "24rem bottom-right"], ["Map popover", "Docked below map", "Anchored to pin"]])),
        sec("touch", "Touch", ul(["Targets ≥ 24px; primary mobile actions ≥ 44px.", "Hover-only affordances (row checks, lifts) are always visible or unnecessary on touch."])),
        sec("testing", "Testing matrix", "<p>Every mock is screenshotted at 360×800, 768×1024 and 1280×800 in light and dark (<code>screenshot_mocks.py</code>).</p>"),
    ])


def accessibility():
    page("foundations/accessibility.html", "Accessibility", "Foundation", "WCAG 2.2 AA by construction: contrast in tokens, one focus ring, native elements first.", [
        sec("overview", "Commitments", '<ul class="ds-checklist">' + "".join(f"<li>{x}</li>" for x in ["Text ≥ 4.5:1, UI edges and focus ≥ 3:1 in both themes (checked).", "One 2px focus ring with offset; never removed.", "Skip link and landmarks on every page.", "Targets ≥ 24px.", "Every form error says how to fix it; summary links to fields; focus moves to the summary.", "Status is never colour alone.", "Toasts live in status regions; errors persist.", "Dialogs trap focus, close on Escape, return focus; page behind is inert.", "All motion respects reduced motion.", "Native elements first; ARIA follows APG patterns named on each component page."]) + "</ul>"),
        sec("testing", "Testing", ul(["Run check_contrast.py and check_design_system.py.", "Tab through one page, one dialog and one toast.", "Check 200% zoom and 320px reflow.", "Test with NVDA + Chrome."])),
        sec("contract", "Component contract", "<p>Every component page answers: role and pattern, keyboard, focus, labelling, contrast pairs, motion, touch.</p>"),
    ])


def content():
    page("foundations/content.html", "Content", "Foundation", "Minimal text. Nouns for labels, verbs for buttons, numbers carry the story.", [
        sec("overview", "Voice", ul(["Calm, specific, brief.", "Sentence case everywhere except product and organisation names.", "Gentle brand moments in titles only: <i>The field is ripe.</i>, <i>Nothing grows here</i>."])),
        sec("numbers", "Numbers and dates", ul(["1,284 with separators; units after (<i>140,000 leaders</i>).", "Relative in lists (<i>Yesterday</i>), absolute on details (<i>Tue 14 Oct</i>).", "Subtitles: counts joined by middots: <i>14 tracked · 9 verified · 5 unverified</i>."])),
        sec("errors", "Error formula", "<p>What happened + what to do + action. <i>Couldn't load organisations. Try again, or share reference HM-4F2A.</i></p>"),
        sec("empty", "Empty formula", "<p>Title (state) + one sentence (why/what) + one action. <i>No organisations yet · Add one or let research find them · Ask the web</i></p>"),
        sec("library", "Microcopy library", table(["Use", "Text"], [["Primary research action", "Ask the web"], ["Create", "New"], ["Save", "Save"], ["Confirm delete", "Delete organisation"], ["Undo", "Undo"], ["Retry", "Try again / Retry"], ["Filters cleared", "Clear filters"], ["Verification", "Verified · Unverified · Conflict · Not found"], ["Saved", "Saved · just now"]])),
    ])


def build():
    for fn in (color, typography, spacing, layout, elevation, shape, motion, iconography, theming, responsive, accessibility, content):
        fn()
