---
name: spacy-pipeline
description: "Load and run spaCy's en_core_web_sm pipeline efficiently over the review dataset at build time. Use when writing nlp/spacy_analyzer.py or tuning build speed."
user-invocable: false
metadata:
  skill-id: S13
  owner: spacy-expert
  shared-with: [build-pipeline-engineer]
---

# spaCy Pipeline (S13)

**Owner:** `spacy-expert` · **Shared with:** `build-pipeline-engineer`

- Pin: `spacy==3.8.18` and `en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl`.
- Load once: `nlp = spacy.load("en_core_web_sm")`; add EntityRuler before "ner".
- Batch: `for doc in nlp.pipe(texts, batch_size=256)`.
- Disable what you don't use with `nlp.select_pipes(disable=[...])` — we need tagger, parser, attribute_ruler, lemmatizer, ner.
- spaCy never runs in the browser (not in Pyodide).
- Reference: knowledge/spacy-expert/01-pipelines.md, 02-en-core-web-sm.md.
