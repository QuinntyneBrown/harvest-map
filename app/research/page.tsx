"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useRunResearch } from "@/components/RunResearch";
import { getJson } from "@/lib/api";
import type { ResearchOverview } from "@/lib/types";
import { FindingsReviewSection } from "./FindingsReviewSection";
import { RunList } from "./RunList";

const POLL_MS = 3000;

export default function ResearchPage() {
  const [overview, setOverview] = useState<ResearchOverview | null>(null);
  const [failed, setFailed] = useState(false);
  const runResearch = useRunResearch();

  const refresh = useCallback(() => getJson<ResearchOverview>("/api/research").then(setOverview, () => setFailed(true)), []);

  const load = useCallback(() => {
    setFailed(false);
    setOverview(null);
    refresh();
  }, [refresh]);

  useEffect(load, [load]);

  useEffect(() => {
    window.addEventListener("research:queued", refresh);
    return () => window.removeEventListener("research:queued", refresh);
  }, [refresh]);

  const inProgress = overview?.runs.some((r) => r.status === "Queued" || r.status === "Running");
  useEffect(() => {
    if (!inProgress) return;
    const timer = setTimeout(refresh, POLL_MS);
    return () => clearTimeout(timer);
  }, [inProgress, overview, refresh]);

  const empty = overview && overview.runs.length === 0;

  return (
    <main id="main" className="container app-main">
      <div className="page-header rise">
        <div>
          <h1>Research</h1>
          {overview ? (
            <p className="subtitle">
              {empty
                ? "No runs yet"
                : `${overview.totalRuns} runs · ${overview.running} running · ${overview.findingsToReview} findings to review`}
            </p>
          ) : (
            !failed && <span className="skeleton skeleton--text" style={{ width: "16rem" }}></span>
          )}
        </div>
        <div className="cluster">
          <button type="button" className="btn btn--primary" onClick={() => runResearch()}>
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.5 6.5l2.5 2.5M15 15l2.5 2.5M6.5 17.5 9 15M15 9l2.5-2.5" />
            </svg>
            Run research
          </button>
        </div>
      </div>

      {failed ? (
        <div className="empty empty--error">
          <div className="empty__icon" aria-hidden="true">
            <svg className="icon icon--lg" viewBox="0 0 24 24">
              <path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
            </svg>
          </div>
          <h2 className="empty__title">Couldn&apos;t load research runs</h2>
          <p className="empty__text">The request timed out. Try again, or share reference HM-4F2A with support.</p>
          <div className="empty__actions">
            <button type="button" className="btn btn--primary" onClick={load}>
              Try again
            </button>
            <Link className="btn btn--ghost" href="/">
              Go back
            </Link>
          </div>
        </div>
      ) : !overview ? (
        <div className="entity-list" aria-busy="true" aria-label="Loading runs">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="card">
              <span className="skeleton skeleton--title"></span>
              <span className="skeleton skeleton--text" style={{ width: "12rem" }}></span>
            </div>
          ))}
        </div>
      ) : empty ? (
        <div className="empty">
          <h2 className="empty__title">Ask the web</h2>
          <p className="empty__text">
            Pick a question, choose sources and depth. Findings come back for you to accept or reject.
          </p>
          <div className="empty__actions">
            <button type="button" className="btn btn--primary" onClick={() => runResearch()}>
              Run the first research
            </button>
          </div>
        </div>
      ) : (
        <div className="stack" style={{ gap: "var(--space-12)" }}>
          {overview.findings.length > 0 && (
            <FindingsReviewSection findings={overview.findings} organizations={overview.organizations} currentUser={overview.currentUser} onChanged={refresh} />
          )}
          <RunList runs={overview.runs} />
        </div>
      )}
    </main>
  );
}
