---
name: sentiment-visuals
description: "Show sentiment in a consistent, color-blind-safe way. Use whenever positive/neutral/negative appears in UI or charts."
user-invocable: false
metadata:
  skill-id: S33
  owner: dataviz-specialist
  shared-with: [frontend-engineer, nlp-evaluator]
---

# Sentiment Visuals (S33)

**Owner:** `dataviz-specialist` · **Shared with:** `frontend-engineer`, `nlp-evaluator`

- One palette for the whole app, defined as CSS custom properties: `--pos`, `--neu`, `--neg` (blue / gray / orange family, color-blind safe; avoid red-green alone).
- Always pair color with a text label or icon (+ / ○ / −).
- Diverging scales centered at 0 for compound scores (−1 … +1).
- Show the numeric compound score on hover/focus.
