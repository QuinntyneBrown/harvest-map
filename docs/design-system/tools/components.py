"""Component specs and the renderer that turns each into a 13-section page."""
from __future__ import annotations

from shell import (COMPONENTS, dodont, example, icon, matrix, mock_links, page, pair, state_row, table, themes, token_table, ul)

SPECS: list[dict] = []
D5 = ["Default", "Hover", "Focus", "Active", "Disabled"]


def C(**spec):
    SPECS.append(spec)
    COMPONENTS.append((spec["id"], spec["name"], spec["group"]))


def keys(rows):
    return table(["Key", "Action"], [[f"<kbd>{k}</kbd>", a] for k, a in rows], "ds-table ds-keys")


# ============================================================================ Actions
C(id="button", name="Button", group="Actions",
  lead="Buttons trigger actions. Five variants, three sizes, every state, a spring press and a halo on primary hover.",
  overview="<p>Use a button when activating it changes something: saves, runs research, deletes, opens a dialog. Use a <a href=\"link.html\">link</a> when it only goes somewhere. Harvest Map keeps <b>one primary per view</b>; in the mocks that is <i>Ask the web</i>, <i>New</i>, <i>Save</i> or the dialog's confirm.</p>"
           + ul(["<b>Primary</b>: the one action the view exists for.", "<b>Secondary</b> (default look): every other action.", "<b>Ghost</b>: toolbars, page-header actions like Import/Export, row actions.", "<b>Link</b>: low-emphasis action inside text.", "<b>Danger</b>: destructive confirmation inside a dialog only."]),
  anatomy=(f'<button class="btn btn--primary btn--lg" type="button">{icon("sparkle")}Ask the web</button>',
           [("Leading icon (optional)", "1.25em, inherits colour, aria-hidden"), ("Label", "Verb phrase, sentence case"), ("Container", "--control-height-md, --radius-md (12px), 1px border")]),
  variants=[(f'<button class="btn btn--primary" type="button">Run</button><button class="btn" type="button">Cancel</button><button class="btn btn--ghost" type="button">{icon("upload")}Import</button><button class="btn btn--link" type="button">Undo</button><button class="btn btn--danger" type="button">Delete organisation</button>', "Primary, secondary, ghost, link, danger."),
            (f'<button class="btn btn--icon" type="button" aria-label="Edit">{icon("edit")}</button><button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{icon("close")}</button><button class="btn btn--primary btn--block" type="button">Continue</button>', "Icon-only buttons need aria-label; block buttons fill auth cards.")],
  sizes=[('<button class="btn btn--primary btn--sm" type="button">Small · 32</button><button class="btn btn--primary" type="button">Medium · 40</button><button class="btn btn--primary btn--lg" type="button">Large · 48</button>', "sm in rows and finding cards, md by default, lg in the hero.")],
  states=(D5 + ["Loading"], [state_row("Primary", '<button class="btn btn--primary" type="button" {s}>Save</button>', D5 + ["Loading"]),
                             state_row("Secondary", '<button class="btn" type="button" {s}>Cancel</button>', D5 + ["Loading"]),
                             state_row("Ghost", '<button class="btn btn--ghost" type="button" {s}>Export</button>', D5 + ["Loading"]),
                             state_row("Link", '<button class="btn btn--link" type="button" {s}>Undo</button>', D5 + ["Loading"]),
                             state_row("Danger", '<button class="btn btn--danger" type="button" {s}>Delete</button>', D5 + ["Loading"])]),
  sample='<button class="btn btn--primary" type="button">Run</button><button class="btn" type="button">Cancel</button><button class="btn btn--ghost" type="button">Export</button><button class="btn btn--danger" type="button">Delete</button>',
  responsive=["Never wraps its label; a cluster of buttons wraps instead.", "Under 640px dialog footers keep buttons side by side; the confirm stays last (right).", "Touch: primary mobile buttons use --control-height-lg (48px) or sit in a 44px target."],
  tokens=[("Primary background", "--color-accent"), ("Primary hover", "--color-accent-hover"), ("Primary label", "--color-fg-on-accent"), ("Secondary border", "--color-border-strong"), ("Danger background", "--color-danger-solid"), ("Height", "--control-height-md"), ("Radius", "--radius-md"), ("Press easing", "--ease-spring-linear")],
  a11y=dict(pattern="Native <code>&lt;button&gt;</code> (APG Button). Toggle buttons add <code>aria-pressed</code>; menu triggers add <code>aria-expanded</code>.",
            keys=[("Enter", "Activate"), ("Space", "Activate"), ("Tab", "Move to next control")],
            focus="Shared 2px ring, 2px offset, never removed. Dialogs autofocus the safe button, never the danger button.",
            label="Visible label is the accessible name; icon-only buttons need <code>aria-label</code> and a tooltip.",
            pairs=[("Label on primary", "--color-fg-on-accent", "--color-accent"), ("Label on danger", "--color-fg-on-danger", "--color-danger-solid"), ("Secondary border on surface", "--color-border-strong", "--color-bg-surface", 3)],
            motion="Press scales to 0.98 with a spring; primary hover grows a 4px accent halo over --duration-base. Both vanish under reduced motion.",
            touch="Hover halo is cosmetic; press feedback is the scale. Minimum 40px tall, 48px for large."),
  content=["Verb first: <i>Run</i>, <i>Save</i>, <i>Delete organisation</i>, never <i>OK</i> or <i>Submit</i>.", "Name the count when acting on a set: <i>Export 14 organisations</i>, <i>Import 312 rows</i>.", "Danger buttons name the thing: <i>Delete organisation</i>, not <i>Delete</i>."],
  dos=[('<button class="btn" type="button">Cancel</button><button class="btn btn--primary" type="button">Run</button>', "One primary, last in the row.", '<button class="btn btn--primary" type="button">Run</button><button class="btn btn--primary" type="button">Save</button>', "Two primaries compete."),
       ('<button class="btn" type="button">Cancel</button><button class="btn btn--danger" type="button">Delete organisation</button>', "Danger names what is lost.", '<button class="btn btn--danger" type="button" autofocus>OK</button>', "Generic label with focus on the danger button.")],
  code=('<button class="btn btn--primary" type="button">Run</button>', [("btn", "Base (secondary look)"), ("btn--primary / --ghost / --link / --danger", "Variant"), ("btn--sm / --lg", "Size"), ("btn--icon", "Square icon-only"), ("btn--block", "Full width"), ('aria-busy="true"', "Loading: spinner, label hidden, width kept")]),
  sources=["pages/field/default", "pages/organizations/default", "dialogs/delete-organization/default", "pages/sign-in/submitting"],
  drift="Mocks used a ghost button tinted with an inline danger colour for Delete in page headers; the system uses ghost + danger text only through <code>btn--ghost</code> with <code>--btn-fg</code>, logged in the README.")

C(id="link", name="Link", group="Actions", lead="Links go somewhere. Always underlined; external links show an icon and open in a new tab.",
  overview="<p>Inline links in copy, standalone links like <i>All problems</i> in section headers, and external links to an organisation's website or a source article.</p>",
  anatomy=(f'<a href="#overview">faithtech.com{icon("external", "icon icon--sm")}</a>', [("Text", "Underlined, 1px, 0.15em offset"), ("External icon", "16px, after the text")]),
  variants=[(f'<p>Read the <a href="#overview">sources</a> first.</p><a href="#overview">All problems</a><a href="#overview" class="linkedin">{icon("linkedin", "icon icon--sm")}LinkedIn{icon("external", "icon icon--sm")}</a>', "Inline, standalone, external (LinkedIn search).")],
  sizes="Links inherit the size of the text they sit in.",
  states=(["Default", "Hover", "Focus"], [state_row("Link", '<a href="#overview" {s}>All problems</a>', ["Default", "Hover", "Focus"])]),
  sample='<a href="#overview">All problems</a> <a href="#overview">faithtech.com</a>',
  responsive=["Long URLs wrap with <code>overflow-wrap: anywhere</code> inside source lists.", "Standalone links in section headers drop below the heading under 640px via the cluster."],
  tokens=[("Text", "--color-fg-link"), ("Hover", "--color-fg-link-hover"), ("Focus ring", "--color-focus-ring")],
  a11y=dict(pattern="Native <code>&lt;a href&gt;</code>. External links carry <code>target=\"_blank\" rel=\"noopener\"</code> and the external icon.", keys=[("Enter", "Follow")],
            focus="Shared ring.", label="Link text must make sense alone: <i>Open run #48</i>, not <i>here</i>.",
            pairs=[("Link on canvas", "--color-fg-link", "--color-bg-canvas"), ("Link on surface", "--color-fg-link", "--color-bg-surface")], motion="Colour change over --duration-fast.", touch="Standalone links sit in a 24px minimum line box."),
  content=["Name the destination: <i>See findings</i>, <i>Review conflict</i>.", "LinkedIn links say <i>LinkedIn</i> and open a people search until a profile is verified."],
  dos=[('<a href="#overview">Open run #48</a>', "Destination in the text.", '<a href="#overview">Click here</a>', "Meaningless out of context."),
       ('<a href="#overview">faithtech.com</a>', "Underlined like every link.", '<span class="text-muted">faithtech.com</span>', "A link that does not look like one.")],
  code=('<a href="https://faithtech.com" target="_blank" rel="noopener">faithtech.com</a>', [("a", "Default link styling"), ("linkedin", "Inline-flex with icon, never wraps")]),
  sources=["pages/organization/default", "pages/people/default"], drift="None.")

C(id="menu", name="Menu", group="Actions", lead="A list of actions behind one trigger. Core component; the mocks have not needed one yet.",
  overview="<p>Use for overflow actions on a record (Archive, Duplicate, Delete) when the page header would otherwise carry more than three buttons.</p>",
  anatomy=('<div class="menu-anchor"><button class="btn" type="button" aria-haspopup="menu" aria-expanded="true">Actions</button><ul class="menu" role="menu" aria-label="Organisation actions" style="position:static;margin-top:var(--space-2);"><li role="none"><button class="menu__item" role="menuitem" type="button">Archive</button></li><li role="none"><button class="menu__item menu__item--danger" role="menuitem" type="button">Delete</button></li></ul></div>',
           [("Trigger", "Button with aria-haspopup"), ("Surface", "--shadow-3, --radius-md"), ("Item", "32px tall, label + optional kbd")]),
  variants=[('<ul class="menu" role="menu" aria-label="Example" style="position:static;"><li role="none"><button class="menu__item" role="menuitem" type="button">Edit<kbd>E</kbd></button></li><li role="none"><button class="menu__item" role="menuitem" type="button">Export</button></li><li class="menu__divider" role="separator"></li><li role="none"><button class="menu__item menu__item--danger" role="menuitem" type="button">Delete</button></li></ul>', "Shortcuts, divider and danger item.")],
  sizes="One size; items are 32px.",
  states=(["Default", "Hover", "Disabled"], [("Item", ['<button class="menu__item" type="button">Archive</button>', '<button class="menu__item" type="button" data-state="hover">Archive</button>', '<button class="menu__item" type="button" aria-disabled="true">Archive</button>'])]),
  sample='<ul class="menu" role="menu" aria-label="Sample" style="position:static;"><li role="none"><button class="menu__item" role="menuitem" type="button">Archive</button></li></ul>',
  responsive=["Under 640px a menu with more than five items becomes a bottom sheet (dialog)."],
  tokens=[("Surface", "--color-bg-surface-raised"), ("Shadow", "--shadow-3"), ("Hover", "--color-bg-subtle"), ("Danger text", "--color-danger-fg")],
  a11y=dict(pattern="APG Menu Button: <code>aria-haspopup=\"menu\"</code>, <code>aria-expanded</code>, <code>role=\"menu/menuitem\"</code>.", keys=[("Enter / Space / ↓", "Open, focus first item"), ("↑ ↓", "Move"), ("Esc", "Close, return focus"), ("Letter", "Type-ahead")],
            focus="Roving focus inside the menu; returns to the trigger.", label="Trigger has a visible label; menu has aria-label.", pairs=[("Item on raised surface", "--color-fg-default", "--color-bg-surface-raised"), ("Danger item", "--color-danger-fg", "--color-bg-surface-raised")],
            motion="Scales in from the trigger over --duration-fast.", touch="Items grow to 44px under (pointer: coarse)."),
  content=["Verbs, sentence case.", "Destructive item last, after a divider."],
  dos=[('<button class="menu__item menu__item--danger" type="button">Delete organisation</button>', "Danger item last and specific.", '<button class="menu__item" type="button">Delete</button>', "Destructive item styled as ordinary.")],
  code=('<ul class="menu" role="menu">…</ul>', [("menu", "Surface"), ("menu__item", "Item"), ("menu__item--danger", "Destructive item"), ("menu__divider", "Separator")]),
  sources=["pages/organization/default"], drift="Not yet used in mocks; documented as part of the core set.")

C(id="command-palette", name="Command palette", group="Actions", lead="⌘K: jump to any organisation, person or action from the keyboard.",
  overview="<p>Opens from the topbar search button, ⌘K or /. Groups results (Organisations, People, Actions) and turns a no-match into <i>Ask the web</i>.</p>",
  anatomy=(f'<div class="palette__panel" style="position:relative;"><div class="palette__input">{icon("search", "icon text-subtle")}<label class="visually-hidden" for="cp-a">Search</label><input id="cp-a" type="search" value="gl"><span class="kbd">Esc</span></div><ul class="palette__list" role="listbox" aria-label="Results"><li class="palette__group">Organisations</li><li><a class="palette__item" href="#overview" aria-selected="true">{icon("building")}Gloo</a></li></ul><div class="palette__foot"><span><span class="kbd">↵</span> open</span></div></div>',
           [("Input", "18px text, 48px tall"), ("Group heading", "Overline"), ("Item", "40px, icon, label, meta, optional kbd"), ("Footer", "Key hints")]),
  variants=[(f'<div class="palette__panel" style="position:relative;"><div class="palette__input">{icon("search", "icon text-subtle")}<label class="visually-hidden" for="cp-b">Search</label><input id="cp-b" type="search" value="zebra"></div><div style="padding:var(--space-6);text-align:center;" class="text-muted">No matches for “zebra”.</div></div>', "No results with a way out.")],
  sizes="One size: 36rem wide, 12vh from the top.",
  states=(["Default", "Selected item", "Loading"], [("Palette", [f'<a class="palette__item" href="#overview">{icon("building")}Gloo</a>', f'<a class="palette__item" href="#overview" aria-selected="true">{icon("building")}Gloo</a>', '<span class="inline-status"><span class="spinner" aria-hidden="true"></span>Searching</span>'])]),
  sample=f'<a class="palette__item" href="#overview" aria-selected="true">{icon("building")}Gloo</a>',
  responsive=["Full width minus 16px under 640px; list max-height 50vh."],
  tokens=[("Panel", "--color-bg-surface-raised"), ("Selected item", "--color-bg-subtle"), ("Shadow", "--shadow-4")],
  a11y=dict(pattern="Dialog containing an APG Combobox with a listbox popup (<code>aria-activedescendant</code>).", keys=[("⌘K or /", "Open"), ("↑ ↓", "Move selection"), ("Enter", "Open selection"), ("Esc", "Close")],
            focus="Focus starts in the input and stays there; selection moves virtually.", label="Input has a visually hidden label; listbox has aria-label.", pairs=[("Item text", "--color-fg-default", "--color-bg-subtle")],
            motion="Scales in over --duration-base.", touch="Items 40px; tapping opens."),
  content=["Group names are plural nouns.", "Empty: “No matches for “query”.” plus Ask the web."],
  dos=[(f'<a class="palette__item" href="#overview">{icon("sparkle")}Run research<span class="kbd">R</span></a>', "Show the shortcut.", '<a class="palette__item" href="#overview">Run research</a>', "Hide shortcuts people could learn.")],
  code=('<div class="palette" role="dialog" aria-modal="true">…</div>', [("palette", "Fixed overlay"), ("palette__panel", "Surface"), ("palette__item", "Result")]),
  sources=["dialogs/command-palette/default", "dialogs/command-palette/no-results"], drift="None.")

# ============================================================================ Inputs
FIELD_COLS = ["Default", "Hover", "Focus", "Invalid", "Read-only", "Disabled"]
FX = {"Invalid": 'aria-invalid="true"', "Read-only": "readonly"}

