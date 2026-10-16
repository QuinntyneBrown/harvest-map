/**
 * Seeds the signed-in user and the problem catalogue. With --demo, also seeds a few organizations
 * and people from the mock cast so /questions has answers before any research is accepted.
 * Run: npm run db:seed [-- --demo]
 */
import { eq } from "drizzle-orm";
import { initials } from "@/lib/format";
import { CURRENT_USER_ID, db } from "./index";
import { organizationProblems, organizations, people, problems, userSettings, users } from "./schema";

const PROBLEMS = [
  { title: "Scripture in every language by 2033", score: 94, moonshot: true },
  { title: "God's Word for every child", score: 91, moonshot: true },
  { title: "Great Commission by 2050", score: 88, moonshot: true },
  { title: "AI that serves human flourishing", score: 83, moonshot: false },
  { title: "Gen Z loneliness and faith formation", score: 79, moonshot: false },
  { title: "Every teen hears the gospel from a friend", score: 72, moonshot: true },
  { title: "Safe AI companions for young believers", score: 64, moonshot: false },
  { title: "Young adults engaging Scripture", score: 61, moonshot: false },
  { title: "Digital evangelism at scale", score: 58, moonshot: false },
];

const DEMO_ORGS = [
  { name: "illumiNations", city: "Dallas", country: "United States", website: "illuminations.bible", founded: "2017", type: "Alliance", reach: "2033 · every language", tags: ["Scripture", "Moonshot"], verified: true, location: "Global alliance", summary: "AI-assisted translation drafting", problems: ["Scripture in every language by 2033"] },
  { name: "OneHope", city: "Pompano Beach", country: "United States", website: "onehope.net", founded: "1987", type: "Ministry", reach: "Next 2B children", tags: ["Youth", "Scripture", "Moonshot"], verified: true, location: "Pompano Beach", summary: "Bible App for Kids · 165M installs", problems: ["God's Word for every child"] },
  { name: "Lausanne Movement", city: "Atlanta", country: "United States", website: "lausanne.org", founded: "1974", type: "Movement", reach: "Global", tags: ["Moonshot"], verified: true, location: "Global", summary: "Great Commission by 2050", problems: ["Great Commission by 2050"] },
  { name: "Gloo", city: "Boulder", country: "United States", website: "gloo.com", founded: "2013", type: "Platform", reach: "140,000 leaders", tags: ["AI", "Youth"], verified: true, location: "Boulder", summary: "Flourishing AI standards · Faith Assistant", problems: ["AI that serves human flourishing"] },
  { name: "FaithTech", city: "Waterloo", country: "Canada", website: "faithtech.com", founded: "2016", type: "Community", reach: "50+ cities", tags: ["AI", "Community", "Youth"], verified: true, location: "Waterloo", summary: "AI trauma-healing sprint · Missional Tech Trends", problems: ["AI that serves human flourishing"] },
  { name: "Kingdom Code", city: "London", country: "United Kingdom", website: "kingdomcode.org", founded: "", type: "Startup", reach: "", tags: ["Digital"], verified: false, location: "London", summary: "", problems: [] as string[] },
];

const DEMO_PEOPLE = [
  { name: "Pat Gelsinger", role: "Executive Chair & Head of Technology", org: "Gloo", linkedinUrl: "https://www.linkedin.com/in/patgelsinger" },
  { name: "James Kelly", role: "Founder & CEO", org: "FaithTech", linkedinUrl: null },
  { name: "Rob Hoskins", role: "President", org: "OneHope", linkedinUrl: null },
];

async function main() {
  await db.insert(users).values({ id: CURRENT_USER_ID, name: "Naomi Achterberg" }).onConflictDoNothing();
  await db.insert(userSettings).values({ userId: CURRENT_USER_ID, defaultDepth: "standard" }).onConflictDoNothing();

  if ((await db.select().from(problems).limit(1)).length === 0) await db.insert(problems).values(PROBLEMS);

  if (process.argv.includes("--demo")) {
    for (const o of DEMO_ORGS) {
      const values = {
        name: o.name, location: o.location, summary: o.summary, type: o.type, city: o.city, country: o.country, website: o.website,
        founded: o.founded, reach: o.reach, tags: o.tags, verificationStatus: o.verified ? "Verified" : "Unverified", mark: initials(o.name), updatedBy: CURRENT_USER_ID,
      };
      const [existing] = await db.select().from(organizations).where(eq(organizations.name, o.name));
      let orgId = existing?.id;
      if (existing) await db.update(organizations).set(values).where(eq(organizations.id, existing.id));
      else orgId = (await db.insert(organizations).values(values).returning())[0].id;
      for (const title of o.problems) {
        const [p] = await db.select().from(problems).where(eq(problems.title, title));
        if (p) await db.insert(organizationProblems).values({ organizationId: orgId!, problemId: p.id }).onConflictDoNothing();
      }
    }
    if ((await db.select().from(people).limit(1)).length === 0) {
      for (const p of DEMO_PEOPLE) {
        const [org] = await db.select().from(organizations).where(eq(organizations.name, p.org));
        await db.insert(people).values({ name: p.name, role: p.role, organizationId: org?.id, linkedinUrl: p.linkedinUrl });
      }
    }
  }
  console.log("Seeded.");
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
