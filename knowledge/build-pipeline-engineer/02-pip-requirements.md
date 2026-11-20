# 02 - pip requirements files (format, pinning, URL refs, hashes)

Sources:
- https://pip.pypa.io/en/stable/reference/requirements-file-format/ (page title: "pip documentation v26.3")
- https://pip.pypa.io/en/stable/topics/secure-installs/
- https://docs.netlify.com/build/configure-builds/manage-dependencies/ (Netlify runs `pip install` on `requirements.txt`)

Fetched: 2026-11-20

## Format

Each line is one of:
- `[[--option]...]`
- `<requirement specifier>`
- `<archive url/path>`
- `[-e] <local project path>`
- `[-e] <vcs project url>`

Rules:
- `#` at line start is a comment; whitespace followed by `#` starts an inline comment. Comments are stripped *after* line continuations are processed.
- A line ending in an unescaped `\` continues on the next line.
- Default encoding is **UTF-8** unless a PEP 263 comment (`# -*- coding: ... -*-`) says otherwise.
- Supported options in the file include `-r/--requirement`, `-c/--constraint`, `-i/--index-url`, `--extra-index-url`, `-f/--find-links`, `--no-index`, `--pre`, `--require-hashes`, and per-requirement `--hash`.
- Netlify note: generate with `pip freeze > requirements.txt`; Netlify installs it with `pip install`.

## Version specifiers (PEP 440 forms shown on the page)

```text
docopt == 0.6.1
requests [security] >= 2.8.1, == 2.8.*
requests [security] >= 2.8.1, == 2.8.* ; python_version < "2.7"   # environment marker after ';'
```
- Operators: `==`, `>=`, `~=` (compatible release), `!=`, `<`.
- Exact pin (`==`) = reproducible builds. For this project pin nltk and spacy exactly (docs/05 uses `nltk==3.10.4`, `spacy==3.8.18`).
- Compatible release example: `spacy~=3.8.0` means `>=3.8.0, ==3.8.*` (standard PEP 440 meaning, not shown verbatim on the page).

## Direct URL references (PEP 508 "name @ url")

```text
urllib3 @ https://github.com/urllib3/urllib3/archive/refs/tags/1.26.8.zip
```
- Also allowed: a bare archive URL or local path line, e.g. a wheel URL
  `http://.../wxPython_Phoenix-...-cp34-none-win_amd64.whl` or `./downloads/numpy-1.9.2-cp34-none-win32.whl`.
- The `name @ URL` form is preferred because it states the distribution name (pip checks that the name matches) and lets other requirements depend on it.
- The spaCy docs show exactly this for a model (see 03).

## Hash-checking mode (optional hardening)

From "Secure installs":
- Hashes in the file protect "against remote tampering and network issues". Add `--hash=sha256:<digest>` after a requirement (use `\` continuations):
  ```text
  FooProject == 1.2 \
    --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 \
    --hash=sha256:486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7
  ```
- "Specifying `--hash` against *any* requirement will activate this mode globally (all-or-nothing)." `--require-hashes` forces it on, and prints the hashes of what it fetched (handy to bootstrap).
- In this mode **every** requirement **and every transitive dependency** must be listed and hashed, else error. Requirements must be pinned with `==` (or to a URL/path).
- URL requirements: a `#md5=...` (or other) fragment in the URL satisfies "has a hash" for legacy reasons; use sha256 where possible. Hashes from PyPI index download URLs (`#sha256=`) do **not** count as local hashes.
- Weak algorithms (md5, sha1, sha224) are excluded from recommended use.
- `pip hash <file>` computes a file's hash; use it to add hashes for the extra archives (binary vs sdist).
- Local directories and VCS URLs cannot be combined with hashed requirements (unless `--no-require-hashes`).

## Practical advice

- Full transitive pinning with hashes for spaCy (thinc, blis, numpy, ...) is long and platform-specific (different wheel hashes per Python version/OS). **Skip hash mode** for this class project; pin top-level versions only. (Opinion, based on the all-or-nothing rule above.)
- Optionally keep a `constraints.txt` (`-c`) to pin transitive deps without forcing hashes (the `-c` option is listed on the page; Netlify installs only `requirements.txt` automatically, so reference it as `-c constraints.txt` from inside requirements.txt).
- Quote nothing in requirements files; spaces around `@` are fine.

## Project application

Recommended `requirements.txt` (versions from the repo's smoke test in docs/README.md; recheck they resolve for the chosen Python):
```text
nltk==3.10.4
spacy==3.8.18
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```
- Validate locally in a clean venv: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`.
- If the model URL download is flaky on Netlify, fallback: vendor the wheel in the repo (e.g. `vendor/en_core_web_sm-3.8.0-py3-none-any.whl`) and use `en_core_web_sm @ file:./vendor/...` relative path. (Relative `file:` handling depends on pip's working directory; Netlify runs pip from the base directory; unverified.)
- Ensure nltk 3.10.x (build) vs 3.9.4 (Pyodide) differences do not leak into shared code (see Pyodide notes).