C(id="text-field", name="Text field", group="Inputs", lead="Single-line text: name, e-mail, URL, search. 40px tall, 12px radius.",
  overview="<p>Always inside a <a href=\"form-field.html\">form field</a> with a visible label. Search inputs carry a leading icon and live in toolbars and the topbar.</p>",
  anatomy=('<div class="field" style="width:100%;max-width:20rem;"><label class="field__label" for="tf-a">Website</label><input class="input" id="tf-a" value="faithtech.com" aria-describedby="tf-a-h"><span class="field__help" id="tf-a-h">Like example.org</span></div>', [("Label", "--text-label"), ("Input", "40px, 1px --color-border-strong"), ("Help", "--text-body-sm muted")]),
  variants=[(f'<form class="search" role="search" style="width:16rem;"><label class="visually-hidden" for="tf-s">Search</label>{icon("search")}<input class="input" id="tf-s" type="search" placeholder="Search"></form><label class="visually-hidden" for="tf-e">E-mail</label><input class="input" id="tf-e" type="email" value="naomi@harvestmap.app" style="width:16rem;">', "Search with icon; e-mail.")],
  sizes=[('<label class="visually-hidden" for="tf-1">Small</label><input class="input input--sm" id="tf-1" value="Small" style="width:10rem;"><label class="visually-hidden" for="tf-2">Medium</label><input class="input" id="tf-2" value="Medium" style="width:10rem;"><label class="visually-hidden" for="tf-3">Large</label><input class="input input--lg" id="tf-3" value="Large" style="width:10rem;">', "32 / 40 / 48px. Large is for the search page.")],
  states=(FIELD_COLS, [("Input", [f'<label class="visually-hidden" for="tf-st{i}">Name</label><input class="input" id="tf-st{i}" value="FaithTech" {dict(STATE := {"Hover": "data-state=\"hover\"", "Focus": "data-state=\"focus\"", "Disabled": "disabled"}, **FX).get(c, "")}>' for i, c in enumerate(FIELD_COLS)])]),
  sample='<label class="visually-hidden" for="tf-th">Name</label><input class="input" id="tf-th" value="FaithTech">',
  responsive=["Fields are full width of their column; two-column grids collapse to one under 640px.", "16px text prevents iOS zoom."],
  tokens=[("Border", "--color-border-strong"), ("Background", "--color-bg-surface"), ("Focus ring", "--color-focus-ring"), ("Invalid border", "--color-danger-solid"), ("Read-only", "--color-bg-surface-sunken"), ("Height", "--control-height-md")],
  a11y=dict(pattern="Native <code>&lt;input&gt;</code> with <code>&lt;label for&gt;</code>; help and error via <code>aria-describedby</code>; <code>aria-invalid</code> when wrong.", keys=[("Tab", "Enter/leave"), ("Enter", "Submit the form")],
            focus="2px ring flush with the border.", label="Visible label always; placeholder is a hint only. <code>autocomplete</code> on e-mail and password.",
            pairs=[("Border on surface", "--color-border-strong", "--color-bg-surface", 3), ("Placeholder", "--color-fg-subtle", "--color-bg-surface")], motion="Border colour over --duration-fast.", touch="40px tall minimum."),
  content=["Labels are nouns: <i>Website</i>, <i>Country</i>.", "Help shows the format: <i>Like example.org</i>."],
  dos=[('<div class="field"><label class="field__label" for="dd1">E-mail</label><input class="input" id="dd1" type="email"></div>', "Visible label.", '<label class="visually-hidden" for="dd2">E-mail</label><input class="input" id="dd2" placeholder="E-mail">', "Placeholder as the only label.")],
  code=('<input class="input" id="org-site" type="url">', [("input", "Base"), ("input--sm / --lg", "Size"), ('aria-invalid="true"', "Invalid"), ("readonly", "Read-only (sunken)"), ("search", "Wrapper with leading icon")]),
  sources=["pages/organization-edit/default", "pages/organization-edit/invalid", "pages/sign-in/default"], drift="None.")

C(id="textarea", name="Textarea", group="Inputs", lead="Multi-line text that grows with its content (field-sizing: content).",
  overview="<p>Summaries, bios, trusted-source lists. Starts at two lines and grows; never scrolls inside until it hits the viewport.</p>",
  anatomy=('<div class="field" style="width:100%;max-width:24rem;"><label class="field__label" for="ta-a">Summary</label><textarea class="textarea" id="ta-a">Global community of Christian technologists.</textarea></div>', [("Label", "Above"), ("Textarea", "Min 2 lines, auto-grow")]),
  variants=[('<div class="field" style="width:20rem;"><label class="field__label" for="ta-b">Bio <span class="optional">(optional)</span></label><textarea class="textarea" id="ta-b" aria-describedby="ta-b-c"></textarea><span class="field__counter" id="ta-b-c">0 / 280</span></div>', "With counter.")],
  sizes="One size; height follows content.",
  states=(FIELD_COLS, [("Textarea", [f'<label class="visually-hidden" for="ta-st{i}">Summary</label><textarea class="textarea" id="ta-st{i}" rows="2" {dict({"Hover": "data-state=\"hover\"", "Focus": "data-state=\"focus\"", "Disabled": "disabled"}, **FX).get(c, "")}>Summary</textarea>' for i, c in enumerate(FIELD_COLS)])]),
  sample='<label class="visually-hidden" for="ta-th">Summary</label><textarea class="textarea" id="ta-th">Summary</textarea>',
  responsive=["Full width of the column at every size."], tokens=[("Border", "--color-border-strong"), ("Min height", "--control-height-md")],
  a11y=dict(pattern="Native <code>&lt;textarea&gt;</code>.", keys=[("Tab", "Leave the field"), ("Enter", "New line")], focus="Shared ring.", label="Visible label; counter linked via aria-describedby.", pairs=[("Text", "--color-fg-default", "--color-bg-surface")], motion="Height changes are instant (no animation).", touch="Resize handle hidden on touch."),
  content=["Help says what the text is for: <i>One sentence.</i>"],
  dos=[('<label class="visually-hidden" for="ta-d1">Bio</label><textarea class="textarea" id="ta-d1">Grows with text</textarea>', "Let it grow.", '<label class="visually-hidden" for="ta-d2">Bio</label><textarea class="textarea" id="ta-d2" rows="1" style="overflow:auto;">Scrolls inside one line</textarea>', "A one-line scrolling box.")],
  code=('<textarea class="textarea" id="org-summary"></textarea>', [("textarea", "Base; field-sizing: content")]), sources=["pages/organization-edit/default", "pages/settings/invalid"], drift="None.")

C(id="select", name="Select", group="Inputs", lead="Native select for short, known lists: type, severity, depth, sort.",
  overview="<p>Use native <code>&lt;select&gt;</code>. For long or searchable lists use the <a href=\"command-palette.html\">palette</a> pattern or a filtered radio list as in <i>Link problem</i>.</p>",
  anatomy=('<div class="field" style="width:16rem;"><label class="field__label" for="se-a">Type</label><select class="select" id="se-a"><option>Community</option></select></div>', [("Label", "Above"), ("Control", "40px, chevron drawn with gradients")]),
  variants=[('<label class="field" style="flex-direction:row;align-items:center;gap:var(--space-2);"><span class="field__label">Sort</span><select class="select input--sm" style="width:auto;" aria-label="Sort"><option>Impact</option></select></label>', "Inline small, for toolbars.")],
  sizes=[('<label class="visually-hidden" for="se-s">S</label><select class="select input--sm" id="se-s" style="width:9rem;"><option>Small</option></select><label class="visually-hidden" for="se-m">M</label><select class="select" id="se-m" style="width:9rem;"><option>Medium</option></select>', "32 / 40px.")],
  states=(["Default", "Hover", "Focus", "Invalid", "Disabled"], [("Select", [f'<label class="visually-hidden" for="se-st{i}">Type</label><select class="select" id="se-st{i}" {a}><option>Community</option></select>' for i, a in enumerate(["", 'data-state="hover"', 'data-state="focus"', 'aria-invalid="true"', "disabled"])])]),
  sample='<label class="visually-hidden" for="se-th">Type</label><select class="select" id="se-th"><option>Community</option></select>',
  responsive=["Native picker on phones."], tokens=[("Border", "--color-border-strong"), ("Chevron", "--color-fg-default")],
  a11y=dict(pattern="Native select.", keys=[("↑ ↓", "Change option"), ("Space / Alt+↓", "Open")], focus="Shared ring.", label="Visible label or aria-label in toolbars.", pairs=[("Border", "--color-border-strong", "--color-bg-surface", 3)], motion="None.", touch="Native."),
  content=["Options in sentence case; most common first."],
  dos=[('<label class="visually-hidden" for="se-d1">Severity</label><select class="select" id="se-d1" style="width:9rem;"><option>Low</option><option>Medium</option><option>High</option></select>', "Ordered by meaning.", '<label class="visually-hidden" for="se-d2">Org</label><select class="select" id="se-d2" style="width:9rem;"><option>1,284 organisations…</option></select>', "Hundreds of options in a select.")],
  code=('<select class="select" id="org-kind">…</select>', [("select", "Base"), ("input--sm", "Small")]), sources=["pages/organization-edit/default", "pages/settings/default"], drift="Person form lists every organisation in a select; flagged to replace with a searchable picker at scale.")

C(id="checkbox", name="Checkbox", group="Inputs", lead="Independent on/off choices and row selection.",
  overview="<p>Use <code>.choice</code> for labelled checkboxes in forms and <code>.row-check</code> for selecting cards in lists.</p>",
  anatomy=('<label class="choice"><input type="checkbox" checked><span class="choice__text">LinkedIn profiles<small>Look up profiles for each person</small></span></label>', [("Box", "20px, --radius-xs"), ("Label", "Body text"), ("Description", "Muted small")]),
  variants=[('<fieldset><legend>Look for</legend><label class="choice"><input type="checkbox" checked><span class="choice__text">Organisations</span></label><label class="choice"><input type="checkbox"><span class="choice__text">People</span></label></fieldset><label class="row-check"><input type="checkbox" aria-label="Select FaithTech" checked></label>', "Group in a fieldset; bare row check.")],
  sizes="One size (20px box, 24px target).",
  states=(["Default", "Hover", "Focus", "Checked", "Indeterminate", "Disabled"], [("Checkbox", [f'<label class="choice"><input type="checkbox" {a}><span class="choice__text">People</span></label>' for a in ["", 'data-state="hover"', 'data-state="focus"', "checked", 'data-state="checked"', "disabled"]])]),
  sample='<label class="choice"><input type="checkbox" checked><span class="choice__text">People</span></label>',
  responsive=["Row checks are always visible on touch; on desktop they show on hover, focus or when any row is checked."], tokens=[("Checked", "--color-accent"), ("Tick", "--color-fg-on-accent"), ("Border", "--color-border-strong")],
  a11y=dict(pattern="Native checkbox inside a <code>&lt;label&gt;</code>; groups in <code>&lt;fieldset&gt;&lt;legend&gt;</code>.", keys=[("Space", "Toggle")], focus="Ring on the box.", label="Row checks use aria-label “Select &lt;name&gt;”.", pairs=[("Tick on accent", "--color-fg-on-accent", "--color-accent"), ("Box border", "--color-border-strong", "--color-bg-surface", 3)], motion="Fill over --duration-fast.", touch="Whole label is the target."),
  content=["Label states the choice, not an instruction."],
  dos=[('<label class="choice"><input type="checkbox" checked><span class="choice__text">Require two sources</span></label>', "Positive phrasing.", '<label class="choice"><input type="checkbox"><span class="choice__text">Don\'t skip single sources</span></label>', "Double negative.")],
  code=('<label class="choice"><input type="checkbox"><span class="choice__text">People</span></label>', [("choice", "Labelled control"), ("row-check", "Bare selection box")]), sources=["dialogs/run-research/default", "pages/organizations/selected"], drift="None.")

C(id="radio-group", name="Radio group", group="Inputs", lead="One choice from a short visible list, with optional descriptions.",
  overview="<p>Used for research question, depth and export format. Card-style radios carry a description.</p>",
  anatomy=('<fieldset><legend>Depth</legend><label class="choice"><input type="radio" name="ra" checked><span class="choice__text">Standard<small>about 5 minutes</small></span></label></fieldset>', [("Legend", "Names the group"), ("Radio", "20px circle"), ("Description", "Muted small")]),
  variants=[('<label class="choice card lift" style="padding:var(--space-4);"><input type="radio" name="rb" checked><span class="choice__text"><strong>Standard</strong><small>about 5 minutes · 2 sources per fact</small></span></label>', "Card-style option.")],
  sizes="One size.",
  states=(["Default", "Hover", "Focus", "Checked", "Invalid", "Disabled"], [("Radio", [f'<label class="choice"><input type="radio" name="rs{i}" {a}><span class="choice__text">Quick</span></label>' for i, a in enumerate(["", 'data-state="hover"', 'data-state="focus"', "checked", 'aria-invalid="true"', "disabled"])])]),
  sample='<label class="choice"><input type="radio" name="rth" checked><span class="choice__text">Standard</span></label>',
  responsive=["Two radio groups side by side collapse into one column under 640px."], tokens=[("Checked", "--color-accent"), ("Dot", "--color-fg-on-accent")],
  a11y=dict(pattern="Native radios in a fieldset.", keys=[("↑ ↓ ← →", "Move and select"), ("Tab", "Leave the group")], focus="Ring on the circle.", label="Legend names the group; error linked to the fieldset.", pairs=[("Dot on accent", "--color-fg-on-accent", "--color-accent")], motion="Fill over --duration-fast.", touch="Card radios make the whole card the target."),
  content=["Order by frequency or by size (Quick, Standard, Deep)."],
  dos=[('<fieldset><legend>Format</legend><label class="choice"><input type="radio" name="rd1" checked><span class="choice__text">CSV</span></label></fieldset>', "A legend and a sensible default.", '<label class="choice"><input type="radio" name="rd2"><span class="choice__text">CSV</span></label>', "Orphan radio without a group label.")],
  code=('<fieldset><legend>Depth</legend><label class="choice"><input type="radio" name="depth">…</label></fieldset>', [("choice", "Labelled radio")]), sources=["dialogs/run-research/default", "pages/people/default", "dialogs/link-problem/invalid"], drift="None.")

C(id="switch", name="Switch", group="Inputs", lead="Settings that take effect on save: notifications, motion, the WebGPU field.",
  overview="<p>The label describes the setting (<i>Animate the field</i>), never the action.</p>",
  anatomy=('<label class="switch"><input type="checkbox" role="switch" checked><span>Animate the field (WebGPU)</span></label>', [("Track", "44×24, accent when on"), ("Thumb", "20px, slides"), ("Label", "Right")]),
  variants=[('<label class="switch"><input type="checkbox" role="switch"><span>Weekly digest by e-mail</span></label>', "Off.")],
  sizes="One size.",
  states=(["Off", "On", "Focus", "Disabled"], [("Switch", [f'<label class="switch"><input type="checkbox" role="switch" {a}><span>Reduce motion</span></label>' for a in ["", "checked", 'data-state="focus"', "disabled"]])]),
  sample='<label class="switch"><input type="checkbox" role="switch" checked><span>On</span></label>',
  responsive=["Label wraps; switch stays top-aligned."], tokens=[("On", "--color-accent"), ("Off", "--color-border-strong"), ("Thumb", "--color-bg-surface")],
  a11y=dict(pattern="Checkbox with <code>role=\"switch\"</code>.", keys=[("Space", "Toggle")], focus="Ring on the track.", label="Wrapping label.", pairs=[("Off track", "--color-border-strong", "--color-bg-surface", 3), ("On track", "--color-accent", "--color-bg-surface", 3)], motion="Thumb slides over --duration-base.", touch="Whole row is the target."),
  content=["Describe the state when on: <i>When a run finishes</i>."],
  dos=[('<label class="switch"><input type="checkbox" role="switch" checked><span>Animate the field</span></label>', "Describes the setting.", '<label class="switch"><input type="checkbox" role="switch"><span>Turn off animation</span></label>', "Describes an action; inverts meaning.")],
  code=('<label class="switch"><input type="checkbox" role="switch"><span>…</span></label>', [("switch", "Wrapper")]), sources=["pages/settings/default"], drift="Mocks omitted role=\"switch\"; added here.")

