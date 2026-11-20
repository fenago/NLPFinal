# 06 - Deploys, previews, rollbacks, Netlify CLI

Sources:
- https://docs.netlify.com/deploy/deploy-overview.md
- https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview.md
- https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli.md
- https://docs.netlify.com/api-and-cli-guides/cli-guides/local-development.md

Fetched: 2026-11-20

## Atomic deploys

- Every change is a new deploy; Netlify uploads only changed files, and nothing goes live until all files are uploaded, then the new version goes live atomically. No partial/inconsistent state.
- Limit: **54,000 files per directory** (no limit on files per deploy overall). If any directory in the publish directory has more, the deploy fails.
- Each successful deploy gets a permalink `<deployid>--<site>.netlify.app` whose content never changes.

## Deploy types and URLs

| Type | URL pattern | Notes |
|---|---|---|
| Production deploy | main site URL | From the production branch; becomes the published deploy if auto publishing is on |
| Branch deploy | `<branch>--<site>.netlify.app` | Not enabled by default; enable in Project configuration > Developer settings > Continuous deployment > Branches and deploy contexts (specific branches or "All") |
| Deploy Preview | `deploy-preview-<N>--<site>.netlify.app` | Built automatically for each PR/MR unless disabled; agent runs use `agent-<runid>--...` |
| Permalink | `<deployid>--<site>.netlify.app` | Immutable |

- Deploy Previews get `X-Robots-Tag: noindex`; the latest branch deploy does not. For privacy use password protection or private project (credit plans).
- Deploy contexts: `production`, `deploy-preview`, `branch-deploy`, `preview-server`, `dev`, plus any branch name. Env var `CONTEXT` exposes the name at build time.
- Skip a build: add `[skip ci]` or `[skip netlify]` to the commit message (or PR title for previews).
- Untrusted deploys (forks of public repos) require approval by default; they may build without sensitive vars depending on policy.

## Reading the deploy log

- Site > Deploys > click a deploy. The detail page shows a **deploy summary** (files uploaded, headers/redirects status, functions count) above the **deploy log** (build image, dependency caching, full stdout of your build command, plugin output, success/failure).
- Click a line number to get a shareable URL (`#L5-L10`); "Copy to clipboard" copies everything.
- "Why did it fail?" button gives an AI diagnosis (no credit use).
- Extra detail: set `NETLIFY_BUILD_DEBUG=true` in the UI.
- Failed/canceled deploys are auto-deleted after 30 days (90 on paid plans); all deploys auto-delete after 30/90 days except the published deploy, the latest successful production deploy and the latest successful branch deploy per branch.

## Rollback (publish a previous deploy)

- Deploys tab > open any previous successful deploy > **Publish deploy**. Instant; does not rebuild.
- If auto publishing is on, the next Git-triggered production deploy overwrites the rollback. To hold a rollback: **Lock to stop auto publishing** (Deploys list); **Unlock to start auto publishing** later.
- Other actions: Cancel deploy; Retry deploy from latest branch commit (with "retry without cache"); Download a deploy (zip or single file) from the deploy file browser; Trigger deploy button on Deploys page. Deleting is permanent, does not save build minutes, and you cannot delete the currently published deploy.

## Netlify CLI

Install: `npm install -g netlify-cli` (needs Node 18.14.0+). In CI prefer a local dev dependency (`npm install netlify-cli --save-dev`). Help: `netlify help`, `netlify help deploy`. Debug output: `DEBUG=* netlify deploy`.

| Command | Purpose |
|---|---|
| `netlify login` | Authenticates (token in `config.json`; Linux `~/.config/netlify/config.json`). In CI use `NETLIFY_AUTH_TOKEN` |
| `netlify link` / `netlify unlink` | Link folder to existing site; writes `.netlify/state.json` (`siteId`). Env alternative: `NETLIFY_SITE_ID` |
| `netlify init` (`--manual`) | Set up continuous deployment from Git |
| `netlify clone owner/repo` | Clone and link in one step |
| `netlify build` | Run the Netlify build locally (uses `netlify.toml` and UI/CLI env vars; all scopes apply) |
| `netlify build --dry` | Print build stages without running |
| `netlify build --context deploy-preview` | Run as another deploy context (default `production`) |
| `netlify dev` | Local dev server (Netlify Dev); `--context production` to use that context's config/env |
| `netlify deploy` | Draft deploy to a unique URL |
| `netlify deploy --alias=NAME` | Draft deploy with custom subdomain (must not equal a branch name) |
| `netlify deploy --prod` (`-p`) | Production deploy |
| `netlify deploy --dir=site` | Choose publish folder; order of lookup: flags, `netlify.toml`, UI config |
| `netlify deploy --allow-anonymous` | Unclaimed project for 1 hour |
| `netlify env:list|get|set|unset|import|clone` | Manage env vars |

Important: `netlify deploy` uploads files as they are; it does **not** run your build. Run the build first (`netlify build` or `python pipeline/build.py`) then `netlify deploy --dir=site [--prod]`.

### Netlify Dev (`netlify dev`)

- Detects the site generator or serves static files. Config via `[dev]` in `netlify.toml`: `publish`, `command`, `targetPort`, `port` (docs example 8888), `framework` (`"#static"` to force static server). By default starts an HTTP server.
- It does not run Bash for `[dev].command`.
- For a prebuilt static `site/` directory use `publish = "site"` and `framework = "#static"` (inference from docs; test it).
- (unverified) Netlify Dev does not run the Python build step by default; run `python pipeline/build.py` yourself first.

## Project application

- Typical workflow: push branch > open PR > Deploy Preview builds with Python 3.12 > review `deploy-preview-N--site.netlify.app` > merge > production deploy.
- Debug locally: `pip install -r requirements.txt && python pipeline/build.py && npx netlify-cli dev --dir site` (or `netlify dev` with `[dev] publish = "site"`).
- If a bad build ships, roll back with **Publish deploy** on the last good deploy and **Lock** auto publishing while fixing.
- Check each preview's deploy log for: Python version line, pip install success, spaCy model import, build script duration, and "files uploaded" count.
- Enable Deploy Previews privacy (password protect) if the dataset sample should not be indexable.
