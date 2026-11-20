# Data sources, terms and curation method

Owner: `dataset-curator`. Reviewers: `spacy-expert`, `nlp-evaluator`.

## Dataset in use: Yelp Review Full ("restaurant/business mode")

- **Dataset:** `Yelp/yelp_review_full` on Hugging Face (https://huggingface.co/datasets/Yelp/yelp_review_full), extracted from the Yelp Dataset Challenge 2015 data. 650,000 train and 50,000 test reviews, balanced by star rating. Fields: `label` (0-4 = 1-5 stars) and `text`. No business name, city, user ID or date.
- **Rows we have:** 200 real reviews, `train` rows 0-99 and `test` rows 0-99, fetched through the Hugging Face datasets-server rows API on 2026-11-20 (provenance and failed offsets: `data/raw/README.md`). Other offsets returned HTTP 502/503 during the fetch.
- **Mixed businesses:** the reviews cover restaurants, bars, shops, auto repair, salons, museums and doctors. The dataset has no category field, so restaurant-only filtering is not possible.

### Why not Amazon Reviews 2023

The project docs (`docs/04-dataset.md`) name Amazon Reviews 2023 (McAuley Lab) as the primary dataset. It is **not reachable from the build sandbox**: Hugging Face file downloads are blocked and the Hugging Face dataset viewer does not support that dataset. The app therefore runs in Yelp "restaurant/business mode": brands and products come from names written in the review text, not from product metadata. Swapping in an Amazon sample later only needs a new `data/reviews_sample.jsonl` with the same fields and a rebuilt `data/entity_patterns.jsonl`.

## Terms of use

- Yelp data is for **academic and non-commercial use** under the Yelp Dataset Agreement (linked from the dataset card: https://s3-media3.fl.yelpcdn.com/assets/srv0/engineering_pages/bea5c1e92bf3/assets/vendor/yelp-dataset-agreement.pdf). The PDF was not fetched in this sandbox; check its current wording before any other use.
- This repository redistributes only a 197-review sample for a course project and credits the source in the app footer and README.

## Citation

> Xiang Zhang, Junbo Zhao, Yann LeCun. 2015. Character-level Convolutional Networks for Text Classification. *Advances in Neural Information Processing Systems 28 (NIPS 2015)*. https://arxiv.org/abs/1509.01626

## Files

| File | Made by | Contents |
|---|---|---|
| `data/raw/yelp_rows.jsonl` | fetch (see `data/raw/README.md`) | 200 raw rows: `split`, `row_idx`, `label`, `text` |
| `data/reviews_sample.jsonl` | `python scripts/curate_sample.py` | 197 cleaned reviews: `id`, `stars`, `text`, `source{dataset, split, row_idx}` |
| `data/entity_patterns.jsonl` | `python scripts/build_entity_patterns.py` | 58 EntityRuler patterns (57 names + 1 model-number regex) |
| `data/demo_reviews.jsonl` | `build-pipeline-engineer` (hand-written) | Demo reviews for `examples.json`, labelled `is_demo` |

## Curation method (`scripts/curate_sample.py`)

1. **Unescape:** the stored text keeps newlines as the two characters `\n` and quotes as `\"`. Both are converted back (`\n` → newline, `\"` → `"`).
2. **Scrub personal data:** e-mail addresses → `[EMAIL]`, phone numbers → `[PHONE]`, URLs and bare domains → `[URL]`. Result on this sample: 0 e-mails, 0 phones, 1 URL (`restaurant.com`). The dataset has no user IDs. Reviews still contain first names of staff and businesses as written by reviewers; these are part of the public dataset and are what the "people" leaderboard shows.
3. **Drop unusable rows:** texts under 20 characters (3 rows: "Tasty", "Good fish sandwich.", "Hoofah.") and exact duplicates (none).
4. **Keep, do not down-sample:** 197 of 200 rows are kept. Balancing to the smallest class (3 stars, 25 reviews) would leave 125 reviews, below the 150 floor set by the orchestrator, so the sample keeps the natural distribution of the fetched rows and the evaluation reports macro-averaged metrics to compensate.
5. **Order:** by stars, then split, then row index (deterministic). IDs are `yelp-<split>-<row_idx>`, for example `yelp-test-000`.

Star distribution of `data/reviews_sample.jsonl`:

| Stars | 1 | 2 | 3 | 4 | 5 | Total |
|---|---|---|---|---|---|---|
| Reviews | 48 | 44 | 25 | 41 | 39 | 197 |

## EntityRuler pattern method (`scripts/build_entity_patterns.py`)

Yelp Review Full has no business or product metadata, so patterns are **derived from names actually present in the sample text**:

1. Ran `en_core_web_sm` over the sample and listed every `ORG`, `PRODUCT` and `FAC` span with its count.
2. Scanned the text for a list of common US chains and consumer brands (restaurants, grocers, retailers, beverages, cars).
3. Read each candidate in context and kept only real businesses, brands and named products. Rejected false positives such as "Apple" (only inside "Applebee's"), "Chick" (inside "Chicken"), shouted words tagged `ORG` by the model ("AWESOME", "UNACCEPTABLE"), and food words ("mayo", "fig").
4. Labels: businesses and brands → `ORG` (app group `brands`); named products, menu items, drinks and apps → `PRODUCT` (app group `products`), e.g. "Big Mac", "Coors Light", "Fruit Ninja".
5. The script writes only variants that occur in the sample (case-insensitive) and logs the skipped ones.
6. One token pattern catches model-number style tokens (`^[A-Z]{1,4}-?\d{2,5}(?:[A-Z]{1,3}\d{0,2})?$`, e.g. `XR-500`, `QC35`, `WH-1000XM5`) as `PRODUCT`. It matters for product reviews such as the hand-written demo; Yelp text has few.

Patterns are phrase patterns matched on the lowercase form (`phrase_matcher_attr = "LOWER"` in `nlp/spacy_analyzer.py`). The ruler runs before `ner` so its spans win.

Known gaps: only names seen in these 197 reviews are covered; new chains in other reviews fall back to the statistical NER. The evaluation (`reports/evaluation.md`) measures entity precision with and without the ruler.
