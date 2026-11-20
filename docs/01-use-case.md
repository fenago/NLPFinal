# 01 — Use Case: Customer Review Analyzer (NLTK + spaCy)

## Problem

Businesses receive more reviews than anyone can read. A manager wants to know, at a glance: *Are customers happy? What exactly do they praise or complain about? Which people, places, brands and products come up?*

## What the app shows

| Feature | Output | Library |
|---|---|---|
| Overall + per‑sentence sentiment | Positive / Neutral / Negative + VADER compound score | NLTK |
| Key words & key phrases | Top words, statistically significant bigrams/trigrams | NLTK (FreqDist, collocations) |
| Aspects | Most‑discussed noun phrases ("battery life", "wait time") | spaCy (noun chunks + lemmas) |
| Aspect sentiment | "battery life → disappointing (−)", "staff → helpful (+)" | spaCy dependency parse + NLTK VADER |
| Mentions | People, Places, Brands, Products | spaCy NER + EntityRuler |
| Evaluation | VADER label vs. star rating — accuracy & confusion matrix | NLTK + dataset stars |

## Two modes

1. **Dataset dashboard** — thousands of real reviews pre‑analysed with the full NLTK + spaCy pipeline at Netlify build time.
2. **Analyze your own review** — paste text; NLTK runs live in the browser via Pyodide.

## Why both libraries (one‑line pitch for the report)

NLTK is a **teaching‑grade toolkit of classic algorithms** (tokenizers, lexicon sentiment, corpus statistics); spaCy is an **industrial pipeline with trained models** (NER, parsing, lemmatization). The analyzer uses each for what it does best and combines them for aspect‑based sentiment — something neither does alone.

See doc 02 (NLTK), 03 (spaCy), 04 (dataset), 05 (Netlify architecture).
