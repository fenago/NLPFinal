# Subagents and Delegation (Claude Code)

Sources:
- https://code.claude.com/docs/en/sub-agents

Fetched: 2026-11-20

## What a subagent is
- A Markdown file with YAML frontmatter; the body is the subagent's system prompt. Only `name` and `description` are required.
- Each subagent starts with a **fresh, isolated context window**. It does not see your conversation history, skills you already invoked, or files already read. Claude writes a delegation message that summarizes the task; the subagent works from that.
- A subagent receives its own system prompt plus environment details (working directory), **not** the Claude Code system prompt.

## Automatic delegation
- Claude delegates based on the task in the request, each subagent's `description`, and current context.
- To encourage proactive delegation, put phrases like "use proactively" in the `description`.
- Keep descriptions brief: Claude Code shows a startup warning when combined subagent descriptions pass the **15,000-token limit** (it still loads every subagent).

## Invoking explicitly (three patterns, escalating)
1. **Natural language**: name the subagent in the prompt; Claude decides whether to delegate.
   - `Use the test-runner subagent to fix failing tests`
2. **@-mention**: type `@` and pick from the typeahead, e.g. `@"code-reviewer (agent)" look at the auth changes`. Manual form: `@agent-<name>`. The full message still goes to Claude, which writes the subagent's task prompt.
3. **Session-wide**: the whole session runs as that subagent: `claude --agent code-reviewer`, or `{"agent": "code-reviewer"}` in `.claude/settings.json` (CLI flag wins). A custom agent's prompt replaces the default Claude Code system prompt; CLAUDE.md files still load.

## Foreground vs background
- **Foreground** subagents block the main conversation; permission prompts pass through to you.
- **Background** subagents run concurrently; their permission prompts surface in the main session naming the subagent.
- With nothing configured, a subagent that Claude spawns from the main conversation **starts in the background**.
- Background subagents get a smaller built-in tool set than foreground ones (they keep all MCP tools, Read, Grep, Glob, Bash, Edit, Write, WebFetch, WebSearch, Skill, SendMessage, Artifact, and others; do not rely on other built-in tools).
- To make Claude wait for a result in an interactive session: set `CLAUDE_CODE_FORK_SUBAGENT` to `0` (turns fork mode off), then say "run the reviewer subagent and wait for its report". `Ctrl+B` moves a waiting run to the background.
- Frontmatter `background: true` keeps a subagent in the background even when Claude asks to wait.

## Common patterns
- **Isolate high-volume operations** (tests, docs fetches, logs): verbose output stays in the subagent; only the summary returns.
- **Parallel research**: `Research the authentication, database, and API modules in parallel using separate subagents`. Works best when paths do not depend on each other. Many detailed results consume main-context tokens; each subagent also spends its own tokens.
- **Chaining**: `Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them`. Each returns to Claude, which passes context to the next.
- Use the **main conversation** for back-and-forth, shared-context phases, quick edits, latency-sensitive work. Use **subagents** for verbose output, tool restrictions, self-contained work that returns a summary.

## What loads at startup (non-fork subagent)
- System prompt (agent body + environment details)
- The task message (delegation prompt)
- CLAUDE.md files (full hierarchy: user, project, local, managed, AGENTS.md); skipped by built-in Explore/Plan, and by `omitClaudeMd: true` (managed policy files still load)
- Git status snapshot
- Preloaded skills from the `skills` field (full content)
- Sibling roster (only if the subagent has `SendMessage` and another named agent exists)
- NOT loaded: your output style, the main conversation's auto memory (use the `memory` field), the parent's conversation.
- If a rule must reach the subagent (e.g. "ignore `vendor/`"), restate it in the delegation prompt.

## Resume and SendMessage
- Each invocation creates a **new instance**. To continue earlier work, ask Claude to resume; resumed subagents keep full history.
- On completion Claude receives an agent ID. For work you will continue, use `general-purpose` or a custom subagent (Explore and Plan may finish without a resumable ID).
- Claude uses `SendMessage` with the agent ID or name as `to`. A completed subagent that gets a message resumes in the background. `SendMessage` does not require agent teams.
- Subagent transcripts persist within the session and are cleaned up after `cleanupPeriodDays` (default 30 days).
- After a restart, if a name no longer resolves, give Claude the agent ID (find it in `agent-{agentId}.meta.json` under `~/.claude/projects/{project}/{sessionId}/subagents/`).
- `maxTurns` limit reached: output is marked partial and the subagent can be resumed.

## Nesting depth and concurrency
- Default: a subagent can spawn subagents up to **three layers** below the main conversation. At the limit the `Agent` tool is withheld. Change with env `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (`1` turns nesting off).
- To prevent one subagent spawning, omit `Agent` from its `tools`.
- Concurrent limit: by default when **20** subagents are running, spawning another fails with `Concurrent subagent limit reached`. Change with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`. No limit on the total spawned over a session.
- Nested subagents default to the spawning subagent's model.

## Restricting spawnable types
- For an agent run as the main thread (`claude --agent`), `tools: Agent(worker, researcher), Read, Bash` allowlists spawnable types. In a normal subagent definition the type list in parentheses is ignored.
- `Task` was renamed `Agent` in v2.1.63; `Task(...)` still works as an alias.

## Forks
- A fork inherits the whole conversation (same system prompt, tools, model); only its final result returns. Start one with `/subtask <task>`. Cheaper than a fresh subagent for context-heavy work because it shares the prompt cache.

## Project application
- The 13 agents live in `.claude/agents/` (project scope, checked into git). Each needs a precise `description`; keep all 13 short to stay under the 15k-token budget.
- ORC cannot assume subagents know the roster or docs: every delegation prompt must state the task, files owned, the data contract path, and the Netlify guardrail (S05). Subagents do load CLAUDE.md.
- Phase order from `docs/expert-roster.md` (DATA -> NLTK + SPACY -> BUILD -> PYO + UI + VIZ, NET in parallel) maps to chaining plus parallel fan-out; keep fan-out well under 20 concurrent.
- Assign disjoint file ownership per parallel subagent (see roster file-ownership table) to avoid overwrites.
