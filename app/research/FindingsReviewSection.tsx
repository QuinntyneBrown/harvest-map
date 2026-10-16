"use client";

import type { FindingView } from "@/lib/types";
import { FindingCard } from "./FindingCard";

type Props = { findings: FindingView[]; organizations: string[]; currentUser: string; onChanged: () => void };

export function FindingsReviewSection({ findings, organizations, currentUser, onChanged }: Props) {
  return (
    <section className="section" style={{ marginTop: 0 }} aria-labelledby="findings-title">
      <div className="cluster cluster--between" style={{ marginBottom: "var(--space-6)" }}>
        <h2 className="section__title" id="findings-title" style={{ margin: 0 }}>
          Findings to review
        </h2>
        <span className="text-caption">Accept creates or updates the record · Reject keeps the source</span>
      </div>
      <div className="stack" style={{ gap: "var(--space-4)" }}>
        {findings.map((finding, i) => (
          <FindingCard key={finding.id} finding={finding} index={i} currentUser={currentUser} organizations={organizations} onChanged={onChanged} />
        ))}
      </div>
    </section>
  );
}
