import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

const globalForDb = globalThis as unknown as { sql?: ReturnType<typeof postgres> };

const sql = (globalForDb.sql ??= postgres(process.env.DATABASE_URL ?? "postgres://harvest:harvest@localhost:5433/harvest_map"));

export const db = drizzle(sql, { schema });

/** No sign-in yet: every request acts as the seeded research lead. */
export const CURRENT_USER_ID = "naomi";
