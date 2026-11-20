# 05 — Error analysis (practical method for this project)

Sources:
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html (rows = true, cols = predicted; `labels`, `normalize`)
- https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html (`output_dict`, per-class support)
- https://spacy.io/api/scorer (`ents_per_type`, `score_spans(labeled=False)` for boundary vs label errors)
- https://github.com/cjhutto/vaderSentiment (what VADER's rules do and do not account for)
- https://spacy.io/api/example (`Example.get_aligned_ner`)

Fetched: 2026-11-20

The method itself (bucket, sample, tag, count, fix) is a general engineering practice assembled by this note — it is not prescribed by the cited docs; the docs supply the tools.

## Step 0 — Freeze the setup
Fixed sample (seed 42), fixed library versions (NLTK 3.10.4, spaCy 3.8.18, `en_core_web_sm` 3.8.0 per docs), fixed label mapping (1–2 neg / 3 neu / 4–5 pos), thresholds +/-0.05.

## Step 1 — Find where the errors are (sentiment)
1. Compute the confusion matrix with `labels=["neg","neu","pos"]` (02-confusion-matrix.md).
2. Rank off-diagonal cells by count; the top 2–3 cells are the analysis targets, plus `neg -> pos` always.
3. Dump the rows of each target cell to a CSV:
   ```python
   import pandas as pd
   df["pred"] = df.compound.map(vader_label); df["gold"] = df.rating.map(star_label)
   errs = df[df.pred != df.gold].assign(cell=lambda d: d.gold + "->" + d.pred)
   errs.sort_values("compound", key=abs, ascending=False)        # confident mistakes first
   errs.groupby("cell").head(25).to_csv("eval/vader_errors.csv", index=False)
   ```
   (pandas usage is general, not from the fetched pages.)
4. Sort within a cell by **confidence** (|compound| large but wrong) — those expose systematic causes; near-threshold errors are just noise.

## Step 2 — Tag causes (open coding, then fix a closed list)
Read ~25 per cell; give each a cause tag, then re-tag with a fixed list so counts are comparable:

| Tag | Meaning | Typical fix |
|---|---|---|
| `entity_leak` | brand/product word carried sentiment (e.g. "Best Buy") | spaCy entity masking before VADER |
| `mixed` | positive + negative sentences in one review | per-sentence scoring / show both |
| `negation` | "not ... good", long-distance negation | rule patch or flag only |
| `no_sentiment_words` | factual complaint ("stopped working after two days") | domain lexicon additions |
| `domain_word` | "sick", "cheap", "light" mis-valenced | `analyzer.lexicon.update({...})` (lexicon is a dict; project idea) |
| `sarcasm` | irony | document as limitation |
| `star_noise` | text is positive, rating low (or reverse) — **label problem, not model** | exclude/report |
| `too_short` | 1–3 word review | document |
| `other` | — | — |

The share of `star_noise` + `mixed` bounds the achievable accuracy; report it explicitly.

## Step 3 — Error analysis for NER
1. Run `Scorer.score(examples)` and print `ents_per_type` (04-ner-evaluation.md).
2. Re-run `Scorer.score_spans(examples, "ents", labeled=False)`: unlabeled F >> labeled F => **label confusion**; both low => **boundary / missed** entities.
3. Build three lists by comparing gold vs predicted spans per review (offsets `(start,end,label)`):
   - **FN** (gold not predicted), **FP** (predicted not in gold), **label swap** (same span, different label), **boundary** (overlap, different span).
4. Tag causes: `retailer_as_person` ("Best Buy" -> PERSON), `model_number_missed` ("WH-1000XM5"), `generic_noun_as_ORG`, `lowercase_brand`, `typo`, `gold_error`.
5. Fix proposals map to docs/03: `EntityRuler` patterns before `ner`; regex for model numbers; brand list from metadata. Re-measure on the **frozen gold set**, not on the reviews used to design patterns.

## Step 4 — Error analysis for aspect <-> opinion pairs (docs/03 rules)
No official metric exists; use a small hand-checked sample: for 50 reviews list the extracted `(aspect, opinion)` pairs and mark each correct / incorrect / missing; report precision on extracted pairs and recall on the hand-listed gold pairs. Tag causes: `neg_not_flipped`, `wrong_head`, `pronoun_aspect`, `chunk_too_long`.

## Step 5 — Quantify, fix, re-measure
1. Count tags per cell (a table: cause x cell).
2. Pick the top 1–2 fixes by count x ease; implement; re-run the full evaluation; record **before/after** macro-F1 and per-class deltas in a table.
3. Keep every analysis CSV in `eval/` with the commit hash and library versions.

## Reporting template
```
Setup: n=..., versions, thresholds
Headline: acc, macro-F1 (per-class P/R/F1 + support)
Confusion matrix (counts + row-normalized)
Top error causes (table above, counts) with 2 verbatim examples each
Change tried -> metric before/after
Limitations: star noise, 3-star mixed reviews, gold set size
```

## Project application
- Owner: nlp-evaluator; hand the QA engineer any stable bad cases as xfail goldens (see qa-engineer/02-snapshot-golden-tests.md).
- Avoid reading only the first N rows; sample with a seed so the analysis is reproducible.
- Never tune thresholds/patterns on the data you report final numbers on — split dev (error analysis) / test (final report).
