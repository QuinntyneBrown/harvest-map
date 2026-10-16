import { boolean, integer, jsonb, pgTable, primaryKey, serial, text, timestamp, uuid } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
});

export const userSettings = pgTable("user_settings", {
  userId: text("user_id").primaryKey().references(() => users.id),
  defaultDepth: text("default_depth").notNull().default("standard"),
});

export const organizations = pgTable("organizations", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  location: text("location").notNull().default(""),
  summary: text("summary").notNull().default(""),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const people = pgTable("people", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  role: text("role").notNull().default(""),
  since: text("since").notNull().default(""),
  organizationId: uuid("organization_id").references(() => organizations.id, { onDelete: "set null" }),
  linkedinUrl: text("linkedin_url"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

/** score is the impact score, reach × severity × tractability, normalised to 0–100. */
export const problems = pgTable("problems", {
  id: uuid("id").primaryKey().defaultRandom(),
  title: text("title").notNull(),
  score: integer("score").notNull(),
  moonshot: boolean("moonshot").notNull().default(false),
});

export const organizationProblems = pgTable(
  "organization_problems",
  {
    organizationId: uuid("organization_id").notNull().references(() => organizations.id, { onDelete: "cascade" }),
    problemId: uuid("problem_id").notNull().references(() => problems.id, { onDelete: "cascade" }),
  },
  (t) => [primaryKey({ columns: [t.organizationId, t.problemId] })],
);

export const researchRuns = pgTable("research_runs", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  question: integer("question"),
  customQuestion: text("custom_question"),
  lookFor: text("look_for").array().notNull(),
  depth: text("depth").notNull(),
  status: text("status").notNull().default("Queued"),
  failureReason: text("failure_reason"),
  startedBy: text("started_by").notNull().references(() => users.id),
  startedAt: timestamp("started_at", { withTimezone: true }).notNull().defaultNow(),
  finishedAt: timestamp("finished_at", { withTimezone: true }),
});

export const findings = pgTable("findings", {
  id: uuid("id").primaryKey().defaultRandom(),
  runId: integer("run_id").notNull().references(() => researchRuns.id, { onDelete: "cascade" }),
  statement: text("statement").notNull(),
  subjectKind: text("subject_kind").notNull(),
  subjectName: text("subject_name").notNull(),
  organizationName: text("organization_name"),
  confidence: integer("confidence").notNull(),
  lowConfidenceReason: text("low_confidence_reason"),
  change: jsonb("change").$type<Record<string, string>>().notNull(),
  /** What accept changed, so undo can reverse it. */
  applied: jsonb("applied").$type<AppliedChange>(),
  state: text("state").notNull().default("Pending"),
  decidedBy: text("decided_by").references(() => users.id),
  decidedAt: timestamp("decided_at", { withTimezone: true }),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export type AppliedChange = {
  subjectId: string;
  createdSubject: boolean;
  createdOrganizationId: string | null;
  previous: Record<string, string | null>;
};

export const sources = pgTable("sources", {
  id: uuid("id").primaryKey().defaultRandom(),
  findingId: uuid("finding_id").notNull().references(() => findings.id, { onDelete: "cascade" }),
  title: text("title").notNull(),
  domain: text("domain").notNull(),
  url: text("url").notNull(),
  date: text("date").notNull().default(""),
});

export const activityEntries = pgTable("activity_entries", {
  id: uuid("id").primaryKey().defaultRandom(),
  at: timestamp("at", { withTimezone: true }).notNull().defaultNow(),
  actorId: text("actor_id").notNull().references(() => users.id),
  runId: integer("run_id").notNull().references(() => researchRuns.id, { onDelete: "cascade" }),
  findingId: uuid("finding_id").notNull().references(() => findings.id, { onDelete: "cascade" }),
  text: text("text").notNull(),
});
