import { z } from "zod";
import { DEPTHS, InputError, LOOK_FOR, startRun } from "@/lib/services/research";

const StartRunInput = z.object({
  question: z.number().int().min(1).max(6).nullable(),
  customQuestion: z.string().nullable(),
  lookFor: z.array(z.enum(LOOK_FOR)),
  depth: z.enum(DEPTHS),
});

export async function POST(request: Request) {
  const input = StartRunInput.safeParse(await request.json().catch(() => null));
  if (!input.success) return Response.json({ message: "Check the question, what to look for and the depth." }, { status: 400 });
  try {
    return Response.json({ ok: true, runId: await startRun(input.data) });
  } catch (e) {
    if (e instanceof InputError) return Response.json({ message: e.message }, { status: 400 });
    console.error(e);
    return Response.json({ message: "The run couldn't be queued. Try again in a moment." }, { status: 503 });
  }
}
