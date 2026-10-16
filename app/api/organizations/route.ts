import { CURRENT_USER_ID } from "@/lib/db";
import { CHIPS, InvalidError, list, save, SORTS } from "@/lib/services/organizations";
import { OrganizationBody } from "./body";

export async function GET(request: Request) {
  const p = new URL(request.url).searchParams;
  const sort = SORTS.find((s) => s === p.get("sort")) ?? "impact";
  const chips = (p.get("chips") ?? "").split(",").filter((c): c is (typeof CHIPS)[number] => (CHIPS as readonly string[]).includes(c));
  return Response.json(await list({ q: p.get("q") ?? "", chips, sort }));
}

/** Creates an organization. */
export async function POST(request: Request) {
  const body = OrganizationBody.safeParse(await request.json().catch(() => null));
  if (!body.success) return Response.json({ message: "Check the form and try again." }, { status: 400 });
  try {
    return Response.json({ ok: true, id: await save(null, body.data, CURRENT_USER_ID) });
  } catch (e) {
    if (e instanceof InvalidError) return Response.json({ message: e.message, errors: e.errors }, { status: 400 });
    console.error(e);
    return Response.json({ message: "Couldn't save — Try again." }, { status: 500 });
  }
}
