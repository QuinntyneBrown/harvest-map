import { and, eq, sql } from "drizzle-orm";
import { db } from "@/lib/db";
import { findings, organizationProblems, organizations, people, problems, sources } from "@/lib/db/schema";
import { CORE_QUESTIONS } from "@/lib/questions";
import type { AnswerItem, AnswerStatus, QuestionAnswer, QuestionsOverview } from "@/lib/types";
import { listRanked } from "./problems";

const TOP = 6;

type Computed = { items: AnswerItem[]; sourceCount: number };

/** Distinct sources behind accepted findings, keyed by subject name (organizations and people). */
async function sourcesBySubject() {
  const rows = await db
    .select({ name: sql<string>`lower(${findings.subjectName})`, url: sources.url })
    .from(sources)
    .innerJoin(findings, eq(sources.findingId, findings.id))
    .where(eq(findings.state, "Accepted"));
  const map = new Map<string, Set<string>>();
  for (const r of rows) map.set(r.name, (map.get(r.name) ?? new Set()).add(r.url));
  return map;
}

function countFor(map: Map<string, Set<string>>, names: string[]) {
  const urls = new Set<string>();
  for (const n of names) for (const u of map.get(n.toLowerCase()) ?? []) urls.add(u);
  return urls.size;
}

const bySourcesThenName = (map: Map<string, Set<string>>) => (a: { name: string }, b: { name: string }) =>
  countFor(map, [b.name]) - countFor(map, [a.name]) || a.name.localeCompare(b.name);

async function compute(number: number): Promise<Computed> {
  const src = await sourcesBySubject();
  const orgs = await db.select().from(organizations);
  const orgName = new Map(orgs.map((o) => [o.id, o.name]));

  switch (number) {
    case 1: {
      // Who is helping Christian youth, especially with AI? Every catalogued organization, best sourced first.
      const top = [...orgs].sort(bySourcesThenName(src)).slice(0, TOP);
      return {
        items: top.map((o) => ({ label: o.name, href: `/organizations/${o.id}`, detail: o.location })),
        sourceCount: countFor(src, top.map((o) => o.name)),
      };
    }
    case 2: {
      // Who is targeting moonshot problems? Organizations linked to a moonshot problem.
      const rows = await db
        .select({ org: organizations, problem: problems.title })
        .from(organizationProblems)
        .innerJoin(organizations, eq(organizationProblems.organizationId, organizations.id))
        .innerJoin(problems, and(eq(organizationProblems.problemId, problems.id), eq(problems.moonshot, true)));
      const seen = new Map<string, { name: string; id: string; problem: string }>();
      for (const r of rows) if (!seen.has(r.org.id)) seen.set(r.org.id, { name: r.org.name, id: r.org.id, problem: r.problem });
      const top = [...seen.values()].sort(bySourcesThenName(src)).slice(0, TOP);
      return {
        items: top.map((o) => ({ label: o.name, href: `/organizations/${o.id}`, detail: o.problem })),
        sourceCount: countFor(src, top.map((o) => o.name)),
      };
    }
    case 3: {
      // Who is targeting the most impactful problem? Problems by score, each with its best-sourced organization.
      const ranked = (await listRanked()).slice(0, TOP);
      const links = await db.select().from(organizationProblems);
      const leaders: string[] = [];
      const items = ranked.map((p) => {
        const linked = links.filter((l) => l.problemId === p.id).map((l) => ({ name: orgName.get(l.organizationId) ?? "" }));
        const leader = linked.sort(bySourcesThenName(src))[0]?.name;
        if (leader) leaders.push(leader);
        return { label: p.title, href: `/problems/${p.id}`, detail: leader ? `Score ${p.score} · ${leader}` : `Score ${p.score}` };
      });
      return { items, sourceCount: countFor(src, leaders) };
    }
    case 4: {
      // What are they doing? Organizations with a recorded summary of their work.
      const top = orgs.filter((o) => o.summary).sort(bySourcesThenName(src)).slice(0, TOP);
      return {
        items: top.map((o) => ({ label: o.name, href: `/organizations/${o.id}`, detail: o.summary })),
        sourceCount: countFor(src, top.map((o) => o.name)),
      };
    }
    case 5:
    case 6: {
      // Who are the key people? / Where are they on LinkedIn?
      const all = (await db.select().from(people)).filter((p) => p.role);
      const pool = number === 5 ? all : all.filter((p) => p.linkedinUrl);
      const top = pool.sort(bySourcesThenName(src)).slice(0, TOP);
      const items = top.map((p) => {
        const org = p.organizationId ? orgName.get(p.organizationId) : undefined;
        return { label: p.name, href: `/people/${p.id}`, detail: org ? `${p.role} · ${org}` : p.role };
      });
      const without = all.length - all.filter((p) => p.linkedinUrl).length;
      if (number === 6 && without > 0) items.push({ label: `${without} more without LinkedIn`, href: "/people", detail: "" });
      return { items, sourceCount: countFor(src, top.map((p) => p.name)) };
    }
    default:
      throw new Error(`Unknown question ${number}`);
  }
}

function statusOf(c: Computed): AnswerStatus {
  const answers = c.items.filter((i) => i.href !== "/people").length;
  return answers === 0 ? "Open" : answers >= 3 ? "Answered" : "Partial";
}

export async function getQuestionAnswer(number: number): Promise<QuestionAnswer> {
  return { number, items: (await compute(number)).items };
}

export async function getQuestionsOverview(): Promise<QuestionsOverview> {
  const computed = await Promise.all(CORE_QUESTIONS.map((_, i) => compute(i + 1)));
  const questions = CORE_QUESTIONS.map((text, i) => ({
    number: i + 1,
    text,
    status: statusOf(computed[i]),
    sourceCount: computed[i].sourceCount,
  }));
  return {
    total: questions.length,
    answered: questions.filter((q) => q.status === "Answered").length,
    partial: questions.filter((q) => q.status === "Partial").length,
    questions,
  };
}
