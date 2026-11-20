---
name: nltk-pyodide-compat
description: "Write NLTK code that runs identically at build time (NLTK 3.10.x) and in Pyodide (NLTK 3.9.x). Use when editing nlp/nltk_analyzer.py or anything the browser executes."
user-invocable: false
metadata:
  skill-id: S12
  owner: nltk-expert
  shared-with: [pyodide-engineer, qa-engineer]
---

# NLTK Pyodide Compat (S12)

**Owner:** `nltk-expert` · **Shared with:** `pyodide-engineer`, `qa-engineer`

- One shared module: `nlp/nltk_analyzer.py`, pure functions, input str → output dict (JSON-serialisable).
- Allowed APIs: sent_tokenize, word_tokenize, stopwords, SentimentIntensityAnalyzer, FreqDist, ngrams, collocation finders.
- No `nltk.download()`, no file paths except `nltk.data`, no threads, no network.
- Round floats to 3 decimals so build and browser outputs compare equal in tests.
- QA runs the same golden inputs through CPython and Pyodide and diffs the JSON.
