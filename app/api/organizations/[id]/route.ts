import { CURRENT_USER_ID } from "@/lib/db";
import { ArchivedError, get, InvalidError, NotFoundError, save } from "@/lib/services/organizations";
import { OrganizationBody } from "../body";

const isId = (id: string) => /^[0-9a-f-]{36}$/i.test(id);

export async function GET(_: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  if (!isId(id)) return Response.json({ message: "Not found" }, { status: 404 });
  try {
    return Response.json(await get(id));
  } catch (e) {
    if (e instanceof NotFoundError) return Response.json({ message: e.message }, { status: 404 });
    console.error(e);
    return Response.json({ message: "Couldn't load this organization." }, { status: 500 });
  }
}

/** Saves changes to an organization. */
export async function POST(request: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  if (!isId(id)) return Response.json({ message: "Not found" }, { status: 404 });
  const body = OrganizationBody.safeParse(await request.json().catch(() => null));
  if (!body.success) return Response.json({ message: "Check the form and try again." }, { status: 400 });
  try {
    return Response.json({ ok: true, id: await save(id, body.data, CURRENT_USER_ID) });
  } catch (e) {
    if (e instanceof InvalidError) return Response.json({ message: e.message, errors: e.errors }, { status: 400 });
    if (e instanceof NotFoundError) return Response.json({ message: e.message }, { status: 404 });
    if (e instanceof ArchivedError) return Response.json({ message: e.message }, { status: 409 });
    console.error(e);
    return Response.json({ message: "Couldn't save — Try again." }, { status: 500 });
  }
}
