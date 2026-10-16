import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  workers: 4,
  expect: { timeout: 10_000 },
  reporter: "list",
  use: { baseURL: "http://localhost:3000", trace: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "npm run dev",
    url: "http://localhost:3000/questions",
    reuseExistingServer: true,
    env: { NEXT_PUBLIC_TOAST_MS: "5000" },
    timeout: 120_000,
  },
});
