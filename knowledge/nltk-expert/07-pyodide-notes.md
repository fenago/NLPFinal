# NLTK in Pyodide (browser)

Sources:
- https://pyodide.org/en/stable/usage/packages-in-pyodide.html (query extraction: version header and table rows)
- https://www.nltk.org/data.html
- https://www.nltk.org/api/nltk.data.html
- https://www.nltk.org/api/nltk.downloader.html

Fetched: 2026-11-20

## What was verified
- The Pyodide docs page "Packages built in Pyodide" is titled **Version 314.0.8** (stable).
- Package table rows seen: `nltk 3.9.4`, `numpy 2.4.6`, `pandas 3.0.2`, `regex 2026.3.32`, `scikit-learn 1.8.0`.
- No `spacy` row appeared on the page (matches the project architecture: spaCy cannot run in the browser).
- Loading: "These packages can be loaded with `pyodide.loadPackage()` or `micropip.install()`." Pure-Python wheels on PyPI can be loaded directly with `micropip.install()`. See https://pyodide.org/en/stable/usage/loading-packages.html (not fetched).
- Version mismatch to remember: the build-time NLTK (PyPI, project docs say 3.10.4) is newer than Pyodide's 3.9.4. Pin build-time code to APIs present in both (everything in notes 01-05 is long-standing), and pin or test the build-time version against 3.9.4 for identical VADER output.

## Loading NLTK in the page (typical pattern)
```js
const pyodide = await loadPyodide();
await pyodide.loadPackage(["nltk", "regex"]);   // regex is a listed package; nltk imports it
```
- `loadPackage("nltk")` resolves dependencies automatically for packages in the Pyodide distribution (general Pyodide behaviour; the exact dependency resolution was not shown on the fetched page: unverified).
- `micropip.install("nltk")` alternative would pull from PyPI (a newer, possibly different version); prefer the prebuilt one for compatibility.

## Getting NLTK data into Pyodide (key constraint)
- `nltk.download()` fetches an index from `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml` over the network (downloader docs). Whether this works from a browser (CORS, sync network APIs, `urllib` in WASM) was not verified; do not rely on it (unverified).
- Reliable approach: ship the needed data as static files on Netlify and write them into Pyodide's virtual filesystem, then add that directory to `nltk.data.path` (list of search directories; or set `NLTK_DATA`):

```python
import nltk
nltk.data.path.insert(0, "/nltk_data")
# files written beforehand, e.g. with pyodide.FS.writeFile / unpackArchive:
# /nltk_data/corpora/stopwords/english
# /nltk_data/sentiment/vader_lexicon.zip   (SentimentIntensityAnalyzer reads sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt)
# /nltk_data/tokenizers/punkt_tab/english/...   (folder layout inferred: unverified)
nltk.data.find("sentiment/vader_lexicon.zip")
```
- `pyodide.unpackArchive(buffer, "zip", {extractDir: "/nltk_data/..."})` is a standard Pyodide API (not on fetched pages: unverified here) for unzipping data fetched with `fetch()`.
- Data lookups raise `LookupError` when files are missing (nltk.data.find docs), so test the path before analyzing.

## Practical guidance
- Keep the browser payload small: only `vader_lexicon`, `stopwords` (or an inlined stopword list), and the Punkt parameters if sentence splitting is needed. Avoid importing Matplotlib (`FreqDist.plot`) or heavy corpora.
- If Punkt data is a hassle in the browser, use a regex-based splitter (`RegexpTokenizer` with a sentence-ish pattern) and `TweetTokenizer` (both are data-free) in the live path, accepting small differences from build-time results (document it).
- Initialize Pyodide once, cache the `SentimentIntensityAnalyzer`, and run in a Web Worker so the UI stays responsive (general practice).
- Pyodide's first load downloads the runtime plus packages (many MB); show a loading state.

## Project application
- Architecture (docs/05): full NLTK + spaCy runs at build time to static JSON; live "analyze your review" uses NLTK only in Pyodide. This page's constraints decide what the live path can call: tokenizers (`TweetTokenizer`, `RegexpTokenizer`), VADER, stopwords, `FreqDist` -- all pure Python.
- Ensure the live scorer and the build-time scorer share one module and one stopword set/negation list so numbers match.
- Check Pyodide's NLTK version at integration time (currently 3.9.4); the version moves with Pyodide releases.