C(id="file-upload", name="File upload", group="Inputs", lead="Choose a CSV to import, with a column-mapping preview and determinate progress.",
  overview="<p>The native file input is the control. Progress and results live in the <a href=\"dialog.html\">import dialog</a>.</p>",
  anatomy=('<div class="field" style="width:22rem;"><label class="field__label" for="fu-a">CSV file</label><input class="input" id="fu-a" type="file" accept=".csv" aria-describedby="fu-a-h"><span class="field__help" id="fu-a-h">Up to 5,000 rows.</span></div>', [("Label", "Names the file type"), ("Input", "Native"), ("Help", "Limits and columns")]),
  variants=[('<div class="stack" style="width:22rem;"><div class="cluster cluster--between"><span>organisations.csv</span><span class="text-caption">120 of 312</span></div><div class="progress" role="progressbar" aria-label="Import progress" aria-valuenow="38" aria-valuemin="0" aria-valuemax="100"><div class="progress__bar" style="--value:38%"></div></div></div>', "Uploading.")],
  sizes="One size.",
  states=(["Default", "Invalid", "Uploading", "Failed"], [("Upload", ['<label class="visually-hidden" for="fu-1">CSV</label><input class="input" id="fu-1" type="file">', '<label class="visually-hidden" for="fu-2">CSV</label><input class="input" id="fu-2" type="file" aria-invalid="true">', '<div class="progress" role="progressbar" aria-label="Upload" aria-valuenow="38" aria-valuemin="0" aria-valuemax="100" style="width:8rem;"><div class="progress__bar" style="--value:38%"></div></div>', '<span class="inline-status inline-status--danger">Stopped at row 41</span>'])]),
  sample='<label class="visually-hidden" for="fu-th">CSV</label><input class="input" id="fu-th" type="file">',
  responsive=["Preview table scrolls inside its wrapper on phones."], tokens=[("Progress", "--color-accent"), ("Error", "--color-danger-fg")],
  a11y=dict(pattern="Native file input.", keys=[("Enter / Space", "Open the picker")], focus="Shared ring.", label="Visible label; errors via aria-describedby.", pairs=[("Error text", "--color-danger-fg", "--color-bg-surface-raised")], motion="Progress width over --duration-slow.", touch="Native picker."),
  content=["Errors say the row and the fix: <i>Row 41: “Website” isn't a URL.</i>"],
  dos=[('<span class="field__error">This file has no Name column.</span>', "Specific error.", '<span class="field__error">Invalid file.</span>', "Vague error.")],
  code=('<input class="input" type="file" accept=".csv">', [("input", "Styled file input"), ("progress", "Upload progress")]), sources=["dialogs/import-csv/default", "dialogs/import-csv/failed"], drift="None.")

C(id="form-field", name="Form field", group="Inputs", lead="Label, control, help, error and counter, spaced 4px apart.",
  overview="<p>The wrapper every input uses. Optional fields say so in the label; required is the default.</p>",
  anatomy=('<div class="field" style="width:20rem;"><label class="field__label" for="ff-a">Name</label><input class="input" id="ff-a" aria-invalid="true" aria-describedby="ff-a-e"><span class="field__error" id="ff-a-e">Enter a name</span></div>', [("Label", "--text-label"), ("Control", "Any input"), ("Error", "⚠ + text, --color-danger-fg"), ("Gap", "--space-1")]),
  variants=[('<div class="field" style="width:16rem;"><label class="field__label" for="ff-b">Founded <span class="optional">(optional)</span></label><input class="input" id="ff-b" inputmode="numeric"></div>', "Optional marker.")],
  sizes="Inherits the control size.",
  states=(["Default", "With help", "Invalid"], [("Field", ['<div class="field"><label class="field__label" for="ff-1">Name</label><input class="input" id="ff-1"></div>', '<div class="field"><label class="field__label" for="ff-2">Website</label><input class="input" id="ff-2" aria-describedby="ff-2h"><span class="field__help" id="ff-2h">Like example.org</span></div>', '<div class="field"><label class="field__label" for="ff-3">Website</label><input class="input" id="ff-3" aria-invalid="true" aria-describedby="ff-3e"><span class="field__error" id="ff-3e">Enter a website like example.org</span></div>'])]),
  sample='<div class="field"><label class="field__label" for="ff-th">Name</label><input class="input" id="ff-th"></div>',
  responsive=["Labels stay above the control at every width."], tokens=[("Label", "--color-fg-default"), ("Help", "--color-fg-muted"), ("Error", "--color-danger-fg"), ("Gap", "--space-1")],
  a11y=dict(pattern="Label + aria-describedby (help then error).", keys=[("Tab", "Into the control")], focus="On the control.", label="Required by default; optional said in words.", pairs=[("Error text", "--color-danger-fg", "--color-bg-surface"), ("Help text", "--color-fg-muted", "--color-bg-surface")], motion="None.", touch="Label tap focuses the control."),
  content=["Error = what to do: <i>Enter a website like example.org</i>."],
  dos=[('<span class="field__error">Enter a name</span>', "Instruction.", '<span class="field__error">Name is invalid</span>', "Blame without help.")],
  code=('<div class="field"><label class="field__label" for="x">…</label>…</div>', [("field", "Wrapper"), ("field__label / __help / __error / __counter", "Parts"), ("optional", "Optional marker")]), sources=["pages/organization-edit/invalid", "pages/person-edit/invalid"], drift="None.")

C(id="form-layout", name="Form layout", group="Inputs", lead="One column, 24px between fields, error summary first, actions last.",
  overview="<p>Forms live in a 44rem card. Two- and three-column grids are used only for short related fields (City/Country, Reach/Severity/Tractability).</p>",
  anatomy=(f'<div class="card stack" style="max-width:24rem;gap:var(--space-4);"><div class="alert alert--danger form-summary" role="alert">{icon("danger")}<div class="alert__body"><div class="alert__title">Fix 1 thing to save</div><a href="#overview">Enter a name</a></div></div><div class="field"><label class="field__label" for="fl-a">Name</label><input class="input" id="fl-a" aria-invalid="true"></div><div class="form-actions"><button class="btn" type="button">Cancel</button><button class="btn btn--primary" type="button">Save</button></div></div>',
           [("Error summary", "Links to each field; receives focus"), ("Fields", "--space-6 apart"), ("Actions", "Right-aligned; saved status left")]),
  variants=[(f'<div class="form-actions" style="width:100%;justify-content:space-between;align-items:center;"><span class="inline-status inline-status--success">{icon("success", "icon icon--sm")} Saved · just now</span><button class="btn btn--primary" type="button">Save</button></div>', "Success: inline saved status.")],
  sizes="Max width 44rem.",
  states=(["Default", "Submitting", "Invalid"], [("Actions", ['<button class="btn btn--primary" type="button">Save</button>', '<button class="btn btn--primary" type="button" aria-busy="true">Save</button>', '<span class="inline-status inline-status--danger">Fix 2 things</span>'])]),
  sample='<div class="form-actions"><button class="btn" type="button">Cancel</button><button class="btn btn--primary" type="button">Save</button></div>',
  responsive=["Multi-column field grids collapse to one column under 640px.", "Actions wrap; primary stays last."], tokens=[("Summary edge", "--color-danger-solid"), ("Field gap", "--space-6")],
  a11y=dict(pattern="<code>&lt;form novalidate&gt;</code> with custom messages; summary has <code>role=\"alert\" tabindex=\"-1\"</code>.", keys=[("Enter", "Submit"), ("Tab", "Next field")], focus="Moves to the summary on failed submit.", label="Each summary item links to its field id.", pairs=[("Summary text", "--color-danger-fg", "--color-danger-bg")], motion="None.", touch="Actions 40px+."),
  content=["Summary title counts: <i>Fix 2 things to save</i>."],
  dos=[('<button class="btn btn--primary" type="button" aria-busy="true">Save</button>', "Busy keeps width; fields go read-only.", '<span class="spinner spinner--lg" aria-hidden="true"></span>', "A page spinner replacing the form.")],
  code=('<form class="stack card" novalidate>…<div class="form-actions">…</div></form>', [("form-summary", "Error summary"), ("form-actions", "Action bar"), ("inline-status", "Saved indicator")]), sources=["pages/organization-edit/invalid", "pages/organization-edit/submitting", "pages/settings/success"], drift="None.")

# ============================================================================ Navigation
C(id="top-bar", name="Top bar", group="Navigation", lead="The only app chrome: brand, seven links, search, notifications, account. Blurred, sticky, shadow only once scrolled.",
  overview="<p>Harvest Map has no sidebar on desktop; the top bar holds navigation. Under 768px the links move into the <a href=\"drawer.html\">navigation drawer</a>.</p>",
  anatomy=(f'<header class="topbar" style="position:relative;width:100%;"><a class="topbar__brand" href="#overview">{icon("wheat", "icon icon--lg")}<span>Harvest Map</span></a><nav class="topbar__nav" aria-label="Primary sample"><a class="nav-link" href="#overview" aria-current="page">Field</a><a class="nav-link" href="#overview">Orgs</a></nav><span class="topbar__spacer"></span><a class="btn btn--ghost btn--icon" href="#overview" aria-label="Search">{icon("search")}</a><a class="avatar avatar--sm" href="#overview" aria-label="Account">NA</a></header>',
           [("Brand", "Wheat mark + name (name hidden under 1024px)"), ("Primary nav", "Nav links; current = accent-subtle"), ("Utilities", "Search ⌘K, bell with count, avatar")]),
  variants=[(f'<header class="topbar" style="position:relative;width:100%;"><a class="btn btn--ghost btn--icon" href="#overview" aria-label="Open navigation">{icon("menu")}</a><a class="topbar__brand" href="#overview" aria-label="Harvest Map">{icon("wheat", "icon icon--lg")}</a><span class="topbar__spacer"></span><a class="btn btn--ghost btn--icon" href="#overview" aria-label="Search">{icon("search")}</a></header>', "Compact (phone).")],
  sizes="64px tall (--layout-topbar-height).",
  states=(["Default", "Hover", "Current"], [("Nav link", ['<a class="nav-link" href="#overview">People</a>', '<a class="nav-link" href="#overview" data-state="hover">People</a>', '<a class="nav-link" href="#overview" aria-current="page">People</a>'])]),
  sample='<a class="nav-link" href="#overview" aria-current="page">Field</a><a class="nav-link" href="#overview">Orgs</a>',
  responsive=["< 768px: menu button, mark, search, bell, avatar.", "768–1023px: inline nav, small labels, mark only.", "≥ 1024px: full brand and 24px gaps.", "Shadow appears via <code>@container scroll-state(stuck: top)</code> (Chrome 133+)."],
  tokens=[("Background", "--color-bg-surface"), ("Height", "--layout-topbar-height"), ("Current link", "--color-accent-subtle"), ("Link text", "--color-fg-muted")],
  a11y=dict(pattern="<code>&lt;header&gt;</code> with <code>&lt;nav aria-label=\"Primary\"&gt;</code>; current link <code>aria-current=\"page\"</code>.", keys=[("Tab", "Through links"), ("⌘K", "Open palette")], focus="Shared ring; skip link precedes it.", label="Icon buttons labelled (“Notifications, 2 unread”).", pairs=[("Link text", "--color-fg-muted", "--color-bg-surface"), ("Current link", "--color-fg-accent", "--color-accent-subtle")], motion="Brand and page title morph across pages with view transitions.", touch="Links 40px tall."),
  content=["Nav labels are one word: Field, Orgs, People."],
  dos=[('<a class="nav-link" href="#overview" aria-current="page">Orgs</a>', "aria-current marks the page.", '<a class="nav-link" href="#overview" style="font-weight:700;">Orgs</a>', "Bold text as the only cue.")],
  code=('<header class="topbar">…</header>', [("topbar", "Bar"), ("topbar__brand / __nav / __spacer / __menu", "Parts"), ("nav-link", "Link")]), sources=["pages/field/default", "pages/organizations/default"], drift="Tooltips inside the bar widened the page at 360px; fixed by hiding them from layout and anchoring right.")

C(id="sidebar-navigation", name="Sidebar navigation", group="Navigation", lead="Vertical list of nav links with groups and counts. Used inside the navigation drawer.",
  overview="<p>Harvest Map uses it in the phone drawer, not as a permanent sidebar. It is the same <code>.nav-link</code> as the top bar.</p>",
  anatomy=(f'<nav class="stack" style="gap:var(--space-1);width:16rem;" aria-label="Sample"><a class="nav-link" href="#overview" aria-current="page">{icon("home")}Field</a><a class="nav-link" href="#overview">{icon("building")}Organizations</a><div class="sidebar__group">Account</div><a class="nav-link" href="#overview">{icon("bell")}Notifications <span class="badge badge--count" aria-label="2 unread">2</span></a></nav>',
           [("Link", "Icon + label, 44px"), ("Group", "Overline heading"), ("Count", "Badge with aria-label")]),
  variants=[(f'<a class="nav-link" href="#overview">{icon("settings")}Settings</a>', "Single link.")], sizes="One size (44px links).",
  states=(["Default", "Hover", "Current"], [("Link", [f'<a class="nav-link" href="#overview" {a}>{icon("people")}People</a>' for a in ["", 'data-state="hover"', 'aria-current="page"']])]),
  sample=f'<a class="nav-link" href="#overview" aria-current="page">{icon("home")}Field</a>',
  responsive=["Only shown inside the drawer under 768px."], tokens=[("Current", "--color-accent-subtle"), ("Group label", "--color-fg-subtle")],
  a11y=dict(pattern="<code>&lt;nav&gt;</code> list of links, <code>aria-current</code>.", keys=[("Tab", "Move")], focus="Shared ring.", label="Counts have meaning in aria-label.", pairs=[("Group label", "--color-fg-subtle", "--color-bg-surface-raised")], motion="None.", touch="44px rows."),
  content=["Same labels as the top bar, expanded (Orgs → Organizations)."],
  dos=[('<span class="badge badge--count" aria-label="2 unread">2</span>', "Count with meaning.", '<span class="badge badge--count">2</span>', "Bare number.")],
  code=('<a class="nav-link" href="…" aria-current="page">…</a>', [("nav-link", "Link"), ("sidebar__group", "Group heading")]), sources=["dialogs/nav-sheet/default"], drift="None.")

C(id="tabs", name="Tabs", group="Navigation", lead="Switch between views of one record. Core component; the mocks use filter chips instead so far.",
  overview="<p>Use tabs when the panels are peers of one object. For filtering a list, use <a href=\"chip.html\">chips</a>.</p>",
  anatomy=('<div class="tabs" role="tablist" aria-label="Organisation"><button class="tab" role="tab" aria-selected="true" type="button">Overview</button><button class="tab" role="tab" aria-selected="false" tabindex="-1" type="button">People <span class="badge">2</span></button></div>', [("Tab", "44px, label + count"), ("Indicator", "2px accent underline")]),
  variants=[('<div class="tabs" role="tablist" aria-label="Sources"><button class="tab" role="tab" aria-selected="true" type="button">Verified</button><button class="tab" role="tab" aria-selected="false" tabindex="-1" type="button">Pending</button><button class="tab" role="tab" aria-selected="false" tabindex="-1" type="button">Rejected</button></div>', "Underline tabs.")],
  sizes="One size.",
  states=(["Default", "Hover", "Focus", "Selected"], [("Tab", [f'<button class="tab" type="button" {a}>People</button>' for a in ["", 'data-state="hover"', 'data-state="focus"', 'aria-selected="true"']])]),
  sample='<div class="tabs" role="tablist" aria-label="Theme sample"><button class="tab" role="tab" aria-selected="true" type="button">One</button><button class="tab" role="tab" aria-selected="false" tabindex="-1" type="button">Two</button></div>',
  responsive=["Scroll horizontally under 640px; no wrapping."], tokens=[("Selected text", "--color-fg-accent"), ("Indicator", "--color-accent")],
  a11y=dict(pattern="APG Tabs, automatic activation.", keys=[("← →", "Move and activate"), ("Home / End", "First / last")], focus="Roving tabindex.", label="tablist has aria-label.", pairs=[("Selected", "--color-fg-accent", "--color-bg-canvas"), ("Unselected", "--color-fg-muted", "--color-bg-canvas")], motion="Indicator colour over --duration-fast.", touch="44px tall."),
  content=["Nouns; counts in a badge."],
  dos=[('<div class="tabs" role="tablist" aria-label="d1"><button class="tab" role="tab" aria-selected="true" type="button">People</button></div>', "Peers of one record.", '<div class="tabs" role="tablist" aria-label="d2"><button class="tab" role="tab" aria-selected="true" type="button">AI</button><button class="tab" role="tab" aria-selected="false" type="button">Youth</button></div>', "Tabs used as filters.")],
  code=('<div class="tabs" role="tablist">…</div>', [("tabs", "List"), ("tab", "Tab")]), sources=["pages/organization/default"], drift="Not used in mocks yet.")

