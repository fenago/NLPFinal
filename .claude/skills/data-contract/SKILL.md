---
name: data-contract
description: "Define and follow the JSON contract between the Python build and the static site (site/data/*.json). Use when producing or consuming any site/data file or changing a field."
user-invocable: false
metadata:
  skill-id: S21
  owner: build-pipeline-engineer
  shared-with: [orchestrator, nltk-expert, spacy-expert, pyodide-engineer, frontend-engineer, dataviz-specialist]
---

# Data Contract (S21)

**Owner:** `build-pipeline-engineer` · **Shared with:** `orchestrator`, `nltk-expert`, `spacy-expert`, `pyodide-engineer`, `frontend-engineer`, `dataviz-specialist`

- Contract lives in `docs/data-contract.md` + `schemas/*.schema.json` (JSON Schema 2020-12).
- Proposed files: `summary.json` (counts, sentiment distribution, VADER-vs-stars matrix), `reviews.json` (per-review: id, rating, text, sentiment, sentences, entities, aspects), `collocations.json`, `aspects.json`, `entities.json` (people/places/brands/products leaderboards), `examples.json` (curated full-spaCy demos), `meta.json` (versions, build time, contract version).
- Every file has `"contract_version"`. Breaking change → bump major + Orchestrator approval.
- Pyodide live output uses the same shape as the NLTK part of `reviews.json`.
