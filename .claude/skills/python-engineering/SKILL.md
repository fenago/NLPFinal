---
name: python-engineering
description: "Python 3.12 coding standards for this repo. Use when writing any Python module, script or test."
user-invocable: false
metadata:
  skill-id: S23
  owner: build-pipeline-engineer
  shared-with: [nltk-expert, spacy-expert, dataset-curator, nlp-evaluator, qa-engineer, pyodide-engineer]
---

# Python Engineering (S23)

**Owner:** `build-pipeline-engineer` · **Shared with:** `nltk-expert`, `spacy-expert`, `dataset-curator`, `nlp-evaluator`, `qa-engineer`, `pyodide-engineer`

- Python 3.12; type hints on public functions; `pathlib` for paths; no global state except loaded models.
- Layout: `nlp/` (analyzers), `pipeline/` (build), `scripts/` (one-off data tools), `tests/`.
- Pure functions in `nlp/`; I/O only in `pipeline/` and `scripts/`.
- Deterministic: fixed seeds, sorted outputs, rounded floats.
- Format with `ruff format`; lint with `ruff check` if available.
