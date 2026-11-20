# 03 — Named Entities (doc.ents)

Sources:
- https://spacy.io/usage/linguistic-features#named-entities
- https://spacy.io/api/doc (Doc.ents, Doc.set_ents, Doc.char_span)
- https://spacy.io/api/token (ent_iob, ent_type attributes)
- https://spacy.io/api/top-level (spacy.explain)
- https://spacy.io/models/en (NER label list)

Fetched: 2026-11-20

## Access
- `doc.ents` returns a **tuple of `Span`** objects (needs the `ner` component or an entity ruler).
- Per entity `Span`: `.text`, `.label` (hash int), `.label_` (str), `.start`/`.end` (token indices), `.start_char`/`.end_char` (character offsets into `doc.text`).
- The `Span` acts as a token sequence (iterate/index) and `ent.text` gives the whole entity.

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
# Apple 0 5 ORG | U.K. 27 31 GPE | $1 billion 44 54 MONEY   (docs' table)
```
Docs' descriptions for these three: ORG "Companies, agencies, institutions"; GPE "Geopolitical entity, i.e. countries, cities, states"; MONEY "Monetary values, including unit".

## Token-level IOB
- `token.ent_iob_` is `B` (begins), `I` (inside), `O` (outside), `""` (no tag set); int `token.ent_iob` is 3 / 1 / 2 / 0 respectively.
- `token.ent_type_` is the label string for tokens in an entity (`""` otherwise).
```python
doc = nlp("San Francisco considers banning sidewalk delivery robots")
doc[0].ent_iob_, doc[0].ent_type_   # ('B', 'GPE')
doc[1].ent_iob_, doc[1].ent_type_   # ('I', 'GPE')
```
- Other token fields: `ent_kb_id_`, `ent_id_` (EntityRuler pattern ids appear as `ent.ent_id_`).

## Label scheme in en_core_web_* (OntoNotes-trained)
`CARDINAL, DATE, EVENT, FAC, GPE, LANGUAGE, LAW, LOC, MONEY, NORP, ORDINAL, ORG, PERCENT, PERSON, PRODUCT, QUANTITY, TIME, WORK_OF_ART`

Mapping used in this project (from docs/03-spacy.md) — the table below is the project's grouping, with spacy.io only listing the labels:
| Label | App category |
| --- | --- |
| `PERSON` | people (staff, chefs, reps) |
| `GPE`, `LOC`, `FAC` | places (cities/states; non-GPE locations; buildings/airports/etc.) |
| `ORG` | brands, companies, stores |
| `PRODUCT` | products (weak in sm) |
| `MONEY`, `DATE`, `TIME`, `QUANTITY` | prices, visit dates, wait times |
- The glossary descriptions for PERSON/LOC/FAC/PRODUCT/DATE etc. are **(unverified)** here: the "Built-in entity types" block on the usage page did not render in the fetch; get them at runtime with `spacy.explain(label)`.

## spacy.explain
```python
spacy.explain("GPE")      # description string
spacy.explain("amod")     # also works for POS tags and dependency labels
spacy.explain("nope")     # None if not in glossary
```
- Docs: "Get a description for a given POS tag, dependency label or entity type"; the data lives in spaCy's `glossary.py`.

## Setting / correcting entities
- Entity annotations must be set at the document level (cannot write `token.ent_iob`/`ent_type` directly).
```python
from spacy.tokens import Span
fb_ent = Span(doc, 0, 1, label="ORG")            # token indices, NOT chars
doc.set_ents([fb_ent], default="unmodified")      # modify only given spans
doc.ents = list(doc.ents) + [fb_ent]              # or assign the whole list (must not overlap)
fb_ent = doc.char_span(0, 2, label="ORG")         # from character offsets; returns None if not aligned
```
- `Doc.char_span(start, end, label=, alignment_mode="strict"|"contract"|"expand")`.
- Spans assigned to `doc.ents` must be valid and non-overlapping or an error is thrown.
- `doc.set_ents(entities, blocked=, missing=, outside=, default="outside")`.

## Known limitations (docs)
- Models are statistical and "doesn't always work perfectly"; PERSON in the training corpus is the bare name without titles like "Mr."/"Dr." (docs' "Expanding named entities" example shows extending spans with rules).

## Project application
- Per review, emit `[{text, label, start_char, end_char}]` from `doc.ents`; offsets let the front end highlight in the original review text without re-running spaCy.
- Group into the app's categories: people (`PERSON`), places (`GPE`/`LOC`/`FAC`), brands (`ORG`), products (`PRODUCT`), plus price/time facts (`MONEY`, `DATE`, `TIME`, `QUANTITY`). Count entities across the corpus with `Counter((ent.text.lower(), ent.label_))`.
- sm mislabels retailers/brands (project smoke test: "Best Buy" as PERSON) — add an EntityRuler before `ner` (see `06-entityruler.md`).
- Mask entity spans (replace with a placeholder) before VADER scoring so brand names do not skew sentiment; use `start_char/end_char` for the replacement.
