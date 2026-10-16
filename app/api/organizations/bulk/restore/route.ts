import { CURRENT_USER_ID } from "@/lib/db";
import { restoreMany } from "@/lib/services/organizations";
import { Ids } from "../ids";

export async function POST(request: Request) {
  const body = Ids.safeParse(await request.json().catch(() => null));
  if (!body.success) return Response.json({ message: "Choose at least one organization." }, { status: 400 });
  try {
    await restoreMany(body.data.ids, CURRENT_USER_ID);
    return Response.json({ ok: true });
  } catch (e) {
    console.error(e);
    return Response.json({ message: "Couldn't restore. Try again." }, { status: 500 });
  }
}
