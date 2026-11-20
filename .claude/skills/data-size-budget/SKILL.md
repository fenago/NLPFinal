---
name: data-size-budget
description: "Keep static JSON and assets small enough for fast page loads. Use when output files grow or the dashboard feels slow."
user-invocable: false
metadata:
  skill-id: S22
  owner: build-pipeline-engineer
  shared-with: [dataset-curator, frontend-engineer, dataviz-specialist, qa-engineer]
---

# Data Size Budget (S22)

**Owner:** `build-pipeline-engineer` · **Shared with:** `dataset-curator`, `frontend-engineer`, `dataviz-specialist`, `qa-engineer`

Budgets: each `site/data/*.json` ≤ 1 MB (`reviews.json` ≤ 3 MB or split into pages); dashboard first view ≤ 500 KB data.
- Round floats to 3 decimals; compact JSON (`separators=(",", ":")`).
- Truncate review text in lists; load full text on drill-down.
- Split large files (`reviews-0001.json` …) and lazy-load.
- QA enforces budgets with a size check test.
