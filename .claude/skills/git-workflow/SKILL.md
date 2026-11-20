---
name: git-workflow
description: "Git and GitHub conventions for every agent on this team. Use whenever creating branches, committing, opening pull requests or merging."
user-invocable: false
metadata:
  skill-id: S06
  owner: orchestrator
  shared-with: [meta-agent, nltk-expert, spacy-expert, dataset-curator, build-pipeline-engineer, pyodide-engineer, frontend-engineer, dataviz-specialist, netlify-engineer, qa-engineer, nlp-evaluator, technical-writer]
---

# Git Workflow (S06)

**Owner:** `orchestrator` · **Shared with:** `meta-agent`, `nltk-expert`, `spacy-expert`, `dataset-curator`, `build-pipeline-engineer`, `pyodide-engineer`, `frontend-engineer`, `dataviz-specialist`, `netlify-engineer`, `qa-engineer`, `nlp-evaluator`, `technical-writer`

- Work on a feature branch named `<agent>/<short-task>`; never commit directly to `main` unless the Orchestrator says so.
- Small commits, imperative subject (< 72 chars), body explains why.
- Only touch files you own (see "Who owns which files" in docs/expert-roster.md); ask the owner for changes elsewhere.
- Before pushing: run the relevant tests (`pytest`, Playwright) and the data-contract check.
- Merge with fast-forward or a PR approved by the Orchestrator; never force-push shared branches.
- Never commit secrets, large raw datasets (> 5 MB) or generated `site/data/*.json` unless the contract says it is committed.
