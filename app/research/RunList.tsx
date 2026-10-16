import type { RunRow } from "@/lib/types";

const STATUS_CLASS: Record<RunRow["status"], string> = {
  Queued: "run-status--running",
  Running: "run-status--running",
  Done: "run-status--done",
  Failed: "run-status--failed",
};

export function RunList({ runs }: { runs: RunRow[] }) {
  return (
    <section aria-labelledby="runs-title">
      <h2 className="section__title" id="runs-title" style={{ marginBottom: "var(--space-6)" }}>
        Earlier runs
      </h2>
      <div className="entity-list">
        {runs.map((run, i) => (
          <div
            key={run.id}
            data-testid="run-row"
            className="card lift rise"
            style={{ "--i": i, padding: "var(--space-5) var(--space-6)" } as React.CSSProperties}
          >
            <div className="cluster cluster--between">
              <div style={{ minWidth: 0 }}>
                <div className="run-row__title" style={{ font: "var(--text-label)" }}>
                  #{run.id} · {run.title}
                </div>
                <div className="text-caption" style={{ marginTop: "var(--space-1)" }}>
                  {run.startedLabel} · {run.person} · {run.findingCount} findings
                </div>
                {run.failureReason && (
                  <div className="text-caption text-muted" style={{ marginTop: "var(--space-1)" }}>
                    {run.failureReason}
                  </div>
                )}
              </div>
              <span className={`run-status ${STATUS_CLASS[run.status]}`}>
                <span className={run.status === "Running" ? "dot dot--pulse" : "dot"}></span>
                {run.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
