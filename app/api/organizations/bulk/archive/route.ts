import { CURRENT_USER_ID } from "@/lib/db";
import { archiveMany } from "@/lib/services/organizations";
import { Ids } from "../ids";

export async function POST(request: Request) {
  const body = Ids.safeParse(await request.json().catch(() => null));
  if (!body.success) return Response.json({ message: "Choose at least one organization." }, { status: 400 });
  try {
    return Response.json({ ok: true, names: await archiveMany(body.data.ids, CURRENT_USER_ID) });
  } catch (e) {
    console.error(e);
    return Response.json({ message: "Couldn't archive. Try again." }, { status: 500 });
  }
}
