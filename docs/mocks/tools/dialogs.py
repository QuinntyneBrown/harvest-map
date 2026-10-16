"""Dialog renderers: each dialog is shown over the page it opens from (inert)."""
from __future__ import annotations

from build import Ctx, icon, note
from data import FINDINGS, ME, ORG_BY_ID, PEOPLE, PERSON_BY_ID, PROBLEMS, QUESTIONS
from pages import alert, field, page_body, select, tags, text_input, textarea, form_summary, avatar, verify


def close_btn() -> str:
    return f'<button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{icon("close")}</button>'


def over(ctx: Ctx, page: str, page_state: str, overlay: str, description: str, notes: list[str] | None = None) -> dict:
    behind = page_body(ctx, page, page_state)
    scripts = ["field.js"] if page == "field" else []
    return dict(description=description, body=f'<div inert aria-hidden="true">{behind}</div><div class="backdrop"></div>{overlay}', notes=notes or [], scripts=scripts)


def panel(title: str, desc: str, body: str, footer: str, icon_kind: str | None = None, size: str = "", labelled: str = "dlg-title") -> str:
    ic = f'<div class="dialog__icon dialog__icon--{icon_kind}" aria-hidden="true">{icon("warning" if icon_kind == "danger" else "info")}</div>' if icon_kind else ""
    d = f'<p id="dlg-desc" class="text-muted" style="margin-top:var(--space-1);">{desc}</p>' if desc else ""
    body_html = f'<div class="dialog__body stack" style="gap:var(--space-5);">{body}</div>' if body else '<div class="dialog__body"></div>'
    return (f'<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="{labelled}"{" aria-describedby=\"dlg-desc\"" if desc else ""} data-dismiss-on-escape>'
            f'<div class="dialog__panel {size}"><div class="dialog__header">{ic}<div style="flex:1;"><h2 class="dialog__title" id="dlg-title">{title}</h2>{d}</div>{close_btn()}</div>'
            f'{body_html}<div class="dialog__footer">{footer}</div></div></div>')


def primary(label: str, busy: bool = False, danger: bool = False, disabled: bool = False, autofocus: bool = False) -> str:
    cls = "btn btn--danger" if danger else "btn btn--primary"
    return f'<button class="{cls}" type="button"{" aria-busy=\"true\"" if busy else ""}{" disabled" if disabled else ""}{" autofocus" if autofocus else ""}>{label}</button>'


def cancel(label: str = "Cancel", disabled: bool = False, autofocus: bool = False) -> str:
    return f'<button class="btn" type="button"{" disabled" if disabled else ""}{" autofocus" if autofocus else ""}>{label}</button>'


ESC_NOTE = "Escape and the close button both cancel; focus returns to the button that opened it. Under 640 px this is a bottom sheet."


# ---------------------------------------------------------------------------
def nav_sheet(ctx: Ctx):
    links = "".join(f'<a class="nav-link" href="{ctx.p(pid)}"{" aria-current=\"page\"" if pid == "field" else ""}>{icon(ic)}{label}</a>' for pid, label, ic in [("field", "Field", "home"), ("organizations", "Organizations", "building"), ("people", "People", "people"), ("problems", "Problems", "target"), ("questions", "Questions", "question"), ("research", "Research", "flask"), ("map", "Map", "globe")])
    drawer = (f'<div class="drawer drawer--left nav-sheet" role="dialog" aria-modal="true" aria-labelledby="dlg-title" data-dismiss-on-escape><div class="drawer__header"><h2 class="drawer__title" id="dlg-title">Harvest Map</h2>{close_btn()}</div>'
              f'<nav class="drawer__body stack" aria-label="Primary" style="gap:var(--space-1);">{links}<div class="sidebar__group">Account</div><a class="nav-link" href="{ctx.p("settings")}">{icon("settings")}Settings</a><a class="nav-link" href="{ctx.p("notifications")}">{icon("bell")}Notifications <span class="badge badge--count" aria-label="2 unread">2</span></a></nav>'
              f'<div class="drawer__footer" style="justify-content:flex-start;">{avatar(ME["initials"])}<span class="text-sm">{ME["name"]}</span></div></div>')
    return over(ctx, "field", "default", drawer, "Mobile navigation drawer opened from the menu button (under 768 px).", [note("Slides in from the left over 320 ms; the page behind is inert. On wider screens the top bar shows the same links inline.", "top: 1rem; right: 1rem;")])


