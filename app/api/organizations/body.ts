import { z } from "zod";

export const OrganizationBody = z.object({
  name: z.string(),
  type: z.string(),
  founded: z.string(),
  city: z.string(),
  country: z.string(),
  website: z.string(),
  summary: z.string(),
  tags: z.array(z.string()),
});
