# 02 - Chart.js chart types for this project

Sources:
- https://www.chartjs.org/docs/latest/charts/bar.html
- https://www.chartjs.org/docs/latest/charts/doughnut.html
- https://www.chartjs.org/docs/latest/charts/scatter.html
- https://www.chartjs.org/docs/latest/general/data-structures.html

Fetched: 2026-11-20

## Bar
```js
const config = { type: 'bar', data: data, options: { scales: { y: { beginAtZero: true } } } };
```
- `indexAxis`: `'x'` (default, vertical bars) or `'y'` (horizontal bars).
- Dataset props (defaults): `backgroundColor` (`rgba(0,0,0,0.1)`), `borderColor` (same), `borderWidth` (`0`), `barThickness`, `maxBarThickness`, `categoryPercentage` (`0.8`), `barPercentage` (`0.9`), `grouped` (`true`), `skipNull`.
- Scale defaults for bar: `offset: true`, `grid.offset: true` (bars sit between grid lines).
- Horizontal bar: set `options.indexAxis: 'y'`. The value axis is then `x`, so use `scales.x.beginAtZero: true` (the category axis becomes `y`). (Axis swap implied by docs; the beginAtZero-on-x detail is our inference, unverified.)
```js
new Chart(ctx, {
  type: 'bar',
  data: { labels: ['battery life', 'screen', 'price'], datasets: [{ label: 'Mentions', data: [42, 30, 25] }] },
  options: { indexAxis: 'y', scales: { x: { beginAtZero: true } }, plugins: { legend: { display: false } } }
});
```
- Stacked bars: set BOTH scales to stacked:
```js
options: { scales: { x: { stacked: true }, y: { stacked: true } } }
```
- Grouped (side by side) is the default with several datasets.

## Doughnut (and pie)
```js
const config = { type: 'doughnut', data: data };
```
- Same class as pie; only default `cutout` differs: `'50%'` doughnut, `0` pie.
- Options: `circumference` (360), `rotation` (0), dataset `backgroundColor`, `borderWidth` (2), `offset` (0), `spacing` (0).
- Radial charts default `aspectRatio` to `1`.
- Data shape: one dataset, `labels` for slices; or `parsing: { key: 'nested.value' }`.

## Scatter
```js
const config = {
  type: 'scatter', data: data,
  options: { scales: { x: { type: 'linear', position: 'bottom' } } }
};
```
- Data as `[{x: 1, y: 2}, ...]` (Object[] shape from data-structures page). Both axes numeric.

## Choosing a type for OUR charts (recommendations, not from docs)
| Chart | Best fit | Why |
|---|---|---|
| Sentiment distribution (pos/neu/neg counts or share) | Horizontal bar, or doughnut with 3 slices | 3 categories, parts of a whole; bar is easier to read exactly; doughnut acceptable for share. Always show counts/percent as text. |
| VADER label vs star rating (1-5 stars x pos/neu/neg) | Stacked bar (x = stars, stack = sentiment) or 100% stacked | Shows composition per star level; reveals where VADER disagrees with ratings. Add a table for exact numbers. |
| VADER compound vs stars (continuous) | Scatter | Only if plotting per-review compound scores; jitter x; may be dense. Mean compound per star as a simple bar/line is cleaner. |
| Top collocations (bigram + score/frequency) | Horizontal bar, sorted descending | Long text labels need horizontal space. |
| Entity leaderboards (PERSON/ORG/PRODUCT/GPE counts) | Horizontal bar, one per type (or tabbed) | Ranked categories with long names. |
| Confusion matrix 3x3 | HTML table (see file 04) | Matrix is tabular; a table is more accessible than a chart. |
- Prefer bars over pies for comparison; limit doughnut to <= 3-5 slices.
- Sort ranked bars descending; cap at top 10-15; label the axis ("Mentions", "Frequency").
- Use consistent sentiment colors across all charts (see file 03).

## Project application
- Write a helper `barH(canvasId, labels, values, title)` that builds the horizontal bar config once; reuse for collocations and each entity type.
- Write `stackedBySentiment(canvasId, stars, {neg, neu, pos})` for VADER vs stars.
- JSON -> chart mapping is done at render time; the JSON should contain already-sorted, already-truncated arrays (agree this in the data contract with ORC).
