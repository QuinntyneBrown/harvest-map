import { and, eq, ilike } from "drizzle-orm";
import { CURRENT_USER_ID, db } from "@/lib/db";
import { activityEntries, findings, organizations, people, users, type AppliedChange } from "@/lib/db/schema";
import { toFindingViews } from "./research";

const UNDO_WINDOW_MS = 30_000;

export class DecisionError extends Error {}

type Tx = Parameters<Parameters<typeof db.transaction>[0]>[0];

async function load(tx: Tx, id: string) {
  const [f] = await tx.select().from(findings).where(eq(findings.id, id)).for("update");
  if (!f) throw new DecisionError("This finding no longer exists.");
  return f;
}

async function view(id: string) {
  const [f] = await db.select().from(findings).where(eq(findings.id, id));
  return (await toFindingViews([f]))[0];
}

async function findOrCreateOrganization(tx: Tx, name: string) {
  const [org] = await tx.select().from(organizations).where(ilike(organizations.name, name));
  if (org) return { id: org.id, created: false };
  const [created] = await tx.insert(organizations).values({ name }).returning();
  return { id: created.id, created: true };
}

/** Applies the change to the subject record, creating or updating it, and records the activity. */
export async function accept(id: string, fields: Record<string, string>, userId = CURRENT_USER_ID) {
  await db.transaction(async (tx) => {
    const f = await load(tx, id);
    if (f.state !== "Pending") throw new DecisionError("This finding was already decided.");
    let applied: AppliedChange;

    if (f.subjectKind === "Person") {
      if (!fields.role?.trim()) throw new DecisionError("Enter a role");
      const org = fields.organization?.trim() ? await findOrCreateOrganization(tx, fields.organization.trim()) : null;
      const values = {
        role: fields.role.trim(),
        since: fields.since?.trim() ?? "",
        organizationId: org?.id ?? null,
        ...(fields.linkedinUrl ? { linkedinUrl: fields.linkedinUrl } : {}),
      };
      const [existing] = await tx.select().from(people).where(ilike(people.name, f.subjectName));
      if (existing) {
        await tx.update(people).set(values).where(eq(people.id, existing.id));
        applied = {
          subjectId: existing.id,
          createdSubject: false,
          createdOrganizationId: org?.created ? org.id : null,
          previous: { role: existing.role, since: existing.since, organizationId: existing.organizationId, linkedinUrl: existing.linkedinUrl },
        };
      } else {
        const [created] = await tx.insert(people).values({ name: f.subjectName, ...values }).returning();
        applied = { subjectId: created.id, createdSubject: true, createdOrganizationId: org?.created ? org.id : null, previous: {} };
      }
    } else {
      if (!fields.name?.trim()) throw new DecisionError("Enter a name");
      const values = { name: fields.name.trim(), location: fields.location?.trim() ?? "", summary: fields.summary?.trim() ?? "" };
      const [existing] = await tx.select().from(organizations).where(ilike(organizations.name, f.subjectName));
      if (existing) {
        await tx.update(organizations).set(values).where(eq(organizations.id, existing.id));
        applied = {
          subjectId: existing.id,
          createdSubject: false,
          createdOrganizationId: null,
          previous: { name: existing.name, location: existing.location, summary: existing.summary },
        };
      } else {
        const [created] = await tx.insert(organizations).values(values).returning();
        applied = { subjectId: created.id, createdSubject: true, createdOrganizationId: null, previous: {} };
      }
    }

    await tx
      .update(findings)
      .set({ state: "Accepted", change: fields, applied, decidedBy: userId, decidedAt: new Date() })
      .where(eq(findings.id, id));
    const [user] = await tx.select().from(users).where(eq(users.id, userId));
    await tx.insert(activityEntries).values({
      actorId: userId,
      runId: f.runId,
      findingId: id,
      text: `${user?.name ?? userId} accepted finding from run #${f.runId}`,
    });
  });
  return view(id);
}

/** Rejects the finding; its sources are kept and no record changes. */
export async function reject(id: string, userId = CURRENT_USER_ID) {
  await db.transaction(async (tx) => {
    const f = await load(tx, id);
    if (f.state !== "Pending") throw new DecisionError("This finding was already decided.");
    await tx.update(findings).set({ state: "Rejected", decidedBy: userId, decidedAt: new Date() }).where(eq(findings.id, id));
  });
  return view(id);
}

/** Reverses an Accept or Reject within the undo window and returns the finding to Pending. */
export async function undo(id: string, userId = CURRENT_USER_ID) {
  await db.transaction(async (tx) => {
    const f = await load(tx, id);
    if (f.state === "Pending") return;
    if (!f.decidedAt || Date.now() - f.decidedAt.getTime() > UNDO_WINDOW_MS) throw new DecisionError("Undo is no longer available.");
    if (f.decidedBy !== userId) throw new DecisionError("Only the person who decided can undo.");

    const a = f.applied;
    if (f.state === "Accepted" && a) {
      const table = f.subjectKind === "Person" ? people : organizations;
      if (a.createdSubject) await tx.delete(table).where(eq(table.id, a.subjectId));
      else if (f.subjectKind === "Person") {
        const p = a.previous;
        await tx
          .update(people)
          .set({ role: p.role ?? "", since: p.since ?? "", organizationId: p.organizationId, linkedinUrl: p.linkedinUrl })
          .where(eq(people.id, a.subjectId));
      } else {
        const p = a.previous;
        await tx
          .update(organizations)
          .set({ name: p.name ?? f.subjectName, location: p.location ?? "", summary: p.summary ?? "" })
          .where(eq(organizations.id, a.subjectId));
      }
      if (a.createdOrganizationId) await tx.delete(organizations).where(eq(organizations.id, a.createdOrganizationId));
      await tx.delete(activityEntries).where(and(eq(activityEntries.findingId, id), eq(activityEntries.actorId, userId)));
    }
    await tx.update(findings).set({ state: "Pending", applied: null, decidedBy: null, decidedAt: null }).where(eq(findings.id, id));
  });
  return view(id);
}
