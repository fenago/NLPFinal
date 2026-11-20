# 02 - Python at build time (image, version, dependencies)

Sources:
- https://docs.netlify.com/build/configure-builds/available-software-at-build-time.md
- https://docs.netlify.com/build/configure-builds/manage-dependencies.md
- https://docs.netlify.com/build/configure-builds/environment-variables.md

Fetched: 2026-11-20

## Build image

- Docs: "Our current build is based on Ubuntu version 24.04 (also called Noble Numbat)."
- Python row of the software table: default version `3.x`; available versions: "Any official Python version"; set using: build env var `PYTHON_VERSION`, a `Pipfile`, or a `runtime.txt`.
- Tools listed: `pip` ("corresponds with the installed Python version"), `Pipenv` (defaults to latest), GNU Make 4.3, libvips 8.15.1, Node.js default 24.
- The exact patch version of the default Python is not stated on the page ("3.x"). The build log lists the software versions actually used (see below).
- The build image can be changed in the UI (Project configuration > Developer settings > Continuous deployment > Build image selection). Netlify pins Node, Ruby, Go and Yarn at first build; the docs do not say Python is pinned (unverified).

## Choosing the Python version (3 ways)

1. Env var `PYTHON_VERSION` (UI, CLI, API, or `[build.environment]` in `netlify.toml`).
2. `runtime.txt` in the base directory. Docs: "must include the version number only: `x.y`, with no trailing newline." Example content: `3.12`.
3. `Pipfile` (Pipenv) in the base directory specifying the Python version.

**Precedence note from docs:** if both `runtime.txt` and `Pipfile` exist, **`runtime.txt` wins**. Precedence between the `PYTHON_VERSION` env var and `runtime.txt` is not stated on the fetched pages (unverified); avoid setting both to different values.

The supported version list "depends on the site's selected build image".

```toml
[build.environment]
  PYTHON_VERSION = "3.12"
```

or `runtime.txt` containing exactly `3.12` (no trailing newline: `printf '3.12' > runtime.txt`).

## Installing Python dependencies

- **pip:** commit `requirements.txt` in the base directory. Docs: "Netlify will use [it] to install your dependencies by running `pip install`." Generate with `pip freeze > requirements.txt`.
- **Pipenv:** commit `Pipfile` (and ideally `Pipfile.lock`); Netlify runs `pipenv install`.
- **If both `requirements.txt` and `Pipfile` exist:** Netlify runs `pip install` for `requirements.txt` and **ignores the Pipfile**.
- Executables from installed dependencies are put on the PATH for the rest of the build.

Example `requirements.txt` for this project (versions from docs/05; verify before pinning):

```text
nltk==3.10.4
spacy==3.8.18
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

(unverified on the Netlify side) Whether the build network can reach `github.com` release assets for the spaCy model wheel is not documented on the fetched pages; test with a deploy preview. A fallback is `python -m spacy download en_core_web_sm` inside the build command, or vendoring the wheel in the repo.

## Dependency cache

- First build is slower; afterwards Netlify caches dependencies ("dependency cache" section). The cached directories are defined by `$NETLIFY_CACHE_DIR` in `run-build-functions.sh` of the selected build image (not shown in docs).
- If dependencies change, the install command is re-run; docs warn a change is not guaranteed to alter the cached copy if the previous deps still satisfy the installer.
- If a build fails strangely, retry with a cleared cache via the retry-deploy dropdown on the latest branch commit (docs wording: "Retry without cache" / "clear cache option"; the exact menu label under Trigger deploy is unverified).

## Seeing what versions the build used

- Docs: "You can also find all of the software versions your build uses in your site's deploy logs." Check the top of each deploy log for the Python version line.
- Local parity: `netlify build` (CLI) mimics the Netlify build; match the local Python version with `PYTHON_VERSION` (docs only state this equivalence for Node; the principle is applied here as an inference).

## Gotchas

- `.env` files are not read on Netlify; `NLTK_DATA` and similar must be set via `[build.environment]` or UI, or handled in code.
- `requirements.txt` must be in the **base directory** (repo root unless `base` is set).
- Large wheels (spaCy + model) increase first-build time; the dependency cache helps later builds.
- Python is a **build-time-only** capability: it is not present at function runtime (see file 05).

## Project application

- Pin `PYTHON_VERSION = "3.12"` in `netlify.toml` (matches docs/05). Do not also add a conflicting `runtime.txt`.
- Keep `requirements.txt` at repo root with exact pins for `nltk`, `spacy`, and the model wheel.
- First deploy to a Deploy Preview and read the log to confirm: Python 3.12.x, successful pip install, `en_core_web_sm` importable.
- Commit `nltk_data/` (punkt_tab, stopwords, vader_lexicon) rather than downloading at build time, and point `NLTK_DATA` at it.
