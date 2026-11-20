---
name: netlify-guardrail
description: "Hard platform constraints for this project: everything runs on Netlify with no outside servers. Use before proposing any architecture, dependency, runtime code or deployment change."
user-invocable: false
metadata:
  skill-id: S05
  owner: orchestrator
  shared-with: [meta-agent, netlify-engineer, build-pipeline-engineer, pyodide-engineer, nltk-expert, spacy-expert]
---

# Netlify Guardrail (S05)

**Owner:** `orchestrator` · **Shared with:** `meta-agent`, `netlify-engineer`, `build-pipeline-engineer`, `pyodide-engineer`, `nltk-expert`, `spacy-expert`

Facts (verified 2026-11-20, see docs/05-netlify-architecture.md and knowledge/netlify-engineer/):
- Python runs ONLY in the Netlify build (Ubuntu 24.04 image; `PYTHON_VERSION`, `runtime.txt` or `Pipfile`; `requirements.txt` at repo root).
- Netlify Functions: TypeScript, JavaScript, Go only. Edge Functions: TS/JS only. Netlify Server: Node.js, Early Access. None run Python.
- Pyodide in the browser has NLTK (prebuilt) but NOT spaCy.
- Project decision: no outside servers, no external APIs.

Therefore:
- spaCy output exists only for dataset reviews and curated examples generated at build time.
- Live "Analyze your own review" = NLTK in Pyodide only. The UI must say so honestly.
- Reject any proposal that needs a Python runtime server, a Python function, a database or a third-party NLP API.
