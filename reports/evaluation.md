# Evaluation: Customer Review Analyzer

Owner: `nlp-evaluator`. Reviewers: `nltk-expert`, `spacy-expert`, `technical-writer`. Date: 2026-11-20.

Reproduce: `python scripts/evaluate.py` (metrics as JSON). Hand judgements: `reports/annotations/`. Baseline before fixes: `reports/annotations/baseline_metrics.json`.

## Headline numbers

| What | Result |
|---|---|
| VADER label vs star rating, 3 classes (197 reviews) | accuracy **60.9%**, macro-F1 **0.430** |
| VADER, binary (1–2 vs 4–5 stars, 172 reviews) | accuracy **69.8%** |
| VADER with entity names masked | identical labels (0 of 197 changed) |
| Entity precision, hand-checked (30 reviews, 68 entities) | **64.7%** with EntityRuler, 62.7% without |
| Entity pooled recall (same 30 reviews) | **97.8%** with EntityRuler, 93.3% without |
| Aspect–opinion pair precision (30 judged pairs) | **83%** after the fix below (43% before) |
| Aspect polarity correct, among correct pairs | **80%** after the fix (46% before) |

The sample is small (197 reviews, 30 judged reviews, 30 judged pairs), so treat each number as ±10 points or more.

## 1. VADER vs star rating

Setup: VADER compound on the raw review text (`nlp/nltk_analyzer.py`), labels with the standard thresholds (≥ 0.05 positive, ≤ −0.05 negative). Gold labels from stars: 1–2 negative, 3 neutral, 4–5 positive.

Confusion matrix (rows = gold from stars, columns = VADER):

| Gold \ VADER | negative | neutral | positive | n |
|---|---|---|---|---|
| negative (1–2★) | **43** | 1 | 48 | 92 |
| neutral (3★) | 2 | **0** | 23 | 25 |
| positive (4–5★) | 3 | 0 | **77** | 80 |

| Class | Precision | Recall | F1 |
|---|---|---|---|
| negative | 0.896 | 0.467 | 0.614 |
| neutral | 0.000 | 0.000 | 0.000 |
| positive | 0.520 | 0.963 | 0.675 |
| **macro** | | | **0.430** |

- VADER is strongly biased to "positive" on these long reviews: 148 of 197 reviews (75%) are scored positive, but only 41% have 4–5 stars. When VADER says "negative" it is right 90% of the time, but it finds fewer than half of the negative reviews.
- VADER almost never outputs "neutral" for multi-sentence text: the compound score saturates towards ±1 as the review gets longer.
- Mean compound by stars rises monotonically (1★ −0.21, 2★ +0.33, 3★ +0.79, 4★ +0.76, 5★ +0.89; `site/data/summary.json`). So the score still ranks reviews sensibly; it is the fixed 0.05 threshold that fails.
- Threshold sweep for the positive cut-off (negative stays at −0.05): 0.05 → macro-F1 0.430; 0.5 → 0.456; 0.7 → 0.476 (accuracy 58.9%). A higher threshold helps macro-F1 a little, but it is tuned on the same 197 reviews. **Decision:** keep the standard 0.05 threshold in the product and report this as a limitation rather than overfit.

### Raw vs entity-masked VADER

Masking the people/places/brands/products spans (`spacy.masked_sentiment`) changed **0** review labels. Business names in this sample rarely contain sentiment words. The masking matters for product-style text such as the "Best Buy" demo, where "Best" alone pushes VADER positive (unit test `test_masked_sentiment_removes_name_polarity`). It is kept because it costs nothing and protects that case.

## 2. Entities (spaCy NER, with and without EntityRuler)

Setup: 30 reviews drawn with seed 13. Every people/places/brands/products entity produced by either configuration was judged once in context: 70 candidate spans, 45 correct (`reports/annotations/entities.jsonl`, each with a note). Correct means a real named entity in the assigned group with acceptable boundaries. Named venues and businesses count for either brands or places.

| Configuration | Entities | Correct | Precision | Pooled recall |
|---|---|---|---|---|
| `en_core_web_sm` + EntityRuler (shipped) | 68 | 44 | **64.7%** | **97.8%** |
| `en_core_web_sm` only | 67 | 42 | 62.7% | 93.3% |

By group (with EntityRuler): places 80% (16/20), brands 68% (19/28), people 45% (9/20). The 30 sampled reviews contain no products. "Pooled recall" is recall against the union of correct spans found by either configuration, not true recall.

