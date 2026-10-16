"""Notification renderers: toasts, banners and inline alerts shown on their page."""
from __future__ import annotations

from build import Ctx, icon, note
from pages import alert, page_body


def toast(kind: str, title: str, text: str = "", action: str = "", role: str = "status", progress: bool = True) -> str:
    act = f'<button class="toast__action" type="button">{action}</button>' if action else ""
    prog = '<span class="toast__progress" aria-hidden="true"></span>' if progress else ""
    return (f'<div class="toast toast--{kind}" role="{role}">{icon(kind)}<div class="toast__body"><div class="toast__title">{title}</div>' + (f'<div class="toast__text">{text}</div>' if text else "") + f'{act}</div>'
            f'<button class="close" type="button" aria-label="Dismiss">{icon("close", "icon icon--sm")}</button>{prog}</div>')


def region(toasts: str, alert_region: bool = False) -> str:
    role = "alert" if alert_region else "status"
    live = "assertive" if alert_region else "polite"
    return f'<div class="toast-region" role="{role}" aria-live="{live}">{toasts}</div>'


def with_toast(ctx: Ctx, page: str, state: str, toasts: str, description: str, notes: list[str] | None = None, alert_region: bool = False) -> dict:
    return dict(description=description, body=page_body(ctx, page, state) + region(toasts, alert_region), notes=notes or [])


def with_banner(ctx: Ctx, page: str, state: str, banner: str, description: str, notes: list[str] | None = None) -> dict:
    body = page_body(ctx, page, state).replace("</header>", "</header>" + banner, 1)
    return dict(description=description, body=body, notes=notes or [])


def banner(kind: str, title: str, text: str = "", actions: str = "", role: str = "status", dismiss: bool = True, pulse: bool = False) -> str:
    ic = icon(kind)
    if pulse:
        ic = '<span class="dot dot--pulse" style="color:var(--color-info-icon);margin-top:0.45rem;" aria-hidden="true"></span>'
    close = f'<button class="close" type="button" aria-label="Dismiss">{icon("close", "icon icon--sm")}</button>' if dismiss else ""
    return f'<div class="alert alert--{kind} banner" role="{role}">{ic}<div class="alert__body"><span class="alert__title">{title}</span>' + (f"<span>{text}</span>" if text else "") + (f'<span class="alert__actions">{actions}</span>' if actions else "") + f"</div>{close}</div>"


# ---------------------------------------------------------------------------
def toast_notification(ctx: Ctx):
    s = ctx.state
    auto = note("Auto-dismisses after 8 s; the timer (the thin bar) pauses on hover and focus.", "bottom: 9rem; right: 1rem;")
    if s == "info":
        return with_toast(ctx, "organizations", "default", toast("info", "Run #48 started", "8 people queued · about 6 minutes"), "Informational toast when a research run starts.", [auto])
    if s == "success":
        return with_toast(ctx, "organizations", "default", toast("success", "FaithTech saved", "", "Undo"), "Success toast after saving, with undo.", [auto])
    if s == "warning":
        return with_toast(ctx, "organizations", "default", toast("warning", "Run #48 slowed", "2 sources are rate-limiting. It will finish, just later."), "Warning toast: nothing broke, but expectations changed.", [auto])
    if s == "danger":
        return with_toast(ctx, "organizations", "default", toast("danger", "Couldn't save FaithTech", "Your changes are still in the form.", "Retry", role="alert", progress=False), "Error toast: persistent until dismissed, with retry.", [note("Error toasts never auto-dismiss and are announced assertively.", "bottom: 9rem; right: 1rem;")], alert_region=True)
    if s == "with-action":
        return with_toast(ctx, "organizations", "default", toast("success", "Kingdom Code archived", "Hidden from lists and the map.", "Undo"), "Toast carrying a primary action (Undo) for a reversible change.", [auto])
    stacked = toast("success", "Pat Gelsinger verified", "", "Undo") + toast("info", "Run #48 started", "8 people queued") + toast("warning", "Run #48 slowed", "2 sources are rate-limiting.")
    return with_toast(ctx, "organizations", "default", stacked, "Three toasts at once: newest at the bottom, each dismissible on its own.", [note("Maximum three visible; a fourth pushes the oldest out. Order is oldest at the top.", "bottom: 16rem; right: 1rem;")])