def command_palette(ctx: Ctx):
    s = ctx.state
    q = {"default": "gl", "busy": "gelsing", "no-results": "zebra hackathon"}[s]
    if s == "default":
        g = ORG_BY_ID["gloo"]
        items = (f'<li class="palette__group">Organisations</li><li><a class="palette__item" href="{ctx.p("organization")}" aria-selected="true">{icon("building")}<span>Gloo</span><span class="text-caption">Boulder · AI</span></a></li>'
                 f'<li class="palette__group">People</li><li><a class="palette__item" href="{ctx.p("person")}">{icon("people")}<span>Scott Beck</span><span class="text-caption">Co-founder &amp; CEO · Gloo</span></a></li><li><a class="palette__item" href="{ctx.p("person")}">{icon("people")}<span>Pat Gelsinger</span><span class="text-caption">Executive Chair · Gloo</span></a></li>'
                 f'<li class="palette__group">Actions</li><li><a class="palette__item" href="{ctx.d("run-research")}">{icon("sparkle")}<span>Run research</span><span class="kbd">R</span></a></li><li><a class="palette__item" href="{ctx.p("organization-edit")}">{icon("plus")}<span>New organisation</span><span class="kbd">N</span></a></li>')
        tail = ""
    elif s == "busy":
        items = '<li class="palette__group">Searching</li>'
        tail = '<div style="padding:var(--space-6);display:flex;gap:var(--space-3);align-items:center;color:var(--color-fg-muted);" role="status"><span class="spinner" aria-hidden="true"></span>Searching organisations, people and findings</div>'
    else:
        items = ""
        tail = f'<div style="padding:var(--space-8) var(--space-6);text-align:center;color:var(--color-fg-muted);" role="status">No matches for “{q}”.<div style="margin-top:var(--space-4);"><a class="btn btn--sm btn--primary" href="{ctx.d("run-research")}">{icon("sparkle", "icon icon--sm")}Ask the web</a></div></div>'
    pal = (f'<div class="palette" role="dialog" aria-modal="true" aria-label="Search" data-dismiss-on-escape><div class="palette__panel"><div class="palette__input">{icon("search", "icon text-subtle")}<label class="visually-hidden" for="palette-q">Search</label><input id="palette-q" type="search" value="{q}" role="combobox" aria-expanded="true" aria-controls="palette-list" aria-autocomplete="list" autofocus>'
           f'<span class="kbd">Esc</span></div><ul class="palette__list" id="palette-list" role="listbox" aria-label="Results">{items}</ul>{tail}<div class="palette__foot"><span><span class="kbd">↑↓</span> move</span><span><span class="kbd">↵</span> open</span><span><span class="kbd">Esc</span> close</span></div></div></div>')
    desc = {"default": "Command palette (⌘K) with grouped results after typing “gl”.", "busy": "Command palette while a search is in flight.", "no-results": "Command palette with no matches and a way to turn the query into research."}[s]
    return over(ctx, "field", "default", pal, desc, [note("Opens with ⌘K or /. Results appear after 150 ms of idle typing; the spinner only shows past 300 ms.", "top: 1rem; right: 1rem;")] if s == "default" else [])


