---
name: build-performance
description: "Keep the Netlify build fast and inside limits. Use when the build is slow, times out or uses too much memory."
user-invocable: false
metadata:
  skill-id: S25
  owner: build-pipeline-engineer
  shared-with: [netlify-engineer, spacy-expert]
---

# Build Performance (S25)

**Owner:** `build-pipeline-engineer` · **Shared with:** `netlify-engineer`, `spacy-expert`

- Use `nlp.pipe(batch_size=256)`; disable unused spaCy components.
- Process the committed sample only (1–3k reviews ≈ about a minute with en_core_web_sm).
- Time each stage and print it in the build log.
- Let Netlify cache pip downloads; avoid re-downloading data.
- If near the plan's build limit: shrink sample, drop `md`/`lg` models, or precompute nothing extra.
