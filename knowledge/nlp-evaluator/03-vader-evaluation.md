# 03 — Evaluating VADER against star ratings

Sources:
- https://github.com/cjhutto/vaderSentiment (README)
- https://www.nltk.org/api/nltk.sentiment.vader.html
- Project docs: /home/user/NLPFinal/docs/02-nltk.md, 04-dataset.md

Fetched: 2026-11-20

## What VADER outputs (README)
- `compound` = sum of lexicon valence scores of words, adjusted by rules, then normalized to [-1, +1]; "the most useful metric if you want a single unidimensional measure".
- Standard thresholds (README: "Typical threshold values"):
  - positive: `compound >= 0.05`
  - neutral: `-0.05 < compound < 0.05`
  - negative: `compound <= -0.05`
- `pos`, `neu`, `neg` are **proportions of text** per raw lexical category (sum ~1) and "do not account for the VADER rule-based enhancements" (word order, degree modifiers, capitalization, punctuation, negation, contrastive conjunctions). Use `compound` for classification, not `pos/neu/neg`.
- README example: `"Not bad at all"` -> `{'pos': 0.487, 'compound': 0.431, 'neu': 0.513, 'neg': 0.0}`.

## NLTK implementation facts (nltk.sentiment.vader)
- `SentimentIntensityAnalyzer().polarity_scores(text)` -> dict with `neg, neu, pos, compound` (class used by docs/02; data package `vader_lexicon`).
- Constants listed in the API page: `B_INCR = 0.293`, `B_DECR = -0.293`, `C_INCR = 0.733`, `N_SCALAR = -0.74`; `normalize(score, alpha=15)` maps to [-1, 1].
- `NEGATE` set includes `not`, `never`, `no`-type words, `without`, `despite`, `rarely`, `seldom`, `nothing`, and contractions like `don't`, `isn't`; `BOOSTER_DICT` covers `very`, `extremely`, `so`, `really` (+) and `slightly`, `somewhat`, `kinda`, `barely`, `hardly` (-).
- `SPECIAL_CASE_IDIOMS`: `'the bomb'`, `'cut the mustard'`, `'yeah right'`, `'hand to mouth'`, `'kiss of death'`, `'the shit'`, `'badass'`.
- Docstring: "Hashtags are not taken into consideration (e.g. #BAD is neutral)."

## Mapping stars -> gold labels (project convention, docs/04)
| rating | gold label |
|---|---|
| 1, 2 | neg |
| 3 | neu |
| 4, 5 | pos |
```python
def star_label(r):  return "neg" if r <= 2 else "neu" if r == 3 else "pos"
def vader_label(c, t=0.05):  return "pos" if c >= t else "neg" if c <= -t else "neu"
```
Caveat to state in the report: **star = author's overall verdict, VADER = tone of the words**; 3-star reviews are often mixed (pos + neg sentences) rather than neutral, so low neutral recall is expected and is a property of the label mapping as much as of VADER.

## Evaluation procedure
1. Score the same sampled reviews (title + text, or text only — pick one and keep it fixed) with `compound`.
2. Predict labels with thresholds +/-0.05 (the standard). Optionally sweep the threshold (e.g. 0.05, 0.1, 0.2, 0.3) and pick on a dev split, report on a held-out split.
3. Metrics: see 01-classification-metrics.md (accuracy, macro-F1, per-class P/R/F1, confusion matrix with fixed label order).
4. Also report 2-class accuracy on 1–2 vs 4–5 only (drop 3-star) as a "polar" upper bound.
5. Report Spearman correlation of `compound` vs rating (SciPy `spearmanr`; not fetched — unverified here) as a threshold-free number.
6. Compare variants: whole review vs per-sentence mean vs entity-masked text (docs/02 lesson 2).

## Known failure modes (documented + from the project's own smoke test)
- **Entity names leak into sentiment**: "Best Buy" scores +0.637 on a purely factual sentence (docs/02 verified output) because "Best" is in the lexicon. Mitigation: mask entities with spaCy first.
- **Mixed reviews**: doc score +0.86 while the sentence "...battery life was disappointing" scores -0.511; whole-review averaging hides complaints; use per-sentence scores.
- **Negation scope** is limited to a window of preceding words (README mentions a negation tri-gram heuristic; wording not re-verified) — long-distance negation ("I wouldn't say that the screen is good") is fragile.
- **Contrastive "but"** is handled by weighting the later clause; sentences without "but" with sequential contrasts ("great at first. Broke in a week.") need sentence splitting.
- **Domain terms**: words neutral in reviews but non-neutral in the lexicon (e.g. "sick", "killer", "cheap", "light") and product-specific negatives ("returned", "refund", "broke") that VADER may not know -> neutral.
- **Sarcasm / irony / questions** and **factual complaints with no sentiment words** ("It stopped working after two days") are typically scored neutral.
- **ALL-CAPS and `!!!`** amplify (rules in README); shouty 1-star reviews may be handled well, shouty praise as well.
- Hashtags ignored (NLTK docstring) — irrelevant for reviews.
- (Failure modes beyond the ones quoted from README/NLTK docs are common expectations to **verify empirically** with 05-error-analysis.md.)

## Project application
- Deliverable: `eval/vader_report.json` containing thresholds, per-class P/R/F1, macro-F1, confusion matrix, 20 worst errors per cell.
- Required baselines in the report: majority-class baseline and "stars>=4 => pos" 2-class baseline, so VADER's numbers have a reference point.
- Run on the same fixed sample as the dashboard (docs/04: stratified equal 1–5 stars, seed 42).