def research_banner(ctx: Ctx):
    s = ctx.state
    if s == "info":
        b = banner("info", "Run #48 running · 62%", "Finding LinkedIn profiles for 8 people.", f'<a href="{ctx.p("research", "running")}">View</a>', pulse=True)
        return with_banner(ctx, "research", "default", b, "Banner while a run is in progress; follows the person across pages.")
    if s == "success":
        b = banner("success", "Run #47 finished", "12 findings to review.", f'<a href="{ctx.p("research", "review")}">Review</a>')
        return with_banner(ctx, "research", "default", b, "Banner when a run completes with findings.")
    if s == "warning":
        b = banner("warning", "Run #48 slowed", "2 sources are rate-limiting; it will finish later than estimated.", '<a href="#">Switch to Quick</a>')
        return with_banner(ctx, "research", "default", b, "Banner warning that a run is slower than expected.")
    if s == "danger":
        b = banner("danger", "Run #45 failed", "Rate limited by 2 sources after 30%.", f'<a href="{ctx.d("run-research")}">Retry</a>', role="alert", dismiss=False)
        return with_banner(ctx, "research", "default", b, "Banner when a run fails; stays until retried or acknowledged.")
    b = banner("info", "Trusted sources changed", "Hannah Okafor added 2 domains. 41 findings re-verify tonight.", f'<a href="{ctx.p("settings")}">See sources</a>')
    return with_banner(ctx, "research", "default", b, "Persistent banner about a workspace change; stays until dismissed.", [note("Persistent: survives navigation and reload until dismissed by this person.", "top: 8rem; right: 1rem;")])


def offline_banner(ctx: Ctx):
    s = ctx.state
    if s == "info":
        return with_banner(ctx, "organizations", "default", banner("info", "Reconnecting", "Syncing 2 queued edits.", pulse=True, dismiss=False), "Banner while the connection is restored and edits sync.")
    if s == "success":
        return with_banner(ctx, "organizations", "default", banner("success", "Back online", "2 queued edits synced."), "Banner when back online; dismisses itself after 8 s.")
    if s == "warning":
        return with_banner(ctx, "organizations", "default", banner("warning", "You're offline", "Edits queue and sync when you're back. Research can't run.", dismiss=False), "Banner while offline; actions that need the network are disabled.", [note("Not dismissible: it is the only indicator that saves are queued. Run research buttons are disabled while it shows.", "top: 8rem; right: 1rem;")])
    if s == "danger":
        return with_banner(ctx, "organizations", "default", banner("danger", "Couldn't sync 1 edit", "FaithTech was changed by Tobias while you were offline.", '<a href="#">Review conflict</a>', role="alert", dismiss=False), "Banner for a sync conflict after reconnecting.")
    return with_banner(ctx, "organizations", "default", banner("warning", "Offline for 2 hours", "5 edits queued.", dismiss=False), "Long offline session: the banner persists with the queue size.")


def inline_alert(ctx: Ctx):
    s = ctx.state
    def inject(a: str) -> str:
        return page_body(ctx, "organization", "default").replace('<div class="detail"', a + '<div class="detail"', 1)
    if s == "info":
        return dict(description="Inline alert on the organisation page while a run checks it.", body=inject(alert("info", "Run #48 is checking this organisation", "Fields may update in the next few minutes.")), notes=[])
    if s == "success":
        return dict(description="Inline alert after findings were accepted.", body=inject(alert("success", "2 findings accepted", "Updated Reach and added 1 initiative.", f'<a href="{ctx.p("research", "review")}">See findings</a>')), notes=[])
    if s == "warning":
        return dict(description="Inline alert when sources disagree.", body=inject(alert("warning", "Sources disagree on the founding year", "ministrywatch.com says 2010; religionnews.com says 2013.", '<a href="#">Resolve</a>')), notes=[note("Resolve opens the two sources side by side and writes the chosen value.", "top: 12rem; right: 1rem;")])
    if s == "danger":
        return dict(description="Inline alert for a broken website link.", body=inject(alert("danger", "Website unreachable since Mon 13 Oct", "faithtech.com returned a timeout three times.", f'<a href="{ctx.p("organization-edit")}">Edit website</a>', role="alert")), notes=[])
    return dict(description="Inline alert carrying a primary action.", body=inject(alert("info", "1 person has no LinkedIn link", "", f'<a href="{ctx.d("run-research")}">Find on LinkedIn</a>')), notes=[])


RENDERERS = {"toast": toast_notification, "research-banner": research_banner, "offline-banner": offline_banner, "inline-alert": inline_alert}


def render(ctx: Ctx):
    return RENDERERS[ctx.sid](ctx)
