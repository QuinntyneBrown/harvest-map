#!/usr/bin/env node
// Captures light-mode screenshots of the running Harvest Map app for a journey video.
//
//   node tools/video-build/capture-app.mjs <folder>
//
// Needs the app running (npm run dev) against PostgreSQL seeded with `npm run db:seed -- --demo`.
// It resets the research tables to a fixed demo set of runs and findings (people and
// organizations from the mock cast), then drives the real UI with Playwright and writes
// <folder>/images/*.png. Env: APP_URL (http://localhost:3000), DATABASE_URL.
import { mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { chromium } from '@playwright/test';
import postgres from 'postgres';

const APP = process.env.APP_URL || 'http://localhost:3000';
const folder = resolve(process.argv[2] || 'docs/videos/journeys/01-answer-research-review');
const out = join(folder, 'images');
mkdirSync(out, { recursive: true });

const sql = postgres(process.env.DATABASE_URL || 'postgres://harvest:harvest@localhost:5433/harvest_map');

const hoursAgo = (h) => new Date(Date.now() - h * 3_600_000);

async function seed() {
  await sql`delete from research_runs`;
  await sql`delete from people where name = 'Kara Powell'`;
  await sql`delete from organizations where name in ('Fuller Youth Institute', 'Creed')`;
  await sql`update people set role = 'Executive Chair & Head of Technology', since = '' where name = 'Pat Gelsinger'`;
  await sql`insert into users ${sql([{ id: 'tobias', name: 'Tobias Mwangi' }, { id: 'priya', name: 'Priya Raman' }, { id: 'elias', name: 'Elias Ferreira' }])} on conflict do nothing`;
  const runs = [
    { id: 44, title: 'Rank problems by reach × severity × tractability', question: 3, look_for: ['orgs'], depth: 'deep', status: 'Done', started_by: 'elias', started_at: hoursAgo(170) },
    { id: 45, title: 'Moonshot goals with a public deadline', question: null, custom_question: 'Moonshot goals with a public deadline', look_for: ['orgs'], depth: 'standard', status: 'Failed', failure_reason: 'Rate limited by 2 sources', started_by: 'naomi', started_at: hoursAgo(146) },
    { id: 46, title: 'What are they doing?', question: 4, look_for: ['orgs'], depth: 'standard', status: 'Done', started_by: 'priya', started_at: hoursAgo(74) },
    { id: 47, title: 'Who is helping Christian youth, especially with AI?', question: 1, look_for: ['orgs', 'people'], depth: 'deep', status: 'Done', started_by: 'tobias', started_at: hoursAgo(26) },
    { id: 48, title: 'Who are the key people?', question: 5, look_for: ['people', 'linkedin'], depth: 'standard', status: 'Done', started_by: 'naomi', started_at: hoursAgo(1) },
  ].map((r) => ({ custom_question: null, failure_reason: null, ...r }));
  await sql`insert into research_runs ${sql(runs)}`;
  await sql`select setval('research_runs_id_seq', 48)`;

  const findings = [
    {
      run_id: 48, subject_kind: 'Person', subject_name: 'Kara Powell', organization_name: 'Fuller Youth Institute', confidence: 92,
      statement: 'Kara Powell leads the Fuller Youth Institute as its Executive Director.',
      change: { role: 'Executive Director', since: '', organization: 'Fuller Youth Institute' },
      sources: [['Our team', 'https://fulleryouthinstitute.org/'], ['Fuller Seminary faculty', 'https://www.fuller.edu/']],
    },
    {
      run_id: 48, subject_kind: 'Person', subject_name: 'Pat Gelsinger', organization_name: 'Gloo', confidence: 92,
      statement: 'Pat Gelsinger moved from chair to executive chair and head of technology at Gloo in April 2025.',
      change: { role: 'Executive Chair & Head of Technology', since: '2025', organization: 'Gloo' },
      sources: [['Former Intel executive Pat Gelsinger joins Gloo', 'https://religionunplugged.com/'], ['Pat Gelsinger expands role at Gloo', 'https://www.christianpost.com/']],
    },
    {
      run_id: 47, subject_kind: 'Organization', subject_name: 'Gloo', organization_name: null, confidence: 90,
      statement: "Gloo's Flourishing AI standards build on the Global Flourishing Study (Harvard, Baylor, Gallup).",
      change: { name: 'Gloo', location: 'Boulder', summary: 'Flourishing AI standards · Faith Assistant' },
      sources: [['Gloo and the Flourishing AI standard', 'https://ministrywatch.com/']],
    },
    {
      run_id: 47, subject_kind: 'Organization', subject_name: 'Creed', organization_name: null, confidence: 41,
      low_confidence_reason: 'Company claim; no independent source.',
      statement: 'Creed has 50,000 daily active users.',
      change: { name: 'Creed', location: '', summary: 'AI · Gen Z app' },
      sources: [['About Creed', 'https://creed.ai/']],
    },
  ];
  // Findings accepted earlier, so the answers have sources behind them.
  const accepted = [
    ['Gloo', 46, 'Gloo builds Flourishing AI standards and a Faith Assistant for churches.', ['https://gloo.com/', 'https://ministrywatch.com/', 'https://religionunplugged.com/']],
    ['FaithTech', 47, 'FaithTech runs AI sprints with Christian technologists in 50+ cities.', ['https://faithtech.com/', 'https://www.mnnonline.org/']],
    ['illumiNations', 46, 'illumiNations drafts Scripture translations with AI to reach every language by 2033.', ['https://illuminations.bible/', 'https://www.christianitytoday.com/']],
    ['OneHope', 46, 'OneHope reaches children through the Bible App for Kids.', ['https://onehope.net/', 'https://www.youversion.com/']],
    ['James Kelly', 47, 'James Kelly is the founder and CEO of FaithTech.', ['https://faithtech.com/']],
    ['Rob Hoskins', 47, 'Rob Hoskins is president of OneHope.', ['https://onehope.net/']],
  ];
  for (const [subject, runId, statement, urls] of accepted) {
    const kind = ['James Kelly', 'Rob Hoskins'].includes(subject) ? 'Person' : 'Organization';
    const [row] = await sql`insert into findings ${sql({
      run_id: runId, subject_kind: kind, subject_name: subject, organization_name: null, confidence: 88, statement,
      change: sql.json(kind === 'Person' ? {} : { name: subject }), state: 'Accepted', decided_by: 'tobias', decided_at: hoursAgo(20),
    })} returning id`;
    for (const url of urls) {
      await sql`insert into sources ${sql({ finding_id: row.id, title: subject, url, domain: new URL(url).hostname.replace(/^www\./, ''), date: '' })}`;
    }
  }

  let minute = 0;
  for (const { sources, ...f } of findings) {
    const [row] = await sql`insert into findings ${sql({ low_confidence_reason: null, ...f, change: sql.json(f.change), created_at: new Date(Date.now() - minute++ * 60_000) })} returning id`;
    for (const [title, url] of sources) {
      await sql`insert into sources ${sql({ finding_id: row.id, title, url, domain: new URL(url).hostname.replace(/^www\./, ''), date: '' })}`;
    }
  }
}

async function shot(page, name, locator) {
  await page.mouse.move(0, 719);
  // Centre element shots so the sticky top bar cannot cover them.
  if (locator) await locator.evaluate((el) => el.scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(700);
  await (locator ?? page).screenshot({ path: join(out, `${name}.png`) });
  console.log(`wrote images/${name}.png`);
}

await seed();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2, colorScheme: 'light', reducedMotion: 'reduce' });

