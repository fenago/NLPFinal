# Customer Review Analyzer

A static web app that reads real Yelp reviews and shows their **sentiment**, **key phrases**, **aspects** (for example "fish sandwich" or "service" with the opinions about them) and the **people, places, brands and products** they mention. It uses both **NLTK** and **spaCy** and deploys to **Netlify with no server**.

- **Dashboard:** sentiment distribution, VADER score vs star rating, top words and key phrases, aspect sentiment, entity leaderboards and a drill-down into every review.
- **Analyze your own review:** paste text and get sentence-by-sentence sentiment, top words and key phrases, computed live in your browser by NLTK running in Pyodide.

Every result panel carries a badge that says which library produced it: **NLTK**, **spaCy** or **NLTK + spaCy**.

## How NLTK and spaCy split the work

| Feature | Library | Where it runs |
|---|---|---|
| Sentence and word tokenizing (Punkt, Treebank), stopwords with negations kept | NLTK | Netlify build and browser |
| VADER sentiment per review and per sentence | NLTK | Netlify build and browser |
| Top words (`FreqDist`), key phrases (bigram collocations, likelihood ratio) | NLTK | Netlify build (corpus) and browser (one review) |
| Named entities mapped to people, places, brands and products, plus an EntityRuler | spaCy | Netlify build only |
| Noun-chunk aspects normalised to lemmas ("battery life") | spaCy | Netlify build only |
| Aspect–opinion pairs from the dependency parse (`amod`, `acomp` + `nsubj`, `neg` flips) | spaCy | Netlify build only |
| Aspect sentiment, and sentiment with entity names masked | spaCy finds the spans, NLTK VADER scores them | Netlify build only |

spaCy cannot run in the browser: it needs compiled extensions that have no WebAssembly build. Netlify Functions cannot run Python either. spaCy results therefore exist only for the dataset reviews and the curated examples, and the live tab says so. For background, see [docs/05-netlify-architecture.md](docs/05-netlify-architecture.md).

## Architecture

```text
┌──────────── Netlify build (Python 3.12) ─────────────┐
│ data/reviews_sample.jsonl (197 Yelp reviews)         │
│ data/entity_patterns.jsonl (EntityRuler)             │
│        │                                             │
│        ▼                                             │
│ pipeline/build.py                                    │
│   ├─ nlp/nltk_analyzer.py  (NLTK 3.10.4)             │
│   └─ nlp/spacy_analyzer.py (spaCy 3.8.18 + sm 3.8.0) │
│        │ writes site/data/*.json (docs/data-contract) │
│        │ copies nltk_data/ and nltk_analyzer.py      │
│ scripts/fetch_pyodide.py                             │
│   └─ site/pyodide/: Pyodide 314.0.8 core (npm) +     │
│      nltk-3.10.4 wheel (PyPI), hash-checked          │
└───────────────────────┬──────────────────────────────┘
                        ▼  publish = "site"
┌──────────── Netlify CDN (static files only) ──────────┐
│ index.html, app.js, charts.js (Chart.js 4.6.1, local) │
│ Dashboard and Reviews tabs ← site/data/*.json         │
│ Live tab → worker.mjs (module Web Worker)             │
│   Pyodide + the same nltk_analyzer.py + nltk_data     │
│   (all served from the same origin, no CDN)           │
└───────────────────────────────────────────────────────┘
```

The browser runs **the same `nltk_analyzer.py` and the same NLTK version (3.10.4)** as the build. A test checks that live output is identical to the build output for all 197 reviews. NLTK's optional `regex` dependency has no WebAssembly wheel on PyPI, so the browser uses a small same-origin shim (`site/vendor-py/regex/`); a test proves it gives identical results.

## Run it locally

You need Python 3.12 (3.11 or later works) and, for the browser tests, Node.js 22.

