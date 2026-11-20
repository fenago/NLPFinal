---
name: cold-start-ux
description: "Make Pyodide's first load bearable: progress, warm-up and fallbacks. Use when users wait for the live analyzer."
user-invocable: false
metadata:
  skill-id: S29
  owner: pyodide-engineer
  shared-with: [frontend-engineer, qa-engineer]
---

# Cold Start UX (S29)

**Owner:** `pyodide-engineer` · **Shared with:** `frontend-engineer`, `qa-engineer`

- Start loading the worker when the user opens the tab (or on idle), not on page load of the dashboard.
- Show staged progress: "Downloading Python… Loading NLTK… Ready".
- Timeout (e.g. 60 s) → friendly error + "Try again" + link to dataset examples.
- Cache: versioned Pyodide files get long cache headers so the second visit is fast.
- QA measures cold and warm load time in Playwright.
