"use client";

import Link from "next/link";
import { OrganizationForm } from "../OrganizationForm";

export default function NewOrganizationPage() {
  return (
    <main id="main" className="container app-main">
      <nav aria-label="Breadcrumb" style={{ marginBottom: "var(--space-6)" }}>
        <ol className="breadcrumb">
          <li>
            <Link href="/organizations">Organizations</Link>
          </li>
          <li aria-current="page">New</li>
        </ol>
      </nav>
      <div className="page-header rise">
        <div>
          <h1>New organization</h1>
          <p className="subtitle">New organizations start as Unverified until research confirms them.</p>
        </div>
      </div>
      <OrganizationForm
        id={null}
        name="this organization"
        backHref="/organizations"
        initial={{ name: "", type: "Community", founded: "", city: "", country: "", website: "", summary: "", tags: [] }}
      />
    </main>
  );
}
