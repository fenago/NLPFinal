---
name: spacy-vader-fusion
description: "Combine spaCy structure with NLTK VADER scores: entity masking before sentiment and per-aspect sentiment. Use whenever both libraries touch the same review."
user-invocable: false
metadata:
  skill-id: S18
  owner: spacy-expert
  shared-with: [nltk-expert, nlp-evaluator]
---

# spaCy VADER Fusion (S18)

**Owner:** `spacy-expert` · **Shared with:** `nltk-expert`, `nlp-evaluator`

- Entity masking: replace each `doc.ents` span (ORG, PRODUCT, PERSON, GPE, FAC, LOC) with a neutral token like `ENT` before `polarity_scores` — stops "Best Buy" scoring positive.
- Aspect sentiment: for each (aspect, opinion, negated) pair, score = VADER compound of the opinion phrase; flip sign if negated.
- Aggregate per aspect: mean score, count, share positive/negative.
- Output both raw and masked sentiment so EVAL can measure the effect.
- This is build-time only (needs spaCy).
