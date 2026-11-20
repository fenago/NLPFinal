# 01 - Chart.js basics

Sources:
- https://www.chartjs.org/docs/latest/getting-started/
- https://www.chartjs.org/docs/latest/getting-started/installation.html
- https://www.chartjs.org/docs/latest/getting-started/usage.html
- https://www.chartjs.org/docs/latest/general/data-structures.html
- https://www.chartjs.org/docs/latest/configuration/responsive.html
- https://www.chartjs.org/docs/latest/configuration/legend.html
- https://www.chartjs.org/docs/latest/developers/api.html

Fetched: 2026-11-20

## Installation
- npm: `npm install chart.js`.
- CDN options listed on the docs: cdnjs (https://cdnjs.com/libraries/Chart.js) and jsDelivr (https://www.jsdelivr.com/package/npm/chart.js?path=dist).
- Getting-started example loads it with a script tag:
```html
<div><canvas id="myChart"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```
- That URL is unpinned ("latest"). For a deployed site PIN a version, e.g. `https://cdn.jsdelivr.net/npm/chart.js@<version>/dist/chart.umd.min.js` (pattern from jsDelivr; choose and test a concrete version - unverified here). The script defines a global `Chart`.
- Component registration (`Chart.register`) is only needed with bundlers/tree-shaking; it was not on the fetched pages (unverified).

## Minimal chart (docs example)
```html
<canvas id="myChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  const ctx = document.getElementById('myChart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{ label: '# of Votes', data: [12, 19, 3, 5, 2, 3], borderWidth: 1 }]
    },
    options: { scales: { y: { beginAtZero: true } } }
  });
</script>
```
- `new Chart(canvasElementOrContext, config)`; config = `{ type, data, options }`.

## data
- `data.labels` (category labels) + `data.datasets[]` each with `label`, `data`, plus style props.
- Dataset `data` accepted shapes:
  - Primitive[]: `data: [20, 10]` with `labels: ['a','b']`.
  - Array[]: `[[10, 20], [15, null]]`.
  - Object[]: `[{x: 'Sales', y: 20}, {x: 'Revenue', y: 10}]`.
  - Object (key -> value): `{ January: 10, February: 20 }`.
  - Custom keys via `options.parsing`: `{ xAxisKey: 'id', yAxisKey: 'nested.value' }`; doughnut/pie use `parsing: { key: 'nested.value' }`. Dots in key names must be escaped (`'data\\.key'`).
  - Per-dataset `parsing: { yAxisKey: 'net' }` lets several datasets share one array of objects.

## options (the ones we use)
- `options.scales.y.beginAtZero: true` (bar charts should start at zero).
- `options.plugins.legend`: `display` (default `true`), `position` (default `'top'`), `labels.usePointStyle` (default `false`), `labels.color`, `onClick(event, legendItem, legend)`.
- `options.responsive`, `options.maintainAspectRatio`, `options.aspectRatio`, `options.resizeDelay` (see below).

## Responsive and maintainAspectRatio
| Option | Default | Meaning |
|---|---|---|
| `responsive` | `true` | Resize chart when its container resizes |
| `maintainAspectRatio` | `true` | Keep canvas width/height ratio |
| `aspectRatio` | `1` for radial charts (doughnut), `2` otherwise | width / height |
| `resizeDelay` | `0` | ms to delay the resize update |
- Container MUST be relatively positioned and dedicated to the canvas (size the container, not the canvas):
```html
<div class="chart-container" style="position: relative; height:40vh; width:80vw">
  <canvas id="chart"></canvas>
</div>
```
- For a fixed-height chart in a flexible width card set `maintainAspectRatio: false` and give the container a height. (Behaviour implied by the options table; the example is ours.)
- Inside CSS grid give the chart container `min-width: 0` or it may not shrink.
- Printing: call `chart.resize()` / `Chart.instances[id].resize()` on `beforeprint`/`afterprint` (docs example).

## Instance methods
- `chart.update(mode?)` after mutating `chart.data` (`'none'` skips animation for one update).
- `chart.destroy()` - must be called before the canvas is reused for a new chart (important when re-rendering on theme change/tab switch).
- `chart.resize(width?, height?)`, `chart.toBase64Image(type?, quality?)`.

## Project application
- Plain script tag, one `site/js/charts.js` that fetches JSON then builds each chart with `new Chart(...)`.
- Keep a registry `{ id: chartInstance }`; on re-render call `.destroy()` first, or `.update()` if only data changed.
- Pin the CDN version (or vendor the file into `site/vendor/` so Netlify serves it and no third-party CDN is needed - recommended for a "no outside servers" project).
- Wrap every canvas in a sized, `position: relative` container.
- Data comes from `site/data/*.json`; map rows to `labels` and `data` arrays at render time.
