import type { Metadata } from "next";
import "./styles/tokens.css";
import "./styles/components.css";
import { RunResearchProvider } from "@/components/RunResearch";
import { TopBar } from "@/components/TopBar";

export const metadata: Metadata = {
  title: "Harvest Map",
  description: "Mapping organizations that serve Christian youth.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta name="color-scheme" content="light dark" />
      </head>
      <body>
        <a className="skip-link" href="#main">
          Skip to content
        </a>
        <RunResearchProvider>
          <TopBar />
          {children}
        </RunResearchProvider>
      </body>
    </html>
  );
}
