# 01 - Netlify builds with Python

Sources:
- https://docs.netlify.com/build/configure-builds/available-software-at-build-time/
- https://docs.netlify.com/build/configure-builds/manage-dependencies/
- https://docs.netlify.com/build/configure-builds/file-based-configuration/

Fetched: 2026-11-20

## Build environment

- Current build image: **Ubuntu 24.04 (Noble Numbat)**.
- Python row of the "Available software" table: default version `3.x` (the minor version is not stated; it is "determined by the site's selected build image"); available: "Any official Python version"; set it with the build environment variable `PYTHON_VERSION`, a `Pipfile`, or a `runtime.txt`.
- Tools present: `pip` ("corresponds with the installed Python version"), `Pipenv` (defaults to latest), GNU Make 4.3, Node.js default `24` (set via `.nvmrc`, `.node-version`, `NODE_VERSION`, or UI), npm, Deno, libvips 8.15.1, Hugo, Zola, Bun, etc.
- Find the actual versions used: the site's **deploy logs**; build image selection is under Project configuration > Developer settings > Continuous deployment > Build image selection.
- Python is available **only at build time**; the runtime (Functions) is JS/TS/Go (see `docs/05-netlify-architecture.md`).

## Choosing the Python version (3 ways, from "Manage build dependencies")

1. Set the `PYTHON_VERSION` environment variable (UI, or `[build.environment]` in `netlify.toml`).
2. Add `runtime.txt` to the site's **base directory**: "must include the version number *only*: `x.y`, with no trailing newline." Example content: `3.12`.
3. Use Pipenv: specify version in a `Pipfile` in the base directory.

The supported-version list "depends on the site's selected build image." A partial version like `3.12` is the documented format for `runtime.txt`; for `PYTHON_VERSION` the page does not spell out whether `3.12` or `3.12.4` is expected ((unverified) the repo docs use `"3.12"`).

## Python dependencies

"If your build requires any Python dependencies, you must provide a list of these for installation using pip or Pipenv."

- **pip**: generate with `pip freeze > requirements.txt` in the base directory. "This creates a `requirements.txt` file that Netlify will use to install your dependencies by running `pip install`." Netlify links to pip's requirements-file-format reference for details (so direct URL requirements and `--hash` options are standard pip behaviour; see 02).
- **Pipenv**: commit `Pipfile` (+ `Pipfile.lock` for exact versions). Netlify runs `pipenv install`.
- Executables from installed dependencies are put on PATH for the rest of the build.
- The requirements file must be in the **base directory** (repo root unless `base` is set). The docs do not say it is re-read from other folders, so keep `requirements.txt` at the base.
- The page does not mention a Python virtualenv location or `python -m pip` details (unverified); invoking `python pipeline/build.py` in the build command is fine.

## Dependency cache

- First build is slow; "After the initial build, we'll cache the dependencies." If dependencies change, the install re-runs, but cached deps may remain if still satisfying (no guarantee a change takes effect).
- If a build fails strangely, retry with **clear cache** ("Deploy site" > "Clear cache and deploy site" / "deploying the latest branch commit with the clear cache option").

## File-based configuration (`netlify.toml`)

- Location: normally the **repo root**; elsewhere requires base/package directory settings (monorepos).
- `[build]` keys: `base`, `publish` (folder containing the finished files deployed), `command` (build command), `environment`, `processing`; also `ignore`.
- Environment variables: put under their own table:
  ```toml
  [build.environment]
    VARIABLE = "value"
  ```
- Context overrides:
  ```toml
  [context.production]
    publish = "output/"
    command = "make publish"
  [context.deploy-preview]
    publish = "dist/"
  ```
- Headers:
  ```toml
  [[headers]]
    for = "/*"
    [headers.values]
      X-Frame-Options = "DENY"
  ```
  Multi-value headers use multi-line strings (`cache-control = '''...'''`).
- Redirects: `[[redirects]]` with `from`, `to`, `status`, `force`, `query`, `conditions`.
- **UI override rule:** "UI settings are overridden if a `netlify.toml` file is present and a setting for the same property/redirect/header exists in the UI and the TOML file." So netlify.toml wins.
- Build time limits: not stated on this page (the repo docs mention ~15 min historically; verify in Netlify UI).

## Project application

Minimal working config for this repo:
```toml
[build]
  command = "pip install -r requirements.txt && python pipeline/build.py"   # pip install is optional: Netlify already runs it for requirements.txt
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.12"
  NLTK_DATA = "/opt/build/repo/nltk_data"   # (unverified path; safer: set it from inside build.py with nltk.data.path.insert)

[[headers]]
  for = "/data/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"
```
- Because Netlify runs `pip install` automatically for `requirements.txt` at the base, the build command can be only `python pipeline/build.py`. Keeping the explicit `pip install` is harmless but doubles install time (cached).
- Pick one Python-version mechanism (`PYTHON_VERSION` in `netlify.toml` is easiest to review). A spaCy 3.8 wheel must exist for the chosen Python; the repo's smoke test used Python 3.13, docs/05 targets 3.12. Verify the first deploy log shows the expected version.
- `publish = "site"` means `site/data/*.json` produced by the build script is deployed; commit only static assets in `site/` and generate `site/data/` at build (or commit it as a fallback).
- Check the deploy log for: Python version, pip install success of the spaCy model URL, build duration.
