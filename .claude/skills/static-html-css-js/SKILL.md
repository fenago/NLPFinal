---
name: static-html-css-js
description: "Build the static site with plain HTML, CSS and JavaScript (no server code). Use for any page, layout or component work in site/."
user-invocable: false
metadata:
  skill-id: S30
  owner: frontend-engineer
  shared-with: [dataviz-specialist, pyodide-engineer]
---

# Static HTML CSS JS (S30)

**Owner:** `frontend-engineer` · **Shared with:** `dataviz-specialist`, `pyodide-engineer`

- Files: `site/index.html`, `site/styles.css`, `site/app.js` (ES modules), `site/charts.js`, `site/worker.mjs`.
- No build step for JS required; no framework unless the Orchestrator approves.
- Two tabs: Dashboard, Analyze your review; plus About/Method.
- Mobile first, works at 360 px wide, no horizontal scroll; light and dark via `prefers-color-scheme`.
- All data from `fetch("/data/*.json")`; handle loading and error states.
