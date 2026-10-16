"use client";

import { startTransition, useEffect, useOptimistic, useState } from "react";
import { AlertIcon } from "@/components/AlertIcon";
import { postJson } from "@/lib/api";
import type { FindingState, FindingView } from "@/lib/types";
import { ReviewFindingDialog } from "./ReviewFindingDialog";

export const UNDO_WINDOW_MS = 30_000;

type Decision = { state: FindingState; by: string | null; at: number | null };

type Props = { finding: FindingView; index: number; currentUser: string; organizations: string[]; onChanged: () => void };

function decisionOf(f: FindingView): Decision {
  return { state: f.state, by: f.decidedBy, at: f.decidedAt ? Date.parse(f.decidedAt) : null };
}

export function FindingCard({ finding, index, currentUser, organizations, onChanged }: Props) {
  const [decision, setDecision] = useState<Decision>(() => decisionOf(finding));
  const [shown, showOptimistic] = useOptimistic(decision, (_: Decision, next: Decision) => next);
  const [failed, setFailed] = useState(false);
  const [now, setNow] = useState(() => Date.now());
  const [editing, setEditing] = useState(false);

  const undoOpen = shown.state !== "Pending" && shown.at !== null && now - shown.at < UNDO_WINDOW_MS;

  useEffect(() => {
    if (!undoOpen || shown.at === null) return;
    const timer = setTimeout(() => setNow(Date.now()), shown.at + UNDO_WINDOW_MS - Date.now());
    return () => clearTimeout(timer);
  }, [undoOpen, shown.at]);

  function decide(action: "accept" | "reject" | "undo") {
    const at = Date.now();
    const next: Decision = action === "undo" ? { state: "Pending", by: null, at: null } : { state: action === "accept" ? "Accepted" : "Rejected", by: currentUser, at };
    setFailed(false);
    setNow(at);
    startTransition(async () => {
      showOptimistic(next);
      try {
        const body = action === "accept" ? { fields: finding.fields } : undefined;
        const result = await postJson<{ finding: FindingView }>(`/api/findings/${finding.id}/${action}`, body);
        startTransition(() => setDecision({ ...decisionOf(result.finding), at: next.at }));
        onChanged();
      } catch {
        setFailed(true);
      }
    });
  }

  async function acceptEdited(fields: Record<string, string>) {
    const result = await postJson<{ finding: FindingView }>(`/api/findings/${finding.id}/accept`, { fields });
    const at = Date.now();
    setNow(at);
    setDecision({ ...decisionOf(result.finding), at });
    setFailed(false);
    setEditing(false);
    onChanged();
  }

  const verb = shown.state === "Accepted" ? "Accepted" : "Rejected";
  const classes = ["card", "finding", "rise", shown.state === "Accepted" && "finding--accepted", shown.state === "Rejected" && "finding--rejected"];

  return (
    <div data-testid="finding" className={classes.filter(Boolean).join(" ")} style={{ "--i": index } as React.CSSProperties}>
      <p className="finding__claim">{finding.statement}</p>
      <div className="finding__meta">
        <span>{finding.subject}</span>
        <span>·</span>
        <span>{finding.sourceDomain}</span>
        <span>·</span>
        <span>Confidence {finding.confidence}%</span>
        {finding.lowConfidenceReason && <span className="verify verify--pending">{finding.lowConfidenceReason}</span>}
      </div>
      {failed && (
        <div className="alert alert--danger" role="alert">
          <AlertIcon />
          <div className="alert__body">Couldn&apos;t save — Try again.</div>
        </div>
      )}
      <div className="finding__actions">
        {shown.state === "Pending" ? (
          <>
            <button className="btn btn--sm btn--primary" type="button" onClick={() => decide("accept")}>
              <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
                <path d="m5 12 4 4L19 6" />
              </svg>
              Accept
            </button>
            <button className="btn btn--sm" type="button" onClick={() => setEditing(true)}>
              Edit
            </button>
            <button className="btn btn--sm btn--ghost" type="button" onClick={() => decide("reject")}>
              Reject
            </button>
          </>
        ) : (
          <>
            <span className="text-caption finding__decision">
              {verb} by {shown.by}
              {undoOpen && " · Undo available for 30 s"}
            </span>
            {undoOpen && (
              <button className="btn btn--sm btn--ghost" type="button" onClick={() => decide("undo")}>
                Undo
              </button>
            )}
          </>
        )}
      </div>
      {editing && (
        <ReviewFindingDialog
          finding={finding}
          organizations={organizations}
          onAccept={acceptEdited}
          onReject={() => {
            setEditing(false);
            decide("reject");
          }}
          onClose={() => setEditing(false)}
        />
      )}
    </div>
  );
}
