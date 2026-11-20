# Memory and CLAUDE.md

Sources:
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/best-practices (Keep CLAUDE.md short)
- https://code.claude.com/docs/en/sub-agents (Enable persistent memory)

Fetched: 2026-11-20

## Two memory systems
- **CLAUDE.md**: written by you; instructions and rules; project, user or org scope; loaded every session.
- **Auto memory**: written by Claude; learnings; per repository; first 200 lines or 25KB of `MEMORY.md` loaded each session. Types: `user`, `feedback`, `project`, `reference`.
- Both are context, not enforced configuration. To block an action regardless, use a `PreToolUse` hook.

## CLAUDE.md locations (load order, broad to specific)
| Scope | Location |
|---|---|
| Managed policy | Linux/WSL `/etc/claude-code/CLAUDE.md`; macOS `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` (team-shared via git) |
| Local | `./CLAUDE.local.md` (add to `.gitignore`) |
- Files in the cwd and every directory above it load at launch; subdirectory files load on demand. All are **concatenated**, root to cwd, so the closest is read last; `CLAUDE.local.md` is appended after `CLAUDE.md`.
- `--add-dir` directories do not load CLAUDE.md unless `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`.
- `AGENTS.md` is supported (see the AGENTS.md section of the page).
- Check what loaded: `/context all` (Memory files list). Generate a starter: `/init`.

## Imports
- Syntax `@path/to/file` anywhere in CLAUDE.md. Relative paths resolve from the **file containing the import**; absolute paths allowed; recursion max **four hops**.
- Escape spaces with a backslash; quoted paths are not imported.
- Code spans and fenced blocks are not parsed: wrap `` `@README` `` to mention without importing.
- External imports (outside the working directory) trigger a one-time approval dialog in project files.
- Imports organize but **do not reduce context cost**: imported files load with the importer.

## Writing effective CLAUDE.md
- Target **under 200 lines** per file; longer files cost context and reduce adherence.
- Be verifiable: "Use 2-space indentation", "Run `npm test` before committing", "API handlers live in `src/api/handlers/`".
- Group with headers and bullets; remove contradictions (Claude may pick one arbitrarily). `/doctor prompt-audit` finds stale or conflicting instructions.
- Include only what Claude cannot learn from the code: exact test/lint commands, misleading spots, decisions not in the repo, anything corrected twice.
- Test before adding a line: could Claude find it by reading the code, and would it go look? If yes to both, leave it out.
- If Claude ignores a line, adding IMPORTANT probably will not help; shorten the file or move the rule to a hook.
- Multi-step procedures go to skills; area-specific rules go to `.claude/rules/*.md` (optionally with `paths:` frontmatter globs).
- Size limits: file over 4 MiB is skipped; on-demand files (subdirectory CLAUDE.md, path rules) are cut at 40,000 chars on a 200K window.

## Subagents and memory
- Subagents load the CLAUDE.md hierarchy (unless `omitClaudeMd: true`), but **not** the main conversation's auto memory. Give a subagent its own memory with the `memory` field: `user` (`~/.claude/agent-memory/<name>/`), `project` (`.claude/agent-memory/<name>/`, recommended), `local` (`.claude/agent-memory-local/<name>/`).
- Subagent memory depends on auto memory being enabled (`autoMemoryEnabled`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`).
- Tell the subagent in its body to consult and update its memory, e.g. "Update your agent memory as you learn the team's preferences..."

## Project application
- Root `CLAUDE.md` for NLPFinal should stay well under 200 lines: stack facts, build/test commands, the Netlify guardrail (S05), the git rule (S06), and pointers via `@docs/expert-roster.md` only if worth the context cost.
- Put role-specific knowledge in `knowledge/<role>/` and per-role skills, not in CLAUDE.md. Use `memory: project` for agents whose learnings should be versioned (EVAL, QA).
- Because subagents get CLAUDE.md automatically, keep it role-neutral; role details belong in each agent file.

## Quick reference
- Show/verify: `/context all`, `/memory` (view and edit), `/status` (warns when an instruction file is over the recommended length).
- Rules dir: `.claude/rules/*.md`, one topic per file, discovered recursively; files without `paths` frontmatter load at launch with the same priority as `.claude/CLAUDE.md`.
- Personal per-project prefs: `CLAUDE.local.md` (gitignored); across worktrees, import a file from home instead: `- @~/.claude/my-project-instructions.md`.
- Instructions seem lost after `/compact`: CLAUDE.md is re-read, but conversational instructions are not; put durable rules in CLAUDE.md (page section "Instructions seem lost after /compact").
- Size guard: run `wc -m path/to/CLAUDE.md` to count characters when checking the on-demand file limit.
