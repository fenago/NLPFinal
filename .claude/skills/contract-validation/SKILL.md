---
name: contract-validation
description: "Validate every site/data JSON file against the JSON Schemas of the data contract. Use after each build and in CI-style checks."
user-invocable: false
metadata:
  skill-id: S39
  owner: qa-engineer
  shared-with: [build-pipeline-engineer, frontend-engineer]
---

# Contract Validation (S39)

**Owner:** `qa-engineer` · **Shared with:** `build-pipeline-engineer`, `frontend-engineer`

```python
from jsonschema import Draft202012Validator
Draft202012Validator(schema).validate(data)
```
- One schema per file in `schemas/`; test iterates over `site/data/*.json`.
- Also check `contract_version` matches `docs/data-contract.md`.
- Validate Pyodide live output against the same per-review NLTK schema.
