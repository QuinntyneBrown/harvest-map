export const ORG_TYPES = ["Community", "Platform", "Ministry", "Alliance", "Movement", "Product", "Startup", "Research", "Nonprofit"] as const;
export const ORG_TAGS = ["AI", "Youth", "Moonshot", "Scripture", "Research", "Community", "Digital"] as const;

export type OrganizationInput = {
  name: string;
  type: string;
  founded: string;
  city: string;
  country: string;
  website: string;
  summary: string;
  tags: string[];
};

export type FieldError = { field: keyof OrganizationInput; message: string };

const DOMAIN = /^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i;

/** Shared by the form (before sending) and the server (before saving). */
export function validateOrganization(input: OrganizationInput): FieldError[] {
  const errors: FieldError[] = [];
  if (!input.name.trim()) errors.push({ field: "name", message: "Enter a name" });
  if (!input.country.trim()) errors.push({ field: "country", message: "Enter a country" });
  if (!DOMAIN.test(input.website.trim())) errors.push({ field: "website", message: "Enter a website like example.org" });
  if (input.founded.trim() && !/^\d{4}$/.test(input.founded.trim())) errors.push({ field: "founded", message: "Enter a four-digit year" });
  return errors;
}
