# Skills Format (SKILL.md)

Sources:
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents (Preload skills into subagents)

Fetched: 2026-11-20

## Basics
- A skill is a directory with a required `SKILL.md`: YAML frontmatter between `---` markers plus Markdown instructions.
- Skills follow the Agent Skills open standard (https://agentskills.io/); Claude Code adds invocation control, subagent execution and dynamic context injection.
- Use a skill when you keep pasting the same procedure, or when a CLAUDE.md section has grown into a procedure. A skill body loads only when used; only name and description sit in context otherwise.
- Custom commands were merged into skills; `.claude/commands/` files still work (same frontmatter except `name` and `paths`).
- The frontmatter is read only if the opening `---` is the file's first line. Malformed YAML: skill still loads with no fields (so it will not match by description).

## Where skills live
| Location | Path | Loads in |
|---|---|---|
| Enterprise | managed settings dir `.claude/skills/<name>/SKILL.md` | all org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<name>/SKILL.md` | this repo (commit it) |
| Nested | `<subdir>/.claude/skills/<name>/SKILL.md` | sessions in/below that subdir |
| Additional dir | `.claude/skills/` under an `--add-dir` directory | that session |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | where enabled, as `/plugin:skill` |
- Reserved: do not name a folder `synced` or `anthropic-skills` (they will not load outside plugins).
- Folder name becomes the command (`/deploy`) unless `name` is set.

## Frontmatter (all optional; `description` recommended)
Names are lowercase with hyphens, except `when_to_use`. Unknown fields are ignored silently.
| Field | Notes |
|---|---|
| `name` | Defaults to directory name. |
| `description` | What it does and when to use it; put the key use case first. |
| `when_to_use` | Extra trigger phrases; appended to `description`. |
| `argument-hint`, `arguments` | Autocomplete hint; named positional args for `$name` substitution. |
| `disable-model-invocation` | `true` = Claude cannot start it itself (use for side effects like `/deploy`, `/commit`). Also blocks preloading into subagents. |
| `user-invocable` | `false` = hidden from `/` menu; only Claude invokes it (background knowledge). |
| `allowed-tools` / `disallowed-tools` | Pre-approve or remove tools during the turn that invokes the skill; cleared at the next message. |
| `model`, `effort` | Override for the rest of the turn. |
| `context` | `fork` runs the skill in a subagent (needs explicit task instructions). |
| `agent` | Subagent type used with `context: fork`. |
| `background` | With `context: fork`, `false` waits for the result. |
| `hooks`, `paths`, `shell` | Skill-scoped hooks; glob patterns that activate the skill; `bash` or `powershell`. |
| `metadata`, `license`, `compatibility` | Passive (compatibility max 500 chars). |

## Size limits
- **`description` + `when_to_use` are truncated at 1,536 characters** in the skill listing.
- **Keep `SKILL.md` under 500 lines**; move detail into supporting files.
- The listing of descriptions has a character budget (1% of the context window); with many skills, descriptions of least-used skills are dropped first. `/doctor` estimates the cost.
- `<` and `>` in descriptions display as `&lt;`/`&gt;`; use `[branch]` or `argument-hint`.

## Supporting files
```
my-skill/
├── SKILL.md        (required: overview and navigation)
├── reference.md    (loaded when needed)
├── examples.md     (loaded when needed)
└── scripts/helper.py (executed, not loaded)
```
Reference each file from `SKILL.md` with a link and when to read it (`## Additional resources`).

## Invocation control matrix
| Frontmatter | You | Claude | Context |
|---|---|---|---|
| default | yes | yes | description always; full body on invoke |
| `disable-model-invocation: true` | yes | not on its own | description not in context |
| `user-invocable: false` | no | yes | description in context |

## Lifecycle gotchas
- Invoked content enters the conversation as one message and stays; the file is **not re-read** on later turns. Write standing instructions ("run tests after every edit").
- After compaction only the start of an invoked skill may be kept: put key instructions at the top.
- Rules that must always hold belong in hooks, not skills.

## Preloading skills into subagents
- Subagent frontmatter `skills: [name1, name2]` injects each skill's **full content** at startup (up to 32 names). The subagent can still discover other skills via the Skill tool unless `Skill` is omitted from `tools`/in `disallowedTools`.
- Cannot preload a skill with `disable-model-invocation: true`.
- Inverse of `context: fork`: with `skills`, the subagent body is the system prompt; with `context: fork`, the skill content is the task and the agent type supplies the system prompt.
- Agent teams do not apply a definition's `skills` to a teammate.

## Project application
- Each of the 13 agents gets a knowledge skill (e.g. `.claude/skills/<role>-knowledge/SKILL.md`) whose body is a short index pointing at `knowledge/<role>/*.md`; preload it with `skills:` in the agent file.
- Keep descriptions under about 300 chars with concrete trigger words; the cap is 1,536.
- Mark side-effect skills (deploy, release) `disable-model-invocation: true`; mark pure reference skills `user-invocable: false`.
- Shared skills in the roster (S05 Netlify guardrail, S06 git workflow) should exist once and be preloaded by every agent that needs them.
