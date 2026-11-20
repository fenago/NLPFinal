# 04 — Evaluating spaCy NER (Scorer, Example, hand-labelled gold set)

Sources:
- https://spacy.io/api/scorer
- https://spacy.io/api/example
- https://spacy.io/api/language (Language.evaluate)
- https://spacy.io/api/data-formats (dict format for Example.from_dict)
- https://spacy.io/usage/training (DocBin / `.spacy` format, `char_span`)
- Project docs: /home/user/NLPFinal/docs/03-spacy.md, 04-dataset.md

Fetched: 2026-11-20

## Scorer (spacy.io/api/scorer)
- `Scorer(nlp=None, default_lang="xx", default_pipeline=("senter","tagger","morphologizer","parser","ner","textcat"), **kwargs)`.
- `Scorer.score(examples, *, per_component=False)` (per_component since v3.6) — "Calculate the scores for a list of Example objects using the scoring methods provided by the components in the pipeline." Returns `Dict[str, Union[float, Dict[str, float]]]`.
- NER keys: `ents_p`, `ents_r`, `ents_f`, `ents_per_type` (per-label P/R/F dict).
- `Scorer.score_spans(examples, attr, *, getter=getattr, has_annotation=None, labeled=True, allow_overlap=False)` — "Returns PRF scores for labeled or unlabeled spans." Returns `{attr}_p`, `{attr}_r`, `{attr}_f` and `{attr}_per_type`.
  - `labeled=False` -> two spans are equal if start and end match irrespective of label (use this to separate **boundary** errors from **label** errors).
  - `has_annotation(doc)` -> docs without annotation are skipped.
  - `getter(doc, attr)` lets you score custom span sets (e.g. only brand entities).
- Matching is **exact span + label** (entity-level micro P/R/F; "labeled" semantics above). A partially overlapping span counts as both a false positive and a false negative.

## Example (spacy.io/api/example)
- `Example(predicted, reference)` — predicted Doc (what the pipeline produced) and reference Doc (gold).
- `Example.from_dict(predicted_doc, example_dict)`; the dict format (data-formats page):
  ```python
  doc = nlp("Laura flew to Silicon Valley.")
  gold_dict = {"entities": [(0, 5, "PERSON"), (14, 28, "LOC")]}   # (start_char, end_char, label)
  example = Example.from_dict(doc, gold_dict)
  ```
  Alternative: BILUO tags per token, e.g. `{"entities": ["U-PERS","O","O","B-LOC","L-LOC"]}`.
- `Example.get_aligned_ner()` returns spans aligned to the reference tokenization.
- Import: `from spacy.training import Example` (import path is standard spaCy 3; not shown in the excerpts).

## Language.evaluate (spacy.io/api/language)
`nlp.evaluate(examples, *, batch_size=None, scorer=None, component_cfg=None, scorer_cfg=None, per_component=False)` -> dict of scores. Note: the examples' `predicted` doc is re-processed by the pipeline in `evaluate`, so pass `Example.from_dict(nlp.make_doc(text), gold)` (typical pattern; `make_doc` not in the excerpts — unverified) rather than an already-annotated doc.

```python
import spacy
from spacy.training import Example
nlp = spacy.load("en_core_web_sm")            # + EntityRuler as in docs/03
gold = [  # hand-labelled
  ("I ordered the Sony WH-1000XM5 headphones from Best Buy in Chicago.",
   {"entities": [(18, 23, "ORG"), (24, 34, "PRODUCT"), (50, 58, "ORG"), (62, 69, "GPE")]}),
]
examples = [Example.from_dict(nlp.make_doc(t), a) for t, a in gold]
scores = nlp.evaluate(examples)
print(scores["ents_p"], scores["ents_r"], scores["ents_f"])
print(scores["ents_per_type"])     # {'ORG': {'p':..,'r':..,'f':..}, ...}
```
(Character offsets above are illustrative — compute them with `text.index(...)` in real code and verify with `doc.char_span(start, end)` which returns `None` if offsets do not align to token boundaries — docs/usage/training uses `char_span` this way.)

## Building a small hand-labelled gold set
1. **Sample**: 100–200 reviews from `data/reviews_sample.jsonl`, stratified by rating and (if two modes) by domain; fixed seed; keep ids.
2. **Annotate** only the labels the app shows: `PERSON`, `GPE` (+`LOC`,`FAC`), `ORG` (brands/stores), `PRODUCT`. Write a one-page guideline first (examples: "Best Buy" = ORG; model numbers like "WH-1000XM5" = PRODUCT; staff first names = PERSON; generic "customer service" = nothing; "Amazon" = ORG).
3. **Format**: one JSONL line per review: `{"id":..., "text":..., "entities":[[start,end,"ORG"],...]}` using character offsets.
4. **Validate**: script that loads each line, calls `nlp.make_doc(text).char_span(s, e, label=l)` and fails on `None` (misaligned) or overlapping spans.
5. **Second pass**: re-label 20 reviews after a few days (or by a teammate) and compute agreement with `Scorer.score_spans(..., labeled=True)`-style P/R/F between the two label sets; report it as the ceiling.
6. **Optionally convert** to `DocBin` (`doc.ents = spans; DocBin().add(doc); to_disk("gold.spacy")`, from usage/training) so the CLI evaluator can use it (`python -m spacy evaluate model gold.spacy` — CLI existence is standard spaCy 3, flags **unverified** here).
7. **Freeze** the gold file in `tests/gold/ner_gold.jsonl`; never use it to build EntityRuler patterns (leakage). Build patterns from Amazon `store`/`title` metadata only (docs/03, docs/04).

## Interpreting scores
- Report **before/after EntityRuler** (docs/03: small model tags "Best Buy" as PERSON, misses "WH-1000XM5").
- Always show `ents_per_type`; macro over types is not given by spaCy — compute from `ents_per_type` if wanted.
- Run once with `labeled=False` span scoring: if unlabeled F is much higher than labeled F, the problem is labels (ORG vs PERSON); if both low, boundaries/missed mentions.
- Small gold sets give wide uncertainty: with ~300 gold entities, +/- a few points is noise; say so in the report.

## Project application
- Gold set size target: ~150 reviews / ~300–400 entity mentions.
- Deliverable: `eval/ner_report.json` with micro P/R/F, per-type table, 15 example errors per type.
- Metadata check (docs/04 idea): fraction of Amazon `store` brand names found as ORG in reviews that mention them — a cheap, label-free recall proxy.
