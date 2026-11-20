# Raw Yelp review rows (partial)

**Status: partial fetch.** Only the first page (offset 0, 100 rows) of each split was reachable. The HF datasets-server returned 502/503 for every other offset on 2026-11-20. Re-run the fetch for the missing offsets before using this file for training or evaluation.

## Source

- Dataset: `Yelp/yelp_review_full` (Hugging Face Datasets), config `yelp_review_full`, split `train`.
- Fetched via the Hugging Face datasets-server rows API on 2026-11-20:
  `https://datasets-server.huggingface.co/rows?dataset=Yelp%2Fyelp_review_full&config=yelp_review_full&split=train&offset=OFFSET&length=100`
- Retrieval path: Firecrawl scrape tool (`rawHtml` format), because direct curl to huggingface.co is blocked in this sandbox.

## Offsets

- Planned: offset = k * 21000 for k = 0..29 (0, 21000, ..., 609000), plus 651000 as the 31st entry in the list given; 30 requested pages of 100 rows.
- Succeeded: `0` (100 rows).
- Failed after one retry (upstream HTTP 502 Bad Gateway or 503 Service Unavailable): 21000, 42000, 63000, 84000, 105000, 126000, 147000, 168000, 189000, 210000, 231000, 252000, 273000, 294000, 315000, 336000, 357000, 378000, 399000, 420000, 441000, 462000, 483000, 504000, 525000, 546000, 567000, 588000, 609000, 630000, 651000.

## Contents

- Row count: 200 total (100 train, 100 test), row_idx 0-99 in each split.
- File: `yelp_rows.jsonl`, one JSON object per line: `{"split": "train" | "test", "row_idx": int, "label": int, "text": str}`. Deduplicated on (split, row_idx).
- Label mapping: 0-4 = 1-5 stars.
- Train label counts (100): 0: 24, 1: 19, 2: 13, 3: 18, 4: 26.
- Test label counts (100): 0: 24, 1: 26, 2: 13, 3: 23, 4: 14.

## Pages

Raw JSON response bodies are kept in `pages/offset_0.json` (train) and `pages/test_offset_0.json` (test).

## Terms and citation

- Yelp Dataset terms: academic and non-commercial use only. Check the current Yelp dataset terms before any other use.
- Citation: Zhang, X., Zhao, J., & LeCun, Y. (2015). Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems (NeurIPS).

## Notes

- Not committed to git.
