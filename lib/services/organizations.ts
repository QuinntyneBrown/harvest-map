import { and, desc, eq, inArray, isNull, ne, sql } from "drizzle-orm";
import { db } from "@/lib/db";
import { activityEntries, findings, initiatives, notifications, organizationProblems, organizations, people, problems, sources, users } from "@/lib/db/schema";
import { dayLabel, initials, whenLabel } from "@/lib/format";
import { ORG_TAGS, type OrganizationInput, validateOrganization } from "@/lib/validation/organization";
import type { OrganizationDetail, OrganizationList, OrganizationListItem, OrgStatus } from "@/lib/types";

export const SORTS = ["impact", "name", "updated"] as const;
export const CHIPS = ["ai", "youth", "moonshot", "verified"] as const;

export type OrganizationQuery = { q: string; chips: (typeof CHIPS)[number][]; sort: (typeof SORTS)[number] };

const toItem = (o: typeof organizations.$inferSelect): OrganizationListItem => ({
  id: o.id,
  name: o.name,
  mark: o.mark,
  type: o.type,
  city: o.city,
  reach: o.reach,
  tags: o.tags,
  status: o.verificationStatus as OrgStatus,
});

/** Organizations that are not archived, filtered, searched and sorted; counts ignore the filters. */
export async function list(query: OrganizationQuery): Promise<OrganizationList> {
  const rows = await db.select().from(organizations).where(isNull(organizations.archivedAt)).orderBy(desc(organizations.updatedAt));
  const links = await db
    .select({ organizationId: organizationProblems.organizationId, score: problems.score })
    .from(organizationProblems)
    .innerJoin(problems, eq(organizationProblems.problemId, problems.id));
  const impact = (id: string) => Math.max(-1, ...links.filter((l) => l.organizationId === id).map((l) => l.score));

  const tagChips = query.chips.filter((c) => c !== "verified");
  const needle = query.q.trim().toLowerCase();
  const matches = rows.filter(
    (o) =>
      tagChips.every((c) => o.tags.some((t) => t.toLowerCase() === c)) &&
      (!query.chips.includes("verified") || o.verificationStatus === "Verified") &&
      (!needle || o.name.toLowerCase().includes(needle)),
  );
  if (query.sort === "name") matches.sort((a, b) => a.name.localeCompare(b.name));
  else if (query.sort === "impact") matches.sort((a, b) => impact(b.id) - impact(a.id) || a.name.localeCompare(b.name));

  const verified = rows.filter((o) => o.verificationStatus === "Verified").length;
  return { total: rows.length, verified, unverified: rows.length - verified, items: matches.map(toItem) };
}

export class NotFoundError extends Error {}
export class ArchivedError extends Error {}

/** Every mutating organization action calls this first: archived records are read-only. */
export async function assertEditable(id: string) {
  const [o] = await db.select({ archivedAt: organizations.archivedAt }).from(organizations).where(eq(organizations.id, id));
  if (!o) throw new NotFoundError("This organization no longer exists.");
  if (o.archivedAt) throw new ArchivedError("This organization is archived. Restore it to make changes.");
}

export async function get(id: string): Promise<OrganizationDetail> {
  const [o] = await db.select().from(organizations).where(eq(organizations.id, id));
  if (!o) throw new NotFoundError("This organization no longer exists.");
  const names = new Map((await db.select().from(users)).map((u) => [u.id, u.name]));

  const staff = await db.select().from(people).where(eq(people.organizationId, id)).orderBy(people.name);
  const ranked = await db.select().from(problems).orderBy(desc(problems.score), problems.title);
  const links = await db.select().from(organizationProblems);
  const orgRows = await db.select().from(organizations);
  const markOf = new Map(orgRows.map((r) => [r.id, { name: r.name, mark: r.mark ?? initials(r.name) }]));
  const mine = new Set(links.filter((l) => l.organizationId === id).map((l) => l.problemId));

  const own = await db.select().from(sources).where(and(eq(sources.subjectKind, "Organization"), eq(sources.subjectId, id)));
  const accepted = await db
    .select({ s: sources, decidedAt: findings.decidedAt })
    .from(sources)
    .innerJoin(findings, eq(sources.findingId, findings.id))
    .where(and(eq(findings.state, "Accepted"), sql`lower(${findings.subjectName}) = lower(${o.name})`));
  const sourceRows = [
    ...own.map((s) => ({ s, verifiedAt: s.verifiedAt })),
    ...accepted.map((a) => ({ s: a.s, verifiedAt: a.decidedAt })),
  ];

  const log = await db
    .select()
    .from(activityEntries)
    .where(and(eq(activityEntries.subjectKind, "Organization"), eq(activityEntries.subjectId, id)))
    .orderBy(desc(activityEntries.at))
    .limit(10);
  const inits = await db.select().from(initiatives).where(eq(initiatives.organizationId, id)).orderBy(initiatives.createdAt);

  return {
    id: o.id,
    name: o.name,
    mark: o.mark,
    status: o.verificationStatus as OrgStatus,
    summary: o.summary,
    tags: o.tags,
    type: o.type,
    founded: o.founded,
    base: [o.city, o.country].filter(Boolean).join(", "),
    city: o.city,
    country: o.country,
    lastSaved: o.updatedBy ? { at: dayLabel(o.updatedAt), by: names.get(o.updatedBy) ?? o.updatedBy } : null,
    reach: o.reach,
    website: o.website,
    archived: o.archivedAt ? { by: names.get(o.archivedBy ?? "") ?? "Someone", at: dayLabel(o.archivedAt) } : null,
    initiatives: inits.map((i) => i.text),
    people: staff.map((p) => ({ id: p.id, name: p.name, initials: initials(p.name), role: p.role, linkedinUrl: p.linkedinUrl })),
    problems: ranked
      .map((p, i) => ({ p, rank: i + 1 }))
      .filter(({ p }) => mine.has(p.id))
      .map(({ p, rank }) => ({
        id: p.id,
        title: p.title,
        score: p.score,
        rank,
        meta: [p.reach, p.status].filter(Boolean).join(" · "),
        organizations: links.filter((l) => l.problemId === p.id).map((l) => markOf.get(l.organizationId)!).filter(Boolean).slice(0, 4),
      })),
    sources: sourceRows.map(({ s, verifiedAt }) => ({
      title: s.title,
      url: s.url,
      domain: s.domain,
      note: verifiedAt ? `Verified ${dayLabel(verifiedAt)}` : `Added ${dayLabel(s.addedAt)}`,
    })),
    activity: log.map((a) => ({ when: whenLabel(a.at), text: a.text })),
  };
}

