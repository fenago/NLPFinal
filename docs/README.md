# Customer Review Analyzer — Research Docs

Research brief for the NLP final project: a **Customer Review Analyzer** that uses **both NLTK and spaCy** to show sentiment, key phrases, and the people, places, brands and products mentioned in product or restaurant reviews — **deployed on Netlify**.

These docs are the shared context for the agent team that will design and build the app. Researched 2026‑11‑20; library behaviour verified with a local smoke test (NLTK 3.10.4, spaCy 3.8.18, `en_core_web_sm` 3.8.0, Python 3.13).

## Index

| # | Doc | What's inside |
|---|---|---|
| 01 | [Use case](01-use-case.md) | Problem, features, which library powers each feature |
| 02 | [NLTK](02-nltk.md) | Tokenizing, stopwords, VADER sentiment, frequency & collocations — code, verified output, gotchas |
| 03 | [spaCy](03-spacy.md) | Named entities (+EntityRuler), noun chunks, lemmas, dependency‑based aspect↔opinion — code, verified output, gotchas |
| 04 | [Dataset](04-dataset.md) | Amazon Reviews 2023 (primary), Yelp Review Full (restaurant mode), Yelp Open Dataset — fields, size, terms, sampling plan |
| 05 | [Netlify architecture](05-netlify-architecture.md) | What Netlify can/cannot run (build‑time Python, Functions languages, Pyodide), recommended architecture, config sketches, risks |

## Key decisions at a glance

1. **NLTK** = sentiment (VADER, per sentence), tokenization, stopwords (keep negations), frequencies, collocations.
2. **spaCy** = entities (people/places/brands/products), noun‑chunk aspects, lemmas, dependency parsing to link aspects to opinions.
3. **Combined** = aspect‑based sentiment (spaCy finds "battery life ← disappointing", VADER scores it), and spaCy entity masking to stop brand names like "Best Buy" skewing VADER.
4. **Dataset** = committed sample of 1–3k Amazon Reviews 2023 (All_Beauty) reviews, stratified by stars; optional Yelp sample for restaurant mode.
5. **Netlify facts** = Python runs **only at build time**; Functions are **JS/TS/Go only**; Netlify Server is **Node only**; **Pyodide runs NLTK but not spaCy**.
6. **Architecture** = full NLTK + spaCy pipeline at build → static JSON dashboard; live "analyze your review" with NLTK in the browser via Pyodide; live spaCy on new text only via an optional external API proxied through Netlify redirects.

## Open questions for the team / instructor

- Is an off‑Netlify helper API (Tier 2 in doc 05) acceptable, or must 100% of compute be on Netlify (Tier 1)?
- Product mode only, or also a restaurant (Yelp) toggle?
- Which Amazon category? (All_Beauty recommended for size; Cell_Phones for richer product names.)
