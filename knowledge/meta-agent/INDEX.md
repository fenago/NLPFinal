# Meta-Agent Knowledge Index

Fetched: 2026-11-20. Real notes from official Claude Code and Anthropic docs.

| File | Use it when | Sources |
|---|---|---|
| 01-subagent-file-format.md | Writing or reviewing `.claude/agents/*.md`: frontmatter fields, skipped files, model choice, memory scopes | code.claude.com/docs/en/sub-agents |
| 02-skills-format.md | Writing `SKILL.md`: fields, locations, 500-line and 1,536-char limits, preloading into subagents | code.claude.com/docs/en/skills |
| 03-memory-claude-md.md | Deciding what goes in CLAUDE.md vs skills vs rules; `@` imports; subagent `memory` | code.claude.com/docs/en/memory |
| 04-prompt-best-practices.md | Writing prompts: specificity, examples, XML tags, delegation, anti-overengineering | code.claude.com/docs/en/best-practices; platform.claude.com prompting guide |

Quick facts
- Only `name` and `description` are required in a subagent; unknown frontmatter fields are silently ignored.
- Subagents skip files with no `name` (treated as docs), or `name` without `description`.
- `skills:` in a subagent injects full content at startup; skills with `disable-model-invocation: true` cannot be preloaded.
- Skill description cap 1,536 chars; `SKILL.md` under 500 lines; CLAUDE.md under 200 lines.
- Subagents get CLAUDE.md but not the parent's auto memory.

Project docs: docs/expert-roster.md (roles, skills S01-S45).
