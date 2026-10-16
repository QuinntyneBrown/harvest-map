"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { useToast } from "@/components/Toasts";
import { getJson, postJson } from "@/lib/api";
import type { OrganizationList } from "@/lib/types";
import { BulkTagDialog } from "./BulkTagDialog";
import { OrganizationCard } from "./OrganizationCard";

const CHIPS = [
  ["ai", "AI"],
  ["youth", "Youth"],
  ["moonshot", "Moonshot"],
  ["verified", "Verified"],
] as const;

export default function OrganizationsPage() {
  const [list, setList] = useState<OrganizationList | null>(null);
  const [failed, setFailed] = useState(false);
  const [text, setText] = useState("");
  const [q, setQ] = useState("");
  const [chips, setChips] = useState<string[]>([]);
  const [sort, setSort] = useState("impact");
  const [selected, setSelected] = useState<string[]>([]);
  const [tagging, setTagging] = useState(false);
  const toast = useToast();

  useEffect(() => {
    const timer = setTimeout(() => setQ(text), 150);
    return () => clearTimeout(timer);
  }, [text]);

  const load = useCallback(() => {
    setFailed(false);
    const params = new URLSearchParams({ q, sort });
    if (chips.length) params.set("chips", chips.join(","));
    getJson<OrganizationList>(`/api/organizations?${params}`).then(setList, () => setFailed(true));
  }, [q, chips, sort]);

  useEffect(load, [load]);
  const loadRef = useRef(load);
  loadRef.current = load;

  const none = list && list.total === 0;

  function clear() {
    setText("");
    setQ("");
    setChips([]);
  }

  async function archive() {
    const ids = selected;
    const names = list!.items.filter((o) => ids.includes(o.id)).map((o) => o.name);
    try {
      await postJson("/api/organizations/bulk/archive", { ids });
      setSelected([]);
      loadRef.current();
      toast({
        kind: "success",
        title: names.length === 1 ? `${names[0]} archived` : `${names.length} organizations archived`,
        text: "Hidden from lists and the map.",
        action: {
          label: "Undo",
          run: () => postJson("/api/organizations/bulk/restore", { ids }).then(() => loadRef.current(), () => toast({ kind: "danger", title: "Couldn't restore", text: "Try again." })),
        },
      });
    } catch {
      toast({ kind: "danger", title: "Couldn't archive", text: "Try again." });
    }
  }

  async function applyTag(tag: string, mode: "add" | "remove") {
    const ids = selected;
    await postJson("/api/organizations/bulk/tag", { ids, tag, mode });
    setTagging(false);
    loadRef.current();
    const noun = ids.length === 1 ? "organization" : "organizations";
    toast({ kind: "success", title: mode === "add" ? `${tag} added to ${ids.length} ${noun}` : `${tag} removed from ${ids.length} ${noun}` });
  }

  function toggle(id: string) {
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));
  }

  return (
    <main id="main" className="container app-main">
      <div className="page-header rise">
        <div>
          <h1>Organizations</h1>
          {list ? (
            <p className="subtitle">
              {none ? "Nothing tracked yet" : `${list.total} tracked · ${list.verified} verified · ${list.unverified} unverified`}
            </p>
          ) : (
            !failed && <span className="skeleton skeleton--text" style={{ width: "16rem" }}></span>
          )}
        </div>
        <div className="cluster">
          <button type="button" className="btn btn--ghost">
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M12 16V4m0 0-4 4m4-4 4 4M4 20h16" />
            </svg>
            Import
          </button>
          <button type="button" className="btn btn--ghost">
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M12 4v12m0 0-4-4m4 4 4-4M4 20h16" />
            </svg>
            Export
          </button>
          <Link className="btn btn--primary" href="/organizations/new">
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <path d="M12 5v14M5 12h14" />
            </svg>
            New
          </Link>
        </div>
      </div>

      {!none && !failed && (
        <div className="toolbar rise" style={{ "--i": 1 } as React.CSSProperties}>
          <form className="search" role="search" style={{ flex: "1 1 16rem", maxWidth: "24rem" }} onSubmit={(e) => e.preventDefault()}>
            <label className="visually-hidden" htmlFor="q">
              Search organisations
            </label>
            <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-3.5-3.5" />
            </svg>
            <input className="input" id="q" type="search" value={text} placeholder="Search" onChange={(e) => setText(e.target.value)} />
          </form>
          <div className="cluster">
            {CHIPS.map(([id, label]) => (
              <button
                key={id}
                className="chip"
                type="button"
                aria-pressed={chips.includes(id)}
                onClick={() => setChips((c) => (c.includes(id) ? c.filter((x) => x !== id) : [...c, id]))}
              >
                {label}
              </button>
            ))}
            <label className="field" style={{ flexDirection: "row", alignItems: "center", gap: "var(--space-2)" }}>
              <span className="field__label">Sort</span>
              <select className="select input--sm" style={{ width: "auto" }} aria-label="Sort organisations" value={sort} onChange={(e) => setSort(e.target.value)}>
                <option value="impact">Impact</option>
                <option value="name">Name</option>
                <option value="updated">Updated</option>
              </select>
            </label>
          </div>
        </div>
      )}

      {failed ? (
        <div className="empty empty--error">
          <h2 className="empty__title">Couldn&apos;t load organizations</h2>
          <p className="empty__text">The request timed out. Try again, or share reference HM-4F2A with support.</p>
          <div className="empty__actions">
            <button type="button" className="btn btn--primary" onClick={load}>
              Retry
            </button>
          </div>
        </div>
      ) : !list ? (
        <div className="entity-list" aria-busy="true" aria-label="Loading organizations">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="card">
              <span className="skeleton skeleton--title"></span>
              <span className="skeleton skeleton--text" style={{ width: "12rem" }}></span>
            </div>
          ))}
        </div>
      ) : none ? (
        <div className="empty rise">
          <h2 className="empty__title">No organisations yet</h2>
          <p className="empty__text">Add the first one by hand, import a CSV, or let a research run find them.</p>
          <div className="empty__actions">
            <Link className="btn" href="/organizations/new">
              Add by hand
            </Link>
          </div>
        </div>
      ) : list.items.length === 0 ? (
        <div className="empty empty--compact rise">
          <h2 className="empty__title">Nothing matches</h2>
          <p className="empty__text">{q ? <>No organisation matches “{q}” with these filters.</> : "No organisation matches these filters."}</p>
          <div className="empty__actions">
            <button type="button" className="btn" onClick={clear}>
              Clear filters
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="entity-list">
            {list.items.map((o, i) => (
              <OrganizationCard key={o.id} org={o} index={i} selected={selected.includes(o.id)} onToggle={() => toggle(o.id)} />
            ))}
          </div>
          {selected.length > 0 && (
            <div className="select-bar" role="region" aria-label={`${selected.length} organisations selected`}>
              <strong>{selected.length} selected</strong>
              <span className="topbar__spacer"></span>
              <button type="button" className="btn btn--sm" onClick={() => setTagging(true)}>
                Tag
              </button>
              <button type="button" className="btn btn--sm">
                Export {selected.length}
              </button>
              <button type="button" className="btn btn--sm" onClick={archive}>
                Archive
              </button>
            </div>
          )}
        </>
      )}
      {tagging && <BulkTagDialog count={selected.length} onApply={applyTag} onClose={() => setTagging(false)} />}
    </main>
  );
}