// Journey 1: answer the questions
await page.goto(`${APP}/questions`);
await page.locator('#q6 .answer__list a').first().waitFor();
await shot(page, 'questions');
await page.locator('#q3').scrollIntoViewIfNeeded();
await shot(page, 'questions-q3', page.locator('#q3'));

// Journey 2: run research
await page.locator('#q5').getByRole('button', { name: 'Re-run' }).click();
const ask = page.getByRole('dialog', { name: 'Ask the web' });
await ask.waitFor();
await shot(page, 'ask-the-web');
await ask.getByRole('radio', { name: 'Something else' }).check();
await ask.getByRole('button', { name: 'Run', exact: true }).click();
await ask.locator('.form-summary').waitFor();
await shot(page, 'ask-the-web-invalid');
await page.keyboard.press('Escape');

// Journey 3: review a finding
await page.goto(`${APP}/research`);
await page.getByTestId('finding').first().waitFor();
await shot(page, 'research');
await shot(page, 'research-runs', page.getByRole('region', { name: 'Earlier runs' }).locator('.entity-list'));
await page.evaluate(() => window.scrollTo(0, 0));
const kara = page.getByTestId('finding').filter({ hasText: 'Kara Powell leads' });
await kara.getByRole('button', { name: 'Accept', exact: true }).click();
await kara.locator('.finding__decision').waitFor();
await page.waitForResponse((r) => r.url().endsWith('/api/research'));
await shot(page, 'finding-accepted', kara);
const pat = page.getByTestId('finding').filter({ hasText: 'Pat Gelsinger moved' });
await pat.getByRole('button', { name: 'Edit', exact: true }).click();
const review = page.getByRole('dialog', { name: 'Review finding' });
await review.waitFor();
await shot(page, 'review-finding');
await review.getByLabel('Role').fill('');
await review.getByRole('button', { name: 'Accept', exact: true }).click();
await review.locator('.form-summary').waitFor();
await shot(page, 'review-finding-invalid');
await page.keyboard.press('Escape');

// Back to the answers: the accepted person now answers question 5
await page.goto(`${APP}/questions`);
await page.locator('#q5 .answer__list a').first().waitFor();
await page.locator('#q5').scrollIntoViewIfNeeded();
await shot(page, 'questions-q5-after', page.locator('#q5'));

await browser.close();
await sql.end();
