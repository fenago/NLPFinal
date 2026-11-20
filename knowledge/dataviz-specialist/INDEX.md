# Dataviz Specialist - Knowledge Index

Project: Customer Review Analyzer dashboard. Charts: sentiment distribution, VADER vs star ratings, top collocations, entity leaderboards, confusion matrix. Library: Chart.js loaded by script tag on a static Netlify site. Notes distilled from chartjs.org, MDN and W3C WAI pages fetched 2026-11-20.

| File | Read when you need to... | Key takeaways |
|---|---|---|
| 01-chartjs-basics.md | add Chart.js and build a first chart | `<script src=...jsdelivr...chart.js>`, `new Chart(ctx, {type,data,options})`, `destroy()` before reuse, sized `position:relative` container, `maintainAspectRatio` |
| 02-chartjs-chart-types.md | pick and configure bar / stacked / horizontal / doughnut / scatter | `indexAxis:'y'`, `scales.x/y.stacked:true`, doughnut `cutout`, scatter `{x,y}` points; mapping of each dashboard chart to a type |
| 03-chartjs-accessibility-and-colors.md | label canvases and choose colors | canvas `role="img"` + `aria-label` or fallback content; WCAG 1.4.1 and 1.4.11; color-blind-safe rules; dark-mode defaults |
| 04-confusion-matrix-heatmap.md | render the 3x3 evaluation matrix | accessible `<table>` with `<caption>`, `th scope`, text in every cell, shading never the only cue |

Conventions
- "(unverified)" marks statements not confirmed on the fetched page.
- Related: knowledge/frontend-engineer/ (layout, fetch, a11y, loading); docs/04-dataset.md and docs/expert-roster.md.
- Source access note: pages were read via Firecrawl query extraction; colorbrewer2.org returned no hex values, so no palette codes are quoted from it.
