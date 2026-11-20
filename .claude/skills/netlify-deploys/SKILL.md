---
name: netlify-deploys
description: "Deploy previews, production deploys, build-log diagnosis and rollbacks on Netlify. Use when deploying or when a build fails."
user-invocable: false
metadata:
  skill-id: S36
  owner: netlify-engineer
  shared-with: [qa-engineer, orchestrator]
---

# Netlify Deploys (S36)

**Owner:** `netlify-engineer` · **Shared with:** `qa-engineer`, `orchestrator`

- Every PR gets a Deploy Preview; QA tests against its URL.
- Production = `main` branch deploy; Orchestrator approves.
- Build failed? Read the log top-down: Python version line, pip install, build.py stage timings, publish dir.
- Rollback: publish the previous successful deploy from the Deploys list.
- Local check: `netlify build` (CLI) or `python pipeline/build.py`.
- Reference: knowledge/netlify-engineer/06-deploys-and-cli.md.
