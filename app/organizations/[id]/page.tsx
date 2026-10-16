"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { AlertIcon } from "@/components/AlertIcon";
import { useRunResearch } from "@/components/RunResearch";
import { getJson, postJson } from "@/lib/api";
import type { OrganizationDetail } from "@/lib/types";

const STATUS_CLASS = { Verified: "verify--verified", Unverified: "verify--pending", Conflict: "verify--conflict" } as const;

type Load = { kind: "loading" } | { kind: "ready"; org: OrganizationDetail } | { kind: "missing" } | { kind: "error" };

export default function OrganizationPage() {
  const { id } = useParams<{ id: string }>();
  const [state, setState] = useState<Load>({ kind: "loading" });
  const [restoreFailed, setRestoreFailed] = useState(false);
  const runResearch = useRunResearch();

  const load = useCallback(() => {
    setState({ kind: "loading" });
    getJson<OrganizationDetail>(`/api/organizations/${id}`).then(
      (org) => setState({ kind: "ready", org }),
      (e: Error) => setState(e.message === "404" ? { kind: "missing" } : { kind: "error" }),
    );
  }, [id]);

  useEffect(load, [load]);

  async function restore() {
    setRestoreFailed(false);
    try {
      const res = await postJson<{ organization: OrganizationDetail }>(`/api/organizations/${id}/restore`);
      setState({ kind: "ready", org: res.organization });
    } catch {
      setRestoreFailed(true);
    }
  }

  if (state.kind === "loading") {
    return (
      <main id="main" className="container app-main" aria-busy="true" aria-label="Loading organization">
        <span className="skeleton skeleton--title"></span>
        <span className="skeleton skeleton--text" style={{ width: "24rem" }}></span>
        <span className="skeleton skeleton--text"></span>
      </main>
    );
  }
  if (state.kind === "missing") {
    return (
      <main id="main" className="container app-main">
        <div className="empty">
          <h1 className="empty__title">Nothing grows here</h1>
          <p className="empty__text">That organization doesn&apos;t exist, or it was deleted.</p>
          <div className="empty__actions">
            <Link className="btn btn--primary" href="/organizations">
              Back to organizations
            </Link>
          </div>
        </div>
      </main>
    );
  }
  if (state.kind === "error") {
    return (
      <main id="main" className="container app-main">
        <div className="empty empty--error">
          <h1 className="empty__title">Couldn&apos;t load this organization</h1>
          <p className="empty__text">The request timed out. Try again, or share reference HM-4F2A with support.</p>
          <div className="empty__actions">
            <button type="button" className="btn btn--primary" onClick={load}>
              Retry
            </button>
          </div>
        </div>
      </main>
    );
  }

  const org = state.org;
  const archived = org.archived !== null;

  return (
    <main id="main" className="container app-main">
      {archived && (
        <div className="alert alert--warning" role="status" style={{ marginBottom: "var(--space-6)" }}>
          <AlertIcon />
          <div className="alert__body">
            <div className="alert__title">
              Archived by {org.archived!.by} · {org.archived!.at}
            </div>
            <div>Read-only until restored.</div>
          </div>
        </div>
      )}
      {restoreFailed && (
        <div className="alert alert--danger" role="alert" style={{ marginBottom: "var(--space-6)" }}>
          <AlertIcon />
          <div className="alert__body">Couldn&apos;t restore. Try again.</div>
        </div>
      )}
      <nav aria-label="Breadcrumb" style={{ marginBottom: "var(--space-6)" }}>
        <ol className="breadcrumb">
          <li>
            <Link href="/organizations">Organizations</Link>
          </li>
          <li aria-current="page">{org.name}</li>
        </ol>
      </nav>

      <div className="page-header rise">
        <div className="cluster" style={{ alignItems: "flex-start", gap: "var(--space-6)" }}>
          <span className="mark mark--lg" aria-hidden="true">
            {org.mark}
          </span>
          <div>
            <div className="cluster" style={{ gap: "var(--space-3)" }}>
              <h1 dir="auto">{org.name}</h1>
              <span className={`verify ${STATUS_CLASS[org.status]}`}>{org.status}</span>
            </div>
            <p className="subtitle">{org.summary}</p>
            <div className="tags">
              {org.tags.map((t) => (
                <span key={t} className={t === "AI" ? "tag tag--ai" : t === "Moonshot" ? "tag tag--moonshot" : "tag"}>
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
        <div className="cluster">
          {archived ? (
            <button type="button" className="btn btn--primary" onClick={restore}>
              Restore
            </button>
          ) : (
            <>
              <Link className="btn btn--ghost" href={`/organizations/${org.id}/edit`}>
                Edit
              </Link>
              <button type="button" className="btn btn--ghost" style={{ color: "var(--color-danger-fg)" }}>
                Delete
              </button>
              <button type="button" className="btn btn--primary" onClick={() => runResearch(undefined, `What is ${org.name} doing?`)}>
                Research
              </button>
            </>
          )}
        </div>
      </div>

      <div className={`detail${archived ? " card--archived" : ""}`} style={{ padding: 0, border: 0, background: "none" }}>
        <div className="stack" style={{ gap: "var(--space-12)" }}>
          <section>
            <h2 className="section__title">What they&apos;re doing</h2>
            {org.initiatives.length ? (
              <ul className="list" style={{ font: "var(--text-body-lg)" }}>
                {org.initiatives.map((i) => (
                  <li key={i} className="people-row" style={{ display: "block" }}>
                    {i}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted">Nothing recorded yet. Run research to find out.</p>
            )}
          </section>

          <section>
            <div className="cluster cluster--between" style={{ marginBottom: "var(--space-6)" }}>
              <h2 className="section__title" style={{ margin: 0 }}>
                People
              </h2>
              {!archived && (
                <button type="button" className="btn btn--sm">
                  Add
                </button>
              )}
            </div>
            {org.people.length ? (
              <div className="entity-list">
                {org.people.map((p) => (
                  <div key={p.id} className="card lift" style={{ padding: 0 }}>
                    <div className="org-card" style={{ gridTemplateColumns: "auto 1fr auto" }}>
                      <span className="avatar" aria-hidden="true">
                        {p.initials}
                      </span>
                      <div style={{ minWidth: 0 }}>
                        <Link className="people-row__name" href={`/people/${p.id}`} style={{ textDecoration: "none", color: "inherit", font: "var(--text-h4)" }}>
                          {p.name}
                        </Link>
                        <div className="people-row__role">
                          {p.role} · {org.name}
                        </div>
                      </div>
                      <a
                        className="linkedin"
                        href={p.linkedinUrl ?? `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(`${p.name} ${org.name}`)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        LinkedIn
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted">No people yet. Add one, or run research.</p>
            )}
          </section>

          <section>
            <div className="cluster cluster--between" style={{ marginBottom: "var(--space-6)" }}>
              <h2 className="section__title" style={{ margin: 0 }}>
                Problems
              </h2>
              {!archived && (
                <button type="button" className="btn btn--sm">
                  Link
                </button>
              )}
            </div>
            {org.problems.length ? (
              <div className="entity-list">
                {org.problems.map((p) => (
                  <div key={p.id} className="card lift" style={{ padding: 0 }}>
                    <div className="org-card" style={{ gridTemplateColumns: "2rem auto 1fr auto" }}>
                      <span className="text-subtle" style={{ font: "var(--text-label)", fontVariantNumeric: "tabular-nums" }}>
                        {p.rank}
                      </span>
                      <span className="score" style={{ "--score": p.score } as React.CSSProperties} role="img" aria-label={`Impact score ${p.score} of 100`} data-rank={p.rank}>
                        <span>{p.score}</span>
                      </span>
                      <div style={{ minWidth: 0 }}>
                        <Link className="org-card__name" href={`/problems/${p.id}`} style={{ textDecoration: "none", color: "inherit" }}>
                          {p.title}
                        </Link>
                        <div className="org-card__meta">{p.meta}</div>
                      </div>
                      <div className="avatar-group" aria-label={`Working on it: ${p.organizations.map((o) => o.name).join(", ")}`}>
                        {p.organizations.map((o) => (
                          <span key={o.name} className="avatar avatar--sm" aria-hidden="true" title={o.name}>
                            {o.mark}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted">No problems linked yet.</p>
            )}
          </section>

          <section>
            <h2 className="section__title">Sources</h2>
            {org.sources.length ? (
              org.sources.map((s) => (
                <div key={s.url} className="source">
                  <svg className="icon icon--sm text-subtle" aria-hidden="true" viewBox="0 0 24 24">
                    <path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" />
                  </svg>
                  <div>
                    <a href={s.url} target="_blank" rel="noopener noreferrer">
                      {s.title}
                    </a>
                    <div className="source__host">
                      {s.domain} · {s.note}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-muted">No sources yet. Run research to find some.</p>
            )}
          </section>
        </div>

        <aside className="detail__aside">
          <section>
            <dl className="facts">
              {(
                [
                  ["Type", org.type],
                  ["Founded", org.founded],
                  ["Base", org.base],
                  ["Reach", org.reach],
                ] as const
              ).map(([label, value]) => (
                <div key={label} className="fact">
                  <dt>{label}</dt>
                  <dd>{value || "—"}</dd>
                </div>
              ))}
              <div className="fact">
                <dt>Website</dt>
                <dd>
                  {org.website ? (
                    <a href={org.website.startsWith("http") ? org.website : `https://${org.website}`} target="_blank" rel="noopener noreferrer">
                      {org.website}
                    </a>
                  ) : (
                    "—"
                  )}
                </dd>
              </div>
              <div className="fact">
                <dt>Status</dt>
                <dd>
                  <span className={`verify ${STATUS_CLASS[org.status]}`}>{org.status}</span>
                </dd>
              </div>
            </dl>
          </section>
          <section>
            <h2 className="section__title">Activity</h2>
            <ul className="timeline">
              {org.activity.map((a, i) => (
                <li key={i}>
                  <time>{a.when}</time>
                  <span>{a.text}</span>
                </li>
              ))}
            </ul>
          </section>
        </aside>
      </div>
    </main>
  );
}