C(id="breadcrumb", name="Breadcrumb", group="Navigation", lead="Where a detail or edit page sits: Organizations / FaithTech / Edit.",
  overview="<p>Shown on detail and edit pages only. List pages are top-level and have none.</p>",
  anatomy=('<nav aria-label="Breadcrumb"><ol class="breadcrumb"><li><a href="#overview">Organizations</a></li><li><a href="#overview">FaithTech</a></li><li aria-current="page">Edit</li></ol></nav>', [("Ancestors", "Muted links"), ("Separator", "/"), ("Current", "Bold, not a link")]),
  variants=[('<nav aria-label="Breadcrumb two"><ol class="breadcrumb"><li><a href="#overview">People</a></li><li aria-current="page">Pat Gelsinger</li></ol></nav>', "Two levels.")], sizes="One size (body-sm).",
  states=(["Default", "Hover", "Current"], [("Crumb", ['<ol class="breadcrumb"><li><a href="#overview">People</a></li></ol>', '<ol class="breadcrumb"><li><a href="#overview" data-state="hover">People</a></li></ol>', '<ol class="breadcrumb"><li aria-current="page">Pat Gelsinger</li></ol>'])]),
  sample='<ol class="breadcrumb"><li><a href="#overview">People</a></li><li aria-current="page">Pat</li></ol>',
  responsive=["Wraps; long names keep full text."], tokens=[("Ancestor", "--color-fg-muted"), ("Current", "--color-fg-default")],
  a11y=dict(pattern="<code>&lt;nav aria-label=\"Breadcrumb\"&gt;&lt;ol&gt;</code>, current <code>aria-current=\"page\"</code>.", keys=[("Tab", "Through links")], focus="Shared ring.", label="Nav labelled Breadcrumb.", pairs=[("Ancestor", "--color-fg-muted", "--color-bg-canvas")], motion="None.", touch="24px line box."),
  content=["Use the record name, not the route."],
  dos=[('<ol class="breadcrumb"><li><a href="#overview">Organizations</a></li><li aria-current="page">FaithTech</li></ol>', "Record names.", '<ol class="breadcrumb"><li><a href="#overview">Home</a></li><li><a href="#overview">Orgs</a></li><li><a href="#overview">ID 42</a></li></ol>', "Routes and ids.")],
  code=('<nav aria-label="Breadcrumb"><ol class="breadcrumb">…</ol></nav>', [("breadcrumb", "List")]), sources=["pages/organization/default", "pages/organization-edit/default"], drift="None.")

C(id="pagination", name="Pagination", group="Navigation", lead="25 per page with a count; virtualises beyond 200 rows but keeps page links for deep linking.",
  overview="<p>Shown only when a list exceeds one page.</p>",
  anatomy=('<nav class="cluster cluster--between" aria-label="Pagination" style="width:100%;"><span class="text-caption">Showing 1–25 of 1,284</span><ul class="pagination"><li><a href="#overview" aria-disabled="true" aria-label="Previous page">‹</a></li><li><a href="#overview" aria-current="page">1</a></li><li><a href="#overview">2</a></li><li><a href="#overview" aria-label="Next page">›</a></li></ul></nav>', [("Count", "Range of total"), ("Pages", "32px squares"), ("Prev/next", "Labelled")]),
  variants=[('<ul class="pagination"><li><a href="#overview" aria-current="page">1</a></li><li><span aria-hidden="true">…</span></li><li><a href="#overview">52</a></li></ul>', "With ellipsis.")], sizes="One size.",
  states=(["Default", "Hover", "Current", "Disabled"], [("Page", ['<ul class="pagination"><li><a href="#overview">2</a></li></ul>', '<ul class="pagination"><li><a href="#overview" data-state="hover">2</a></li></ul>', '<ul class="pagination"><li><a href="#overview" aria-current="page">1</a></li></ul>', '<ul class="pagination"><li><a href="#overview" aria-disabled="true" aria-label="Previous page">‹</a></li></ul>'])]),
  sample='<ul class="pagination"><li><a href="#overview" aria-current="page">1</a></li><li><a href="#overview">2</a></li></ul>',
  responsive=["Under 640px show prev, current, next only."], tokens=[("Current", "--color-accent-subtle"), ("Text", "--color-fg-muted")],
  a11y=dict(pattern="<code>&lt;nav aria-label=\"Pagination\"&gt;</code>.", keys=[("Tab", "Through pages")], focus="Shared ring.", label="Arrows labelled.", pairs=[("Current", "--color-fg-accent", "--color-accent-subtle")], motion="None.", touch="32px + spacing ≥ 24px target."),
  content=["Count with separators: 1,284."],
  dos=[('<span class="text-caption">Showing 1–25 of 1,284</span>', "Say where you are.", '<span class="text-caption">Page 1</span>', "No sense of size.")],
  code=('<ul class="pagination">…</ul>', [("pagination", "List")]), sources=["pages/organizations/long", "pages/people/long"], drift="None.")

C(id="skip-link", name="Skip link", group="Navigation", lead="First focusable element on every page; jumps to #main.",
  overview="<p>Hidden until focused, then slides in at the top-left.</p>",
  anatomy=('<a class="skip-link" href="#overview" style="position:static;">Skip to content</a>', [("Link", "Inverse surface, --shadow-3")]),
  variants=[('<a class="skip-link" href="#overview" style="position:static;">Skip to content</a>', "Only variant.")], sizes="One size.",
  states=(["Focused"], [("Skip link", ['<a class="skip-link" href="#overview" style="position:static;" data-state="focus">Skip to content</a>'])]),
  sample='<a class="skip-link" href="#overview" style="position:static;">Skip to content</a>',
  responsive=["Same at all widths."], tokens=[("Background", "--color-bg-surface"), ("Shadow", "--shadow-3")],
  a11y=dict(pattern="Same-page link to <code>#main</code>.", keys=[("Tab", "Reveal (first stop)"), ("Enter", "Jump")], focus="Visible on focus only.", label="“Skip to content”.", pairs=[("Text", "--color-fg-link", "--color-bg-surface")], motion="Slides in over --duration-fast.", touch="Not shown to touch users."),
  content=["Always “Skip to content”."],
  dos=[('<a class="skip-link" href="#overview" style="position:static;">Skip to content</a>', "First in the DOM.", '<span class="text-muted">No skip link</span>', "Leaving it out.")],
  code=('<a class="skip-link" href="#main">Skip to content</a>', [("skip-link", "Hidden until focus")]), sources=["pages/field/default"], drift="None.")

# ============================================================================ Containers & overlays
C(id="card", name="Card", group="Containers", lead="White surface, 20px radius, hairline border, a lift on hover.",
  overview="<p>Groups one thing. Clickable cards have one real link (the name); the lift is decoration.</p>",
  anatomy=('<div class="card lift" style="max-width:20rem;"><div class="card__header"><h3 class="card__title">Profile</h3></div><p class="text-muted">Name and e-mail.</p></div>', [("Surface", "--color-bg-surface, --radius-lg"), ("Border", "1px --color-border-default"), ("Padding", "--space-6 (32 in forms)")]),
  variants=[('<div class="card" style="width:12rem;">Default</div><div class="card lift" style="width:12rem;">Interactive (lift)</div><div class="card card--selected" style="width:12rem;">Selected</div><div class="card card--archived" style="width:12rem;">Archived</div>', "Default, interactive, selected, archived.")],
  sizes="Padding --space-6 default; --space-8 for answer and form cards.",
  states=(["Default", "Hover", "Selected"], [("Card", ['<div class="card lift">FaithTech</div>', '<div class="card lift" data-state="hover">FaithTech</div>', '<div class="card" aria-selected="true">FaithTech</div>'])]),
  sample='<div class="card lift" style="width:12rem;">Card</div>',
  responsive=["Full width under 640px; grids use auto-fill minmax(19rem, 1fr)."], tokens=[("Surface", "--color-bg-surface"), ("Border", "--color-border-default"), ("Radius", "--radius-lg"), ("Shadow", "--shadow-1"), ("Hover shadow", "--shadow-2")],
  a11y=dict(pattern="Plain container; the link inside is the control.", keys=[("Tab", "To the link inside")], focus="Lift also on :focus-within.", label="—", pairs=[("Text on card", "--color-fg-default", "--color-bg-surface")], motion="Lift 2px with --ease-spring-linear.", touch="No hover dependency."),
  content=["One idea per card."],
  dos=[('<div class="card lift"><a href="#overview">FaithTech</a></div>', "One link inside.", '<a class="card" href="#overview"><button class="btn btn--sm" type="button">Edit</button></a>', "Button nested inside a link card.")],
  code=('<div class="card lift">…</div>', [("card", "Surface"), ("lift", "Hover lift"), ("card--selected / --archived / --flush", "Variants")]), sources=["pages/organizations/default", "pages/settings/default"], drift="None.")

C(id="entity-card", name="Entity card", group="Data display", lead="One organisation, person or problem in a list: mark, name, meta, tags, status, arrow.",
  overview="<p>The workhorse of every list page. Grid on desktop, wrapping flex on phones so status drops under the name.</p>",
  anatomy=(f'<div class="card lift" style="padding:0;width:100%;max-width:36rem;"><div class="org-card"><span class="mark" aria-hidden="true">FT</span><div><a class="org-card__name" href="#overview" style="text-decoration:none;color:inherit;">FaithTech</a><div class="org-card__meta">Community · Waterloo · 50+ cities</div><div class="tags"><span class="tag tag--ai">AI</span><span class="tag">Youth</span></div></div><div class="org-card__end"><span class="verify verify--verified">Verified</span>{icon("arrow", "icon text-subtle")}</div></div></div>',
           [("Mark", "48px initials tile"), ("Name", "h4, the link"), ("Meta", "Type · place · reach"), ("Tags", "AI, Moonshot highlighted"), ("End", "Status + arrow")]),
  variants=[(f'<div class="card" style="padding:0;width:100%;max-width:36rem;"><div class="org-card" style="grid-template-columns:auto 1fr auto auto;"><span class="avatar" aria-hidden="true">PG</span><div><a href="#overview" style="font:var(--text-h4);text-decoration:none;color:inherit;">Pat Gelsinger</a><div class="people-row__role">Executive Chair · Gloo</div></div><span class="verify verify--verified">Verified</span><a class="linkedin" href="#overview">LinkedIn</a></div></div>', "Person row."),
            ('<div class="card" style="padding:0;width:100%;max-width:36rem;"><div class="org-card" style="grid-template-columns:2rem auto 1fr;"><span class="text-subtle">1</span><span class="score" style="--score:94" role="img" aria-label="Impact score 94 of 100" data-rank="1"><span>94</span></span><div><span class="org-card__name">Scripture in every language</span><div class="org-card__meta">3,800 languages · Tracked</div></div></div></div>', "Problem row.")],
  sizes="One size; padding 20/24px.",
  states=(["Default", "Hover", "Selected"], [("Entity", ['<div class="card lift" style="padding:var(--space-4);">FaithTech</div>', '<div class="card lift" data-state="hover" style="padding:var(--space-4);">FaithTech</div>', '<div class="card" aria-selected="true" style="padding:var(--space-4);">FaithTech</div>'])]),
  sample='<div class="card" style="padding:0;"><div class="org-card"><span class="mark" aria-hidden="true">GL</span><div><span class="org-card__name">Gloo</span><div class="org-card__meta">Platform · Boulder</div></div></div></div>',
  responsive=["≥ 640px: grid (check, mark, body, end).", "< 640px: flex-wrap; end group moves to its own line, right-aligned."], tokens=[("Mark background", "--color-accent-subtle"), ("Mark text", "--color-fg-accent"), ("Meta", "--color-fg-muted")],
  a11y=dict(pattern="Card containing one link (the name) and optional row checkbox.", keys=[("Tab", "Name link, then status actions")], focus="Card lifts on focus-within.", label="Row check aria-label “Select &lt;name&gt;”.", pairs=[("Mark text", "--color-fg-accent", "--color-accent-subtle"), ("Meta", "--color-fg-muted", "--color-bg-surface")], motion="Staggered rise on entry (--stagger).", touch="Name link 24px+ line."),
  content=["Meta order: type · place · reach.", "Long names wrap; never truncate without a title."],
  dos=[('<span class="org-card__meta">Community · Waterloo · 50+ cities</span>', "Three facts, fixed order.", '<span class="org-card__meta">50+ cities, Waterloo (Canada), a Community founded 2016</span>', "Sentence meta.")],
  code=('<div class="card lift"><div class="org-card">…</div></div>', [("org-card", "Row grid"), ("mark", "Initials tile"), ("org-card__name / __meta / __end", "Parts")]), sources=["pages/organizations/default", "pages/organizations/edge", "pages/people/default", "pages/problems/default"], drift="People and problem rows override grid-template-columns inline; promoted to documented variants.")

C(id="question-card", name="Question card", group="Data display", lead="One of the six research questions with its current answer as a big number.",
  overview="<p>The Field page's core. Number, question, answer + unit, status and source count.</p>",
  anatomy=('<a class="card q-card lift" href="#overview" style="max-width:20rem;" data-status="answered"><span class="q-card__n">01</span><span class="q-card__q">Who is helping Christian youth, especially with AI?</span><div class="q-card__a"><span class="q-card__num">9</span><span class="q-card__unit">organisations</span></div><div class="q-card__foot"><span>Answered</span><span>23 sources</span></div></a>',
           [("Number", "Overline"), ("Question", "h4, balanced"), ("Answer", "h2 tabular + unit"), ("Foot", "Status · sources")]),
  variants=[('<a class="card q-card" href="#overview" style="max-width:20rem;" data-status="open"><span class="q-card__n">06</span><span class="q-card__q">Where are they on LinkedIn?</span><div class="q-card__a"><span class="q-card__num">—</span><span class="q-card__unit">open</span></div><div class="q-card__foot"><span>Open</span><span>0 sources</span></div></a>', "Open: subtle dash.")],
  sizes="Min height 14rem; 32px padding.",
  states=(["Answered", "Hover", "Open"], [("Question", ['<a class="card q-card lift" href="#overview" data-status="answered"><span class="q-card__num">9</span></a>', '<a class="card q-card lift" href="#overview" data-state="hover"><span class="q-card__num">9</span></a>', '<a class="card q-card" href="#overview" data-status="open"><span class="q-card__num">—</span></a>'])]),
  sample='<a class="card q-card" href="#overview"><span class="q-card__num">16</span><span class="q-card__unit">people</span></a>',
  responsive=["auto-fill minmax(19rem, 1fr): 3 / 2 / 1 columns."], tokens=[("Number", "--color-fg-default"), ("Open number", "--color-fg-subtle"), ("Number label", "--color-fg-subtle")],
  a11y=dict(pattern="Whole card is one link to the answer.", keys=[("Enter", "Open")], focus="Ring around the card.", label="Link text is the question + answer.", pairs=[("Foot", "--color-fg-subtle", "--color-bg-surface")], motion="Staggered rise.", touch="Whole card target."),
  content=["Questions end with “?”; units are plural nouns."],
  dos=[('<span class="q-card__num">9</span><span class="q-card__unit">organisations</span>', "Number + unit.", '<span class="q-card__num">Nine orgs found!</span>', "Sentence instead of a number.")],
  code=('<a class="card q-card lift" data-status="answered">…</a>', [("q-card", "Layout"), ('data-status="open"', "Unanswered")]), sources=["pages/field/default", "pages/field/empty"], drift="None.")

