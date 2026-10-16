"use client";

import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";

type Props = {
  title: string;
  description?: string;
  onClose: () => void;
  footer: React.ReactNode;
  children: React.ReactNode;
};

/** Modal dialog in the markup of the mocks, portalled to <body>: backdrop, panel, Escape and Close, page behind made inert. */
export function Modal({ title, description, onClose, footer, children }: Props) {
  const onCloseRef = useRef(onClose);
  onCloseRef.current = onClose;

  useEffect(() => {
    const opener = document.activeElement as HTMLElement | null;
    const main = document.getElementById("main");
    main?.setAttribute("inert", "");
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onCloseRef.current();
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      main?.removeAttribute("inert");
      opener?.focus();
    };
  }, []);

  return createPortal(
    <>
      <div className="backdrop" onClick={onClose}></div>
      <div className="dialog" role="dialog" aria-modal="true" aria-labelledby="dlg-title" aria-describedby={description ? "dlg-desc" : undefined}>
        <div className="dialog__panel dialog__panel--lg" style={{ overflow: "hidden" }}>
          <div className="dialog__header">
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
            <button className="btn btn--ghost btn--icon" type="button" aria-label="Close" onClick={onClose}>
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
