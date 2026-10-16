"""Page renderers for Harvest Map mocks. Each returns {description, body, notes, scripts}."""
from __future__ import annotations

from build import Ctx, icon, note, topbar
from data import FINDINGS, ME, ORG_BY_ID, ORGS, PEOPLE, PERSON_BY_ID, PROBLEM_BY_ID, PROBLEMS, QUESTIONS, RUNS, TEAM

VERIFY_LABEL = {"verified": "Verified", "pending": "Unverified", "conflict": "Conflict", "none": "Not found"}
LINKEDIN_SEARCH = "https://www.linkedin.com/search/results/people/?keywords="

EXTRA_ORGS = ["Cru", "Youth With A Mission", "Youth for Christ International", "Awana", "Scripture Union", "Jesus Film Project",
              "Wycliffe Bible Translators", "SIL Global", "Biblica", "BibleProject", "Hallow", "Pray.com", "Compassion International",
              "Kingdom Code", "Praxis", "Faith Driven Entrepreneur", "AI and Faith", "Christian Transhumanist Association", "Lead Today", "Hope Media Group"]


# ---------------------------------------------------------------------------
# Fragments
# ---------------------------------------------------------------------------
def main_wrap(ctx: Ctx, current: str | None, inner: str, banner: str = "", unread: int = 2) -> str:
    return f'{topbar(ctx, current, unread)}{banner}<main id="main" class="container app-main">{inner}</main>'


def header(title: str, subtitle: str = "", actions: str = "", crumbs: str = "") -> str:
    sub = f'<p class="subtitle">{subtitle}</p>' if subtitle else ""
    act = f'<div class="cluster">{actions}</div>' if actions else ""
    return f'{crumbs}<div class="page-header rise"><div><h1>{title}</h1>{sub}</div>{act}</div>'


def crumbs(items: list[tuple[str, str | None]]) -> str:
    lis = "".join(f'<li><a href="{href}">{label}</a></li>' if href else f'<li aria-current="page">{label}</li>' for label, href in items)
    return f'<nav aria-label="Breadcrumb" style="margin-bottom: var(--space-6);"><ol class="breadcrumb">{lis}</ol></nav>'


def verify(status: str) -> str:
    return f'<span class="verify verify--{status if status != "none" else "none"}">{VERIFY_LABEL[status]}</span>'


def tags(items: list[str]) -> str:
    cls = {"AI": " tag--ai", "Moonshot": " tag--moonshot"}
    return '<div class="tags">' + "".join(f'<span class="tag{cls.get(t, "")}">{t}</span>' for t in items) + "</div>"


def skeleton_lines(n: int = 3, widths=("70%", "50%", "40%")) -> str:
    return "".join(f'<span class="skeleton skeleton--text" style="width:{widths[i % len(widths)]}"></span>' for i in range(n))


def skeleton_cards(n: int, with_mark: bool = True) -> str:
    cards = []
    for i in range(n):
        mark = '<span class="skeleton skeleton--rect" style="width:3rem;height:3rem;"></span>' if with_mark else ""
        cards.append(f'<div class="card" style="--i:{i}"><div class="org-card">{mark}<div style="min-width:0;">{skeleton_lines(2, ("55%", "85%"))}</div><span class="skeleton" style="width:4rem;height:1.25rem;"></span></div></div>')
    return f'<div class="entity-list" aria-busy="true" aria-label="Loading">{"".join(cards)}</div>'


def header_skeleton(actions: bool = True, title: str | None = None) -> str:
    act = '<span class="skeleton skeleton--rect" style="width:9rem;height:2.5rem;"></span>' if actions else ""
    h1 = f"<h1>{title}</h1>" if title else '<h1 class="visually-hidden">Loading</h1><span class="skeleton skeleton--title" style="width:min(12rem, 60vw);height:2.25rem;"></span>'
    return f'<div class="page-header" style="width:100%;"><div style="flex:1;min-width:0;">{h1}<span class="skeleton skeleton--text" style="width:min(18rem, 80%);margin-top:var(--space-4);"></span></div>{act}</div>'


def empty(ctx: Ctx, icon_name: str, title: str, text: str, actions: str, error: bool = False, compact: bool = False) -> str:
    cls = "empty" + (" empty--error" if error else "") + (" empty--compact" if compact else "")
    return f'<div class="{cls} rise"><div class="empty__icon">{icon(icon_name, "icon icon--lg")}</div><h2 class="empty__title">{title}</h2><p class="empty__text">{text}</p><div class="empty__actions">{actions}</div></div>'


def error_block(ctx: Ctx, what: str, retry: str = "default.html", back: str | None = None, ref: str = "HM-4F2A") -> str:
    back_html = f'<a class="btn btn--ghost" href="{back}">Go back</a>' if back else ""
    return empty(ctx, "danger", f"Couldn't load {what}", f"The request timed out. Try again, or share reference {ref} with support.",
                 f'<a class="btn btn--primary" href="{retry}">{icon("refresh")}Try again</a>{back_html}', error=True)


def btn(label: str, href: str | None = None, kind: str = "", icon_name: str | None = None, attrs: str = "") -> str:
    ic = icon(icon_name) if icon_name else ""
    cls = f"btn {kind}".strip()
    if href:
        return f'<a class="{cls}" href="{href}" {attrs}>{ic}{label}</a>'
    return f'<button class="{cls}" type="button" {attrs}>{ic}{label}</button>'


def field(fid: str, label: str, control: str, help_text: str = "", error: str = "", optional: bool = False) -> str:
    opt = ' <span class="optional">(optional)</span>' if optional else ""
    desc = []
    help_html = err_html = ""
    if help_text:
        help_html = f'<span class="field__help" id="{fid}-help">{help_text}</span>'
        desc.append(f"{fid}-help")
    if error:
        err_html = f'<span class="field__error" id="{fid}-error">{error}</span>'
        desc.append(f"{fid}-error")
    control = control.replace("__DESC__", f'aria-describedby="{" ".join(desc)}"' if desc else "")
    return f'<div class="field"><label class="field__label" for="{fid}">{label}{opt}</label>{control}{help_html}{err_html}</div>'


def text_input(fid: str, value: str = "", typ: str = "text", invalid: bool = False, readonly: bool = False, placeholder: str = "", extra: str = "") -> str:
    inv = ' aria-invalid="true"' if invalid else ""
    ro = " readonly" if readonly else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    return f'<input class="input" id="{fid}" name="{fid}" type="{typ}" value="{value}"{inv}{ro}{ph} __DESC__ {extra}>'


def select(fid: str, options: list[str], selected: str = "", invalid: bool = False, disabled: bool = False) -> str:
    opts = "".join(f'<option{" selected" if o == selected else ""}>{o}</option>' for o in options)
    return f'<select class="select" id="{fid}" name="{fid}"{" aria-invalid=\"true\"" if invalid else ""}{" disabled" if disabled else ""} __DESC__>{opts}</select>'


def textarea(fid: str, value: str = "", rows: int = 3, invalid: bool = False, readonly: bool = False) -> str:
    return f'<textarea class="textarea" id="{fid}" name="{fid}" rows="{rows}"{" aria-invalid=\"true\"" if invalid else ""}{" readonly" if readonly else ""} __DESC__>{value}</textarea>'


def form_summary(errors: list[tuple[str, str]]) -> str:
    items = "".join(f'<li><a href="#{fid}">{msg}</a></li>' for fid, msg in errors)
    n = len(errors)
    return f'<div class="alert alert--danger form-summary" role="alert" tabindex="-1" id="form-summary">{icon("danger")}<div class="alert__body"><div class="alert__title">Fix {n} {"thing" if n == 1 else "things"} to save</div><ul style="margin:0;padding-left:var(--space-5);">{items}</ul></div></div>'


def alert(kind: str, title: str, text: str = "", actions: str = "", icon_name: str | None = None, role: str = "status", dismiss: bool = True) -> str:
    ic = icon(icon_name or kind)
    body = f'<div class="alert__title">{title}</div>' + (f"<div>{text}</div>" if text else "") + (f'<div class="alert__actions">{actions}</div>' if actions else "")
    close = f'<button class="close" type="button" aria-label="Dismiss">{icon("close", "icon icon--sm")}</button>' if dismiss else ""
    return f'<div class="alert alert--{kind}" role="{role}">{ic}<div class="alert__body">{body}</div>{close}</div>'


def avatar(initials: str, size: str = "avatar--sm") -> str:
    return f'<span class="avatar {size}" aria-hidden="true">{initials}</span>'


def score(value: int, size: str = "", rank: int | None = None) -> str:
    r = f' data-rank="{rank}"' if rank else ""
    return f'<span class="score {size}" style="--score:{value}" role="img" aria-label="Impact score {value} of 100"{r}><span>{value}</span></span>'


def org_card(ctx: Ctx, o: dict, i: int = 0, checkbox: bool = False, checked: bool = False, name: str | None = None, mark: str | None = None,
             meta: str | None = None, tag_list: list[str] | None = None) -> str:
    name = name or o["name"]
    place = o["city"] or o["country"]
    meta = meta if meta is not None else f'{o["kind"]} · {place} · {o["reach"]}'
    check = f'<label class="row-check"><input type="checkbox" aria-label="Select {name}"{" checked" if checked else ""}></label>' if checkbox else ""
    mk = f'<span class="mark" aria-hidden="true">{mark if mark is not None else o["mark"]}</span>'
    sel = ' aria-selected="true"' if checked else ""
    return (f'<div class="card lift rise" style="--i:{i}"{sel}><div class="org-card">{check}{mk}'
            f'<div style="min-width:0;"><a class="org-card__name" href="{ctx.p("organization")}" style="text-decoration:none;color:inherit;">{name}</a>'
            f'<div class="org-card__meta">{meta}</div>{tags(tag_list if tag_list is not None else o["tags"])}</div>'
            f'<div class="org-card__end">{verify(o["verified"])}{icon("arrow", "icon text-subtle")}</div></div></div>')


def linkedin_cell(ctx: Ctx, p: dict) -> str:
    q = (p["name"] + " " + ORG_BY_ID[p["org"]]["name"]).replace(" ", "%20")
    if p["linkedin"] == "verified":
        return f'<a class="linkedin" href="{LINKEDIN_SEARCH}{q}" target="_blank" rel="noopener">{icon("linkedin", "icon icon--sm")}LinkedIn{icon("external", "icon icon--sm")}</a>'
    return '<span class="text-subtle">No LinkedIn yet</span>'


def person_row(ctx: Ctx, p: dict, i: int = 0, name: str | None = None, role: str | None = None) -> str:
    o = ORG_BY_ID[p["org"]]
    return (f'<div class="card lift rise" style="--i:{i};padding:0;"><div class="org-card" style="grid-template-columns:auto 1fr auto;">'
            f'{avatar(p["initials"], "avatar")}<div style="min-width:0;"><a class="people-row__name" href="{ctx.p("person")}" style="text-decoration:none;color:inherit;font:var(--text-h4);">{name or p["name"]}</a>'
            f'<div class="people-row__role">{role or p["role"]} · {o["name"]}</div></div>{linkedin_cell(ctx, p)}</div></div>')


def problem_row(ctx: Ctx, pr: dict, i: int = 0) -> str:
    orgs = "".join(f'<span class="avatar avatar--sm" aria-hidden="true" title="{ORG_BY_ID[o]["name"]}">{ORG_BY_ID[o]["mark"]}</span>' for o in pr["orgs"][:4])
    names = ", ".join(ORG_BY_ID[o]["name"] for o in pr["orgs"])
    return (f'<div class="card lift rise" style="--i:{i};padding:0;"><div class="org-card" style="grid-template-columns:2rem auto 1fr auto;">'
            f'<span class="text-subtle" style="font:var(--text-label);font-variant-numeric:tabular-nums;">{pr["rank"]}</span>{score(pr["score"], rank=pr["rank"])}'
            f'<div style="min-width:0;"><a class="org-card__name" href="{ctx.p("problem")}" style="text-decoration:none;color:inherit;">{pr["title"]}</a>'
            f'<div class="org-card__meta">{pr["reach"]} · {pr["status"]}</div></div>'
            f'<div class="avatar-group" aria-label="Working on it: {names}">{orgs}</div></div></div>')


