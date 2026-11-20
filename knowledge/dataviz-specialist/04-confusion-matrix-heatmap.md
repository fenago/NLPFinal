# 04 - Confusion matrix / heatmap as an accessible table

Sources:
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/table
- https://www.w3.org/WAI/tutorials/tables/
- https://www.w3.org/WAI/tutorials/tables/two-headers/
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

Fetched: 2026-11-20 (the two-headers subpage URL was listed on the WAI tutorial page but not itself fetched)

## Why a table
- A 3x3 confusion matrix (rows = actual class from star rating, columns = predicted class from VADER) is tabular data. Chart.js has no built-in heatmap/matrix type (that is a plugin; not verified), so use an HTML `<table>` with cell shading. Tables are natively navigable by screen readers.

## MDN table accessibility guidance
- `<caption>`: clearly and concisely describes the table's purpose; helps screen-reader, low-vision and cognitive-concern users decide whether to read it.
- `<thead>` encloses column header cells; `<tbody>` the data rows; `<th>` header cell.
- `scope="col"` / `scope="row"` on `<th>`: redundant in simple tables (inferred) but may help AT that infer incorrectly; useful in complex tables.
- `colspan`/`rowspan` mean a "complex table" that AT can struggle with; prefer splitting into simpler tables. If unavoidable use `id` + `headers`.
- Example from MDN:
```html
<table>
  <tr><th scope="col">Name</th><th scope="col">Age</th></tr>
  <tr><td>Maria Sanchez</td><td>28</td></tr>
</table>
```

## WAI Tables tutorial (key points)
- Mark header cells with `<th>`, data with `<td>`.
- Set `scope` to `col` or `row` where direction is unclear; `colgroup`/`rowgroup` for irregular headers.
- Caption identifies the table topic; a summary gives orientation for complex tables.
- Subpages: one-header, two-headers, irregular, multi-level, caption-summary (URLs under https://www.w3.org/WAI/tutorials/tables/).
- A matrix has BOTH row and column headers ("two headers" case): column `<th scope="col">`, row `<th scope="row">`.

## Pattern for the 3x3 matrix
```html
<table class="cm">
  <caption>Confusion matrix: star-derived label (rows) vs VADER label (columns), n = 2,000 reviews</caption>
  <thead>
    <tr>
      <td></td>
      <th scope="col">Predicted negative</th>
      <th scope="col">Predicted neutral</th>
      <th scope="col">Predicted positive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Actual negative</th>
      <td style="--v:0.62">310 <small>(62%)</small></td>
      <td style="--v:0.18">90 <small>(18%)</small></td>
      <td style="--v:0.20">100 <small>(20%)</small></td>
    </tr>
    <!-- neutral and positive rows likewise -->
  </tbody>
</table>
```
```css
.cm td { background: color-mix(in srgb, var(--accent) calc(var(--v) * 100%), transparent); text-align: center; }
```
- `color-mix()` and the `--v` custom property are our technique (unverified on MDN pages fetched); generate inline background colors in JS if older browser support is needed.
- The empty top-left cell: use `<td></td>` (or a `<th>` with visually hidden text "Actual / Predicted").
- Row/column totals and per-class precision/recall go in extra columns/rows or a second simple table.

## Accessibility rules for the heatmap shading
- Never rely on shade alone (WCAG 1.4.1): every cell prints the count AND percentage as text.
- Text in each cell must meet 4.5:1 against its shaded background (1.4.3); pick dark text on light shades and switch to light text above ~55% intensity, or cap the max shade lightness.
- Highlight the diagonal (correct predictions) with an additional non-color cue such as a bold border or a "correct" marker, not just a darker hue.
- Use a sequential single-hue ramp (e.g. a ColorBrewer sequential scheme), colorblind-safe by design since only lightness varies.
- Let the table scroll horizontally in a wrapper on narrow screens (WCAG Reflow allows 2-D layout for data tables): `<div style="overflow-x:auto" tabindex="0" role="region" aria-label="Confusion matrix">`.
- Add a sentence summary: "Overall accuracy 71%. VADER most often confuses neutral reviews with positive."

## Project application
- Data contract: `evaluation.json` with `labels: ["negative","neutral","positive"]`, `matrix: [[..],[..],[..]]` (rows actual, cols predicted), `accuracy`, `n`. Render with `document.createElement` / `textContent` (no innerHTML from data).
- Define how stars map to classes in the caption (e.g. 1-2 negative, 3 neutral, 4-5 positive) so readers understand "actual" is a proxy.
- Optionally also offer a stacked-bar chart (file 02) of the same numbers; the table remains the primary accessible form.
