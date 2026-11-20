---
name: pytest-testing
description: "Write pytest unit and golden-output tests for the NLP modules and build pipeline. Use when adding or changing Python code."
user-invocable: false
metadata:
  skill-id: S38
  owner: qa-engineer
  shared-with: [nltk-expert, spacy-expert, build-pipeline-engineer]
---

# pytest Testing (S38)

**Owner:** `qa-engineer` · **Shared with:** `nltk-expert`, `spacy-expert`, `build-pipeline-engineer`

- `tests/test_nltk_analyzer.py`, `tests/test_spacy_analyzer.py`, `tests/test_build.py`.
- Load spaCy once: `@pytest.fixture(scope="session")`.
- Golden files in `tests/golden/*.json`; compare after rounding.
- Must-have cases: the smoke-test review from docs/02-nltk.md, negation ("not good"), "but" contrast, empty string, emoji, very long review.
- `pytest -q` must pass before any push.
- Reference: knowledge/qa-engineer/01-pytest.md.
