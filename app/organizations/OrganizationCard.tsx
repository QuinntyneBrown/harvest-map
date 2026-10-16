import Link from "next/link";
import type { OrganizationListItem } from "@/lib/types";

type Props = { org: OrganizationListItem; index: number; selected: boolean; onToggle: () => void };

const STATUS_CLASS = { Verified: "verify--verified", Unverified: "verify--pending", Conflict: "verify--conflict" } as const;

export function OrganizationCard({ org, index, selected, onToggle }: Props) {
  const meta = [org.type, org.city, org.reach].filter(Boolean).join(" · ");
  return (
    <div data-testid="org-card" className="card lift rise" style={{ "--i": index } as React.CSSProperties} aria-selected={selected || undefined}>
      <div className="org-card">
        <label className="row-check">
          <input type="checkbox" aria-label={`Select ${org.name}`} checked={selected} onChange={onToggle} />
        </label>
        <span className="mark" aria-hidden="true">
          {org.mark}
        </span>
        <div style={{ minWidth: 0 }}>
          <Link className="org-card__name" href={`/organizations/${org.id}`} dir="auto" style={{ textDecoration: "none", color: "inherit", overflowWrap: "anywhere" }}>
            {org.name}
          </Link>
          <div className="org-card__meta">{meta}</div>
          <div className="tags">
            {org.tags.map((t) => (
              <span key={t} className={t === "AI" ? "tag tag--ai" : t === "Moonshot" ? "tag tag--moonshot" : "tag"}>
                {t}
              </span>
            ))}
          </div>
        </div>
        <div className="org-card__end">
          <span className={`verify ${STATUS_CLASS[org.status]}`}>{org.status}</span>
        </div>
      </div>
    </div>
  );
}
