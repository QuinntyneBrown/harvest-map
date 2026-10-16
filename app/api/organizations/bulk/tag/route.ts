import { z } from "zod";
import { CURRENT_USER_ID } from "@/lib/db";
import { InvalidError, tagMany } from "@/lib/services/organizations";
import { Ids } from "../ids";

const Body = Ids.extend({ tag: z.string(), mode: z.enum(["add", "remove"]) });

export async function POST(request: Request) {
  const body = Body.safeParse(await request.json().catch(() => null));
  if (!body.success) return Response.json({ message: "Choose organizations and a tag." }, { status: 400 });
  try {
    await tagMany(body.data.ids, body.data.tag, body.data.mode, CURRENT_USER_ID);
    return Response.json({ ok: true });
  } catch (e) {
    if (e instanceof InvalidError) return Response.json({ message: e.message }, { status: 400 });
    console.error(e);
    return Response.json({ message: "Couldn't tag. Try again." }, { status: 500 });
  }
}
