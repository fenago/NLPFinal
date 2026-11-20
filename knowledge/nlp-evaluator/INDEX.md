# NLP Evaluator knowledge — index

Fetched 2026-11-20 from official docs. Project context: /home/user/NLPFinal/docs (02-nltk, 03-spacy, 04-dataset).

| File | Use it when | Primary sources |
|---|---|---|
| 01-classification-metrics.md | Computing accuracy, per-class P/R/F1, macro vs weighted averages, `classification_report` | scikit-learn 1.9.1 API pages |
| 02-confusion-matrix.md | Building/plotting/reading the neg-neu-pos matrix; fixed `labels` order; `normalize` | scikit-learn `confusion_matrix`, `ConfusionMatrixDisplay` |
| 03-vader-evaluation.md | Stars -> labels, +/-0.05 thresholds, VADER facts and failure modes | github.com/cjhutto/vaderSentiment, nltk.org VADER API |
| 04-ner-evaluation.md | spaCy `Scorer`, `Example.from_dict`, `nlp.evaluate`, building a gold set | spacy.io/api (scorer, example, language, data-formats), usage/training |
| 05-error-analysis.md | Bucketing and tagging mistakes, fix-and-remeasure loop | scikit-learn + spaCy docs (method is project-specific) |

## Evaluation checklist
1. Freeze sample (seed 42), versions, label mapping (1–2 neg / 3 neu / 4–5 pos), thresholds.
2. Sentiment: accuracy + macro-F1 + per-class table + confusion matrix (`labels=["neg","neu","pos"]`).
3. Compare variants: raw vs entity-masked, whole review vs per-sentence.
4. NER: hand-labelled gold (~150 reviews), `nlp.evaluate` before/after EntityRuler, `ents_per_type`.
5. Error analysis: top confusion cells, cause tags, before/after table.
6. Deliver JSON + PNG in `eval/`; hand stable failures to qa-engineer as goldens.

## Known gaps / unverified
- `ConfusionMatrixDisplay.from_predictions` parameters and `spacy evaluate` CLI flags not extracted.
- Spearman correlation (SciPy) and pandas snippets are general knowledge, not from fetched pages.
- VADER README negation/"but" details only partly re-quoted; failure modes beyond quoted text must be confirmed empirically.
- Character offsets in the NER example are illustrative.
