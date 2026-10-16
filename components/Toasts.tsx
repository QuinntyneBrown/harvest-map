"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";

export type ToastInput = {
  kind: "info" | "success" | "warning" | "danger";
  title: string;
  text?: string;
  action?: { label: string; run: () => void };
};

type Toast = ToastInput & { id: number };

/** 8 s by default; the end-to-end tests shorten it so the timer can run in real time. */
const AUTO_DISMISS_MS = Number(process.env.NEXT_PUBLIC_TOAST_MS) || 8000;
const MAX_VISIBLE = 3;

const ToastContext = createContext<(toast: ToastInput) => void>(() => {});

export function useToast() {
  return useContext(ToastContext);
}

const ICONS = {
  info: <path d="M12 8h.01M11 12h1v5h1" />,
  success: <path d="m8 12 3 3 5-6" />,
  warning: <path d="M12 8v5M12 16h.01" />,
  danger: <path d="M12 7v6M12 16h.01" />,
};

/** Toast region: at most three stacked, oldest first; each dismisses after 8 s unless it is a danger toast. */
export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const nextId = useRef(1);

  const show = useCallback((toast: ToastInput) => {
    setToasts((all) => [...all, { ...toast, id: nextId.current++ }].slice(-MAX_VISIBLE));
  }, []);
  const dismiss = useCallback((id: number) => setToasts((all) => all.filter((t) => t.id !== id)), []);

  return (
    <ToastContext.Provider value={show}>
      {children}
      <div className="toast-region" role="status" aria-live="polite">
        {toasts.map((t) => (
          <ToastItem key={t.id} toast={t} onDismiss={() => dismiss(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

function ToastItem({ toast, onDismiss }: { toast: Toast; onDismiss: () => void }) {
  const [paused, setPaused] = useState(false);
  const remaining = useRef(AUTO_DISMISS_MS);
  const startedAt = useRef(0);
  const auto = toast.kind !== "danger";

  useEffect(() => {
    if (!auto || paused) return;
    startedAt.current = Date.now();
    const timer = setTimeout(onDismiss, remaining.current);
    return () => {
      clearTimeout(timer);
      remaining.current -= Date.now() - startedAt.current;
    };
  }, [auto, paused, onDismiss]);

  return (
    <div
      className={`toast toast--${toast.kind}`}
      data-testid="toast"
      role={toast.kind === "danger" ? "alert" : "status"}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
    >
      <svg className="icon" aria-hidden="true" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="9" />
        {ICONS[toast.kind]}
      </svg>
      <div className="toast__body">
        <div className="toast__title">{toast.title}</div>
        {toast.text && <div className="toast__text">{toast.text}</div>}
        {toast.action && (
          <button
            className="toast__action"
            type="button"
            onClick={() => {
              toast.action!.run();
              onDismiss();
            }}
          >
            {toast.action.label}
          </button>
        )}
      </div>
      <button className="close" type="button" aria-label="Dismiss" onClick={onDismiss}>
        <svg className="icon icon--sm" aria-hidden="true" viewBox="0 0 24 24">
          <path d="M6 6l12 12M18 6 6 18" />
        </svg>
      </button>
      {auto && <span className="toast__progress" aria-hidden="true" style={{ animation: `toast-timer ${AUTO_DISMISS_MS}ms linear forwards`, animationPlayState: paused ? "paused" : "running" }}></span>}
    </div>
  );
}
