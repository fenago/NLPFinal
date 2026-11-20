# 05 - Downloading and deploying Pyodide (CDN, self-hosting, versions)

Sources:
- https://pyodide.org/en/stable/usage/downloading-and-deploying.html
- https://pyodide.org/en/stable/usage/index.html
- https://pyodide.org/en/stable/usage/quickstart.html

Fetched: 2026-11-20

## Current stable version

**Pyodide 314.0.8** (the docs site header and "stable" alias show Version 314.0.8; version list: 314.0.0 ... 314.0.8, then the 0.29.x line). Versioning changed from 0.x.y to a scheme starting with 314.x (the "314" matches the Python 3.14 line; the mapping is inferred from docs/05 of this repo, not stated on the fetched page).

Package versions in this release (packages page): nltk 3.9.4, numpy 2.4.6, micropip 0.11.1. spaCy is not included.

## CDN (jsDelivr)

| channel | indexURL | comments |
|---|---|---|
| Latest release | `https://cdn.jsdelivr.net/pyodide/v314.0.8/full/` | Recommended, cached by the browser |
| Dev (`main`) | `https://cdn.jsdelivr.net/pyodide/dev/full/` | re-deployed per commit, no caching, testing only |

- Format: `https://cdn.jsdelivr.net/pyodide/v<version>/full/<file>`; build variants per version: `<version>/full/` (default) and `<version>/debug/` (unminified `pyodide.asm.mjs`).
- Script tag: `https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.js`; ES module: `.../full/pyodide.mjs`.
- **Always pin the version** (`v314.0.8`) rather than `latest`/`dev`; stable moves and package versions change.
- Do not confuse with the npm mirror `cdn.jsdelivr.net/npm/pyodide@x/` (runtime only, no wheels).
- Note: the build task environment may be unable to reach jsDelivr with curl; browsers can.

## Self-hosting

Downloads from GitHub releases (https://github.com/pyodide/pyodide/releases):
- `pyodide-314.0.8.tar.bz2`: full distribution with all vendored packages, **"quite large (200+ megabytes)"**. Too big to commit or deploy as-is on Netlify; trim it.
- `pyodide-core-314.0.8.tar.bz2`: minimal files needed to start Pyodide (same set `npm install pyodide` installs); intended for node, which fetches missing packages from the CDN.
- "You will need to serve these files yourself."

Files in the core bundle (all required to start): `pyodide.asm.mjs`, `pyodide.asm.wasm`, `pyodide.js`, `pyodide.mjs`, `python_stdlib.zip`, `pyodide-lock.json` ("Necessary in all cases"; the lockfile used by loadPackage/micropip), `package.json`, `python`, `python_cli_entry.mjs`.
Extra files in the full bundle: `*.whl` (package wheels), `*.metadata` (PEP 658), `*.zip` (shared libraries), `*-tests.tar`, `fonts/`, `ffi.d.ts`, `pyodide.d.ts`, `console.html`, source maps.

Serving locally: from the distribution folder run `python -m http.server`, open `http://localhost:8000/console.html`.

### Minimal self-hosted layout for this project (derived; verify before relying)
- Copy the core files above, plus from the full bundle only: the `nltk` wheel and the wheels it depends on (regex, click, joblib, tqdm, and their dependencies) and keep the full `pyodide-lock.json` (it lists all packages; pruning wheels while keeping the lock is OK as long as you never load the missing ones). Check `pyodide-lock.json` "nltk" entry `depends` to list exact wheels (unverified: not read here).
- In the worker: `loadPyodide({indexURL: "/pyodide/"})` and `import ... from "/pyodide/pyodide.mjs"`.
- Size check: core runtime is on the order of 10+ MB (unverified); nltk and deps add a few MB.

## Hosting requirements (remote deployments)

"Any service that hosts static files and that **correctly sets the WASM MIME type and CORS headers** will work. For instance, you can use GitHub Pages or similar." Further size/load-time tips: Emscripten deployment docs https://emscripten.org/docs/compiling/Deploying-Pages.html.
- WASM MIME type is `application/wasm` (standard; the page itself only says "WASM MIME type", so the exact string is unverified here). Required for streaming compilation; wrong type makes the browser fall back or fail.
- `.mjs` must be served with a JavaScript MIME type (`text/javascript`) for module scripts/workers (general browser rule; unverified on this page).
- CORS: needed when files come from another origin (CDN). Same-origin Netlify serving needs no CORS headers.
- Netlify specifics (derived, check Netlify docs): Netlify serves `.wasm` as `application/wasm`; if a `_headers`/`netlify.toml` rule is needed use e.g. `Content-Type = "application/wasm"` for `/pyodide/*.wasm`, and a long `Cache-Control` for versioned paths.

## CDN vs self-host decision

| | CDN (jsDelivr) | Self-host in `site/pyodide/` |
|---|---|---|
| Setup | one URL | copy files at build, manage size |
| Offline/grading risk | depends on jsDelivr | none beyond Netlify |
| Cache | shared across sites | per-site |
| Netlify bandwidth | none | counts against plan |
| Deploy size | tiny | tens of MB |

Recommendation for the grading deadline: CDN with a pinned version, plus a documented fallback path to self-host.

## Project application

- Single constant for version/base URL, e.g. `const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v314.0.8/full/";` used for both the module import and `indexURL`.
- Update `docs/05-netlify-architecture.md` sketch: use module worker + `pyodide.mjs` (see 03-web-worker.md).
- If CSP headers are added in `netlify.toml`, allow `cdn.jsdelivr.net` for `script-src`/`connect-src`, `'wasm-unsafe-eval'` for WebAssembly compilation, and `worker-src` for the module worker (CSP knowledge is general, not from the Pyodide page; unverified).
