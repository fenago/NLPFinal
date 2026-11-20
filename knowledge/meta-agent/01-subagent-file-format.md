# Subagent File Format (Claude Code)

Sources:
- https://code.claude.com/docs/en/sub-agents (sections: Write subagent files, Frontmatter reference, Subagent files Claude Code skips, Choose a model, Permission modes, Preload skills, Enable persistent memory)

Fetched: 2026-11-20

## File shape
- Markdown file with YAML frontmatter between `---` markers; the **body is the system prompt**.
- Location by priority (higher wins on same `name`): managed settings (1) > `--agents` CLI JSON (2) > `.claude/agents/` project (3) > `~/.claude/agents/` user (4) > plugin `agents/` (5).
- Project subagents are discovered by walking up from the cwd; nested duplicates resolve to the closest definition. Commit `.claude/agents/` to share with the team.
- Claude Code watches `~/.claude/agents/` and `.claude/agents/` and picks up edits within seconds (no restart), except directories added by `--add-dir`.
- Subagents get their prompt plus environment details, **not** the Claude Code system prompt.

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

## Frontmatter fields (only `name` and `description` required)
Field names are camelCase and must match exactly; an unrecognized field is **ignored without error**.

| Field | Meaning |
|---|---|
| `name` | Unique id, at most 256 chars (e.g. `code-reviewer`). No `:` (reserved for plugin scopes). Filename need not match. |
| `description` | When Claude should delegate to this subagent. |
| `tools` | Allowlist, comma string or YAML list (`Read, Grep, Bash`). Inherits all tools if omitted. Use `Agent(worker, researcher)` only for `--agent` main-thread agents. Do not list `Skill` to preload skills; use `skills`. |
| `disallowedTools` | Denylist, applied first, then `tools` resolves against what is left. `Bash(git push *)` still removes the whole Bash tool. |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full ID (e.g. `claude-opus-5-5`), or `inherit`. |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` (`manual` = alias for `default`). Parent's mode can override it. Ignored for plugin subagents. |
| `maxTurns` | Max agentic turns; at the limit output is marked partial and can be resumed. |
| `autoCompactWindow` | Token count of 100000 or more (needs v2.1.296+). |
| `skills` | Skills whose **full content** is injected at startup (first 32 names). Unlisted skills stay discoverable via the Skill tool. |
| `mcpServers` | Server names or inline definitions. Ignored for plugin subagents. |
| `hooks` | Lifecycle hooks scoped to the subagent. Ignored for plugin subagents. |
| `memory` | `user`, `project`, or `local` persistent memory scope. |
| `background` | `true` keeps it in the background even when Claude asks to wait. |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` (available levels depend on model); overrides session effort. |
| `isolation` | `worktree` runs it in a temporary git worktree; cleaned up if no changes. |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`. Task-list display only. |
| `omitClaudeMd` | `true` skips user/project/local CLAUDE.md in its initial context (managed policy still loads). v2.1.271+. |
| `initialPrompt` | Auto-submitted first turn when the agent runs as the main session agent. |
| `experimental` | Map; `cacheTtl: 5m` or `1h` (inside the map, not top level). |

## Files Claude Code skips (in an `agents` directory)
- No `name`: treated as documentation kept beside the agents.
- Opening `---` not on the file's first line: read as having no frontmatter, so documentation.
- `name` starting with `-`, containing `:`, or over 256 chars: skipped, error in debug log.
- `name` but no `description`: skipped, reason in debug log.
- YAML that does not parse: no fields read, file skipped.
- Debug: `claude --debug`; search `~/.claude/debug/<session-id>.txt` for `does not recognize or apply` (v2.1.296+). Validate a directory with `claude plugin validate .claude/agents` (does not flag a file that parses but lacks `name`).

## Choose a model
Order of precedence: (1) per-invocation `model` parameter Claude passes (alias only), (2) the definition's `model` field, (3) env `CLAUDE_CODE_SUBAGENT_MODEL`, (4) the main conversation's model. With no `model`, a subagent runs on the same model as the conversation. Nested subagents default to their parent's model. The best-practices page suggests `model: haiku` for simple jobs (collecting importers of a module, link checks).

## Tools and permissions notes
- Subagents never get: `AskUserQuestion`, `EnterPlanMode`, `ExitPlanMode` (unless `permissionMode: plan`), `Workflow`, `ScheduleWakeup`, `EndConversation`, and `Agent` at the depth limit.
- Omit `Agent` from `tools` to stop a subagent spawning others.
- `permissionMode` is overridden when the parent runs `bypassPermissions`, `acceptEdits` or `auto`; under parent `plan` the subagent stays in plan mode.
- Skills with `disable-model-invocation: true` cannot be preloaded.

## Memory scopes (`memory` field)
- `user`: `~/.claude/agent-memory/<name>/`; `project` (recommended default): `.claude/agent-memory/<name>/`; `local`: `.claude/agent-memory-local/<name>/` (not for version control).
- Enabling memory adds read/write instructions, the first 200 lines or 25KB of `MEMORY.md`, and auto-enables Read/Write/Edit.

## Project application
- One file per role in `.claude/agents/<id>.md` with `name`, a one-sentence trigger-style `description`, minimal `tools` (reviewers/analysts read-only: `Read, Grep, Glob`; builders add `Edit, Write, Bash`), and a `model` choice (haiku for simple lookup roles, sonnet default, opus for ORC/META if needed).
- Do not use `color` or `experimental` expecting effect in `--agents` JSON; they are ignored there.
- Preload each role's knowledge skill via `skills:` rather than listing `Skill` in `tools`.
- Validate after writing: `claude plugin validate .claude/agents` and a `--debug` run to catch typo'd field names.
