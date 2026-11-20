# Agent Knowledge Base

One folder per subagent in `.claude/agents/`. Each holds reference notes taken from **official documentation**, written on 2026-11-20. Every note lists its `Sources:` (exact URLs) and its `Fetched:` date, and ends with a "Project application" section.

**Rule:** every agent reads `knowledge/<its-name>/INDEX.md` and the notes it lists *before answering* (this is in each agent's system prompt).

| Folder | Main official sources |
|---|---|
| [orchestrator](orchestrator/) | code.claude.com (subagents, workflows), git-scm.com, docs.github.com |
| [meta-agent](meta-agent/) | code.claude.com (subagents, skills, memory, best practices) |
| [nltk-expert](nltk-expert/) | nltk.org (tokenize, stopwords, VADER, FreqDist, collocations, data), github.com/cjhutto/vaderSentiment, pyodide.org |
| [spacy-expert](spacy-expert/) | spacy.io (pipelines, en_core_web_sm, entities, noun chunks, dependency parse, EntityRuler, displaCy) |
| [dataset-curator](dataset-curator/) | Hugging Face dataset cards (Amazon Reviews 2023, Yelp), huggingface_hub / datasets docs, pandas docs |
| [build-pipeline-engineer](build-pipeline-engineer/) | docs.netlify.com (Python builds), pip.pypa.io, spacy.io/usage/models, nltk.org/data, docs.python.org |
| [pyodide-engineer](pyodide-engineer/) | pyodide.org (getting started, packages, web worker, file system, deploying) |
| [frontend-engineer](frontend-engineer/) | developer.mozilla.org (Workers, Fetch, responsive design), w3.org WCAG 2.2 / WAI-ARIA APG |
| [dataviz-specialist](dataviz-specialist/) | chartjs.org, WCAG, colorbrewer2.org, MDN tables |
| [netlify-engineer](netlify-engineer/) | docs.netlify.com (build config, Python, netlify.toml, headers, caching, functions limits, deploys, CLI) |
| [qa-engineer](qa-engineer/) | docs.pytest.org, json-schema.org, python-jsonschema, playwright.dev, web.dev |
| [nlp-evaluator](nlp-evaluator/) | scikit-learn.org metrics, spacy.io Scorer, nltk.org VADER, vaderSentiment repo |
| [technical-writer](technical-writer/) | developers.google.com/style, diataxis.fr, official citations (NLTK, spaCy, VADER, datasets) |

Items a researcher could not confirm on a fetched page are marked **"(unverified)"**. Check them before relying on them. The meta-agent owns the structure of this folder, and each specialist owns the content of its own notes.
