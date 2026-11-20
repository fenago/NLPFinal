# 03 - Pyodide in a web worker (official pattern)

Sources:
- https://pyodide.org/en/stable/usage/webworker.html
- https://pyodide.org/en/stable/usage/index.html (Web Workers section)

Fetched: 2026-11-20 (docs version 314.0.8)

## Critical rule (differs from older tutorials and from the sketch in docs/05)

Official note: "Pyodide requires a **module-type worker** because `pyodide.asm.mjs` is an ES module. **Classic workers using `importScripts()` are not supported.**"

So the `importScripts("https://cdn.jsdelivr.net/pyodide/v.../pyodide.js")` snippet in `docs/05-netlify-architecture.md` section 4 is outdated for this version. Use `new Worker(url, {type: "module"})` and an ES `import` of `pyodide.mjs` inside the worker.

## Why a worker

- WebAssembly runs on the main thread by default; long Python computations make the UI unresponsive.
- A worker runs Python in a separate thread. Trade-offs: no shared globals with the main thread, and a worker cannot touch the DOM. Communicate by messages only.

## The official three-part pattern (no Comlink)

1. **Consumer** (main thread) calls `asyncRun(script, context)` and awaits `{result, error}`.
2. **Worker API** (`workerApi.mjs`) wraps `postMessage` in a promise using a per-message `id`.
3. **Web worker** (`webworker.mjs`) loads Pyodide once and runs scripts.

### Worker (verbatim from the docs, version-pinned CDN import)
```js
// webworker.mjs
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.mjs";

let pyodideReadyPromise = loadPyodide();

self.onmessage = async (event) => {
  // make sure loading is done
  const pyodide = await pyodideReadyPromise;
  const { id, python, context } = event.data;
  // Now load any packages we need, run the code, and send the result back.
  await pyodide.loadPackagesFromImports(python);
  // make a Python dictionary with the data from `context`
  const dict = pyodide.globals.get("dict");
  const globals = dict(Object.entries(context));
  try {
    // Execute the python code in this context
    const result = await pyodide.runPythonAsync(python, { globals });
    self.postMessage({ result, id });
  } catch (error) {
    self.postMessage({ error: error.message, id });
  }
};
```

### Worker API (verbatim logic)
```js
// workerApi.mjs
function getPromiseAndResolve() {
  let resolve;
  let promise = new Promise((res) => { resolve = res; });
  return { promise, resolve };
}
let lastId = 1;
function getId() { return lastId++; }

function requestResponse(worker, msg) {
  const { promise, resolve } = getPromiseAndResolve();
  const idWorker = getId();
  worker.addEventListener("message", function listener(event) {
    if (event.data?.id !== idWorker) return;
    worker.removeEventListener("message", listener);
    const { id, ...rest } = event.data;
    resolve(rest);
  });
  worker.postMessage({ id: idWorker, ...msg });
  return promise;
}

const pyodideWorker = new Worker("./webworker.mjs", { type: "module" });

export function asyncRun(script, context) {
  return requestResponse(pyodideWorker, { context, python: script });
}
```

### Consumer
```js
import { asyncRun } from "./workerApi.js";
const script = `
    import statistics
    statistics.stdev(A_rank)
`;
const context = { A_rank: [0.8, 0.4, 1.2, 3.7, 2.6, 5.8] };
const { result, error } = await asyncRun(script, context);
```

## Key mechanics

- `loadPyodide()` is started at worker top level and stored as `pyodideReadyPromise`; every message `await`s it, so early messages queue safely.
- Every request carries an `id`; the reply echoes it, so concurrent requests resolve correctly.
- `context` values are structured-cloned by postMessage, then turned into a Python dict: `dict(Object.entries(context))` (the JS object entries pass as the `globals` for that run, isolating each call's variables).
- Errors: wrap `runPythonAsync` in try/catch and post `error.message`; PyodideErrors surface as JS `Error` with the Python traceback in the message.
- Results that are PyProxy cannot be structured-cloned through postMessage: convert (`toJs`) or return primitives/JSON strings. Primitives like numbers/strings pass fine.
- Interrupting long Python: `pyodide.setInterruptBuffer(sab)` with a `SharedArrayBuffer`; writing `2` (SIGINT) raises `KeyboardInterrupt`. SharedArrayBuffer needs cross-origin isolation headers on the page (COOP/COEP) (the isolation requirement is general web-platform knowledge, not from this page). Simplest alternative: terminate and recreate the worker.
- Pyodide in a **service worker** is also documented (https://pyodide.org/en/stable/usage/service-worker.html), not needed here.

## Project application

- Files: `site/js/analyze-worker.mjs` (module worker) and a small main-thread wrapper like `workerApi.mjs`. Start the worker with `new Worker("/js/analyze-worker.mjs", {type: "module"})`.
- Replace the generic "run any script" pattern with a fixed protocol, e.g. messages `{id, type: "analyze", text}` and replies `{id, ok, data}` / `{id, ok:false, error}`, plus progress messages `{type:"status", message}` during load (loadPackage `messageCallback`).
- Do not run arbitrary user code: only pass the review text as data (`context`/function argument), never as part of the script string.
- Import `pyodide.mjs` from the CDN URL pinned to the version, or from a self-hosted `/pyodide/` folder (module workers can `import` same-origin URLs; with a self-hosted copy also pass `indexURL`).
- Module workers need a browser supporting them; official tested minimums are Chrome 112 / Firefox 112 / Safari 16.4, which all support them.
- Show a loading state: first load downloads the runtime (~10 MB+ per docs/05, unverified here) plus the nltk wheels.
