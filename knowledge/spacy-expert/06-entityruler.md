# 06 — EntityRuler (rule-based entities for brands and products)

Sources:
- https://spacy.io/api/entityruler
- https://spacy.io/usage/rule-based-matching (section "Rule-based entity recognition", PhraseMatcher, token patterns)

Fetched: 2026-11-20

## What it is
- `entity_ruler` pipeline component adds spans to `doc.ents` using **phrase patterns** or **token patterns**. Can complement the statistical `ner` or run alone (purely rule-based NER).
- Note: the fetched rule-based-matching page also describes the newer `SpanRuler` (v3.3.1), "a generalized version of the entity ruler" writing to `doc.spans["ruler"]` or `doc.ents`; the EntityRuler docs were still current when fetched. Whether EntityRuler is deprecated in 3.8 is **(unverified)**; this project can keep using it.

## Pattern formats (dict with `label` and `pattern`, optional `id`)
```python
{"label": "ORG", "pattern": "Apple"}                                   # phrase pattern (str, exact match)
{"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]}   # token pattern (list of per-token dicts)
{"label": "ORG", "pattern": "Apple", "id": "apple"}                    # id -> ent.ent_id_
```
- Token patterns accept Matcher attributes: `LOWER`, `TEXT`, `IS_PUNCT`, `POS`, `TAG`, `SHAPE`, and operators like `{"TEXT": {"REGEX": "^[A-Z]{1,4}-?\\d{2,5}[A-Z0-9]*$"}}` (REGEX works on any string attribute, e.g. `{"TAG": {"REGEX": "^V"}}`).
- Phrase patterns are tokenized with `nlp` so you need not mirror tokenization ("Washington, D.C." works).

## Adding to the pipeline
```python
import spacy
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler", before="ner")      # ruler runs first; ner respects its spans
ruler.add_patterns([
    {"label": "ORG", "pattern": "Best Buy"},
    {"label": "PRODUCT", "pattern": [{"TEXT": {"REGEX": r"^[A-Z]{1,4}-?\d{2,5}[A-Z0-9]*$"}}]},
])
doc = nlp("Sony WH-1000XM5 bought at Best Buy")
[(e.text, e.label_) for e in doc.ents]
```
- **Before `ner`** (docs): the entity recognizer "will respect the existing entity spans and adjust its predictions around it", which can significantly improve accuracy.
- **After `ner`** (default `last`): the ruler only adds spans that do not overlap model entities, unless `overwrite_ents=True`.
- `nlp.add_pipe("entity_ruler", config={"overwrite_ents": True, "phrase_matcher_attr": "LOWER", "validate": True})`.

## Config / init settings
| Setting | Default | Meaning |
| --- | --- | --- |
| `phrase_matcher_attr` | `None` | attribute for phrase matching; `"LOWER"` = case-insensitive phrase patterns; `"POS"` possible |
| `validate` | `False` | validate patterns against JSON schema (helps debugging) |
| `overwrite_ents` | `False` | replace existing (model) entities on overlap |
| `ent_id_sep` | `"||"` | separator used internally for ids |
| `matcher_fuzzy_compare` | levenshtein (v3.5) | fuzzy comparison for the internal Matcher |
| `scorer` | `get_ner_prf` | scoring function |

## Overlap rules
- Among overlapping rule matches, the **longer** match wins; if equal length, the one **first in the Doc**.
- Each token can have only one entity label; entities must be non-overlapping.

## Methods and attributes (EntityRuler API)
| API | Notes |
| --- | --- |
| `ruler.add_patterns(patterns)` | list of dicts; phrase patterns are run through `nlp.pipe` |
| `ruler.patterns` | all patterns (one dict each) |
| `ruler.labels` / `ruler.ent_ids` | labels / ids present in patterns |
| `len(ruler)`, `label in ruler` | pattern count / membership |
| `ruler.remove(ent_id)` (v3.2.1) | remove by pattern id; `ValueError` if absent |
| `ruler.to_disk(path)` / `ruler.from_disk(path)` | JSONL file (`*.jsonl`) or a directory containing `patterns.jsonl` + `cfg` |
| `ruler.to_bytes()` / `from_bytes()` | serialize patterns |
| `ruler.initialize(get_examples, nlp=, patterns=)` | used before training |

## Pattern files (JSONL, one pattern per line)
```json
{"label": "ORG", "pattern": "Apple"}
{"label": "GPE", "pattern": [{"LOWER": "san"}, {"LOWER": "francisco"}]}
```
```python
ruler.to_disk("./patterns.jsonl")
new_ruler = nlp.add_pipe("entity_ruler").from_disk("./patterns.jsonl")
```
- `nlp.to_disk("/path/to/pipeline")` also saves the ruler (its `patterns.jsonl` and entry in `config.cfg`); loading restores it.
- Use the `.jsonl` suffix: `from_disk` with a `.jsonl` path reads patterns directly.

## Many phrase patterns (> ~10,000)
Each phrase pattern is passed through the nlp pipeline to build a Doc; speed it up by running only needed pipes while adding:
```python
with nlp.select_pipes(enable="tagger"):     # docs example; use enable=[] / minimal for pure text patterns (unverified)
    ruler.add_patterns(big_list)
```
Alternative for large lists: `PhraseMatcher(nlp.vocab, attr="LOWER")` with `[nlp.make_doc(t) for t in terms]` (fast; only tokenizes).

## Pitfalls
- Order matters: a ruler *after* `ner` loses to model mistakes unless `overwrite_ents=True`.
- Phrase patterns are case-sensitive unless `phrase_matcher_attr="LOWER"`.
- Adding patterns on an `nlp` with no patterns triggers a warning (W036) when run — add patterns before processing.
- `PERSON` spans from the model do not include titles; use rules to expand if needed (docs' "Expanding named entities").

## Project application
- Generate patterns at build time from dataset metadata: Amazon `store`/`brand` → `{"label":"ORG"}`, `title`-derived product lines/model numbers → `{"label":"PRODUCT"}`; Yelp business names → `ORG`/`FAC` (restaurants). Write them to `data/patterns.jsonl`, commit it, and reload with `from_disk` so builds are reproducible.
- Add model-number regex token patterns (e.g. `WH-1000XM5`) as `PRODUCT`; keep a generic regex narrow to avoid false positives on words like "USB-C" (decide by test).
- Use `id` to merge aliases ("Best Buy"/"BestBuy") so brand counts aggregate via `ent.ent_id_`.
- Place with `before="ner"` so brand names stop being mislabeled (e.g. "Best Buy" as PERSON in the project's smoke test) and downstream sentiment masking uses the corrected spans.
