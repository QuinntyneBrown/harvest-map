import { z } from "zod";

export const Ids = z.object({ ids: z.array(z.string().uuid()).min(1).max(500) });
