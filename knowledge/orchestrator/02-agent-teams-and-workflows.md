# Agent Teams and Common Workflows (Claude Code)

Sources:
- https://code.claude.com/docs/en/agent-teams (page exists, fetched)
- https://code.claude.com/docs/en/common-workflows (page exists, fetched)

Fetched: 2026-11-20

## Agent teams: status
- **Experimental and disabled by default.** Enable with env `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (shell or `settings.json` under `"env"`).
- Side effect: when enabled, a subagent that Claude *names* when spawning launches as a teammate, so teams can form even if you did not ask.

## Subagents vs agent teams
| | Subagents | Agent teams |
|---|---|---|
| Context | Own window; result returns to caller | Own window; fully independent |
| Communication | Report to caller (named subagents can also message each other) | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list plus messages |
| Best for | Focused tasks where only the result matters | Complex work needing discussion |
| Token cost | Lower | Higher (each teammate is a separate Claude instance) |
- Agent teams are best for: research and review, new modules (each teammate owns a piece), debugging with competing hypotheses, cross-layer coordination.
- For sequential tasks, same-file edits, or many dependencies, use one session or subagents instead.

## Architecture
- Components: **team lead** (main session), **teammates** (separate Claude Code instances), **task list** (`~/.claude/tasks/{team-name}/`), **mailbox** (JSON per agent at `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`).
- Team config `~/.claude/teams/{team-name}/config.json` is runtime state; do not edit by hand. Reusable roles come from subagent definitions.
- Teammates load CLAUDE.md, MCP servers and skills but **not** the lead's conversation history: put task details in the spawn prompt.
- Reusing a subagent definition: `Spawn a teammate using the security-reviewer agent type to audit the auth module.` Applied from the definition: `tools`, `model`, and (in-process) `disallowedTools`, `effort`, body appended to the system prompt. **`skills` is not applied**; `mcpServers` only for split-pane teammates.
- Permissions: a teammate starts in the lead's permission mode; no per-teammate modes at spawn. Teammate permission prompts appear in the lead session. A message from another agent is treated as untrusted input, not user approval.

## Best practices (from the page)
- Start with **3-5 teammates**; "three focused teammates often outperform five scattered ones".
- Size tasks: too small = overhead; too large = risk of wasted effort; right = self-contained deliverable (function, test file, review). About 5-6 tasks per teammate.
- Avoid file conflicts: each teammate owns a different set of files.
- If the lead starts implementing itself: `Wait for your teammates to complete their tasks before proceeding`.
- Begin with research/review tasks (no code writing) before parallel implementation.
- Monitor and steer; do not leave a team unattended too long.

## Limitations (as documented)
- No session resumption for in-process teammates (`/resume`, `/rewind` do not restore them).
- Task status can lag; shutdown can be slow.
- One team per session; no nested teams; lead is fixed.
- In-process teammates cannot run background subagents.
- Split panes need tmux or iTerm2; default in-process mode works anywhere.

## Common workflows relevant to orchestration
- **Delegate research**: `use a subagent to investigate how our auth system handles token refresh`; only the summary returns.
- **Parallel sessions with worktrees**: `claude --worktree feature-auth` gives an isolated checkout on its own branch (repo needs at least one commit). Subagent frontmatter `isolation: worktree` does the same per subagent.
- **Plan before editing**: `claude --permission-mode plan` or `Shift+Tab` until "plan mode on"; Claude proposes, makes no edits until approved.
- **Create PRs**: ask `create a pr`; Claude links the session to the PR when it uses `gh pr create`. Resume later with `claude --from-pr 1234`. The page says: review Claude's generated PR before submitting and ask Claude to highlight risks.
- **Resume**: `claude --continue` (most recent in cwd), `claude --resume` (picker).
- **Non-interactive**: `git log --oneline -20 | claude -p "summarize these recent commits"`.

## Project application
- This project's decision is a flat team of 13 role subagents driven by ORC, not experimental agent teams. Use subagents for fan-out; if teams are ever tried, start with a review-only pass (QA/EVAL).
- Handoffs go through files (data contract, `site/data/*.json`), not chat: subagents do not share history.
- Keep parallel batches to disjoint file owners (roster ownership table).
- Gate each phase with a review step before PR merge (see 03-git-workflow.md).

## Decision guide for ORC (derived from the pages above)
| Situation | Use |
|---|---|
| Independent lookups (e.g. read dataset docs, read Pyodide docs) | Parallel subagents, short summaries back |
| Sequential handoff (DATA then NLTK/SPACY then BUILD) | Chain subagents; pass file paths, not prose |
| Many files, long-running, needs discussion between workers | Agent teams (experimental), only if enabled; start with review work |
| Task needs your conversation history | Main conversation or a fork (`/subtask`), not a fresh subagent |
| Risky or large edits | Plan mode first, or `isolation: worktree` |
