import { getDefaultDepth } from "@/lib/services/research";

export async function GET() {
  return Response.json({ defaultDepth: await getDefaultDepth() });
}
