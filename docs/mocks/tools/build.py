#!/usr/bin/env python3
"""Build every Harvest Map mock from the manifest and the renderers.

    python docs/mocks/tools/build.py          # writes manifest.json and all pages/dialogs/notifications
    python docs/mocks/tools/build.py --list   # prints the file count per kind

The shell (topbar, navigation, mock bar) lives here so every mock shares it;
page, dialog and notification bodies live in pages.py, dialogs.py and
notifications.py. After building, run the skill checker:

    python .claude/skills/writing-html-mocks/scripts/check_mocks.py docs/mocks --write
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "Harvest Map"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import ME  # noqa: E402

# ---------------------------------------------------------------------------
# Manifest: every screen and every state. Not-applicable states carry a reason.
# ---------------------------------------------------------------------------
PAGE_STATES_LIST = ["default", "loading", "empty", "error", "no-results", "long"]
PAGE_STATES_FORM = ["default", "loading", "error", "invalid", "submitting", "success"]

SCREENS = [
    # Entry
    dict(id="sign-in", kind="page", title="Sign in", route="/sign-in", states=["default", "invalid", "submitting", "error", "success"],
         not_applicable={"loading": "The form renders with no request in flight; nothing to skeleton.", "empty": "No collection on this page."}),
    dict(id="forgot-password", kind="page", title="Forgot password", route="/forgot-password", states=["default", "invalid", "submitting", "error", "success"],
         not_applicable={"loading": "The form renders with no request in flight.", "empty": "No collection on this page."}),
    dict(id="reset-password", kind="page", title="Reset password", route="/reset-password", states=["default", "loading", "invalid", "submitting", "error", "success"],
         not_applicable={"empty": "No collection on this page."}),
    # Shell
    dict(id="field", kind="page", title="Field", route="/", states=["default", "loading", "empty", "error", "partial"]),
    dict(id="organizations", kind="page", title="Organizations", route="/organizations", states=PAGE_STATES_LIST + ["selected", "edge"]),
    dict(id="organization", kind="page", title="Organization", route="/organizations/:id", states=["default", "loading", "empty", "error", "read-only", "edge"]),
    dict(id="organization-edit", kind="page", title="Edit organization", route="/organizations/:id/edit", states=PAGE_STATES_FORM,
         not_applicable={"empty": "A form always has fields; creating a new organization is the default state with blank values, shown in organization-edit/default via the New organization note."}),
    dict(id="people", kind="page", title="People", route="/people", states=PAGE_STATES_LIST),
    dict(id="person", kind="page", title="Person", route="/people/:id", states=["default", "loading", "empty", "error", "edge"]),
    dict(id="person-edit", kind="page", title="Edit person", route="/people/:id/edit", states=PAGE_STATES_FORM,
         not_applicable={"empty": "A form always has fields."}),
    dict(id="problems", kind="page", title="Problems", route="/problems", states=["default", "loading", "empty", "error", "no-results"]),
    dict(id="problem", kind="page", title="Problem", route="/problems/:id", states=["default", "loading", "empty", "error"]),
    dict(id="problem-edit", kind="page", title="Edit problem", route="/problems/:id/edit", states=PAGE_STATES_FORM,
         not_applicable={"empty": "A form always has fields."}),
    dict(id="questions", kind="page", title="Questions", route="/questions", states=["default", "loading", "empty", "error", "partial"]),
    dict(id="research", kind="page", title="Research", route="/research", states=["default", "loading", "empty", "error", "running", "review"]),
    dict(id="map", kind="page", title="Map", route="/map", states=["default", "loading", "empty", "error", "no-results"]),
    dict(id="search", kind="page", title="Search", route="/search", states=["default", "loading", "empty", "error", "no-results"]),
    dict(id="notifications", kind="page", title="Notifications", route="/notifications", states=["default", "loading", "empty", "error", "read"]),
    dict(id="settings", kind="page", title="Settings", route="/settings", states=PAGE_STATES_FORM,
         not_applicable={"empty": "Settings always has values."}),
    # Errors as pages
    dict(id="not-found", kind="page", title="Not found", route="/404", states=["default"],
         not_applicable={"loading": "Static page.", "empty": "Static page.", "error": "This page is the error."}),
    dict(id="forbidden", kind="page", title="Forbidden", route="/403", states=["default"],
         not_applicable={"loading": "Static page.", "empty": "Static page.", "error": "This page is the error."}),
    dict(id="server-error", kind="page", title="Something went wrong", route="/500", states=["default"],
         not_applicable={"loading": "Static page.", "empty": "Static page.", "error": "This page is the error."}),
    dict(id="offline", kind="page", title="Offline", route="/offline", states=["default"],
         not_applicable={"loading": "Static page.", "empty": "Static page.", "error": "This page is the error."}),
    dict(id="unsupported-browser", kind="page", title="Unsupported browser", route="/unsupported", states=["default"],
         not_applicable={"loading": "Static page.", "empty": "Static page.", "error": "This page is the error."}),
    # Dialogs
    dict(id="nav-sheet", kind="dialog", title="Navigation", opens_from="field", states=["default"],
         not_applicable={"busy": "Navigation only; nothing is submitted.", "invalid": "No inputs."}),
    dict(id="command-palette", kind="dialog", title="Command palette", opens_from="field", states=["default", "busy", "no-results"],
         not_applicable={"invalid": "Free-text search cannot be invalid."}),
    dict(id="delete-organization", kind="dialog", title="Delete organization", opens_from="organization", states=["default", "invalid", "busy", "failed"]),
    dict(id="delete-person", kind="dialog", title="Delete person", opens_from="person", states=["default", "busy", "failed"],
         not_applicable={"invalid": "No inputs; a single danger button."}),
    dict(id="delete-problem", kind="dialog", title="Delete problem", opens_from="problem", states=["default", "busy", "failed"],
         not_applicable={"invalid": "No inputs; a single danger button."}),
    dict(id="add-person", kind="dialog", title="Add person", opens_from="organization", states=["default", "invalid", "busy", "failed", "success"]),
    dict(id="link-problem", kind="dialog", title="Link problem", opens_from="organization", states=["default", "invalid", "busy", "failed"]),
    dict(id="run-research", kind="dialog", title="Run research", opens_from="research", states=["default", "invalid", "busy", "failed"]),
    dict(id="review-finding", kind="dialog", title="Review finding", opens_from="research", states=["default", "invalid", "busy", "failed", "scroll"]),
    dict(id="import-csv", kind="dialog", title="Import CSV", opens_from="organizations", states=["default", "invalid", "busy", "failed", "success"]),
    dict(id="export", kind="dialog", title="Export", opens_from="organizations", states=["default", "busy", "failed"],
         not_applicable={"invalid": "Radio choices only; always valid."}),
    dict(id="sign-out", kind="dialog", title="Sign out", opens_from="settings", states=["default", "busy", "failed"],
         not_applicable={"invalid": "No inputs."}),
    dict(id="unsaved-changes", kind="dialog", title="Unsaved changes", opens_from="organization-edit", states=["default"],
         not_applicable={"busy": "Discard is local and instant.", "invalid": "No inputs."}),
    dict(id="keyboard-shortcuts", kind="dialog", title="Keyboard shortcuts", opens_from="field", states=["default"],
         not_applicable={"busy": "Read-only reference.", "invalid": "No inputs."}),
    # Notifications
    dict(id="toast", kind="notification", title="Toast", opens_from="organizations", states=["info", "success", "warning", "danger", "with-action", "stacked"]),
    dict(id="research-banner", kind="notification", title="Research banner", opens_from="research", states=["info", "success", "warning", "danger", "persistent"]),
    dict(id="offline-banner", kind="notification", title="Offline banner", opens_from="organizations", states=["info", "success", "warning", "danger", "persistent"]),
    dict(id="inline-alert", kind="notification", title="Inline alert", opens_from="organization", states=["info", "success", "warning", "danger", "with-action"]),
]

MANIFEST = {
    "project": PROJECT,
    "required_states": {
        "page": ["default", "loading", "empty", "error"],
        "dialog": ["default", "busy", "invalid"],
        "notification": ["info", "success", "warning", "danger"],
    },
    "screens": SCREENS,
}

KIND_FOLDER = {"page": "pages", "dialog": "dialogs", "notification": "notifications"}
SCREEN_BY_ID = {s["id"]: s for s in SCREENS}

# ---------------------------------------------------------------------------
# Icons: inline SVG, currentColor, 24 viewBox, 2px stroke.
# ---------------------------------------------------------------------------
ICONS = {
    "wheat": '<path d="M12 22V10M12 10c-3 0-5-2-5-5 3 0 5 2 5 5zM12 10c3 0 5-2 5-5-3 0-5 2-5 5zM12 15c-3 0-5-2-5-5 3 0 5 2 5 5zM12 15c3 0 5-2 5-5-3 0-5 2-5 5zM12 20c-3 0-5-2-5-5 3 0 5 2 5 5zM12 20c3 0 5-2 5-5-3 0-5 2-5 5z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 20a2 2 0 0 0 4 0"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "back": '<path d="M19 12H5m6 6-6-6 6-6"/>',
    "edit": '<path d="M4 20h4l10-10-4-4L4 16zM13 7l4 4"/>',
    "trash": '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 13v6H5V6h6"/>',
    "refresh": '<path d="M20 12a8 8 0 0 1-14 5.3L4 15M4 12a8 8 0 0 1 14-5.3L20 9M4 4v5h5M20 20v-5h-5"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.5 6.5l2.5 2.5M15 15l2.5 2.5M6.5 17.5 9 15M15 9l2.5-2.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "building": '<path d="M4 21V5a1 1 0 0 1 1-1h9v17M14 9h5a1 1 0 0 1 1 1v11M8 8h2M8 12h2M8 16h2M17 13h1M17 17h1"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 19a1 1 0 0 0 .9 1.5h13.2a1 1 0 0 0 .9-1.5L14 9V3"/>',
    "home": '<path d="M3 12 12 3l9 9M5 10v10h14V10"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/>',
    "warning": '<path d="M12 3 2 20h20zM12 9v5M12 17h.01"/>',
    "danger": '<circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16h.01"/>',
    "success": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "wifi-off": '<path d="M2 8a16 16 0 0 1 20 0M5 12a12 12 0 0 1 14 0M8.5 15.5a7 7 0 0 1 7 0M12 19h.01M3 3l18 18"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "chrome": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M12 8.5h8.2M9 13.8 4.9 6.7M15 13.8l-4.1 7.1"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19 12a7 7 0 0 0-.1-1l2-1.5-2-3.4-2.3.9a7 7 0 0 0-1.7-1L14.5 3h-5l-.4 2.4a7 7 0 0 0-1.7 1L5.1 5.5l-2 3.4 2 1.5a7 7 0 0 0 0 2l-2 1.5 2 3.4 2.3-.9a7 7 0 0 0 1.7 1l.4 2.4h5l.4-2.4a7 7 0 0 0 1.7-1l2.3.9 2-3.4-2-1.5c.1-.3.1-.7.1-1z"/>',
    "upload": '<path d="M12 16V4m0 0-4 4m4-4 4 4M4 20h16"/>',
    "download": '<path d="M12 4v12m0 0-4-4m4 4 4-4M4 20h16"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "map-pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    "linkedin": '<path d="M4 4h16v16H4zM8 10v6M8 7v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10v6"/>',
    "keyboard": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h.01M11 10h.01M15 10h.01M7 14h10"/>',
    "logout": '<path d="M10 17l5-5-5-5M15 12H3M13 3h6v18h-6"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
}


def icon(name: str, cls: str = "icon") -> str:
    return f'<svg class="{cls}" aria-hidden="true" viewBox="0 0 24 24">{ICONS[name]}</svg>'


# ---------------------------------------------------------------------------
# Context: path helpers for the file being written.
# ---------------------------------------------------------------------------
NAV = [
    ("field", "Field", "home"),
    ("organizations", "Orgs", "building"),
    ("people", "People", "people"),
    ("problems", "Problems", "target"),
    ("questions", "Questions", "question"),
    ("research", "Research", "flask"),
    ("map", "Map", "globe"),
]


class Ctx:
    def __init__(self, kind: str, sid: str, state: str):
        self.kind, self.sid, self.state = kind, sid, state
        self.pages = ".." if kind == "page" else "../../pages"
        self.dialogs = "../../dialogs" if kind == "page" else ("../../dialogs" if kind == "notification" else "..")
        self.notifs = "../../notifications" if kind != "notification" else ".."
        self.assets = "../../assets"

    def p(self, pid: str, state: str = "default") -> str:
        return f"{self.pages}/{pid}/{state}.html"

    def d(self, did: str, state: str = "default") -> str:
        return f"{self.dialogs}/{did}/{state}.html"

    def n(self, nid: str, state: str = "info") -> str:
        return f"{self.notifs}/{nid}/{state}.html"


# ---------------------------------------------------------------------------
# Shell fragments
# ---------------------------------------------------------------------------
def topbar(ctx: Ctx, current: str | None, unread: int = 2) -> str:
    links = "".join(
        f'<a class="nav-link" href="{ctx.p(pid)}"{" aria-current=\"page\"" if pid == current else ""}>{label}</a>'
        for pid, label, _ in NAV
    )
    bell_label = f"Notifications, {unread} unread" if unread else "Notifications"
    badge = f'<span class="badge badge--count" aria-hidden="true" style="position:absolute; top: 2px; right: 2px;">{unread}</span>' if unread else ""
    return f'''<header class="topbar">
  <span class="topbar__shadow" aria-hidden="true"></span>
  <a class="btn btn--ghost btn--icon topbar__menu" href="{ctx.d("nav-sheet")}" aria-label="Open navigation">{icon("menu")}</a>
  <a class="topbar__brand" href="{ctx.p("field")}">{icon("wheat", "icon icon--lg")}<span>Harvest Map</span></a>
  <nav class="topbar__nav" aria-label="Primary">{links}</nav>
  <span class="topbar__spacer"></span>
  <a class="btn btn--ghost" href="{ctx.d("command-palette")}" aria-label="Search, Control K">{icon("search")}<span class="topbar__kbd kbd">⌘K</span></a>
  <a class="btn btn--ghost btn--icon has-tooltip" href="{ctx.p("notifications")}" aria-label="{bell_label}" style="position: relative;">{icon("bell")}{badge}<span class="tooltip" role="tooltip">{bell_label}</span></a>
  <a class="avatar avatar--sm" href="{ctx.p("settings")}" aria-label="Account settings for {ME["name"]}" style="text-decoration: none;">{ME["initials"]}</a>
</header>'''


def mock_bar(ctx: Ctx, screen: dict) -> str:
    items = "".join(
        f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == ctx.state else ""}>{s}</a></li>' for s in screen["states"]
    )
    return f'''<nav class="mock-bar" aria-label="Mock navigation">
  <a class="mock-bar__home" href="../../index.html" aria-label="All mocks">⌂</a>
  <span class="mock-bar__screen">{screen["title"]}</span>
  <ul class="mock-bar__states">{items}</ul>
  <button type="button" data-theme-toggle aria-pressed="false">☾ Dark</button>
  <button type="button" data-chrome-toggle aria-label="Hide mock chrome">×</button>
</nav>'''


def note(text: str, style: str) -> str:
    return f'<p class="mock-note" style="{style}">{text}</p>'


def document(ctx: Ctx, screen: dict, description: str, body: str, notes: list[str], scripts: list[str], head: str = "") -> str:
    kind_label = {"page": "", "dialog": " dialog", "notification": " notification"}[ctx.kind]
    script_tags = "".join(f'<script src="{ctx.assets}/{s}"></script>' for s in scripts)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{screen["title"]} · {ctx.state} — {PROJECT} mocks</title>
<meta name="mock:kind" content="{ctx.kind}">
<meta name="mock:screen" content="{ctx.sid}">
<meta name="mock:state" content="{ctx.state}">
<meta name="description" content="{description}">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="{ctx.assets}/tokens.css">
<link rel="stylesheet" href="{ctx.assets}/ui.css">
<link rel="stylesheet" href="{ctx.assets}/harvest.css">
<link rel="stylesheet" href="{ctx.assets}/mock.css">{head}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{body}
{"".join(notes)}
{mock_bar(ctx, screen)}
<script src="{ctx.assets}/mock.js"></script>{script_tags}
</body>
</html>
'''


def write(ctx: Ctx, result: dict) -> Path:
    screen = SCREEN_BY_ID[ctx.sid]
    out = ROOT / KIND_FOLDER[ctx.kind] / ctx.sid / f"{ctx.state}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = document(ctx, screen, result["description"], result["body"], result.get("notes", []), result.get("scripts", []), result.get("head", ""))
    out.write_text(html, encoding="utf-8", newline="\n")
    return out


def main(argv: list[str]) -> int:
    import dialogs, notifications, pages  # noqa: E401

    renderers = {"page": pages.render, "dialog": dialogs.render, "notification": notifications.render}
    counts = {"page": 0, "dialog": 0, "notification": 0}
    (ROOT / "manifest.json").write_text(json.dumps(MANIFEST, indent=2) + "\n", encoding="utf-8", newline="\n")
    # Remove stale files so the checker's orphan rule stays meaningful.
    for folder in KIND_FOLDER.values():
        for file in (ROOT / folder).glob("*/*.html"):
            file.unlink()
    for screen in SCREENS:
        for state in screen["states"]:
            ctx = Ctx(screen["kind"], screen["id"], state)
            result = renderers[screen["kind"]](ctx)
            if result is None:
                raise SystemExit(f"no renderer for {screen['kind']} {screen['id']}/{state}")
            write(ctx, result)
            counts[screen["kind"]] += 1
    total = sum(counts.values())
    print(f"wrote {total} mocks: {counts['page']} page states, {counts['dialog']} dialog states, {counts['notification']} notification states across {len(SCREENS)} screens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
