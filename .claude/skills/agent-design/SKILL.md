---
name: agent-design
description: "Write and update Claude Code subagent files (.claude/agents/*.md) and skills (.claude/skills/*/SKILL.md) for this team. Use when adding, splitting, renaming or re-scoping an agent or skill."
user-invocable: false
metadata:
  skill-id: S03
  owner: meta-agent
  shared-with: [orchestrator]
---

# Agent Design (S03)

**Owner:** `meta-agent` · **Shared with:** `orchestrator`

- Subagent file: YAML frontmatter first line `---`; required `name` (kebab-case, no `:`) and `description` (when to delegate). Optional: `tools`, `model` (opus | sonnet | haiku | inherit), `skills` (preloaded in full, max 32), `color`, `memory`, `effort`.
- Body = the agent's whole system prompt. Include: persona, mission, "Before you answer: read knowledge/<agent>/INDEX.md and every note it lists", owned files, handoffs, guardrails, output format.
- Skill: `.claude/skills/<name>/SKILL.md`, `description` puts the use case first (listing truncates at 1,536 chars). Keep SKILL.md < 500 lines; move detail to supporting files or knowledge/.
- Do not set `disable-model-invocation: true` on a skill an agent preloads — preloading would then fail.
- Keep docs/expert-roster.md, docs/agent-brains.md and CLAUDE.md in sync with any change.
- Reference: knowledge/meta-agent/.
