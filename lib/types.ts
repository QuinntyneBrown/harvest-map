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
