# 03 - Installing and loading spaCy models

Sources:
- https://spacy.io/usage/models (sections: download, "Downloading and requirements.txt", usage)
- https://spacy.io/models/en (en_core_web_sm model card)
- Repo smoke test: `docs/README.md` ("spaCy 3.8.18, en_core_web_sm 3.8.0, Python 3.13")

Fetched: 2026-11-20

## Concept

"spaCy's trained pipelines can be installed as Python packages. ... They're versioned and can be defined as a dependency in your requirements.txt. Trained pipelines can be installed from a download URL or a local directory, manually or via pip."

## Install methods (from the docs)

```bash
# best-matching version for the installed spaCy
python -m spacy download en_core_web_sm
# exact version
python -m spacy download en_core_web_sm-3.0.0 --direct
```
`spacy download` installs via pip into site-packages and picks the package "compatible with your spaCy installation".

Direct pip install from a wheel URL ("Installing the wheel is usually more efficient"):
```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
pip install $(spacy info en_core_web_sm --url)     # print the matching URL
pip install /Users/you/en_core_web_sm-3.0.0-py3-none-any.whl   # local file
```

## In requirements.txt (verbatim pattern from the docs)

```text
spacy>=3.0.0,<4.0.0
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```
- URL pattern: `https://github.com/explosion/spacy-models/releases/download/<name>-<version>/<name>-<version>-py3-none-any.whl`.
- "See the list of models for model download links for the current spaCy version."
- For this project (3.8 line) the URL becomes `.../en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl`. The model card page https://spacy.io/models/en lists **en_core_web_sm 3.8.0** (12 MB; components: tok2vec, tagger, parser, senter, attribute_ruler, lemmatizer, ner), consistent with the repo's smoke test.

## Version compatibility

- "All pipeline packages are versioned and specify their spaCy dependency. This ensures cross-compatibility."
- A model built for spaCy 3.8.x should be installed with spaCy 3.8.x (model pins a spaCy range; the exact range string is not on the fetched page, (unverified); the model's metadata `spacy_version` shows it, and `spacy info en_core_web_sm` / `python -m spacy validate` report mismatches).
- Mismatched minor versions give warnings or errors at `spacy.load` ("W095 model version ... may not be compatible"), per general spaCy behaviour (unverified here).
- Pin both: `spacy==3.8.18` and model `3.8.0`.

## Loading

```python
import spacy
nlp = spacy.load("en_core_web_sm")            # load package by name
nlp = spacy.load("/path/to/en_core_web_sm")   # load from a directory

import en_core_web_sm                          # import as a module
nlp = en_core_web_sm.load()
doc = nlp("This is a sentence.")
```
- `spacy.load` also accepts `disable=[...]` / `exclude=[...]` to skip components (e.g. exclude `["lemmatizer"]` is not recommended if lemmas are needed); not shown on the fetched page, (unverified) here; verify against https://spacy.io/api/top-level#spacy.load before use.
- Load the model **once** at the top of the build script, then `nlp.pipe(texts, batch_size=...)`.

## Pitfalls

- Plain `python -m spacy download` inside a Netlify build needs network access to GitHub at build time and a working `pip`; requirement-file URL is more declarative and is cached by Netlify's pip cache.
- Do not attempt this in the browser: spaCy is not in Pyodide (see Pyodide notes 02).
- If the wheel URL 404s (release renamed), check https://github.com/explosion/spacy-models/releases.

## Project application

- `requirements.txt` carries the model wheel URL (see 02). In `pipeline/build.py`: `nlp = spacy.load("en_core_web_sm")` inside a try/except `OSError` that prints a clear message ("model not installed; check requirements.txt").
- Add a build-time assertion logging `spacy.__version__` and `nlp.meta["version"]` so the deploy log proves versions.
- Disable unneeded components only after testing, e.g. keep `ner`, `parser` (dependency aspect-opinion linking), `lemmatizer`/`attribute_ruler`/`tagger`; `senter` can stay disabled by default.
