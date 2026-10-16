export type OrgItem = {
  id: string;
  name: string;
  mark: string | null;
  type: string;
  city: string;
  reach: string;
  tags: string[];
  status: "Verified" | "Unverified" | "Conflict";
};

export const faithtech: OrgItem = { id: "o1", name: "FaithTech", mark: "FT", type: "Community", city: "Waterloo", reach: "50+ cities", tags: ["AI", "Community", "Youth"], status: "Verified" };
export const gloo: OrgItem = { id: "o2", name: "Gloo", mark: "GL", type: "Platform", city: "Boulder", reach: "140,000 leaders", tags: ["AI", "Youth"], status: "Verified" };
export const kingdomCode: OrgItem = { id: "o3", name: "Kingdom Code", mark: "KC", type: "Startup", city: "London", reach: "", tags: ["Digital"], status: "Unverified" };

export const orgList = (items: OrgItem[] = [faithtech, gloo, kingdomCode], over = {}) => ({
  total: 19,
  verified: 12,
  unverified: 7,
  items,
  ...over,
});

export const faithtechDetail = {
  id: "o1",
  name: "FaithTech",
  mark: "FT",
  status: "Verified",
  summary: "Global community of Christian technologists in 50+ cities and 20+ countries.",
  tags: ["AI", "Community", "Youth"],
  type: "Community",
  founded: "2016",
  base: "Waterloo, Canada",
  city: "Waterloo",
  country: "Canada",
  lastSaved: { at: "Tue 14 Oct", by: "Tobias Mwangi" } as null | { at: string; by: string },
  reach: "50+ cities",
  website: "faithtech.com",
  archived: null as null | { by: string; at: string },
  initiatives: ["Missional Tech Trends research reports", "AI-assisted trauma-healing tool sprint for MENA (Feb 2026)"],
  people: [{ id: "p1", name: "James Kelly", initials: "JK", role: "Founder & CEO", linkedinUrl: null }],
  problems: [
    { id: "pr4", title: "AI that serves human flourishing", score: 83, rank: 4, meta: "Every AI user · Tracked", organizations: [{ name: "Gloo", mark: "GL" }, { name: "FaithTech", mark: "FT" }] },
  ],
  sources: [
    { title: "Canada's FaithTech aims to redeem technology", url: "https://ministrywatch.com/a", domain: "ministrywatch.com", note: "Verified Tue 14 Oct" },
    { title: "What is redemptive technology?", url: "https://letu.edu/b", domain: "letu.edu", note: "Added Mon 13 Oct" },
  ],
  activity: [{ when: "Today 12:04", text: "Run #48 looking for LinkedIn profiles" }],
};
