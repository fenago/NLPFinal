# 01 - Web Workers (MDN)

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers
- https://developer.mozilla.org/en-US/docs/Web/API/Worker/Worker

Fetched: 2026-11-20

## What a worker is
- Runs a named JS file in a background thread so the UI thread is not blocked. Workers can use `fetch()` and `XMLHttpRequest`.
- Runs in a different global context: `DedicatedWorkerGlobalScope` (dedicated) or `SharedWorkerGlobalScope`. Use `self`, not `window` (using `window` in a worker errors).
- Cannot touch the DOM or the parent page's objects. To change the UI, post a message back to the main script and update the DOM in its handler.
- Available inside workers: `Navigator`, `fetch()`, `Array/Date/Math/String`, `setTimeout()`/`setInterval()`, WebSockets, IndexedDB.
- Workers can spawn sub-workers (same origin only; sub-worker URIs resolve relative to the parent worker).

## Creating and messaging
```js
if (window.Worker) {            // feature detection (MDN suggestion)
  const myWorker = new Worker("worker.js");
}
```
Main thread:
```js
myWorker.postMessage([first.value, second.value]);   // "you can send pretty much anything"
myWorker.onmessage = (e) => { result.textContent = e.data; };
```
Worker (global scope, so no `myWorker.` prefix):
```js
onmessage = (e) => { postMessage(`Result: ${e.data[0] * e.data[1]}`); };
```
- Message data is in `event.data` of the `message` event.
- Data is COPIED (structured clone), not shared. Structured clone accepts JSON plus things JSON cannot (e.g. circular references).
- `myWorker.terminate()` kills the worker immediately.

## Worker() constructor
- `new Worker(url)` / `new Worker(url, options)`.
- `options.type`: `"classic"` (default) or `"module"`.
- `options.credentials`: `"omit"`, `"same-origin"` (default), `"include"` - only for importing modules into a module worker.
- `options.name`: name for the `DedicatedWorkerGlobalScope`.
- Can throw `NetworkError`, `SecurityError`, `SyntaxError` (DOMException) or `TypeError`.
- Module worker: `new Worker("worker_module.js", { type: "module" })`.
- Bundler note (MDN): `new Worker(new URL("worker.js", import.meta.url))`. Not needed for plain static HTML.

## Importing scripts (classic workers)
- `importScripts("a.js", "b.js")` is synchronous; scripts execute in the order listed; a load failure throws `NETWORK_ERROR` and later code does not run. Cross-origin URLs are allowed.
- Pyodide's loader is typically brought in this way in a classic worker: `importScripts("https://cdn.jsdelivr.net/pyodide/...")` (unverified, not on the fetched MDN pages; check Pyodide docs).
- With `type: "module"` use `import` statements instead (`importScripts` is not available in module workers - unverified here, widely documented elsewhere).

## Error handling
- Runtime error in the worker fires `onerror` on the `Worker` object with an `ErrorEvent`: `message`, `filename`, `lineno`. Event does not bubble, is cancelable (`preventDefault()`).
```js
worker.onerror = (error) => { console.log(`Worker error: ${error.message}`); };
```
- Errors you catch inside the worker should be posted back as a message (e.g. `{type:"error", message}`) so the UI can show them.
- `messageerror` event (data cannot be deserialized) is not covered on the fetched pages (unverified).

## Transferable objects and sharing
- Transferables move with zero-copy; the sender's copy becomes unusable:
```js
worker.postMessage(uInt8Array.buffer, [uInt8Array.buffer]);
```
- `SharedArrayBuffer` allows shared memory but has determinism/security concerns (MDN). Not needed here; review texts are small strings.

## Other facts
- CSP: workers have their own context and generally are NOT governed by the creating document's CSP; set a `Content-Security-Policy` header on the worker script response. Exception: `data:`/`blob:` worker scripts inherit the creator's CSP.
- `SharedWorker` needs a `port` and same exact origin; not useful for this single-page app.
- Debug: `chrome://inspect/`, `edge://inspect/`, `about:debugging#/runtime/this-firefox`.
- Embedded worker via `Blob` + `URL.createObjectURL(blob)` is possible but a separate file is simpler.

## Project application
- Put NLTK/Pyodide in `site/worker.js`; create ONE long-lived worker when the Analyze tab is first opened (cold start is slow), reuse it for every review.
- Define a tiny message protocol and keep it stable, for example:
  - UI -> worker: `{ id, type: "analyze", text }`
  - worker -> UI: `{ type: "status", stage }` (loading-pyodide, loading-nltk, ready), `{ id, type: "result", data }`, `{ id, type: "error", message }`
- Echo `id` so late results from an older request can be ignored.
- Wire `worker.onerror` to show a visible error and offer retry (create a new Worker).
- Results are plain JSON objects (clone-safe); convert Pyodide proxies with `.toJs()` / `JSON.stringify` inside the worker before `postMessage` (Pyodide detail, unverified here).
- Feature-detect `window.Worker`; if missing, disable the Analyze tab with an explanation.
