# 02 — English Models (en_core_web_sm) and Installation

Sources:
- https://spacy.io/models/en
- https://spacy.io/usage/models
- https://spacy.io/api/top-level (spacy.load, spacy.blank)

Fetched: 2026-11-20

## Package family (all "English pipeline optimized for CPU", genre: web written text — blogs, news, comments; MIT license; author Explosion; latest listed = `3.8.0`)
| Package | Size (listed) | Vectors | Notes |
| --- | --- | --- | --- |
| `en_core_web_sm` | 12 MB | none (0 keys) | smallest, default for this project |
| `en_core_web_md` | 31 MB | 685k keys, 20k unique vectors, 300 dims | |
| `en_core_web_lg` | 382 MB | 685k keys, 343k unique vectors, 300 dims | |
| `en_core_web_trf` | 436 MB | none | roberta-base transformer; no `tok2vec`/`senter` |

Note: the repo docs say "≈15 MB installed" for sm; spacy.io lists 12 MB (the package download size). Both can be true (unverified which measure each uses).

## en_core_web_sm components
- Components listed: `tok2vec`, `tagger`, `parser`, `senter`, `attribute_ruler`, `lemmatizer`, `ner`.
- Default **Pipeline** (what runs; `senter` is shipped but not in the active pipeline): `tok2vec`, `tagger`, `parser`, `attribute_ruler`, `lemmatizer`, `ner`.
- Training sources: OntoNotes 5, ClearNLP constituent-to-dependency conversion, WordNet 3.0.
- Download link (wheel): `https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl`
- Lemmatizer in English pipelines is rule-based: `nlp.get_pipe("lemmatizer").mode  # 'rule'` (from linguistic-features page).

## Accuracy as listed on spacy.io/models/en (sm)
| Metric | Meaning | sm |
| --- | --- | --- |
| TOKEN_ACC / P / R / F | tokenization | 1.00 |
| TAG_ACC | fine-grained POS tags | 0.97 |
| SENTS_P / R / F | sentence segmentation | 0.92 / 0.89 / 0.91 |
| DEP_UAS | unlabeled dependencies | 0.92 |
| DEP_LAS | labeled dependencies | 0.90 |
| ENTS_P / R / F | named entities | 0.84 / 0.84 / 0.84 |

Comparison (ENTS_F): sm 0.84, md 0.85, lg 0.86, trf 0.90. (DEP_LAS: sm/md/lg 0.90, trf 0.94; TAG_ACC trf 0.98.)
- These are on OntoNotes-style news/web text, not product reviews; expect lower and noisier results on informal review text (inference, not from the page).

## Label scheme (sm; "specific to the corpus the model was trained on")
- **ner (18 labels):** `CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP, ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART`
- **parser dep labels:** `ROOT, acl, acomp, advcl, advmod, agent, amod, appos, attr, aux, auxpass, case, cc, ccomp, compound, conj, csubj, csubjpass, dative, dep, det, dobj, expl, intj, mark, meta, neg, nmod, npadvmod, nsubj, nsubjpass, nummod, oprd, parataxis, pcomp, pobj, poss, preconj, predet, prep, prt, punct, quantmod, relcl, xcomp`
- **tagger:** Penn Treebank-style fine tags (`NN, NNP, NNS, VB, VBD, VBG, VBN, VBP, VBZ, JJ, JJR, JJS, RB, ...`, plus `_SP`, `ADD`, `AFX`, `HYPH`, `NFP`, `XX`).
- Describe any label with `spacy.explain("GPE")` (returns `None` if unknown).

## Installing
```bash
pip install -U spacy
python -m spacy download en_core_web_sm              # picks the best match for installed spaCy
python -m spacy download en_core_web_sm-3.0.0 --direct   # exact version (docs example)
```
- `spacy download` installs via pip into site-packages. In Jupyter use `!python -m spacy download ...` and restart the kernel.
- **For automated builds the docs recommend a direct pip link instead of `spacy download`** ("an unnecessary layer of complexity"). Use in `requirements.txt` (docs' example form, shown for 3.7.1):
```text
spacy>=3.0.0,<4.0.0
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```
  For spaCy 3.8 use the 3.8.0 wheel URL from the table above:
```text
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```
- Other forms: `pip install $(spacy info en_core_web_sm --url)`, or a local `.whl`/`.tar.gz` path.
- From Python: `import spacy; spacy.cli.download("en_core_web_sm")`.

## Loading
```python
import spacy
nlp = spacy.load("en_core_web_sm")                 # by package name
nlp = spacy.load("/path/to/en_core_web_sm")        # from a data directory
import en_core_web_sm; nlp = en_core_web_sm.load() # native import; ImportError immediately if missing
nlp = spacy.load("en_core_web_sm", exclude=["ner"], disable=[...], enable=[...])
nlp = spacy.blank("en")                            # tokenizer-only, no trained components
```
- `spacy.load` keyword args: `vocab`, `disable`, `enable` (v3.4), `exclude` (v3.0), `config`.
- Docs recommend the native `import en_core_web_sm` style for larger code bases/CI; each package exposes `__version__` for compatibility checks.

## Version compatibility
- Pipeline packages are versioned and declare their spaCy dependency; `spacy download` does compatibility checks and picks a matching version.
- The 3.8.0 packages are listed as latest on the models page. Model minor version should match spaCy minor (3.8.x with 3.8.0 model). Repo smoke test used spaCy 3.8.18 + en_core_web_sm 3.8.0 (from the project's docs, not from spacy.io).
- Using a model built for an older spaCy minor typically triggers a version warning (general spaCy behavior; exact wording unverified).

## Project application
- Pin in `requirements.txt` at build root: `spacy>=3.8,<3.9` plus the direct 3.8.0 wheel URL — avoids `spacy download` network step differences on Netlify and is the docs' recommended pattern for automation.
- sm lacks vectors: do not call `.similarity()` meaningfully; use md/lg only if similarity-based aspect clustering is added (not needed).
- Expected review-domain weakness: `PRODUCT` is sparse and `ORG`/`PERSON` get confused on brand names (see `06-entityruler.md` for the fix). Accept ENTS_F ≈ 0.84 as a news-domain ceiling.
- Label set to surface in UI: `PERSON`, `GPE`/`LOC`/`FAC`, `ORG`, `PRODUCT`, `MONEY`, `DATE`/`TIME`, `QUANTITY`.
