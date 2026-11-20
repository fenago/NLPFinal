# 04 - Custom headers and caching

Sources:
- https://docs.netlify.com/manage/routing/headers.md
- https://docs.netlify.com/build/caching/caching-overview.md
- https://docs.netlify.com/build/configure-builds/file-based-configuration.md

Fetched: 2026-11-20

## Two ways to set custom headers

1. A plain-text `_headers` file saved in the **publish directory**.
2. `[[headers]]` tables in `netlify.toml`.

### `_headers` syntax

```
# comment
/path/or/pattern
  Header-Name: value
  Another-Header: value
```
- Lines starting with `#` are comments. Names are case-insensitive. Paths may use wildcards/placeholders.
- The file must end up in the folder that is deployed (so the build script must write/copy `_headers` into `site/`).
- Multi-value: repeat the same header name on several lines; Netlify concatenates with commas.

### `netlify.toml` syntax

```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
```
Keywords: `for`, `values`. Multi-value headers use multi-line strings (see file 03).

## Path patterns

- `*` wildcard can appear anywhere within a path segment.
- `:placeholder` only at the **start** of a segment; matches anything except `/`.
- A wildcard and a placeholder cannot be in the same segment (`/templates/:placeholder*` is invalid).
- Header wildcards/placeholders behave differently from redirect splats.

## Limitations (important)

- Custom headers apply **only to files served from Netlify's own backing store** (i.e. static files). Not applied to proxied content, Functions or Edge Functions responses.
- Headers in `_headers` or `netlify.toml` are **global for all deploy contexts**; they cannot be scoped per branch/context directly. Workaround: keep per-context header files elsewhere and copy one to `<publish>/_headers` in the context's build command (e.g. `command = "npm run build && cp ./custom-headers/_stagingHeaders ./dist/_headers"`).
- These headers are ignored if you try to set them (server controls them): `Accept-Ranges`, `Age`, `Allow`, `Alt-Svc`, `Connection`, `Content-Encoding`, `Content-Length`, `Content-Range`, `Date`, `Location`, `Server`, `Set-Cookie` (may be overridden), `Trailer`, `Transfer-Encoding`, `Upgrade`.
- Notably `Content-Encoding` and `Content-Length` cannot be customized, so you cannot hand-set gzip/brotli encoding on a file via headers.
- Basic-auth headers are Pro/Enterprise only and disable caching for the entire website.

## Content-Type for `.wasm` (and other types)

- The fetched headers page does **not** document default MIME types or `.wasm` handling. `Content-Type` is not in the list of ignored headers, so it can in principle be set per path (unverified for overriding).
- (unverified) Netlify's CDN is widely reported to serve `.wasm` as `application/wasm`. Verify after the first preview deploy with `curl -I https://<preview>/path/to/file.wasm` and check `content-type`. Browsers need `application/wasm` for streaming compilation (`WebAssembly.instantiateStreaming`); otherwise it falls back or fails.
- If a fix is needed, add:

```toml
[[headers]]
  for = "/*.wasm"
  [headers.values]
    Content-Type = "application/wasm"
```
(unverified that a `Content-Type` override is honored for static files; test it.)

## Caching defaults (static assets)

- Static assets are cached on Netlify's global edge and **auto-invalidated on every new deploy** (atomic deploys). The deploy-context cache is invalidated per context (a Deploy Preview deploy only invalidates that preview).
- Docs: unless there is a new deploy or manual purge, static asset responses are treated as fresh for **up to one year** at Netlify's CDN, and Netlify "ignore[s] any attempts to set cache control headers with a shorter `max-age`" for its own edge cache.
- Default headers for static assets if you set none:
  - `Netlify-CDN-Cache-Control: public, s-maxage=31536000, must-revalidate`
  - `Cache-Control: public, max-age=0, must-revalidate`
  So browsers revalidate each time (cheap 304s), the edge serves from cache, and a new deploy updates content immediately.
- Header precedence: `Netlify-CDN-Cache-Control` > `CDN-Cache-Control` > `Cache-Control` for Netlify's edge; `CDN-Cache-Control` and `Cache-Control` are always passed downstream to browsers.
- Supported directives: `public`, `private`, `no-store`, `s-maxage`, `max-age`, `stale-while-revalidate`, `durable` (functions only).
- `Cache-Status` response header (RFC 9211) shows edge behavior: `"Netlify Edge"; hit` / `fwd=miss`. Make several requests when debugging; each request may land on a different cache instance.
- Purge: by site or cache tag through `purgeCache` helper (functions) or `POST https://api.netlify.com/api/v1/purge` with a personal access token. Not needed for a static site because each deploy invalidates automatically.

## Recommended cache strategy for this project (derived from the above, not a docs quote)

| Path | Suggested header | Why |
|---|---|---|
| `/data/*.json` | `Cache-Control: public, max-age=3600` (from docs/05) or default | Data changes per deploy; edge is auto-invalidated anyway |
| Pyodide/NLTK `.wasm`, `pyodide*.js`, `*.whl`, `nltk_data/*` | `Cache-Control: public, max-age=31536000, immutable` only if filenames are versioned/hashed; otherwise leave default | Big files; browsers should not re-download on every visit |
| `index.html`, app JS | default (`max-age=0, must-revalidate`) | Always fresh after deploy |

(unverified) How the browser-side `max-age` interacts when Netlify says edge-side freshness is one year: the docs state the edge ignores shorter `max-age`; they do not state that a longer `max-age` is overridden for browsers, and `Cache-Control` is passed downstream.

## Project application

- Put `[[headers]]` in `netlify.toml` (single source of truth) or write `_headers` into `site/` from `pipeline/build.py`; avoid doing both for the same path (precedence unverified).
- Self-hosted Pyodide `.wasm`: after first deploy run `curl -sI` on each `.wasm` and `.whl`/`.zip`/`.json` to confirm `content-type` and `cache-control`. Add the `[[headers]]` block above only if wrong.
- Do not set `Content-Encoding` yourself (ignored); let Netlify compress text assets. Whether Netlify compresses `.wasm` automatically is not documented on the fetched pages (unverified).
- No functions/edge functions are used, so the "headers do not apply to functions" limitation does not bite.
