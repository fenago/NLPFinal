# 05 — Performance checks (LCP, Lighthouse, size budgets)

Sources:
- https://web.dev/articles/lcp
- https://developer.chrome.com/docs/lighthouse/overview
- https://web.dev/articles/performance-budgets-101
- https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver — **fetched but extraction returned empty; MDN details below are unverified**

Fetched: 2026-11-20

## Largest Contentful Paint (web.dev/articles/lcp)
- LCP = "render time of the largest image, text block, or video visible in the viewport, relative to when the user first navigated to the page."
- Thresholds, measured at the **75th percentile** of page loads (segment mobile/desktop): **good <= 2.5 s**, **poor > 4.0 s**, in between = needs improvement.
- Elements considered: `<img>`, `<image>` inside `<svg>`, `<video>` (poster or first frame), elements with a `url()` background image, block-level elements containing text.
- Not considered "rendered" until visible: images not yet loaded; text using web fonts during the font-block period.
- Measure in code:
  ```js
  new PerformanceObserver((entryList) => {
    for (const entry of entryList.getEntries()) {
      console.log('LCP candidate:', entry.startTime, entry);
    }
  }).observe({type: 'largest-contentful-paint', buffered: true});
  ```
  The last emitted entry's `startTime` is normally the LCP value ("however, that is not always the case").
- In Playwright you can read the last candidate with `page.evaluate` around the same observer (project idea, not from docs).

## Lighthouse (developer.chrome.com)
- Open-source automated auditing tool: audits for performance, accessibility, SEO, and more.
- Run via Chrome DevTools (Lighthouse tab, ~30–60 s), CLI, Node module (for CI), PageSpeed Insights, or the Chrome extension.
- CLI:
  ```bash
  npm install -g lighthouse
  lighthouse <url>
  lighthouse --help
  lighthouse <url> --output json --output-path ./lh.json   # JSON for scripted checks
  ```
- JSON output can be loaded into the Lighthouse Viewer. (Parsing `categories.performance.score` and `audits['largest-contentful-paint'].numericValue` from that JSON is how Lighthouse reports are normally consumed — field names from general knowledge, **unverified** on the fetched page.)
- Lab data caveat: Lighthouse is a synthetic lab test; run it against the built static output served locally or the Netlify deploy preview, mobile profile default (unverified).

## Performance budgets (web.dev/articles/performance-budgets-101)
- Definition: "a set of limits imposed on metrics that affect site performance" (page size, load time on a mobile network, HTTP request count).
- Budget kinds: **quantity-based** (max image size, number of web fonts, max script size, number of third-party resources), **milestone timings** (FCP, TTI), **rule-based** (Lighthouse score).
- Default numbers suggested: **< 5 s** to interactive and **< 170 KB** critical-path resources (compressed/minified) on a slow-3G / mid-range-phone baseline.
- Example budget statements: "Our product page must ship less than 170 KB of JavaScript on mobile"; "must score > 80 on Lighthouse performance audits".

## Practical file-size budget check (project script)
Uses only the standard library; compare gzip sizes, because Netlify serves compressed assets.
```python
# tests/test_budgets.py
import gzip, pathlib, pytest

SITE = pathlib.Path("site")
BUDGET = {          # bytes after gzip -- proposed numbers, tune with the team
    "index.html": 30_000,
    "data/summary.json": 50_000,
    "data/*.json (each)": 150_000,
    "app.js": 170_000,            # web.dev default critical-path figure
}
def gz(p): return len(gzip.compress(p.read_bytes(), 6))

def test_json_budget():
    big = {p.name: gz(p) for p in SITE.glob("data/*.json") if gz(p) > BUDGET["data/*.json (each)"]}
    assert not big, f"over budget (gzip bytes): {big}"

def test_total_data_budget():
    assert sum(gz(p) for p in SITE.glob("data/*.json")) < 1_000_000
```
Also record raw size of `data/reviews_sample.jsonl` (docs/04 target < 5 MB).

## Project application
- Biggest LCP risks: large JSON fetched before first paint, a chart library, and Pyodide (several MB). Load Pyodide lazily in the Web Worker only when "Analyze your own review" is first used, so dashboard LCP is unaffected.
- Check: `lighthouse http://localhost:3000 --output json` in CI, assert LCP <= 2.5 s on the lab run (allow headroom, e.g. fail only above 4 s), plus the size-budget tests above.
- Report both numbers: dashboard LCP and "time until Pyodide result visible" (the latter measured with Playwright, 04-playwright.md).
