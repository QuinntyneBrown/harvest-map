"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  ["Field", "/"],
  ["Orgs", "/organizations"],
  ["People", "/people"],
  ["Problems", "/problems"],
  ["Questions", "/questions"],
  ["Research", "/research"],
  ["Map", "/map"],
] as const;

export function TopBar() {
  const pathname = usePathname();
  return (
    <header className="topbar">
      <span className="topbar__shadow" aria-hidden="true"></span>
      <button type="button" className="btn btn--ghost btn--icon topbar__menu" aria-label="Open navigation">
        <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
      </button>
      <Link className="topbar__brand" href="/">
        <svg className="icon icon--lg" aria-hidden="true" viewBox="0 0 24 24">
          <path d="M12 22V10M12 10c-3 0-5-2-5-5 3 0 5 2 5 5zM12 10c3 0 5-2 5-5-3 0-5 2-5 5zM12 15c-3 0-5-2-5-5 3 0 5 2 5 5zM12 15c3 0 5-2 5-5-3 0-5 2-5 5zM12 20c-3 0-5-2-5-5 3 0 5 2 5 5zM12 20c3 0 5-2 5-5-3 0-5 2-5 5z" />
        </svg>
        <span>Harvest Map</span>
      </Link>
      <nav className="topbar__nav" aria-label="Primary">
        {NAV.map(([label, href]) => (
          <Link key={href} className="nav-link" href={href} aria-current={pathname === href ? "page" : undefined}>
            {label}
          </Link>
        ))}
      </nav>
      <span className="topbar__spacer"></span>
      <span className="avatar avatar--sm" aria-label="Naomi Achterberg" role="img">
        NA
      </span>
    </header>
  );
}
