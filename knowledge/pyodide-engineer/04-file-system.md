# 04 - Pyodide file system (pyodide.FS / Emscripten FS)

Sources:
- https://pyodide.org/en/stable/usage/file-system.html
- https://pyodide.org/en/stable/usage/api/js-api.html (FS, mountNativeFS, unpackArchive)
- Emscripten FS API referenced by the page: https://emscripten.org/docs/api_reference/Filesystem-API.html (not fetched; function behaviours below beyond the Pyodide page are marked unverified)

Fetched: 2026-11-20 (docs version 314.0.8)

## Basics

- Pyodide ships an Emscripten virtual file system. In JS it is `pyodide.FS`, which "re-exports the Emscripten File System API". `pyodide.PATH` aliases the Emscripten Path API.
- Default file system is **MEMFS**: in-memory; **data is lost when the page is reloaded**. The worker's FS is separate from the main thread's.
- Python and JS see the same files.

### Read/write examples (from the docs)
```js
// Python writes, JS reads
pyodide.runPython(`
  from pathlib import Path
  Path("/hello.txt").write_text("hello world!")
`);
let file = pyodide.FS.readFile("/hello.txt", { encoding: "utf8" });

// JS writes, Python reads
pyodide.FS.writeFile("/hello.txt", "hello world!", { encoding: "utf8" });
pyodide.runPython(`
  from pathlib import Path
  print(Path("/hello.txt").read_text())
`);
```
- `FS.writeFile(path, data, opts)` accepts a string (with `{encoding:"utf8"}`) or a `Uint8Array` for binary (the binary form is used in docs/05 of this repo; standard Emscripten behaviour, unverified on this page).
- `FS.mkdirTree(path)` creates nested directories (used by the docs' mount example). `FS.mkdir`, `FS.readdir`, `FS.stat`, `FS.unlink`, `FS.rmdir` are standard Emscripten FS calls (unverified here).
- `FS.writeFile` fails if the parent directory does not exist: call `mkdirTree` first.

## Getting remote files into the FS (fetch then write)

Typical pattern (assembled from the docs' API; the docs page itself does not show fetch):
```js
const res = await fetch("/nltk_data/sentiment/vader_lexicon.zip");
if (!res.ok) throw new Error("fetch failed " + res.status);
const bytes = new Uint8Array(await res.arrayBuffer());
pyodide.FS.mkdirTree("/nltk_data/sentiment");
pyodide.FS.writeFile("/nltk_data/sentiment/vader_lexicon.zip", bytes);
```
- Alternative: `pyodide.unpackArchive(buffer, format, {extractDir})` unpacks an archive (e.g. `"zip"`, `"tar"`, `"gztar"`) directly into a target directory. Signature: `unpackArchive(buffer: ArrayBuffer | TypedArray, format: string, options?: {extractDir})`. Useful to ship one `nltk_data.zip` and unpack to `/nltk_data`.
- Alternative in Python: `from pyodide.http import pyfetch`; `resp = await pyfetch(url); await resp.bytes()` (pyodide.http API exists; not fetched here, unverified).
- Use absolute paths and a same-origin URL (relative `/nltk_data/...`) to avoid CORS; Netlify serves `site/` files directly.

## Mounting other file systems

Other Emscripten file systems: `IDBFS`, `NODEFS`, `PROXYFS`, `WORKERFS` (some work only in specific runtimes).

- **Persist across reloads (IndexedDB)** from the docs:
  ```js
  let mountDir = "/mnt";
  pyodide.FS.mkdirTree(mountDir);
  pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, mountDir);
  ```
  IDBFS needs explicit `pyodide.FS.syncfs(populate, callback)` calls to load from / flush to IndexedDB (standard Emscripten behaviour; the docs show `pyodide.FS.syncfs(false, callback_func)` in the native-FS section).
- **Node only:** `pyodide.FS.mount(pyodide.FS.filesystems.NODEFS, {root: "."}, "/mnt")` or `pyodide.mountNodeFS(emscriptenPath, hostPath)`.
- **Browser native directory (experimental, File System Access API):** `const nativefs = await pyodide.mountNativeFS("/mount_dir", dirHandle);` requires `showDirectoryPicker()` and readwrite permission; changes are not synchronized automatically: call `await nativefs.syncfs()`. Not relevant for a static Netlify site.

## Python-side notes

- Normal `open()`, `pathlib`, `os` work on the virtual FS.
- Current working directory defaults to the Pyodide home dir (not specified on the fetched page; use absolute paths).

## Project application

- NLTK data must be present in the worker FS before `SentimentIntensityAnalyzer()` / `word_tokenize` run. Plan:
  1. Build step copies `nltk_data` pieces into `site/nltk_data/` (served statically).
  2. Worker: `fetch` each file, `FS.mkdirTree`, `FS.writeFile` under `/nltk_data/<category>/...`.
  3. Python: `import nltk; nltk.data.path.insert(0, "/nltk_data")`.
- NLTK looks for `sentiment/vader_lexicon.zip` (or unzipped folder), `corpora/stopwords.zip`, `tokenizers/punkt_tab/` ; NLTK can read zipped data via `nltk.data.find`. If a zip layout causes `LookupError`, unpack with `pyodide.unpackArchive(buf, "zip", {extractDir: "/nltk_data/corpora"})` (NLTK zips contain a top-level folder, e.g. `stopwords/`).
- Keep the lexicon payload small: only fetch what is needed (vader lexicon, punkt_tab for English, stopwords english).
- MEMFS is lost on reload; either re-fetch (browser HTTP cache makes this cheap) or mount IDBFS if repeated cold-start fetch is a problem (optional).
