"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { getJson } from "@/lib/api";
import type { OrganizationDetail } from "@/lib/types";
import { OrganizationForm } from "../../OrganizationForm";

export default function EditOrganizationPage() {
  const { id } = useParams<{ id: string }>();
  const [org, setOrg] = useState<OrganizationDetail | null>(null);
  const [failed, setFailed] = useState(false);

  const load = useCallback(() => {
    setFailed(false);
    setOrg(null);
    getJson<OrganizationDetail>(`/api/organizations/${id}`).then(setOrg, () => setFailed(true));
  }, [id]);

  useEffect(load, [load]);

  return (
    <main id="main" className="container app-main">
      <nav aria-label="Breadcrumb" style={{ marginBottom: "var(--space-6)" }}>
        <ol className="breadcrumb">
          <li>
            <Link href="/organizations">Organizations</Link>
          </li>
          <li>{org ? <Link href={`/organizations/${id}`}>{org.name}</Link> : "…"}</li>
          <li aria-current="page">Edit</li>
        </ol>
      </nav>
      <div className="page-header rise">
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1>Edit organization</h1>
          {org ? (
            <p className="subtitle">
              {org.name}
              {org.lastSaved ? ` · last saved ${org.lastSaved.at} by ${org.lastSaved.by}` : ""}
            </p>
          ) : (
            !failed && <span className="skeleton skeleton--text" style={{ width: "min(18rem, 80%)", marginTop: "var(--space-4)" }}></span>
          )}
        </div>
      </div>
      {failed ? (
        <div className="empty empty--error rise">
          <h2 className="empty__title">Couldn&apos;t load the form</h2>
          <p className="empty__text">The request timed out. Try again, or share reference HM-4F2A with support.</p>
          <div className="empty__actions">
            <button type="button" className="btn btn--primary" onClick={load}>
              Try again
            </button>
            <Link className="btn btn--ghost" href={`/organizations/${id}`}>
              Go back
            </Link>
          </div>
        </div>
      ) : !org ? (
        <div className="card" style={{ maxWidth: "44rem" }} aria-busy="true" aria-label="Loading form">
          {[0, 1, 2, 3, 4].map((i) => (
            <span key={i} className="skeleton skeleton--rect" style={{ height: "2.5rem", marginTop: "var(--space-4)" }}></span>
          ))}
        </div>
      ) : (
        <OrganizationForm
          id={org.id}
          name={org.name}
          backHref={`/organizations/${org.id}`}
          initial={{
            name: org.name,
            type: org.type,
            founded: org.founded,
            city: org.city,
            country: org.country,
            website: org.website,
            summary: org.summary,
            tags: org.tags,
          }}
        />
      )}
    </main>
  );
}
