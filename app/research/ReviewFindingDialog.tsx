"use client";

import { useEffect, useRef, useState } from "react";
import { AlertIcon } from "@/components/AlertIcon";
import { Modal } from "@/components/Modal";
import type { FindingView } from "@/lib/types";

type Field = { key: string; label: string; required?: string; kind?: "select" | "textarea" };

const FIELDS: Record<FindingView["subjectKind"], Field[]> = {
  Person: [
    { key: "role", label: "Role", required: "Enter a role" },
    { key: "since", label: "Since" },
    { key: "organization", label: "Organisation", kind: "select" },
  ],
  Organization: [
    { key: "name", label: "Name", required: "Enter a name" },
    { key: "location", label: "Location" },
    { key: "summary", label: "Summary", kind: "textarea" },
  ],
};

type Props = {
  finding: FindingView;
  organizations: string[];
  onAccept: (fields: Record<string, string>) => Promise<void>;
  onReject: () => void;
  onClose: () => void;
};

export function ReviewFindingDialog({ finding, organizations, onAccept, onReject, onClose }: Props) {
  const fields = FIELDS[finding.subjectKind];
  const [values, setValues] = useState<Record<string, string>>(() => ({ ...finding.fields }));
  const [errors, setErrors] = useState<Field[]>([]);
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);
  const verified = finding.sources.length >= 2;
  const orgOptions = [...new Set([values.organization, ...organizations].filter(Boolean))];

  useEffect(() => {
    if (errors.length) summaryRef.current?.focus();
  }, [errors]);

  async function accept() {
    const missing = fields.filter((f) => f.required && !values[f.key]?.trim());
    setErrors(missing);
    if (missing.length) return;
    setFailed(false);
    setBusy(true);
    try {
      await onAccept(values);
    } catch {
      setFailed(true);
      setBusy(false);
    }
  }

  const id = (key: string) => `rf-${key}`;

  return (
    <Modal
      title="Review finding"
      description={finding.organization ? `Updates ${finding.subject} · ${finding.organization}` : `Updates ${finding.subject}`}
      onClose={onClose}
      footer={
        <>
          <button className="btn btn--ghost" type="button" onClick={onReject} disabled={busy}>
            Reject
          </button>
          <button className="btn" type="button" onClick={onClose} disabled={busy}>
            Cancel
          </button>
          <button className="btn btn--primary" type="button" onClick={accept} aria-busy={busy || undefined}>
            Accept
          </button>
        </>
      }
    >
      {errors.length > 0 && (
        <div className="alert alert--danger form-summary" role="alert" tabIndex={-1} ref={summaryRef}>
          <AlertIcon />
          <div className="alert__body">
            <div className="alert__title">
              Fix {errors.length} {errors.length === 1 ? "thing" : "things"} to save
            </div>
            <ul style={{ margin: 0, paddingLeft: "var(--space-5)" }}>
              {errors.map((f) => (
                <li key={f.key}>
                  <a href={`#${id(f.key)}`}>{f.required}</a>
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
            <div>Your edits are kept. Try again.</div>
          </div>
        </div>
      )}
      <blockquote className="finding__claim" style={{ borderLeft: "4px solid var(--color-accent)", paddingLeft: "var(--space-4)" }}>
        {finding.statement}
      </blockquote>
      <div className="finding__meta">
        <span>Confidence {finding.confidence}%</span>
        <span>·</span>
        <span>{finding.sources.length} sources</span>
        <span>·</span>
        <span className={verified ? "verify verify--verified" : "verify verify--pending"}>{verified ? "Verified" : "Unverified"}</span>
      </div>
      {fields.map((f, i) => {
        const invalid = errors.includes(f);
        const common = {
          id: id(f.key),
          name: id(f.key),
          value: values[f.key] ?? "",
          disabled: busy,
          autoFocus: i === 0,
          "aria-invalid": invalid || undefined,
          "aria-describedby": invalid ? `${id(f.key)}-error` : undefined,
          onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
            setValues({ ...values, [f.key]: e.target.value }),
        };
        return (
          <div key={f.key} className="field">
            <label className="field__label" htmlFor={id(f.key)}>
              {f.label}
            </label>
            {f.kind === "select" ? (
              <select className="select" {...common}>
                {orgOptions.map((o) => (
                  <option key={o}>{o}</option>
                ))}
              </select>
            ) : f.kind === "textarea" ? (
              <textarea className="textarea" rows={3} {...common}></textarea>
            ) : (
              <input className="input" type="text" {...common} />
            )}
            {invalid && (
              <span className="field__error" id={`${id(f.key)}-error`}>
                {f.required}
              </span>
            )}
          </div>
        );
      })}
      <section aria-labelledby="rf-sources">
        <h3 className="section__title" id="rf-sources" style={{ marginBottom: "var(--space-2)" }}>
          Sources
        </h3>
        {finding.sources.map((s, i) => (
          <div key={i} className="source">
            <svg className="icon icon--sm text-subtle" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" />
            </svg>
            <div>
              <a href={s.url} target="_blank" rel="noopener">
                {s.title}
              </a>
              <div className="source__host">
                {s.domain}
                {s.date && ` · ${s.date}`}
              </div>
            </div>
          </div>
        ))}
      </section>
    </Modal>
  );
}
