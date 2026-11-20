# Orchestrator memory (Atlas)

## 2026-11-20: first full build
- Session had no Agent tool and no reachable specialists: work was done in each owner's role and recorded in docs/plan.md. Next run: ask owners to review their files (plan "Owner review queue").
- Dataset: Yelp Review Full, 200 raw rows -> 197 kept. Amazon 2023 not reachable from the sandbox.
- Browser NLTK = PyPI nltk 3.10.4 wheel unpacked into Pyodide 314.0.8 (npm core), not Pyodide's nltk 3.9.4 (CDN blocked; full dist is 337 MB). Same version as the build -> parity test is exact.
- NLTK 3.10 gotchas in Pyodide: every regex goes through nltk.redos -> needs `regex` (shim in site/vendor-py, translates \p{L}\p{N}); nltk/pathsec.py calls os.geteuid (alias to getuid) and refuses world-writable data dirs (chmod /nltk_data 0755/0644). Do not disable pathsec.
- Netlify headers: never let two [[headers]] rules set the same header for one path (duplicate Content-Type broke wasm). Pyodide lives in versioned site/pyodide/v<ver>/ so immutable caching is safe.
- Python Playwright 1.65 has no matching browser here; use Node Playwright 1.63 (PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers, NODE_PATH=$(npm root -g)). `node --test` needs glob patterns, not directories.
- Eval baseline: VADER 60.9% acc / 0.430 macro-F1; entity P 64.7% (ruler) vs 62.7%; aspect pair P 83% after amod-valence filter (43% before).
