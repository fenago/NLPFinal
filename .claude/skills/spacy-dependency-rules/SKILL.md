---
name: spacy-dependency-rules
description: "Link opinion words to the aspects they describe using spaCy's dependency parse. Use when building or debugging aspect\u2194opinion extraction."
user-invocable: false
metadata:
  skill-id: S17
  owner: spacy-expert
  shared-with: [nltk-expert, nlp-evaluator]
---

# spaCy Dependency Rules (S17)

**Owner:** `spacy-expert` · **Shared with:** `nltk-expert`, `nlp-evaluator`

Rules (verified on the smoke-test review in docs/03-spacy.md):
1. `amod`: adjective modifying a noun → (head noun chunk, adjective). "amazing noise cancelling".
2. `acomp` + `nsubj`: "battery life was disappointing" → (subject chunk, complement).
3. Negation: a `neg` child on the opinion or its head flips polarity ("was not helpful").
- Expand the aspect token to its full noun chunk.
- Score the opinion word with VADER (see spacy-vader-fusion).
- Keep rules few and explainable; EVAL measures precision on a hand-checked sample.
- Reference: knowledge/spacy-expert/05-dependency-parse.md.
