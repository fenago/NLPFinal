# Expert Roster — Agent Team for the Customer Review Analyzer

**Project decision (locked):** everything runs on Netlify, with no outside servers.
- **Build time (Netlify, Python 3.12):** NLTK and spaCy run over the committed review sample and write static JSON to `site/data/`.
- **Static site (Netlify CDN):** an HTML/CSS/JS dashboard that reads that JSON.
- **In the browser (Pyodide):** NLTK runs live for "Analyze your own review." spaCy is not used in the browser; its output appears for dataset reviews and curated examples only.

The roles below cover only what that stack needs. See [What we deliberately do not need](#what-we-deliberately-do-not-need).

---

## 1. The roster (13 agents)

| # | Agent | ID | One-line job description |
|---|---|---|---|
| 1 | **Orchestrator** | `ORC` | Splits the project into tasks, assigns them to the right experts in dependency order, approves the JSON data contract, merges work and decides go or no-go at each phase. |
| 2 | **Meta Agent** | `META` | Designs, writes and improves every other agent's prompt and skill set, reviews how well the agents perform, and keeps this roster and the handoff templates current. |
| 3 | **NLTK Expert** | `NLTK` | Owns the NLTK side: tokenizing, stopwords (negations kept), per-sentence VADER sentiment, word frequencies and collocations. The same code runs at build time and in Pyodide. |
| 4 | **spaCy Expert** | `SPACY` | Owns the spaCy side: named entities with an EntityRuler for brands and products, noun-chunk aspects, lemmas and dependency-based aspect-to-opinion pairs. Build time only. |
| 5 | **Dataset Curator** | `DATA` | Pulls, cleans, samples by star rating and removes personal data from the Amazon Reviews 2023 sample (plus the optional Yelp sample), builds the brand/product list for the EntityRuler, and records the license and citation. |
| 6 | **Build Pipeline Engineer** | `BUILD` | Writes `pipeline/build.py`, which runs the NLTK and spaCy modules over the sample, writes `site/data/*.json` to the agreed contract, and keeps the Netlify build fast and reproducible. |
| 7 | **Pyodide Engineer** | `PYO` | Runs NLTK in the browser: a Web Worker that loads Pyodide and NLTK, mounts the bundled `nltk_data`, runs the shared NLTK code and returns JSON to the UI. Pyodide is self-hosted or pinned to one version. |
| 8 | **Frontend Engineer** | `UI` | Builds the static site (layout, dashboard and "Analyze your review" tabs, review drill-down, loading and error states), so that it works on phones and meets accessibility standards. |
| 9 | **Data Visualization Specialist** | `VIZ` | Designs the charts: sentiment distribution, VADER score vs. star rating, top collocations, aspects with sentiment, and entity leaderboards for people, places, brands and products. |
| 10 | **Netlify Deployment Engineer** | `NET` | Owns `netlify.toml`, the Python version setting, the publish folder, cache and file-type headers for the Pyodide/WASM files, deploy previews, reading build logs and the production deploy. |
| 11 | **QA / Test Engineer** | `QA` | Writes and runs Python unit tests for the pipeline and browser end-to-end tests with Playwright for both tabs (including the Pyodide cold start), plus checks on file sizes and page speed. |
| 12 | **NLP Evaluation Analyst** | `EVAL` | Measures quality independently of the NLTK and spaCy experts: VADER labels vs. star ratings (accuracy and confusion matrix), entity precision and recall with and without the EntityRuler, and how often aspect pairs are correct. |
| 13 | **Technical Writer** | `DOC` | Writes the project README, the in-app "About / Method" page, dataset credits and the final report and demo script, using the experts' notes and EVAL's numbers. |

### Who works in each phase

| Phase | Lead | Active agents |
|---|---|---|
| **Design** | ORC | META (sets up the agents), NLTK, SPACY, DATA, BUILD, PYO, UI, VIZ, NET (agree the JSON contract and the size budgets) |
| **Build** | ORC | DATA → NLTK + SPACY → BUILD → PYO + UI + VIZ; NET in parallel (first deploy preview early) |
| **Test** | QA | EVAL (metrics), NLTK and SPACY (fixes), PYO and UI (browser fixes), META (agent performance review) |
| **Deploy** | NET | ORC (go/no-go), QA (smoke test on the production URL), DOC (final report and links) |

### Who owns which files

| File or folder | Owner | Reviewers |
|---|---|---|
| `data/reviews_sample.jsonl`, `data/entity_patterns.jsonl` | DATA | SPACY, EVAL |
| `nlp/nltk_analyzer.py` (shared by the build and Pyodide) | NLTK | PYO, QA |
| `nlp/spacy_analyzer.py` | SPACY | BUILD, QA |
| `pipeline/build.py`, `requirements.txt` | BUILD | NET, QA |
| `site/data/*.json` contract (`docs/data-contract.md`) | ORC (approves) / BUILD (writes) | UI, VIZ, PYO |
| `nltk_data/` (vendored) | NLTK | BUILD, PYO |
| `site/worker.js`, `site/pyodide/` | PYO | NET, QA |
| `site/index.html`, `site/*.css`, `site/app.js` | UI | VIZ, QA |
| `site/charts.js` | VIZ | UI |
| `netlify.toml` | NET | BUILD, PYO |
| `tests/` (pytest + Playwright) | QA | all owners |
| `reports/evaluation.md` | EVAL | NLTK, SPACY, DOC |
| `README.md`, final report | DOC | ORC |
| Agent prompts and skills, `docs/expert-roster.md` | META | ORC |

---

## 2. Skills and who shares them

Each skill is listed once with the agents that need it. **Owner** is the agent accountable for that skill on the team; **Shared with** lists the other agents that also use it.

### A. Coordination and the agents themselves

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S01 | Breaking work into tasks, ordering them by dependency, tracking milestones | ORC | META |
| S02 | Merge and approval gates (check each piece against the data contract, decide go or no-go) | ORC | QA, NET |
| S03 | Agent design: writing role prompts and skills, handoff briefs, keeping each agent's scope tight | META | ORC |
| S04 | Reviewing agent output and improving prompts and skills over time | META | ORC, EVAL |
| S05 | **Netlify constraint guardrail**: Python runs only at build time; Functions are JS/TS/Go only; Netlify Server is Node.js only; Pyodide has NLTK but not spaCy | ORC | META, NET, BUILD, PYO, NLTK, SPACY |
| S06 | Git/GitHub workflow (branches, pull requests, protecting `main`, clear commits) | ORC | **all agents** |

### B. NLP: NLTK

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S07 | NLTK tokenizing (`sent_tokenize`, `word_tokenize`, `TweetTokenizer`) | NLTK | PYO, BUILD |
| S08 | Stopword engineering (keep negations, add domain words; never remove stopwords before VADER) | NLTK | SPACY, EVAL |
| S09 | VADER sentiment: compound score thresholds, scoring each sentence, rule behavior and known limits | NLTK | PYO, EVAL |
| S10 | Frequency and collocations (`FreqDist`, PMI and likelihood-ratio finders, `apply_freq_filter`) | NLTK | BUILD, VIZ |
| S11 | Packaging `nltk_data` (punkt_tab, stopwords, vader_lexicon; `NLTK_DATA`; committing it to the repo; the NLTK 3.10 proxy-download guard) | NLTK | BUILD, PYO, NET |
| S12 | Writing NLTK code that also runs in Pyodide (APIs that are the same in NLTK 3.10 and Pyodide's 3.9.4, no file or network access) | NLTK | PYO, QA |

### C. NLP: spaCy

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S13 | spaCy pipeline and models (`en_core_web_sm` 3.8.0 wheel pin, `nlp.pipe`, `select_pipes`, batch size) | SPACY | BUILD |
| S14 | Named entity recognition and mapping labels to app groups (PERSON → people; GPE/LOC/FAC → places; ORG → brands; PRODUCT → products) | SPACY | VIZ, EVAL |
| S15 | EntityRuler pattern design built from dataset product data (store, title, model-number regex) | SPACY | DATA |
| S16 | Noun-chunk aspect extraction and normalization (lemmas, remove determiners and pronouns) | SPACY | NLTK, VIZ |
| S17 | Dependency-parse aspect-to-opinion rules (`amod`, `acomp` + `nsubj`, `neg` flips the sign) | SPACY | NLTK, EVAL |
| S18 | Combining spaCy and VADER: hide entity names before scoring, score each opinion word for aspect sentiment | SPACY | NLTK, EVAL |

### D. Data

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S19 | Finding datasets and reading their terms (Amazon Reviews 2023, Yelp; academic and non-commercial use; citations) | DATA | DOC |
| S20 | Sampling by star rating, cleaning text, removing user IDs and other personal data, writing JSONL | DATA | EVAL |
| S21 | Designing the JSON data contract (schema for `site/data/*.json`, field names, versioning) | BUILD | ORC, NLTK, SPACY, PYO, UI, VIZ |
| S22 | Keeping data small (file size limits, rounding numbers, splitting files, lazy loading) | BUILD | DATA, UI, VIZ, QA |

### E. Python build step

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S23 | Python 3.12 engineering (modules, typing, CLI scripts) | BUILD | NLTK, SPACY, DATA, EVAL, QA, PYO |
| S24 | Reproducible builds (`requirements.txt` with pinned versions and wheel URLs, consistent random seeds, the same output every run) | BUILD | NET, SPACY |
| S25 | Build-time performance (batching, keeping the build well under the time limit, caching) | BUILD | NET, SPACY |

### F. Browser and Pyodide

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S26 | Pyodide runtime (`loadPyodide`, `loadPackage("nltk")`, the virtual file system `FS.writeFile`, `runPythonAsync`, passing data between JS and Python) | PYO | QA |
| S27 | Self-hosting Pyodide and pinning its version (files in `site/pyodide/`, `.wasm` file type, caching) | PYO | NET |
| S28 | Web Workers and async message passing between JS and Python | PYO | UI |
| S29 | Cold-start experience (progress bar, warming up while idle, timeouts, a fallback message) | PYO | UI, QA |

### G. Frontend and visualization

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S30 | Plain HTML/CSS/JS (no server code), layout that works on phones | UI | VIZ, PYO |
| S31 | Accessibility (WCAG AA: contrast, keyboard use, ARIA live regions for results) | UI | VIZ, QA |
| S32 | Charting library (Chart.js or D3: bar, stacked bar, heatmap or confusion matrix, leaderboard) | VIZ | UI |
| S33 | Visual encoding of sentiment (color scale that works for color-blind users, labels as well as color) | VIZ | UI, EVAL |
| S34 | UX writing (empty states, error messages, explaining "dataset mode vs. live mode" when spaCy isn't available live) | UI | DOC, VIZ |

### H. Netlify deployment

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S35 | `netlify.toml` (build command, publish folder, `PYTHON_VERSION`, `NLTK_DATA`, `[[headers]]` cache and file-type rules) | NET | BUILD, PYO |
| S36 | Netlify CLI, deploy previews, reading build logs, rollbacks | NET | QA, ORC |
| S37 | Static-hosting performance (cache headers, compression, file sizes for JSON and Pyodide) | NET | PYO, UI, QA |

### I. Testing and evaluation

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S38 | pytest unit tests and saved expected-output tests for the NLTK and spaCy modules | QA | NLTK, SPACY, BUILD |
| S39 | Checking the JSON output against the data contract | QA | BUILD, UI |
| S40 | Playwright browser tests (both tabs, Pyodide cold start, mobile screen size) | QA | PYO, UI |
| S41 | NLP metrics (accuracy, precision, recall, F1, confusion matrix, comparing with and without the EntityRuler) | EVAL | NLTK, SPACY |
| S42 | Error analysis (sarcasm, domain slang, mislabeled brands) feeding fixes back to the NLP experts | EVAL | NLTK, SPACY, DOC |

### J. Documentation

| ID | Skill | Owner | Shared with |
|---|---|---|---|
| S43 | Technical writing (README, method page, final report, demo script) | DOC | ORC, META |
| S44 | Explaining NLP choices (why NLTK vs. spaCy for each feature, known limits) | DOC | NLTK, SPACY, EVAL |
| S45 | Citations and dataset credits | DOC | DATA |

---

## 3. Skill matrix (✔ = needs the skill, ★ = owns it)

| Skill | ORC | META | NLTK | SPACY | DATA | BUILD | PYO | UI | VIZ | NET | QA | EVAL | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S01 Task planning | ★ | ✔ | | | | | | | | | | | |
| S02 Approval gates | ★ | | | | | | | | | ✔ | ✔ | | |
| S03 Agent design | ✔ | ★ | | | | | | | | | | | |
| S04 Agent review | ✔ | ★ | | | | | | | | | | ✔ | |
| S05 Netlify guardrail | ★ | ✔ | ✔ | ✔ | | ✔ | ✔ | | | ✔ | | | |
| S06 Git workflow | ★ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| S07 NLTK tokenizing | | | ★ | | | ✔ | ✔ | | | | | | |
| S08 Stopwords | | | ★ | ✔ | | | | | | | | ✔ | |
| S09 VADER | | | ★ | | | | ✔ | | | | | ✔ | |
| S10 Freq/collocations | | | ★ | | | ✔ | | | ✔ | | | | |
| S11 nltk_data packaging | | | ★ | | | ✔ | ✔ | | | ✔ | | | |
| S12 Pyodide-safe NLTK | | | ★ | | | | ✔ | | | | ✔ | | |
| S13 spaCy pipeline | | | | ★ | | ✔ | | | | | | | |
| S14 NER mapping | | | | ★ | | | | | ✔ | | | ✔ | |
| S15 EntityRuler | | | | ★ | ✔ | | | | | | | | |
| S16 Noun-chunk aspects | | | ✔ | ★ | | | | | ✔ | | | | |
| S17 Dependency rules | | | ✔ | ★ | | | | | | | | ✔ | |
| S18 spaCy + VADER | | | ✔ | ★ | | | | | | | | ✔ | |
| S19 Dataset terms | | | | | ★ | | | | | | | | ✔ |
| S20 Sampling/cleaning | | | | | ★ | | | | | | | ✔ | |
| S21 Data contract | ✔ | | ✔ | ✔ | | ★ | ✔ | ✔ | ✔ | | | | |
| S22 Small data files | | | | | ✔ | ★ | | ✔ | ✔ | | ✔ | | |
| S23 Python 3.12 | | | ✔ | ✔ | ✔ | ★ | ✔ | | | | ✔ | ✔ | |
| S24 Reproducible builds | | | | ✔ | | ★ | | | | ✔ | | | |
| S25 Build performance | | | | ✔ | | ★ | | | | ✔ | | | |
| S26 Pyodide runtime | | | | | | | ★ | | | | ✔ | | |
| S27 Self-host Pyodide | | | | | | | ★ | | | ✔ | | | |
| S28 Web Workers | | | | | | | ★ | ✔ | | | | | |
| S29 Cold-start UX | | | | | | | ★ | ✔ | | | ✔ | | |
| S30 HTML/CSS/JS | | | | | | | ✔ | ★ | ✔ | | | | |
| S31 Accessibility | | | | | | | | ★ | ✔ | | ✔ | | |
| S32 Charting | | | | | | | | ✔ | ★ | | | | |
| S33 Sentiment visuals | | | | | | | | ✔ | ★ | | | ✔ | |
| S34 UX writing | | | | | | | | ★ | ✔ | | | | ✔ |
| S35 netlify.toml | | | | | | ✔ | ✔ | | | ★ | | | |
| S36 CLI/previews/logs | ✔ | | | | | | | | | ★ | ✔ | | |
| S37 Static performance | | | | | | | ✔ | ✔ | | ★ | ✔ | | |
| S38 pytest | | | ✔ | ✔ | | ✔ | | | | | ★ | | |
| S39 Contract checks | | | | | | ✔ | | ✔ | | | ★ | | |
| S40 Playwright E2E | | | | | | | ✔ | ✔ | | | ★ | | |
| S41 NLP metrics | | | ✔ | ✔ | | | | | | | | ★ | |
| S42 Error analysis | | | ✔ | ✔ | | | | | | | | ★ | ✔ |
| S43 Technical writing | ✔ | ✔ | | | | | | | | | | | ★ |
| S44 Explaining NLP choices | | | ✔ | ✔ | | | | | | | | ✔ | ★ |
| S45 Citations | | | | | ✔ | | | | | | | | ★ |

**Skills shared most widely (good topics for shared skill files the Meta Agent writes once and reuses):**
- **S06 Git workflow:** all 13 agents.
- **S21 JSON data contract:** 7 agents. This is the main link between the Python build and the browser.
- **S23 Python 3.12:** 7 agents.
- **S05 Netlify constraint guardrail:** 7 agents. This stops anyone proposing a server or a Python function.
- **S11 `nltk_data` packaging:** 4 agents (NLTK, BUILD, PYO, NET). It's the main build-to-browser handoff for NLTK.

---

## 4. What we deliberately do not need

| Role you might expect | Why it's left out |
|---|---|
| Backend / API engineer | No runtime server. Netlify Functions can't run Python, and the decision rules out outside servers. |
| Database engineer | All data is static JSON built at deploy time. Nothing is stored at runtime. |
| ML training / MLOps engineer | No model training. VADER is rule-based, and spaCy uses a pretrained `en_core_web_sm`. |
| Auth / security engineer | No logins, no user data stored, nothing to protect beyond standard static-site headers (covered by NET). |
| Cloud / DevOps / container engineer | Netlify's build and CDN replace containers and infrastructure. NET covers it. |
| JS NLP engineer (compromise / wink-nlp) | Not spaCy, so it would weaken the "NLTK + spaCy" requirement. spaCy output comes from build time only. |
| Pyodide spaCy porting engineer | Compiling spaCy to WebAssembly is unsupported and too risky for a graded deadline (see doc 05). |

---

## 5. Agent handoff order (for the Orchestrator)

1. **META** creates the 12 other agents from this roster: role prompt, owned skills, shared-skill files and file ownership.
2. **ORC** has BUILD write `docs/data-contract.md` and gets UI, VIZ, PYO, NLTK and SPACY to agree it. This is gate 1.
3. **DATA** commits the sample and the EntityRuler patterns. Then **NLTK** and **SPACY** deliver their analyzer modules, each with pytest tests (QA reviews).
4. **BUILD** connects the pipeline. **NET** gets a first deploy preview working early (with placeholder JSON if needed).
5. **PYO** builds the browser side using `nlp/nltk_analyzer.py` and the vendored `nltk_data`, working alongside **UI** and **VIZ** on the dashboard.
6. **QA** runs the full test suite against the deploy preview, and **EVAL** produces `reports/evaluation.md`. This is gate 2.
7. **NET** deploys to production, **QA** smoke-tests the live URL, and **DOC** finishes the report. **ORC** makes the final go/no-go. **META** writes a short review of how each agent performed.
