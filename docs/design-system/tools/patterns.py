"""Pattern pages: compositions and the rules that span components."""
from __future__ import annotations

from shell import dodont, example, icon, mock_links, page, ul

P = []


def pattern(pid, title, lead, overview, when, structure_html, states, responsive, a11y, content, dos, sources):
    P.append(dict(pid=pid, title=title, lead=lead, overview=overview, when=when, structure=structure_html, states=states, responsive=responsive, a11y=a11y, content=content, dos=dos, sources=sources))


pattern("forms", "Forms", "One column in a 44rem card; validate on submit, then on input; summary first.",
        "<p>Create and edit pages for organisations, people and problems share one form shape.</p>",
        ["Page form for records; dialog form for one to three fields (Add person).", "Destructive confirmation needs the typed name."],
        f'<form class="card stack" style="max-width:28rem;gap:var(--space-6);" novalidate><div class="field"><label class="field__label" for="pf-n">Name</label><input class="input" id="pf-n" value="FaithTech"></div><div class="field"><label class="field__label" for="pf-w">Website</label><input class="input" id="pf-w" type="url" value="faithtech.com"></div><div class="form-actions"><button class="btn btn--ghost" type="button">Cancel</button><button class="btn btn--primary" type="button">Save</button></div></form>',
        ["Default · Invalid (summary + inline) · Submitting (busy, read-only) · Success (Saved · just now) · Unsaved changes dialog on leave."],
        ["Grids of short fields collapse to one column under 640px."], ["Focus to summary on failed submit; aria-invalid + aria-describedby."], ["Labels nouns; errors instructions."],
        [('<button class="btn btn--primary" type="button" aria-busy="true">Save</button>', "Busy on the pressed button.", '<span class="spinner spinner--lg" aria-hidden="true"></span>', "Form replaced by a spinner.")],
        ["pages/organization-edit/default", "pages/organization-edit/invalid", "dialogs/unsaved-changes/default"])

pattern("feedback-and-loading", "Feedback & loading", "Every action answers within 100ms; skeletons for pages, busy buttons for actions, progress for runs.",
        "<p>Choose the quietest feedback that is still seen.</p>",
        ["Inline status for saves.", "Toast for completed actions with Undo.", "Banner for long runs and connectivity.", "Dialog only for decisions."],
        '<div class="stack"><span class="inline-status inline-status--success">Saved · just now</span><div class="progress" role="progressbar" aria-label="Run" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" style="width:16rem;"><div class="progress__bar" style="--value:62%"></div></div></div>',
        ["< 300ms nothing; skeleton for first load; determinate progress when the length is known; optimistic accept/reject with undo."],
        ["Toasts span the width on phones."], ["Live regions for status; never steal focus."], ["Say what happened and what's next."],
        [('<span class="inline-status inline-status--success">Saved · just now</span>', "Quiet and specific.", '<div class="alert alert--success" role="alert"><div class="alert__body">Success!</div></div>', "Loud and vague.")],
        ["pages/settings/success", "pages/research/running", "notifications/toast/success"])

pattern("empty-and-error-states", "Empty & error states", "Teach on first run, help on no-results, recover on errors. Chrome stays.",
        "<p>Three kinds of empty, five error pages.</p>", ["First-run: what + why + one action.", "Filtered: echo query + Clear filters.", "Error: what + retry + reference."],
        f'<div class="empty empty--compact"><div class="empty__icon">{icon("filter", "icon icon--lg")}</div><h3 class="empty__title">Nothing matches</h3><p class="empty__text">No organisation matches “youth hackathon”.</p><div class="empty__actions"><button class="btn" type="button">Clear filters</button></div></div>',
        ["First-run · no-results · partial (one section failed) · error · 404/403/500/offline/unsupported."], ["Centred at all widths."], ["Headings in order; one action."], ["Never “No data”."],
        [('<p class="empty__text">No people yet. Add one or run research.</p>', "Next step.", '<p class="empty__text">Empty.</p>', "Dead end.")],
        ["pages/organizations/empty", "pages/organizations/no-results", "pages/field/partial", "pages/not-found/default"])

pattern("navigation", "Navigation & page structure", "Top bar, page header with numbers, breadcrumbs on details, ⌘K everywhere.",
        "<p>Seven destinations, no sidebar.</p>", ["Tabs for peers of one record; chips for filters; breadcrumbs for depth."],
        '<div class="page-header" style="margin:0;width:100%;"><div><h3 style="font:var(--text-h1);">Organizations</h3><p class="subtitle">14 tracked · 9 verified · 5 unverified</p></div><button class="btn btn--primary" type="button">New</button></div>',
        ["Current page marked with aria-current; page title morphs via view transitions."], ["Drawer under 768px."], ["Skip link; landmarks; unique titles."], ["Subtitles are numbers, not sentences."],
        [('<p class="subtitle">14 tracked · 9 verified</p>', "Numbers first.", '<p class="subtitle">Here you can find all the organisations we track.</p>', "Explaining the page.")],
        ["pages/organizations/default", "dialogs/nav-sheet/default", "dialogs/command-palette/default"])

