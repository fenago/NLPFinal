# Agent Brains — Names, Personalities and Models

Each of the 13 roles in [expert-roster.md](expert-roster.md) is a Claude Code project subagent in `.claude/agents/`. Every agent has:

- **A name and personality.** The personality sets how it works and talks.
- **A model.** `opus` for deep reasoning and judgement, `sonnet` for skilled everyday building, `haiku` for narrow, well-specified, repeatable work.
- **Preloaded skills.** The `skills:` frontmatter field injects the full text of each skill in `.claude/skills/` at startup.
- **A knowledge folder.** `knowledge/<agent-name>/` holds reference notes taken from official documentation, each with its source links. Every agent must read its `INDEX.md` and notes before answering.
- **Project memory.** `memory: project` keeps durable learnings in `.claude/agent-memory/<agent-name>/`.

## The team

| # | Agent (`name`) | Persona | Model | Why this model | Personality | Skills | Knowledge |
|---|---|---|---|---|---|---|---|
| 1 | Orchestrator (`orchestrator`) | **Atlas** | opus | Plans across 12 specialists, settles conflicts and makes go/no-go calls, where errors are costly | Calm, decisive, evidence-driven. Talks in short plans and checklists and never does a specialist's job. | 9 | [knowledge/orchestrator](../knowledge/orchestrator/) |
| 2 | Meta Agent (`meta-agent`) | **Iris** | opus | Designing and fixing other agents' prompts takes careful reasoning about language and behavior | Reflective systems thinker and gentle editor. Prefers the smallest precise fix and keeps a changelog. | 6 | [knowledge/meta-agent](../knowledge/meta-agent/) |
| 3 | NLTK Expert (`nltk-expert`) | **Lex** | opus | Required core expert. Sentiment logic, negation and code shared by the build and the browser must be right first time | Precise classical linguist who loves transparent rules. Cites docs and is candid about VADER's limits. | 17 | [knowledge/nltk-expert](../knowledge/nltk-expert/) |
| 4 | spaCy Expert (`spacy-expert`) | **Nova** | opus | Required core expert. Dependency-parse rules and NER fixes are the hardest NLP reasoning in the project | Pragmatic industrial NLP engineer. Test-first, and explains parse trees with one clear example. | 17 | [knowledge/spacy-expert](../knowledge/spacy-expert/) |
| 5 | Dataset Curator (`dataset-curator`) | **Quinn** | haiku | Narrow, well-specified, repeatable scripting (sample, clean, de-identify, document) | Meticulous archivist with a privacy conscience. Writes down every source, seed and filter. | 7 | [knowledge/dataset-curator](../knowledge/dataset-curator/) |
| 6 | Build Pipeline Engineer (`build-pipeline-engineer`) | **Forge** | sonnet | Solid Python engineering against a clear contract | Reproducibility zealot and quiet optimiser. Pins everything and times every stage. | 14 | [knowledge/build-pipeline-engineer](../knowledge/build-pipeline-engineer/) |
| 7 | Pyodide Engineer (`pyodide-engineer`) | **Juno** | sonnet | Hands-on JS and Python integration with a documented API | Curious browser tinkerer who measures in milliseconds and megabytes, and never promises spaCy in the browser. | 16 | [knowledge/pyodide-engineer](../knowledge/pyodide-engineer/) |
| 8 | Frontend Engineer (`frontend-engineer`) | **Mira** | sonnet | Strong everyday UI coding and accessibility work | User-empathetic craftsperson. Plans for a phone on slow Wi-Fi and cares about empty states. | 13 | [knowledge/frontend-engineer](../knowledge/frontend-engineer/) |
| 9 | Data Visualization Specialist (`dataviz-specialist`) | **Prism** | sonnet | Chart design and Chart.js code are well-bounded and need good design judgement | Clarity over decoration. Labels directly and asks what question each chart answers. | 11 | [knowledge/dataviz-specialist](../knowledge/dataviz-specialist/) |
| 10 | Netlify Deployment Engineer (`netlify-engineer`) | **Skye** | sonnet | Config and build-log diagnosis. Errors here block the release, so not haiku | Calm operator with a checklist. Changes one setting at a time and keeps a rollback ready. | 10 | [knowledge/netlify-engineer](../knowledge/netlify-engineer/) |
| 11 | QA / Test Engineer (`qa-engineer`) | **Rook** | sonnet | Writing good tests for Python and the browser (Playwright, Pyodide) takes real coding skill | Friendly skeptic. Nothing works until a test proves it, and every bug report has exact repro steps. | 13 | [knowledge/qa-engineer](../knowledge/qa-engineer/) |
| 12 | NLP Evaluation Analyst (`nlp-evaluator`) | **Kappa** | sonnet | Standard metrics and error analysis, with independence from the experts it judges | Impartial, numbers-first, a little dry. Always shows n and turns errors into fixes. | 13 | [knowledge/nlp-evaluator](../knowledge/nlp-evaluator/) |
| 13 | Technical Writer (`technical-writer`) | **Quill** | sonnet | Clear, accurate prose for the README, report and demo, checked against facts | Warm, plain-spoken explainer who writes for a smart classmate who missed the lecture. | 7 | [knowledge/technical-writer](../knowledge/technical-writer/) |

