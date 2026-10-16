"""Shared page shell and helpers for the Harvest Map design-system docs."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = "Harvest Map"
DATE = "16 Oct 2026"

FOUNDATIONS = [
    ("color", "Color"), ("typography", "Typography"), ("spacing", "Spacing"), ("layout", "Layout"), ("elevation", "Elevation"),
    ("shape", "Shape"), ("motion", "Motion"), ("iconography", "Iconography"), ("theming", "Theming"), ("responsive", "Responsive"),
    ("accessibility", "Accessibility"), ("content", "Content"),
]
PATTERNS = [
    ("forms", "Forms"), ("feedback-and-loading", "Feedback & loading"), ("empty-and-error-states", "Empty & error states"),
    ("navigation", "Navigation & page structure"), ("dialogs-and-overlays", "Dialogs & overlays"), ("data-lists", "Data tables & lists"),
    ("notifications", "Notifications"), ("content-and-tone", "Content & tone"), ("research-review", "Research & review"),
]
COMPONENTS: list[tuple[str, str, str]] = []  # (id, name, group) filled by components.py

ICONS = {
    "plus": '<path d="M12 5v14M5 12h14"/>', "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>', "check": '<path d="m5 12 4 4L19 6"/>', "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "edit": '<path d="M4 20h4l10-10-4-4L4 16zM13 7l4 4"/>', "trash": '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.5 6.5l2.5 2.5M15 15l2.5 2.5M6.5 17.5 9 15M15 9l2.5-2.5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>', "warning": '<path d="M12 3 2 20h20zM12 9v5M12 17h.01"/>',
    "danger": '<circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16h.01"/>', "success": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0"/>', "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "wheat": '<path d="M12 22V10M12 10c-3 0-5-2-5-5 3 0 5 2 5 5zM12 10c3 0 5-2 5-5-3 0-5 2-5 5zM12 15c-3 0-5-2-5-5 3 0 5 2 5 5zM12 15c3 0 5-2 5-5-3 0-5 2-5 5zM12 20c-3 0-5-2-5-5 3 0 5 2 5 5zM12 20c3 0 5-2 5-5-3 0-5 2-5 5z"/>',
    "building": '<path d="M4 21V5a1 1 0 0 1 1-1h9v17M14 9h5a1 1 0 0 1 1 1v11M8 8h2M8 12h2M8 16h2M17 13h1M17 17h1"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 19a1 1 0 0 0 .9 1.5h13.2a1 1 0 0 0 .9-1.5L14 9V3"/>', "home": '<path d="M3 12 12 3l9 9M5 10v10h14V10"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 13v6H5V6h6"/>', "refresh": '<path d="M20 12a8 8 0 0 1-14 5.3L4 15M4 12a8 8 0 0 1 14-5.3L20 9M4 4v5h5M20 20v-5h-5"/>',
    "upload": '<path d="M12 16V4m0 0-4 4m4-4 4 4M4 20h16"/>', "download": '<path d="M12 4v12m0 0-4-4m4 4 4-4M4 20h16"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>', "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "map-pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    "linkedin": '<path d="M4 4h16v16H4zM8 10v6M8 7v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10v6"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "wifi-off": '<path d="M2 8a16 16 0 0 1 20 0M5 12a12 12 0 0 1 14 0M8.5 15.5a7 7 0 0 1 7 0M12 19h.01M3 3l18 18"/>',
    "chrome": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M12 8.5h8.2M9 13.8 4.9 6.7M15 13.8l-4.1 7.1"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19 12a7 7 0 0 0-.1-1l2-1.5-2-3.4-2.3.9a7 7 0 0 0-1.7-1L14.5 3h-5l-.4 2.4a7 7 0 0 0-1.7 1L5.1 5.5l-2 3.4 2 1.5a7 7 0 0 0 0 2l-2 1.5 2 3.4 2.3-.9a7 7 0 0 0 1.7 1l.4 2.4h5l.4-2.4a7 7 0 0 0 1.7-1l2.3.9 2-3.4-2-1.5c.1-.3.1-.7.1-1z"/>',
    "keyboard": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h.01M11 10h.01M15 10h.01M7 14h10"/>',
    "logout": '<path d="M10 17l5-5-5-5M15 12H3M13 3h6v18h-6"/>', "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "back": '<path d="M19 12H5m6 6-6-6 6-6"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    return f'<svg class="{cls}" aria-hidden="true" viewBox="0 0 24 24">{ICONS[name]}</svg>'


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def nav(prefix: str) -> str:
    def items(folder, entries):
        return "".join(f'<li><a href="{prefix}{folder}/{pid}.html">{label}</a></li>' for pid, label in entries)
    comps = [(cid, name) for cid, name, _ in COMPONENTS]
    return (f'<nav class="ds-nav" aria-label="Design system"><div class="ds-nav__brand"><a href="{prefix}index.html">{PRODUCT} DS</a>'
            f'<button class="ds-theme-toggle" type="button" aria-pressed="false">☾ Dark</button></div>'
            f'<details open><summary>Foundations</summary><ul>{items("foundations", FOUNDATIONS)}</ul></details>'
            f'<details open><summary>Components</summary><ul>{items("components", comps)}</ul></details>'
            f'<details open><summary>Patterns</summary><ul>{items("patterns", PATTERNS)}</ul></details></nav>')


def page(path: str, title: str, kicker: str, lead: str, sections: list[tuple[str, str, str, str | None]], meta: str = "", head: str = "") -> None:
    """sections: (id, heading, body_html, na_reason)."""
    depth = path.count("/")
    prefix = "../" * depth
    toc = "".join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _, _ in sections)
    body = ""
    for sid, heading, content, na in sections:
        if na:
            body += f'<section class="ds-section" id="{sid}" data-na="{esc(na)}"><h2><a href="#{sid}">{heading}</a></h2><p class="ds-na">{esc(na)}</p></section>\n'
        else:
            body += f'<section class="ds-section" id="{sid}"><h2><a href="#{sid}">{heading}</a></h2>{content}</section>\n'
    pills = meta or '<span class="ds-pill ds-pill--ok">WCAG 2.2 AA</span><span class="ds-pill">Status: stable</span><span class="ds-pill">Since v1.0</span>'
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {PRODUCT} design system</title>
<meta name="description" content="{esc(lead)}">
<link rel="stylesheet" href="{prefix}tokens/tokens.css">
<link rel="stylesheet" href="{prefix}assets/components.css">
<link rel="stylesheet" href="{prefix}assets/ds.css">{head}
</head>
<body id="top">
<a class="skip-link" href="#main">Skip to content</a>
<div class="ds-shell">
{nav(prefix)}
<main id="main" class="ds-main">
<header class="ds-header"><p class="ds-kicker">{kicker}</p><h1>{title}</h1><p class="ds-lead">{lead}</p><div class="ds-meta">{pills}</div><ul class="ds-toc">{toc}</ul></header>
{body}<footer class="ds-footer"><span>{PRODUCT} design system · extracted from <a href="{prefix}../mocks/index.html">docs/mocks</a> on {DATE}</span><a href="#top">Back to top</a></footer>
</main>
</div>
<script src="{prefix}assets/ds.js"></script>
</body>
</html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8", newline="\n")


# ---------- Small builders ---------------------------------------------------
def example(canvas: str, caption: str = "", code: str | None = None, cls: str = "") -> str:
    cap = f'<div class="ds-example__caption"><span>{caption}</span></div>' if caption else ""
    src = code if code is not None else canvas
    snippet = f'<details class="ds-example__code"><summary>HTML</summary><pre><code>{html.escape(src.strip())}</code></pre></details>'
    return f'<div class="ds-example"><div class="ds-example__canvas {cls}">{canvas}</div>{cap}{snippet}</div>'


def themes(canvas: str) -> str:
    return (f'<h3>Both themes</h3><div class="ds-themes"><div data-theme="light"><div class="ds-example__canvas">{canvas}</div></div>'
            f'<div data-theme="dark"><div class="ds-example__canvas">{canvas}</div></div></div>')


def matrix(cols: list[str], rows: list[tuple[str, list[str]]]) -> str:
    head = '<th scope="col">Variant</th>' + "".join(f'<th scope="col">{c}</th>' for c in cols)
    body = "".join(f'<tr><th scope="row">{label}</th>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for label, cells in rows)
    return f'<div class="ds-matrix"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


STATE_ATTR = {"Default": "", "Hover": 'data-state="hover"', "Focus": 'data-state="focus"', "Active": 'data-state="active"', "Disabled": "disabled", "Loading": 'aria-busy="true"'}


def state_row(label: str, template: str, cols: list[str], extra: dict[str, str] | None = None) -> tuple[str, list[str]]:
    """template contains {s} where state attributes go."""
    attrs = dict(STATE_ATTR, **(extra or {}))
    return label, [template.replace("{s}", attrs.get(c, "")) for c in cols]


def token_table(rows: list[tuple[str, str]]) -> str:
    def cell(token, theme):
        if any(k in token for k in ("color", "shadow-color")):
            return f'<span class="ds-swatch-cell" data-theme="{theme}"><i data-token="{token}" data-swatch></i><span data-token="{token}"></span></span>'
        return f'<span data-theme="{theme}"><span data-token="{token}"></span></span>'
    body = "".join(f"<tr><td>{part}</td><td><code>{tok}</code></td><td>{cell(tok, 'light')}</td><td>{cell(tok, 'dark')}</td></tr>" for part, tok in rows)
    return f'<div class="ds-table-wrap"><table class="ds-table"><thead><tr><th scope="col">Part</th><th scope="col">Token</th><th scope="col">Light</th><th scope="col">Dark</th></tr></thead><tbody>{body}</tbody></table></div>'


def table(head: list[str], rows: list[list[str]], cls: str = "ds-table") -> str:
    h = "".join(f'<th scope="col">{c}</th>' for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="ds-table-wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def pair(label: str, fg: str, bg: str, minimum: float = 4.5) -> str:
    return f'<div class="ds-pair"><span>{label}</span><span class="ds-pair__ratio" data-contrast="{fg}|{bg}" data-min="{minimum}"></span></div>'


def dodont(pairs: list[tuple[str, str, str, str]]) -> str:
    out = ""
    for do_html, do_cap, dont_html, dont_cap in pairs:
        out += (f'<div class="ds-dodont"><figure class="ds-do"><div class="ds-example__canvas">{do_html}</div><figcaption>{do_cap}</figcaption></figure>'
                f'<figure class="ds-dont"><div class="ds-example__canvas">{dont_html}</div><figcaption>{dont_cap}</figcaption></figure></div>')
    return out


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def mock_links(prefix: str, paths: list[str]) -> str:
    return "<ul>" + "".join(f'<li><a href="{prefix}../mocks/{p}.html">{p}</a></li>' for p in paths) + "</ul>"
