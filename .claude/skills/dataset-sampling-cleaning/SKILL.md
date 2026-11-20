---
name: dataset-sampling-cleaning
description: "Create the committed review sample: stratified by star rating, cleaned, de-identified JSONL. Use when building or refreshing data/reviews_sample.jsonl."
user-invocable: false
metadata:
  skill-id: S20
  owner: dataset-curator
  shared-with: [nlp-evaluator]
---

# Dataset Sampling Cleaning (S20)

**Owner:** `dataset-curator` · **Shared with:** `nlp-evaluator`

- Target 1,000–3,000 reviews, equal per star (1–5), fixed `random_state=42`.
- Keep fields: `id`, `rating`, `title`, `text`, `parent_asin`/`business`, `verified_purchase`, `helpful_vote`, `source`.
- Drop: `user_id`, images, URLs, emails/phone numbers in text (regex scrub).
- Drop reviews < 80 chars or non-English.
- Output `data/reviews_sample.jsonl` (< 5 MB) + `data/SOURCES.md`.
- Reference: knowledge/dataset-curator/04-sampling-and-privacy.md.
