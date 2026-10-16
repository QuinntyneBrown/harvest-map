import { getQuestionsOverview } from "@/lib/services/coreQuestions";

export async function GET() {
  return Response.json(await getQuestionsOverview());
}
