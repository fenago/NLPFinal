---
name: spacy-noun-chunk-aspects
description: "Turn spaCy noun chunks into normalised aspect phrases (e.g. 'battery life', 'wait time'). Use for most-discussed-aspect lists and aspect keys."
user-invocable: false
metadata:
  skill-id: S16
  owner: spacy-expert
  shared-with: [nltk-expert, dataviz-specialist]
---

# spaCy Noun Chunk Aspects (S16)

**Owner:** `spacy-expert` · **Shared with:** `nltk-expert`, `dataviz-specialist`

- Source: `doc.noun_chunks`; skip chunks whose root is a pronoun.
- Normalise: drop determiners/pronouns, lemmatise, lowercase → "the battery lives" → "battery life".
- Count normalised aspects across the corpus; keep top N per product and per sentiment class.
- Use lemmas (`token.lemma_`) so plurals merge.
- Reference: knowledge/spacy-expert/04-noun-chunks.md.
