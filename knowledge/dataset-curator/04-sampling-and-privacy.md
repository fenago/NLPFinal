# Sampling, JSONL I/O and Privacy

Sources:
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html (pandas 3.1.1 docs)
- https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.core.groupby.DataFrameGroupBy.sample.html (pandas 2.2.3; the same page under /docs/reference/... returned 404 in the 3.1 docs, so the 2.2 version is cited)
- https://pandas.pydata.org/docs/reference/api/pandas.read_json.html (pandas 3.1.1)
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html (pandas 3.1.1)
- Project doc docs/04-dataset.md (sampling and ethics checklist)

Fetched: 2026-11-20

## DataFrame.sample
Signature: `DataFrame.sample(n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False)`
- `n`: number of items; "Cannot be used with frac. Default = 1 if frac = None."
- `frac`: fraction of items; cannot be used with `n`. If `frac > 1`, set `replace=True`.
- `replace`: allow the same row more than once (default False).
- `weights`: column name (axis 0) or array; normalized to sum to 1; missing values count as zero.
- `random_state`: "If int, array-like, or BitGenerator, seed for random number generator... Default None results in sampling with the current state of np.random." **Pass an int for reproducible samples.**
- `ignore_index=True` relabels the result 0..n-1.
- Docs example note: "we use random_state to ensure the reproducibility of the examples", e.g. `df["num_legs"].sample(n=3, random_state=1)`.

## Stratified sampling with groupby
`DataFrameGroupBy.sample(n=None, frac=None, replace=False, weights=None, random_state=None)`
- "Return a random sample of items from each group. You can use random_state for reproducibility."
- `n`: "Number of items to return for each group. Cannot be used with frac and must be no larger than the smallest group unless replace is True."
- Docs examples: `df.groupby("a").sample(n=1, random_state=1)` and `df.groupby("a")["b"].sample(frac=0.5, random_state=2)`.
- Equal-per-star sample (sketch, follows the documented API):
```python
import pandas as pd
df = pd.read_json(path, lines=True)               # or built from a streamed filter
df = df[df["text"].str.len().between(80, 1500)]
per_star = df["rating"].round().astype(int).value_counts().min()   # smallest group
n = min(400, per_star)
sample = (df.assign(star=df["rating"].round().astype(int))
            .groupby("star").sample(n=n, random_state=42)
            .sample(frac=1, random_state=42)       # shuffle, keep reproducible
            .reset_index(drop=True))
```
- Because `n` must not exceed the smallest group (unless `replace=True`), compute the minimum group size first, as above.
- `groupby(...).sample` on a column used as the key keeps that column; drop helper columns before saving.

## read_json (JSON Lines)
- `lines` (bool, default False): "Read the file as a json object per line."
- `chunksize`: returns a `JsonReader` for iteration; "This can only be passed if lines=True. If this is None, the file will be read into memory all at once."
- `nrows`: number of lines to read; "can only be passed if lines=True".
- `compression='infer'` detects `.gz`, `.bz2`, `.zip`, `.xz`, `.zst`, `.tar...` from the extension, so `All_Beauty.jsonl.gz` reads directly.
- `engine`: `"ujson"` (default) or `"pyarrow"` (only with `lines=True`).
- Date inference (default `convert_dates=True`; labels starting with `timestamp` or ending `_time`/`_at` count as datelike) is deprecated since 3.1.0; "Pass `dtype=False` to disable type conversion". For Amazon data pass `dtype=False` (or `convert_dates=False`) so the integer `timestamp` and string ids are not altered.
- Memory: the All_Beauty review file is 327 MB; either stream with `chunksize`:
```python
rows = []
for chunk in pd.read_json(path, lines=True, chunksize=100_000, dtype=False):
    chunk = chunk[chunk["text"].str.len() > 80]
    rows.append(chunk[["rating", "title", "text", "parent_asin", "verified_purchase", "helpful_vote"]])
df = pd.concat(rows, ignore_index=True)
```
  or read line by line with `json.loads` (no pandas needed).

## to_json
- DataFrame `orient`: default `'columns'`; allowed `split`, `records`, `index`, `columns`, `values`, `table`. `'records'` is "list like [{column -> value}, ... ]"; "index labels are not preserved with this encoding".
- `lines` (bool, default False): "If 'orient' is 'records' write out line-delimited json format. Will throw ValueError if incorrect 'orient'".
- `force_ascii` (default True): output is ASCII-escaped; set `force_ascii=False` to keep UTF-8 characters readable and smaller.
- `index`: only used for `split`, `index`, `columns`, `table` orients.
- `mode='a'` (append) is "only supported when lines is True and orient is 'records'".
- `compression='infer'` from the extension.
```python
sample.to_json("data/reviews_sample.jsonl", orient="records", lines=True, force_ascii=False)
```
- Float precision `double_precision=10` default (max 15).

## Privacy and data minimisation
Rationale from the project checklist (docs/04-dataset.md) plus the dataset cards:
- Keep only fields the app needs; the Amazon `user_id` and review `images` are not needed and add personal data. Drop them before committing (docs/04: "Drop `user_id` and images").
- The Yelp Review Full card has no author id but its text contains real business and staff names; the card's personal-information section is "[More Information Needed]". Do not add inference about individuals.
- Use `parent_asin` or a salted sequential id (`r0001`) as the public review id instead of any source user id.
- Do not redistribute the full dataset; the repo holds a small sample only (target under 5 MB), with the cards' citations and terms in the footer (docs/04 item 5).
- Optional light scrub for text: flag emails and phone-number patterns with regex and drop or mask those reviews; log the count. (Practical suggestion, not from the docs.)
- Record the seed (`random_state=42`), source file, commit hash and date so the sample is reproducible.

## Project application
- Target 1,000-3,000 Amazon All_Beauty reviews, equal per star (e.g. 400 per star for 2,000), `random_state=42`; length filter on `text` (docs/04 uses over 80 characters).
- Output `data/reviews_sample.jsonl` with `id`, `rating`, `title`, `text`, `parent_asin`, `verified_purchase`; separate `data/entity_patterns.jsonl` built from `meta_All_Beauty` `store` and `title`.
- Map rating to label for EVAL: 1-2 negative, 3 neutral, 4-5 positive.
- Verify after writing: line count, star counts, file size, no `user_id` key anywhere (`grep -c user_id data/reviews_sample.jsonl` should print 0).
