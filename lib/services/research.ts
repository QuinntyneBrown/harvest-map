import { and, count, desc, eq, gt, inArray, or } from "drizzle-orm";
import { CURRENT_USER_ID, db } from "@/lib/db";
import { findings, organizations, researchRuns, sources, userSettings, users } from "@/lib/db/schema";
import { CORE_QUESTIONS } from "@/lib/questions";
import { executeRun } from "@/lib/research/executor";
import type { FindingView, ResearchOverview, RunRow, RunStatus } from "@/lib/types";

export const LOOK_FOR = ["orgs", "people", "linkedin"] as const;
export const DEPTHS = ["quick", "standard", "deep"] as const;
const UNDO_WINDOW_MS = 30_000;

export type StartRunInput = {
  question: number | null;
  customQuestion: string | null;
  lookFor: (typeof LOOK_FOR)[number][];
  depth: (typeof DEPTHS)[number];
};

export class InputError extends Error {}

export async function startRun(input: StartRunInput, userId = CURRENT_USER_ID) {
  const custom = input.customQuestion?.trim();
  const title = input.question ? CORE_QUESTIONS[input.question - 1] : custom;
  if (!title) throw new InputError("Write the question you want answered");
  if (!input.lookFor.length) throw new InputError("Choose what to look for");
  const [run] = await db
    .insert(researchRuns)
    .values({ title, question: input.question, customQuestion: custom || null, lookFor: input.lookFor, depth: input.depth, startedBy: userId })
    .returning();
  void executeRun(run.id);
  return run.id;
}

export async function getDefaultDepth(userId = CURRENT_USER_ID) {
  const [s] = await db.select().from(userSettings).where(eq(userSettings.userId, userId));
  return s?.defaultDepth ?? "standard";
}

function startedLabel(at: Date, now = new Date()) {
  const day = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
  const diffDays = Math.round((day(now) - day(at)) / 86_400_000);
  if (diffDays === 0) return at.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
  if (diffDays === 1) return "Yesterday";
  return at.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }).replace(",", "");
}

export async function toFindingViews(rows: (typeof findings.$inferSelect)[]): Promise<FindingView[]> {
  if (!rows.length) return [];
  const srcs = await db.select().from(sources).where(inArray(sources.findingId, rows.map((r) => r.id)));
  const names = new Map((await db.select().from(users)).map((u) => [u.id, u.name]));
  return rows.map((f) => {
    const own = srcs.filter((s) => s.findingId === f.id);
    return {
      id: f.id,
      runId: f.runId,
      statement: f.statement,
      subjectKind: f.subjectKind as FindingView["subjectKind"],
      subject: f.subjectName,
      organization: f.organizationName,
      sourceDomain: own[0]?.domain ?? "",
      confidence: f.confidence,
      lowConfidenceReason: f.lowConfidenceReason,
      state: f.state as FindingView["state"],
      decidedBy: f.decidedBy ? (names.get(f.decidedBy) ?? f.decidedBy) : null,
      decidedAt: f.decidedAt?.toISOString() ?? null,
      fields: f.change,
      sources: own.map((s) => ({ title: s.title, domain: s.domain, url: s.url, date: s.date })),
    };
  });
}

export async function getOverview(userId = CURRENT_USER_ID): Promise<ResearchOverview> {
  const runs = await db.select().from(researchRuns).orderBy(desc(researchRuns.id)).limit(20);
  const [{ total }] = await db.select({ total: count() }).from(researchRuns);
  const [{ running }] = await db
    .select({ running: count() })
    .from(researchRuns)
    .where(inArray(researchRuns.status, ["Queued", "Running"]));
  const [{ pending }] = await db.select({ pending: count() }).from(findings).where(eq(findings.state, "Pending"));
  const findingCounts = runs.length
    ? await db
        .select({ runId: findings.runId, n: count() })
        .from(findings)
        .where(inArray(findings.runId, runs.map((r) => r.id)))
        .groupBy(findings.runId)
    : [];
  const recent = await db
    .select()
    .from(findings)
    .where(or(eq(findings.state, "Pending"), and(gt(findings.decidedAt, new Date(Date.now() - UNDO_WINDOW_MS)))))
    .orderBy(desc(findings.createdAt))
    .limit(50);
  const names = new Map((await db.select().from(users)).map((u) => [u.id, u.name]));

  const rows: RunRow[] = runs.map((r) => ({
    id: r.id,
    title: r.title,
    startedLabel: startedLabel(r.startedAt),
    person: names.get(r.startedBy) ?? r.startedBy,
    findingCount: findingCounts.find((c) => c.runId === r.id)?.n ?? 0,
    status: r.status as RunStatus,
    failureReason: r.failureReason,
  }));

  return {
    currentUser: names.get(userId) ?? userId,
    totalRuns: total,
    running,
    findingsToReview: pending,
    runs: rows,
    findings: await toFindingViews(recent),
    organizations: (await db.select({ name: organizations.name }).from(organizations).orderBy(organizations.name)).map((o) => o.name),
  };
}
