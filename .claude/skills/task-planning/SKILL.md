---
name: task-planning
description: "Break the Customer Review Analyzer into ordered tasks with owners, dependencies and milestones. Use when planning a phase, assigning work to subagents, or re-planning after a blocker."
user-invocable: false
metadata:
  skill-id: S01
  owner: orchestrator
  shared-with: [meta-agent]
---

# Task Planning (S01)

**Owner:** `orchestrator` · **Shared with:** `meta-agent`

- Plan in the four phases from docs/expert-roster.md: Design → Build → Test → Deploy.
- Every task has: one owner agent, inputs (files it needs), outputs (files it writes), done-criteria, reviewers.
- Respect the handoff order: data contract (gate 1) → dataset → NLTK + spaCy modules → build pipeline → Pyodide/UI/charts → tests + evaluation (gate 2) → production deploy.
- Run independent tasks in parallel (e.g. NLTK and spaCy modules; UI and charts), dependent ones in sequence.
- Keep the plan in `docs/plan.md` as a checklist; update status after every handoff.
- When a task is blocked, record the blocker, the owner who can unblock it, and the fallback.
