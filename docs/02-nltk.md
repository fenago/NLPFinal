# 02 — What NLTK Does Best in the Customer Review Analyzer

> Role in the app: **the "statistics and sentiment" engine.** NLTK owns tokenization, stopword filtering, VADER sentiment, word frequencies, and collocations (key phrases by statistical association).

Verified with **NLTK 3.10.4** (PyPI, Python 3.13) on 2026‑11‑20. In the browser, Pyodide ships **NLTK 3.9.4** — same APIs used below.

---

## 1. Tokenizing

| Function | Use in the app |
|---|---|
| `nltk.sent_tokenize(text)` | Split a review into sentences so we can score sentiment **per sentence** (mixed reviews are common). |
| `nltk.word_tokenize(text)` | Penn‑Treebank‑style word tokens for frequency counts and collocations. |
| `nltk.tokenize.TweetTokenizer` | Optional: keeps emoticons/hashtags (`:)`, `#fail`) intact — useful for informal reviews. |

Required data package: **`punkt_tab`** (replaced the old `punkt` pickle in NLTK ≥ 3.8.2).

## 2. Stopwords

`nltk.corpus.stopwords.words("english")` — 198 common words. Recommended app tweaks:

- **Remove negations from the stopword list** (`not`, `no`, `nor`, `don't`, `won't`…) for keyword views — "not good" must not become "good".
- **Add domain stopwords** (`product`, `item`, `order`, `place`, `restaurant`, `get`, `would`) so frequency charts show meaningful words.
- Never strip stopwords **before VADER** — VADER needs them (negation, "but", intensifiers).

## 3. VADER sentiment (headline feature)

`nltk.sentiment.SentimentIntensityAnalyzer` (Hutto & Gilbert, 2014) — a lexicon + rules model tuned for short, informal, social/review text. No training required, runs in milliseconds, works in the browser.

Output: `{'neg', 'neu', 'pos', 'compound'}` where `compound ∈ [-1, 1]`.

Standard thresholds (from the VADER authors):

| compound | label |
|---|---|
| ≥ 0.05 | Positive |
| ≤ −0.05 | Negative |
| otherwise | Neutral |

Rules VADER handles that a naive word list does not: negation ("not great"), intensifiers ("super helpful"), ALL CAPS, `!!!`, contrastive "but" (weights the clause after "but" more heavily), and many emoticons/slang.

**Evaluation idea for the report:** map star ratings to labels (1–2 = neg, 3 = neutral, 4–5 = pos) and report VADER accuracy / confusion matrix against the dataset's stars. This gives the project a measurable result.

Data package: **`vader_lexicon`**.

## 4. Frequency and collocations (key phrases)

| Tool | Use |
|---|---|
| `nltk.FreqDist(words)` | Top words per product / per sentiment class ("what do negative reviews talk about?"). |
| `nltk.ngrams` / `nltk.bigrams` | Raw n‑gram counts. |
| `BigramCollocationFinder` + `BigramAssocMeasures.pmi` / `.likelihood_ratio` | Statistically meaningful phrases ("battery life", "customer service", "wait time"). |
| `TrigramCollocationFinder` | Three‑word phrases ("fried chicken sandwich"). |
| `finder.apply_freq_filter(3)` | **Essential** on real corpora — PMI over‑rewards rare pairs without it. |

Collocations are a *corpus‑level* feature: they shine on 100s–1000s of reviews (build time), and are weak on a single review.

## 5. Verified smoke test

Input: *"I ordered the Sony WH-1000XM5 headphones from Best Buy in Chicago. The noise cancelling is amazing but the battery life was disappointing. Customer service rep Maria was super helpful though!"*

```text
doc VADER:  {'neg': 0.132, 'neu': 0.534, 'pos': 0.333, 'compound': 0.8639}
per sentence:
   0.637  I ordered the Sony WH-1000XM5 headphones from Best Buy in Chicago.
  -0.511  The noise cancelling is amazing but the battery life was disappointing.
   0.790  Customer service rep Maria was super helpful though!
bigrams (PMI, single review): ('amazing','battery'), ('battery','life'), ('best','buy')
```

Lessons the team should act on:

1. **Per‑sentence scores reveal mixed reviews** — the overall 0.86 hides a real complaint. Show both.
2. **Entity names leak into sentiment**: the purely factual first sentence scores +0.64 because "Best" (in the brand *Best Buy*) is in the lexicon. Fix: use spaCy entities to **mask entity spans** (e.g., replace with `ENT`) before VADER.
3. **Collocations need a corpus** — "amazing battery" is a cross‑clause artifact; with `apply_freq_filter` on many reviews this disappears.

## 6. Reference code

```python
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures

NEGATIONS = {"not", "no", "nor", "don't", "won't", "isn't", "wasn't", "didn't", "never"}
STOP = (set(stopwords.words("english")) - NEGATIONS) | {"product", "item", "order", "would", "get"}
sia = SentimentIntensityAnalyzer()

def label(c): return "positive" if c >= 0.05 else "negative" if c <= -0.05 else "neutral"

def nltk_analyze(text):
    sents = nltk.sent_tokenize(text)
    per_sent = [{"text": s, **sia.polarity_scores(s)} for s in sents]
    doc = sia.polarity_scores(text)
    words = [t for t in nltk.word_tokenize(text.lower()) if t.isalpha() and t not in STOP]
    return {"sentiment": {**doc, "label": label(doc["compound"])},
            "sentences": per_sent,
            "top_words": nltk.FreqDist(words).most_common(15)}

def corpus_collocations(all_texts, n=20, min_freq=3):
    words = [t for txt in all_texts for t in nltk.word_tokenize(txt.lower())
             if t.isalpha() and t not in STOP]
    f = BigramCollocationFinder.from_words(words)
    f.apply_freq_filter(min_freq)
    return f.nbest(BigramAssocMeasures.likelihood_ratio, n)
```

## 7. Gotchas

- **NLTK data is separate from the pip package.** Download `punkt_tab`, `stopwords`, `vader_lexicon` into a project folder (e.g. `./nltk_data`) and set `NLTK_DATA`. Do this in the build, and copy the same files into the static site so the browser (Pyodide) can load them without hitting GitHub at runtime.
- **NLTK 3.10 security change:** `nltk.download()` now refuses to fetch through an HTTP proxy (`pathsec` SSRF guard) unless `NLTK_ALLOW_PROXIED_URLOPEN=1` is set. We hit this in our sandbox; Netlify builds normally have direct egress, but if a build log shows "Security Violation [pathsec.urlopen]", this is why. Safest option: **commit the three small data packages to the repo**.
- VADER is English‑only and lexicon‑based: sarcasm and domain terms ("this phone is *sick*") will be misread. Document this as a limitation.

## Sources

- NLTK VADER module: https://www.nltk.org/api/nltk.sentiment.vader.html
- NLTK collocations how‑to: https://www.nltk.org/howto/collocations.html
- NLTK data install: https://www.nltk.org/data.html
- Hutto & Gilbert (2014), VADER, ICWSM: https://github.com/cjhutto/vaderSentiment
- Pyodide package list (nltk 3.9.4): https://pyodide.org/en/stable/usage/packages-in-pyodide.html