C(id="dialog", name="Dialog", group="Containers", lead="Modal: centred and scaled in on desktop, bottom sheet under 640px. Page behind is inert.",
  overview="<p>For confirmations, short forms and review. Destructive dialogs require typing the name. Prefer a page for long forms.</p>",
  anatomy=(f'<div class="dialog__panel" style="position:relative;max-width:26rem;animation:none;"><div class="dialog__header"><div class="dialog__icon dialog__icon--danger" aria-hidden="true">{icon("warning")}</div><div style="flex:1;"><h3 class="dialog__title">Delete FaithTech?</h3><p class="text-muted">This can\'t be undone.</p></div><button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{icon("close")}</button></div><div class="dialog__body"><p>Removes 3 sources.</p></div><div class="dialog__footer"><button class="btn" type="button">Cancel</button><button class="btn btn--danger" type="button">Delete organisation</button></div></div>',
           [("Header", "Icon, title (h2 in product), description, close"), ("Body", "Scrolls"), ("Footer", "Sticky; cancel then confirm")]),
  variants=[(f'<div class="dialog__panel" style="position:relative;max-width:26rem;animation:none;"><div class="dialog__header"><div style="flex:1;"><h3 class="dialog__title">Add person</h3></div><button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{icon("close")}</button></div><div class="dialog__body"><div class="field"><label class="field__label" for="dl-a">Name</label><input class="input" id="dl-a"></div></div><div class="dialog__footer"><button class="btn" type="button">Cancel</button><button class="btn btn--primary" type="button">Add person</button></div></div>', "Form dialog.")],
  sizes=[('<span class="tag">sm 24rem</span><span class="tag">md 32rem</span><span class="tag">lg 48rem</span>', "lg for Run research, Review finding and Import.")],
  states=(["Default", "Busy", "Failed"], [("Confirm", ['<button class="btn btn--primary" type="button">Run</button>', '<button class="btn btn--primary" type="button" aria-busy="true">Run</button>', '<span class="inline-status inline-status--danger">Couldn\'t start · input kept</span>'])]),
  sample='<div class="dialog__panel" style="position:relative;animation:none;"><div class="dialog__body">Dialog surface</div></div>',
  responsive=["< 640px: full-width bottom sheet with 28px top radius, slides up.", "≥ 640px: centred, scales in.", "Footer stays sticky while the body scrolls."], tokens=[("Surface", "--color-bg-surface-raised"), ("Backdrop", "--color-bg-backdrop"), ("Shadow", "--shadow-4"), ("Radius", "--radius-lg"), ("Enter", "--duration-slow")],
  a11y=dict(pattern="APG Dialog (Modal): <code>role=\"dialog\" aria-modal=\"true\" aria-labelledby aria-describedby</code>; page behind <code>inert</code>.", keys=[("Esc", "Close"), ("Tab", "Cycle inside"), ("Enter", "Submit form")], focus="Starts on the first field or the safe button; returns to the trigger.", label="Title labels the dialog.", pairs=[("Text on raised", "--color-fg-default", "--color-bg-surface-raised"), ("Muted on raised", "--color-fg-muted", "--color-bg-surface-raised")], motion="Scale-in (desktop) or slide-up (sheet) over --duration-slow.", touch="Sheet reachable by thumb."),
  content=["Title is a question for confirmations: <i>Delete FaithTech?</i>", "Description says what is lost."],
  dos=[('<button class="btn" type="button" autofocus>Cancel</button><button class="btn btn--danger" type="button">Delete</button>', "Safe button focused.", '<button class="btn btn--danger" type="button" autofocus>Delete</button>', "Focus on destruction.")],
  code=('<div class="backdrop"></div><div class="dialog" role="dialog" aria-modal="true" aria-labelledby="t"><div class="dialog__panel">…</div></div>', [("dialog", "Positioning"), ("dialog__panel(--lg/--sm)", "Surface"), ("dialog__header/__body/__footer", "Parts"), ("backdrop", "Scrim")]),
  sources=["dialogs/delete-organization/default", "dialogs/run-research/default", "dialogs/review-finding/scroll"], drift="None.")

C(id="drawer", name="Drawer", group="Containers", lead="Panel that slides from an edge. Harvest Map uses the left drawer for phone navigation.",
  overview="<p>Same contract as a dialog. Full width on phones.</p>",
  anatomy=(f'<div class="drawer" style="position:relative;height:12rem;animation:none;"><div class="drawer__header"><h3 class="drawer__title">Harvest Map</h3><button class="btn btn--ghost btn--icon" type="button" aria-label="Close">{icon("close")}</button></div><div class="drawer__body">Links</div></div>', [("Header", "Title + close"), ("Body", "Scrolls"), ("Footer", "Account")]),
  variants=[('<span class="tag">Left (navigation)</span><span class="tag">Right (details)</span>', "Two edges.")], sizes="28rem max; 100% on phones.",
  states=(["Open"], [("Drawer", ['<span class="tag">Slides in over --duration-slow</span>'])]),
  sample='<div class="drawer" style="position:relative;height:6rem;animation:none;"><div class="drawer__body">Drawer</div></div>',
  responsive=["Full width under 640px."], tokens=[("Surface", "--color-bg-surface-raised"), ("Shadow", "--shadow-4")],
  a11y=dict(pattern="APG Dialog.", keys=[("Esc", "Close")], focus="Trapped; returns to the menu button.", label="aria-labelledby the title.", pairs=[("Text", "--color-fg-default", "--color-bg-surface-raised")], motion="Slide over --duration-slow.", touch="44px links."),
  content=["Title is the product name for navigation."],
  dos=[('<span class="tag">Navigation only</span>', "One job.", '<span class="tag">Navigation + filters + settings</span>', "A junk drawer.")],
  code=('<div class="drawer drawer--left" role="dialog" aria-modal="true">…</div>', [("drawer / drawer--left", "Panel"), ("drawer__header/__body/__footer", "Parts")]), sources=["dialogs/nav-sheet/default"], drift="None.")

C(id="popover", name="Popover", group="Containers", lead="Small anchored surface: the map pin card, positioned with CSS anchor positioning.",
  overview="<p>Uses <code>position-anchor</code>, <code>position-area: top center</code> and flip fallbacks. Docks under the map on phones.</p>",
  anatomy=('<div class="popover" style="position:relative;"><strong>FaithTech</strong><div class="text-muted">Waterloo · 50+ cities</div></div>', [("Surface", "--shadow-3, --radius-md"), ("Content", "Name, place, tags")]),
  variants=[('<div class="map__pop" style="position:relative;position-anchor:none;"><span class="org-card__name">Gloo</span><div class="org-card__meta">Boulder · 140,000 leaders</div></div>', "Map pin popover.")], sizes="Max 18rem.",
  states=(["Closed", "Open"], [("Pin", ['<span class="tag">aria-expanded=false</span>', '<span class="tag">aria-expanded=true</span>'])]),
  sample='<div class="popover" style="position:relative;">Popover</div>',
  responsive=["< 640px: docks below the map full-width; the map adds bottom margin via :has()."], tokens=[("Surface", "--color-bg-surface-raised"), ("Shadow", "--shadow-3"), ("Z", "--z-popover")],
  a11y=dict(pattern="Disclosure: pin button <code>aria-expanded</code>; popover <code>role=\"dialog\"</code> with a label.", keys=[("Enter", "Open"), ("Esc", "Close")], focus="Stays on the pin unless the popover has links.", label="Pin aria-label “Name, city”.", pairs=[("Text", "--color-fg-default", "--color-bg-surface-raised")], motion="Scale-in over --duration-fast.", touch="24px pin target."),
  content=["Name, place, reach; no paragraphs."],
  dos=[('<span class="tag">Anchored with CSS</span>', "No JS measuring.", '<span class="tag">Absolute pixels from JS</span>', "Breaks on resize.")],
  code=('<div class="map__pop" style="--pin-anchor:--pin-id">…</div>', [("popover", "Generic"), ("map__pop", "Anchored map variant")]), sources=["pages/map/default"], drift="None.")

C(id="tooltip", name="Tooltip", group="Containers", lead="Short label for icon-only controls. Shown on hover and focus; never interactive.",
  overview="<p>Removed from layout while hidden (<code>visibility</code>) so it never widens the page.</p>",
  anatomy=('<span class="tooltip" role="tooltip" style="position:relative;">3 unread</span>', [("Bubble", "Inverse surface, caption text"), ("Arrow", "5px")]),
  variants=[('<span class="tooltip" role="tooltip" style="position:relative;">Search <kbd>⌘K</kbd></span>', "With shortcut.")], sizes="One size.",
  states=(["Hidden", "Visible"], [("Tooltip", [f'<span class="has-tooltip"><button class="btn btn--icon" type="button" aria-label="Notifications">{icon("bell")}</button><span class="tooltip" role="tooltip">2 unread</span></span>', f'<span class="has-tooltip" data-state="hover"><button class="btn btn--icon" type="button" aria-label="Notifications">{icon("bell")}</button><span class="tooltip" role="tooltip">2 unread</span></span>'])]),
  sample='<span class="tooltip" role="tooltip" style="position:relative;">Tooltip</span>',
  responsive=["In the top bar it anchors right and opens downward."], tokens=[("Surface", "--color-bg-inverse"), ("Text", "--color-fg-inverse"), ("Z", "--z-tooltip")],
  a11y=dict(pattern="<code>role=\"tooltip\"</code>; the control still has its own aria-label.", keys=[("Tab", "Show on focus"), ("Esc", "Hide")], focus="Shows with focus.", label="Never the only label.", pairs=[("Text", "--color-fg-inverse", "--color-bg-inverse")], motion="Opacity over --duration-fast.", touch="Not relied on; labels are visible elsewhere."),
  content=["Two to four words."],
  dos=[('<span class="tooltip" role="tooltip" style="position:relative;">2 unread</span>', "Short.", '<span class="tooltip" role="tooltip" style="position:relative;">You have two unread notifications from research</span>', "A sentence.")],
  code=('<span class="has-tooltip">…<span class="tooltip" role="tooltip">…</span></span>', [("has-tooltip", "Anchor"), ("tooltip", "Bubble")]), sources=["pages/field/default"], drift="Tooltips overflowed at 360px in the first sweep; fixed.")

C(id="divider", name="Divider", group="Containers", lead="Hairline between related rows. Decorative; exempt from contrast.",
  overview="<p>Most separation in Harvest Map is whitespace. Dividers appear only inside lists, sources and timelines.</p>",
  anatomy=('<div style="width:16rem;"><p>Above</p><hr class="divider"><p>Below</p></div>', [("Line", "1px --color-border-default")]),
  variants=[('<hr class="divider" style="width:12rem;"><span class="menu__divider" role="separator" style="display:block;width:12rem;"></span>', "Horizontal; menu separator.")], sizes="1px.",
  states=(["Default"], [("Divider", ['<hr class="divider" style="width:8rem;">'])]),
  sample='<hr class="divider" style="width:8rem;">',
  responsive=["Full width of its container."], tokens=[("Line", "--color-border-default")],
  a11y=dict(pattern="<code>&lt;hr&gt;</code> or <code>role=\"separator\"</code>.", keys=[], focus="Not focusable.", label="—", pairs=[], motion="None.", touch="—"),
  content=["Prefer space over lines."],
  dos=[('<div class="stack"><span>One</span><span>Two</span></div>', "Space separates.", '<div><span>One</span><hr class="divider"><span>Two</span><hr class="divider"></div>', "Lines between everything.")],
  code=('<hr class="divider">', [("divider", "Hairline")]), sources=["pages/organization/default"], drift="Mocks drew separators with borders on rows; formalised as .divider for standalone use.")

C(id="layout", name="Layout primitives", group="Containers", lead="Container, stack, cluster, grid. Generous whitespace is the brand.",
  overview="<p>Container max 76rem; margins 20/40/64px; sections 64px apart; page padding 64/96px.</p>",
  anatomy=('<div class="stack" style="width:100%;"><div class="cluster"><span class="tag">cluster</span><span class="tag">wraps</span></div><div class="grid" style="--layout-columns:3;"><span class="tag">grid</span><span class="tag">grid</span><span class="tag">grid</span></div></div>', [("container", "Centred, max width, side margins"), ("stack", "Vertical gap --space-4"), ("cluster", "Wrapping row"), ("grid", "Token columns + gutter")]),
  variants=[('<div class="ds-grid-demo" style="width:100%;">' + "".join(f"<span>{i}</span>" for i in range(1, 13)) + "</div>", "Live grid: 4 / 8 / 12 columns.")], sizes="See layout foundation.",
  states=(["Default"], [("Stack", ['<div class="stack stack--sm"><span class="tag">a</span><span class="tag">b</span></div>'])]),
  sample='<div class="cluster"><span class="tag">a</span><span class="tag">b</span></div>',
  responsive=["Columns 4/8/12, gutter 16/24/32, margin 20/40/64 at 0/768/1024."], tokens=[("Gutter", "--layout-gutter"), ("Margin", "--layout-margin"), ("Container", "--layout-container-max"), ("Columns", "--layout-columns")],
  a11y=dict(pattern="Presentational.", keys=[], focus="—", label="—", pairs=[], motion="—", touch="Reflows to 320px."),
  content=["—"],
  dos=[('<div class="stack"><span class="tag">a</span><span class="tag">b</span></div>', "Gap from tokens.", '<div><span class="tag" style="margin:13px;">a</span></div>', "Ad-hoc margins.")],
  code=('<main class="container app-main">…</main>', [("container / app-main", "Page"), ("stack (--sm/--lg)", "Vertical"), ("cluster (--between/--end)", "Row"), ("grid / grid--auto", "Grid")]), sources=["pages/field/default"], drift="Several mocks use inline style gaps; all map to space tokens.")

# ============================================================================ Data display
C(id="table", name="Table", group="Data display", lead="Tabular data with a sunken sticky header. Harvest Map prefers entity cards; tables are for imports and mappings.",
  overview="<p>Use for comparing columns (CSV mapping, exports). Lists of records use <a href=\"entity-card.html\">entity cards</a>.</p>",
  anatomy=('<div class="table-wrap" style="width:100%;"><table class="table"><caption class="visually-hidden">Mapping</caption><thead><tr><th scope="col">CSV column</th><th scope="col">Field</th></tr></thead><tbody><tr><td>org</td><td>Name</td></tr><tr><td>url</td><td>Website</td></tr></tbody></table></div>', [("Wrapper", "Scrolls horizontally"), ("Header", "Sunken, sticky"), ("Row", "Hover subtle")]),
  variants=[('<div class="table-wrap"><table class="table"><caption class="visually-hidden">Sorted</caption><thead><tr><th scope="col" aria-sort="ascending"><button type="button">Score</button></th><th scope="col" class="num">Orgs</th></tr></thead><tbody><tr><td>94</td><td class="num">1</td></tr></tbody></table></div>', "Sortable with numeric column.")],
  sizes="One density.",
  states=(["Default", "Hover", "Selected"], [("Row", ['<table class="table"><tbody><tr><td>org</td></tr></tbody></table>', '<table class="table"><tbody><tr data-state="hover"><td>org</td></tr></tbody></table>', '<table class="table"><tbody><tr aria-selected="true"><td>org</td></tr></tbody></table>'])]),
  sample='<table class="table"><thead><tr><th scope="col">A</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>',
  responsive=["Scrolls inside .table-wrap; page never scrolls sideways."], tokens=[("Header", "--color-bg-surface-sunken"), ("Row hover", "--color-bg-subtle"), ("Selected", "--color-accent-subtle")],
  a11y=dict(pattern="Native table with caption and scope.", keys=[("Tab", "Into sort buttons")], focus="Shared ring.", label="Caption, visually hidden if obvious.", pairs=[("Header text", "--color-fg-muted", "--color-bg-surface-sunken")], motion="None.", touch="Scrolls."),
  content=["Headers are nouns; numbers right-aligned, tabular."],
  dos=[('<td class="num">1,284</td>', "Right-aligned tabular numbers.", '<td>1284</td>', "Left-aligned without separators.")],
  code=('<div class="table-wrap"><table class="table">…</table></div>', [("table-wrap", "Scroll + border"), ("table", "Base"), ("num", "Numeric cell")]), sources=["dialogs/import-csv/default"], drift="None.")

