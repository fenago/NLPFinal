---
name: nlp-metrics
description: "Measure NLP quality: VADER vs star ratings and NER precision/recall/F1. Use when producing reports/evaluation.md or comparing variants."
user-invocable: false
metadata:
  skill-id: S41
  owner: nlp-evaluator
  shared-with: [nltk-expert, spacy-expert]
---

# NLP Metrics (S41)

**Owner:** `nlp-evaluator` · **Shared with:** `nltk-expert`, `spacy-expert`

- Sentiment: stars → labels (1–2 neg, 3 neu, 4–5 pos); report accuracy, macro-F1, confusion matrix (labels order neg, neu, pos); compare raw vs entity-masked VADER.
- NER: hand-label 100 reviews (people/places/brands/products); report P/R/F1 per group, with and without EntityRuler.
- Aspect pairs: precision on 100 sampled pairs, hand-checked.
- Tools: scikit-learn metrics at analysis time (not needed in the site build).
- Reference: knowledge/nlp-evaluator/.
