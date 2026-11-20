# 01 - Build configuration (command, publish dir, base dir, env vars)

Sources:
- https://docs.netlify.com/build/configure-builds/overview.md
- https://docs.netlify.com/build/configure-builds/environment-variables.md
- https://docs.netlify.com/build/configure-builds/file-based-configuration.md

Fetched: 2026-11-20

## Core terms (from the build configuration overview)

- **Base directory**: where Netlify checks for dependency files (`package.json`, `.nvmrc`, and for Python `requirements.txt`, `runtime.txt`, `Pipfile`), installs dependencies and runs the build command. Also used for build caching. Defaults to the repo root.
- **Build command**: runs in the **Bash shell**, so Bash syntax (`&&`, env var expansion `$VAR`) is allowed. Example from docs: `npm run build`.
- **Publish directory**: directory containing the deploy-ready HTML/assets produced by the build. Relative to the base directory (root by default).
  - Docs note: **only files in the publish directory are deployed.** Anything outside it is not in the site.
- **Functions directory**: default `netlify/functions` (relative to base). Not needed for this project.
- **Package directory**: monorepo-only. Not needed here.
- **Netlify configuration file**: optional `netlify.toml`.

## Where to set build settings

1. Netlify UI: Project configuration > Developer settings > Continuous deployment > Build settings.
2. `netlify.toml` (`[build]` table): keys `command`, `publish`, `base`, `environment`, `processing`.
3. Netlify CLI when setting up continuous deployment (`netlify init`).

**Precedence:** settings in `netlify.toml` override the same settings in the UI. A `base` in a root-level `netlify.toml` overrides the UI base directory.

Netlify auto-detects settings for known frameworks; for a custom Python build the command and publish directory must be set manually.

## Path rules

- All paths in `netlify.toml` are "absolute paths relative to the base directory" (root `/` by default), e.g. `publish = "site"` or `publish = "site/"`.
- The build image is a VM snapshot (Ubuntu 24.04, see file 02). You can choose among build images in the UI (Developer settings > Continuous deployment > Build image selection); the chosen image applies to production, branch deploys and Deploy Previews.

## Build environment variables

Declare via UI, CLI (`netlify env:set`), API, or `netlify.toml` (`[build.environment]`).
- If the UI offers scopes, the scope must include **Builds** to be visible at build time.
- Docs recommend the UI for sensitive values (not committing them to the repo).
- Netlify **does not read `.env` files** during a Netlify build. Import them with `netlify env:import .env` if needed.
- Variables set in `netlify.toml` are available to the build but **not** to the deploy runtime (functions etc.).
- Using `$VAR` as a value inside `netlify.toml` (e.g. `key = "$VAR"`) is **not** supported (except signed proxy redirects).

### Reserved/config variables relevant here

| Variable | Effect |
|---|---|
| `PYTHON_VERSION` | Sets the Python version used by the build |
| `NODE_VERSION`, `NPM_FLAGS` | Node settings (not needed for a pure-Python build) |
| `CI` | Defaults to `true`; override with `CI=''` prefix in the build command if a tool misbehaves |
| `NETLIFY_BUILD_DEBUG` | Set `true` in the UI for extra build-log debugging output (not secret-leaking) |
| `GIT_LFS_ENABLED`, `GIT_LFS_FETCH_INCLUDE` | Must be set in the UI, not `netlify.toml` (file is read after clone) |

### Read-only variables set by Netlify

`NETLIFY` (always `true`), `BUILD_ID`, `CONTEXT` (`production`, `deploy-preview`, `branch-deploy`, `dev`), `REPOSITORY_URL`, `BRANCH`, `HEAD`, `COMMIT_REF`, `CACHED_COMMIT_REF`, `PULL_REQUEST`, `REVIEW_ID`, `URL`, `DEPLOY_URL`, `DEPLOY_PRIME_URL`, `DEPLOY_ID`, `SITE_NAME`, `SITE_ID`, `ACCOUNT_ID`.

Python usage: `os.environ.get("CONTEXT")` or `os.environ.get("NETLIFY") == "true"` lets `pipeline/build.py` detect it is running on Netlify (for example to skip optional local-only steps).

## Minimal example

```toml
[build]
  command = "python pipeline/build.py"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.12"
```

## Post-build variable access

Build variables are not available to the finished static site. If the site needs a value, the build script must write it into the output (only non-sensitive values), per the docs section "Use variables in a site after it's built".

## Project application

- Set `command = "python pipeline/build.py"` (or a `bash` chain such as `pip install -r requirements.txt && python pipeline/build.py` only if auto-install is not relied on; see file 02) and `publish = "site"`.
- The build script must write **everything** the browser needs into `site/`: `site/data/*.json`, the Pyodide `.wasm`/runtime files, `site/nltk_data/`. Files outside `site/` are never deployed.
- Keep `base` unset (repo root) so `requirements.txt` at the root is found.
- No secrets are needed (no outside servers), so no UI env vars are required beyond optionally `PYTHON_VERSION`.
- Use `CONTEXT` if the build should do less work on `deploy-preview` (for example a smaller dataset sample).
- (unverified) Whether `command` in `netlify.toml` may span multiple lines: the docs only show single-line strings; use `&&` in one string.
