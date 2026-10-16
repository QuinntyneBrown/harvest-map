"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { useRunResearch } from "@/components/RunResearch";
import { getJson } from "@/lib/api";
import type { QuestionAnswer, QuestionHeader } from "@/lib/types";

export function QuestionCard({ question, index }: { question: QuestionHeader; index: number }) {
  const [answer, setAnswer] = useState<QuestionAnswer | null>(null);
  const [failed, setFailed] = useState(false);
  const open = question.status === "Open";
  const runResearch = useRunResearch();

  const load = useCallback(() => {
    if (open) return;
    setFailed(false);
    setAnswer(null);
    getJson<QuestionAnswer>(`/api/questions/${question.number}`).then(setAnswer, () => setFailed(true));
  }, [open, question.number]);

  useEffect(load, [load]);

  const n = String(question.number).padStart(2, "0");

  return (
    <section className="card answer rise" style={{ "--i": index } as React.CSSProperties} id={`q${question.number}`}>
      <div className="cluster cluster--between">
        <span className="q-card__n">
          {n} · {question.status} · {question.sourceCount} sources
        </span>
        <button type="button" className="btn btn--sm btn--ghost" onClick={() => runResearch(question.number)}>
          <svg className="icon icon--sm" aria-hidden="true" viewBox="0 0 24 24">
            <path d="M20 12a8 8 0 0 1-14 5.3L4 15M4 12a8 8 0 0 1 14-5.3L20 9M4 4v5h5M20 20v-5h-5" />
          </svg>
          Re-run
        </button>
      </div>
      <h2 className="answer__q">{question.text}</h2>
      {failed ? (
        <div className="alert alert--danger" role="alert">
          <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v6M12 16h.01" />
          </svg>
          <div className="alert__body">
            <div className="alert__title">Couldn&apos;t load this answer</div>
            <div>The findings service didn&apos;t answer in time.</div>
            <div className="alert__actions">
              <button type="button" className="btn btn--link" onClick={load}>
                Retry
              </button>
            </div>
          </div>
        </div>
      ) : open ? (
        <ol className="answer__list">
          <li>
            <button type="button" className="btn btn--link" onClick={() => runResearch(question.number)}>
              Run research to answer this
            </button>
          </li>
        </ol>
      ) : !answer ? (
        <div aria-busy="true" aria-label={`Loading answer ${question.number}`}>
          <span className="skeleton skeleton--text"></span>
          <span className="skeleton skeleton--text"></span>
        </div>
      ) : (
        <ol className="answer__list">
          {answer.items.map((item) => (
            <li key={item.href + item.label}>
              <Link href={item.href}>{item.label}</Link>
              <span className="answer__spacer"></span>
              <span className="text-caption">{item.detail}</span>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
