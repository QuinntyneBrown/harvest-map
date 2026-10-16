"use client";

import { createContext, useContext, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { getJson, postJson } from "@/lib/api";
import { CORE_QUESTIONS } from "@/lib/questions";
import { AlertIcon } from "./AlertIcon";
import { Modal } from "./Modal";

type Depth = "quick" | "standard" | "deep";

const LOOK_FOR = [
  ["orgs", "Organisations"],
  ["people", "People"],
  ["linkedin", "LinkedIn profiles"],
] as const;

const DEPTHS = [
  ["quick", "Quick", "about 1 minute"],
  ["standard", "Standard", "about 5 minutes"],
  ["deep", "Deep", "about 20 minutes · more sources"],
] as const;

const RunResearchContext = createContext<(question?: number) => void>(() => {});

/** Opens the Ask the web dialog, optionally with a core question preselected. */
export function useRunResearch() {
  return useContext(RunResearchContext);
}

export function RunResearchProvider({ children }: { children: React.ReactNode }) {
  const [openWith, setOpenWith] = useState<number | null>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (e.key !== "r" || e.ctrlKey || e.metaKey || e.altKey) return;
      if (target.closest("input, textarea, select, [contenteditable], [role=dialog]")) return;
      e.preventDefault();
      setOpenWith((current) => current ?? 1);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, []);

  return (
    <RunResearchContext.Provider value={(question = 1) => setOpenWith(question)}>
      {children}
      {openWith !== null && <RunResearchDialog question={openWith} onClose={() => setOpenWith(null)} />}
    </RunResearchContext.Provider>
  );
}

function RunResearchDialog({ question, onClose }: { question: number; onClose: () => void }) {
  const [choice, setChoice] = useState<string>(`q${question}`);
  const [lookFor, setLookFor] = useState<string[]>(LOOK_FOR.map(([v]) => v));
  const [depth, setDepth] = useState<Depth>("standard");
  const [custom, setCustom] = useState("");
  const [invalid, setInvalid] = useState(false);
  const [busy, setBusy] = useState(false);
  const [failure, setFailure] = useState<string | null>(null);
  const router = useRouter();
  const checkedRef = useRef<HTMLInputElement>(null);
  const summaryRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    checkedRef.current?.focus();
    getJson<{ defaultDepth: Depth }>("/api/settings").then((s) => setDepth(s.defaultDepth), () => {});
  }, []);

  useEffect(() => {
    if (invalid) summaryRef.current?.focus();
  }, [invalid]);

  async function run() {
    if (choice === "custom" && !custom.trim()) {
      setInvalid(true);
      return;
    }
    setInvalid(false);
    setFailure(null);
    setBusy(true);
    try {
      await postJson("/api/research/runs", {
        question: choice === "custom" ? null : Number(choice.slice(1)),
        customQuestion: choice === "custom" ? custom.trim() : null,
        lookFor,
        depth,
      });
      onClose();
      window.dispatchEvent(new Event("research:queued"));
      router.push("/research");
    } catch (e) {
      setFailure((e as Error).message);
      setBusy(false);
    }
  }

  return (
    <Modal
      title="Ask the web"
      onClose={onClose}
      footer={
        <>
          <button className="btn" type="button" onClick={onClose} disabled={busy}>
            Cancel
          </button>
          <button className="btn btn--primary" type="button" onClick={run} aria-busy={busy || undefined}>
            Run
          </button>
        </>
      }
    >
      {invalid && (
        <div className="alert alert--danger form-summary" role="alert" tabIndex={-1} ref={summaryRef}>
          <AlertIcon />
          <div className="alert__body">
            <div className="alert__title">Fix 1 thing to save</div>
            <ul style={{ margin: 0, paddingLeft: "var(--space-5)" }}>
              <li>
                <a href="#rr-custom">Write the question you want answered</a>
              </li>
            </ul>
          </div>
        </div>
      )}
      {failure && (
        <div className="alert alert--danger" role="alert">
          <AlertIcon />
          <div className="alert__body">
            <div className="alert__title">Couldn&apos;t start the run</div>
            <div>{failure}</div>
          </div>
        </div>
      )}
      <fieldset disabled={busy} className="stack" style={{ gap: "var(--space-5)", border: 0, padding: 0, margin: 0, minWidth: 0 }}>
      <fieldset>
        <legend>Question</legend>
        {[...CORE_QUESTIONS.map((text, i) => [`q${i + 1}`, text]), ["custom", "Something else"]].map(([value, text]) => (
          <label key={value} className="choice">
            <input
              ref={value === choice ? checkedRef : undefined}
              type="radio"
              name="question"
              value={value}
              checked={choice === value}
              onChange={() => setChoice(value)}
            />
            <span className="choice__text">{text}</span>
          </label>
        ))}
      </fieldset>
      {choice === "custom" && (
        <div className="field">
          <label className="field__label" htmlFor="rr-custom">
            Your question
          </label>
          <textarea
            className="textarea"
            id="rr-custom"
            name="rr-custom"
            rows={2}
            value={custom}
            onChange={(e) => setCustom(e.target.value)}
            aria-invalid={invalid || undefined}
            aria-describedby={invalid ? "rr-custom-error" : undefined}
          ></textarea>
          {invalid && (
            <span className="field__error" id="rr-custom-error">
              Write the question you want answered
            </span>
          )}
        </div>
      )}
      <div className="grid" style={{ "--layout-columns": 2 } as React.CSSProperties}>
        <fieldset>
          <legend>Look for</legend>
          {LOOK_FOR.map(([value, label]) => (
            <label key={value} className="choice">
              <input
                type="checkbox"
                name="scope"
                value={value}
                checked={lookFor.includes(value)}
                onChange={(e) => setLookFor(e.target.checked ? [...lookFor, value] : lookFor.filter((v) => v !== value))}
              />
              <span className="choice__text">{label}</span>
            </label>
          ))}
        </fieldset>
        <fieldset>
          <legend>Depth</legend>
          {DEPTHS.map(([value, label, hint]) => (
            <label key={value} className="choice">
              <input type="radio" name="depth" value={value} checked={depth === value} onChange={() => setDepth(value)} />
              <span className="choice__text">
                {label} <small>{hint}</small>
              </span>
            </label>
          ))}
        </fieldset>
      </div>
      </fieldset>
      <p className="text-caption">Findings need two sources, or one trusted source, before they count as verified.</p>
    </Modal>
  );
}
