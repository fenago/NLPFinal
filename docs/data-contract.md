# Data contract: `site/data/*.json`

Owner: `build-pipeline-engineer` (writes). Approver: `orchestrator`. Consumers: `frontend-engineer`, `dataviz-specialist`, `pyodide-engineer`.

- **Contract version:** `1.0.0` (semantic versioning; a breaking change bumps the major and needs orchestrator approval).
- **Schemas:** `schemas/<file>.schema.json` (JSON Schema 2020-12). `tests/test_schema.py` validates every generated file.
- Every file is a JSON object with a top-level `"contract_version"` string.
- Numbers: sentiment scores and means are rounded to **3 decimal places**. Output is deterministic (sorted keys in stable order, no timestamps), so unchanged data re-uploads nothing on Netlify.
- Sentiment label rule (VADER, Hutto & Gilbert 2014): `compound >= 0.05` → `positive`; `compound <= -0.05` → `negative`; otherwise `neutral`.
- Star → expected label (used for "VADER vs stars"): 1-2 stars → `negative`, 3 → `neutral`, 4-5 → `positive`.
- Entity groups (spaCy label → app group): `PERSON` → `people`; `GPE`, `LOC`, `FAC` → `places`; `ORG` → `brands`; `PRODUCT` → `products`. Other labels are kept in per-review output with `group: null` and are not in leaderboards.

Sign-off (gate 1, 2026-11-20): BUILD, NLTK, SPACY, PYO, UI, VIZ (roles executed by the orchestrator in this run, see `docs/plan.md`), approved by ORC.

## Shared object: `NltkAnalysis`

Returned by `nlp.nltk_analyzer.analyze(text)`. The **same shape** is the `nltk` field of each review in `reviews.json` / `examples.json` and the live Pyodide result in the browser.

```json
{
  "n_chars": 182,
  "n_sentences": 3,
  "n_tokens": 41,
  "sentiment": {"compound": 0.771, "pos": 0.254, "neu": 0.701, "neg": 0.045, "label": "positive"},
  "sentences": [
    {"index": 0, "text": "The pizza was great.", "compound": 0.625, "pos": 0.506, "neu": 0.494, "neg": 0.0, "label": "positive"}
  ],
  "top_words": [{"word": "pizza", "count": 2}],
  "key_phrases": [{"phrase": "not good", "count": 1}]
}
```

- `sentiment` is VADER over the whole raw text (no stopword removal before VADER).
- `top_words`: up to 10 lowercased alphabetic content words (length ≥ 2): English stopwords, review filler words and negations removed; ties broken alphabetically.
- `key_phrases`: up to 10 bigrams of words that are adjacent inside one sentence, where neither word is a stopword or filler word; negations are allowed, so "not good" survives. Ranked by count, ties alphabetical.

## Files

| File | Purpose | Main fields |
|---|---|---|
| `meta.json` | Versions and provenance | `contract_version`, `dataset{name, source, mode, n_reviews, license_note, citation}`, `versions{python, nltk, spacy, en_core_web_sm}`, `sentiment_thresholds`, `entity_groups`, `commit` (Netlify `COMMIT_REF` or `null`) |
| `summary.json` | Dashboard headline numbers | `n_reviews`, `stars_counts{"1".."5"}`, `sentiment_counts{negative,neutral,positive}`, `mean_compound_by_stars{"1".."5"}`, `vader_vs_stars{stars[5], labels[3], counts[5][3]}`, `compound_histogram{bin_edges[11], counts[10]}`, `accuracy_vs_stars` |
| `reviews.json` | Per-review drill-down | `reviews[]`: `id`, `stars`, `text`, `nltk` (`NltkAnalysis`), `spacy{entities[], aspects[], masked_sentiment}` |
| `collocations.json` | Corpus key phrases (NLTK) | `top_words[{word,count}]`, `bigrams[{phrase, count, score}]`, `measure` ("likelihood_ratio"), `min_freq` |
| `aspects.json` | Aspect sentiment (spaCy + NLTK VADER) | `aspects[{aspect, mentions, mean_compound, positive, neutral, negative, top_opinions[{word,count}], review_ids[]}]` |
| `entities.json` | Leaderboards (spaCy) | `groups{people[], places[], brands[], products[]}` each `{text, count, n_reviews, review_ids[], sources{ner, ruler}}` |
| `examples.json` | Curated full-spaCy demos | `examples[{id, title, is_demo, stars, text, nltk, spacy{entities[], aspects[], masked_sentiment, noun_chunks[], tokens[]}}]` |

### `spacy.entities[]`
`{"text": "Starbucks", "label": "ORG", "group": "brands", "start": 10, "end": 19, "source": "ruler" | "ner"}` (character offsets into `text`).

### `spacy.aspects[]`
`{"aspect": "battery life", "opinion": "short", "negated": false, "rule": "amod" | "acomp", "compound": -0.0, "label": "neutral", "sentence_index": 0}`. `compound` is VADER on the opinion phrase (the opinion word, prefixed with "not" when negated).

### `spacy.masked_sentiment`
VADER on the review text with every entity span replaced by a neutral placeholder: `{"compound", "pos", "neu", "neg", "label"}`.

### `examples[].spacy.tokens[]` (examples only)
`{"i", "text", "lemma", "pos", "dep", "head"}`.

`is_demo: true` marks hand-written demo reviews (not from the dataset); `stars` is `null` for them.

## Change log

| Version | Date | Change | Approved |
|---|---|---|---|
| 1.0.0 | 2026-11-20 | Initial contract | orchestrator |
