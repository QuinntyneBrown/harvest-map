"use client";

import { useState } from "react";
import { AlertIcon } from "@/components/AlertIcon";
import { Modal } from "@/components/Modal";
import { ORG_TAGS } from "@/lib/validation/organization";

type Props = { count: number; onApply: (tag: string, mode: "add" | "remove") => Promise<void>; onClose: () => void };

/** Adds or removes one tag on every selected organization. */
export function BulkTagDialog({ count, onApply, onClose }: Props) {
  const [tag, setTag] = useState<string>(ORG_TAGS[0]);
  const [mode, setMode] = useState<"add" | "remove">("add");
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);

  async function apply() {
    setFailed(false);
    setBusy(true);
    try {
      await onApply(tag, mode);
    } catch {
      setFailed(true);
      setBusy(false);
    }
  }

  return (
    <Modal
      title={`Tag ${count} ${count === 1 ? "organization" : "organizations"}`}
      size="sm"
      busy={busy}
      onClose={onClose}
      footer={
        <>
          <button className="btn" type="button" onClick={onClose} disabled={busy}>
            Cancel
          </button>
          <button className="btn btn--primary" type="button" onClick={apply} aria-busy={busy || undefined}>
            Apply
          </button>
        </>
      }
    >
      {failed && (
        <div className="alert alert--danger" role="alert">
          <AlertIcon />
          <div className="alert__body">Couldn&apos;t tag. Try again.</div>
        </div>
      )}
      <div className="field">
        <label className="field__label" htmlFor="bulk-tag">
          Tag
        </label>
        <select className="select" id="bulk-tag" value={tag} disabled={busy} onChange={(e) => setTag(e.target.value)}>
          {ORG_TAGS.map((t) => (
            <option key={t}>{t}</option>
          ))}
        </select>
      </div>
      <fieldset disabled={busy}>
        <legend>Change</legend>
        <label className="choice">
          <input type="radio" name="mode" checked={mode === "add"} onChange={() => setMode("add")} />
          <span className="choice__text">Add tag</span>
        </label>
        <label className="choice">
          <input type="radio" name="mode" checked={mode === "remove"} onChange={() => setMode("remove")} />
          <span className="choice__text">Remove tag</span>
        </label>
      </fieldset>
    </Modal>
  );
}
