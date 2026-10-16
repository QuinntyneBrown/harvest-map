export const runs = [
  { id: 48, title: "Find LinkedIn profiles for 8 people", startedLabel: "12:04", person: "Naomi Achterberg", findingCount: 5, status: "Running", failureReason: null },
  { id: 47, title: "Who is helping Christian youth with AI?", startedLabel: "Yesterday", person: "Tobias Mwangi", findingCount: 12, status: "Done", failureReason: null },
  { id: 45, title: "Moonshot goals with a public deadline", startedLabel: "Fri 10 Oct", person: "Naomi Achterberg", findingCount: 0, status: "Failed", failureReason: "Rate limited by 2 sources" },
];

export const findings = [
  {
    id: "f1",
    runId: 47,
    statement: "Pat Gelsinger moved from chair to executive chair and head of technology at Gloo in April 2025.",
    subjectKind: "Person",
    subject: "Pat Gelsinger",
    organization: "Gloo",
    sourceDomain: "religionunplugged.com",
    confidence: 92,
    lowConfidenceReason: null,
    state: "Pending",
    decidedBy: null,
    decidedAt: null,
    fields: { role: "Executive Chair & Head of Technology", since: "2025", organization: "Gloo" },
    sources: [
      { title: "Pat Gelsinger takes on bigger role at Gloo", domain: "religionunplugged.com", url: "https://religionunplugged.com/gelsinger", date: "2 Apr 2025" },
      { title: "Gloo leadership", domain: "gloo.com", url: "https://gloo.com/leadership", date: "1 Apr 2025" },
    ],
  },
  {
    id: "f2",
    runId: 47,
    statement: "Creed has 1 million Gen Z users of its AI faith companion.",
    subjectKind: "Organization",
    subject: "Creed",
    organization: null,
    sourceDomain: "creed.app",
    confidence: 41,
    lowConfidenceReason: "Company claim; no independent source.",
    state: "Pending",
    decidedBy: null,
    decidedAt: null,
    fields: { name: "Creed", location: "", summary: "AI faith companion for Gen Z" },
    sources: [{ title: "About Creed", domain: "creed.app", url: "https://creed.app/about", date: "3 Sep 2026" }],
  },
];

export const organizations = ["Gloo", "FaithTech", "OneHope"];

export function overview(over: Partial<{ runs: unknown[]; findings: unknown[]; totalRuns: number; running: number; findingsToReview: number }> = {}) {
  return { currentUser: "Naomi Achterberg", totalRuns: 48, running: 1, findingsToReview: 2, runs, findings, organizations, ...over };
}

export function decided(finding: (typeof findings)[number], state: "Accepted" | "Rejected" | "Pending") {
  return {
    ok: true,
    finding: {
      ...finding,
      state,
      decidedBy: state === "Pending" ? null : "Naomi Achterberg",
      decidedAt: state === "Pending" ? null : new Date().toISOString(),
    },
  };
}