def q_card(ctx: Ctx, q: dict, i: int = 0, loading: bool = False, failed: bool = False) -> str:
    if loading:
        return f'<div class="card q-card" style="--i:{i}"><span class="skeleton skeleton--text" style="width:2rem"></span><span class="skeleton skeleton--text" style="width:80%;height:1.4em;"></span><span class="skeleton skeleton--title" style="width:30%;height:2.2em;"></span></div>'
    if failed:
        return f'<div class="card q-card" style="--i:{i}" data-status="open"><span class="q-card__n">{q["n"]}</span><span class="q-card__q">{q["text"]}</span><div class="q-card__a"><span class="q-card__num text-subtle">—</span><span class="q-card__unit">couldn\'t load</span></div><div class="q-card__foot"><a href="{ctx.p("questions", "partial")}">Retry</a></div></div>'
    status = {"answered": "Answered", "partial": "Partial", "open": "Open"}[q["status"]]
    num = q["num"] if q["status"] != "open" else "—"
    return (f'<a class="card q-card lift rise" href="{ctx.p("questions")}" style="--i:{i}" data-status="{q["status"]}"><span class="q-card__n">{q["n"]}</span>'
            f'<span class="q-card__q">{q["text"]}</span><div class="q-card__a"><span class="q-card__num">{num}</span><span class="q-card__unit">{q["unit"]}</span></div>'
            f'<div class="q-card__foot"><span>{status}</span><span>{q["sources"]} sources</span></div></a>')


def run_status(status: str) -> str:
    label = {"running": "Running", "done": "Done", "failed": "Failed", "queued": "Queued"}[status]
    dot = ' dot--pulse' if status == "running" else ""
    return f'<span class="run-status run-status--{status}"><span class="dot{dot}"></span>{label}</span>'


def run_row(ctx: Ctx, r: dict, i: int = 0) -> str:
    prog = f'<div class="progress progress--thin" role="progressbar" aria-label="Run {r["id"]} progress" aria-valuenow="{r["progress"]}" aria-valuemin="0" aria-valuemax="100" style="margin-top:var(--space-3);"><div class="progress__bar" style="--value:{r["progress"]}%"></div></div>' if r["status"] == "running" else ""
    return (f'<div class="card lift rise" style="--i:{i};padding:var(--space-5) var(--space-6);"><div class="cluster cluster--between"><div style="min-width:0;">'
            f'<a href="{ctx.p("research", "running" if r["status"] == "running" else "review")}" style="text-decoration:none;color:inherit;font:var(--text-label);">#{r["id"]} · {r["title"]}</a>'
            f'<div class="text-caption" style="margin-top:var(--space-1);">{r["started"]} · {r["by"]} · {r["findings"]} findings</div></div>{run_status(r["status"])}</div>{prog}</div>')


def finding_card(ctx: Ctx, f: dict, i: int = 0) -> str:
    cls = {"new": "", "accepted": " finding--accepted", "rejected": " finding--rejected"}[f["state"]]
    entity = PERSON_BY_ID[f["entity"]]["name"] if f["kind"] == "person" else ORG_BY_ID[f["entity"]]["name"]
    pct = int(f["conf"] * 100)
    noteh = f'<span class="verify verify--pending">{f["note"]}</span>' if f.get("note") else ""
    if f["state"] == "new":
        actions = (f'<a class="btn btn--sm btn--primary" href="{ctx.d("review-finding")}">{icon("check")}Accept</a>'
                   f'<a class="btn btn--sm" href="{ctx.d("review-finding")}">Edit</a><button class="btn btn--sm btn--ghost" type="button">Reject</button>')
    else:
        actions = f'<span class="text-caption">{f["state"].capitalize()} by {ME["name"]} · Undo available for 30 s</span><button class="btn btn--sm btn--ghost" type="button">Undo</button>'
    return (f'<div class="card finding{cls} rise" style="--i:{i}"><p class="finding__claim">{f["claim"]}</p>'
            f'<div class="finding__meta"><span>{entity}</span><span>·</span><span>{f["source"]}</span><span>·</span><span>Confidence {pct}%</span>{noteh}</div>'
            f'<div class="finding__actions">{actions}</div></div>')


def auth_shell(inner: str) -> str:
    return f'<main id="main" class="auth-layout"><div class="auth-card card rise" style="padding:var(--space-10);">{inner}</div></main>'


def brand_lockup() -> str:
    return f'<div class="logo" style="justify-content:flex-start;color:var(--color-fg-accent);">{icon("wheat", "icon icon--lg")}</div>'