def delete_organization(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    failed = alert("danger", "Couldn't delete FaithTech", "It's referenced by run #48, which is still running. Stop the run and try again.", f'<a href="{ctx.p("research", "running")}">Open run #48</a>', role="alert", dismiss=False) if s == "failed" else ""
    body = failed + field("confirm-name", "Type FaithTech to confirm", text_input("confirm-name", "Faithtech" if invalid else ("FaithTech" if s in ("busy", "failed") else ""), invalid=invalid, readonly=busy, extra='autocomplete="off" autofocus'),
                          error="Names must match exactly, including capitals" if invalid else "")
    footer = cancel(disabled=busy) + primary("Delete organisation", busy=busy, danger=True, disabled=(s == "default"))
    dlg = panel("Delete FaithTech?", "Removes the organisation, 1 person link and 3 sources. This can't be undone.", body, footer, icon_kind="danger")
    desc = {"default": "Destructive confirmation with typed name; the danger button stays disabled until the name matches.", "invalid": "Typed name doesn't match exactly.", "busy": "Deleting; cancel disabled to avoid a double action.", "failed": "Delete blocked by a running research run."}[s]
    return over(ctx, "organization", "default", dlg, desc, [note("Focus starts in the text field, never on the danger button. " + ESC_NOTE, "top: 1rem; right: 1rem;")] if s == "default" else [])


def delete_person(ctx: Ctx):
    s = ctx.state
    busy = s == "busy"
    failed = alert("danger", "Couldn't delete", "The server didn't respond. Nothing was changed.", role="alert", dismiss=False) if s == "failed" else ""
    dlg = panel("Delete Pat Gelsinger?", "Removes the person and 3 sources. Gloo stays.", failed, cancel(disabled=busy, autofocus=True) + primary("Delete person", busy=busy, danger=True), icon_kind="danger")
    desc = {"default": "Confirm deleting a person; Cancel has focus.", "busy": "Deleting the person.", "failed": "Delete failed; nothing changed, retry available."}[s]
    return over(ctx, "person", "default", dlg, desc, [note(ESC_NOTE, "top: 1rem; right: 1rem;")] if s == "default" else [])


def delete_problem(ctx: Ctx):
    s = ctx.state
    busy = s == "busy"
    failed = alert("danger", "Couldn't delete", "The server didn't respond. Nothing was changed.", role="alert", dismiss=False) if s == "failed" else ""
    dlg = panel("Delete “Scripture in every language by 2033”?", "2 organisations stay; their link to this problem is removed.", failed, cancel(disabled=busy, autofocus=True) + primary("Delete problem", busy=busy, danger=True), icon_kind="danger")
    desc = {"default": "Confirm deleting a problem.", "busy": "Deleting the problem.", "failed": "Delete failed; retry available."}[s]
    return over(ctx, "problem", "default", dlg, desc)


def add_person(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    if s == "success":
        body = alert("success", "Elise Varga added", "Head of Community · FaithTech. Research will look for her LinkedIn profile.", dismiss=False)
        dlg = panel("Add person", "", body, f'<a class="btn" href="{ctx.p("organization")}">Done</a>' + primary("Add another", autofocus=True))
        return over(ctx, "organization", "default", dlg, "Person added; the dialog stays open to add another.")
    summary = form_summary([("ap-name", "Enter a name")]) if invalid else ""
    failed = alert("danger", "Couldn't add the person", "Your input is kept. Try again.", role="alert", dismiss=False) if s == "failed" else ""
    body = (summary + failed
            + field("ap-name", "Name", text_input("ap-name", "" if invalid else ("Elise Varga" if s != "default" else ""), invalid=invalid, readonly=busy, extra="autofocus"), error="Enter a name" if invalid else "")
            + field("ap-role", "Role", text_input("ap-role", "Head of Community" if s != "default" else "", readonly=busy))
            + field("ap-linkedin", "LinkedIn", text_input("ap-linkedin", "", "url", readonly=busy, placeholder="linkedin.com/in/"), optional=True, help_text="Leave blank to let research find it."))
    dlg = panel("Add person to FaithTech", "", body, cancel(disabled=busy) + primary("Add person", busy=busy))
    desc = {"default": "Add a person to an organisation.", "invalid": "Submitted without a name.", "busy": "Adding the person.", "failed": "Adding failed; input preserved."}[s]
    return over(ctx, "organization", "default", dlg, desc)


def link_problem(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    choices = "".join(f'<label class="choice"><input type="radio" name="problem" value="{p["id"]}"{" checked" if (p["id"] == "youth-formation" and s in ("busy", "failed")) else ""}{" disabled" if busy else ""}{" aria-invalid=\"true\"" if invalid else ""}><span class="choice__text">{p["title"]}<small>Score {p["score"]} · {len(p["orgs"])} organisations</small></span></label>' for p in PROBLEMS[:6])
    err = '<span class="field__error" id="lp-error">Choose a problem</span>' if invalid else ""
    failed = alert("danger", "Couldn't link", "Try again.", role="alert", dismiss=False) if s == "failed" else ""
    body = (failed + f'<form class="search" role="search"><label class="visually-hidden" for="lp-q">Filter problems</label>{icon("search")}<input class="input" id="lp-q" type="search" placeholder="Filter"{" disabled" if busy else ""}></form>'
            f'<fieldset{" aria-describedby=\"lp-error\"" if invalid else ""}><legend>Problem</legend>{choices}{err}</fieldset><a href="{ctx.p("problem-edit")}">New problem</a>')
    dlg = panel("Link FaithTech to a problem", "", body, cancel(disabled=busy) + primary("Link", busy=busy), size="")
    desc = {"default": "Choose a problem to link to the organisation.", "invalid": "Submitted with no problem chosen.", "busy": "Linking.", "failed": "Linking failed."}[s]
    return over(ctx, "organization", "default", dlg, desc)


def run_research(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    qs = "".join(f'<label class="choice"><input type="radio" name="question" value="{q["id"]}"{" checked" if q["id"] == "q1" and not invalid else ""}{" disabled" if busy else ""}><span class="choice__text">{q["text"]}</span></label>' for q in QUESTIONS)
    custom = f'<label class="choice"><input type="radio" name="question" value="custom"{" checked" if invalid else ""}{" disabled" if busy else ""}><span class="choice__text">Something else</span></label>'
    custom_field = field("rr-custom", "Your question", textarea("rr-custom", "", rows=2, invalid=invalid, readonly=busy), error="Write the question you want answered" if invalid else "") if invalid else ""
    scope = "".join(f'<label class="choice"><input type="checkbox" name="scope" value="{v}" checked{" disabled" if busy else ""}><span class="choice__text">{l}</span></label>' for v, l in [("orgs", "Organisations"), ("people", "People"), ("linkedin", "LinkedIn profiles")])
    depth = "".join(f'<label class="choice"><input type="radio" name="depth" value="{v}"{" checked" if v == "standard" else ""}{" disabled" if busy else ""}><span class="choice__text">{l}<small>{t}</small></span></label>' for v, l, t in [("quick", "Quick", "about 1 minute"), ("standard", "Standard", "about 5 minutes"), ("deep", "Deep", "about 20 minutes · more sources")])
    failed = alert("danger", "Couldn't start the run", "Two sources are rate-limiting us. Try again in 2 minutes, or run Quick.", role="alert", dismiss=False) if s == "failed" else ""
    summary = form_summary([("rr-custom", "Write the question you want answered")]) if invalid else ""
    body = (summary + failed + f'<fieldset><legend>Question</legend>{qs}{custom}</fieldset>{custom_field}'
            f'<div class="grid" style="--layout-columns:2;"><fieldset><legend>Look for</legend>{scope}</fieldset><fieldset><legend>Depth</legend>{depth}</fieldset></div>'
            '<p class="text-caption">Findings need two sources, or one trusted source, before they count as verified.</p>')
    dlg = panel("Ask the web", "", body, cancel(disabled=busy) + primary("Run", busy=busy), size="dialog__panel--lg")
    desc = {"default": "Start a research run: pick a question, scope and depth.", "invalid": "“Something else” chosen with an empty question.", "busy": "Starting the run.", "failed": "Run couldn't start because of rate limits."}[s]
    return over(ctx, "research", "default", dlg, desc, [note("Focus starts on the checked question. Run queues immediately and the dialog closes; progress shows on the Research page and in the banner.", "top: 1rem; right: 1rem;")] if s == "default" else [])


def review_finding(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    f = FINDINGS[0]
    p = PERSON_BY_ID[f["entity"]]
    failed = alert("danger", "Couldn't save", "Your edits are kept. Try again.", role="alert", dismiss=False) if s == "failed" else ""
    summary = form_summary([("rf-role", "Enter a role")]) if invalid else ""
    sources = [("Former Intel executive Pat Gelsinger joins Gloo", "religionunplugged.com", "2 Apr 2025"), ("Former Intel CEO Pat Gelsinger expands role at Gloo", "christianpost.com", "Apr 2025")]
    if s == "scroll":
        sources += [("Gelsinger hopes to make AI a force for good and for God", "baptiststandard.com", "2025"), ("Former Intel executive joins Gloo", "ministrywatch.com", "Apr 2025"), ("Gloo losses top $400M, SEC filing shows", "christiancentury.org", "Jul 2026"), ("Gloo introduces Flourishing AI standards", "religionnews.com", "2025")]
    src = "".join(f'<div class="source">{icon("link", "icon icon--sm text-subtle")}<div><a href="https://{h}" target="_blank" rel="noopener">{t}</a><div class="source__host">{h} · {w}</div></div></div>' for t, h, w in sources)
    body = (summary + failed + f'<blockquote class="finding__claim" style="border-left:4px solid var(--color-accent);padding-left:var(--space-4);">{f["claim"]}</blockquote>'
            f'<div class="finding__meta"><span>Confidence 92%</span><span>·</span><span>{len(sources)} sources</span><span>·</span>{verify("verified")}</div>'
            '<div class="grid" style="--layout-columns:2;">'
            + field("rf-role", "Role", text_input("rf-role", "" if invalid else "Executive Chair & Head of Technology", invalid=invalid, readonly=busy, extra="autofocus"), error="Enter a role" if invalid else "")
            + field("rf-since", "Since", text_input("rf-since", "2025", readonly=busy))
            + "</div>"
            + field("rf-org", "Organisation", select("rf-org", ["Gloo", "FaithTech", "OneHope"], "Gloo", disabled=busy))
            + f'<section><h3 class="section__title" style="margin-bottom:var(--space-2);">Sources</h3>{src}</section>')
    footer = f'<button class="btn btn--ghost" type="button"{" disabled" if busy else ""}>Reject</button>' + cancel(disabled=busy) + primary("Accept", busy=busy)
    dlg = panel("Review finding", f"Updates {p['name']} · Gloo", body, footer, size="dialog__panel--lg")
    desc = {"default": "Review a finding, adjust the fields it will write, then accept or reject.", "invalid": "Accepted with an empty role.", "busy": "Saving the accepted finding.", "failed": "Accept failed; edits kept.", "scroll": "Long finding with six sources: the body scrolls, header and footer stay."}[s]
    return over(ctx, "research", "review", dlg, desc, [note("Header and footer are sticky inside the panel; only the body scrolls.", "top: 1rem; right: 1rem;")] if s == "scroll" else [])


def import_csv(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "busy"
    if s == "success":
        body = alert("success", "312 organisations imported", "8 rows skipped as duplicates. New rows are unverified until research checks them.", dismiss=False)
        dlg = panel("Import CSV", "", body, f'<a class="btn" href="#">Download skipped rows</a><a class="btn btn--primary" href="{ctx.p("organizations", "long")}" autofocus>View organisations</a>')
        return over(ctx, "organizations", "default", dlg, "Import finished with a summary and the skipped rows available.")
    if s == "busy":
        body = f'<div class="stack"><div class="cluster cluster--between"><span>Importing organisations.csv</span><span class="text-caption">120 of 312</span></div><div class="progress" role="progressbar" aria-label="Import progress" aria-valuenow="38" aria-valuemin="0" aria-valuemax="100"><div class="progress__bar" style="--value:38%"></div></div><p class="text-caption">You can close this; the import continues and you\'ll get a notification.</p></div>'
        dlg = panel("Import CSV", "", body, cancel("Close") + primary("Import 312 rows", busy=True))
        return over(ctx, "organizations", "default", dlg, "Import in progress with determinate progress; closing doesn't cancel.")
    failed = alert("danger", "Import stopped at row 41", "“Website” isn't a URL: “faithtech”. Fix the file and import again; the first 40 rows were not saved.", '<a href="#">Download error report</a>', role="alert", dismiss=False) if s == "failed" else ""
    summary = form_summary([("csv-file", "Choose a .csv file with a Name column")]) if invalid else ""
    file_err = "This file has no Name column. Expected: Name, Website, Country, City, Tags." if invalid else ""
    preview = ('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Column mapping preview</caption><thead><tr><th scope="col">CSV column</th><th scope="col">Field</th><th scope="col">Sample</th></tr></thead><tbody>'
               '<tr><td>org</td><td>Name</td><td>Awana</td></tr><tr><td>url</td><td>Website</td><td>awana.org</td></tr><tr><td>hq</td><td>City</td><td>Streamwood</td></tr><tr><td>focus</td><td>Tags</td><td>Youth; Discipleship</td></tr></tbody></table></div>') if s in ("default", "failed") else ""
    body = (summary + failed + field("csv-file", "CSV file", f'<input class="input" id="csv-file" type="file" accept=".csv"{" aria-invalid=\"true\"" if invalid else ""} __DESC__>', help_text="Up to 5,000 rows. Columns: Name, Website, Country, City, Tags.", error=file_err)
            + (f'<p class="text-sm">organisations.csv · 312 rows · columns matched automatically</p>{preview}' if preview else ""))
    dlg = panel("Import CSV", "", body, cancel() + primary("Import 312 rows" if s != "invalid" else "Import", disabled=invalid), size="dialog__panel--lg")
    desc = {"default": "Import organisations from CSV with an automatic column mapping preview.", "invalid": "Chosen file lacks a Name column.", "failed": "Import stopped on a bad row with an error report."}[s]
    return over(ctx, "organizations", "default", dlg, desc)


def export(ctx: Ctx):
    s = ctx.state
    busy = s == "busy"
    fmt = "".join(f'<label class="choice"><input type="radio" name="format" value="{v}"{" checked" if v == "csv" else ""}{" disabled" if busy else ""}><span class="choice__text">{l}</span></label>' for v, l in [("csv", "CSV"), ("json", "JSON")])
    scope = "".join(f'<label class="choice"><input type="radio" name="scope" value="{v}"{" checked" if v == "all" else ""}{" disabled" if busy else ""}><span class="choice__text">{l}</span></label>' for v, l in [("all", "All 14 organisations"), ("filtered", "Current filter · 14"), ("people", "Include people · 16")])
    failed = alert("danger", "Couldn't build the export", "Try again.", role="alert", dismiss=False) if s == "failed" else ""
    body = failed + f'<div class="grid" style="--layout-columns:2;"><fieldset><legend>Format</legend>{fmt}</fieldset><fieldset><legend>Scope</legend>{scope}</fieldset></div>'
    dlg = panel("Export", "", body, cancel(disabled=busy) + primary("Export 14 organisations", busy=busy))
    desc = {"default": "Export organisations as CSV or JSON.", "busy": "Building the export file.", "failed": "Export failed."}[s]
    return over(ctx, "organizations", "default", dlg, desc)


def sign_out(ctx: Ctx):
    s = ctx.state
    busy = s == "busy"
    failed = alert("danger", "Couldn't sign out", "The server didn't respond. You're still signed in.", role="alert", dismiss=False) if s == "failed" else ""
    dlg = panel("Sign out?", "No unsynced edits. You'll need your password to come back.", failed, cancel(disabled=busy, autofocus=True) + primary("Sign out", busy=busy))
    desc = {"default": "Confirm sign out.", "busy": "Signing out.", "failed": "Sign out failed; still signed in."}[s]
    return over(ctx, "settings", "default", dlg, desc)


def unsaved_changes(ctx: Ctx):
    dlg = panel("Discard changes to FaithTech?", "3 fields changed: Summary, Website, Tags.", "", '<button class="btn btn--danger" type="button">Discard</button>' + primary("Keep editing", autofocus=True), icon_kind="danger")
    return over(ctx, "organization-edit", "default", dlg, "Leaving an edit form with unsaved changes; Keep editing is the safe default.", [note("Also triggered by the browser back button and by closing the tab (beforeunload).", "top: 1rem; right: 1rem;")])


def keyboard_shortcuts(ctx: Ctx):
    rows = [("⌘ K", "Search"), ("G then F", "Field"), ("G then O", "Organisations"), ("G then P", "People"), ("G then M", "Map"), ("N", "New organisation"), ("R", "Run research"), ("E", "Edit this record"), ("T", "Toggle theme"), ("?", "This list"), ("Esc", "Close")]
    dl = '<dl class="dl" style="gap:var(--space-3) var(--space-8);">' + "".join(f'<dt><span class="kbd">{k}</span></dt><dd>{v}</dd>' for k, v in rows) + "</dl>"
    dlg = panel("Keyboard shortcuts", "", dl, cancel("Close", autofocus=True))
    return over(ctx, "field", "default", dlg, "Reference list of keyboard shortcuts, opened with ?.")


RENDERERS = {
    "nav-sheet": nav_sheet, "command-palette": command_palette, "delete-organization": delete_organization, "delete-person": delete_person,
    "delete-problem": delete_problem, "add-person": add_person, "link-problem": link_problem, "run-research": run_research,
    "review-finding": review_finding, "import-csv": import_csv, "export": export,
    "sign-out": sign_out, "unsaved-changes": unsaved_changes, "keyboard-shortcuts": keyboard_shortcuts,
}


def render(ctx: Ctx):
    return RENDERERS[ctx.sid](ctx)
