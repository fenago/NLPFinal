# 03 - netlify.toml reference

Sources:
- https://docs.netlify.com/build/configure-builds/file-based-configuration.md
- https://docs.netlify.com/deploy/deploy-overview.md (deploy contexts)

Fetched: 2026-11-20

## Basics

- File: `netlify.toml`, normally in the repo root. For other locations set base/package directory.
- **Settings in `netlify.toml` override the same settings in the UI.**
- Not every setting can be set in the file; some are UI/CLI/API only.
- Optional schema validation line at the top: `"$schema" = "https://open-api.netlify.com/netlify.schema.json"` (ignored by the build; editors may use it).
- Paths are relative to the base directory (root `/` by default).
- Environment variable references like `"$VAR"` are NOT expanded inside `netlify.toml` values. Exception: for `[[headers]]`/`[[redirects]]` you may `sed` placeholders in the build command (docs example uses `sed -i "s|HEADER_PLACEHOLDER|${VAR}|g" netlify.toml && ...`).

## [build]

Keys: `base`, `publish`, `command`, `environment`, `processing`.
`command` runs in Bash.

```toml
[build]
  base = "."            # optional; default repo root
  command = "python pipeline/build.py"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.12"
```

Other `[build]` things: `ignore` (a Bash/Node command that decides whether to skip a build), `[build.processing.html] pretty_urls = true` (overrides UI Pretty URLs).

## Deploy contexts: [context.*]

Context-aware keys: `[build]` and `[[plugins]]` (NOT `[[redirects]]` or `[[headers]]`).
Predefined contexts: `production`, `deploy-preview`, `branch-deploy`, `dev` (also `preview-server` per deploy overview). Any branch name can be a custom context: `[context.staging]`, `[context."feat/branch"]` (quote names with special characters).

Specificity (low to high): `[build]` < `[context.production|deploy-preview|branch-deploy|dev]` < `[context.<branchname>]`. Only properties explicitly set are overridden.

```toml
[context.production]
  command = "python pipeline/build.py"

[context.deploy-preview]
  command = "python pipeline/build.py --sample 500"

[context.deploy-preview.environment]
  SAMPLE_SIZE = "500"

[context.dev.environment]       # for `netlify dev` / local CLI only
  NODE_ENV = "development"
```

Note the inline form also exists: `[context.production]` with `environment = { NODE_VERSION = "14.15.3" }`.

## [[redirects]]

Array of tables; each block is one rule. Redirects (like headers) are **global**, not scoped to contexts.

```toml
[[redirects]]
  from = "/old-path"
  to = "/new-path"
  status = 301          # default 301
  force = false         # true => rule wins over an existing file at `from`
  # query = {id = ":id"}
  # conditions = {Language = ["en"], Country = ["US"]}
  # signed = "ENV_VAR_NAME"
  # [redirects.headers]
  #   X-From = "Netlify"
```

SPA-style rewrite from docs: `from = "/*"`, `to = "/index.html"`, `status = 200`.
Default behaviour: a redirect is NOT applied if a file exists at the `from` path unless `force = true`.
Proxy rewrites (status 200 to an external URL) are possible but irrelevant here (no outside servers).

## [[headers]]

```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    cache-control = '''
    max-age=0,
    no-cache,
    no-store,
    must-revalidate'''
```

- `for` = path/URL pattern; `values` = map of response headers. Header names are case-insensitive.
- Multi-value headers are written as multi-line strings; they collapse to `a,b,c`.
- Global for all deploys (cannot be scoped per context in the file). Details in file 04.

## [functions], [dev], [server], [[plugins]], [[integrations]], [template]

- `[functions]`: `directory` (default `netlify/functions`), `node_bundler`, `external_node_modules`, `included_files`, per-function blocks like `[functions.heavy] memory = "2gb"`. Not used by this project.
- `[dev]`: Netlify Dev overrides: `command`, `port`, `targetPort`, `functionsPort`, `publish`, `autoLaunch`, `framework` (`#auto`, `#static`, `#custom`), `https.certFile/keyFile`. There is **no** `[dev.environment]`; use `[context.dev.environment]`. `[dev]` does not run in Bash.
- `[server]`: Netlify Server (Early Access, Node only). Not used.
- `[[plugins]]` with `package = "..."`: build plugins (JS packages). Not needed.

## Complete example for this project (sketch)

```toml
"$schema" = "https://open-api.netlify.com/netlify.schema.json"

[build]
  command = "python pipeline/build.py"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.12"

[dev]
  publish = "site"
  framework = "#static"

[[headers]]
  for = "/data/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"
```

## Project application

- Keep `netlify.toml` minimal: `[build]`, `[build.environment]`, `[[headers]]`. No `[functions]`, no `[[redirects]]` proxying.
- Do not rely on `$VAR` substitution inside TOML values.
- Use `[context.deploy-preview]` only if a faster/smaller build is wanted for previews.
- (unverified) Behaviour when both `_headers` file and `[[headers]]` define the same path; see file 04.
- `netlify.toml` overrides UI settings, so after adding it the UI "Build settings" values are shadowed; check the deploy log to see which values were used.
