# Build plan: Customer Review Analyzer

Owner: `orchestrator` (Atlas). Updated after every handoff. Phases follow `docs/expert-roster.md` section 5.

## Execution note (2026-11-20)

In this run the orchestrator session had no `Agent` tool (spawn depth/tool limit) and no specialist was reachable over `SendMessage`. Every task below was therefore executed by the orchestrator **acting in the owner's role**, following that owner's agent file, preloaded skills and `knowledge/<agent>/` notes. Ownership, reviewers and gates are unchanged; the owners should review their files on the next pass (see "Owner review queue").

## Environment facts (verified in the sandbox, 2026-11-20)

| Fact | Evidence |
|---|---|
| Python 3.12.x available (`/usr/bin/python3.12`), default `python3` is 3.13 | `python3.12 -m venv` succeeded |
| PyPI, npm registry, github.com releases, raw.githubusercontent.com reachable | `curl` range requests returned 206 |
| cdn.jsdelivr.net blocked | `curl` returned 000 |
| Pyodide full distribution = 337 MB; npm `pyodide@314.0.8` core = 13.9 MB unpacked | GitHub release `Content-Length`; npm `dist.unpackedSize` |
| Dataset: 200 real Yelp Review Full rows (100 train + 100 test, row_idx 0-99) | `data/raw/README.md` |

## Decisions

- D1. Dataset: Yelp Review Full ("restaurant/business mode"); Amazon Reviews 2023 is unreachable from the sandbox.
- D2. Self-hosted Pyodide: core files from the npm tarball (sha512 checked), nltk + pure-Python deps from PyPI wheels (sha256 checked), a same-origin `regex` shim. Fetched at build time by `scripts/fetch_pyodide.py`; `site/pyodide/` is generated-only (gitignored).
- D3. `site/data/*.json`, `site/nltk_data/`, `site/py/` are generated-only (gitignored); the Netlify build regenerates them.
- D4. Data contract v1.0.0 approved (gate 1), see `docs/data-contract.md`.
- D5. Live tab = NLTK only (Pyodide). spaCy output only for dataset reviews and `examples.json` (netlify-guardrail S05).

## Checklist

### Design
- [x] Gate 1: `docs/data-contract.md` + `schemas/*.schema.json` (owner BUILD, approved ORC)

### Build
- [x] DATA: `data/reviews_sample.jsonl`, `data/entity_patterns.jsonl`, `data/SOURCES.md`, `scripts/curate_sample.py`
- [x] NLTK: `nlp/nltk_analyzer.py`, `nltk_data/`
- [x] SPACY: `nlp/spacy_analyzer.py`
- [x] BUILD: `pipeline/build.py`, `requirements.txt`, `requirements-dev.txt`, `data/demo_reviews.jsonl`
- [x] PYO: `site/worker.mjs`, `site/pyodide-setup.mjs`, `scripts/fetch_pyodide.py`, `site/vendor-py/regex/`
- [x] UI + VIZ: `site/index.html`, `site/styles.css`, `site/app.js`, `site/charts.js`, `scripts/fetch_vendor_js.py`
- [x] NET: `netlify.toml`, `.gitignore`

### Test
- [x] QA: `tests/` (pytest unit, golden, schema, sizes, guardrails; Node Pyodide parity; Playwright e2e), `tests/support/serve_netlify.py`, `package.json`
- [x] EVAL: `reports/evaluation.md`, `scripts/evaluate.py`
- [x] Gate 2 (local): full build + pytest + Playwright green (deploy-preview run pending, needs Netlify)

### Deploy
- [x] DOC: `README.md`
- [ ] NET: first Netlify deploy preview, build log check (needs Netlify account access; not possible from the sandbox)
- [ ] QA: Playwright against the deploy preview URL
- [ ] ORC: production go/no-go

## Gate evidence

- **Gate 1 (contract):** `docs/data-contract.md` v1.0.0 + `schemas/*.schema.json`; `tests/test_schema.py` validates every generated file. Approved by ORC 2026-11-20.
- **Gate 2 (quality, local):** fresh `git clone` + new Python 3.12.3 venv from `requirements-dev.txt`, then the exact `netlify.toml` build command (`python pipeline/build.py && python scripts/fetch_pyodide.py`): build 7.2 s, `site/` data 0.9 MB, Pyodide 15.25 MB (largest file 9.60 MB). `pytest`: 57 passed. `npm run test:pyodide`: 3 passed (197/197 reviews identical between browser and build). `npm run test:e2e`: 5 passed. `npm run test:e2e:netlify-headers`: 5 passed. `reports/evaluation.md` has numbers. **Pending:** the same e2e run against a real deploy preview (`E2E_BASE_URL=...`).
- **Fixes found by the gates:** duplicate `.wasm` Content-Type from overlapping header rules (NET, fixed + guard test); hidden filter chip still visible (UI); model-number regex missed `WH-1000XM5` (DATA); classifier adjectives in `amod` pairs (SPACY) and missing food words in VADER (NLTK) from EVAL.

## Owner review queue

Each owner reviews the files listed against their checklist above on their next run.

## Blockers

| Blocker | Unblocks | Fallback |
|---|---|---|
| No Netlify credentials in sandbox | NET (deploy preview), QA (preview e2e) | Local parity: same build command, `python -m http.server -d site`, Playwright locally |
