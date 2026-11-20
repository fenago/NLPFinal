# 03 - Chart.js accessibility and colors

Sources:
- https://www.chartjs.org/docs/latest/general/accessibility.html
- https://www.chartjs.org/docs/latest/general/colors.html
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html (WCAG 1.4.1)
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html (WCAG 1.4.11)
- https://www.w3.org/WAI/WCAG22/quickref/
- https://colorbrewer2.org/ (only its scheme categories could be confirmed)

Fetched: 2026-11-20

## Chart.js accessibility page (canvas)
`<canvas>` is not readable by assistive tech by itself. Chart.js docs show two ways to give it a text alternative:
```html
<canvas id="goodCanvas1" width="400" height="100" aria-label="Hello ARIA World" role="img"></canvas>

<canvas id="okCanvas2" width="400" height="100">
    <p>Hello Fallback World</p>
</canvas>
```
- First form (`role="img"` + `aria-label`) is labelled "good", the fallback-content form "ok" in the docs' example IDs.
- The fetched summary of the page did not mention patterns/textures, legend point styles or plugins (not on the page as extracted; unverified whether the full page covers more).
- An `aria-label` is short. For data-heavy charts add a visible data table or a sentence summary (see file 04 and WCAG 1.1.1).

## Colors page
- Accepted formats: hex (`#36A2EB`, `#36A2EB80`), `rgb()/rgba()`, `hsl()/hsla()`, or a `CanvasPattern` / `CanvasGradient` object.
- Defaults: `Chart.defaults.backgroundColor = '#9BD0F5'`, `Chart.defaults.borderColor = '#36A2EB'`, `Chart.defaults.color = '#000'` (the options table lists older/other defaults; check at runtime).
- Per-dataset colors; for bar/doughnut give an ARRAY to color each bar/slice:
```js
datasets: [{ data: [1, 2, 3], borderColor: '#36A2EB', backgroundColor: '#9BD0F5' }]
```
- Patterns: `ctx.createPattern(img, 'repeat')` as `backgroundColor`; the docs also show a third-party pattern helper (`pattern.draw('square', '#ff6384')`) - that is the `patternomaly` library (name from its API; not stated in fetched text, unverified).
- Dark mode: `Chart.defaults.color` (text/ticks) and `Chart.defaults.borderColor` (grid) must be set manually for dark themes because canvas ignores CSS. Re-render or `chart.update()` after a theme change.

## WCAG requirements for charts
- 1.4.1 Use of Color (A): color must not be the only means of conveying information. Intent: users with color deficiencies must get the info another visual way. Related techniques listed by W3C: G111 (color AND pattern), G14 (info conveyed by color also available in text), failure F13 (chart conveying info only by color with a text alternative that omits it).
- 1.4.11 Non-text Contrast (AA): graphical objects needed to understand content need >= 3:1 against adjacent colors. Pie/doughnut: slice edges/adjacent slices need 3:1 unless labels/values are also provided as text. Adding text labels and values for each item, or borders, removes the reliance on color contrast.
- 1.1.1 Non-text Content (A): provide a text alternative serving the equivalent purpose.
- 1.4.3 text (axis labels, legend text): 4.5:1.

## Color-blind-safe guidance
- ColorBrewer (colorbrewer2.org) offers scheme types `sequential`, `diverging`, `qualitative` and filters for "colorblind safe", "print friendly", "photocopy safe". The fetched page did not expose hex values, so no hexes are copied here.
- Practical rule set (project guidance, grounded in WCAG 1.4.1):
  1. Never encode sentiment by color alone: put the words Positive/Neutral/Negative in the legend, axis labels, tooltips, and table.
  2. Avoid red vs green as the only distinction; use a blue/orange (or blue/vermillion) pair plus a neutral grey. Verify with ColorBrewer's colorblind-safe filter or a simulator listed by W3C (e.g. Vischeck, Microsoft Edge DevTools color-blindness emulation).
  3. Use ColorBrewer "diverging" for negative-to-positive scales and "sequential" for counts (heatmap).
  4. Add patterns or distinct border/marker shapes where slices/stacks are adjacent.
  5. Keep >= 3:1 contrast between each fill and the card background in BOTH light and dark themes.
- Candidate categorical sentiment palette (unverified by tool; check contrast and CVD yourself): negative `#d95f02`-like orange, neutral grey `#999999`, positive `#1b7fbd`-like blue.

## Project application
- Every `<canvas>` gets `role="img"` and a specific `aria-label` ("Bar chart: sentiment distribution; 58% positive, 12% neutral, 30% negative"), generated from the JSON so it stays accurate.
- Provide a `<details>` "View data as table" under each chart, or place the table next to it.
- Shared constants: `SENTIMENT_COLORS = {pos, neu, neg}` for light and dark; entity types use a single neutral accent because bar position and labels already carry the meaning.
- Legend: `plugins.legend.labels.usePointStyle: true` helps distinguish shapes (docs: matches point style).
- Hide legend on single-series horizontal bars (`legend.display: false`) and use a chart title/heading instead.

## Checklist before shipping a chart
- [ ] Canvas has `role="img"` and a data-specific `aria-label`.
- [ ] Same numbers available as text or table.
- [ ] Meaning not carried by color alone; legend/labels use words.
- [ ] Fills and strokes pass 3:1 in light and dark themes; text passes 4.5:1.
