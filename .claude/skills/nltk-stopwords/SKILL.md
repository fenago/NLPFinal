---
name: nltk-stopwords
description: "Build the project's stopword list from NLTK's English stopwords. Use when filtering tokens for frequencies, keywords, collocations or aspect counts."
user-invocable: false
metadata:
  skill-id: S08
  owner: nltk-expert
  shared-with: [spacy-expert, nlp-evaluator]
---

# NLTK Stopwords (S08)

**Owner:** `nltk-expert` · **Shared with:** `spacy-expert`, `nlp-evaluator`

```python
from nltk.corpus import stopwords
NEGATIONS = {"not", "no", "nor", "don't", "won't", "isn't", "wasn't", "didn't", "never"}
DOMAIN = {"product", "item", "order", "would", "get", "place", "restaurant"}
STOP = (set(stopwords.words("english")) - NEGATIONS) | DOMAIN
```
- NLTK English list has 198 words (NLTK 3.10.4).
- Never remove stopwords before VADER — negations, "but" and intensifiers matter.
- spaCy side may use `token.is_stop`; keep both lists consistent for negations.
- Reference: knowledge/nltk-expert/02-stopwords.md.
