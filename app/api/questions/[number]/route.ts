import { getQuestionAnswer } from "@/lib/services/coreQuestions";

export async function GET(_: Request, ctx: { params: Promise<{ number: string }> }) {
  const number = Number((await ctx.params).number);
  if (!Number.isInteger(number) || number < 1 || number > 6) return Response.json({ message: "Unknown question" }, { status: 404 });
  return Response.json(await getQuestionAnswer(number));
}
