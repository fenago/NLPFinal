# Prompt Best Practices (Claude Code and Claude prompting guide)

Sources:
- https://code.claude.com/docs/en/best-practices
- https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices (redirects to https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

Fetched: 2026-11-20

## Be specific (Claude Code best practices)
- Only write down what Claude cannot find by reading the repo, or would waste time rediscovering.
- A specific prompt names the file, describes the symptom, and says what "fixed" looks like.

| Instead of | Try |
|---|---|
| "fix the login bug" | "users report login fails after the session times out. look at token refresh in src/auth/, write a failing test that reproduces it, then fix it" |
| "add a calendar widget" | "follow the pattern in HotDogWidget.php and build a calendar widget that lets you pick a month and page between years. no new libraries" |

- State preferences between reasonable approaches up front; hand over files (`@path`), screenshots, or piped output instead of describing them.
- "think step by step" and "be thorough" are ordinary text, not keywords; effort level is the real control. "be ambitious" helps with scope.
- Give Claude a pass/fail check to run (tests, build exit code, linter, fixture diff) and ask for evidence (the command and output). For enforcement use a `Stop` hook; for an independent review use a fresh-context reviewer subagent.
- Use an interview prompt when the spec is unclear: "Interview me until you could write the spec, then write it to SPEC.md", then build in a fresh session.

## Subagent prompts
- Reviewer subagent example from the page: `tools: Read, Grep, Glob`, description "Reviews changed files against the spec they were built from. Use after implementing a feature, before opening the PR."; body: "You're reviewing code you didn't write... report only the gaps that affect correctness. Skip style."
- Subagent costs are mostly tokens; use `model: haiku` for simple jobs, ask for short summaries back, restrict tools.
- Subagents start with a fresh context, so a delegation prompt must carry the task, constraints, and paths.

## General principles (Claude prompting guide)
- **Be clear and direct.** Treat Claude as a brilliant new employee without your context. Key test: show the prompt to a colleague with minimal context; if they would be confused, so will Claude.
- Use numbered steps when order or completeness matters; state output format and constraints.
- If you want more than the task strictly requires, ask explicitly.
- **Add the why.** Instead of "NEVER use ellipses", say "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine will not know how to pronounce them." Claude generalizes from the reason.
- **Examples are among the most reliable ways to steer format, tone and structure.** Make them relevant, diverse (cover edge cases), and structured (wrap in `<example>`, several in `<examples>`).
- **XML tags** (`<instructions>`, `<context>`, `<input>`) separate instruction, context, examples and inputs; use consistent descriptive names and nest when hierarchical.
- **Give a role** in the system prompt; even one sentence helps.
- Long documents: place them in tagged blocks (see the page's multidocument structure and quote-extraction examples).

## Tool use and action
- Latest models follow instructions precisely: "Can you suggest some changes?" yields suggestions; "Change this function to improve its performance." yields edits. Say explicitly when you want action.
- Avoid over-prompting tool use ("If in doubt, use [tool]" can overtrigger); prefer "use [tool] when it would enhance your understanding".

## Agentic patterns
- **Subagent orchestration**: models delegate natively; if they overuse subagents, add guidance: "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits... work directly rather than delegating."
- **Overeagerness**: to keep solutions minimal, say "Avoid over-engineering. Only make changes that are directly requested or clearly necessary" and list scope, documentation, defensive coding, and abstraction limits.
- **Hallucinations**: wrap an `<investigate_before_answering>` instruction: never speculate about code you have not opened; read referenced files first.
- **Chaining**: draft, review against criteria, refine, when you need to inspect intermediate outputs.
- **Verbosity**: models are more concise and may skip summaries after tool calls; ask "After completing a task that involves tool use, provide a quick summary of the work you've done" if you want that.
- **Commit to a choice** to curb overthinking: "choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning."
- The guide lists current models including Claude Sonnet 5.5; where a technique names a model, re-check it with your own evals before applying to another (the page says so).

## Project application
- Agent prompt skeleton: one-sentence role; scope (files owned); inputs to read first (data contract, `knowledge/<role>/INDEX.md`); numbered procedure; output format and done-check (a command that returns pass/fail); explicit "do not" list (e.g. no server-side Python on Netlify).
- Add the reason behind each hard rule (e.g. "Python runs only at build time because Netlify Functions are JS/TS/Go only").
- Include 1-2 `<example>` blocks of a good handoff note, not long prose.
- Keep each agent file short; move reference material to skills/knowledge files loaded on demand.
- Move any rule that cannot have exceptions (never commit to `main`, never delete `nltk_data/`) into a hook, not a prompt.

## Checklist before shipping an agent prompt
- Can a colleague with no context follow it (the "key test")?
- Does it name concrete files, commands and a pass/fail check?
- Does every "never" carry a reason?
- Is verbosity set (for example "report in under 200 words with file paths")?
- Is anything in it something the agent could read from the repo? If yes, cut it.
