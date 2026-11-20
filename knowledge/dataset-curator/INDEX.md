# Dataset Curator Knowledge Index

Fetched: 2026-11-20. Notes from dataset cards, project pages and library docs. Items marked "(unverified)" were not confirmed from a fetched page (mainly the Yelp Open Dataset terms and field list).

| File | Use it when | Sources |
|---|---|---|
| 01-amazon-reviews-2023.md | Picking a category, exact file paths and sizes, field names, BibTeX | huggingface.co card; amazon-reviews-2023.github.io |
| 02-yelp-datasets.md | Restaurant mode data: Yelp Review Full fields and sizes; Open Dataset facts | huggingface.co/datasets/Yelp/yelp_review_full; business.yelp.com open dataset page (partial) |
| 03-huggingface-hub-download.md | Downloading one raw file with `hf_hub_download(repo_type="dataset")`; `load_dataset` for parquet/json; script removal | huggingface.co/docs/huggingface_hub, /docs/datasets |
| 04-sampling-and-privacy.md | Stratified reproducible sampling, JSONL read/write, dropping personal data | pandas docs; docs/04-dataset.md |

Quick facts
- Amazon reviews path on HF: `raw/review_categories/All_Beauty.jsonl` (327 MB); metadata `raw/meta_categories/meta_All_Beauty.jsonl` (213 MB). Repo total 750 GB: download single files only.
- Amazon fields: `rating, title, text, images, asin, parent_asin, user_id, timestamp, verified_purchase, helpful_vote`. Join metadata on `parent_asin`. The project site sample shows `sort_timestamp`/`helpful_votes`: code defensively.
- No license is stated on the Amazon card; cite Hou et al. 2024 (arXiv:2403.03952).
- Yelp Review Full: 650k train / 50k test, fields `label` (0-4) and `text`, no business metadata; points to the Yelp dataset agreement.
- Scripts and `trust_remote_code` are reported as removed in `datasets` 4.x: download raw files instead.
- Sampling: `df.groupby("star").sample(n=n, random_state=42)`; write `to_json(orient="records", lines=True, force_ascii=False)`.

Project docs: docs/04-dataset.md, docs/expert-roster.md (DATA agent, skills S19-S20).
