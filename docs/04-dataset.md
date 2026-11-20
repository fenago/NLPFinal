# 04 — Free, Public Review Datasets

> **Recommendation:** use a **curated sample of 1,000–3,000 reviews from Amazon Reviews 2023 (product mode)** plus, optionally, **~1,000 from Yelp Review Full (restaurant mode)**. Commit the sample as JSONL in the repo so the Netlify build never depends on a multi‑GB download.

---

## Option A (primary) — Amazon Reviews 2023 (McAuley Lab, UCSD)

| | |
|---|---|
| Where | https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 · project site https://amazon-reviews-2023.github.io/ |
| Size | 571.54 M reviews, 33 categories |
| Review fields | `rating` (1–5), `title`, `text`, `images`, `asin`, `parent_asin`, `user_id`, `timestamp`, `verified_purchase`, `helpful_vote` |
| Item metadata | Separate `raw_meta_<Category>` files: product `title`, `store` (brand), `categories`, `price`, … |
| Small categories | Magazine_Subscriptions 71.5K · Gift_Cards 152.4K · **All_Beauty 701.5K** |
| License | Not stated on the dataset card — released by a university lab for research; cite the paper, use for academic/non‑commercial purposes. |
| Cite | Hou, Li, He, Yan, Chen, McAuley. *Bridging Language and Items for Retrieval and Recommendation.* arXiv:2403.03952 (2024). |

**Why it fits:** product reviews mention **brands and products** constantly, and the `store`/`title` metadata gives us a ready‑made **brand/product list for spaCy's EntityRuler** and a ground truth for checking NER. Star ratings give ground truth for VADER.

Suggested category: **All_Beauty** (manageable size, brand‑heavy) or Cell_Phones_and_Accessories (more product model numbers; larger file).

**Loading note:** the card's example uses `load_dataset(..., trust_remote_code=True)`, which relies on a loading script — recent `datasets` releases (4.x) dropped script support. Download the raw JSONL file directly instead:

```python
from huggingface_hub import hf_hub_download
import json, random
p = hf_hub_download("McAuley-Lab/Amazon-Reviews-2023",
                    "raw/review_categories/All_Beauty.jsonl", repo_type="dataset")
rows = [json.loads(l) for l in open(p)]
random.seed(42)
sample = random.sample([r for r in rows if len(r["text"]) > 80], 2000)
```

(Confirm the exact file path in the repo's *Files* tab before scripting.)

## Option B (restaurant mode) — Yelp Review Full

| | |
|---|---|
| Where | https://huggingface.co/datasets/Yelp/yelp_review_full |
| Size | 650,000 train / 50,000 test |
| Fields | `label` (star class; HF encodes 0–4 = 1–5 stars), `text` |
| Source | Yelp Dataset Challenge 2015, via Zhang, Zhao & LeCun, *Character‑level Convolutional Networks for Text Classification*, NeurIPS 2015 |
| Terms | Governed by the Yelp Dataset terms of use (academic / non‑commercial). |

Pros: tiny to load (`load_dataset("Yelp/yelp_review_full")` — parquet, no script), restaurant language (dishes, staff names, wait times). Cons: **no business metadata** — no restaurant name/city fields to validate entities.

## Option C (richest, heavier) — Yelp Open Dataset (official)

https://business.yelp.com/data/resources/open-dataset/ — ~7M reviews (counts vary by release) **plus `business.json` with name, city, state, categories**. Requires accepting Yelp's dataset agreement; multi‑GB tar download; academic/non‑commercial only. Best if the team wants to validate PERSON/GPE/ORG extraction against real business names and cities. Not recommended for the build pipeline due to size — pre‑sample offline.

## Comparison

| | Amazon 2023 | Yelp Review Full | Yelp Open Dataset |
|---|---|---|---|
| Domain | Products | Restaurants/businesses | Restaurants/businesses |
| Brand/product metadata | ✅ | ❌ | ✅ (business names) |
| Star ratings | ✅ 1–5 | ✅ 1–5 | ✅ 1–5 |
| Ease of download | Medium (per‑category JSONL) | Easy (HF parquet) | Hard (agreement, GBs) |
| Use in project | **Primary** | Secondary / restaurant toggle | Optional enrichment |

## Sampling & ethics checklist (for the build team)

1. Sample offline once, commit `data/reviews_sample.jsonl` (target < 5 MB).
2. Stratify by star rating (equal 1–5) so sentiment evaluation is balanced.
3. Drop `user_id` and images — not needed, reduces personal data.
4. Keep `rating` for VADER evaluation (1–2 neg / 3 neutral / 4–5 pos).
5. Put dataset citations + terms in the app footer and the final report.

## Sources

- Amazon Reviews 2023 dataset card: https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
- Hou et al. 2024, arXiv:2403.03952: https://arxiv.org/abs/2403.03952
- Yelp Review Full card: https://huggingface.co/datasets/Yelp/yelp_review_full
- Yelp Open Dataset: https://business.yelp.com/data/resources/open-dataset/
