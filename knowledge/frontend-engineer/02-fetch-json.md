# 02 - Fetch API and JSON (MDN)

Sources:
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- https://developer.mozilla.org/en-US/docs/Web/API/Response/json
- https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort
- https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static

Fetched: 2026-11-20

## Basic pattern (MDN)
```js
async function getData() {
  const url = "https://example.org/products.json";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const result = await response.json();
    console.log(result);
  } catch (error) {
    console.error(error.message);
  }
}
```
- `fetch()` rejects on network failure (and similar low-level errors); an HTTP error such as 404 or 500 does NOT reject. You must check `response.ok` / `response.status`.

## Response.json()
- Syntax: `response.json()`; returns a Promise resolving to the parsed value (object, array, string, number...).
- Rejects with:
  - `AbortError` (DOMException): request was aborted.
  - `TypeError`: body already used/locked ("disturbed"), or body could not be decoded (e.g. wrong `Content-Encoding`).
  - `SyntaxError`: body is not valid JSON (typical when a 404 HTML page or an SPA fallback `index.html` is returned instead of the JSON file).
- The body can be read only once; call `response.clone()` first if you need it twice (general Fetch behaviour, "disturbed" per MDN).

## AbortController / AbortSignal
- `const controller = new AbortController(); fetch(url, { signal: controller.signal }); controller.abort();`
- `abort()` or `abort(reason)`; `reason` can be any JS value; default reason is an `AbortError` DOMException. Aborts fetches, body consumption, or streams.
- `AbortSignal.timeout(ms)` returns a signal that aborts itself after `ms`:
```js
try {
  const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
  const result = await res.blob();
} catch (err) {
  if (err.name === "TimeoutError") { /* took longer than 5 s */ }
  else if (err.name === "AbortError") { /* aborted by user action / navigation */ }
  else if (err.name === "TypeError") { /* MDN: could be unsupported AbortSignal.timeout(), or network failure */ }
  else { console.error(`Error: type: ${err.name}, message: ${err.message}`); }
}
```

## Headers / POST (MDN)
```js
const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
await fetch("https://example.org/post", {
  method: "POST", headers: myHeaders, body: JSON.stringify({ username: "example" }),
});
```
(Our site only GETs static JSON; no POST needed.)

## Robust loader template (assembled from the above)
```js
async function loadJSON(path, { timeoutMs = 10000 } = {}) {
  const res = await fetch(path, { signal: AbortSignal.timeout(timeoutMs) });
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.json();   // may throw SyntaxError if not JSON
}
```

## Project application
- Dashboard JSON lives under `site/data/` (see docs/05-netlify-architecture.md). Use relative URLs (`data/sentiment.json`) so it works under any base path.
- Load all dashboard files in parallel with `Promise.allSettled([...loadJSON(...)])` so one missing file shows an error card for that panel instead of blanking the whole dashboard.
- Always check `response.ok`; a missing file on Netlify may return the 404 page (HTML) which makes `.json()` throw `SyntaxError` - catch and show "data file missing or malformed".
- Use a timeout signal so the loading state cannot spin forever; show a Retry button on failure.
- Show skeleton/loading state while pending (see 05-loading-states.md) and announce errors in a `role="status"`/`role="alert"` region (see 03-accessibility.md).
- Cache behaviour on Netlify (headers, `cache` option) is outside the fetched pages (unverified); keep JSON file names stable or add a version query string when data is regenerated.
