# Build-pipeline engineer knowledge - index

Grounded in official docs (Netlify, pip, spaCy, NLTK, Python), fetched 2026-11-20. Items not confirmed on a fetched page are marked "(unverified)" inside the notes.

| File | Read it when |
|---|---|
| 01-netlify-python-builds.md | configuring `netlify.toml`, `PYTHON_VERSION`/`runtime.txt`/`Pipfile`, publish dir, what Netlify auto-installs |
| 02-pip-requirements.md | writing `requirements.txt`: pins, `name @ URL`, optional `--hash` |
| 03-spacy-model-install.md | installing `en_core_web_sm` by wheel URL, `spacy.load`, version compatibility |
| 04-nltk-data-vendoring.md | committing `nltk_data/`, `NLTK_DATA`, `nltk.data.path`, shipping data to the browser |
| 05-python-json-output.md | writing `site/data/*.json` with `json.dumps` options and `pathlib` |

## Key facts (quick reference)

- Netlify build image: Ubuntu 24.04; Python default is "3.x" (set `PYTHON_VERSION`, `runtime.txt` containing only `x.y`, or `Pipfile`); `pip` and `pipenv` available.
- Netlify runs `pip install` automatically on a `requirements.txt` in the base directory; `netlify.toml` settings override the UI.
- `[build] command = "python pipeline/build.py"`, `publish = "site"`.
- spaCy model in requirements: `en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl` (spaCy docs show this pattern with 3.7.1; en_core_web_sm 3.8.0 confirmed on the spaCy model page).
- Vendor NLTK data (`vader_lexicon`, `stopwords`, `punkt_tab`) in `nltk_data/` and copy to `site/nltk_data/` for Pyodide; do not call `nltk.download` on Netlify.
- JSON output: `ensure_ascii=False`, `allow_nan=False`, compact `separators=(",", ":")`, write with `Path.write_text(..., encoding="utf-8")`.

## Open items / unverified

- Exact accepted formats of `PYTHON_VERSION` (`3.12` vs `3.12.x`) and the Python minor version of the default build image (check deploy log).
- Netlify build time limit for the current plan (not on the fetched pages).
- Exact spaCy compatibility range string for en_core_web_sm 3.8.0 and `spacy.load(exclude=...)` details (check spacy.io/api/top-level).
- `nltk.data.path` is not on nltk.org/data.html; it is documented in the NLTK API docs.
- Cross-reference: Pyodide runs nltk 3.9.4 (see `knowledge/pyodide-engineer/`), build may use 3.10.x.
