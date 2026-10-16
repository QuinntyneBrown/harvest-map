"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Modal } from "./Modal";

export const NAV_LINKS = [
  ["Field", "/"],
  ["Organizations", "/organizations"],
  ["People", "/people"],
  ["Problems", "/problems"],
  ["Questions", "/questions"],
  ["Research", "/research"],
  ["Map", "/map"],
] as const;

/** Navigation sheet for viewports below 768 px: the same links as the header, plus the Account group. */
export function NavSheet({ userName, onClose }: { userName: string; onClose: () => void }) {
  const pathname = usePathname();
  const link = (label: string, href: string) => (
    <Link key={href} className="nav-link" href={href} aria-current={pathname === href ? "page" : undefined} onClick={onClose}>
      {label}
    </Link>
  );
  return (
    <Modal title="Harvest Map" placement="left" onClose={onClose}>
      <nav className="drawer__body stack" aria-label="Primary" style={{ gap: "var(--space-1)" }}>
        {NAV_LINKS.map(([label, href]) => link(label, href))}
        <div className="sidebar__group">Account</div>
        {link("Settings", "/settings")}
        {link("Notifications", "/notifications")}
        <p className="text-muted" style={{ marginTop: "var(--space-4)" }}>
          {userName}
        </p>
      </nav>
    </Modal>
  );
}
