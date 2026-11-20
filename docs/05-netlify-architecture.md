# 05 — Netlify: What It Can and Cannot Run, and the Recommended Architecture

> **Bottom line:** Netlify can run Python **only during the build**. Its runtime functions are **JavaScript/TypeScript/Go only**, and its new long‑lived "Netlify Server" is **Node.js only**. In the browser, **Pyodide can run NLTK but not spaCy**. Therefore: run the full NLTK + spaCy pipeline **at build time** over the dataset, ship the results as static JSON, and run **live NLTK in the browser with Pyodide** for user‑pasted reviews. Live spaCy on arbitrary text needs either an external Python API (optional tier) or is shown from precomputed examples.

Researched 2026‑11‑20 against current Netlify and Pyodide docs.

---

## 1. Capability matrix

| Where | Python? | NLTK? | spaCy? | Notes |
|---|---|---|---|---|
| **Netlify build** (Ubuntu 24.04 "Noble" image) | ✅ any official 3.x | ✅ | ✅ | Set version via `PYTHON_VERSION` env var, `runtime.txt`, or `Pipfile`. pip available; Netlify installs `requirements.txt` at the build root. |
| **Netlify Functions** (serverless) | ❌ | ❌ | ❌ | Docs: functions can be written in **TypeScript, JavaScript, Go** (Go via Lambda‑compatible API). No Python runtime. |
| **Netlify Background / Scheduled Functions** | ❌ | ❌ | ❌ | Same languages. |
| **Netlify Edge Functions** | ❌ | ❌ | ❌ | TypeScript/JavaScript (Deno) only; 20 MB compressed bundle limit. |
| **Netlify Server** (Early Access) | ❌ | ❌ | ❌ | Long‑lived **Node.js** apps (Express/Hono/Fastify). Not Python. |
| **Static site + Pyodide in the browser** | ✅ (CPython→WASM) | ✅ prebuilt (nltk 3.9.4) | ❌ not available | Current Pyodide stable = **314.0.8** (Python 3.14 line). spaCy and its C deps (thinc, blis, cymem, preshed, murmurhash, srsly) are absent from the package list. |

### Netlify Functions limits (for reference, from Functions configuration docs)

| Limit | Value |
|---|---|
| Synchronous execution | 60 s |
| Background execution | 15 min |
| Memory | 1024 MB default, up to 4096 MB |
| Buffered request/response payload | 6 MB |
| Streamed response | 20 MB |
| Background payload | 256 KB |

These are moot for Python, but relevant if the team adds a JS function (e.g., a proxy).

### Why "just pip install spaCy in Pyodide" doesn't work

`micropip` installs **pure‑Python** wheels or wheels compiled for Emscripten/WASM. spaCy depends on Cython/C extensions with no official WASM wheels. Community attempts (`spacy-wasm`) require custom Emscripten toolchains and are unmaintained — **too risky for a graded deadline**. Re‑check in future: PEP 783 now allows WASM wheels on PyPI, so this may change.

### Why "spawn python from a JS function" doesn't work

The function runtime has no Python interpreter (a common forum failure: `spawn python3 ENOENT`). Build‑time Python is not present at runtime.

---

## 2. Recommended architecture — "Build‑time NLP + in‑browser NLTK"

```text
┌──────────────────────────── Netlify BUILD (Python 3.12) ───────────────────────────┐
│ data/reviews_sample.jsonl  ──►  pipeline/build.py                                  │
│                                  ├─ NLTK: sent/word tokenize, stopwords, VADER,     │
│                                  │        FreqDist, collocations (corpus-level)     │
│                                  ├─ spaCy: NER (+EntityRuler), noun chunks,         │
│                                  │         lemmas, dependency aspect↔opinion        │
│                                  └─ writes site/data/*.json                         │
│ copies nltk_data/{punkt_tab,stopwords,vader_lexicon} → site/nltk_data/             │
└───────────────────────────────────────────────┬────────────────────────────────────┘
                                                ▼  publish = "site"
┌──────────────────────────── Netlify CDN (static) ──────────────────────────────────┐
│ index.html + JS + Chart lib                                                        │
│  • Dashboard tab: reads site/data/*.json — sentiment distribution, VADER vs stars, │
│    top collocations, top aspects w/ sentiment, entity leaderboards                 │
│    (people / places / brands / products), per‑review drill‑down                    │
│  • "Analyze your review" tab: Pyodide in a Web Worker                              │
│      loadPackage("nltk") → load lexicons from /nltk_data → VADER per sentence,     │
│      keywords, n‑grams — all live, no server                                       │
│  • Live spaCy features: see tiers below                                            │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### Live spaCy options (pick one; team decision)

| Tier | How | Pros | Cons |
|---|---|---|---|
| **1 — All‑Netlify (default)** | Live box does NLTK only; spaCy views available for every dataset review (precomputed) and a gallery of ~20 curated "try these" examples. Live box labels entities as "available in dataset mode". | 100% on Netlify, zero servers, zero cost, nothing to break during grading | No spaCy on *new* user text |
| **1b — JS approximation** | Add a lightweight JS NER (e.g. `compromise` / `wink-nlp`) for live entities | Still all‑Netlify | It isn't spaCy — must be labelled clearly; does not satisfy "spaCy" requirement on its own |
| **2 — External Python API** | Tiny FastAPI (spaCy + NLTK) on a free Python host (e.g. Hugging Face Spaces); Netlify `[[redirects]] from="/api/*" to="https://<space>/:splat" status=200` proxies it so the browser only talks to the Netlify domain | Real spaCy on any text | Part of the stack runs off‑Netlify; cold starts; another deploy to maintain |

**Recommendation:** ship **Tier 1** as the guaranteed baseline (meets "deployed on Netlify" strictly; both libraries demonstrably used — spaCy at build, NLTK at build *and* live). Add **Tier 2 behind a feature flag** only if the instructor accepts a non‑Netlify helper; the UI must degrade gracefully to Tier 1 if the API is down.

---

## 3. Build configuration sketch

`netlify.toml`
```toml
[build]
  command = "python pipeline/build.py"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.12"
  NLTK_DATA = "/opt/build/repo/nltk_data"

