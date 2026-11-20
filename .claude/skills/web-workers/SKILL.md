---
name: web-workers
description: "Run Pyodide in a Web Worker and message results to the page. Use when wiring the 'Analyze your review' tab."
user-invocable: false
metadata:
  skill-id: S28
  owner: pyodide-engineer
  shared-with: [frontend-engineer]
---

# Web Workers (S28)

**Owner:** `pyodide-engineer` · **Shared with:** `frontend-engineer`

- `const w = new Worker("/worker.mjs", { type: "module" })` — module worker required by Pyodide 314.x; messages: `{type:"init"}`, `{type:"analyze", id, text}` → `{type:"ready"}`, `{type:"progress", pct}`, `{type:"result", id, data}`, `{type:"error", id, message}`.
- Match responses by `id`; ignore stale ones.
- Never block the main thread; UI disables the button until `ready`.
- Reference: knowledge/frontend-engineer/01-web-workers.md, knowledge/pyodide-engineer/03-web-worker.md.
