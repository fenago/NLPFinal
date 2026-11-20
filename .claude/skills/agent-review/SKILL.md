---
name: agent-review
description: "Review how well each agent performed and improve its prompt, skills or knowledge. Use after each phase or when an agent produced wrong, off-scope or low-quality work."
user-invocable: false
metadata:
  skill-id: S04
  owner: meta-agent
  shared-with: [orchestrator, nlp-evaluator]
---

# Agent Review (S04)

**Owner:** `meta-agent` · **Shared with:** `orchestrator`, `nlp-evaluator`

- For each agent: what was asked, what it delivered, defects found by QA/EVAL, scope violations.
- Classify the root cause: missing knowledge (add a note to knowledge/<agent>/), unclear instructions (edit the agent body), wrong skill (edit or add a skill), wrong model (propose a model change).
- Make the smallest change that fixes the cause; record it in `docs/agent-changelog.md` (date, agent, change, reason).
- Never weaken a guardrail (Netlify constraints, data contract, tests) to make an agent "pass".
