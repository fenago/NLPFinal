# QA Engineer knowledge — index

Fetched 2026-11-20 from official docs. Project context: /home/user/NLPFinal/docs (README, 02-nltk, 03-spacy, 04-dataset).

| File | Use it when | Primary sources |
|---|---|---|
| 01-pytest.md | Writing/organising Python tests: discovery, assert, session fixture for spaCy, parametrize, tmp_path, skip/xfail | docs.pytest.org (goodpractices, assert, fixtures, parametrize, tmp_path, skipping) |
| 02-snapshot-golden-tests.md | Pinning NLP outputs in `tests/golden/*.json`, `--update-golden` flow | docs.pytest.org (assert, tmp_path, example/simple) — no official snapshot feature; plugins unverified |
| 03-json-schema-validation.md | Validating the build's static JSON contract | json-schema.org getting started, python-jsonschema `validate` docs |
| 04-playwright.md | Browser E2E for the static site, mobile project, webServer, traces | playwright.dev docs |
| 05-performance-checks.md | LCP, Lighthouse CLI, gzip size budgets | web.dev (LCP, perf budgets), developer.chrome.com Lighthouse |

## Quick test plan
1. Unit/pipeline (pytest): sentiment thresholds, entity masking, aspect pairs on the doc-02/03 smoke review.
2. Golden JSON: small fixtures, tolerant floats.
3. Schema: every `data/*.json` validates against `tests/schemas`.
4. E2E (Playwright): dashboard renders; live Pyodide analyze works (long timeout); mobile viewport.
5. Budgets: gzip size limits + Lighthouse LCP.

## Known gaps / unverified
- pytest-playwright (Python bindings) and snapshot plugins not fetched.
- MDN PerformanceObserver page returned no extractable content.
- python-jsonschema `errors` page (`best_match`, `.path`) not fetched.
