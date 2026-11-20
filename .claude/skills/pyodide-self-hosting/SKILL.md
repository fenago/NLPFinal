---
name: pyodide-self-hosting
description: "Self-host and pin the Pyodide distribution inside the static site. Use when setting up site/pyodide/ or debugging Pyodide load failures."
user-invocable: false
metadata:
  skill-id: S27
  owner: pyodide-engineer
  shared-with: [netlify-engineer]
---

# Pyodide Self Hosting (S27)

**Owner:** `pyodide-engineer` · **Shared with:** `netlify-engineer`

- Pin one Pyodide version (stable at research time: 314.0.8); record it in `meta.json`.
- Copy only needed files to `site/pyodide/` (core + nltk and its deps) — the full distribution is 200 MB+.
- Netlify warns files > 10 MB may fail to upload: check `pyodide.asm.wasm` size on the first deploy preview.
- Ensure `.wasm` served as `application/wasm` and long-cache headers for versioned files (NET owns netlify.toml).
- Project decision: everything on Netlify — do not load Pyodide from a CDN in production.
- Reference: knowledge/pyodide-engineer/05-downloading-deploying.md.
