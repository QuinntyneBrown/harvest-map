import { CURRENT_USER_ID } from "@/lib/db";
import { NotFoundError, restore } from "@/lib/services/organizations";

export async function POST(_: Request, ctx: { params: Promise<{ id: string }> }) {
  const { id } = await ctx.params;
  try {
    return Response.json({ ok: true, organization: await restore(id, CURRENT_USER_ID) });
  } catch (e) {
    if (e instanceof NotFoundError) return Response.json({ message: e.message }, { status: 404 });
    console.error(e);
    return Response.json({ message: "Couldn't restore. Try again." }, { status: 500 });
  }
}
