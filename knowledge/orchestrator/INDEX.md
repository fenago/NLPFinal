# Orchestrator Knowledge Index

Fetched: 2026-11-20. Real notes from official docs; read the file that matches the question.

| File | Use it when | Sources |
|---|---|---|
| 01-subagents-delegation.md | Writing delegation prompts; choosing foreground/background, chaining, parallel fan-out; limits (20 concurrent, depth 3); what a subagent sees at startup; resuming with SendMessage | code.claude.com/docs/en/sub-agents |
| 02-agent-teams-and-workflows.md | Deciding subagents vs experimental agent teams; plan mode, worktrees, PR creation, resume | code.claude.com/docs/en/agent-teams, /common-workflows |
| 03-git-workflow.md | Branching, `--ff-only` merges, PR review flow, branch cleanup | git-scm.com/docs/git-branch, git-merge; docs.github.com pull requests |

Quick facts
- Subagents start with a fresh context: restate rules and file ownership in each delegation prompt.
- Default limits: 20 concurrent subagents, 3 nesting layers.
- Agent teams are experimental and off by default; this project uses subagents.
- `git merge --ff-only` refuses (non-zero exit) when a fast-forward is not possible.

Project docs: docs/README.md, docs/expert-roster.md, docs/04-dataset.md.
