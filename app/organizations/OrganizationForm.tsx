"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { AlertIcon } from "@/components/AlertIcon";
import { useToast } from "@/components/Toasts";
import { UnsavedChangesDialog } from "@/components/UnsavedChangesDialog";
import { postJson } from "@/lib/api";
import { type FieldError, ORG_TAGS, ORG_TYPES, type OrganizationInput, validateOrganization } from "@/lib/validation/organization";

const FIELD_IDS: Record<keyof OrganizationInput, string> = {
  name: "org-name",
  type: "org-kind",
  founded: "org-founded",
  city: "org-city",
  country: "org-country",
  website: "org-site",
  summary: "org-summary",
  tags: "org-tags",
};

const LABELS: Record<keyof OrganizationInput, string> = {
  name: "Name",
  type: "Type",
  founded: "Founded",
  city: "City",
  country: "Country",
  website: "Website",
  summary: "Summary",
  tags: "Tags",
};

type Props = {
  /** Null when creating a new organization. */
  id: string | null;
  name: string;
  initial: OrganizationInput;
  /** Where Cancel and Discard go. */
  backHref: string;
};

export function OrganizationForm({ id, name, initial: given, backHref }: Props) {
  // Tags are kept in the canonical order so toggling one on and off is not a change.
  const [initial] = useState<OrganizationInput>(() => ({ ...given, tags: ORG_TAGS.filter((t) => given.tags.includes(t)) }));
  const router = useRouter();
  const toast = useToast();
  const [input, setInput] = useState<OrganizationInput>(initial);
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);
  const [confirmLeave, setConfirmLeave] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);
  const saved = useRef(false);

  const changed = (Object.keys(initial) as (keyof OrganizationInput)[]).filter((k) => JSON.stringify(input[k]) !== JSON.stringify(initial[k]));
  const dirty = changed.length > 0 && !saved.current;

  useEffect(() => {
    if (errors.length) summaryRef.current?.focus();
  }, [errors]);

  useEffect(() => {
    if (!dirty) return;
    const beforeUnload = (e: BeforeUnloadEvent) => e.preventDefault();
    const onPop = () => {
      setConfirmLeave(true);
      history.pushState(null, "", location.href);
    };
    history.pushState(null, "", location.href);
    window.addEventListener("beforeunload", beforeUnload);
    window.addEventListener("popstate", onPop);
    return () => {
      window.removeEventListener("beforeunload", beforeUnload);
      window.removeEventListener("popstate", onPop);
    };
  }, [dirty]);

  const set = <K extends keyof OrganizationInput>(key: K, value: OrganizationInput[K]) => setInput((i) => ({ ...i, [key]: value }));
  const errorOf = (key: keyof OrganizationInput) => errors.find((e) => e.field === key)?.message;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (busy) return;
    const found = validateOrganization(input);
    setErrors(found);
    if (found.length) return;
    setFailed(false);
    setBusy(true);
    try {
      const res = await postJson<{ id: string }>(id ? `/api/organizations/${id}` : "/api/organizations", input);
      saved.current = true;
      toast({ kind: "success", title: `${input.name.trim()} saved` });
      router.push(`/organizations/${res.id}`);
    } catch {
      setFailed(true);
      setBusy(false);
    }
  }

  function cancel() {
    if (dirty) setConfirmLeave(true);
    else router.push(backHref);
  }

  const field = (key: keyof OrganizationInput, optional = false) => (
    <label className="field__label" htmlFor={FIELD_IDS[key]}>
      {LABELS[key]} {optional && <span className="optional">(optional)</span>}
    </label>
  );
  const err = (key: keyof OrganizationInput) =>
    errorOf(key) && (
      <span className="field__error" id={`${FIELD_IDS[key]}-error`}>
        {errorOf(key)}
      </span>
    );
  const aria = (key: keyof OrganizationInput) => ({ "aria-invalid": errorOf(key) ? true : undefined, "aria-describedby": errorOf(key) ? `${FIELD_IDS[key]}-error` : undefined });

  return (
    <>
      <form className="stack card" style={{ gap: "var(--space-6)", padding: "var(--space-8)", maxWidth: "44rem" }} noValidate onSubmit={submit}>
        {errors.length > 0 && (
          <div className="alert alert--danger form-summary" role="alert" tabIndex={-1} ref={summaryRef}>
            <AlertIcon />
            <div className="alert__body">
              <div className="alert__title">
                Fix {errors.length} {errors.length === 1 ? "thing" : "things"} to save
              </div>
              <ul style={{ margin: 0, paddingLeft: "var(--space-5)" }}>
                {errors.map((e) => (
                  <li key={e.field}>
                    <a
                      href={`#${FIELD_IDS[e.field]}`}
                      onClick={(ev) => {
                        ev.preventDefault();
                        document.getElementById(FIELD_IDS[e.field])?.focus();
                      }}
                    >
                      {e.message}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
        {failed && (
          <div className="alert alert--danger" role="alert">
            <AlertIcon />
            <div className="alert__body">
              <div className="alert__title">Couldn&apos;t save</div>
              <div>Your changes are kept. Try again.</div>
            </div>
          </div>
        )}

        <div className="field">
          {field("name")}
          <input className="input" id="org-name" name="org-name" type="text" dir="auto" value={input.name} onChange={(e) => set("name", e.target.value)} autoFocus {...aria("name")} />
          {err("name")}
        </div>
        <div className="grid" style={{ "--layout-columns": 2 } as React.CSSProperties}>
          <div className="field">
            {field("type")}
            <select className="select" id="org-kind" name="org-kind" value={input.type} onChange={(e) => set("type", e.target.value)}>
              {ORG_TYPES.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>
          <div className="field">
            {field("founded", true)}
            <input className="input" id="org-founded" name="org-founded" type="text" inputMode="numeric" value={input.founded} onChange={(e) => set("founded", e.target.value)} {...aria("founded")} />
            {err("founded")}
          </div>
          <div className="field">
            {field("city", true)}
            <input className="input" id="org-city" name="org-city" type="text" value={input.city} onChange={(e) => set("city", e.target.value)} />
          </div>
          <div className="field">
            {field("country")}
            <input className="input" id="org-country" name="org-country" type="text" value={input.country} onChange={(e) => set("country", e.target.value)} {...aria("country")} />
            {err("country")}
          </div>
        </div>
        <div className="field">
          {field("website")}
          <input className="input" id="org-site" name="org-site" type="text" value={input.website} onChange={(e) => set("website", e.target.value)} {...aria("website")} />
          {err("website")}
        </div>
        <div className="field">
          {field("summary")}
          <textarea className="textarea" id="org-summary" name="org-summary" rows={3} dir="auto" value={input.summary} onChange={(e) => set("summary", e.target.value)} aria-describedby="org-summary-help"></textarea>
          <span className="field__help" id="org-summary-help">
            One sentence. The field grows with the text.
          </span>
        </div>
        <fieldset id="org-tags">
          <legend>Tags</legend>
          <div className="cluster">
            {ORG_TAGS.map((t) => (
              <label key={t} className="chip" style={{ gap: "var(--space-2)" }}>
                <input
                  type="checkbox"
                  name="tags"
                  value={t}
                  checked={input.tags.includes(t)}
                  onChange={(e) => set("tags", ORG_TAGS.filter((x) => (x === t ? e.target.checked : input.tags.includes(x))))}
                  style={{ accentColor: "var(--color-accent)", margin: 0 }}
                />{" "}
                {t}
              </label>
            ))}
          </div>
        </fieldset>
        <div className="form-actions" style={{ justifyContent: "space-between", alignItems: "center" }}>
          <span className="topbar__spacer"></span>
          <button className="btn btn--ghost" type="button" onClick={cancel}>
            Cancel
          </button>
          <button className="btn btn--primary" type="submit" aria-busy={busy || undefined}>
            Save
          </button>
        </div>
      </form>
      {confirmLeave && (
        <UnsavedChangesDialog
          name={name}
          changed={changed.map((k) => LABELS[k])}
          onKeep={() => setConfirmLeave(false)}
          onDiscard={() => {
            saved.current = true;
            router.push(backHref);
          }}
        />
      )}
    </>
  );
}
