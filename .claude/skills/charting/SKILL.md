---
name: charting
description: "Build the dashboard charts with Chart.js. Use for any chart: sentiment distribution, VADER vs stars, collocations, aspects, entity leaderboards."
user-invocable: false
metadata:
  skill-id: S32
  owner: dataviz-specialist
  shared-with: [frontend-engineer]
---

# Charting (S32)

**Owner:** `dataviz-specialist` · **Shared with:** `frontend-engineer`

- Chart.js loaded via pinned version (self-hosted or approved CDN).
- Sentiment distribution: bar/doughnut. VADER vs stars: stacked bar or 3×3 confusion table/heatmap. Collocations & entities: horizontal bar (`indexAxis: "y"`). Aspect sentiment: diverging horizontal bar.
- `responsive: true`; set container height in CSS.
- Data comes only from site/data JSON; no hard-coded numbers.
- Reference: knowledge/dataviz-specialist/.
