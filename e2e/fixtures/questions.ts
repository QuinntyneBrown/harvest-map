export const QUESTIONS = [
  "Who is helping Christian youth, especially with AI?",
  "Who is targeting moonshot problems?",
  "Who is targeting the most impactful problem?",
  "What are they doing?",
  "Who are the key people?",
  "Where are they on LinkedIn?",
];

export const overview = {
  total: 6,
  answered: 4,
  partial: 2,
  questions: [
    { number: 1, text: QUESTIONS[0], status: "Answered", sourceCount: 23 },
    { number: 2, text: QUESTIONS[1], status: "Answered", sourceCount: 14 },
    { number: 3, text: QUESTIONS[2], status: "Answered", sourceCount: 9 },
    { number: 4, text: QUESTIONS[3], status: "Partial", sourceCount: 38 },
    { number: 5, text: QUESTIONS[4], status: "Answered", sourceCount: 21 },
    { number: 6, text: QUESTIONS[5], status: "Partial", sourceCount: 8 },
  ],
};

export const emptyOverview = {
  total: 6,
  answered: 0,
  partial: 0,
  questions: QUESTIONS.map((text, i) => ({ number: i + 1, text, status: "Open", sourceCount: 0 })),
};

type Answer = { number: number; items: { label: string; href: string; detail: string }[] };

export const answers: Record<number, Answer> = {
  1: {
    number: 1,
    items: [
      { label: "Gloo", href: "/organizations/gloo", detail: "AI · 140,000 leaders" },
      { label: "FaithTech", href: "/organizations/faithtech", detail: "AI · 50+ cities" },
      { label: "Creed", href: "/organizations/creed", detail: "AI · Gen Z app" },
    ],
  },
  2: {
    number: 2,
    items: [
      { label: "illumiNations", href: "/organizations/illuminations", detail: "2033 · every language" },
      { label: "OneHope", href: "/organizations/onehope", detail: "2033 · next 2B children" },
      { label: "Lausanne Movement", href: "/organizations/lausanne", detail: "2050 · Great Commission" },
    ],
  },
  3: {
    number: 3,
    items: [
      { label: "Scripture in every language by 2033", href: "/problems/p1", detail: "Score 94 · illumiNations" },
      { label: "God's Word for every child", href: "/problems/p2", detail: "Score 91 · OneHope" },
      { label: "Great Commission by 2050", href: "/problems/p3", detail: "Score 88 · Lausanne Movement" },
    ],
  },
  4: {
    number: 4,
    items: [
      { label: "Gloo", href: "/organizations/gloo", detail: "Flourishing AI standards · Faith Assistant" },
      { label: "illumiNations", href: "/organizations/illuminations", detail: "AI-assisted translation drafting" },
    ],
  },
  5: {
    number: 5,
    items: [
      { label: "Pat Gelsinger", href: "/people/pat", detail: "Executive Chair & Head of Technology · Gloo" },
      { label: "Scott Beck", href: "/people/scott", detail: "Co-founder & CEO · Gloo" },
      { label: "James Kelly", href: "/people/james", detail: "Founder & CEO · FaithTech" },
    ],
  },
  6: {
    number: 6,
    items: [
      { label: "Pat Gelsinger", href: "/people/pat", detail: "Executive Chair & Head of Technology · Gloo" },
      { label: "James Kelly", href: "/people/james", detail: "Founder & CEO · FaithTech" },
      { label: "8 more without LinkedIn", href: "/people", detail: "" },
    ],
  },
};
