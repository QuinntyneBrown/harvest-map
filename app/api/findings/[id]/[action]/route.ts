import { accept, DecisionError, reject, undo } from "@/lib/services/findings";

export async function POST(request: Request, ctx: { params: Promise<{ id: string; action: string }> }) {
  const { id, action } = await ctx.params;
  try {
    if (action === "accept") {
      const body = (await request.json().catch(() => null)) as { fields?: Record<string, string> } | null;
      return Response.json({ ok: true, finding: await accept(id, body?.fields ?? {}) });
    }
    if (action === "reject") return Response.json({ ok: true, finding: await reject(id) });
    if (action === "undo") return Response.json({ ok: true, finding: await undo(id) });
    return Response.json({ message: "Unknown action" }, { status: 404 });
  } catch (e) {
    if (e instanceof DecisionError) return Response.json({ message: e.message }, { status: 409 });
    console.error(e);
    return Response.json({ message: "Couldn't save — Try again." }, { status: 500 });
  }
}
