---
name: nltk-vader
description: "Score review sentiment with NLTK's VADER, per review and per sentence. Use for any sentiment feature, label threshold or sentiment bug."
user-invocable: false
metadata:
  skill-id: S09
  owner: nltk-expert
  shared-with: [pyodide-engineer, nlp-evaluator]
---

# NLTK VADER (S09)

**Owner:** `nltk-expert` · **Shared with:** `pyodide-engineer`, `nlp-evaluator`

```python
from nltk.sentiment import SentimentIntensityAnalyzer   # data: vader_lexicon
sia = SentimentIntensityAnalyzer()
s = sia.polarity_scores(text)      # {'neg','neu','pos','compound'}
label = "positive" if s["compound"] >= 0.05 else "negative" if s["compound"] <= -0.05 else "neutral"
```
- Always also score each sentence (`sent_tokenize`) — mixed reviews hide complaints in the overall score.
- VADER handles negation, intensifiers, ALL CAPS, `!`, and contrastive "but".
- Known issue: entity names leak sentiment ("Best Buy" → +0.64). Mask entity spans first when spaCy entities are available (build time).
- Limitations: sarcasm, domain slang, English only. Report them, don't hide them.
- Reference: knowledge/nltk-expert/03-vader.md.
