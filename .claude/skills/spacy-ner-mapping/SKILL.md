---
name: spacy-ner-mapping
description: "Extract named entities with spaCy and map labels to the app's People, Places, Brands and Products groups. Use for entity extraction, leaderboards or NER evaluation."
user-invocable: false
metadata:
  skill-id: S14
  owner: spacy-expert
  shared-with: [dataviz-specialist, nlp-evaluator]
---

# spaCy NER Mapping (S14)

**Owner:** `spacy-expert` · **Shared with:** `dataviz-specialist`, `nlp-evaluator`

| spaCy label | App group |
|---|---|
| PERSON | people |
| GPE, LOC, FAC | places |
| ORG | brands |
| PRODUCT | products |
| MONEY, DATE, TIME, QUANTITY | details (optional) |

- Normalise entity text for counting (strip, collapse spaces, case-fold for keys, keep display form).
- Known errors of the small model: retailers as PERSON ("Best Buy"), missed model numbers — fix with the EntityRuler skill.
- Use `spacy.explain(label)` for UI tooltips.
- Reference: knowledge/spacy-expert/03-named-entities.md.
