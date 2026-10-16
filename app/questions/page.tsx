"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useRunResearch } from "@/components/RunResearch";
import { getJson } from "@/lib/api";
import type { QuestionsOverview } from "@/lib/types";
import { QuestionCard } from "./QuestionCard";

export default function QuestionsPage() {
  const [overview, setOverview] = useState<QuestionsOverview | null>(null);
  const [failed, setFailed] = useState(false);
  const runResearch = useRunResearch();

  const load = useCallback(() => {
    setFailed(false);
    setOverview(null);
    getJson<QuestionsOverview>("/api/questions").then(setOverview, () => setFailed(true));
  }, []);

  useEffect(load, [load]);

  const empty = overview && overview.answered + overview.partial === 0;

  return (
    <main id="main" className="container app-main">
      <div className="page-header rise">
        <div>
          <h1>Questions</h1>
          {overview || failed ? (
            <p className="subtitle">
              {failed || !overview
                ? ""
                : empty
                  ? "Nothing answered yet"
                  : `${overview.total} questions · ${overview.answered} answered · ${overview.partial} partial`}
            </p>
          ) : (
            <span className="skeleton skeleton--text" style={{ width: "16rem" }}></span>
          )}
        </div>
        <div className="cluster">
          <button type="button" className="btn btn--primary" onClick={() => runResearch()}>
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.5 6.5l2.5 2.5M15 15l2.5 2.5M6.5 17.5 9 15M15 9l2.5-2.5" />
            </svg>
            Ask the web
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
          <h2 className="empty__title">Couldn&apos;t load the answers</h2>
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
        <div className="stack" aria-busy="true" aria-label="Loading questions" style={{ gap: "var(--space-6)" }}>
          {[0, 1, 2].map((i) => (
            <div key={i} className="card answer">
              <span className="skeleton skeleton--text" style={{ width: "10rem" }}></span>
              <span className="skeleton skeleton--title"></span>
              <span className="skeleton skeleton--text"></span>
              <span className="skeleton skeleton--text"></span>
            </div>
          ))}
        </div>
      ) : (
        <div className="stack" style={{ gap: "var(--space-6)" }}>
          {overview.questions.map((q, i) => (
            <QuestionCard key={q.number} question={q} index={i} />
          ))}
        </div>
      )}
    </main>
  );
}
