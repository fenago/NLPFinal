# Frontend Engineer - Knowledge Index

Project: Customer Review Analyzer (static site on Netlify; dashboard reads static JSON; "Analyze your review" runs NLTK in Pyodide inside a Web Worker). Notes distilled from MDN and W3C WAI pages fetched 2026-11-20.

| File | Read when you need to... | Key takeaways |
|---|---|---|
| 01-web-workers.md | build the Pyodide worker and message protocol | `new Worker(url, {type})`, `postMessage`/`onmessage`, `onerror`, structured clone, no DOM, `terminate()` |
| 02-fetch-json.md | load `site/data/*.json` | check `response.ok`; `.json()` can throw `SyntaxError`; `AbortSignal.timeout()` |
| 03-accessibility.md | make tabs, forms, status messages, colors accessible | WCAG 1.4.1/1.4.3/1.4.11/2.1.1/2.4.7/4.1.3, `role="status"`, APG tabs keys |
| 04-responsive-layout.md | layout, theming, zoom | viewport meta (never disable zoom), mobile-first media queries, grid/flex, `prefers-color-scheme`, reflow 320px |
| 05-loading-states.md | Pyodide cold start and dashboard loading UI | `<progress>` (no value = indeterminate), `aria-busy`, staged status messages |

Conventions
- "(unverified)" marks statements not confirmed on the fetched page.
- Related: knowledge/dataviz-specialist/ for charts; docs/05-netlify-architecture.md for the architecture; docs/expert-roster.md for roles.
- Source access note: pages were read via Firecrawl; some summaries were produced by its query extraction rather than raw page text.
