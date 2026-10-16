import { getOverview } from "@/lib/services/research";

export async function GET() {
  return Response.json(await getOverview());
}
