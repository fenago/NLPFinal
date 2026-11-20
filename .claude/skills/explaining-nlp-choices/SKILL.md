---
name: explaining-nlp-choices
description: "Explain why each feature uses NLTK or spaCy, and the known limits, in plain language. Use for the report, About page and presentation."
user-invocable: false
metadata:
  skill-id: S44
  owner: technical-writer
  shared-with: [nltk-expert, spacy-expert, nlp-evaluator]
---

# Explaining NLP Choices (S44)

**Owner:** `technical-writer` · **Shared with:** `nltk-expert`, `spacy-expert`, `nlp-evaluator`

- NLTK = classic, transparent algorithms (tokenizers, VADER lexicon rules, corpus statistics); runs in the browser via Pyodide.
- spaCy = trained industrial pipeline (NER, parser, lemmatizer); build time only on Netlify.
- Combined = aspect-based sentiment and entity-masked sentiment.
- Limits: VADER sarcasm/slang; small-model NER errors; no spaCy on live text because Netlify has no Python runtime and Pyodide lacks spaCy.
- Use the division-of-labour table in docs/03-spacy.md.