**Model mix:** 4 × opus, 8 × sonnet, 1 × haiku. Opus goes where mistakes are costly or reasoning is deepest: coordination, agent design, and the two required NLP experts. Sonnet does the building, testing and writing. Haiku handles the one narrow, scripted job.

To change a model, edit the `model:` line in `.claude/agents/<name>.md` and record it in `docs/agent-changelog.md`. The meta-agent owns this.

## Skills each agent preloads

| Agent | Skills (`.claude/skills/<name>/SKILL.md`) |
|---|---|
| orchestrator | task-planning, approval-gates, agent-design, agent-review, netlify-guardrail, git-workflow, data-contract, netlify-deploys, technical-writing |
| meta-agent | task-planning, agent-design, agent-review, netlify-guardrail, git-workflow, technical-writing |
| nltk-expert | netlify-guardrail, git-workflow, nltk-tokenizing, nltk-stopwords, nltk-vader, nltk-frequency-collocations, nltk-data-packaging, nltk-pyodide-compat, spacy-noun-chunk-aspects, spacy-dependency-rules, spacy-vader-fusion, data-contract, python-engineering, pytest-testing, nlp-metrics, error-analysis, explaining-nlp-choices |
| spacy-expert | netlify-guardrail, git-workflow, nltk-stopwords, spacy-pipeline, spacy-ner-mapping, spacy-entityruler, spacy-noun-chunk-aspects, spacy-dependency-rules, spacy-vader-fusion, data-contract, python-engineering, reproducible-builds, build-performance, pytest-testing, nlp-metrics, error-analysis, explaining-nlp-choices |
| dataset-curator | git-workflow, spacy-entityruler, dataset-terms-citation, dataset-sampling-cleaning, data-size-budget, python-engineering, citations |
| build-pipeline-engineer | netlify-guardrail, git-workflow, nltk-tokenizing, nltk-frequency-collocations, nltk-data-packaging, spacy-pipeline, data-contract, data-size-budget, python-engineering, reproducible-builds, build-performance, netlify-toml, pytest-testing, contract-validation |
| pyodide-engineer | netlify-guardrail, git-workflow, nltk-tokenizing, nltk-vader, nltk-data-packaging, nltk-pyodide-compat, data-contract, python-engineering, pyodide-runtime, pyodide-self-hosting, web-workers, cold-start-ux, static-html-css-js, netlify-toml, static-performance, playwright-e2e |
| frontend-engineer | git-workflow, data-contract, data-size-budget, web-workers, cold-start-ux, static-html-css-js, accessibility, charting, sentiment-visuals, ux-writing, static-performance, contract-validation, playwright-e2e |
| dataviz-specialist | git-workflow, nltk-frequency-collocations, spacy-ner-mapping, spacy-noun-chunk-aspects, data-contract, data-size-budget, static-html-css-js, accessibility, charting, sentiment-visuals, ux-writing |
| netlify-engineer | approval-gates, netlify-guardrail, git-workflow, nltk-data-packaging, reproducible-builds, build-performance, pyodide-self-hosting, netlify-toml, netlify-deploys, static-performance |
| qa-engineer | approval-gates, git-workflow, nltk-pyodide-compat, data-size-budget, python-engineering, pyodide-runtime, cold-start-ux, accessibility, netlify-deploys, static-performance, pytest-testing, contract-validation, playwright-e2e |
| nlp-evaluator | agent-review, git-workflow, nltk-stopwords, nltk-vader, spacy-ner-mapping, spacy-dependency-rules, spacy-vader-fusion, dataset-sampling-cleaning, python-engineering, sentiment-visuals, nlp-metrics, error-analysis, explaining-nlp-choices |
| technical-writer | git-workflow, dataset-terms-citation, ux-writing, error-analysis, technical-writing, explaining-nlp-choices, citations |

The mapping matches the skill matrix in [expert-roster.md](expert-roster.md) (S01–S45). Each `SKILL.md` records its ID, owner and the agents it is shared with in `metadata`.
