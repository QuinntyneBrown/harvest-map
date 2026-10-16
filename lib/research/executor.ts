import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import { eq } from "drizzle-orm";
import { z } from "zod";
import { db } from "@/lib/db";
import { findings, organizations, people, researchRuns, sources } from "@/lib/db/schema";

const MODEL = "claude-opus-5-5";
const SEARCHES = { quick: 3, standard: 8, deep: 20 } as const;
const LOW_CONFIDENCE = 60;

const FindingsSchema = z.object({
  findings: z.array(
    z.object({
      subjectKind: z.enum(["Organization", "Person"]),
      subjectName: z.string(),
      organizationName: z.string().nullable(),
      statement: z.string(),
      confidence: z.number().int(),
      lowConfidenceReason: z.string().nullable(),
      role: z.string().nullable(),
      since: z.string().nullable(),
      linkedinUrl: z.string().nullable(),
      location: z.string().nullable(),
      summary: z.string().nullable(),
      sources: z.array(z.object({ title: z.string(), url: z.string(), date: z.string().nullable() })),
    }),
  ),
});

type Extracted = z.infer<typeof FindingsSchema>["findings"][number];

const LOOK_FOR_TEXT: Record<string, string> = {
  orgs: "organizations",
  people: "key people (name, current role, organization)",
  linkedin: "public LinkedIn profile URLs of key people",
};

/** Executes one research run in-process: web search through Claude, then findings held for review. */
export async function executeRun(runId: number) {
  try {
    const [run] = await db.update(researchRuns).set({ status: "Running" }).where(eq(researchRuns.id, runId)).returning();
    const known = {
      orgs: (await db.select({ name: organizations.name }).from(organizations)).map((o) => o.name),
      people: (await db.select({ name: people.name }).from(people)).map((p) => p.name),
    };
    const extracted = await research(run.title, run.lookFor, run.depth as keyof typeof SEARCHES, known);
    for (const f of extracted) await saveFinding(runId, f);
    await db.update(researchRuns).set({ status: "Done", finishedAt: new Date() }).where(eq(researchRuns.id, runId));
  } catch (e) {
    const reason = e instanceof Anthropic.APIError ? `${e.status ?? ""} ${e.message}`.trim() : (e as Error).message;
    await db
      .update(researchRuns)
      .set({ status: "Failed", failureReason: reason.slice(0, 300), finishedAt: new Date() })
      .where(eq(researchRuns.id, runId));
  }
}

async function research(question: string, lookFor: string[], depth: keyof typeof SEARCHES, known: { orgs: string[]; people: string[] }) {
  const client = new Anthropic();
  const prompt = [
    "You research organizations worldwide that serve Christian youth, especially those helping young people navigate AI-driven change, loneliness and the search for meaning, and organizations targeting moonshot problems.",
    `Question: ${question}`,
    `Look for: ${lookFor.map((l) => LOOK_FOR_TEXT[l]).join("; ")}.`,
    `Already in the catalogue — organizations: ${known.orgs.join(", ") || "none"}; people: ${known.people.join(", ") || "none"}. Prefer new facts or corrections about these, and new subjects.`,
    "Search the web, then return findings. Each finding is one factual statement about one organization or one person, with every source URL that supports it.",
    "For a person, set role (current title), since (year), organizationName and linkedinUrl when found. For an organization, set location and a one-line summary of what it does for youth. Leave fields you did not find as null.",
    `confidence is 0-100: how likely the statement is correct. Below ${LOW_CONFIDENCE}, give lowConfidenceReason in a few words, e.g. "Company claim; no independent source." Never invent sources.`,
  ].join("\n\n");

  const messages: Anthropic.Beta.BetaMessageParam[] = [{ role: "user", content: prompt }];
  for (let turn = 0; turn < 5; turn++) {
    const response = await client.beta.messages.parse({
      model: MODEL,
      max_tokens: 16000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      tools: [{ type: "web_search_20260209", name: "web_search", max_uses: SEARCHES[depth] }],
      output_config: { effort: "medium", format: betaZodOutputFormat(FindingsSchema) },
      messages,
    });
    if (response.stop_reason === "pause_turn") {
      messages.push({ role: "assistant", content: response.content });
      continue;
    }
    if (response.stop_reason === "refusal") throw new Error("The research request was declined");
    if (!response.parsed_output) throw new Error("The research returned no findings");
    return response.parsed_output.findings;
  }
  throw new Error("The research did not finish");
}

async function saveFinding(runId: number, f: Extracted) {
  const valid = f.sources.filter((s) => URL.canParse(s.url));
  if (!valid.length) return;
  const change: Record<string, string> =
    f.subjectKind === "Person"
      ? {
          role: f.role ?? "",
          since: f.since ?? "",
          organization: f.organizationName ?? "",
          ...(f.linkedinUrl ? { linkedinUrl: f.linkedinUrl } : {}),
        }
      : { name: f.subjectName, location: f.location ?? "", summary: f.summary ?? "" };
  const confidence = Math.max(0, Math.min(100, f.confidence));
  const [row] = await db
    .insert(findings)
    .values({
      runId,
      statement: f.statement,
      subjectKind: f.subjectKind,
      subjectName: f.subjectName,
      organizationName: f.subjectKind === "Person" ? f.organizationName : null,
      confidence,
      lowConfidenceReason: confidence < LOW_CONFIDENCE ? (f.lowConfidenceReason ?? "Low confidence") : null,
      change,
    })
    .returning();
  await db.insert(sources).values(
    valid.map((s) => ({
      findingId: row.id,
      title: s.title,
      url: s.url,
      domain: new URL(s.url).hostname.replace(/^www\./, ""),
      date: s.date ?? "",
    })),
  );
}