1. Create a virtual environment and install the dependencies:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt   # requirements.txt + pytest, jsonschema
   ```

2. Run the same build that Netlify runs:

   ```bash
   python pipeline/build.py          # NLTK + spaCy → site/data/*.json (about 5 s)
   python scripts/fetch_pyodide.py   # Pyodide + NLTK wheel → site/pyodide/ (15 MB, cached in .cache/)
   ```

3. Serve the site and open http://localhost:8000:

   ```bash
   python -m http.server 8000 -d site
   ```

   To serve it with the same headers as Netlify (CSP, caching, `.wasm` type), run `python tests/support/serve_netlify.py --port 8000` instead.

## Run the tests

```bash
pytest -q                                      # unit, golden, JSON-schema, budget and guardrail tests
npm install                                    # Playwright 1.63 for the browser tests (once)
npx playwright install chromium                # once, if you have no Chromium for Playwright
npm run test:pyodide                           # headless Pyodide: live NLTK == build output, all reviews
npm run test:e2e                               # Playwright: dashboard, drill-down, live tab, phone viewport
npm run test:e2e:netlify-headers               # the same tests with netlify.toml headers applied
E2E_BASE_URL=https://<your-deploy-preview>.netlify.app npm run test:e2e   # against a deploy preview
```

Golden files live in `tests/golden/`. After an intended change, regenerate them with `UPDATE_GOLDEN=1 pytest tests/test_golden.py` and review the diff.

## Deploy to Netlify

All settings come from [`netlify.toml`](netlify.toml): build command, `publish = "site"`, `PYTHON_VERSION = "3.12"`, `NLTK_DATA`, and cache and content-type headers. There are no functions and no environment variables to set.

**Option A: connect the repository**

1. In Netlify, select **Add new project → Import an existing project** and choose this GitHub repository.
2. Keep the detected settings (they are read from `netlify.toml`) and select **Deploy**.
3. Every pull request gets a deploy preview; production deploys from `main`.

**Option B: Netlify CLI**

```bash
npm install -g netlify-cli
netlify login
netlify init            # link or create the site
netlify deploy --build  # draft deploy, prints a preview URL
netlify deploy --build --prod
```

After the first deploy, check the build log for the Python 3.12 line and the `[build]` and `[pyodide]` stage timings. Then confirm the headers with `curl -sI https://<site>/pyodide/v314.0.8/pyodide.asm.wasm`, which should return `content-type: application/wasm` and a one-year `cache-control`.

## Repository layout

| Path | What it is |
|---|---|
| `data/` | Review sample, EntityRuler patterns, hand-written demo reviews, [SOURCES.md](data/SOURCES.md) |
| `nlp/` | `nltk_analyzer.py` (shared with the browser), `spacy_analyzer.py` (build only) |
| `pipeline/build.py` | The Netlify build step |
| `scripts/` | Sample curation, pattern builder, Pyodide and Chart.js fetchers, evaluation |
| `nltk_data/` | Vendored English `punkt_tab`, `stopwords`, `vader_lexicon` (340 KB) |
| `schemas/`, [docs/data-contract.md](docs/data-contract.md) | JSON contract between the build and the site (v1.0.0) |
| `site/` | Static site; `site/data`, `site/pyodide`, `site/nltk_data`, `site/py` are generated |
| `tests/` | pytest, Node Pyodide parity test, Playwright e2e |
| [reports/evaluation.md](reports/evaluation.md) | Metrics and error analysis |

## Results

The [evaluation report](reports/evaluation.md) has the full numbers. In short:

- VADER agrees with the star rating on 60.9% of reviews (3 classes, macro-F1 0.430). It over-predicts positive on long reviews.
- Entity precision is 64.7% with the EntityRuler and 62.7% without it, on 68 hand-checked entities.
- Aspect–opinion pair precision is 83% after requiring evaluative adjectives (43% before), on 30 hand-judged pairs.

## Limitations

- The sample is small: 197 real reviews from Yelp Review Full, fetched as two pages of 100 rows each. Amazon Reviews 2023 could not be downloaded in the build environment, so the app runs in restaurant/business mode, and brands and products come only from names in the review text.
- spaCy results are not available for text you type, by design (no server, no Python at runtime).
- VADER misses sarcasm, polite complaints and context-dependent words such as "cold". The small spaCy model tags some dish names as people. See the [error analysis](reports/evaluation.md#4-error-analysis).
- The first live analysis downloads about 15 MB (Pyodide and NLTK), which takes about 4 seconds on a fast connection. Later visits use the browser cache.

## Data and credits

- **Reviews:** Yelp Review Full ([Hugging Face](https://huggingface.co/datasets/Yelp/yelp_review_full)), from the Yelp Dataset Challenge 2015. Used under the Yelp Dataset terms for academic, non-commercial use. Cite: Xiang Zhang, Junbo Zhao, Yann LeCun. 2015. *Character-level Convolutional Networks for Text Classification.* NeurIPS 28. https://arxiv.org/abs/1509.01626. Curation details: [data/SOURCES.md](data/SOURCES.md).
- **VADER:** C.J. Hutto and Eric Gilbert. 2014. *VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text.* ICWSM.
- **Libraries:** [NLTK](https://www.nltk.org/) (Apache 2.0), [spaCy](https://spacy.io/) and `en_core_web_sm` (MIT), [Pyodide](https://pyodide.org/) (MPL 2.0), [Chart.js](https://www.chartjs.org/) (MIT).
