/**
 * Seeds the signed-in user and the problem catalogue. With --demo, also seeds a few organizations
 * and people from the mock cast so /questions has answers before any research is accepted.
 * Run: npm run db:seed [-- --demo]
 */
import { eq } from "drizzle-orm";
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
  { name: "illumiNations", location: "Global alliance", summary: "AI-assisted translation drafting", problems: ["Scripture in every language by 2033"] },
  { name: "OneHope", location: "Pompano Beach", summary: "Bible App for Kids · 165M installs", problems: ["God's Word for every child"] },
  { name: "Lausanne Movement", location: "Global", summary: "Great Commission by 2050", problems: ["Great Commission by 2050"] },
  { name: "Gloo", location: "Boulder", summary: "Flourishing AI standards · Faith Assistant", problems: ["AI that serves human flourishing"] },
  { name: "FaithTech", location: "Waterloo", summary: "AI trauma-healing sprint · Missional Tech Trends", problems: ["AI that serves human flourishing"] },
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

  if (process.argv.includes("--demo") && (await db.select().from(organizations).limit(1)).length === 0) {
    for (const o of DEMO_ORGS) {
      const [org] = await db.insert(organizations).values({ name: o.name, location: o.location, summary: o.summary }).returning();
      for (const title of o.problems) {
        const [p] = await db.select().from(problems).where(eq(problems.title, title));
        if (p) await db.insert(organizationProblems).values({ organizationId: org.id, problemId: p.id });
      }
    }
    for (const p of DEMO_PEOPLE) {
      const [org] = await db.select().from(organizations).where(eq(organizations.name, p.org));
      await db.insert(people).values({ name: p.name, role: p.role, organizationId: org?.id, linkedinUrl: p.linkedinUrl });
    }
  }
  console.log("Seeded.");
  process.exit(0);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
