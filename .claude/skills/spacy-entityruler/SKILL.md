---
name: spacy-entityruler
description: "Build EntityRuler patterns from dataset metadata (brands, product titles, model numbers) to fix spaCy NER. Use when entities are mislabeled or missed."
user-invocable: false
metadata:
  skill-id: S15
  owner: spacy-expert
  shared-with: [dataset-curator]
---

# spaCy EntityRuler (S15)

**Owner:** `spacy-expert` · **Shared with:** `dataset-curator`

```python
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([{"label": "ORG", "pattern": "Best Buy"},
  {"label": "PRODUCT", "pattern": [{"TEXT": {"REGEX": r"^[A-Z]{1,4}-?\d{2,5}[A-Z0-9]*$"}}]}])
```
- DATA generates `data/entity_patterns.jsonl` from Amazon `store` (→ ORG) and cleaned product titles (→ PRODUCT).
- Phrase patterns for exact names; token patterns for shapes (model numbers).
- Placed before "ner" so the statistical model respects ruler spans.
- Measure before/after with EVAL — don't add patterns that only fit the test examples.
- Reference: knowledge/spacy-expert/06-entityruler.md.
