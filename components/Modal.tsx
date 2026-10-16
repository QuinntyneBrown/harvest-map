"use client";

import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";

type Props = {
  title: string;
  description?: string;
  onClose: () => void;
  footer?: React.ReactNode;
  children?: React.ReactNode;
  /** While busy, Escape and the backdrop do not close the dialog. */
  busy?: boolean;
  size?: "sm" | "lg";
  /** Shows the danger icon in the header, for destructive confirmations. */
  danger?: boolean;
  /** "left" renders a navigation drawer instead of a dialog panel. */
  placement?: "center" | "left";
};

const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/** Modal dialog in the markup of the mocks, portalled to <body>: backdrop, panel, Escape and Close, Tab kept inside, page behind made inert. */
export function Modal({ title, description, onClose, footer, children, busy = false, size = "lg", danger = false, placement = "center" }: Props) {
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;
  const busyRef = useRef(busy);
  busyRef.current = busy;
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const opener = document.activeElement as HTMLElement | null;
    const main = document.getElementById("main");
    main?.setAttribute("inert", "");
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !busyRef.current) {
        e.stopPropagation();
        onCloseRef.current();
      }
      if (e.key === "Tab" && dialogRef.current) {
        const items = [...dialogRef.current.querySelectorAll<HTMLElement>(FOCUSABLE)].filter((el) => el.offsetParent !== null);
        if (!items.length) return;
        const first = items[0];
        const last = items[items.length - 1];
        const active = document.activeElement;
        if (!dialogRef.current.contains(active)) {
          e.preventDefault();
          first.focus();
        } else if (e.shiftKey && active === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && active === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener("keydown", onKey, true);
    return () => {
      document.removeEventListener("keydown", onKey, true);
      main?.removeAttribute("inert");
      opener?.focus();
    };
  }, []);

  if (placement === "left") {
    return createPortal(
      <>
        <div className="backdrop" onClick={onClose}></div>
        <div ref={dialogRef} className="drawer drawer--left nav-sheet" role="dialog" aria-modal="true" aria-labelledby="dlg-title">
          <div className="drawer__header">
            <h2 className="drawer__title" id="dlg-title">
              {title}
            </h2>
            <button className="btn btn--ghost btn--icon" type="button" aria-label="Close" onClick={onClose}>
              <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
                <path d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>
          {children}
        </div>
      </>,
      document.body,
    );
  }

  return createPortal(
    <>
      <div className="backdrop" onClick={() => !busy && onClose()}></div>
      <div ref={dialogRef} className="dialog" role="dialog" aria-modal="true" aria-labelledby="dlg-title" aria-describedby={description ? "dlg-desc" : undefined}>
        <div className={size === "sm" ? "dialog__panel" : "dialog__panel dialog__panel--lg"} style={{ overflow: "hidden" }}>
          <div className="dialog__header">
            {danger && (
              <div className="dialog__icon dialog__icon--danger" aria-hidden="true">
                <svg className="icon" viewBox="0 0 24 24">
                  <path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
                </svg>
              </div>
            )}
            <div style={{ flex: 1 }}>
              <h2 className="dialog__title" id="dlg-title">
                {title}
              </h2>
              {description && (
                <p className="text-muted" id="dlg-desc" style={{ marginTop: "var(--space-1)" }}>
                  {description}
                </p>
              )}
            </div>
            <button className="btn btn--ghost btn--icon" type="button" aria-label="Close" onClick={onClose} disabled={busy}>
              <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
                <path d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>
          <div className="dialog__body stack" style={{ gap: "var(--space-5)", overflowY: "auto", minHeight: 0 }}>
            {children}
          </div>
          <div className="dialog__footer">{footer}</div>
        </div>
      </div>
    </>,
    document.body,
  );
}
