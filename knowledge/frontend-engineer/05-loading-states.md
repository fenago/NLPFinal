# 05 - Loading states: progress, aria-busy, Pyodide cold start

Sources:
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/progress
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers

Fetched: 2026-11-20

## `<progress>` (MDN)
- `max`: work required; must be > 0; default `1`.
- `value`: work completed; between 0 and `max` (or 0..1 if `max` omitted).
- NO `value` attribute = indeterminate (activity of unknown length). To go back to indeterminate remove it: `el.removeAttribute('value')`. CSS: `:indeterminate`.
- Give it an accessible label: `<label for>` works, or `aria-labelledby` / `aria-label`. Text between the tags is only a fallback for old browsers, NOT a label.
```html
<label for="boot">Loading Python</label>
<progress id="boot" max="100"></progress>   <!-- indeterminate -->
<progress value="70" max="100">70 %</progress>
```
- MDN: when it describes loading of a page section, use `aria-describedby` pointing to the status text and set `aria-busy="true"` on the section being updated, removing it when done.

## `aria-busy` (MDN)
- Values: `false` (default), `true` (element is being updated).
- Tells AT to wait until changes finish before announcing; prevents multiple interruptions as parts of a live region load.
- Set `true` while loading, `false` when complete. DOM property: `el.ariaBusy = "true"`.
```html
<section id="results" aria-busy="true" aria-describedby="load-status">...</section>
<p id="load-status" role="status">Loading dashboard data...</p>
```
- In a `feed` role, busy suppresses announcements except user-initiated changes.

## Live announcements
- Use a pre-existing `role="status"` (implicit `aria-live="polite"`, `aria-atomic="true"`) and update its text; do not move focus. Avoid `assertive` unless critical. (See 03-accessibility.md.)

## Pyodide cold start (practical notes; project knowledge, not from the fetched pages)
- Loading the Pyodide runtime + NLTK + the VADER lexicon is the slow part (seconds, tens of MB; exact size unverified - measure). Do it inside the Web Worker so the page stays interactive.
- Strategy:
  1. Do NOT start loading on page load; start when the user opens the "Analyze" tab (or on first focus of the textarea) to protect dashboard performance.
  2. Disable the Analyze button and show a determinate or indeterminate `<progress>` with stage text: "Starting Python", "Loading NLTK", "Loading sentiment lexicon", "Ready".
  3. Worker posts `{type:"status", stage, pct?}`; UI updates the status region (throttle announcements: one per stage, not per percent).
  4. When ready: enable the button, set `aria-busy="false"`, announce "Analyzer ready".
  5. On failure: show the error, a Retry button (spawn a fresh Worker), and a plain-language fallback (the dashboard still works).
  6. After warm-up each analysis should be quick; show a short busy state on the button/results only.
- Tell users the first load is slow and later runs are fast, and that it is cached by the browser on revisits (HTTP cache behaviour depends on headers; unverified).
- Offer sample reviews that prefill the textarea so there is something to click while loading.
- Respect reduced motion: wrap any spinner animation in `@media (prefers-reduced-motion: reduce)` (media feature name from MDN; not fetched here, unverified).

## Project application
- Dashboard: skeleton cards + `aria-busy="true"` on the grid until all JSON promises settle; then set false and announce "Dashboard loaded".
- Analyze tab: the staged progress flow above, single `role="status"` region shared with the results summary.
- Never leave an indefinite spinner: combine with the timeout in 02-fetch-json.md and a worker `onerror` handler (01-web-workers.md).

## Sketch: worker status wiring (assembled from the patterns above)
```js
const status = document.getElementById("status");      // <p role="status"> present in initial HTML
const bar = document.getElementById("boot");           // <progress> without value = indeterminate
worker.onmessage = ({ data }) => {
  if (data.type === "status") {
    status.textContent = data.stage;                    // polite announcement, no focus change
    if (data.pct != null) bar.value = data.pct; else bar.removeAttribute("value");
  } else if (data.type === "ready") {
    document.getElementById("analyze-btn").disabled = false;
    panel.ariaBusy = "false";
    status.textContent = "Analyzer ready";
  }
};
worker.onerror = (e) => { status.textContent = `Analyzer failed: ${e.message}`; };
```
- Initialize with `panel.ariaBusy = "true"` before posting the first message to the worker.