pattern("dialogs-and-overlays", "Dialogs & overlays", "Dialog for decisions, drawer for navigation, popover for previews, page for long forms.",
        "<p>One overlay at a time; palette replaces, never stacks.</p>", ["Dialog: confirm, short form, review.", "Drawer: phone nav.", "Popover: map pin.", "Page: anything with more than five fields."],
        '<div class="dialog__panel" style="position:relative;max-width:24rem;animation:none;"><div class="dialog__header"><h3 class="dialog__title">Sign out?</h3></div><div class="dialog__footer"><button class="btn" type="button">Cancel</button><button class="btn btn--primary" type="button">Sign out</button></div></div>',
        ["Default · busy · invalid · failed (inputs kept) · success (stay open to add another) · scroll."], ["Bottom sheets under 640px."], ["APG Dialog; inert page; return focus."], ["Title is a question for confirmations."],
        [('<span class="tag">Typed name to delete</span>', "Friction for destruction.", '<span class="tag">Two nested dialogs</span>', "Stacked modals.")],
        ["dialogs/delete-organization/default", "dialogs/review-finding/scroll", "pages/map/default"])

pattern("data-lists", "Data tables & lists", "Entity cards for records, tables for comparisons; filters as chips; 25 per page.",
        "<p>Lists sort by impact by default and remember the last sort.</p>", ["Cards when each row is a thing; table when columns are compared."],
        '<div class="toolbar" style="width:100%;margin:0;"><div class="cluster"><button class="chip" type="button" aria-pressed="true">AI</button><button class="chip" type="button" aria-pressed="false">Youth</button></div><span class="text-caption">Showing 1–25 of 1,284</span></div>',
        ["Loading skeleton · empty · no-results · long (pagination) · selected (bulk bar) · edge (long names, RTL, CJK)."], ["Cards wrap on phones; tables scroll inside."], ["Row checks labelled; bulk bar is a region."], ["Count actions: Export 3."],
        [('<span class="tag">Wrap long names</span>', "Full names.", '<span class="tag">Truncate…</span>', "Ellipsis with no title.")],
        ["pages/organizations/default", "pages/organizations/selected", "pages/organizations/edge", "pages/organizations/long"])

pattern("notifications", "Notifications", "Toast for what you did, banner for what is happening, centre for what happened while away.",
        "<p>Three channels, no duplicates.</p>", ["Toast: own action, 8s, Undo.", "Banner: runs, offline, workspace changes.", "Notification centre: history with unread dots."],
        '<div class="alert alert--info banner" role="status" style="width:100%;"><span class="dot dot--pulse" aria-hidden="true"></span><div class="alert__body"><span class="alert__title">Run #48 running · 62%</span></div></div>',
        ["info · success · warning · danger (persistent) · with action · stacked (max 3) · persistent banner."], ["Toasts full width on phones."], ["Polite for status, assertive for errors."], ["Past tense, specific."],
        [('<span class="tag">Error persists</span>', "Errors wait.", '<span class="tag">Error auto-dismisses</span>', "Lost failures.")],
        ["notifications/toast/stacked", "notifications/research-banner/info", "pages/notifications/default"])

pattern("content-and-tone", "Content & tone", "Minimal text: nouns, verbs and numbers. See the content foundation for the library.",
        "<p>Every word earns its place.</p>", ["Labels nouns; buttons verbs; subtitles numbers."],
        '<p class="subtitle">9 ranked · illumiNations leads with 94</p>',
        ["—"], ["Shorter labels on phones (Orgs)."], ["Link text stands alone."], ["See foundations/content.html."],
        [('<button class="btn btn--primary" type="button">Ask the web</button>', "Verb, short.", '<button class="btn btn--primary" type="button">Click here to start a new research run</button>', "Wordy.")],
        ["pages/field/default", "pages/problems/default"])

pattern("research-review", "Research & review", "Ask the web → live run → findings → accept/edit/reject → records. Nothing unverified becomes fact.",
        "<p>Harvest Map's core loop.</p>", ["Run research from any empty state, the Field hero, or a record."],
        '<div class="card finding" style="max-width:28rem;"><p class="finding__claim">FaithTech is active in 50+ cities.</p><div class="finding__meta"><span>mnnonline.org</span><span>·</span><span>Confidence 78%</span></div><div class="finding__actions"><button class="btn btn--sm btn--primary" type="button">Accept</button><button class="btn btn--sm btn--ghost" type="button">Reject</button></div></div>',
        ["Queued · running (live log, determinate progress) · done · failed (retry) · findings new/accepted/rejected."], ["Run log wraps; actions wrap."], ["Run log is a polite live region."], ["Low confidence states its reason inline."],
        [('<span class="verify verify--pending">Company claim; no independent source.</span>', "Reason shown.", '<span class="verify verify--verified">Verified</span>', "Verifying a single claim.")],
        ["pages/research/running", "pages/research/review", "dialogs/run-research/default", "pages/people/default"])


def build():
    for p in P:
        sections = [("overview", "Overview", p["overview"], None), ("when", "When to use", ul(p["when"]), None),
                    ("structure", "Structure", example(p["structure"], "Live composition."), None), ("states", "States", ul(p["states"]), None),
                    ("responsive", "Responsive", ul(p["responsive"]), None), ("accessibility", "Accessibility", ul(p["a11y"]), None),
                    ("content", "Content", ul(p["content"]), None), ("do-dont", "Do and don't", dodont(p["dos"]), None),
                    ("sources", "Sources", mock_links("../", p["sources"]), None)]
        page(f"patterns/{p['pid']}.html", p["title"], "Pattern", p["lead"], sections)
