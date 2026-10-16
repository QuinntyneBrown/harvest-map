"use client";

import { Modal } from "./Modal";

type Props = { name: string; changed: string[]; onDiscard: () => void; onKeep: () => void };

/** "Discard changes to {name}?" with the changed fields; Keep editing is the default action. */
export function UnsavedChangesDialog({ name, changed, onDiscard, onKeep }: Props) {
  return (
    <Modal
      title={`Discard changes to ${name}?`}
      description={`${changed.length} ${changed.length === 1 ? "field" : "fields"} changed: ${changed.join(", ")}.`}
      size="sm"
      danger
      onClose={onKeep}
      footer={
        <>
          <button className="btn btn--danger" type="button" onClick={onDiscard}>
            Discard
          </button>
          <button className="btn btn--primary" type="button" onClick={onKeep} autoFocus>
            Keep editing
          </button>
        </>
      }
    />
  );
}