C(id="list", name="List", group="Data display", lead="Rows with dividers: notifications, run logs, sources, recent searches.",
  overview="<p>Interactive items are links. Unread rows carry an accent dot and full-strength text.</p>",
  anatomy=(f'<div class="card card--flush" style="width:100%;max-width:30rem;"><div class="list"><a class="list__item list__item--interactive" href="#overview"><span class="dot" style="color:var(--color-accent);" aria-label="Unread"></span>{icon("flask")}<div class="list__body"><div class="list__title">Run #47 finished</div><div class="list__meta">12 findings to review</div></div><span class="text-caption">Yesterday</span></a></div></div>', [("Dot", "Unread"), ("Icon", "Type"), ("Body", "Title + meta"), ("Time", "Caption, right")]),
  variants=[('<ul class="list" style="width:20rem;"><li class="list__item">Queued 8 people</li><li class="list__item">2 sources found</li></ul>', "Simple log.")], sizes="One size.",
  states=(["Default", "Hover", "Read"], [("Item", ['<a class="list__item list__item--interactive" href="#overview">Run #47 finished</a>', '<a class="list__item list__item--interactive" href="#overview" style="background:var(--color-bg-subtle);">Run #47 finished</a>', '<a class="list__item list__item--interactive" href="#overview" style="color:var(--color-fg-muted);">Run #47 finished</a>'])]),
  sample='<ul class="list"><li class="list__item">Item</li></ul>',
  responsive=["Time wraps under the body under 360px."], tokens=[("Divider", "--color-border-default"), ("Meta", "--color-fg-muted")],
  a11y=dict(pattern="<code>&lt;ul&gt;</code>; live logs use <code>aria-live=\"polite\"</code>.", keys=[("Tab", "Through links")], focus="Shared ring.", label="Unread dot has aria-label.", pairs=[("Meta", "--color-fg-muted", "--color-bg-surface")], motion="Rise on entry.", touch="Rows ≥ 44px."),
  content=["Title says what happened; meta says what next."],
  dos=[('<span class="list__title">Run #47 finished</span>', "Past tense event.", '<span class="list__title">Notification</span>', "Generic title.")],
  code=('<ul class="list"><li class="list__item">…</li></ul>', [("list / list__item(--interactive)", "List"), ("list__body/__title/__meta", "Parts")]), sources=["pages/notifications/default", "pages/research/running"], drift="Read rows used an inline muted colour; documented as the read state.")

C(id="description-list", name="Facts list", group="Data display", lead="Key facts beside a record: overline key, body value.",
  overview="<p>The detail-page aside. Keys are short uppercase captions.</p>",
  anatomy=('<dl class="facts"><div class="fact"><dt>Founded</dt><dd>2016</dd></div><div class="fact"><dt>Base</dt><dd>Waterloo, Canada</dd></div></dl>', [("Key", "Caption, uppercase, subtle"), ("Value", "Body")]),
  variants=[('<dl class="dl"><dt>⌘ K</dt><dd>Search</dd><dt>R</dt><dd>Run research</dd></dl>', "Horizontal (.dl).")], sizes="One size.",
  states=(["Default"], [("Fact", ['<dl class="facts"><div class="fact"><dt>Reach</dt><dd>50+ cities</dd></div></dl>'])]),
  sample='<dl class="facts"><div class="fact"><dt>Type</dt><dd>Community</dd></div></dl>',
  responsive=["Aside moves below main content under 1024px."], tokens=[("Key", "--color-fg-subtle"), ("Gap", "--space-4")],
  a11y=dict(pattern="<code>&lt;dl&gt;</code>.", keys=[], focus="—", label="—", pairs=[("Key", "--color-fg-subtle", "--color-bg-canvas")], motion="None.", touch="—"),
  content=["Keys one word."],
  dos=[('<dl class="facts"><div class="fact"><dt>Founded</dt><dd>2016</dd></div></dl>', "One fact per pair.", '<p>Founded: 2016, Base: Waterloo</p>', "Facts as prose.")],
  code=('<dl class="facts"><div class="fact"><dt>…</dt><dd>…</dd></div></dl>', [("facts / fact", "Vertical"), ("dl", "Horizontal")]), sources=["pages/organization/default", "pages/person/default"], drift="None.")

C(id="avatar", name="Avatar", group="Data display", lead="Initials on accent-subtle. No photos are stored.",
  overview="<p>People and the signed-in account. Decorative next to a name.</p>",
  anatomy=('<span class="avatar" aria-hidden="true">PG</span>', [("Circle", "--radius-full"), ("Initials", "Two letters")]),
  variants=[('<span class="avatar-group" aria-label="FaithTech, Gloo"><span class="avatar avatar--sm" aria-hidden="true">FT</span><span class="avatar avatar--sm" aria-hidden="true">GL</span></span>', "Group.")],
  sizes=[('<span class="avatar avatar--sm" aria-hidden="true">NA</span><span class="avatar" aria-hidden="true">NA</span><span class="avatar avatar--lg" aria-hidden="true">NA</span>', "32 / 40 / 56px.")],
  states=(["Default"], [("Avatar", ['<span class="avatar" aria-hidden="true">JK</span>'])]),
  sample='<span class="avatar" aria-hidden="true">NA</span>',
  responsive=["Fixed size."], tokens=[("Background", "--color-accent-subtle"), ("Text", "--color-fg-accent")],
  a11y=dict(pattern="Decorative (aria-hidden) beside the name; labelled when it is the account link.", keys=[], focus="When a link, shared ring.", label="“Account settings for Naomi Achterberg”.", pairs=[("Initials", "--color-fg-accent", "--color-accent-subtle")], motion="None.", touch="32px as a link."),
  content=["First + last initial."],
  dos=[('<a class="avatar avatar--sm" href="#overview" aria-label="Account settings">NA</a>', "Labelled link.", '<a class="avatar avatar--sm" href="#overview">NA</a>', "Initials as the only name.")],
  code=('<span class="avatar" aria-hidden="true">PG</span>', [("avatar(--sm/--lg)", "Size"), ("avatar-group", "Overlap")]), sources=["pages/people/default"], drift="None.")

C(id="badge", name="Badge", group="Data display", lead="Dot + uppercase word for status; red counts on the bell.",
  overview="<p>Badges label state. For categories use <a href=\"tag.html\">tags</a>.</p>",
  anatomy=('<span class="badge badge--success">81% match</span>', [("Dot", "--size-dot"), ("Text", "Overline")]),
  variants=[('<span class="badge">Neutral</span><span class="badge badge--info">Info</span><span class="badge badge--success">Success</span><span class="badge badge--warning">Warning</span><span class="badge badge--danger">Danger</span><span class="badge badge--count" aria-label="2 unread">2</span>', "Tones and count.")],
  sizes="One size (--size-badge).",
  states=(["Default"], [("Badge", ['<span class="badge badge--warning">Due</span>'])]),
  sample='<span class="badge badge--success">Ok</span><span class="badge badge--danger">Failed</span>',
  responsive=["Never wraps."], tokens=[("Success", "--color-success-bg"), ("Count", "--color-danger-solid"), ("Height", "--size-badge")],
  a11y=dict(pattern="Text; counts carry aria-label.", keys=[], focus="—", label="Count meaning in aria-label.", pairs=[("Success", "--color-success-fg", "--color-success-bg"), ("Danger", "--color-danger-fg", "--color-danger-bg"), ("Count", "--color-fg-on-danger", "--color-danger-solid")], motion="None.", touch="—"),
  content=["One or two words."],
  dos=[('<span class="badge badge--danger">Failed</span>', "Dot + word.", '<span class="dot" style="color:var(--color-danger-icon);"></span>', "Colour alone.")],
  code=('<span class="badge badge--success">…</span>', [("badge--info/success/warning/danger/solid/count", "Tone")]), sources=["pages/people/default", "pages/field/default"], drift="Badge height 22px snapped to 24px (--size-badge).")

C(id="chip", name="Chip", group="Data display", lead="Pill toggles that filter a list: AI, Youth, Moonshot, Verified.",
  overview="<p>Filter chips use <code>aria-pressed</code>. They press with a spring scale.</p>",
  anatomy=('<button class="chip" type="button" aria-pressed="true">AI</button>', [("Pill", "32px, 1px border"), ("Label", "Label text")]),
  variants=[('<button class="chip" type="button" aria-pressed="false">Youth</button><button class="chip" type="button" aria-pressed="true">Moonshot</button><span class="chip">Tag <button class="remove" type="button" aria-label="Remove tag">×</button></span>', "Filter off/on; removable.")],
  sizes="One size (32px).",
  states=(["Default", "Hover", "Focus", "Pressed", "Disabled"], [("Chip", [f'<button class="chip" type="button" {a}>AI</button>' for a in ['aria-pressed="false"', 'aria-pressed="false" data-state="hover"', 'aria-pressed="false" data-state="focus"', 'aria-pressed="true"', 'aria-pressed="false" disabled']])]),
  sample='<button class="chip" type="button" aria-pressed="true">On</button><button class="chip" type="button" aria-pressed="false">Off</button>',
  responsive=["Chip rows wrap via .cluster."], tokens=[("Pressed bg", "--color-accent-subtle"), ("Pressed text", "--color-fg-accent"), ("Border", "--color-border-strong")],
  a11y=dict(pattern="Toggle button (<code>aria-pressed</code>).", keys=[("Space / Enter", "Toggle")], focus="Shared ring.", label="Visible label.", pairs=[("Pressed", "--color-fg-accent", "--color-accent-subtle"), ("Border", "--color-border-strong", "--color-bg-canvas", 3)], motion="Scale 0.96 on press, spring.", touch="32px + 12px gap."),
  content=["Single nouns."],
  dos=[('<button class="chip" type="button" aria-pressed="true">AI</button>', "aria-pressed.", '<span class="chip" style="cursor:pointer;">AI</span>', "Span as a button.")],
  code=('<button class="chip" type="button" aria-pressed="false">AI</button>', [("chip", "Pill"), ("remove", "Remove button")]), sources=["pages/organizations/default", "pages/organizations/no-results"], drift="None.")

C(id="tag", name="Tag", group="Data display", lead="Static category labels on records. AI and Moonshot are highlighted.",
  overview="<p>Not interactive. Up to nine wrap on one card (see the edge mock).</p>",
  anatomy=('<div class="tags"><span class="tag tag--ai">AI</span><span class="tag tag--moonshot">Moonshot</span><span class="tag">Youth</span></div>', [("Tag", "24px, --radius-sm, caption medium")]),
  variants=[('<span class="tag">Default</span><span class="tag tag--ai">AI</span><span class="tag tag--moonshot">Moonshot</span>', "Three tones.")], sizes="One size.",
  states=(["Default"], [("Tag", ['<span class="tag tag--ai">AI</span>'])]),
  sample='<span class="tag tag--ai">AI</span><span class="tag tag--moonshot">Moonshot</span><span class="tag">Youth</span>',
  responsive=["Wrap with 4px gaps."], tokens=[("Default bg", "--color-bg-subtle"), ("AI bg", "--color-accent-subtle"), ("Moonshot bg", "--color-warning-bg")],
  a11y=dict(pattern="Text.", keys=[], focus="—", label="—", pairs=[("Default", "--color-fg-muted", "--color-bg-subtle"), ("AI", "--color-fg-accent", "--color-accent-subtle"), ("Moonshot", "--color-warning-fg", "--color-warning-bg")], motion="None.", touch="—"),
  content=["Title case for the fixed set: AI, Youth, Moonshot, Scripture, Research, Community, Digital."],
  dos=[('<span class="tag tag--ai">AI</span>', "From the fixed set.", '<span class="tag">ai-stuff</span>', "Ad-hoc tags.")],
  code=('<div class="tags"><span class="tag tag--ai">AI</span></div>', [("tags", "Wrapper"), ("tag(--ai/--moonshot)", "Tag")]), sources=["pages/organizations/default", "pages/organizations/edge"], drift="Moonshot background used color-mix(); replaced with --color-warning-bg so contrast can be checked.")

C(id="status", name="Status indicator", group="Data display", lead="Verification (Verified, Unverified, Conflict, Not found) and run status (Running, Done, Failed, Queued).",
  overview="<p>Most facts come from research, so every record and link carries its verification. Pending states pulse.</p>",
  anatomy=('<span class="verify verify--verified">Verified</span>', [("Dot", "8px"), ("Word", "Caption")]),
  variants=[('<span class="verify verify--verified">Verified</span><span class="verify verify--pending">Unverified</span><span class="verify verify--conflict">Conflict</span><span class="verify">Not found</span>', "Verification."),
            ('<span class="run-status run-status--running"><span class="dot dot--pulse"></span>Running</span><span class="run-status run-status--done"><span class="dot"></span>Done</span><span class="run-status run-status--failed"><span class="dot"></span>Failed</span><span class="run-status run-status--queued"><span class="dot"></span>Queued</span>', "Run status.")],
  sizes="Caption (verify) and label (run).",
  states=(["Verified", "Pending", "Conflict", "None"], [("Verify", ['<span class="verify verify--verified">Verified</span>', '<span class="verify verify--pending">Unverified</span>', '<span class="verify verify--conflict">Conflict</span>', '<span class="verify">Not found</span>'])]),
  sample='<span class="verify verify--verified">Verified</span><span class="verify verify--pending">Unverified</span>',
  responsive=["Never wraps."], tokens=[("Verified", "--color-success-fg"), ("Pending", "--color-warning-fg"), ("Conflict", "--color-danger-fg")],
  a11y=dict(pattern="Text; never colour alone.", keys=[], focus="—", label="The word is the status.", pairs=[("Verified", "--color-success-fg", "--color-bg-surface"), ("Pending", "--color-warning-fg", "--color-bg-surface"), ("Conflict", "--color-danger-fg", "--color-bg-surface")], motion="Pending dot pulses over --duration-loop.", touch="—"),
  content=["Verified means two sources or one trusted source."],
  dos=[('<span class="verify verify--pending">Unverified</span>', "Honest status.", '<span class="verify verify--verified">Verified</span><span class="text-caption">(company claim)</span>', "Verified on a single company claim.")],
  code=('<span class="verify verify--verified">Verified</span>', [("verify--verified/--pending/--conflict", "Verification"), ("run-status--running/--done/--failed/--queued", "Run")]), sources=["pages/organizations/default", "pages/research/default"], drift="None.")

C(id="score-ring", name="Score ring", group="Data display", lead="Impact score 0–100 drawn with an animated conic-gradient (@property --score). Rank 1 is gold.",
  overview="<p>Impact = reach × severity × tractability. Fills from 0 on entry.</p>",
  anatomy=('<span class="score score--lg" style="--score:94" role="img" aria-label="Impact score 94 of 100" data-rank="1"><span>94</span></span>', [("Track", "--color-bg-subtle-hover"), ("Fill", "Accent, gold for rank 1"), ("Number", "Tabular")]),
  variants=[('<span class="score" style="--score:94" data-rank="1" role="img" aria-label="94"><span>94</span></span><span class="score" style="--score:79" role="img" aria-label="79"><span>79</span></span><span class="score" style="--score:0" role="img" aria-label="No score"><span>—</span></span>', "Rank 1, normal, unscored.")],
  sizes=[('<span class="score score--sm" style="--score:58" role="img" aria-label="58"><span>58</span></span><span class="score" style="--score:58" role="img" aria-label="58"><span>58</span></span><span class="score score--lg" style="--score:58" role="img" aria-label="58"><span>58</span></span>', "36 / 52 / 88px.")],
  states=(["Default", "Unscored"], [("Score", ['<span class="score" style="--score:83" role="img" aria-label="83"><span>83</span></span>', '<span class="score" style="--score:0" role="img" aria-label="No score"><span>—</span></span>'])]),
  sample='<span class="score" style="--score:83" role="img" aria-label="83"><span>83</span></span>',
  responsive=["Fixed size."], tokens=[("Fill", "--color-accent"), ("Gold", "--color-warning-icon"), ("Track", "--color-bg-subtle-hover")],
  a11y=dict(pattern="<code>role=\"img\"</code> with aria-label “Impact score 94 of 100”.", keys=[], focus="—", label="Required.", pairs=[("Fill vs track", "--color-accent", "--color-bg-surface", 3)], motion="--score transitions over --duration-deliberate; instant with reduced motion.", touch="—"),
  content=["Never show decimals."],
  dos=[('<span class="score" style="--score:94" role="img" aria-label="Impact score 94 of 100"><span>94</span></span>', "Labelled.", '<span class="score" style="--score:94"><span>94</span></span>', "Unlabelled graphic.")],
  code=('<span class="score" style="--score:94" role="img" aria-label="…"><span>94</span></span>', [("score(--sm/--lg)", "Size"), ('data-rank="1"', "Gold")]), sources=["pages/problems/default", "pages/problem/default"], drift="None.")

