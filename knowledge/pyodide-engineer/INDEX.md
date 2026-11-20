# Pyodide engineer knowledge - index

Grounded in the official Pyodide docs (https://pyodide.org/en/stable/), fetched 2026-11-20. **Current stable: Pyodide 314.0.8** (bundled nltk 3.9.4; spaCy NOT included).

| File | Read it when |
|---|---|
| 01-getting-started.md | writing loadPyodide / runPython / runPythonAsync calls, passing data JS<->Python, avoiding PyProxy leaks |
| 02-loading-packages.md | loading nltk (`loadPackage`), deciding micropip vs loadPackage, confirming spaCy is unavailable |
| 03-web-worker.md | building the analyzer worker: module worker, postMessage id pattern |
| 04-file-system.md | putting NLTK data (vader_lexicon, punkt_tab, stopwords) into the worker FS |
| 05-downloading-deploying.md | choosing CDN URL vs self-hosting, WASM MIME/CORS, version pinning |

## Key facts (quick reference)

- CDN base: `https://cdn.jsdelivr.net/pyodide/v314.0.8/full/` (files `pyodide.mjs`, `pyodide.js`).
- Workers must be **module workers** (`new Worker(url, {type:"module"})`); `importScripts` classic workers are NOT supported. The sketch in `docs/05-netlify-architecture.md` section 4 must be updated accordingly.
- Python dict returned to JS is a Map/PyProxy; return `json.dumps(...)` strings instead.
- `pyodide.loadPackage("nltk")` gives nltk 3.9.4 plus regex/click/joblib/tqdm; build step may use a newer nltk, so keep API usage compatible with both.
- NLTK data is not in the nltk wheel: ship it in `site/nltk_data/` and write it into `pyodide.FS` before use; set `nltk.data.path`.

## Open items / unverified

- Exact `pyodide-lock.json` dependency list for the nltk wheel (needed for a minimal self-host).
- Exact on-the-wire size of the first load.
- Netlify header config for `.wasm` / `.mjs` MIME types (see build-pipeline-engineer notes and Netlify docs).
