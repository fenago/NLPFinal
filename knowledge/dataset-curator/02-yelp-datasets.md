# Yelp Datasets (Yelp Review Full and Yelp Open Dataset)

Sources:
- https://huggingface.co/datasets/Yelp/yelp_review_full (fetched in full)
- https://business.yelp.com/data/resources/open-dataset/ (page could not be scraped directly; only a search-result excerpt was retrieved, so details below are partly unverified)
- https://arxiv.org/abs/1509.01626 (linked from the HF card, not fetched)

Fetched: 2026-11-20

## A. Yelp Review Full (Hugging Face)
- Card title: "Dataset Card for YelpReviewFull". "The Yelp reviews dataset consists of reviews from Yelp. It is extracted from the Yelp Dataset Challenge 2015 data."
- Task: `text-classification` / `sentiment-classification`. Languages: "mainly written in english".
- Size: **650,000 train + 50,000 test = 700k rows**; 323 MB total file size; viewer shows one subset `yelp_review_full`, splits `train` (650k) and `test` (50k).
- Construction: "randomly taking 130,000 training samples and 10,000 testing samples for each review star from 1 to 5." So classes are perfectly balanced.
- Fields:
  - `label`: class label with 5 classes. Card text: "Corresponds to the score associated with the review (between 1 and 5)." In the dataset viewer each row shows the integer label followed by its class name (rows such as "4" + "5 stars", "0" + "1 star"), so the integer labels are 0-4 and the class names are "1 star" to "5 stars". The card's own test example has `'label': 0` for a one-star-style complaint. Add 1 to get stars; verify with `ds["train"].features["label"].names`.
  - `text`: review text. Newlines appear as the two characters backslash-n in the stored text (card: "New lines are escaped by a backslash followed with an 'n' character"); quotes may be escaped. Normalize with `text.replace("\\n", " ")` before NLP. Texts range from 1 to about 5.64k characters.
- No business metadata: no business name, city, user id or date.
- Loads as parquet with no script: the viewer notes "Auto-converted to Parquet" (branch `refs/convert/parquet`). `load_dataset("Yelp/yelp_review_full")` works with `datasets` (see 03).
- Card sections "Personal and Sensitive Information", "Discussion of Biases" and "Other Known Limitations" are all "[More Information Needed]". Reviews mention real business and staff names (the preview shows examples naming doctors and restaurants).
- Homepage link: https://www.yelp.com/dataset; repository https://github.com/zhangxiangxiao/Crepe; paper https://arxiv.org/abs/1509.01626; point of contact Xiang Zhang.
- Licensing section: "You can check the official yelp-dataset-agreement" (PDF linked from the card: https://s3-media3.fl.yelpcdn.com/assets/srv0/engineering_pages/bea5c1e92bf3/assets/vendor/yelp-dataset-agreement.pdf; PDF not fetched, so terms not verified).
- Citation (card): Xiang Zhang, Junbo Zhao, Yann LeCun. Character-level Convolutional Networks for Text Classification. Advances in Neural Information Processing Systems 28 (NIPS 2015).

## B. Yelp Open Dataset (official)
From the search excerpt of the official page (page text not fully scraped):
- "The Yelp Open Dataset is a subset of Yelp data that is intended for educational use. It provides real-world data related to businesses including reviews, photos, check-ins, and attributes like hours, parking availability, and ambience."
- Counts on the page: **6,990,280 reviews**, **150,346 businesses**.
- Download: JSON version is "1 compressed TAR file (4.35 GB). Uncompressed it contains 1 PDF and 5 JSON files (8.65 GB). Documentation is included." A second (photos) download is one compressed TAR of 7.45 GB.
- The five JSON files are not named in the excerpt. From general knowledge of this dataset they are business, review, user, tip and checkin JSON files, one object per line (unverified here; confirm against the included documentation PDF).
- Access: a download form and agreement on the official page (details unverified).
- Unverified: exact field list (typically `review_id`, `user_id`, `business_id`, `stars`, `date`, `text`, `useful`, `funny`, `cool` for reviews; `name`, `city`, `state`, `categories` for businesses).
- The page directs commercial users to licensed data products ("For educational purposes, please use our Open Dataset" appears on the Data Licensing form). Treat the Open Dataset as educational / non-commercial only.

## Comparison for this project
| | Yelp Review Full | Yelp Open Dataset |
|---|---|---|
| Rows | 700k | about 7.0M reviews |
| Access | HF parquet, no agreement click-through | Form and agreement, 4.35 GB tar |
| Business names/cities | no | yes (business JSON) |
| Stars | label 0-4 | stars 1-5 (unverified) |

## Project application
- Restaurant mode (optional): take about 1,000 rows from `Yelp/yelp_review_full` `train`, stratified by `label` (200 per star).
- Convert `label + 1` to `rating`; keep `text` only; do not keep anything else. Clean `\n` escapes.
- Note in the data README: "mixed businesses (doctors, auto shops, restaurants), not only restaurants"; the card gives no category field, so restaurant filtering is not possible. Say so in the report rather than claiming restaurant-only data.
- Credit Zhang et al. 2015 and link the Yelp dataset agreement in the footer; do not redistribute more than the small sample.
- Avoid the Open Dataset in the Netlify build; it is multi-GB and behind an agreement.

## Quick check commands (run once, record the output in the data README)
```python
from datasets import load_dataset
ds = load_dataset("Yelp/yelp_review_full")          # parquet, no script
print(ds)                                             # train 650,000 / test 50,000
print(ds["train"].features["label"].names)            # confirm the 5 class names
print(ds["train"][0])
```
(The snippet follows the `load_dataset` usage in the Hugging Face "Load" guide; the printed values are what the card says to expect, not output captured in this session.)