export async function restore(id: string, userId: string) {
  const [o] = await db.select().from(organizations).where(eq(organizations.id, id));
  if (!o) throw new NotFoundError("This organization no longer exists.");
  await db.update(organizations).set({ archivedAt: null, archivedBy: null, updatedAt: new Date(), updatedBy: userId }).where(eq(organizations.id, id));
  const [user] = await db.select().from(users).where(eq(users.id, userId));
  await db.insert(activityEntries).values({ actorId: userId, subjectKind: "Organization", subjectId: id, text: `${user?.name ?? userId} restored ${o.name}` });
  return get(id);
}

export class InvalidError extends Error {
  constructor(readonly errors: ReturnType<typeof validateOrganization>) {
    super(errors.map((e) => e.message).join("; "));
  }
}

/** Creates (id null) or updates an organization. New ones start Unverified; archived ones cannot be changed. */
export async function save(id: string | null, input: OrganizationInput, userId: string): Promise<string> {
  const errors = validateOrganization(input);
  if (errors.length) throw new InvalidError(errors);
  const values = {
    name: input.name.trim(),
    type: input.type,
    founded: input.founded.trim(),
    city: input.city.trim(),
    location: input.city.trim() || input.country.trim(),
    country: input.country.trim(),
    website: input.website.trim(),
    summary: input.summary.trim(),
    tags: input.tags,
    updatedAt: new Date(),
    updatedBy: userId,
  };
  const [user] = await db.select().from(users).where(eq(users.id, userId));
  const actor = user?.name ?? userId;
  if (id) {
    await assertEditable(id);
    await db.update(organizations).set(values).where(eq(organizations.id, id));
    await db.insert(activityEntries).values({ actorId: userId, subjectKind: "Organization", subjectId: id, text: `${actor} edited ${values.name}` });
    return id;
  }
  const [created] = await db.insert(organizations).values({ ...values, mark: initials(values.name), verificationStatus: "Unverified" }).returning();
  await db.insert(activityEntries).values({ actorId: userId, subjectKind: "Organization", subjectId: created.id, text: `${actor} created ${values.name}` });
  return created.id;
}

/** Archives organizations: they leave lists and the map, and the rest of the team is told. */
export async function archiveMany(ids: string[], userId: string) {
  const [user] = await db.select().from(users).where(eq(users.id, userId));
  const actor = user?.name ?? userId;
  const rows = await db.select().from(organizations).where(and(inArray(organizations.id, ids), isNull(organizations.archivedAt)));
  const team = await db.select().from(users).where(ne(users.id, userId));
  const now = new Date();
  for (const o of rows) {
    await db.update(organizations).set({ archivedAt: now, archivedBy: userId, updatedAt: now, updatedBy: userId }).where(eq(organizations.id, o.id));
    await db.insert(activityEntries).values({ actorId: userId, subjectKind: "Organization", subjectId: o.id, text: `${actor} archived ${o.name}` });
    if (team.length) {
      await db.insert(notifications).values(
        team.map((t) => ({ userId: t.id, type: "archived", title: `${actor} archived ${o.name}`, detail: "Hidden from lists and the map.", href: `/organizations/${o.id}` })),
      );
    }
  }
  return rows.map((o) => o.name);
}

export async function restoreMany(ids: string[], userId: string) {
  const [user] = await db.select().from(users).where(eq(users.id, userId));
  const rows = await db.select().from(organizations).where(inArray(organizations.id, ids));
  for (const o of rows) {
    await db.update(organizations).set({ archivedAt: null, archivedBy: null, updatedAt: new Date(), updatedBy: userId }).where(eq(organizations.id, o.id));
    await db.insert(activityEntries).values({ actorId: userId, subjectKind: "Organization", subjectId: o.id, text: `${user?.name ?? userId} restored ${o.name}` });
  }
}

/** Adds or removes one tag on every selected organization; archived ones are skipped. */
export async function tagMany(ids: string[], tag: string, mode: "add" | "remove", userId: string) {
  if (!(ORG_TAGS as readonly string[]).includes(tag)) throw new InvalidError([{ field: "tags", message: "Choose a tag" }]);
  const rows = await db.select().from(organizations).where(and(inArray(organizations.id, ids), isNull(organizations.archivedAt)));
  for (const o of rows) {
    const without = o.tags.filter((t) => t !== tag);
    const tags = mode === "add" ? ORG_TAGS.filter((t) => t === tag || without.includes(t)) : without;
    await db.update(organizations).set({ tags, updatedAt: new Date(), updatedBy: userId }).where(eq(organizations.id, o.id));
  }
}
