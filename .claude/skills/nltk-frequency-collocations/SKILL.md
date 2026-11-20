---
name: nltk-frequency-collocations
description: "Find top words and statistically significant key phrases with NLTK FreqDist and collocation finders. Use for keyword lists, key-phrase charts and per-sentiment word comparisons."
user-invocable: false
metadata:
  skill-id: S10
  owner: nltk-expert
  shared-with: [build-pipeline-engineer, dataviz-specialist]
---

# NLTK Frequency Collocations (S10)

**Owner:** `nltk-expert` · **Shared with:** `build-pipeline-engineer`, `dataviz-specialist`

```python
fd = nltk.FreqDist(words); fd.most_common(20)
f = BigramCollocationFinder.from_words(words)
f.apply_freq_filter(3)                       # essential on real corpora
f.nbest(BigramAssocMeasures.likelihood_ratio, 20)   # or .pmi
```
- Collocations are corpus-level: compute at build time per product / per sentiment class.
- In Pyodide (single review) show top words and plain bigram counts, not PMI.
- Filter tokens with the project stopword list first; use `TrigramCollocationFinder` for 3-word phrases.
- Reference: knowledge/nltk-expert/04-freqdist.md, 05-collocations.md.
