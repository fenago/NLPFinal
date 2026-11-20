# 05 - Functions, Edge Functions, Netlify Server: limits and why this project uses none

Sources:
- https://docs.netlify.com/build/functions/overview.md
- https://docs.netlify.com/build/functions/configuration.md
- https://docs.netlify.com/build/functions/get-started.md
- https://docs.netlify.com/build/edge-functions/limits.md
- https://docs.netlify.com/build/server.md
- https://docs.netlify.com/llms.txt (page descriptions)

Fetched: 2026-11-20

GUARDRAIL: This is a reference to explain why the project has **no Netlify Functions, Edge Functions, Background/Scheduled Functions or Netlify Server**. Do not add `netlify/functions/`, `[functions]` in `netlify.toml`, or any "call a function that runs Python" design.

## Supported languages (Functions)

- The functions overview and configuration pages show **TypeScript**, **JavaScript** and **Go** tabs only. llms.txt describes "Get started with Functions" as: "Create functions source files in TypeScript and JavaScript". Go uses the Lambda-compatible API ("To write functions in Go, use the Lambda-compatible functions API").
- **Python is not a supported function language** on any fetched page. Inference (not an explicit docs sentence): a Python function file will not be built or run. The build environment has Python; the function runtime does not (see below).
- Functions deploy from `netlify/functions` (default, relative to base) or `[functions] directory = "..."`.
- Node.js functions runtime follows the build's Node version (if a valid AWS Lambda runtime) else fallback Node.js 24; override with `AWS_LAMBDA_JS_RUNTIME` (set in UI/CLI/API, not `netlify.toml`).

## Functions limits (configuration page, same for TS/JS/Go)

| Setting | Value | Configurable |
|---|---|---|
| Synchronous execution limit | 60 seconds | No |
| Scheduled execution limit | 30 seconds | No |
| Background execution limit | 15 minutes | No |
| Buffered request/response payload | 6 MB (binary uploads are Base64, about 30% overhead, so effectively about 4.5 MB) | No |
| Streamed response payload | 20 MB | No |
| Background request/response payload | 256 KB | No |
| Memory | 1024 MB default; 1024 to 4096 MB via `memory` or `vcpu` 0.5 to 2.0 (credit-based Pro/Enterprise only) | Yes |
| Default region | `cmh` (US East, Ohio); changing region is Pro/Enterprise | Yes |

Routing: default URL `/.netlify/functions/<name>`; custom paths via `config.path` (TS/JS) or `[[redirects]]` (Go).

## Edge Functions limits

- Runtime: TypeScript/JavaScript only (the "Deno-based" detail comes from docs/05, not re-verified on the limits page).
- Code size: **20 MB after compression**.
- Memory per set of deployed edge functions: 512 MB.
- CPU execution time per request: **50 ms**.
- Response header timeout: 40 s.
- Invocation quotas vary by plan.
- Custom headers (`_headers` / `[[headers]]`) do not apply to edge-function responses; split testing disables them; they cannot rewrite to external sites (use `fetch`).

## Netlify Server

- Early Access. "Run your application's backend as a long-lived **Node.js** server" (Express, Fastify, Hono, Koa or a handler). Entry file `netlify/server/index.ts` (or `.mts`, `.js`, `.mjs`). Up to 3 instances (1 on Free/Personal); scales to zero after about 5 minutes idle. Available on credit-based plans and Enterprise with credits.
- **Not Python.** No Python runtime is mentioned.

## Why Python cannot run at request time on Netlify

- Python exists only in the **build image** (file 02). It is not in the function runtime. A commonly reported failure is `spawn python3 ENOENT` (this claim is from docs/05 of this repo; not re-verified on Netlify docs).
- So "analyze a review with spaCy on demand" cannot be done on Netlify. spaCy results are precomputed at build time; live analysis uses NLTK-in-browser (Pyodide).

## Alternatives that stay inside the "no outside servers" rule

| Need | Approach |
|---|---|
| Heavy NLP (NLTK + spaCy over corpus) | Build-time Python (`pipeline/build.py`) writes `site/data/*.json` |
| Live sentiment on pasted text | Pyodide + NLTK VADER in the browser (static files only) |
| Live spaCy on new text | Not available; show precomputed examples (docs/05 decision) |
| Anything needing JS server code | Only if the team explicitly decides to add a TS/JS function; it could not call Python |

## Project application

- Do not create `netlify/` directory or `[functions]` config. If one appears, it is a mistake.
- If a deploy summary shows "functions deployed", investigate: likely a stray `netlify/functions/` folder.
- Keep Deploy Previews/Branch deploys static; no env secrets are needed.
- Do not add redirects with `status = 200` proxying to external APIs.
- If someone proposes "just add a Python function", point to this file: Functions = TS/JS/Go; Edge = TS/JS; Server = Node.
