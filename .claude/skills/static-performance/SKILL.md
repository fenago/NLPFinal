---
name: static-performance
description: "Make the static site load fast: caching, compression and asset sizes. Use when tuning load time or headers."
user-invocable: false
metadata:
  skill-id: S37
  owner: netlify-engineer
  shared-with: [pyodide-engineer, frontend-engineer, qa-engineer]
---

# Static Performance (S37)

**Owner:** `netlify-engineer` · **Shared with:** `pyodide-engineer`, `frontend-engineer`, `qa-engineer`

- Netlify compresses text assets; keep JSON small (data-size-budget).
- Long-cache versioned assets (`/pyodide/*`, hashed JS/CSS); short-cache data.
- Load Pyodide only on the Analyze tab.
- Target: dashboard usable < 2 s on fast 4G; Lighthouse performance ≥ 90 for the dashboard.
