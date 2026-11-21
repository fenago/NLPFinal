# Customer Review Analyzer: team guide

NLP final project. A web app that reads product or restaurant reviews and shows **sentiment, key phrases, and the people, places, brands and products mentioned**. It uses **both NLTK and spaCy** and is **deployed only on Netlify, with no outside servers**.

## Architecture (locked decision)

- **Netlify build (Python 3.12):** NLTK and spaCy run over the committed review sample (`data/`) and write static JSON to `site/data/`.
- **Static site (`site/`):** a plain HTML/CSS/JS dashboard that reads that JSON.
- **In the browser:** Pyodide runs NLTK live for "Analyze your own review". spaCy is *not* available there; its results appear only for dataset reviews and curated examples.
- Netlify Functions can't run Python (JS/TS/Go only), so the project has **no functions, no APIs and no database**.

Details: `docs/05-netlify-architecture.md`. Research index: `docs/README.md`.

## The agent team (`.claude/agents/`)

| Agent | Persona | Model | Job |
|---|---|---|---|
| `orchestrator` | Atlas | opus | Plans, delegates, runs the approval gates, decides go/no-go |
| `meta-agent` | Iris | opus | Builds and improves the agents, skills and knowledge |
| `nltk-expert` | Lex | opus | Tokenizing, stopwords, VADER, FreqDist, collocations; code that also runs in Pyodide |
| `spacy-expert` | Nova | opus | Entities, EntityRuler, noun-chunk aspects, lemmas, dependency aspect↔opinion (build only) |
| `dataset-curator` | Quinn | haiku | Stratified, de-identified review sample; brand patterns; citations |
| `build-pipeline-engineer` | Forge | sonnet | `pipeline/build.py`, `requirements.txt`, JSON data contract |
| `pyodide-engineer` | Juno | sonnet | Web Worker running Pyodide + NLTK; self-hosted Pyodide |
| `frontend-engineer` | Mira | sonnet | Static HTML/CSS/JS, tabs, states, accessibility |
| `dataviz-specialist` | Prism | sonnet | Chart.js charts for sentiment, phrases, aspects, entities |
| `netlify-engineer` | Skye | sonnet | `netlify.toml`, Python version, headers, deploys, rollbacks |
| `qa-engineer` | Rook | sonnet | pytest, JSON-schema checks, Playwright end-to-end tests, budgets |
| `nlp-evaluator` | Kappa | sonnet | VADER vs stars, NER P/R/F1, error analysis |
| `technical-writer` | Quill | sonnet | README, method page, report, citations, demo script |
| `ui-designer-apple-liquid-glass` | Sable | sonnet | Visual design: Liquid Glass materials, typography, color, light/dark, spacing, icons, motion; design options in `site/options/` |
| `ux-designer-apple-hig` | Wren | opus | UX: navigation, flows, clarity, microcopy, empty/loading/error states, accessibility audits (`docs/ux-review.md`) |

Full roles, the skill matrix and handoff order: `docs/expert-roster.md`. Personalities and model choices: `docs/agent-brains.md`.

## How to work with the team

- The orchestrator runs independent experts **in parallel** (several Agent calls in one message) and only chains tasks that depend on each other.
- Run the lead as the main agent: `claude --agent orchestrator`. Or ask in a normal session: "Use the orchestrator subagent to plan the build phase."
- Call a specialist directly by name, e.g. "Use the spacy-expert subagent to fix Best Buy being tagged PERSON."
- **Skills** (`.claude/skills/<name>/SKILL.md`, 57 total) are team conventions. Each agent preloads its skills through the `skills:` frontmatter field.
- **Knowledge** (`knowledge/<agent-name>/`) holds notes from official docs, each with source links. Every agent reads its `INDEX.md` and notes before answering. The two design agents also have `docs/` (key reference summaries) and `examples/` (worked examples they study before working).
- **Memory:** agents keep durable learnings in `.claude/agent-memory/<agent-name>/` (`memory: project`).

## Rules for everyone

1. Respect the Netlify guardrail: Python only at build time, no outside servers, no spaCy in the browser.
2. Only edit files you own (see "Who owns which files" in `docs/expert-roster.md`).
3. The JSON data contract (`docs/data-contract.md`, `schemas/`) is the interface between the build and the site. Changes need orchestrator approval.
4. No merge to `main` without green `pytest`, a valid JSON contract, and a passing Playwright run on the deploy preview.
5. Never commit secrets, raw multi-GB datasets, or user IDs.
6. Design: glass only on the navigation/controls layer; never embed SF Pro, Apple logos or SF Symbols. Every screen passes the `accessibility-audit` skill, including reduce transparency, increase contrast and reduce motion.
7. Changes to agents, skills or knowledge structure go through `meta-agent` and are logged in `docs/agent-changelog.md`.

## Planned repo layout

```text
data/            committed review sample, entity patterns, SOURCES.md
nlp/             nltk_analyzer.py (shared with Pyodide), spacy_analyzer.py
pipeline/        build.py (Netlify build command)
nltk_data/       vendored punkt_tab, stopwords, vader_lexicon
site/            static site; site/data/*.json generated at build
schemas/         JSON Schemas for the data contract
tests/           pytest + Playwright
reports/         evaluation.md, final-report.md
knowledge/       per-agent reference notes from official docs
.claude/agents/  15 subagents   ·   .claude/skills/  57 skills
```
