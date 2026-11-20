---
name: approval-gates
description: "Run go/no-go gates: check deliverables against the data contract, tests and deploy preview before merging or releasing. Use at gate 1 (contract), gate 2 (tests + evaluation) and the production release."
user-invocable: false
metadata:
  skill-id: S02
  owner: orchestrator
  shared-with: [qa-engineer, netlify-engineer]
---

# Approval Gates (S02)

**Owner:** `orchestrator` · **Shared with:** `qa-engineer`, `netlify-engineer`

Gate 1 — Data contract: `docs/data-contract.md` exists; BUILD, UI, VIZ, PYO, NLTK, SPACY have all signed off.
Gate 2 — Quality: `pytest` green; Playwright green on the deploy preview; JSON validates against the schema; `reports/evaluation.md` exists with numbers; size budgets met (see data-size-budget skill).
Release: deploy preview URL checked by QA; NET confirms build log clean; DOC links updated.

Rules:
- A gate passes only with evidence (command output, URL, file path). "Looks fine" is not evidence.
- On fail: name the failing check, the owner, and the exact fix requested. Do not fix it yourself.
- Never merge to `main` with a red test or an unapproved contract change.
