# Netlify Engineer Knowledge Index

Fetched: 2026-11-20. Source of truth: official Netlify docs (docs.netlify.com, `.md` versions) unless a note says otherwise. Anything not confirmed on a fetched page is marked "(unverified)".

Project context: Customer Review Analyzer static site on Netlify, no outside servers. Netlify build runs Python 3.12 (NLTK + spaCy) and writes static JSON into `site/`; the browser runs NLTK via Pyodide with self-hosted `.wasm`. See `/home/user/NLPFinal/docs/05-netlify-architecture.md`.

| File | Topic | Read when |
|---|---|---|
| 01-build-configuration.md | Build command, publish/base dir, UI vs `netlify.toml`, build env vars, read-only vars (`CONTEXT`, etc.) | Setting up or debugging the build settings |
| 02-python-version.md | Ubuntu 24.04 image, `PYTHON_VERSION`/`runtime.txt`/`Pipfile`, `requirements.txt`, dependency cache | Python version or pip install problems |
| 03-netlify-toml-reference.md | `[build]`, `[build.environment]`, `[context.*]`, `[[headers]]`, `[[redirects]]`, `[dev]` syntax | Writing or reviewing `netlify.toml` |
| 04-headers-and-caching.md | `_headers`, `[[headers]]`, caching defaults, `.wasm` content-type (unverified), Cache-Control | Serving Pyodide/wasm/JSON correctly |
| 05-functions-limits.md | Guardrail: Functions TS/JS/Go only, Edge TS/JS, Server Node; limits | Anyone proposing server code |
| 06-deploys-and-cli.md | Deploy previews, branch deploys, rollback, CLI (`netlify build/dev/deploy`), deploy logs | Releasing, rolling back, local parity |
| 07-build-limits.md | Build timeouts (forum-sourced), build cache, 10 MB file warning, 54,000 files/dir | Build slowness, big wasm/wheel files |

## Quick answers

- Python on Netlify: build time only, Ubuntu 24.04. Select with `PYTHON_VERSION = "3.12"` in `[build.environment]` (file 02).
- Dependencies: root `requirements.txt` auto-installed with pip (file 02).
- `netlify.toml` beats UI settings (files 01, 03).
- Only the publish directory (`site`) is deployed (file 01).
- No Python at runtime; no functions in this project (file 05).
- `.wasm` content-type and caching: verify after first preview deploy (file 04).
- Biggest known risk: files over 10 MB in the deploy (Pyodide wasm/wheels) (file 07).
- Roll back with "Publish deploy"; lock auto publishing while fixing (file 06).
- CLI: `netlify build`, `netlify dev`, `netlify deploy --prod --dir=site` (deploy does not build) (file 06).

## Pages that were NOT found / gaps

- No official docs page with a numeric build timeout was found; file 07 uses a Netlify Support forum guide (15 min build command, about 30 min overall) and marks it unverified.
- No official statement on `.wasm` MIME type or on whether `Content-Type` overrides apply to static files (file 04).
- Total deploy size cap and bandwidth/build-minute allotments (plan pages) were not fetched.
- Pipfile/runtime.txt vs `PYTHON_VERSION` precedence not stated (file 02).
