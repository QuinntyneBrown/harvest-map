import { desc } from "drizzle-orm";
import { db } from "@/lib/db";
import { problems } from "@/lib/db/schema";

/** Problems ordered by impact score (reach × severity × tractability). */
export function listRanked() {
  return db.select().from(problems).orderBy(desc(problems.score), problems.title);
}