- The EntityRuler fixes the cases it covers: "Bar Louie" was tagged PERSON without it and ORG with it, and "Carnegie Museum of Art" got a clean span. The gain is small because only names that appear in the sample are in the ruler.
- **People is the weakest group.** The small model tags dish names as PERSON ("Fish Sandwich", "Reuben", "Mussels Diavolo"), plus neighbourhoods ("Squirrel Hill", "'Burgh"), demonyms ("Pittsburgher") and interjections ("Yuck").
- Wrong group: "Lester" and "Tonya" (people) tagged GPE; "Allentown" (a neighbourhood) tagged ORG.
- Boundary error: "Dr. Goldberg 2 stars" gives the span "Goldberg 2".

## 3. Aspect–opinion pairs (spaCy dependency rules + NLTK VADER)

Setup: 30 pairs drawn with seed 13 from all pairs of the 197 reviews, **before** the fix, and judged by hand (`reports/annotations/aspect_pairs.jsonl`). A pair is correct when the aspect is a real feature of the experience and the adjective is an opinion about it. Polarity is checked against a human label.

| Version | Pairs | Pair precision | Polarity correct (on correct pairs) | Correct and right polarity |
|---|---|---|---|---|
| Before fix | 30 | 43% (13/30); `amod` 7/24, `acomp` 6/6 | 46% (6/13) | 20% |
| After fix (same 30 judged pairs, re-scored) | 12 retained | **83% (10/12)** | **80% (8/10)** | 67% |

The fix removed 18 pairs, of which 3 were correct ("real Pittsburgh place", "old veggies", "small selection"). The shipped build has 721 pairs over 197 reviews. The "after" row re-scores the pre-fix sample, so a fresh sample should confirm it.

Fixes fed back to the experts (both applied and covered by tests):

1. **spacy-expert:** `amod` pairs now require an evaluative adjective, one with a VADER valence (`_is_opinion` in `nlp/spacy_analyzer.py`). Before the fix, 17 of 24 `amod` pairs were classifier or quantifier adjectives: "french fries", "iced tea", "hot sauce", "same day", "few minutes", "nineteenth century". `acomp` pairs were already 6/6 correct.
2. **nltk-expert:** a 25-word review-domain extension to the VADER lexicon (`DOMAIN_LEXICON` in `nlp/nltk_analyzer.py`), for words VADER does not know: bland, stale, soggy, tasteless, mediocre, overpriced, tasty, flavorful, attentive and others. Context-dependent words (cold, slow, cheap, small, dry) are deliberately excluded. This lifted review accuracy from 60.4% to 60.9% (macro-F1 0.426 to 0.430), and it applies identically in the browser.

## 4. Error analysis

| Pattern | Example (review id) | Library | Why it fails |
|---|---|---|---|
| Long mixed reviews saturate positive | yelp-train-031 (2★, compound +0.99): praise for past visits, then complaints | NLTK VADER | Compound sums over all sentences; many mildly positive words outweigh a few strong complaints. Sentence-level scores in the drill-down show the shift. |
| Polite negative reviews | yelp-train-044 (2★, +0.99): "I really wanted to like this place… the food was decent" | NLTK VADER | Hedged, courteous wording; disappointment is implied, not stated. |
| "Okay" reviews with no neutral output | yelp-test-078 (2★, +0.99): "Its okay, but it was just ok" | NLTK VADER | "okay" is positive in the lexicon; nothing in VADER maps faint praise to neutral. |
| Negation window flips domain words | "I can't believe how bland the pasta was." → positive (golden test) | NLTK VADER | VADER negates a word within 3 tokens after "can't", so "bland" flips to positive. |
| Food words missing from the lexicon | "The veggies were old and wilted" (before the fix) | NLTK VADER | Domain vocabulary is absent; partly fixed by `DOMAIN_LEXICON`. |
| Dishes as people | "Reuben", "Fish Sandwich", "Mussels Diavolo" → PERSON | spaCy NER | The small model generalises from capitalisation; menu items are capitalised. |
| Local places as people | "Squirrel Hill", "'Burgh" → PERSON | spaCy NER | Pittsburgh neighbourhoods are rare in the model's training data. |
| Hyphenated opinion split | "dungeon-like dining room" → opinion "like" | spaCy tokenizer + `amod` rule | The infix hyphen splits the adjective; now filtered by the valence check. |

## 5. Recommendations (not done; cost/benefit for the next iteration)

- **spaCy:** add a PERSON → product guard for capitalised dish names (for example a menu-word list), and place patterns for Pittsburgh neighbourhoods. Do not add names from the judged 30 reviews, because that would leak the evaluation sample into the ruler.
- **NLTK:** show both the review-level label and the share of negative sentences in the UI; the share separates 2★ from 4★ reviews better than the compound score on long text (not measured here).
- **Data:** with the full 650k-row Yelp set reachable, judge a fresh, larger sample (≥ 100 entities, ≥ 100 pairs) to tighten these estimates.
