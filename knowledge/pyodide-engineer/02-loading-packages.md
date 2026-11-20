# 02 - Loading packages in Pyodide (loadPackage, micropip, packages built in)

Sources:
- https://pyodide.org/en/stable/usage/loading-packages.html
- https://pyodide.org/en/stable/usage/packages-in-pyodide.html
- https://pyodide.org/en/stable/usage/api/js-api.html (loadPackage, loadPackagesFromImports)

Fetched: 2026-11-20 (docs version 314.0.8)

## What is available at startup

"Only the Python standard library is available after importing Pyodide." Everything else is loaded by one of:

1. `micropip.install()` (Python, async): pure-Python wheels from PyPI, **plus** Pyodide packages (Emscripten/wasm32 binary wheels) from the JsDelivr CDN or other URLs. Does dependency resolution. Docs advice: "use micropip.install() for everything" except to load micropip itself or when optimizing for size.
2. `pyodide.loadPackage()` (JS, async): packages built with Pyodide (the official repo), less overhead, more limited. micropip uses it internally.
3. `pyodide.loadPackagesFromImports(code)`: scans Python source for imports and loads any known Pyodide-distribution package. It does **not** download from PyPI.

## pyodide.loadPackage

```js
await pyodide.loadPackage("numpy");
await pyodide.loadPackage(["cycler", "pytz"]);          // several at once
await pyodide.loadPackage("https://foo/bar/numpy-1.22.3-cp310-cp310-emscripten_3_1_13_wasm32.whl"); // custom URL
```
- Signature: `loadPackage(names: string | string[] | PyProxy, options)`; options `messageCallback(msg)`, `errorCallback(msg)`, `checkIntegrity` (boolean). Returns `Promise<PackageData[]>`.
- Requesting a package from the official repo also loads its dependencies. **No dependency resolution for custom URLs.**
- Loading the same package twice is not permitted (a custom URL with the same name may be loaded first to override a dependency).
- File name of a URL wheel must be a valid wheel name (PEP 427).

## micropip

```js
await pyodide.loadPackage("micropip");
const micropip = pyodide.pyimport("micropip");
await micropip.install("snowballstemmer");
```
Or in Python: `import micropip; await micropip.install("pkg")` (inside `runPythonAsync` for top-level await).
- Default index is PyPI; alternative indexes via the `index_urls` parameter.
- Wheel URL: `micropip.install("https://example.com/files/pkg-2.0.0-py2.py3-none-any.whl")`. micropip treats an argument as a URL if it ends in `.whl`. `deps=False` skips dependency installation.
- Integrity: wheels from PyPI are checked against hash digests from the PyPI JSON API. For arbitrary URLs integrity is not checked.
- **CORS:** a remote wheel server must send CORS headers; third-party CORS proxies have security implications.
- Which wheels work: pure Python (`py3-none-any`) and wasm32/emscripten binary wheels. A normal CPython wheel with C extensions (e.g. `cp312-manylinux...`) does **not** work.
- Latest micropip shown in docs: **0.11.1**.

## Packages built in Pyodide 314.0.8 (list page; relevant rows)

Text of the page: "These packages can be loaded with `pyodide.loadPackage()` or `micropip.install()`... Pure Python packages with wheels on PyPI can be loaded directly from PyPI with `micropip.install()`."

Verified rows from the stable page (full list is much longer):

| package | version |
|---|---|
| **nltk** | **3.9.4** |
| regex | 2026.3.32 |
| click | 8.3.1 |
| joblib | 1.5.3 |
| tqdm | 4.67.3 |
| numpy | 2.4.6 |
| pandas | 3.0.2 |
| scikit-learn | 1.8.0 |
| scipy | 1.18.0 |
| pyyaml | 6.0.3 |
| micropip | 0.11.1 |

Confirmed absent from the list: **spacy, thinc, blis, cymem, preshed, murmurhash, srsly**, textblob, gensim. (Absence was reported by the page extraction tool; spot-check visually if it matters.)

So: `loadPackage("nltk")` pulls nltk 3.9.4 plus its dependencies (click, joblib, regex, tqdm are all in-distribution, so no PyPI access is needed).

## spaCy in Pyodide

Not provided and no pure-Python wheel exists (it needs compiled Cython/C deps). Do not try `micropip.install("spacy")`. Anything spaCy-based must be computed at build time (see build-pipeline notes) or approximated in JS.

## Version skew to remember

- Build step (pip) may use nltk 3.10.x; the browser runs **nltk 3.9.4**. Data files and APIs used must work on both: `punkt_tab`, `stopwords`, `vader_lexicon` are fine on both (nltk 3.9+ uses `punkt_tab`). (Check `nltk.__version__` in the worker if behaviour differs.)

## Project application

- Worker setup sequence: `await pyodide.loadPackage("nltk")` (no micropip needed, saves size). Only fetch micropip if a pure-Python extra is added.
- Use `messageCallback` to surface "Loading nltk..." progress in the UI.
- Do not call `loadPackagesFromImports` on user text: user input could name arbitrary imports (it only loads from the Pyodide distribution, but it is needless work). Load packages explicitly.
- Pyodide's package wheels are served from the same `indexURL` as the runtime (CDN or self-hosted); with self-hosting you must include the nltk wheel and its dependency wheels plus `pyodide-lock.json` (see 05).