C(id="finding", name="Finding", group="Data display", lead="A claim from research with source, confidence and Accept / Edit / Reject.",
  overview="<p>Nothing from the web becomes a record until a person accepts it.</p>",
  anatomy=(f'<div class="card finding" style="max-width:32rem;"><p class="finding__claim">Pat Gelsinger became executive chair at Gloo in April 2025.</p><div class="finding__meta"><span>religionunplugged.com</span><span>·</span><span>Confidence 92%</span></div><div class="finding__actions"><button class="btn btn--sm btn--primary" type="button">{icon("check")}Accept</button><button class="btn btn--sm" type="button">Edit</button><button class="btn btn--sm btn--ghost" type="button">Reject</button></div></div>',
           [("Edge", "4px accent left border"), ("Claim", "Body large"), ("Meta", "Entity · source · confidence"), ("Actions", "Small buttons")]),
  variants=[('<div class="card finding finding--accepted" style="max-width:20rem;"><p class="finding__claim">Accepted</p></div><div class="card finding finding--rejected" style="max-width:20rem;"><p class="finding__claim">Rejected</p></div>', "Accepted (green edge, faded) and rejected (struck).")],
  sizes="One size.",
  states=(["New", "Accepted", "Rejected"], [("Finding", ['<div class="card finding"><p class="finding__claim">Claim</p></div>', '<div class="card finding finding--accepted"><p class="finding__claim">Claim</p></div>', '<div class="card finding finding--rejected"><p class="finding__claim">Claim</p></div>'])]),
  sample='<div class="card finding"><p class="finding__claim">Claim</p></div>',
  responsive=["Actions wrap."], tokens=[("Edge", "--color-accent"), ("Accepted edge", "--color-success-icon")],
  a11y=dict(pattern="Card with buttons; outcome announced by a toast.", keys=[("Tab", "Through actions")], focus="Shared ring.", label="Buttons are verbs.", pairs=[("Meta", "--color-fg-subtle", "--color-bg-surface")], motion="Optimistic fade; undo for 30s.", touch="32px buttons with gaps."),
  content=["Claim is one sentence of fact, with a date."],
  dos=[('<span class="verify verify--pending">Company claim; no independent source.</span>', "Reason for low confidence inline.", '<span class="text-caption">Confidence 41%</span>', "Number without reason.")],
  code=('<div class="card finding">…</div>', [("finding(--accepted/--rejected)", "State"), ("finding__claim/__meta/__actions", "Parts")]), sources=["pages/research/review", "dialogs/review-finding/default"], drift="Rejected style struck through the whole card; scoped to the claim.")

C(id="timeline", name="Timeline", group="Data display", lead="Activity and milestones: time column, event column.",
  overview="<p>Relative times in lists, absolute on milestones.</p>",
  anatomy=('<ul class="timeline" style="width:20rem;"><li><time>Today 12:04</time><span>Run #48 started</span></li><li><time>Mon 13 Oct</time><span>Created by Naomi</span></li></ul>', [("Time", "6rem, tabular, subtle"), ("Event", "Body small")]),
  variants=[('<ul class="timeline" style="width:20rem;"><li><time>2033</time><span>All Access Goals deadline</span></li></ul>', "Milestones.")], sizes="One size.",
  states=(["Default"], [("Timeline", ['<ul class="timeline"><li><time>Today</time><span>Event</span></li></ul>'])]),
  sample='<ul class="timeline"><li><time>Today</time><span>Event</span></li></ul>',
  responsive=["Same at all widths."], tokens=[("Time", "--color-fg-subtle")],
  a11y=dict(pattern="<code>&lt;ul&gt;</code> with <code>&lt;time&gt;</code>.", keys=[], focus="—", label="—", pairs=[("Time", "--color-fg-subtle", "--color-bg-canvas")], motion="None.", touch="—"),
  content=["Actor + verb + object."],
  dos=[('<ul class="timeline"><li><time>Tue 14 Oct</time><span>Priya verified 2 sources</span></li></ul>', "Who did what.", '<ul class="timeline"><li><time>1760400000</time><span>update</span></li></ul>', "Raw timestamps.")],
  code=('<ul class="timeline"><li><time>…</time><span>…</span></li></ul>', [("timeline", "List")]), sources=["pages/organization/default", "pages/problem/default"], drift="None.")

C(id="map", name="Map", group="Data display", lead="Dot-matrix world (SVG mask, theme-coloured) with pulsing pins and anchored popovers.",
  overview="<p>Equirectangular 2.4° dot grid. Organisations without a single home are listed below instead of pinned.</p>",
  anatomy=('<div class="map" style="max-width:24rem;"><div class="map__land"></div><button class="map__pin" type="button" style="left:27.6%;top:25.8%;" aria-label="FaithTech, Waterloo" aria-expanded="false"></button></div>', [("Land", "Dot mask, --color-fg-subtle at 35%"), ("Pin", "12px core + ripple"), ("Popover", "Anchored")]),
  variants=[('<div class="map__legend" style="margin:0;"><span><i></i>Verified</span><span><i class="unverified"></i>Unverified</span></div>', "Legend: verified filled, unverified ring.")],
  sizes="2:1, full width.",
  states=(["Pin", "Unverified", "Selected"], [("Pin", ['<span style="position:relative;display:inline-block;width:2rem;height:2rem;"><button class="map__pin" type="button" style="left:50%;top:50%;" aria-label="Pin"></button></span>', '<span style="position:relative;display:inline-block;width:2rem;height:2rem;"><button class="map__pin map__pin--unverified" type="button" style="left:50%;top:50%;" aria-label="Pin"></button></span>', '<span style="position:relative;display:inline-block;width:2rem;height:2rem;"><button class="map__pin map__pin--selected" type="button" style="left:50%;top:50%;" aria-label="Pin" aria-expanded="true"></button></span>'])]),
  sample='<div class="map" style="max-width:12rem;"><div class="map__land"></div></div>',
  responsive=["Popover docks under the map under 640px."], tokens=[("Pin", "--color-accent"), ("Unverified", "--color-warning-icon"), ("Land", "--color-fg-subtle"), ("Ripple", "--duration-loop-slow")],
  a11y=dict(pattern="Pins are buttons; a text list of placed and unplaced organisations sits beside the map.", keys=[("Tab", "Pin to pin"), ("Enter", "Open popover"), ("Esc", "Close")], focus="Pin scales 1.4 on focus.", label="“Name, city”.", pairs=[("Pin on surface", "--color-accent", "--color-bg-surface", 3)], motion="Pin ripple staggered; off with reduced motion.", touch="24px targets; dense clusters spread on zoom."),
  content=["Say where the gaps are in one sentence below the map."],
  dos=[('<p class="text-caption">Not on the map: illumiNations, Lausanne.</p>', "List what can't be placed.", '<p class="text-caption">—</p>', "Silently drop them.")],
  code=('<div class="map"><div class="map__land"></div><button class="map__pin" …></button></div>', [("map / map__land / map__pin(--unverified/--selected) / map__pop / map__legend", "Parts"), ("world-dots.css", "Land mask (data URI)")]), sources=["pages/map/default"], drift="External SVG mask blocked under file://; inlined as a data URI.",
  head='\n<link rel="stylesheet" href="../../mocks/assets/world-dots.css">')

# ============================================================================ Feedback
C(id="toast", name="Toast", group="Feedback", lead="Bottom-right on desktop, full-width bottom on phones. 8s with Undo; errors persist.",
  overview="<p>Confirms an action the person just took. Max three; oldest on top.</p>",
  anatomy=(f'<div class="toast toast--success" style="width:22rem;">{icon("success")}<div class="toast__body"><div class="toast__title">FaithTech saved</div><button class="toast__action" type="button">Undo</button></div><button class="close" type="button" aria-label="Dismiss">{icon("close", "icon icon--sm")}</button><span class="toast__progress" aria-hidden="true"></span></div>',
           [("Icon", "Tone"), ("Title", "What happened"), ("Action", "Undo / Retry"), ("Close", "Labelled"), ("Timer", "Thin bar")]),
  variants=[(f'<div class="toast toast--info" style="width:18rem;">{icon("info")}<div class="toast__body"><div class="toast__title">Run #48 started</div></div></div><div class="toast toast--warning" style="width:18rem;">{icon("warning")}<div class="toast__body"><div class="toast__title">Run #48 slowed</div></div></div><div class="toast toast--danger" style="width:18rem;">{icon("danger")}<div class="toast__body"><div class="toast__title">Couldn\'t save</div></div></div>', "Info, warning, danger.")],
  sizes="24rem wide on desktop.",
  states=(["Entering", "Leaving"], [("Toast", ['<div class="toast toast--info"><div class="toast__body">Rises</div></div>', '<div class="toast toast--info" data-state="leaving"><div class="toast__body">Fades</div></div>'])]),
  sample='<div class="toast toast--success"><div class="toast__body"><div class="toast__title">Saved</div></div></div>',
  responsive=["< 640px: spans the width with 16px margins."], tokens=[("Surface", "--color-bg-inverse"), ("Text", "--color-fg-inverse"), ("Z", "--z-toast")],
  a11y=dict(pattern="Region <code>role=\"status\" aria-live=\"polite\"</code>; errors in <code>role=\"alert\"</code>.", keys=[("Tab", "Reach action and close")], focus="Never steals focus.", label="Close has aria-label.", pairs=[("Text", "--color-fg-inverse", "--color-bg-inverse")], motion="Rises over --duration-base.", touch="24px close."),
  content=["Title: past tense, specific. <i>FaithTech saved</i>."],
  dos=[('<div class="toast toast--danger"><div class="toast__body"><div class="toast__title">Couldn\'t save FaithTech</div><button class="toast__action" type="button">Retry</button></div></div>', "Error persists with Retry.", '<div class="toast toast--danger"><div class="toast__body"><div class="toast__title">Error</div></div><span class="toast__progress" aria-hidden="true"></span></div>', "Auto-dismissing vague error.")],
  code=('<div class="toast-region" role="status" aria-live="polite">…</div>', [("toast-region", "Live region"), ("toast(--info/--success/--warning/--danger)", "Toast")]), sources=["notifications/toast/success", "notifications/toast/stacked"], drift="None.")

C(id="alert", name="Alert and banner", group="Feedback", lead="Inline alerts in content; full-width banners under the top bar for runs and connectivity.",
  overview="<p>Alerts explain a condition on this page; banners follow the person across pages.</p>",
  anatomy=(f'<div class="alert alert--warning" role="status" style="width:100%;">{icon("warning")}<div class="alert__body"><div class="alert__title">Sources disagree on the founding year</div><div>2010 vs 2013.</div><div class="alert__actions"><a href="#overview">Resolve</a></div></div></div>', [("Edge", "4px left"), ("Icon", "Tone"), ("Title / text / actions", "Body")]),
  variants=[(f'<div class="alert alert--info banner" role="status" style="width:100%;"><span class="dot dot--pulse" aria-hidden="true"></span><div class="alert__body"><span class="alert__title">Run #48 running · 62%</span><span class="alert__actions"><a href="#overview">View</a></span></div></div>', "Banner with live dot.")],
  sizes="Alert: content width. Banner: full width.",
  states=(["Info", "Success", "Warning", "Danger"], [("Alert", [f'<div class="alert alert--{t}" role="status">{icon(t)}<div class="alert__body"><div class="alert__title">{t.title()}</div></div></div>' for t in ["info", "success", "warning", "danger"]])]),
  sample=f'<div class="alert alert--info" role="status">{icon("info")}<div class="alert__body">Info</div></div>',
  responsive=["Banner content wraps; actions drop to a second line."], tokens=[("Info bg", "--color-info-bg"), ("Danger bg", "--color-danger-bg"), ("Edge", "--color-info-border")],
  a11y=dict(pattern="<code>role=\"status\"</code>; <code>role=\"alert\"</code> only for new failures.", keys=[("Tab", "Actions")], focus="Not moved.", label="Title + text.", pairs=[("Info", "--color-info-fg", "--color-info-bg"), ("Warning", "--color-warning-fg", "--color-warning-bg"), ("Danger", "--color-danger-fg", "--color-danger-bg")], motion="None.", touch="Actions are links."),
  content=["Title states the condition; action fixes it."],
  dos=[('<div class="alert alert--warning" role="status"><div class="alert__body"><div class="alert__title">You\'re offline</div><div>Edits queue.</div></div></div>', "Condition + consequence.", '<div class="alert alert--warning" role="status"><div class="alert__body">Warning!</div></div>', "Alarm without content.")],
  code=('<div class="alert alert--warning" role="status">…</div>', [("alert(--success/--warning/--danger)", "Tone"), ("banner", "Full-width")]), sources=["notifications/research-banner/info", "notifications/offline-banner/warning", "notifications/inline-alert/warning"], drift="None.")

C(id="inline-message", name="Inline message", group="Feedback", lead="Field help, field error, inline saved status.",
  overview="<p>Small text tied to a control or an action bar.</p>",
  anatomy=(f'<span class="inline-status inline-status--success">{icon("success", "icon icon--sm")} Saved · just now</span>', [("Icon or dot", "Tone"), ("Text", "Body small")]),
  variants=[('<span class="field__help">Like example.org</span><span class="field__error">Enter a name</span><span class="inline-status"><span class="spinner" aria-hidden="true"></span>Saving</span>', "Help, error, busy.")], sizes="Body small.",
  states=(["Help", "Error", "Saving", "Saved"], [("Message", ['<span class="field__help">Like example.org</span>', '<span class="field__error">Enter a name</span>', '<span class="inline-status"><span class="dot dot--pulse"></span>Saving</span>', '<span class="inline-status inline-status--success">Saved</span>'])]),
  sample='<span class="field__error">Enter a name</span>',
  responsive=["Wraps under the control."], tokens=[("Help", "--color-fg-muted"), ("Error", "--color-danger-fg"), ("Saved", "--color-success-fg")],
  a11y=dict(pattern="aria-describedby for field text; <code>role=\"status\"</code> for saved.", keys=[], focus="—", label="—", pairs=[("Error", "--color-danger-fg", "--color-bg-surface"), ("Saved", "--color-success-fg", "--color-bg-surface")], motion="Saving dot pulses.", touch="—"),
  content=["Saved + relative time."],
  dos=[('<span class="inline-status inline-status--success">Saved · just now</span>', "With time.", '<span class="inline-status inline-status--success">Success!</span>', "Exclamation, no time.")],
  code=('<span class="inline-status inline-status--success">…</span>', [("field__help / field__error", "Field text"), ("inline-status(--success/--danger)", "Status")]), sources=["pages/settings/success", "pages/organization-edit/invalid"], drift="None.")

C(id="progress", name="Progress", group="Feedback", lead="Determinate bar for runs and imports; thin bar inside run cards.",
  overview="<p>Use determinate whenever the queue length is known.</p>",
  anatomy=('<div class="progress" role="progressbar" aria-label="Run 48" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" style="width:20rem;"><div class="progress__bar" style="--value:62%"></div></div>', [("Track", "8px, --color-bg-subtle-hover"), ("Bar", "Accent")]),
  variants=[('<div class="progress progress--thin" role="progressbar" aria-label="Thin" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" style="width:12rem;"><div class="progress__bar" style="--value:62%"></div></div><div class="progress progress--indeterminate" role="progressbar" aria-label="Indeterminate" style="width:12rem;"><div class="progress__bar"></div></div><div class="progress progress--success" role="progressbar" aria-label="Done" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:12rem;"><div class="progress__bar" style="--value:100%"></div></div>', "Thin, indeterminate, success.")],
  sizes="8px default, 4px thin.",
  states=(["0%", "62%", "100%"], [("Bar", [f'<div class="progress" role="progressbar" aria-label="p" aria-valuenow="{v}" aria-valuemin="0" aria-valuemax="100" style="width:6rem;"><div class="progress__bar" style="--value:{v}%"></div></div>' for v in (0, 62, 100)])]),
  sample='<div class="progress" role="progressbar" aria-label="t" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:8rem;"><div class="progress__bar" style="--value:50%"></div></div>',
  responsive=["Full width of its card."], tokens=[("Bar", "--color-accent"), ("Track", "--color-bg-subtle-hover")],
  a11y=dict(pattern="<code>role=\"progressbar\"</code> with value attributes.", keys=[], focus="—", label="aria-label names the task.", pairs=[("Bar vs track", "--color-accent", "--color-bg-subtle-hover", 3)], motion="Width over --duration-slow.", touch="—"),
  content=["Pair with text: “3 of 8 people done · about 4 minutes left”."],
  dos=[('<span class="text-muted">3 of 8 · about 4 minutes left</span>', "Counts and time.", '<span class="text-muted">Please wait…</span>', "No information.")],
  code=('<div class="progress" role="progressbar" aria-valuenow="62" …><div class="progress__bar" style="--value:62%"></div></div>', [("progress(--thin/--indeterminate/--success)", "Variants")]), sources=["pages/research/running", "dialogs/import-csv/busy"], drift="None.")

