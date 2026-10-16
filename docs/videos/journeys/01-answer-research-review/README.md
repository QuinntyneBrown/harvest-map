# Journey 01 · Answer, research, review

> **Runtime:** about 3 min 53 s · **Audience:** Harvest Map team members (researchers, analysts) · **Prerequisites:** none

**Video:** [01-answer-research-review.mp4](01-answer-research-review.mp4) · [Slides](slides.html) · **Audio:** [01-answer-research-review.mp3](01-answer-research-review.mp3) · [Transcript](script.md)

## Why this video exists

The first three journeys in [`docs/user-journeys.md`](../../../user-journeys.md) form one loop:
read the answers to the core questions, ask the web where they are thin, and decide what the
web found. This video walks that loop in the running app.

## Learning objectives

By the end, the viewer can:

- Read the Questions page: status, source count and the records behind each answer.
- Start a run from Re-run, Ask the web or the R key, and choose what to look for and how deep.
- Accept, reject, undo or edit a finding, and see the accepted record change an answer.

## Key questions

| Question | What a strong answer includes |
| --- | --- |
| Where does an answer come from? | Records in the catalogue; sources come from accepted findings |
| What does a research run produce? | Findings with a statement, sources and a confidence, held for review |
| When does a record change? | Only when a person accepts a finding; undo within 30 s reverses it |

## Code / assets on screen

| File | What to show |
| --- | --- |
| `images/questions.png` | The Questions page header and first question |
| `images/questions-q3.png` | Question three: problems by impact score with their leading organization |
| `images/ask-the-web.png` | Ask the web opened from Re-run on question five |
| `images/ask-the-web-invalid.png` | Something else with an empty question: Fix 1 thing to save |
| `images/research-runs.png` | Earlier runs with person, finding count and status |
| `images/research.png` | Findings to review, including a low-confidence reason |
| `images/finding-accepted.png` | Accepted by Naomi Achterberg · Undo available for 30 s |
| `images/review-finding.png`, `images/review-finding-invalid.png` | The Review finding dialog, then Enter a role |
| `images/questions-q5-after.png` | Question five after the accept, led by Kara Powell |

Screens are light-mode captures of the running app (`app/questions`, `app/research`), taken by
`tools/video-build/capture-app.mjs`. It resets the research tables to a fixed demo set of runs
and findings drawn from the mock cast, then drives the real UI. Slides are dark mode, styled from
the design-system tokens through `docs/videos/assets/slides.css`.

## Run sheet

| Time | Segment | Content |
| --- | --- | --- |
| 00:00-00:34 | Welcome | The six questions; three journeys, one loop |
| 00:34-01:22 | Answer the questions | Header counts, impact-ranked problems, per-card failure |
| 01:22-02:22 | Run research | Re-run or R, look for and depth, validation, runs list |
| 02:22-03:27 | Review a finding | Findings, Accept and Undo, Reject, Edit, required fields |
| 03:27-03:53 | The loop closes | The accepted person now answers question five; recap |

## Demo commands

From the repository root, with PostgreSQL up (`docker compose up -d`), migrated and seeded
(`npm run db:migrate`, `npm run db:seed -- --demo`):

```sh
npx next build && npx next start --port 3001        # capture against a production build
APP_URL=http://localhost:3001 node tools/video-build/capture-app.mjs docs/videos/journeys/01-answer-research-review
node tools/video-audio/generate-audio.mjs docs/videos/journeys/01-answer-research-review --dry-run
node tools/video-audio/generate-audio.mjs docs/videos/journeys/01-answer-research-review
node tools/video-build/build-video.mjs docs/videos/journeys/01-answer-research-review --check
node tools/video-build/build-video.mjs docs/videos/journeys/01-answer-research-review
```

The narration uses the offline Kokoro voice `af_heart` at speed 0.8, the same voice as the Coop
journey videos. One-time setup is in the header of `tools/video-audio/generate-audio.mjs`; the
generator picks up `.cache/kokoro-venv` and `.cache/kokoro/` automatically.

## Pitfalls

- Capture against `next start`, not `next dev`: the dev server's file watcher reloads the page when screenshots are written into the repository.
- The capture script deletes all research runs and findings in the database it points at. Use a local database.
- Cues must be copied exactly from `script.md`. Edit the script and the slide cue together.

## References

- [Kokoro-82M ONNX voices](https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX)
- [Playwright screenshots](https://playwright.dev/docs/screenshots)