# ---------------------------------------------------------------------------
# Entry pages
# ---------------------------------------------------------------------------
def sign_in(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "submitting"
    summary = form_summary([("email", "Enter the e-mail address you were invited with"), ("password", "Enter your password")]) if invalid else ""
    err = alert("danger", "Can't reach Harvest Map", "Check your connection, then try again.", f'<button type="button">{icon("refresh", "icon icon--sm")} Retry</button>', role="alert", dismiss=False) if s == "error" else ""
    if s == "success":
        inner = f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Welcome back</h1><p class="text-muted" style="margin-top:var(--space-3);">Signed in. Taking you to the field.</p><div class="inline-status" style="margin-top:var(--space-8);"><span class="spinner" aria-hidden="true"></span> Loading your workspace</div>'
        return dict(description="Sign-in succeeded; a brief transition before the Field page.", body=auth_shell(inner),
                    notes=[note("Redirects to Field after the session is stored (under 1 s). The spinner only appears if that takes more than 300 ms.", "top: 1rem; right: 1rem;")])
    inner = (f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Sign in</h1><p class="text-muted" style="margin-top:var(--space-2);">Harvest Map is invite-only.</p>'
             f'<form class="stack" style="margin-top:var(--space-8);gap:var(--space-5);" novalidate>{summary}{err}'
             + field("email", "E-mail", text_input("email", "naomi@harvestmap" if invalid else ("naomi@harvestmap.app" if s != "default" else ""), "email", invalid=invalid, readonly=busy, extra='autocomplete="username" autofocus'),
                     error="Enter an e-mail address like name@example.com" if invalid else "")
             + field("password", "Password", text_input("password", "" if invalid else ("••••••••••" if s != "default" else ""), "password", invalid=invalid, readonly=busy, extra='autocomplete="current-password"'),
                     error="Enter your password" if invalid else "")
             + f'<div class="cluster cluster--between" style="margin-top:var(--space-2);"><a href="{ctx.p("forgot-password")}">Forgot password?</a>'
             + (f'<button class="btn btn--primary" type="submit" aria-busy="true">Continue</button>' if busy else '<button class="btn btn--primary" type="submit">Continue</button>')
             + '</div></form>'
             + f'<p class="text-caption" style="margin-top:var(--space-10);">Works in Chrome 125 or newer. {icon("chrome", "icon icon--sm")}</p>')
    desc = {"default": "Sign-in form with e-mail and password; invite-only workspace.", "invalid": "Sign-in submitted with an invalid e-mail and empty password.",
            "submitting": "Sign-in in flight; button busy, fields read-only.", "error": "Sign-in failed because the server could not be reached."}[s]
    notes = [note("Focus starts in the e-mail field. Enter submits.", "top: 1rem; right: 1rem;")] if s == "default" else []
    if invalid:
        notes = [note("On submit, focus moves to the error summary; each item links to its field.", "top: 1rem; right: 1rem;")]
    return dict(description=desc, body=auth_shell(inner), notes=notes)


def forgot_password(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "submitting"
    if s == "success":
        inner = (f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Check your inbox</h1><p class="text-muted" style="margin-top:var(--space-3);">We sent a reset link to naomi@harvestmap.app. It works for 30 minutes.</p>'
                 f'<div class="cluster" style="margin-top:var(--space-8);"><button class="btn" type="button" disabled>Resend in 58 s</button><a class="btn btn--ghost" href="{ctx.p("sign-in")}">Back to sign in</a></div>')
        return dict(description="Reset link sent; resend is rate-limited.", body=auth_shell(inner), notes=[note("Resend counts down from 60 s and then enables.", "top: 1rem; right: 1rem;")])
    summary = form_summary([("email", "Enter the e-mail address you were invited with")]) if invalid else ""
    err = alert("danger", "Couldn't send the link", "Try again in a moment.", role="alert", dismiss=False) if s == "error" else ""
    inner = (f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Reset your password</h1><p class="text-muted" style="margin-top:var(--space-2);">We\'ll e-mail you a link.</p>'
             f'<form class="stack" style="margin-top:var(--space-8);gap:var(--space-5);" novalidate>{summary}{err}'
             + field("email", "E-mail", text_input("email", "naomi@" if invalid else ("naomi@harvestmap.app" if s != "default" else ""), "email", invalid=invalid, readonly=busy, extra='autocomplete="username" autofocus'),
                     error="Enter an e-mail address like name@example.com" if invalid else "")
             + f'<div class="cluster cluster--between" style="margin-top:var(--space-2);"><a href="{ctx.p("sign-in")}">Back to sign in</a>'
             + (f'<button class="btn btn--primary" type="submit" aria-busy="true">Send link</button>' if busy else '<button class="btn btn--primary" type="submit">Send link</button>') + '</div></form>')
    desc = {"default": "Request a password reset link.", "invalid": "Submitted with a malformed e-mail.", "submitting": "Sending the reset link.", "error": "Sending the link failed."}[s]
    return dict(description=desc, body=auth_shell(inner), notes=[])


def reset_password(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "submitting"
    if s == "loading":
        inner = f'{brand_lockup()}<h1 class="visually-hidden">Checking your link</h1><span class="skeleton skeleton--title" style="width:60%;height:2.25rem;margin-top:var(--space-6);"></span>{skeleton_lines(1, ("50%",))}<span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-8);"></span><span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-4);"></span>'
        return dict(description="Validating the reset link before showing the form.", body=auth_shell(f'<div aria-busy="true" aria-label="Checking your link">{inner}</div>'), notes=[])
    if s == "error":
        inner = f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">This link has expired</h1><p class="text-muted" style="margin-top:var(--space-3);">Reset links work for 30 minutes. Request a new one.</p><div class="cluster" style="margin-top:var(--space-8);"><a class="btn btn--primary" href="{ctx.p("forgot-password")}">Request a new link</a><a class="btn btn--ghost" href="{ctx.p("sign-in")}">Back to sign in</a></div>'
        return dict(description="Reset link expired or already used.", body=auth_shell(inner), notes=[])
    if s == "success":
        inner = f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Password updated</h1><p class="text-muted" style="margin-top:var(--space-3);">Sign in with your new password.</p><div class="cluster" style="margin-top:var(--space-8);"><a class="btn btn--primary" href="{ctx.p("sign-in")}">Sign in</a></div>'
        return dict(description="Password changed; next step is sign in.", body=auth_shell(inner), notes=[])
    summary = form_summary([("new-password", "Use at least 12 characters"), ("confirm-password", "Passwords don't match")]) if invalid else ""
    inner = (f'{brand_lockup()}<h1 style="margin-top:var(--space-6);">Choose a new password</h1>'
             f'<form class="stack" style="margin-top:var(--space-8);gap:var(--space-5);" novalidate>{summary}'
             + field("new-password", "New password", text_input("new-password", "••••••" if invalid else ("••••••••••••••" if busy else ""), "password", invalid=invalid, readonly=busy, extra='autocomplete="new-password" autofocus'),
                     help_text="At least 12 characters.", error="Use at least 12 characters" if invalid else "")
             + field("confirm-password", "Confirm password", text_input("confirm-password", "••••••••" if invalid else ("••••••••••••••" if busy else ""), "password", invalid=invalid, readonly=busy, extra='autocomplete="new-password"'),
                     error="Passwords don't match" if invalid else "")
             + '<div class="cluster cluster--end" style="margin-top:var(--space-2);">'
             + (f'<button class="btn btn--primary" type="submit" aria-busy="true">Update password</button>' if busy else '<button class="btn btn--primary" type="submit">Update password</button>') + '</div></form>')
    desc = {"default": "New password form from a valid reset link.", "invalid": "Submitted with a short password and a mismatch.", "submitting": "Saving the new password."}[s]
    return dict(description=desc, body=auth_shell(inner), notes=[])


# ---------------------------------------------------------------------------
# Field (home)
# ---------------------------------------------------------------------------
def hero(ctx: Ctx, title: str, lead: str, actions: str) -> str:
    return (f'<section class="hero"><canvas class="field-canvas" aria-hidden="true"></canvas><h1 class="hero__title rise">{title}</h1>'
            f'<p class="hero__lead rise" style="--i:1">{lead}</p><div class="hero__actions cluster rise" style="--i:2">{actions}</div></section>')


def field_page(ctx: Ctx):
    s = ctx.state
    actions = f'<a class="btn btn--primary btn--lg" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a><a class="btn btn--ghost btn--lg" href="{ctx.p("map")}">See the map</a>'
    top3 = PROBLEMS[:3]
    if s == "empty":
        inner = hero(ctx, "The field is empty.", "Add an organisation or let a research run find the first ones.", f'<a class="btn btn--primary btn--lg" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a><a class="btn btn--ghost btn--lg" href="{ctx.p("organization-edit")}">{icon("plus")}Add an organisation</a>')
        inner += '<section class="section"><h2 class="section__title">Questions</h2><div class="q-grid">' + "".join(q_card(ctx, dict(q, status="open", sources=0), i) for i, q in enumerate(QUESTIONS)) + "</div></section>"
        return dict(description="First run: no organisations, people or research yet; every question is open.", body=main_wrap(ctx, "field", inner, unread=0), scripts=["field.js"],
                    notes=[note("The field behind the title is a WebGPU particle simulation (assets/field.js); without WebGPU it falls back to a slow CSS gradient.", "top: 5rem; right: 1rem;")])
    if s == "loading":
        inner = hero(ctx, "The field is ripe.", "Loading your workspace.", actions)
        inner += '<section class="section" aria-busy="true"><h2 class="section__title">Questions</h2><div class="q-grid">' + "".join(q_card(ctx, q, i, loading=True) for i, q in enumerate(QUESTIONS)) + "</div></section>"
        inner += '<section class="section"><h2 class="section__title">Most impactful</h2>' + skeleton_cards(3, with_mark=False) + "</section>"
        return dict(description="Field page while the questions and rankings load; skeletons match the final layout.", body=main_wrap(ctx, "field", inner), scripts=["field.js"], notes=[])
    if s == "error":
        inner = hero(ctx, "The field is ripe.", "We couldn't load your workspace.", actions) + error_block(ctx, "the field", back=None)
        return dict(description="Field page when the workspace request fails; hero and navigation stay.", body=main_wrap(ctx, "field", inner), scripts=["field.js"], notes=[])
    lead = "19 organisations · 16 people · 9 problems. 2 research runs since yesterday."
    inner = hero(ctx, "The field is ripe.", lead, actions)
    inner += '<section class="section"><h2 class="section__title">Questions</h2><div class="q-grid">' + "".join(q_card(ctx, q, i) for i, q in enumerate(QUESTIONS)) + "</div></section>"
    if s == "partial":
        inner += ('<section class="section reveal"><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Most impactful</h2></div>'
                  + alert("danger", "Couldn't load the ranking", "The problems service didn't answer in time.", f'<a href="{ctx.p("field")}">Retry</a>', role="alert", dismiss=False) + "</section>")
    else:
        inner += ('<section class="section reveal"><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Most impactful</h2><a href="' + ctx.p("problems") + '">All problems</a></div><div class="entity-list">'
                  + "".join(problem_row(ctx, p, i) for i, p in enumerate(top3)) + "</div></section>")
    inner += ('<section class="section reveal"><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Latest research</h2><a href="' + ctx.p("research") + '">All runs</a></div><div class="entity-list">'
              + "".join(run_row(ctx, r, i) for i, r in enumerate(RUNS[:3])) + "</div></section>")
    desc = "Field page: the six questions at a glance, the top three problems and the latest research runs." if s == "default" else "Field page where the questions loaded but the ranking failed; the rest keeps working."
    notes = [note("Hero particles are a WebGPU compute + render pass (assets/field.js), tinted from the accent token so themes just work. Cards enter with @starting-style; lower sections reveal with scroll-driven animation.", "top: 5rem; right: 1rem;")] if s == "default" else []
    return dict(description=desc, body=main_wrap(ctx, "field", inner), scripts=["field.js"], notes=notes)


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------
def org_toolbar(ctx: Ctx, query: str = "", active: list[str] = (), disabled: bool = False) -> str:
    chips = "".join(f'<button class="chip" type="button" aria-pressed="{"true" if c in active else "false"}"{" disabled" if disabled else ""}>{c}</button>' for c in ["AI", "Youth", "Moonshot", "Verified"])
    return (f'<div class="toolbar rise" style="--i:1"><form class="search" role="search" style="flex:1 1 16rem;max-width:24rem;"><label class="visually-hidden" for="q">Search organisations</label>{icon("search")}<input class="input" id="q" type="search" value="{query}" placeholder="Search"{" disabled" if disabled else ""}></form>'
            f'<div class="cluster">{chips}<label class="field" style="flex-direction:row;align-items:center;gap:var(--space-2);"><span class="field__label">Sort</span><select class="select input--sm" style="width:auto;" aria-label="Sort organisations"{" disabled" if disabled else ""}><option>Impact</option><option>Name</option><option>Updated</option></select></label></div></div>')


def org_actions(ctx: Ctx) -> str:
    return (f'<a class="btn btn--ghost" href="{ctx.d("import-csv")}">{icon("upload")}Import</a><a class="btn btn--ghost" href="{ctx.d("export")}">{icon("download")}Export</a>'
            f'<a class="btn btn--primary" href="{ctx.p("organization-edit")}">{icon("plus")}New</a>')


def organizations(ctx: Ctx):
    s = ctx.state
    h = header("Organizations", "19 tracked · 12 verified · 7 unverified", org_actions(ctx))
    if s == "loading":
        inner = header_skeleton(title="Organizations") + org_toolbar(ctx, disabled=True) + skeleton_cards(6)
        return dict(description="Organisations list loading; six skeleton cards in the final layout.", body=main_wrap(ctx, "organizations", inner), notes=[])
    if s == "empty":
        inner = header("Organizations", "Nothing tracked yet", org_actions(ctx)) + empty(ctx, "building", "No organisations yet", "Add the first one by hand, import a CSV, or let a research run find them.", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a><a class="btn" href="{ctx.p("organization-edit")}">Add by hand</a>')
        return dict(description="First-run empty state for organisations with the one next action.", body=main_wrap(ctx, "organizations", inner, unread=0), notes=[])
    if s == "error":
        return dict(description="Organisations failed to load; chrome stays, retry offered.", body=main_wrap(ctx, "organizations", h + error_block(ctx, "organisations", back=ctx.p("field"))), notes=[])
    if s == "no-results":
        inner = h + org_toolbar(ctx, "youth hackathon", ["Moonshot", "Verified"]) + empty(ctx, "filter", "Nothing matches", "No organisation matches “youth hackathon” with these filters.", f'<a class="btn" href="{ctx.p("organizations")}">Clear filters</a><a class="btn btn--ghost" href="{ctx.d("run-research")}">Ask the web instead</a>', compact=True)
        return dict(description="Filters active with no matching organisations; filters remain visible and clearable.", body=main_wrap(ctx, "organizations", inner), notes=[])
    if s == "long":
        rows = [org_card(ctx, o, i) for i, o in enumerate(ORGS)]
        for j, name in enumerate(EXTRA_ORGS[:11]):
            rows.append(org_card(ctx, dict(ORGS[j % len(ORGS)], verified="pending"), len(ORGS) + j, name=name, mark="".join(w[0] for w in name.split()[:2]).upper(), meta="Unverified · imported from CSV", tag_list=["Imported"]))
        pag = (f'<nav class="cluster cluster--between" aria-label="Pagination" style="margin-top:var(--space-8);"><span class="text-caption">Showing 1–25 of 1,284</span><ul class="pagination">'
               f'<li><a href="#" aria-disabled="true" aria-label="Previous page">‹</a></li><li><a href="#" aria-current="page">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><span aria-hidden="true">…</span></li><li><a href="#">52</a></li><li><a href="#" aria-label="Next page">›</a></li></ul></nav>')
        inner = header("Organizations", "1,284 tracked · 412 verified · 872 unverified", org_actions(ctx)) + org_toolbar(ctx) + f'<div class="entity-list">{"".join(rows)}</div>' + pag
        return dict(description="A large imported catalogue: 1,284 organisations, paginated 25 per page.", body=main_wrap(ctx, "organizations", inner), notes=[note("Beyond 200 rows the list virtualises; pagination stays for deep links.", "top: 5rem; right: 1rem;")])
    if s == "selected":
        rows = "".join(org_card(ctx, o, i, checkbox=True, checked=i in (0, 1, 6)) for i, o in enumerate(ORGS))
        bar = (f'<div class="select-bar" role="region" aria-label="3 organisations selected"><strong>3 selected</strong><span class="topbar__spacer"></span>'
               f'<button class="btn btn--sm" type="button">Tag</button><a class="btn btn--sm" href="{ctx.d("export")}">Export 3</a><button class="btn btn--sm" type="button">Archive</button><button class="btn btn--sm btn--ghost" type="button" aria-label="Clear selection">{icon("close", "icon icon--sm")}</button></div>')
        inner = h + org_toolbar(ctx) + f'<div class="entity-list">{rows}</div>' + bar
        return dict(description="Three organisations selected with the bulk action bar visible.", body=main_wrap(ctx, "organizations", inner), notes=[note("Checkboxes appear on hover, focus and whenever one is checked; always visible on touch.", "top: 5rem; right: 1rem;")])
    if s == "edge":
        rows = [org_card(ctx, ORGS[0], 0, name="The International Fellowship of Evangelical Students Global Youth, Technology and Artificial Intelligence Working Group", mark="IF", meta="Alliance · Oxford · 9,999 chapters", tag_list=["AI", "Youth", "Moonshot", "Scripture", "Research", "Community", "Digital", "Translation", "Mental health"]),
                org_card(ctx, dict(ORGS[1], verified="conflict"), 1, name="مؤسسة الشباب المسيحي للتقنية", mark="", meta="Ministry · عمّان · 1,204 students", tag_list=["Youth"]),
                org_card(ctx, ORGS[2], 2, name="Ōkami Kyōkai Seinen-bu (大神教会青年部)", mark="OK", meta="Ministry · 東京 · 12 staff", tag_list=[]),
                org_card(ctx, ORGS[3], 3, name="X", mark="X", meta="Unknown · — · —", tag_list=["Imported"])]
        inner = header("Organizations", "1,284 tracked · 412 verified · 872 unverified", org_actions(ctx)) + org_toolbar(ctx) + f'<div class="entity-list">{"".join(rows)}</div>'
        return dict(description="Edge content: a very long name, an RTL name without a mark, CJK script, nine tags and a one-letter name.", body=main_wrap(ctx, "organizations", inner),
                    notes=[note("Long names wrap; they never truncate without a title. A missing mark leaves an empty tile rather than a broken image. Conflict means two sources disagree.", "top: 5rem; right: 1rem;")])
    rows = "".join(org_card(ctx, o, i, checkbox=True) for i, o in enumerate(ORGS))
    inner = h + org_toolbar(ctx) + f'<div class="entity-list">{rows}</div>'
    return dict(description="Organisations list, sorted by impact, with filters and bulk-select checkboxes.", body=main_wrap(ctx, "organizations", inner),
                notes=[note("Cards lift on hover with a spring curve (linear()). Entrance is staggered 40 ms per card via --i.", "top: 5rem; right: 1rem;")])


def org_facts(o: dict) -> str:
    site = f'<a href="https://{o["site"]}" target="_blank" rel="noopener">{o["site"]}{icon("external", "icon icon--sm")}</a>'
    place = ", ".join(x for x in (o["city"], o["country"]) if x)
    return (f'<dl class="facts"><div class="fact"><dt>Type</dt><dd>{o["kind"]}</dd></div><div class="fact"><dt>Founded</dt><dd>{o["founded"]}</dd></div><div class="fact"><dt>Base</dt><dd>{place}</dd></div>'
            f'<div class="fact"><dt>Reach</dt><dd>{o["reach"]}</dd></div><div class="fact"><dt>Website</dt><dd>{site}</dd></div><div class="fact"><dt>Status</dt><dd>{verify(o["verified"])}</dd></div></dl>')


def sources_list(items: list[tuple[str, str, str]]) -> str:
    return "".join(f'<div class="source">{icon("link", "icon icon--sm text-subtle")}<div><a href="https://{host}" target="_blank" rel="noopener">{title}</a><div class="source__host">{host} · {when}</div></div></div>' for title, host, when in items)


def organization(ctx: Ctx):
    s = ctx.state
    o = ORG_BY_ID["faithtech"]
    cr = crumbs([("Organizations", ctx.p("organizations")), (o["name"], None)])
    if s == "loading":
        inner = cr + header_skeleton() + '<div class="detail"><div class="stack" style="gap:var(--space-8);">' + skeleton_lines(4) + skeleton_cards(2, with_mark=False) + '</div><div>' + skeleton_lines(6, ("8rem", "12rem")) + "</div></div>"
        return dict(description="Organisation detail loading with the two-column skeleton.", body=main_wrap(ctx, "organizations", f'<div aria-busy="true" aria-label="Loading organisation">{inner}</div>'), notes=[])
    if s == "error":
        return dict(description="Organisation detail failed to load.", body=main_wrap(ctx, "organizations", cr + header("Organization") + error_block(ctx, "this organisation", back=ctx.p("organizations"))), notes=[])
    archived = s == "read-only"
    edge = s == "edge"
    name = "The International Fellowship of Evangelical Students Global Youth, Technology and Artificial Intelligence Working Group" if edge else o["name"]
    if s == "empty":
        o2 = dict(o, name="Kingdom Code", mark="KC", summary="", verified="pending", city="London", country="United Kingdom", founded="2014", site="kingdomcode.org.uk", reach="—", kind="Community", tags=["Community"])
        head = header(o2["name"], "Added 2 minutes ago by " + ME["name"], f'<a class="btn btn--ghost" href="{ctx.p("organization-edit")}">{icon("edit")}Edit</a><a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Research this org</a>', cr)
        mainc = (f'<div class="stack" style="gap:var(--space-12);">'
                 + '<section><h2 class="section__title">What they\'re doing</h2>' + empty(ctx, "list", "Nothing recorded yet", "A research run fills this in from the web, or add a line by hand.", f'<a class="btn" href="{ctx.p("organization-edit")}">Add by hand</a>', compact=True) + "</section>"
                 + '<section><h2 class="section__title">People</h2>' + empty(ctx, "people", "No people yet", "Who leads this?", f'<a class="btn" href="{ctx.d("add-person")}">{icon("plus")}Add person</a>', compact=True) + "</section>"
                 + '<section><h2 class="section__title">Problems</h2>' + empty(ctx, "target", "Not linked to a problem", "Link it to the problem it is working on.", f'<a class="btn" href="{ctx.d("link-problem")}">{icon("link")}Link problem</a>', compact=True) + "</section></div>")
        aside = f'<aside class="detail__aside"><section>{org_facts(o2)}</section></aside>'
        return dict(description="A just-created organisation with no initiatives, people, problems or sources yet.", body=main_wrap(ctx, "organizations", head + f'<div class="detail">{mainc}{aside}</div>'), notes=[])
    actions = ("" if archived else f'<a class="btn btn--ghost" href="{ctx.p("organization-edit")}">{icon("edit")}Edit</a><a class="btn btn--ghost" href="{ctx.d("delete-organization")}" style="color:var(--color-danger-fg);">{icon("trash")}Delete</a><a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Research</a>')
    if archived:
        actions = '<button class="btn btn--primary" type="button">Restore</button>'
    banner = alert("warning", "Archived by Hannah Okafor · Mon 13 Oct", "Read-only until restored.", dismiss=False) if archived else ""
    doing = "".join(f'<li class="people-row" style="display:block;">{d}</li>' for d in o["doing"])
    if edge:
        doing += '<li class="people-row" style="display:block;">Launching a 14-language, 40-country, 2,000-volunteer, AI-assisted youth discipleship curriculum with a 2033 deadline and a $12,400,000 budget that wraps onto several lines without truncation</li>'
    people = "".join(person_row(ctx, PERSON_BY_ID[p], i) for i, p in enumerate(o["people"]))
    if edge:
        people += person_row(ctx, PERSON_BY_ID["james-kelly"], 1, name="Dr. Maria-Theresa von Hohenlohe-Langenburg-Schillingsfürst", role="Interim Co-Executive Director, Global Youth & AI (acting)")
    probs = "".join(problem_row(ctx, PROBLEM_BY_ID[p], i) for i, p in enumerate(o["problems"]))
    add_person = "" if archived else f'<a class="btn btn--sm" href="{ctx.d("add-person")}">{icon("plus")}Add</a>'
    link_problem = "" if archived else f'<a class="btn btn--sm" href="{ctx.d("link-problem")}">{icon("link")}Link</a>'
    mainc = (f'<div class="stack" style="gap:var(--space-12);"><section><h2 class="section__title">What they\'re doing</h2><ul class="list" style="font:var(--text-body-lg);">{doing}</ul></section>'
             f'<section><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">People</h2>{add_person}</div><div class="entity-list">{people}</div></section>'
             f'<section><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Problems</h2>{link_problem}</div><div class="entity-list">{probs}</div></section>'
             f'<section><h2 class="section__title">Sources</h2>{sources_list([("Canada\'s FaithTech aims to redeem technology", "ministrywatch.com", "Verified Tue 14 Oct"), ("Using technology for missions", "mnnonline.org", "Verified Tue 14 Oct"), ("What is redemptive technology?", "letu.edu", "Added Mon 13 Oct")])}</section></div>')
    timeline = ('<ul class="timeline"><li><time>Today 12:04</time><span>Run #48 looking for LinkedIn profiles</span></li><li><time>Yesterday</time><span>Run #47 added 2 initiatives</span></li><li><time>Tue 14 Oct</time><span>Tobias verified 2 sources</span></li><li><time>Mon 13 Oct</time><span>Created by Naomi</span></li></ul>')
    aside = f'<aside class="detail__aside"><section>{org_facts(o)}</section><section><h2 class="section__title">Activity</h2>{timeline}</section></aside>'
    sub = o["summary"] if not edge else "Alliance · Oxford · 9,999 chapters · a subtitle long enough to wrap on a phone and still read as one line of numbers that matter"
    head = (f'{cr}<div class="page-header rise"><div class="cluster" style="align-items:flex-start;gap:var(--space-6);"><span class="mark mark--lg" aria-hidden="true">{o["mark"]}</span><div><div class="cluster" style="gap:var(--space-3);"><h1>{name}</h1>{verify(o["verified"])}</div><p class="subtitle">{sub}</p>{tags(o["tags"])}</div></div><div class="cluster">{actions}</div></div>')
    card_cls = ' card--archived' if archived else ""
    body = main_wrap(ctx, "organizations", banner + head + f'<div class="detail{card_cls}" style="padding:0;border:0;background:none;">{mainc}{aside}</div>')
    desc = {"default": "FaithTech detail: initiatives, people, linked problems, sources and facts.", "read-only": "An archived organisation: editing affordances removed, restore offered.",
            "edge": "Edge content on the detail page: very long organisation and person names, long initiative text."}[s]
    notes = [note("The h1 carries view-transition-name: page-title, so navigating from the list morphs the name into place (Chrome 126+ cross-document view transitions).", "top: 5rem; right: 1rem;")] if s == "default" else []
    return dict(description=desc, body=body, notes=notes)


def org_form(ctx: Ctx, s: str) -> str:
    o = ORG_BY_ID["faithtech"]
    invalid, busy = s == "invalid", s == "submitting"
    summary = form_summary([("org-name", "Enter a name"), ("org-site", "Enter a website like example.org")]) if invalid else ""
    saved = f'<div class="inline-status inline-status--success" role="status">{icon("success", "icon icon--sm")} Saved · just now</div>' if s == "success" else ""
    f = (summary
         + field("org-name", "Name", text_input("org-name", "" if invalid else o["name"], invalid=invalid, readonly=busy, extra="autofocus"), error="Enter a name" if invalid else "")
         + '<div class="grid" style="--layout-columns:2;">'
         + field("org-kind", "Type", select("org-kind", ["Community", "Platform", "Ministry", "Alliance", "Movement", "Product", "Startup", "Research", "Nonprofit"], o["kind"], disabled=busy))
         + field("org-founded", "Founded", text_input("org-founded", o["founded"], readonly=busy, extra='inputmode="numeric"'), optional=True)
         + field("org-city", "City", text_input("org-city", o["city"], readonly=busy), optional=True)
         + field("org-country", "Country", text_input("org-country", o["country"], readonly=busy))
         + "</div>"
         + field("org-site", "Website", text_input("org-site", "faithtech" if invalid else o["site"], "url", invalid=invalid, readonly=busy), error="Enter a website like example.org" if invalid else "")
         + field("org-summary", "Summary", textarea("org-summary", o["summary"], readonly=busy), help_text="One sentence. The textarea grows with the text (field-sizing: content).")
         + f'<fieldset><legend>Tags</legend><div class="cluster">' + "".join(f'<label class="chip" style="gap:var(--space-2);"><input type="checkbox" name="tags" value="{t}"{" checked" if t in o["tags"] else ""}{" disabled" if busy else ""} style="accent-color:var(--color-accent);margin:0;"> {t}</label>' for t in ["AI", "Youth", "Moonshot", "Scripture", "Research", "Community", "Digital"]) + "</div></fieldset>"
         + f'<div class="form-actions" style="justify-content:space-between;align-items:center;">{saved}<span class="topbar__spacer"></span><a class="btn btn--ghost" href="{ctx.d("unsaved-changes") if s == "default" else ctx.p("organization")}">Cancel</a>'
         + (f'<button class="btn btn--primary" type="submit" aria-busy="true">Save</button>' if busy else '<button class="btn btn--primary" type="submit">Save</button>') + "</div>")
    return f'<form class="stack card" style="gap:var(--space-6);padding:var(--space-8);max-width:44rem;" novalidate>{f}</form>'


def organization_edit(ctx: Ctx):
    s = ctx.state
    cr = crumbs([("Organizations", ctx.p("organizations")), ("FaithTech", ctx.p("organization")), ("Edit", None)])
    if s == "loading":
        inner = cr + header_skeleton(False, title="Edit organization") + '<div class="card" style="max-width:44rem;" aria-busy="true" aria-label="Loading form">' + "".join('<span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-4);"></span>' for _ in range(5)) + "</div>"
        return dict(description="Edit form loading; skeleton fields in the final layout.", body=main_wrap(ctx, "organizations", inner), notes=[])
    if s == "error":
        return dict(description="Edit form could not load the organisation.", body=main_wrap(ctx, "organizations", cr + header("Edit organization") + error_block(ctx, "the form", back=ctx.p("organization"))), notes=[])
    h = header("Edit organization", "FaithTech · last saved Tue 14 Oct by Tobias Mwangi", crumbs=cr)
    desc = {"default": "Edit form for FaithTech with all fields populated.", "invalid": "Submitted with a blank name and malformed website; summary plus inline errors.",
            "submitting": "Saving: fields read-only, Save busy, no layout shift.", "success": "Saved: inline status with a timestamp; the form stays editable."}[s]
    notes = []
    if s == "default":
        notes = [note("New organisation uses this same page with blank fields and the title “New organization”. Leaving with unsaved changes opens the Unsaved changes dialog.", "top: 5rem; right: 1rem;")]
    if s == "invalid":
        notes = [note("Focus moves to the summary on submit; each link focuses its field.", "top: 5rem; right: 1rem;")]
    return dict(description=desc, body=main_wrap(ctx, "organizations", h + org_form(ctx, s)), notes=notes)


# ---------------------------------------------------------------------------
# People
# ---------------------------------------------------------------------------
def people_toolbar(ctx: Ctx, query: str = "", active=(), disabled: bool = False) -> str:
    chips = "".join(f'<button class="chip" type="button" aria-pressed="{"true" if c in active else "false"}"{" disabled" if disabled else ""}>{c}</button>' for c in ["On LinkedIn", "No LinkedIn"])
    return (f'<div class="toolbar rise" style="--i:1"><form class="search" role="search" style="flex:1 1 16rem;max-width:24rem;"><label class="visually-hidden" for="q">Search people</label>{icon("search")}<input class="input" id="q" type="search" value="{query}" placeholder="Search"{" disabled" if disabled else ""}></form><div class="cluster">{chips}</div></div>')


def people(ctx: Ctx):
    s = ctx.state
    actions = f'<a class="btn btn--primary" href="{ctx.p("person-edit")}">{icon("plus")}New</a>'
    h = header("People", "16 people · 8 on LinkedIn", actions)
    if s == "loading":
        return dict(description="People list loading.", body=main_wrap(ctx, "people", header_skeleton(title="People") + people_toolbar(ctx, disabled=True) + skeleton_cards(6)), notes=[])
    if s == "empty":
        inner = header("People", "Nobody yet", actions) + empty(ctx, "people", "No people yet", "People arrive with organisations. Add one or run research.", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a><a class="btn" href="{ctx.p("person-edit")}">Add by hand</a>')
        return dict(description="Empty people list.", body=main_wrap(ctx, "people", inner, unread=0), notes=[])
    if s == "error":
        return dict(description="People failed to load.", body=main_wrap(ctx, "people", h + error_block(ctx, "people", back=ctx.p("field"))), notes=[])
    if s == "no-results":
        inner = h + people_toolbar(ctx, "gelsinger", ["No LinkedIn"]) + empty(ctx, "filter", "Nothing matches", "No person matches “gelsinger” without a LinkedIn profile.", f'<a class="btn" href="{ctx.p("people")}">Clear filters</a>', compact=True)
        return dict(description="People filters with no matches.", body=main_wrap(ctx, "people", inner), notes=[])
    rows = "".join(person_row(ctx, p, i) for i, p in enumerate(PEOPLE))
    if s == "long":
        extra = "".join(person_row(ctx, PEOPLE[i % len(PEOPLE)], 16 + i, name=f"{n}", role="Staff") for i, n in enumerate(["Grace Adebayo", "Samuel Ortiz", "Lena Fischer", "Daniel Park", "Ruth Mbeki", "Caleb Nguyen", "Abigail Rossi", "Isaac Haddad", "Miriam Cohen"]))
        pag = ('<nav class="cluster cluster--between" aria-label="Pagination" style="margin-top:var(--space-8);"><span class="text-caption">Showing 1–25 of 3,412</span><ul class="pagination"><li><a href="#" aria-disabled="true" aria-label="Previous page">‹</a></li><li><a href="#" aria-current="page">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><span aria-hidden="true">…</span></li><li><a href="#">137</a></li><li><a href="#" aria-label="Next page">›</a></li></ul></nav>')
        inner = header("People", "3,412 people · 1,208 on LinkedIn", actions) + people_toolbar(ctx) + f'<div class="entity-list">{rows}{extra}</div>' + pag
        return dict(description="Thousands of people, paginated.", body=main_wrap(ctx, "people", inner), notes=[])
    return dict(description="People list with role, organisation and LinkedIn link.", body=main_wrap(ctx, "people", h + people_toolbar(ctx) + f'<div class="entity-list">{rows}</div>'),
                notes=[note("LinkedIn links open a people search for the name and organisation; the product never stores a guessed profile URL.", "top: 5rem; right: 1rem;")])


def person(ctx: Ctx):
    s = ctx.state
    p = PERSON_BY_ID["pat-gelsinger"]
    o = ORG_BY_ID[p["org"]]
    cr = crumbs([("People", ctx.p("people")), (p["name"], None)])
    if s == "loading":
        inner = cr + header_skeleton() + '<div class="detail"><div>' + skeleton_lines(5) + '</div><div>' + skeleton_lines(5, ("8rem", "12rem")) + "</div></div>"
        return dict(description="Person detail loading.", body=main_wrap(ctx, "people", f'<div aria-busy="true" aria-label="Loading person">{inner}</div>'), notes=[])
    if s == "error":
        return dict(description="Person detail failed to load.", body=main_wrap(ctx, "people", cr + header("Person") + error_block(ctx, "this person", back=ctx.p("people"))), notes=[])
    if s == "empty":
        p = PERSON_BY_ID["newt-crenshaw"]; o = ORG_BY_ID[p["org"]]
        head = header(p["name"], f'{p["role"]} · <a href="{ctx.p("organization")}">{o["name"]}</a>', f'<a class="btn btn--ghost" href="{ctx.p("person-edit")}">{icon("edit")}Edit</a><a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("linkedin")}Find on LinkedIn</a>', crumbs([("People", ctx.p("people")), (p["name"], None)]))
        mainc = ('<div class="stack" style="gap:var(--space-12);"><section><h2 class="section__title">About</h2>' + empty(ctx, "people", "Nothing verified yet", "One unverified finding from 2019. Run research to confirm the role and find a profile.", f'<a class="btn" href="{ctx.d("run-research")}">{icon("sparkle")}Research this person</a>', compact=True) + "</section></div>")
        aside = f'<aside class="detail__aside"><dl class="facts"><div class="fact"><dt>Organisation</dt><dd><a href="{ctx.p("organization")}">{o["name"]}</a></dd></div><div class="fact"><dt>LinkedIn</dt><dd><span class="text-subtle">None yet</span></dd></div><div class="fact"><dt>Sources</dt><dd>1 · unverified</dd></div></dl></aside>'
        return dict(description="A person with no verified facts and no LinkedIn profile yet.", body=main_wrap(ctx, "people", head + f'<div class="detail">{mainc}{aside}</div>'), notes=[])
    edge = s == "edge"
    name = "Dr. Maria-Theresa von Hohenlohe-Langenburg-Schillingsfürst" if edge else p["name"]
    role = "Interim Co-Executive Director, Global Youth & AI (acting) · Chair, Flourishing AI Standards Board · Board member, 4 organisations" if edge else p["role"]
    actions = f'<a class="btn btn--ghost" href="{ctx.p("person-edit")}">{icon("edit")}Edit</a><a class="btn btn--ghost" href="{ctx.d("delete-person")}" style="color:var(--color-danger-fg);">{icon("trash")}Delete</a><a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Research</a>'
    head = (f'{cr}<div class="page-header rise"><div class="cluster" style="align-items:flex-start;gap:var(--space-6);">{avatar("MT" if edge else p["initials"], "avatar avatar--lg")}<div><div class="cluster" style="gap:var(--space-3);"><h1>{name}</h1>{verify("verified")}</div><p class="subtitle">{role} · <a href="{ctx.p("organization")}">{o["name"]}</a></p></div></div><div class="cluster">{actions}</div></div>')
    orgs = org_card(ctx, o, 0)
    if edge:
        orgs += "".join(org_card(ctx, ORGS[i], i) for i in (0, 2, 4))
    mainc = (f'<div class="stack" style="gap:var(--space-12);"><section><h2 class="section__title">About</h2><p style="font:var(--text-body-lg);">{p["bio"]}</p></section>'
             f'<section><h2 class="section__title">Organisations</h2><div class="entity-list">{orgs}</div></section>'
             f'<section><h2 class="section__title">Sources</h2>{sources_list([("Former Intel CEO Pat Gelsinger expands role at Gloo", "christianpost.com", "Verified Tue 14 Oct"), ("Former Intel executive joins Gloo", "ministrywatch.com", "Verified Tue 14 Oct"), ("Gelsinger hopes to make AI a force for good and for God", "baptiststandard.com", "Added Mon 13 Oct")])}</section></div>')
    aside = (f'<aside class="detail__aside"><dl class="facts"><div class="fact"><dt>Organisation</dt><dd><a href="{ctx.p("organization")}">{o["name"]}</a></dd></div><div class="fact"><dt>Since</dt><dd>{p["since"]}</dd></div>'
             f'<div class="fact"><dt>LinkedIn</dt><dd>{linkedin_cell(ctx, p)}</dd></div><div class="fact"><dt>Sources</dt><dd>3 · 2 verified</dd></div></dl>'
             '<section><h2 class="section__title">Activity</h2><ul class="timeline"><li><time>Tue 14 Oct</time><span>LinkedIn added by Priya</span></li><li><time>Mon 13 Oct</time><span>Run #46 added role change</span></li></ul></section></aside>')
    desc = "Pat Gelsinger: role, bio, organisations, sources and a LinkedIn link." if not edge else "Edge content: a very long name, three stacked roles and four organisations."
    return dict(description=desc, body=main_wrap(ctx, "people", head + f'<div class="detail">{mainc}{aside}</div>'), notes=[])


def person_form(ctx: Ctx, s: str) -> str:
    p = PERSON_BY_ID["pat-gelsinger"]
    invalid, busy = s == "invalid", s == "submitting"
    summary = form_summary([("person-name", "Enter a name"), ("person-linkedin", "Enter a LinkedIn profile URL like linkedin.com/in/name")]) if invalid else ""
    saved = f'<div class="inline-status inline-status--success" role="status">{icon("success", "icon icon--sm")} Saved · just now</div>' if s == "success" else ""
    f = (summary
         + field("person-name", "Name", text_input("person-name", "" if invalid else p["name"], invalid=invalid, readonly=busy, extra="autofocus"), error="Enter a name" if invalid else "")
         + field("person-role", "Role", text_input("person-role", p["role"], readonly=busy))
         + field("person-org", "Organisation", select("person-org", [o["name"] for o in ORGS], "Gloo", disabled=busy))
         + field("person-linkedin", "LinkedIn", text_input("person-linkedin", "pat gelsinger" if invalid else "", "url", invalid=invalid, readonly=busy, placeholder="linkedin.com/in/"), help_text="Paste the profile URL. Leave blank to let research find it.", error="Enter a LinkedIn profile URL like linkedin.com/in/name" if invalid else "", optional=True)
         + field("person-bio", "Bio", textarea("person-bio", p["bio"], readonly=busy), optional=True)
         + f'<div class="form-actions" style="justify-content:space-between;align-items:center;">{saved}<span class="topbar__spacer"></span><a class="btn btn--ghost" href="{ctx.p("person")}">Cancel</a>'
         + ('<button class="btn btn--primary" type="submit" aria-busy="true">Save</button>' if busy else '<button class="btn btn--primary" type="submit">Save</button>') + "</div>")
    return f'<form class="stack card" style="gap:var(--space-6);padding:var(--space-8);max-width:44rem;" novalidate>{f}</form>'


def person_edit(ctx: Ctx):
    s = ctx.state
    cr = crumbs([("People", ctx.p("people")), ("Pat Gelsinger", ctx.p("person")), ("Edit", None)])
    if s == "loading":
        inner = cr + header_skeleton(False, title="Edit person") + '<div class="card" style="max-width:44rem;" aria-busy="true" aria-label="Loading form">' + "".join('<span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-4);"></span>' for _ in range(4)) + "</div>"
        return dict(description="Person edit form loading.", body=main_wrap(ctx, "people", inner), notes=[])
    if s == "error":
        return dict(description="Person edit form failed to load.", body=main_wrap(ctx, "people", cr + header("Edit person") + error_block(ctx, "the form", back=ctx.p("person"))), notes=[])
    h = header("Edit person", "Pat Gelsinger · Gloo", crumbs=cr)
    desc = {"default": "Edit form for a person.", "invalid": "Submitted with a blank name and a LinkedIn value that is not a URL.", "submitting": "Saving the person.", "success": "Person saved with inline status."}[s]
    return dict(description=desc, body=main_wrap(ctx, "people", h + person_form(ctx, s)), notes=[note("New person uses this same page with blank fields.", "top: 5rem; right: 1rem;")] if s == "default" else [])


# ---------------------------------------------------------------------------
# Problems
# ---------------------------------------------------------------------------
def problems(ctx: Ctx):
    s = ctx.state
    actions = f'<a class="btn btn--primary" href="{ctx.p("problem-edit")}">{icon("plus")}New</a>'
    chips = '<div class="toolbar rise" style="--i:1"><div class="cluster"><button class="chip" type="button" aria-pressed="true">All</button><button class="chip" type="button" aria-pressed="false">Tracked</button><button class="chip" type="button" aria-pressed="false">Watching</button></div><span class="text-caption">Impact = reach × severity × tractability</span></div>'
    h = header("Problems", "9 ranked · illumiNations leads with 94", actions)
    if s == "loading":
        return dict(description="Problem ranking loading.", body=main_wrap(ctx, "problems", header_skeleton(title="Problems") + skeleton_cards(5, with_mark=False)), notes=[])
    if s == "empty":
        inner = header("Problems", "Nothing ranked yet", actions) + empty(ctx, "target", "No problems yet", "Name the moonshots you care about; research links organisations to them.", f'<a class="btn btn--primary" href="{ctx.p("problem-edit")}">{icon("plus")}Add a problem</a>')
        return dict(description="Empty problems list.", body=main_wrap(ctx, "problems", inner, unread=0), notes=[])
    if s == "error":
        return dict(description="Problems failed to load.", body=main_wrap(ctx, "problems", h + error_block(ctx, "problems", back=ctx.p("field"))), notes=[])
    if s == "no-results":
        chips2 = chips.replace('aria-pressed="true">All', 'aria-pressed="false">All').replace('aria-pressed="false">Watching', 'aria-pressed="true">Watching').replace("Impact = reach × severity × tractability", "")
        inner = h + chips2 + empty(ctx, "filter", "Nothing matches", "No problem is both “Watching” and tagged AI.", f'<a class="btn" href="{ctx.p("problems")}">Clear filters</a>', compact=True)
        return dict(description="Problem filters with no matches.", body=main_wrap(ctx, "problems", inner), notes=[])
    rows = "".join(problem_row(ctx, p, i) for i, p in enumerate(PROBLEMS))
    return dict(description="Problems ranked by impact score with the organisations working on each.", body=main_wrap(ctx, "problems", h + chips + f'<div class="entity-list">{rows}</div>'),
                notes=[note("Score rings animate from 0 on entry using a registered @property (--score) and a conic-gradient; rank 1 uses the warning hue as gold.", "top: 5rem; right: 1rem;")])


def problem(ctx: Ctx):
    s = ctx.state
    pr = PROBLEM_BY_ID["every-language"]
    cr = crumbs([("Problems", ctx.p("problems")), (pr["title"], None)])
    if s == "loading":
        inner = cr + header_skeleton() + '<div class="detail"><div>' + skeleton_cards(2, with_mark=False) + '</div><div>' + skeleton_lines(5, ("8rem", "12rem")) + "</div></div>"
        return dict(description="Problem detail loading.", body=main_wrap(ctx, "problems", f'<div aria-busy="true" aria-label="Loading problem">{inner}</div>'), notes=[])
    if s == "error":
        return dict(description="Problem detail failed to load.", body=main_wrap(ctx, "problems", cr + header("Problem") + error_block(ctx, "this problem", back=ctx.p("problems"))), notes=[])
    actions = f'<a class="btn btn--ghost" href="{ctx.p("problem-edit")}">{icon("edit")}Edit</a><a class="btn btn--ghost" href="{ctx.d("delete-problem")}" style="color:var(--color-danger-fg);">{icon("trash")}Delete</a><a class="btn btn--primary" href="{ctx.d("link-problem")}">{icon("link")}Link organisation</a>'
    if s == "empty":
        pr2 = dict(pr, title="Youth mental health in East Africa", score=0, rank=None, reach="—", severity="High", tractability="—", status="Watching", summary="Added from a conversation; no organisation linked yet.")
        head = f'{crumbs([("Problems", ctx.p("problems")), (pr2["title"], None)])}<div class="page-header rise"><div class="cluster" style="align-items:flex-start;gap:var(--space-6);"><span class="score score--lg" style="--score:0" role="img" aria-label="No impact score yet"><span>—</span></span><div><h1>{pr2["title"]}</h1><p class="subtitle">{pr2["summary"]}</p></div></div><div class="cluster">{actions}</div></div>'
        mainc = '<section><h2 class="section__title">Organisations</h2>' + empty(ctx, "building", "Nobody linked yet", "Link an organisation, or let research find who is working on this.", f'<a class="btn btn--primary" href="{ctx.d("link-problem")}">{icon("link")}Link organisation</a><a class="btn" href="{ctx.d("run-research")}">Ask the web</a>', compact=True) + "</section>"
        aside = f'<aside class="detail__aside"><dl class="facts"><div class="fact"><dt>Reach</dt><dd>Not set</dd></div><div class="fact"><dt>Severity</dt><dd>High</dd></div><div class="fact"><dt>Tractability</dt><dd>Not set</dd></div><div class="fact"><dt>Status</dt><dd>Watching</dd></div></dl><p class="text-caption">The score appears once reach and tractability are set.</p></aside>'
        return dict(description="A problem with no organisations linked and no score yet.", body=main_wrap(ctx, "problems", head + f'<div class="detail">{mainc}{aside}</div>'), notes=[])
    head = f'{cr}<div class="page-header rise"><div class="cluster" style="align-items:flex-start;gap:var(--space-6);">{score(pr["score"], "score--lg", rank=1)}<div><h1>{pr["title"]}</h1><p class="subtitle">{pr["summary"]}</p></div></div><div class="cluster">{actions}</div></div>'
    orgs = "".join(org_card(ctx, ORG_BY_ID[o], i) for i, o in enumerate(pr["orgs"]))
    orgs += org_card(ctx, ORGS[5], 1)
    mainc = (f'<div class="stack" style="gap:var(--space-12);"><section><h2 class="section__title">Organisations</h2><div class="entity-list">{orgs}</div></section>'
             '<section><h2 class="section__title">Milestones</h2><ul class="timeline"><li><time>2033</time><span>All Access Goals deadline: full Bible for 95% of people</span></li><li><time>2021</time><span>I Want to Know campaign launched</span></li><li><time>2010</time><span>ETEN Alliance formed</span></li></ul></section>'
             f'<section><h2 class="section__title">Sources</h2>{sources_list([("Vision, goals and the alliance", "wycliffe.net", "Verified Thu 9 Oct"), ("Bible translators launch campaign for every language by 2033", "religionnews.com", "Verified Thu 9 Oct"), ("illumiNations, Bible and AI", "sobicain.org", "Added Thu 9 Oct · single source")])}</section></div>')
    aside = (f'<aside class="detail__aside"><dl class="facts"><div class="fact"><dt>Rank</dt><dd>1 of 9</dd></div><div class="fact"><dt>Reach</dt><dd>{pr["reach"]}</dd></div><div class="fact"><dt>Severity</dt><dd>{pr["severity"]}</dd></div><div class="fact"><dt>Tractability</dt><dd>{pr["tractability"]}</dd></div><div class="fact"><dt>Status</dt><dd>{pr["status"]}</dd></div></dl>'
             '<section><h2 class="section__title">Activity</h2><ul class="timeline"><li><time>Thu 9 Oct</time><span>Run #44 scored 94</span></li><li><time>Thu 9 Oct</time><span>Created by Elias</span></li></ul></section></aside>')
    return dict(description="The top-ranked problem: score, factors, organisations, milestones and sources.", body=main_wrap(ctx, "problems", head + f'<div class="detail">{mainc}{aside}</div>'), notes=[])


def problem_form(ctx: Ctx, s: str) -> str:
    pr = PROBLEM_BY_ID["every-language"]
    invalid, busy = s == "invalid", s == "submitting"
    summary = form_summary([("problem-title", "Enter a title"), ("problem-reach", "Enter who or how many this affects")]) if invalid else ""
    saved = f'<div class="inline-status inline-status--success" role="status">{icon("success", "icon icon--sm")} Saved · just now</div>' if s == "success" else ""
    f = (summary
         + field("problem-title", "Title", text_input("problem-title", "" if invalid else pr["title"], invalid=invalid, readonly=busy, extra="autofocus"), error="Enter a title" if invalid else "")
         + field("problem-summary", "Summary", textarea("problem-summary", pr["summary"], readonly=busy))
         + '<div class="grid" style="--layout-columns:3;">'
         + field("problem-reach", "Reach", text_input("problem-reach", "" if invalid else pr["reach"], invalid=invalid, readonly=busy), error="Enter who or how many this affects" if invalid else "")
         + field("problem-severity", "Severity", select("problem-severity", ["Low", "Medium", "High"], pr["severity"], disabled=busy))
         + field("problem-tractability", "Tractability", select("problem-tractability", ["Low", "Medium", "High"], pr["tractability"], disabled=busy))
         + "</div>"
         + field("problem-status", "Status", select("problem-status", ["Tracked", "Watching", "Archived"], pr["status"], disabled=busy))
         + f'<div class="form-actions" style="justify-content:space-between;align-items:center;">{saved}<span class="topbar__spacer"></span><a class="btn btn--ghost" href="{ctx.p("problem")}">Cancel</a>'
         + ('<button class="btn btn--primary" type="submit" aria-busy="true">Save</button>' if busy else '<button class="btn btn--primary" type="submit">Save</button>') + "</div>")
    return f'<form class="stack card" style="gap:var(--space-6);padding:var(--space-8);max-width:44rem;" novalidate>{f}</form>'


def problem_edit(ctx: Ctx):
    s = ctx.state
    cr = crumbs([("Problems", ctx.p("problems")), ("Scripture in every language by 2033", ctx.p("problem")), ("Edit", None)])
    if s == "loading":
        inner = cr + header_skeleton(False, title="Edit problem") + '<div class="card" style="max-width:44rem;" aria-busy="true" aria-label="Loading form">' + "".join('<span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-4);"></span>' for _ in range(4)) + "</div>"
        return dict(description="Problem edit form loading.", body=main_wrap(ctx, "problems", inner), notes=[])
    if s == "error":
        return dict(description="Problem edit form failed to load.", body=main_wrap(ctx, "problems", cr + header("Edit problem") + error_block(ctx, "the form", back=ctx.p("problem"))), notes=[])
    h = header("Edit problem", "Score recalculates on save", crumbs=cr)
    desc = {"default": "Edit form for a problem with the three scoring factors.", "invalid": "Submitted with a blank title and reach.", "submitting": "Saving the problem.", "success": "Problem saved; score recalculated."}[s]
    return dict(description=desc, body=main_wrap(ctx, "problems", h + problem_form(ctx, s)), notes=[note("New problem uses this same page with blank fields.", "top: 5rem; right: 1rem;")] if s == "default" else [])


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------
def answer_panel(ctx: Ctx, q: dict, items: list[tuple[str, str, str]], i: int = 0, failed: bool = False) -> str:
    if failed:
        body = alert("danger", "Couldn't load this answer", "The findings service didn't answer in time.", f'<a href="{ctx.p("questions", "partial")}">Retry</a>', role="alert", dismiss=False)
    else:
        lis = "".join(f'<li><a href="{href}">{label}</a><span class="answer__spacer"></span><span class="text-caption">{meta}</span></li>' for label, href, meta in items)
        body = f'<ol class="answer__list">{lis}</ol>'
    status = {"answered": "Answered", "partial": "Partial", "open": "Open"}[q["status"]]
    return (f'<section class="card answer rise" style="--i:{i}" id="{q["id"]}"><div class="cluster cluster--between"><span class="q-card__n">{q["n"]} · {status} · {q["sources"]} sources</span><a class="btn btn--sm btn--ghost" href="{ctx.d("run-research")}">{icon("refresh", "icon icon--sm")}Re-run</a></div>'
            f'<h2 class="answer__q">{q["text"]}</h2>{body}</section>')


def questions(ctx: Ctx):
    s = ctx.state
    h = header("Questions", "6 questions · 4 answered · 2 partial", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a>')
    if s == "loading":
        return dict(description="Questions loading.", body=main_wrap(ctx, "questions", header_skeleton(title="Questions") + '<div class="stack" style="gap:var(--space-6);">' + "".join(f'<div class="card answer" style="--i:{i}"><span class="skeleton skeleton--text" style="width:8rem"></span><span class="skeleton skeleton--title" style="width:60%;"></span>{skeleton_lines(3)}</div>' for i in range(3)) + "</div>"), notes=[])
    if s == "empty":
        inner = header("Questions", "Nothing answered yet", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a>') + '<div class="stack" style="gap:var(--space-6);">' + "".join(answer_panel(ctx, dict(q, status="open", sources=0), [("Run research to answer this", ctx.d("run-research"), "")], i) for i, q in enumerate(QUESTIONS)) + "</div>"
        return dict(description="All six questions open with no findings yet.", body=main_wrap(ctx, "questions", inner, unread=0), notes=[])
    if s == "error":
        return dict(description="Questions failed to load.", body=main_wrap(ctx, "questions", h + error_block(ctx, "the answers", back=ctx.p("field"))), notes=[])
    org = lambda oid, meta: (ORG_BY_ID[oid]["name"], ctx.p("organization"), meta)  # noqa: E731
    per = lambda pid: (PERSON_BY_ID[pid]["name"], ctx.p("person"), f'{PERSON_BY_ID[pid]["role"]} · {ORG_BY_ID[PERSON_BY_ID[pid]["org"]]["name"]}')  # noqa: E731
    panels = [
        answer_panel(ctx, QUESTIONS[0], [org("gloo", "AI · 140,000 leaders"), org("faithtech", "AI · 50+ cities"), org("creed", "AI · Gen Z app"), org("fuller-youth", "AI guidance for youth workers"), org("abs", "AI Bible assistant pilot"), org("indigitous", "AI chat for seekers")], 0),
        answer_panel(ctx, QUESTIONS[1], [org("illuminations", "2033 · every language"), org("onehope", "2033 · next 2B children"), org("lausanne", "2050 · Great Commission"), org("gloo", "Flourishing AI standard"), org("dare2share", "Every teen · unverified")], 1),
        answer_panel(ctx, QUESTIONS[2], [(PROBLEMS[0]["title"], ctx.p("problem"), "Score 94 · illumiNations"), (PROBLEMS[1]["title"], ctx.p("problem"), "Score 91 · OneHope"), (PROBLEMS[2]["title"], ctx.p("problem"), "Score 88 · Lausanne")], 2),
        answer_panel(ctx, QUESTIONS[3], [org("gloo", "Flourishing AI standards · Faith Assistant"), org("illuminations", "AI-assisted translation drafting"), org("faithtech", "AI trauma-healing sprint · Missional Tech Trends"), org("onehope", "Bible App for Kids · 165M installs")], 3),
        answer_panel(ctx, QUESTIONS[4], [per("pat-gelsinger"), per("scott-beck"), per("james-kelly"), per("rob-hoskins"), per("michael-oh"), per("kara-powell")], 4),
        answer_panel(ctx, QUESTIONS[5], [per("pat-gelsinger"), per("james-kelly"), per("michael-oh"), per("david-kinnaman"), ("8 more without LinkedIn", ctx.p("people"), "Run #48 in progress")], 5, failed=(s == "partial")),
    ]
    desc = "The six research questions with their current answers, each linking to the records behind it." if s == "default" else "Five answers loaded; the LinkedIn answer failed and can be retried alone."
    return dict(description=desc, body=main_wrap(ctx, "questions", h + '<div class="stack" style="gap:var(--space-6);">' + "".join(panels) + "</div>"), notes=[])


# ---------------------------------------------------------------------------
# Research
# ---------------------------------------------------------------------------
def research(ctx: Ctx):
    s = ctx.state
    run_btn = f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Run research</a>'
    h = header("Research", "48 runs · 1 running · 5 findings to review", run_btn)
    if s == "loading":
        return dict(description="Research runs loading.", body=main_wrap(ctx, "research", header_skeleton(title="Research") + skeleton_cards(4, with_mark=False)), notes=[])
    if s == "empty":
        inner = header("Research", "No runs yet", run_btn) + empty(ctx, "flask", "Ask the web", "Pick a question, choose sources and depth. Findings come back for you to accept or reject.", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Run the first research</a>')
        return dict(description="No research runs yet.", body=main_wrap(ctx, "research", inner, unread=0), notes=[])
    if s == "error":
        return dict(description="Research runs failed to load.", body=main_wrap(ctx, "research", h + error_block(ctx, "research runs", back=ctx.p("field"))), notes=[])
    if s == "running":
        r = RUNS[0]
        log = "".join(f'<li class="people-row" style="display:grid;grid-template-columns:4rem 1fr;gap:var(--space-4);font:var(--text-body-sm);"><time class="text-subtle">{t}</time><span>{m}</span></li>' for t, m in [("12:04:10", "Queued 8 people"), ("12:04:12", "Searching linkedin.com for “Mart Green ETEN”"), ("12:04:31", "2 sources found for Mart Green"), ("12:05:02", "Searching for “Adi Agrawal Creed”"), ("12:05:40", "1 source found for Adi Agrawal"), ("12:06:03", "Searching for “Jennifer Holloran American Bible Society”")])
        inner = (h + f'<section class="card rise" style="padding:var(--space-8);"><div class="cluster cluster--between"><div><div class="cluster" style="gap:var(--space-3);"><h2 style="font:var(--text-h3);">#{r["id"]} · {r["title"]}</h2>{run_status("running")}</div><p class="text-muted" style="margin-top:var(--space-2);">Started 12:04 by {r["by"]} · 3 of 8 people done · about 4 minutes left</p></div><button class="btn" type="button">Stop</button></div>'
                 f'<div class="progress" role="progressbar" aria-label="Run 48 progress" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" style="margin-top:var(--space-6);"><div class="progress__bar" style="--value:62%"></div></div>'
                 f'<ul class="list" style="margin-top:var(--space-6);" aria-live="polite" aria-label="Run log">{log}</ul></section>'
                 + '<section class="section"><h2 class="section__title">Earlier runs</h2><div class="entity-list">' + "".join(run_row(ctx, rr, i) for i, rr in enumerate(RUNS[1:])) + "</div></section>")
        return dict(description="A research run in progress with a live log and determinate progress.", body=main_wrap(ctx, "research", inner), notes=[note("Log lines stream in via a polite live region; the progress bar is determinate because the run knows its queue length. Findings appear as each item completes.", "top: 5rem; right: 1rem;")])
    if s == "review":
        inner = (h + '<section class="section" style="margin-top:0;"><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Findings to review</h2><span class="text-caption">Accept creates or updates the record · Reject keeps the source</span></div><div class="stack" style="gap:var(--space-4);">'
                 + "".join(finding_card(ctx, f, i) for i, f in enumerate(FINDINGS)) + "</div></section>")
        return dict(description="Findings from recent runs waiting for review, with accepted and rejected examples.", body=main_wrap(ctx, "research", inner), notes=[note("Accept and Reject are optimistic: the card fades and an undo toast appears for 30 s. Low-confidence findings carry the reason inline.", "top: 5rem; right: 1rem;")])
    inner = (h + f'<section><div class="cluster cluster--between" style="margin-bottom:var(--space-6);"><h2 class="section__title" style="margin:0;">Runs</h2><a href="{ctx.p("research", "review")}">5 findings to review</a></div><div class="entity-list">' + "".join(run_row(ctx, r, i) for i, r in enumerate(RUNS)) + "</div></section>")
    return dict(description="Research runs: one running, three done, one failed; findings to review linked.", body=main_wrap(ctx, "research", inner), notes=[])


# ---------------------------------------------------------------------------
# Map
# ---------------------------------------------------------------------------
WORLD_BOX = (-180, 180, -90, 90)  # lon0, lon1, lat0, lat1
GTA_BOX = (-79.85, -78.75, 43.42, 43.98)  # keep in step with BOX in gta_map.py, which draws the land
GTA_LABELS = [("Mississauga", -79.64, 43.56), ("Toronto", -79.40, 43.665), ("Oshawa", -78.86, 43.90)]


def project(lon: float, lat: float, box: tuple = WORLD_BOX) -> tuple[float, float]:
    lon0, lon1, lat0, lat1 = box
    return (lon - lon0) / (lon1 - lon0) * 100, (lat1 - lat) / (lat1 - lat0) * 100


def in_box(o: dict, box: tuple) -> bool:
    lon0, lon1, lat0, lat1 = box
    return o["lon"] is not None and lon0 <= o["lon"] <= lon1 and lat0 <= o["lat"] <= lat1


def pin(ctx: Ctx, o: dict, i: int, expanded: bool = False, box: tuple = WORLD_BOX) -> str:
    left, top = project(o["lon"], o["lat"], box)
    cls = "map__pin" + (" map__pin--unverified" if o["verified"] != "verified" else "") + (" map__pin--selected" if expanded else "")
    pop = ""
    if expanded:
        pop = (f'<div class="map__pop" role="dialog" aria-label="{o["name"]}" style="--pin-anchor:--pin-{o["id"]};"><div class="org-card" style="padding:0;gap:var(--space-3);"><span class="mark" aria-hidden="true">{o["mark"]}</span><div><a class="org-card__name" href="{ctx.p("organization")}" style="text-decoration:none;color:inherit;">{o["name"]}</a><div class="org-card__meta">{o["city"]} · {o["reach"]}</div></div></div>{tags(o["tags"])}</div>')
    return f'<button class="{cls}" type="button" style="left:{left:.1f}%;top:{top:.1f}%;--i:{i};--pin-anchor:--pin-{o["id"]};" aria-label="{o["name"]}, {o["city"]}" aria-expanded="{"true" if expanded else "false"}"></button>{pop}'


MAP_HEAD = '\n<link rel="stylesheet" href="../../assets/world-dots.css">'
GTA_HEAD = '\n<link rel="stylesheet" href="../../assets/gta-dots.css">'


def region_switch(ctx: Ctx, current: str) -> str:
    links = "".join(f'<a class="chip" href="{ctx.p("map", st)}"{" aria-current=\"page\"" if st == current else ""}>{label}</a>'
                    for st, label in [("default", "World"), ("gta", "Greater Toronto")])
    return f'<nav class="cluster" aria-label="Region" style="gap:var(--space-2);">{links}</nav>'


def map_page(ctx: Ctx):
    s = ctx.state
    placed = [o for o in ORGS if o["lon"] is not None]
    homeless = [o for o in ORGS if o["lon"] is None]
    chips = '<div class="toolbar rise" style="--i:1"><div class="cluster">' + "".join(f'<button class="chip" type="button" aria-pressed="{"true" if c == "All" else "false"}">{c}</button>' for c in ["All", "AI", "Youth", "Moonshot"]) + '</div><div class="map__legend" style="margin:0;"><span><i></i>Verified</span><span><i class="unverified"></i>Unverified</span></div></div>'
    h = header("Map", f"{len(placed)} placed · {len(homeless)} without a single home", region_switch(ctx, "default"))
    if s == "gta":
        local = [o for o in placed if in_box(o, GTA_BOX)]
        pins = "".join(pin(ctx, o, i, expanded=(o["id"] == "youth-unlimited-toronto"), box=GTA_BOX) for i, o in enumerate(local))
        labels = "".join(f'<span class="map__label" style="left:{x:.1f}%;top:{y:.1f}%;">{name}</span>' for name, (x, y) in ((n, project(lo, la, GTA_BOX)) for n, lo, la in GTA_LABELS))
        inner = (header("Map", f"Greater Toronto · {len(local)} placed", region_switch(ctx, "gta")) + chips
                 + f'<div class="map map--gta rise" style="--i:2"><div class="map__land"></div>{labels}{pins}</div>'
                 + f'<p class="text-caption" style="margin-top:var(--space-6);"><a href="{ctx.p("map")}">{len(placed) - len(local)} more on the world map</a>.</p>'
                 + '<section class="section reveal"><h2 class="section__title">Where the gaps are</h2><p style="font:var(--text-body-lg);max-width:48ch;">Every pin is west of Pickering. Nothing in Ajax, Whitby or Oshawa yet.</p></section>')
        return dict(head=GTA_HEAD, description="Greater Toronto region of the map, Mississauga to Oshawa, with local pins, three city labels and the Durham gap.", body=main_wrap(ctx, "map", inner),
                    notes=[note("Same dot matrix, finer grid: the land mask is Lake Ontario's shoreline from Natural Earth inside a Mississauga-to-Oshawa box, latitude scaled so the frame is true to the ground. Pins and labels share the box projection.", "top: 5rem; right: 1rem;")])
    if s == "loading":
        return dict(head=MAP_HEAD, description="Map loading: the world fades in while pins are fetched.", body=main_wrap(ctx, "map", header_skeleton(False, title="Map") + '<div class="map map--skeleton" aria-busy="true" aria-label="Loading map"><div class="map__land"></div></div>'), notes=[])
    if s == "empty":
        inner = header("Map", "Nothing placed yet") + f'<div class="map"><div class="map__land"></div></div>' + empty(ctx, "map-pin", "No organisations on the map", "Organisations appear here once they have a city.", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a>', compact=True)
        return dict(head=MAP_HEAD, description="Map with no organisations placed.", body=main_wrap(ctx, "map", inner, unread=0), notes=[])
    if s == "error":
        return dict(head=MAP_HEAD, description="Map pins failed to load; the world still renders.", body=main_wrap(ctx, "map", h + '<div class="map"><div class="map__land"></div></div>' + error_block(ctx, "the pins", back=ctx.p("field"))), notes=[])
    if s == "no-results":
        chips2 = chips.replace('aria-pressed="true">All', 'aria-pressed="false">All').replace('aria-pressed="false">Moonshot', 'aria-pressed="true">Moonshot')
        inner = h + chips2 + '<div class="map"><div class="map__land"></div></div>' + empty(ctx, "filter", "No pins match", "Moonshot organisations in this set have no single city.", f'<a class="btn" href="{ctx.p("map")}">Clear filters</a>', compact=True)
        return dict(head=MAP_HEAD, description="Map filters that leave no pins.", body=main_wrap(ctx, "map", inner), notes=[])
    pins = "".join(pin(ctx, o, i, expanded=(o["id"] == "faithtech")) for i, o in enumerate(placed))
    rest = ", ".join(f'<a href="{ctx.p("organization")}">{o["name"]}</a>' for o in homeless)
    inner = h + chips + f'<div class="map rise" style="--i:2"><div class="map__land"></div>{pins}</div><p class="text-caption" style="margin-top:var(--space-6);">Not on the map: {rest}.</p>'
    inner += '<section class="section reveal"><h2 class="section__title">Where the gaps are</h2><p style="font:var(--text-body-lg);max-width:48ch;">Fourteen of sixteen pins are in North America. No organisation in the catalogue is based in Africa, South America or mainland Asia yet.</p></section>'
    return dict(head=MAP_HEAD, description="World dot map with organisation pins, one expanded in an anchored popover, and a note on geographic gaps.", body=main_wrap(ctx, "map", inner),
                notes=[note("The land is a dot-matrix SVG used as a CSS mask so it takes the theme colour. The popover uses CSS anchor positioning (position-anchor, position-area) with flip fallbacks. Pins pulse on a staggered delay.", "top: 5rem; right: 1rem;")])


# ---------------------------------------------------------------------------
# Search, notifications, settings
# ---------------------------------------------------------------------------
def search_box(query: str, disabled: bool = False) -> str:
    return f'<form class="search rise" role="search" style="max-width:40rem;margin-bottom:var(--space-10);"><label class="visually-hidden" for="q">Search</label>{icon("search")}<input class="input input--lg" id="q" type="search" value="{query}" placeholder="Organisations, people, problems" autofocus{" disabled" if disabled else ""}></form>'


def search(ctx: Ctx):
    s = ctx.state
    if s == "loading":
        return dict(description="Search results loading for “gloo”.", body=main_wrap(ctx, None, header("Search") + search_box("gloo", disabled=True) + skeleton_cards(4)), notes=[])
    if s == "empty":
        recent = "".join(f'<li><a class="palette__item" href="{ctx.p("search")}">{icon("clock", "icon icon--sm text-subtle")}{q}</a></li>' for q in ["gloo", "youth AI", "2033"])
        inner = header("Search") + search_box("") + f'<section><h2 class="section__title">Recent</h2><ul class="list" style="max-width:40rem;">{recent}</ul></section>'
        return dict(description="Search page before a query, with recent searches.", body=main_wrap(ctx, None, inner), notes=[])
    if s == "error":
        return dict(description="Search failed.", body=main_wrap(ctx, None, header("Search") + search_box("gloo") + error_block(ctx, "results", back=ctx.p("field"))), notes=[])
    if s == "no-results":
        inner = header("Search") + search_box("youth hackathon kenya") + empty(ctx, "search", "No results for “youth hackathon kenya”", "Try fewer words, or ask the web.", f'<a class="btn btn--primary" href="{ctx.d("run-research")}">{icon("sparkle")}Ask the web</a>', compact=True)
        return dict(description="Search with no results and a way to turn it into research.", body=main_wrap(ctx, None, inner), notes=[])
    g = ORG_BY_ID["gloo"]
    inner = (header("Search", "7 results for “gloo”") + search_box("gloo")
             + f'<section class="section" style="margin-top:0;"><h2 class="section__title">Organisations · 1</h2><div class="entity-list">{org_card(ctx, g, 0)}</div></section>'
             + f'<section class="section"><h2 class="section__title">People · 2</h2><div class="entity-list">{person_row(ctx, PERSON_BY_ID["scott-beck"], 1)}{person_row(ctx, PERSON_BY_ID["pat-gelsinger"], 2)}</div></section>'
             + f'<section class="section"><h2 class="section__title">Problems · 1</h2><div class="entity-list">{problem_row(ctx, PROBLEM_BY_ID["ai-flourishing"], 3)}</div></section>'
             + f'<section class="section"><h2 class="section__title">Findings · 3</h2><div class="stack" style="gap:var(--space-4);">{finding_card(ctx, FINDINGS[0], 4)}{finding_card(ctx, FINDINGS[1], 5)}</div></section>')
    return dict(description="Search results for “gloo” grouped by organisation, person, problem and finding.", body=main_wrap(ctx, None, inner), notes=[])


def notif_item(title: str, text: str, when: str, href: str, unread: bool, icon_name: str = "info", i: int = 0) -> str:
    dot = '<span class="dot" style="color:var(--color-accent);" aria-label="Unread"></span>' if unread else '<span style="width:0.5rem;"></span>'
    return (f'<a class="list__item list__item--interactive rise" href="{href}" style="--i:{i};padding:var(--space-5) var(--space-6);gap:var(--space-4);{"" if unread else "color:var(--color-fg-muted);"}">{dot}{icon(icon_name)}<div class="list__body"><div class="list__title">{title}</div><div class="list__meta">{text}</div></div><span class="text-caption">{when}</span></a>')


def notifications(ctx: Ctx):
    s = ctx.state
    actions = '<button class="btn btn--ghost" type="button">Mark all read</button>'
    if s == "loading":
        return dict(description="Notification centre loading.", body=main_wrap(ctx, None, header_skeleton(title="Notifications") + '<div class="card card--flush" aria-busy="true" aria-label="Loading notifications">' + "".join(f'<div class="list__item" style="padding:var(--space-5) var(--space-6);"><span class="skeleton skeleton--circle" style="width:1.25rem;height:1.25rem;"></span><div class="list__body">{skeleton_lines(2, ("14rem", "22rem"))}</div></div>' for _ in range(4)) + "</div>"), notes=[])
    if s == "empty":
        return dict(description="No notifications yet.", body=main_wrap(ctx, None, header("Notifications", "Nothing yet") + empty(ctx, "bell", "You're all caught up", "Research results and teammates' changes show up here.", f'<a class="btn" href="{ctx.p("field")}">Back to the field</a>'), unread=0), notes=[])
    if s == "error":
        return dict(description="Notifications failed to load.", body=main_wrap(ctx, None, header("Notifications", "", actions) + error_block(ctx, "notifications", back=ctx.p("field"))), notes=[])
    read = s == "read"
    items = [("Run #47 finished", "12 findings to review · Who is helping Christian youth with AI?", "Yesterday", ctx.p("research", "review"), not read, "flask"),
             ("Priya added Pat Gelsinger's LinkedIn", "Gloo · 1 of 8 outstanding", "Tue 14 Oct", ctx.p("person"), not read, "linkedin"),
             ("Run #45 failed", "Moonshot goals with a public deadline · rate limited by 2 sources", "Fri 10 Oct", ctx.p("research"), not read, "danger"),
             ("Hannah archived Kingdom Code", "Restore from the organisation page", "Mon 13 Oct", ctx.p("organization", "read-only"), False, "building"),
             ("Elias scored 9 problems", "illumiNations leads with 94", "Thu 9 Oct", ctx.p("problems"), False, "target")]
    lis = "".join(notif_item(t, x, w, href, u, ic, i) for i, (t, x, w, href, u, ic) in enumerate(items))
    sub = "3 unread" if not read else "All read"
    return dict(description="Notification centre with unread items." if not read else "Notification centre after Mark all read.", body=main_wrap(ctx, None, header("Notifications", sub, actions if not read else "") + f'<div class="card card--flush"><div class="list">{lis}</div></div>', unread=0 if read else 3), notes=[])


def settings(ctx: Ctx):
    s = ctx.state
    invalid, busy = s == "invalid", s == "submitting"
    if s == "loading":
        return dict(description="Settings loading.", body=main_wrap(ctx, None, header_skeleton(False, title="Settings") + '<div class="card" style="max-width:44rem;" aria-busy="true" aria-label="Loading settings">' + "".join('<span class="skeleton skeleton--rect" style="height:2.5rem;margin-top:var(--space-4);"></span>' for _ in range(5)) + "</div>"), notes=[])
    if s == "error":
        return dict(description="Settings failed to load.", body=main_wrap(ctx, None, header("Settings") + error_block(ctx, "settings", back=ctx.p("field"))), notes=[])
    summary = form_summary([("me-email", "Enter an e-mail address like name@example.com"), ("ws-sources", "Enter one domain per line, like barna.com")]) if invalid else ""
    saved = f'<div class="inline-status inline-status--success" role="status">{icon("success", "icon icon--sm")} Saved · just now</div>' if s == "success" else ""
    theme = "".join(f'<label class="choice"><input type="radio" name="theme" value="{v}"{" checked" if v == "system" else ""}{" disabled" if busy else ""}><span class="choice__text">{l}</span></label>' for v, l in [("system", "Match system"), ("light", "Light"), ("dark", "Dark")])
    form = (f'<form class="stack" style="gap:var(--space-12);max-width:44rem;" novalidate>{summary}'
            f'<section class="card stack" style="gap:var(--space-6);padding:var(--space-8);"><h2 class="section__title" style="margin:0;">Profile</h2><div class="cluster" style="gap:var(--space-4);">{avatar(ME["initials"], "avatar avatar--lg")}<button class="btn btn--sm" type="button">Change photo</button></div>'
            + field("me-name", "Name", text_input("me-name", ME["name"], readonly=busy))
            + field("me-email", "E-mail", text_input("me-email", "naomi@harvestmap" if invalid else ME["email"], "email", invalid=invalid, readonly=busy), error="Enter an e-mail address like name@example.com" if invalid else "")
            + "</section>"
            f'<section class="card stack" style="gap:var(--space-6);padding:var(--space-8);"><h2 class="section__title" style="margin:0;">Research</h2>'
            + field("ws-depth", "Default depth", select("ws-depth", ["Quick · 1 minute", "Standard · 5 minutes", "Deep · 20 minutes"], "Standard · 5 minutes", disabled=busy), help_text="How long a run may search before it reports.")
            + field("ws-sources", "Trusted sources", textarea("ws-sources", "barna.com\nchristianitytoday.com\nreligionnews.com\nministrywatch.com" + ("\nnot a domain" if invalid else ""), rows=4, invalid=invalid, readonly=busy), help_text="One domain per line. Findings from these need one source instead of two.", error="Enter one domain per line, like barna.com" if invalid else "")
            + f'<label class="switch"><input type="checkbox" checked{" disabled" if busy else ""}><span>Require two sources before a finding is verified</span></label></section>'
            f'<section class="card stack" style="gap:var(--space-6);padding:var(--space-8);"><h2 class="section__title" style="margin:0;">Appearance</h2><fieldset><legend>Theme</legend>{theme}</fieldset><label class="switch"><input type="checkbox"{" disabled" if busy else ""}><span>Reduce motion</span></label><label class="switch"><input type="checkbox" checked{" disabled" if busy else ""}><span>Animate the field (WebGPU)</span></label></section>'
            f'<section class="card stack" style="gap:var(--space-6);padding:var(--space-8);"><h2 class="section__title" style="margin:0;">Notifications</h2><label class="switch"><input type="checkbox" checked{" disabled" if busy else ""}><span>When a run finishes</span></label><label class="switch"><input type="checkbox" checked{" disabled" if busy else ""}><span>When a teammate verifies a finding</span></label><label class="switch"><input type="checkbox"{" disabled" if busy else ""}><span>Weekly digest by e-mail</span></label></section>'
            f'<div class="form-actions" style="justify-content:space-between;align-items:center;">{saved}<span class="topbar__spacer"></span>'
            + ('<button class="btn btn--primary" type="submit" aria-busy="true">Save changes</button>' if busy else '<button class="btn btn--primary" type="submit">Save changes</button>') + "</div></form>"
            f'<section class="section" style="max-width:44rem;"><h2 class="section__title">Account</h2><div class="cluster"><a class="btn" href="{ctx.d("sign-out")}">{icon("logout")}Sign out</a><a class="btn btn--ghost" href="{ctx.d("keyboard-shortcuts")}">{icon("keyboard")}Keyboard shortcuts</a></div></section>')
    desc = {"default": "Settings: profile, research defaults, appearance and notifications.", "invalid": "Settings submitted with a bad e-mail and a bad source domain.", "submitting": "Saving settings.", "success": "Settings saved."}[s]
    return dict(description=desc, body=main_wrap(ctx, None, header("Settings", "Signed in as " + ME["email"]) + form), notes=[])


# ---------------------------------------------------------------------------
# Error pages
# ---------------------------------------------------------------------------
def big_page(ctx: Ctx, code: str, title: str, text: str, actions: str, icon_name: str, nav: bool = True) -> str:
    inner = f'<div class="big-empty"><div class="empty rise"><div class="empty__code" aria-hidden="true">{code}</div><div class="empty__icon">{icon(icon_name, "icon icon--lg")}</div><h1 class="empty__title">{title}</h1><p class="empty__text">{text}</p><div class="empty__actions">{actions}</div></div></div>'
    if nav:
        return main_wrap(ctx, None, inner)
    return f'<main id="main" class="container app-main">{inner}</main>'


def not_found(ctx: Ctx):
    return dict(description="404: the record or page does not exist.", body=big_page(ctx, "404", "Nothing grows here", "The page you asked for doesn't exist, or was deleted.", f'<a class="btn btn--primary" href="{ctx.p("field")}">Back to the field</a><a class="btn btn--ghost" href="{ctx.p("search", "empty")}">Search</a>', "map-pin"), notes=[])


def forbidden(ctx: Ctx):
    return dict(description="403: the person lacks access to this workspace or record.", body=big_page(ctx, "403", "Not your field", "You don't have access to this workspace. Ask Hannah Okafor, the admin, to invite you.", f'<a class="btn btn--primary" href="mailto:hannah@harvestmap.app">Ask Hannah</a><a class="btn btn--ghost" href="{ctx.p("field")}">Back to the field</a>', "lock"), notes=[])


def server_error(ctx: Ctx):
    return dict(description="500: an unexpected failure with a reference code.", body=big_page(ctx, "500", "Something went wrong", "We've been notified. Try again, or share reference HM-9C21 with support.", f'<a class="btn btn--primary" href="{ctx.p("field")}">{icon("refresh")}Try again</a><a class="btn btn--ghost" href="mailto:support@harvestmap.app?subject=HM-9C21">Contact support</a>', "danger"), notes=[])


def offline(ctx: Ctx):
    return dict(description="Offline with nothing cached for this page.", body=big_page(ctx, "", "You're offline", "Cached pages still open. This one isn't cached yet.", f'<a class="btn btn--primary" href="{ctx.p("field")}">{icon("refresh")}Retry</a>', "wifi-off"), notes=[note("Pages visited this session stay available offline; edits queue and sync when back online (see the offline banner).", "top: 5rem; right: 1rem;")])


def unsupported_browser(ctx: Ctx):
    body = big_page(ctx, "", "Harvest Map needs Chrome", "It uses WebGPU, anchor positioning and view transitions that only Chrome 125 or newer supports. Open this link in Chrome to continue.", '<a class="btn btn--primary" href="https://www.google.com/chrome/" target="_blank" rel="noopener">Get Chrome</a><button class="btn btn--ghost" type="button">Copy link</button>', "chrome", nav=False)
    return dict(description="Shown in any browser that lacks the Chrome-only features the app relies on.", body=body, notes=[note("Detection is feature-based (navigator.gpu, CSS.supports('anchor-name: --a')), not user-agent sniffing. Edge and other Chromium browsers that pass are allowed through.", "top: 1rem; right: 1rem;")])


RENDERERS = {
    "sign-in": sign_in, "forgot-password": forgot_password, "reset-password": reset_password,
    "field": field_page, "organizations": organizations, "organization": organization, "organization-edit": organization_edit,
    "people": people, "person": person, "person-edit": person_edit,
    "problems": problems, "problem": problem, "problem-edit": problem_edit,
    "questions": questions, "research": research, "map": map_page, "search": search, "notifications": notifications, "settings": settings,
    "not-found": not_found, "forbidden": forbidden, "server-error": server_error, "offline": offline, "unsupported-browser": unsupported_browser,
}


def render(ctx: Ctx):
    return RENDERERS[ctx.sid](ctx)


def page_body(ctx: Ctx, sid: str, state: str = "default") -> str:
    """Body HTML of a page for use behind a dialog or under a notification."""
    sub = Ctx(ctx.kind, ctx.sid, ctx.state)
    saved = (sub.sid, sub.state)
    sub.sid, sub.state = sid, state
    result = RENDERERS[sid](sub)
    sub.sid, sub.state = saved
    return result["body"]