C(id="spinner", name="Spinner", group="Feedback", lead="Only after 300ms, only for small in-place waits.",
  overview="<p>Buttons use their own busy state. Pages use skeletons.</p>",
  anatomy=('<span class="spinner" aria-hidden="true"></span>', [("Ring", "Border + accent top")]),
  variants=[('<span class="inline-status"><span class="spinner" aria-hidden="true"></span>Searching</span>', "With text.")],
  sizes=[('<span class="spinner" aria-hidden="true"></span><span class="spinner spinner--lg" aria-hidden="true"></span>', "20 / 40px.")],
  states=(["Spinning"], [("Spinner", ['<span class="spinner" aria-hidden="true"></span>'])]),
  sample='<span class="spinner" aria-hidden="true"></span>',
  responsive=["Fixed."], tokens=[("Arc", "--color-accent"), ("Track", "--color-border-default"), ("Speed", "--duration-loop-fast")],
  a11y=dict(pattern="Decorative; the text beside it is in a status region.", keys=[], focus="—", label="Visible text.", pairs=[("Arc", "--color-accent", "--color-bg-surface", 3)], motion="Stops under reduced motion (one turn).", touch="—"),
  content=["Gerund + object: <i>Searching organisations</i>."],
  dos=[('<span class="inline-status"><span class="spinner" aria-hidden="true"></span>Searching</span>', "With text.", '<span class="spinner spinner--lg" aria-hidden="true"></span>', "Alone on a blank page.")],
  code=('<span class="spinner" aria-hidden="true"></span>', [("spinner(--lg)", "Size")]), sources=["dialogs/command-palette/busy", "pages/sign-in/success"], drift="None.")

C(id="skeleton", name="Skeleton", group="Feedback", lead="Shimmering shapes that match the final layout. No layout shift on load.",
  overview="<p>Every list and detail page has a loading state built from the same cards with skeleton content.</p>",
  anatomy=('<div class="card" style="width:20rem;" aria-busy="true" aria-label="Loading"><span class="skeleton skeleton--title"></span><span class="skeleton skeleton--text"></span><span class="skeleton skeleton--text"></span></div>', [("Title", "1.5em"), ("Text", "0.9em lines; last 60%")]),
  variants=[('<span class="skeleton skeleton--circle" style="width:2.5rem;height:2.5rem;"></span><span class="skeleton skeleton--rect" style="width:3rem;height:3rem;"></span>', "Circle, rect.")], sizes="Sized by the content it replaces.",
  states=(["Loading"], [("Skeleton", ['<span class="skeleton skeleton--text" style="width:8rem;"></span>'])]),
  sample='<span class="skeleton skeleton--text" style="width:8rem;"></span>',
  responsive=["Use relative widths so skeletons never overflow 360px."], tokens=[("Base", "--color-bg-subtle"), ("Shine", "--color-bg-subtle-hover"), ("Cycle", "--duration-loop")],
  a11y=dict(pattern="Container <code>aria-busy=\"true\"</code> and a label; shapes hidden.", keys=[], focus="—", label="“Loading organisations”.", pairs=[], motion="Shimmer off under reduced motion.", touch="—"),
  content=["Page title stays real (known from the route)."],
  dos=[('<span class="skeleton skeleton--text" style="width:85%;"></span>', "Relative widths.", '<span class="skeleton skeleton--text" style="width:20rem;"></span>', "Fixed widths that overflow phones.")],
  code=('<div aria-busy="true" aria-label="Loading"><span class="skeleton skeleton--text"></span></div>', [("skeleton(--text/--title/--circle/--rect)", "Shape")]), sources=["pages/organizations/loading", "pages/field/loading"], drift="Fixed 12–20rem skeleton widths overflowed 360px; changed to percentages.")

C(id="empty-state", name="Empty state", group="Feedback", lead="Icon, title, one sentence, one action. First-run, filtered and error variants.",
  overview="<p>Replaces the list, never sits under an empty header.</p>",
  anatomy=(f'<div class="empty"><div class="empty__icon">{icon("building", "icon icon--lg")}</div><h3 class="empty__title">No organisations yet</h3><p class="empty__text">Add one or let research find them.</p><div class="empty__actions"><button class="btn btn--primary" type="button">Ask the web</button></div></div>', [("Icon", "64px circle"), ("Title", "h3"), ("Text", "≤ 36ch"), ("Actions", "One primary")]),
  variants=[(f'<div class="empty empty--compact">{icon("filter", "icon icon--lg")}<h3 class="empty__title">Nothing matches</h3><button class="btn" type="button">Clear filters</button></div><div class="empty empty--compact empty--error"><div class="empty__icon">{icon("danger", "icon icon--lg")}</div><h3 class="empty__title">Couldn\'t load</h3></div>', "No-results and error.")],
  sizes="Full (48px padding) and compact (32px).",
  states=(["First-run", "No results", "Error"], [("Empty", [f'<div class="empty empty--compact"><h3 class="empty__title">{t}</h3></div>' for t in ["No people yet", "Nothing matches", "Couldn't load"]])]),
  sample='<div class="empty empty--compact"><h3 class="empty__title">Empty</h3></div>',
  responsive=["Centred at every width."], tokens=[("Icon bg", "--color-accent-subtle"), ("Error icon bg", "--color-danger-bg")],
  a11y=dict(pattern="Heading + text + button.", keys=[], focus="—", label="—", pairs=[("Text", "--color-fg-muted", "--color-bg-canvas"), ("Icon", "--color-fg-accent", "--color-accent-subtle", 3)], motion="Rise on entry.", touch="—"),
  content=["What it is · why empty · what to do."],
  dos=[('<p class="empty__text">No organisation matches “youth hackathon”.</p>', "Echo the query.", '<p class="empty__text">No data.</p>', "Says nothing.")],
  code=('<div class="empty">…</div>', [("empty(--compact/--error)", "Variants")]), sources=["pages/organizations/empty", "pages/organizations/no-results", "pages/organizations/error"], drift="None.")

C(id="error-page", name="Error page", group="Feedback", lead="404, 403, 500, offline, unsupported browser. Big faint code, one recovery action.",
  overview="<p>Keeps the top bar when the session is valid. 500 shows a reference code.</p>",
  anatomy=(f'<div class="empty"><div class="empty__code" aria-hidden="true" style="font:var(--text-display);color:var(--color-border-default);">404</div><h3 class="empty__title">Nothing grows here</h3><div class="empty__actions"><button class="btn btn--primary" type="button">Back to the field</button></div></div>', [("Code", "Display, border colour"), ("Title", "h1 in product"), ("Action", "One primary")]),
  variants=[(f'<div class="empty empty--compact"><div class="empty__icon">{icon("chrome", "icon icon--lg")}</div><h3 class="empty__title">Harvest Map needs Chrome</h3></div>', "Unsupported browser.")], sizes="Full viewport.",
  states=(["404", "403", "500", "Offline"], [("Page", [f'<span class="tag">{t}</span>' for t in ["Nothing grows here", "Not your field", "Something went wrong · HM-9C21", "You're offline"]])]),
  sample='<div class="empty empty--compact"><h3 class="empty__title">Nothing grows here</h3></div>',
  responsive=["Centred."], tokens=[("Code", "--color-border-default")],
  a11y=dict(pattern="Page with one h1.", keys=[], focus="—", label="—", pairs=[("Title", "--color-fg-default", "--color-bg-canvas")], motion="None.", touch="—"),
  content=["Gentle, on-brand titles; plain instructions."],
  dos=[('<p class="empty__text">Share reference HM-9C21 with support.</p>', "Reference code.", '<p class="empty__text">Error 500</p>', "Code alone.")],
  code=('<div class="big-empty"><div class="empty">…</div></div>', [("big-empty", "Full-height centring")]), sources=["pages/not-found/default", "pages/server-error/default", "pages/unsupported-browser/default"], drift="None.")

C(id="selection-bar", name="Selection bar", group="Feedback", lead="Inverse bar that rises at the bottom when list items are selected.",
  overview="<p>Count, bulk actions, clear.</p>",
  anatomy=(f'<div class="select-bar" style="position:relative;width:100%;"><strong>3 selected</strong><span class="topbar__spacer"></span><button class="btn btn--sm" type="button">Tag</button><button class="btn btn--sm" type="button">Export 3</button><button class="btn btn--sm btn--ghost" type="button" aria-label="Clear selection">{icon("close", "icon icon--sm")}</button></div>', [("Count", "Bold"), ("Actions", "Small inverse buttons"), ("Clear", "Icon")]),
  variants=[('<div class="select-bar" style="position:relative;"><strong>1 selected</strong></div>', "Single.")], sizes="One size.",
  states=(["Visible"], [("Bar", ['<div class="select-bar" style="position:relative;"><strong>3 selected</strong></div>'])]),
  sample='<div class="select-bar" style="position:relative;"><strong>3 selected</strong><button class="btn btn--sm" type="button">Export 3</button></div>',
  responsive=["Sticky 24px above the bottom; wraps on phones."], tokens=[("Surface", "--color-bg-inverse"), ("Text", "--color-fg-inverse"), ("Button border", "--color-border-inverse")],
  a11y=dict(pattern="<code>role=\"region\" aria-label=\"3 organisations selected\"</code>.", keys=[("Tab", "Actions"), ("Esc", "Clear selection")], focus="Not moved on appear.", label="Count in the region label.", pairs=[("Text", "--color-fg-inverse", "--color-bg-inverse")], motion="Slides up over --duration-base.", touch="32px buttons."),
  content=["Actions name the count: Export 3."],
  dos=[('<button class="btn btn--sm" type="button">Export 3</button>', "Counted.", '<button class="btn btn--sm" type="button">Export</button>', "Ambiguous scope.")],
  code=('<div class="select-bar" role="region" aria-label="…">…</div>', [("select-bar", "Bar")]), sources=["pages/organizations/selected"], drift="None.")

C(id="hero-field", name="Hero field", group="Feedback", lead="The WebGPU grain field behind the home hero. Thins out on the left so the title sits on clean canvas.",
  overview="<p>4,000 grains, compute + render passes in WGSL, tinted from <code>--color-accent</code>. Falls back to a slow conic gradient without WebGPU; stills under reduced motion.</p>",
  anatomy=('<div style="position:relative;width:100%;height:8rem;isolation:isolate;overflow:hidden;border-radius:var(--radius-lg);"><canvas class="field-canvas" data-gpu="off" aria-hidden="true" style="top:0;left:0;width:100%;height:100%;"></canvas><p style="padding:var(--space-6);font:var(--text-h3);">The field is ripe.</p></div>', [("Canvas", "Bleeds into margins, masked to fade down"), ("Title", "Display, max 14ch")]),
  variants=[('<span class="tag">data-gpu="on" (WebGPU)</span><span class="tag">data-gpu="off" (CSS fallback)</span>', "Two renderers.")], sizes="Hero height; canvas covers it.",
  states=(["WebGPU", "Fallback", "Reduced motion"], [("Field", ['<span class="tag">Drifting grains</span>', '<span class="tag">Turning gradient</span>', '<span class="tag">Single still frame</span>'])]),
  sample='<div style="position:relative;width:100%;height:4rem;isolation:isolate;overflow:hidden;"><canvas class="field-canvas" data-gpu="off" aria-hidden="true" style="top:0;left:0;width:100%;height:100%;"></canvas></div>',
  responsive=["Resolution follows devicePixelRatio (max 2) via ResizeObserver."], tokens=[("Tint", "--color-accent"), ("Fallback cycle", "--duration-ambient")],
  a11y=dict(pattern="Decorative canvas, <code>aria-hidden</code>, pointer-events none.", keys=[], focus="—", label="—", pairs=[], motion="Can be switched off in Settings; reduced motion renders one frame.", touch="—"),
  content=["Never put text on the dense right side."],
  dos=[('<span class="tag">Accent at 55% opacity</span>', "Quiet.", '<span class="tag">Full-opacity, full-width</span>', "Competes with the title.")],
  code=('<canvas class="field-canvas" aria-hidden="true"></canvas><script src="field.js"></script>', [("field-canvas", "Positioning and fallback"), ("data-gpu", "Set by field.js")]), sources=["pages/field/default"], drift="Canvas had no intrinsic size and rendered 300×150; explicit width/height added.")


# ============================================================================ Renderer
def render(spec: dict) -> None:
    prefix = "../"
    fig, parts = spec["anatomy"]
    callouts = "".join(f'<span class="ds-callout" style="left:{8 + i * 22}%;top:{8 if i % 2 == 0 else 78}%;" aria-hidden="true">{i + 1}</span>' for i in range(len(parts)))
    anatomy = (f'<div class="ds-anatomy"><figure class="ds-anatomy__figure">{fig}{callouts}</figure><ol class="ds-anatomy__list">'
               + "".join(f"<li><div><b>{t}</b><small>{n}</small></div></li>" for t, n in parts) + "</ol></div>")
    variants = "<p>Variants change emphasis or content, never meaning.</p>" + "".join(example(h, c) for h, c in spec["variants"])
    sizes = spec["sizes"]
    sizes_html, sizes_na = (None, sizes) if isinstance(sizes, str) else ("".join(example(h, c) for h, c in sizes), None)
    cols, rows = spec["states"]
    states = ("<p>Pointer and focus states are forced with <code>data-state</code>; real pages use the pseudo-classes.</p>" + matrix(cols, rows) + themes(spec["sample"]))
    responsive = ul(spec["responsive"])
    tok_list = ", ".join(f"<code>{t}</code>" for _, t in spec["tokens"])
    theming = (f"<p>Reads {tok_list}. Dark theme comes from the semantic tokens; nothing in the component changes. To re-theme, override the semantic tokens in a <code>[data-theme]</code> block (see <a href=\"../foundations/theming.html\">theming</a>).</p>" + themes(spec["sample"]))
    a = spec["a11y"]
    pairs = "".join(pair(p[0], p[1], p[2], p[3] if len(p) > 3 else 4.5) for p in a["pairs"]) or "<p>No text or meaningful non-text colour; decorative only.</p>"
    access = (f"<h3>Role and pattern</h3><p>{a['pattern']}</p><h3>Keyboard</h3>" + (keys(a["keys"]) if a["keys"] else "<p>Not interactive.</p>")
              + f"<h3>Focus</h3><p>{a['focus']}</p><h3>Labelling</h3><p>{a['label']}</p><h3>Contrast</h3>{pairs}<h3>Motion</h3><p>{a['motion']}</p><h3>Touch</h3><p>{a['touch']}</p>")
    content = ul(spec["content"])
    snippet, classes = spec["code"]
    code = (f"<pre><code>{snippet.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</code></pre>" + table(["Class / attribute", "Effect"], [[f"<code>{c}</code>", e] for c, e in classes]))
    sources = "<p>Mocks this component was extracted from:</p>" + mock_links(prefix, spec["sources"]) + f"<p>Drift fixed during extraction: {spec['drift']}</p>"
    sections = [("overview", "Overview", spec["overview"], None), ("anatomy", "Anatomy", anatomy, None), ("variants", "Variants", variants, None),
                ("sizes", "Sizes", sizes_html or "", sizes_na), ("states", "States", states, None), ("responsive", "Responsive behaviour", responsive, None),
                ("theming", "Theming", theming, None), ("accessibility", "Accessibility", access, None), ("content", "Content", content, None),
                ("do-dont", "Do and don't", dodont(spec["dos"]), None), ("tokens", "Tokens", token_table(spec["tokens"]), None), ("code", "Code", code, None),
                ("sources", "Sources", sources, None)]
    page(f"components/{spec['id']}.html", spec["name"], f"Component · {spec['group']}", spec["lead"], sections, head=spec.get("head", ""))


def build() -> None:
    for spec in SPECS:
        render(spec)
