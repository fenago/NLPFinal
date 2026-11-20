---
name: playwright-e2e
description: "Browser end-to-end tests with Playwright for both tabs, including Pyodide cold start and mobile. Use when testing the site locally or on a deploy preview."
user-invocable: false
metadata:
  skill-id: S40
  owner: qa-engineer
  shared-with: [pyodide-engineer, frontend-engineer]
---

# Playwright E2E (S40)

**Owner:** `qa-engineer` · **Shared with:** `pyodide-engineer`, `frontend-engineer`

- Serve `site/` locally (`python -m http.server -d site`) or test the Deploy Preview URL.
- Dashboard: charts render, entity leaderboards non-empty, drill-down opens a review.
- Analyze tab: paste review → result appears within timeout (cold start ≤ 60 s), sentence scores shown, limitation note visible.
- Run a mobile project (e.g. iPhone device) and desktop Chromium.
- Use `--trace off` normally; `--trace on` to debug a failure.
- Reference: knowledge/qa-engineer/04-playwright.md.
