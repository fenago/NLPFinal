---
name: error-analysis
description: "Find and categorise NLP errors and feed concrete fixes back to the NLTK and spaCy experts. Use after metrics are computed."
user-invocable: false
metadata:
  skill-id: S42
  owner: nlp-evaluator
  shared-with: [nltk-expert, spacy-expert, technical-writer]
---

# Error Analysis (S42)

**Owner:** `nlp-evaluator` · **Shared with:** `nltk-expert`, `spacy-expert`, `technical-writer`

- Sample errors from each confusion-matrix cell and each NER false positive/negative.
- Tag each: sarcasm, domain slang, negation scope, entity leak, mislabeled brand, missed model number, parser error.
- Count tags → top 3 causes → one proposed fix each, owner named (NLTK or SPACY).
- Write findings to `reports/evaluation.md`; DOC uses them in "Limitations".
