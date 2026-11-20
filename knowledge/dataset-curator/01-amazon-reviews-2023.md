# Amazon Reviews 2023 (McAuley Lab)

Sources:
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
- https://amazon-reviews-2023.github.io/
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/review_categories
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/meta_categories

Fetched: 2026-11-20

## Overview
- Collected in 2023 by McAuley Lab (UCSD). Contains user reviews, item metadata and links (user-item, bought-together graphs).
- 571.54M reviews, 54.51M users, 48.19M items, 33 domains; interactions May 1996 to Sep 2023; "30.14B" review tokens.
- Total repo size on the Hub: 750 GB. Do not clone the repo; download single files.
- Card links: paper https://arxiv.org/abs/2403.03952; GitHub https://github.com/hyp1231/AmazonReviews2023; bug reports via GitHub issues.
- April 7, 2024 additions: `all_categories.txt` (34 lines = 33 categories + "Unknown") and `asin2category.json` (maps `parent_asin` to category).

## Categories (33 + Unknown) and sizes for the small ones
Category names match file names. Counts are #Rating (reviews) from the site table:
- Small: Magazine_Subscriptions 71.5K, Subscription_Boxes 16.2K, Gift_Cards 152.4K, Digital_Music 130.4K, Health_and_Personal_Care 494.1K, Handmade_Products 664.2K, **All_Beauty 701.5K**.
- Medium: Appliances 2.1M, Amazon_Fashion 2.5M, Musical_Instruments 3.0M, Software 4.9M, Video_Games 4.6M, CDs_and_Vinyl 4.8M, Industrial_and_Scientific 5.2M, Baby_Products 6.0M.
- Large: Cell_Phones_and_Accessories 20.8M, Electronics 43.9M, Books 29.5M, Home_and_Kitchen 67.4M, Clothing_Shoes_and_Jewelry 66.0M, Unknown 63.8M.
- Others: Arts_Crafts_and_Sewing, Automotive, Beauty_and_Personal_Care, Grocery_and_Gourmet_Food, Health_and_Household, Kindle_Store, Movies_and_TV, Office_Products, Patio_Lawn_and_Garden, Pet_Supplies, Sports_and_Outdoors, Tools_and_Home_Improvement, Toys_and_Games.

## File paths
- On the Hugging Face dataset repo (verified in the file tree):
  - Reviews: `raw/review_categories/<Category>.jsonl` (e.g. `All_Beauty.jsonl`, 327 MB; `Cell_Phones_and_Accessories.jsonl`, 9.34 GB; `Magazine_Subscriptions.jsonl`, 33.3 MB; `Subscription_Boxes.jsonl`, 8.95 MB; `Gift_Cards.jsonl`, 50.2 MB; `Digital_Music.jsonl`, 78.8 MB).
  - Metadata: `raw/meta_categories/meta_<Category>.jsonl` (e.g. `meta_All_Beauty.jsonl`, 213 MB; `meta_Magazine_Subscriptions.jsonl`, 4.1 MB).
  - All stored as plain `.jsonl` (xet storage), one JSON object per line.
- On the project site (gzip, alternative mirror): `https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/<Category>.jsonl.gz` and `.../raw/meta_categories/meta_<Category>.jsonl.gz`. The HF card links the same files under `https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/...` (two different hosts appear in the two pages).
- "Pure ID" (ratings-only) files and standard splits are described under "Common Data Processing" at https://amazon-reviews-2023.github.io/data_processing/index.html (not fetched).

## Review fields (HF card / project site table)
| Field | Type | Notes |
|---|---|---|
| `rating` | float | 1.0 to 5.0 |
| `title` | str | review title |
| `text` | str | review body |
| `images` | list | user-posted images (small/medium/large URLs) |
| `asin` | str | product id |
| `parent_asin` | str | parent id; "Please use parent ID to find product meta" |
| `user_id` | str | ID of the reviewer |
| `timestamp` | int | unix time; sample shows milliseconds (e.g. 1588687728923) |
| `verified_purchase` | bool | |
| `helpful_vote` | int | helpful votes |
- Discrepancy (verified): the project-site sample record shows `sort_timestamp` and `helpful_votes`, while the field table and the HF card sample show `timestamp` and `helpful_vote`. Code defensively with `r.get("helpful_vote", r.get("helpful_votes"))` and inspect the first line of the downloaded file.

## Item metadata fields
`main_category`, `title`, `average_rating`, `rating_number`, `features` (list), `description` (list), `price` (float; may be the string `'None'` in the HF sample), `images`, `videos`, `store` (store/brand name), `categories` (hierarchical list; may be empty), `details` (dict or JSON string with Brand, Manufacturer, etc.), `parent_asin`, `bought_together`. The HF card sample also shows `subtitle` and `author`.
- Join reviews to metadata on `parent_asin`.
- Example (HF card): `store: 'Howard Products'`, `title: 'Howard LC0008 Leather Conditioner, 8-Ounce (4-Pack)'`.

## Loading note
- The card's quick start uses `load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_review_All_Beauty", trust_remote_code=True)`. The HF Dataset Viewer on the card is disabled with the message that the repo "requires arbitrary Python code execution" and suggests removing the loading script. See 03-huggingface-hub-download.md: download the raw JSONL file instead.
- The project site's own quick start just opens the downloaded file and parses each line with `json.loads`.

## Citation (from the card and the site)
```bibtex
@article{hou2024bridging,
  title={Bridging Language and Items for Retrieval and Recommendation},
  author={Hou, Yupeng and Li, Jiacheng and He, Zhankui and Yan, An and Chen, Xiusi and McAuley, Julian},
  journal={arXiv preprint arXiv:2403.03952},
  year={2024}
}
```

## Terms
- Neither the dataset card nor the project site fetched here states a license or terms of use (not stated). Treat as research use, cite the paper, and record "no license stated on card, accessed 2026-11-20" in the data README.

## Project application
- Primary choice: `All_Beauty` reviews (327 MB file, 701.5K reviews) plus `meta_All_Beauty` (213 MB) for `store`/`title` to seed EntityRuler patterns. Alternative with more model-number products: `Cell_Phones_and_Accessories` (9.34 GB, avoid at build time).
- Download once offline; commit only the sampled JSONL (target under 5 MB).
- Keep: `rating`, `title`, `text`, `parent_asin`, `verified_purchase`, `helpful_vote`. Drop `user_id`, `images`, `asin`-level user data, timestamps unless needed.
- Footer/report credit: cite Hou et al. 2024 and name the category.
