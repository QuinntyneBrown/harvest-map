export type AnswerStatus = "Open" | "Partial" | "Answered";

export type QuestionHeader = { number: number; text: string; status: AnswerStatus; sourceCount: number };

export type QuestionsOverview = { total: number; answered: number; partial: number; questions: QuestionHeader[] };

export type AnswerItem = { label: string; href: string; detail: string };

export type QuestionAnswer = { number: number; items: AnswerItem[] };

export type RunStatus = "Queued" | "Running" | "Done" | "Failed";

export type RunRow = {
  id: number;
  title: string;
  startedLabel: string;
  person: string;
  findingCount: number;
  status: RunStatus;
  failureReason: string | null;
};

export type FindingState = "Pending" | "Accepted" | "Rejected";

export type SourceView = { title: string; domain: string; url: string; date: string };

export type FindingView = {
  id: string;
  runId: number;
  statement: string;
  subjectKind: "Organization" | "Person";
  subject: string;
  organization: string | null;
  sourceDomain: string;
  confidence: number;
  lowConfidenceReason: string | null;
  state: FindingState;
  decidedBy: string | null;
  decidedAt: string | null;
  fields: Record<string, string>;
  sources: SourceView[];
};

export type ResearchOverview = {
  currentUser: string;
  totalRuns: number;
  running: number;
  findingsToReview: number;
  runs: RunRow[];
  findings: FindingView[];
  organizations: string[];
};

export type OrgStatus = "Verified" | "Unverified" | "Conflict";

export type OrganizationListItem = {
  id: string;
  name: string;
  mark: string | null;
  type: string;
  city: string;
  reach: string;
  tags: string[];
  status: OrgStatus;
};

export type OrganizationList = { total: number; verified: number; unverified: number; items: OrganizationListItem[] };

export type OrganizationDetail = {
  id: string;
  name: string;
  mark: string | null;
  status: OrgStatus;
  summary: string;
  tags: string[];
  type: string;
  founded: string;
  base: string;
  city: string;
  country: string;
  lastSaved: { at: string; by: string } | null;
  reach: string;
  website: string;
  archived: { by: string; at: string } | null;
  initiatives: string[];
  people: { id: string; name: string; initials: string; role: string; linkedinUrl: string | null }[];
  problems: { id: string; title: string; score: number; rank: number; meta: string; organizations: { name: string; mark: string }[] }[];
  sources: { title: string; url: string; domain: string; note: string }[];
  activity: { when: string; text: string }[];
};