[[headers]]
  for = "/data/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"
```

`requirements.txt` (at repo root — Netlify installs it automatically)
```text
nltk==3.10.4
spacy==3.8.18
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

Notes:
- **Commit `nltk_data/`** (punkt_tab, stopwords, vader_lexicon — a few MB) instead of downloading at build; avoids network flakiness and NLTK 3.10's proxy‑download guard.
- Keep the dataset sample small (1–3k reviews) so the build stays well within Netlify's build time limit (verify the plan's limit in the Netlify UI; the free tier has historically been ~15 min). `nlp.pipe` on 3k reviews with `en_core_web_sm` takes on the order of a minute.
- Cache: Netlify caches pip downloads between builds; first build is the slowest.
- Local parity: `netlify dev` / `netlify build` via Netlify CLI, or just run `python pipeline/build.py && python -m http.server -d site`.

## 4. Pyodide front‑end sketch (Web Worker)

```js
// worker.js
importScripts("https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.js");
let py;
async function init() {
  py = await loadPyodide();
  await py.loadPackage("nltk");
  // copy lexicons shipped with the site into Pyodide's virtual FS
  for (const f of ["sentiment/vader_lexicon.zip", "corpora/stopwords.zip",
                   "tokenizers/punkt_tab.zip"]) {
    const buf = new Uint8Array(await (await fetch(`/nltk_data/${f}`)).arrayBuffer());
    py.FS.mkdirTree("/nltk_data/" + f.split("/")[0]);
    py.FS.writeFile("/nltk_data/" + f, buf);
  }
  await py.runPythonAsync(`
import nltk; nltk.data.path.insert(0, "/nltk_data")
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()`);
}
const ready = init();
onmessage = async (e) => {
  await ready;
  py.globals.set("review", e.data);
  const out = await py.runPythonAsync(`
import json
json.dumps({"doc": sia.polarity_scores(review),
            "sentences": [[s, sia.polarity_scores(s)["compound"]] for s in nltk.sent_tokenize(review)]})`);
  postMessage(JSON.parse(out));
};
```

- Check the exact `.zip` vs unzipped layout NLTK expects (`nltk.data.find`) when wiring this; unzipped folders also work.
- First load downloads Pyodide (~10 MB+) — show a loading state and run it in a Worker so the UI stays responsive.
- Pin the Pyodide version; verify the URL against https://pyodide.org/en/stable/usage/downloading-and-deploying.html (CDN path format changed with the 314.x versioning). Self‑hosting the Pyodide distribution inside `site/` is also allowed and removes the CDN dependency.

## 5. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Build fails installing spaCy on a new default Python | Pin `PYTHON_VERSION=3.12` |
| Model download from GitHub fails during build | Pin wheel URL; optional: vendor the wheel in repo (~13 MB) |
| NLTK data download blocked | Commit `nltk_data/` |
| Pyodide CDN slow/blocked | Self‑host Pyodide files in `site/pyodide/` |
| NLTK version skew (3.10 build vs 3.9.4 Pyodide) | Use only stable APIs (VADER, tokenize, FreqDist, collocations) — identical across both |
| Instructor expects live spaCy | Tier 2 API behind flag; document in report why Netlify can't host Python at runtime |

## Sources

- Netlify Functions overview: https://docs.netlify.com/build/functions/overview/
- Netlify Functions get started (TS/JS; Go via Lambda‑compatible API): https://docs.netlify.com/build/functions/get-started/
- Netlify Functions configuration & limits: https://docs.netlify.com/build/functions/configuration/
- Netlify Go functions: https://docs.netlify.com/functions/build-with-go
- Netlify Edge Functions limits: https://docs.netlify.com/build/edge-functions/limits/
- Netlify Server (Early Access, Node.js): https://docs.netlify.com/build/server/
- Available software at build time (Ubuntu 24.04, Python via PYTHON_VERSION/runtime.txt/Pipfile): https://docs.netlify.com/build/configure-builds/available-software-at-build-time/
- Manage dependencies (requirements.txt): https://docs.netlify.com/build/configure-builds/manage-dependencies/
- Netlify blog — configurable Python versions in builds: https://www.netlify.com/blog/announcing-configurable-python-versions-in-netlify-builds
- Forum — no Python Lambda functions on Netlify: https://answers.netlify.com/t/python-lambda-functions/3423
- Forum — `spawn python3 ENOENT`: https://answers.netlify.com/t/spawn-python3-enoent-when-running-a-python-script-in-nextjs-api/91823
- Netlify redirects/proxying: https://docs.netlify.com/manage/routing/redirects/rewrites-proxies/
- Pyodide packages (nltk present, spaCy absent; v314.0.8): https://pyodide.org/en/stable/usage/packages-in-pyodide.html
- Pyodide loading packages / micropip: https://pyodide.org/en/stable/usage/loading-packages.html
- spacy-wasm community attempt: https://github.com/SyedAhkam/spacy-wasm
- PEP 783 (Emscripten/WASM wheels): https://peps.python.org/pep-0783/
