# Hugging Face Hub Downloads and datasets Loading

Sources:
- https://huggingface.co/docs/huggingface_hub/guides/download (docs version shown: v2.4.0 / main)
- https://huggingface.co/docs/datasets/loading (docs version shown: v5.2.0)
- https://discuss.huggingface.co/t/dataset-scripts-are-no-longer-supported/163891 (search excerpt only, community thread)
- https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 (card banner about scripts)

Fetched: 2026-11-20

## hf_hub_download
- "The `hf_hub_download()` function is the main function for downloading files from the Hub. It downloads the remote file, caches it on disk (in a version-aware way), and returns its local file path."
- Parameters used in the guide: `repo_id`, `filename`, `repo_type`, `revision`, `cache_dir`, `local_dir`. "By default, the file will be considered as being part of a `model` repo", so **datasets need `repo_type="dataset"`**.
```python
from huggingface_hub import hf_hub_download
# Download from a dataset (guide example)
hf_hub_download(repo_id="google/fleurs", filename="fleurs.py", repo_type="dataset")
# This project
path = hf_hub_download(
    repo_id="McAuley-Lab/Amazon-Reviews-2023",
    filename="raw/review_categories/All_Beauty.jsonl",
    repo_type="dataset",
)
```
- The returned path points into the HF local cache. "it is important to not modify the file to avoid having a corrupted cache". Copy or read it; do not edit in place.
- `revision` accepts a tag, branch, PR (`refs/pr/3`) or a **full-length** commit hash (a 7-character hash does not work). Pin a commit hash for reproducibility.
- `local_dir="path/to/folder"` keeps the repo's relative path (`filename="data/train.csv"` gives `path/to/folder/data/train.csv`) and creates a `.cache/huggingface/` metadata folder that can be deleted afterwards. Add that folder to `.gitignore`.
- Default cache location can be changed with `cache_dir` or the `HF_HOME` environment variable.
- `dry_run=True` on `hf_hub_download` / `snapshot_download` returns file name, size and cached status without downloading. CLI: `hf download <repo> <file> --dry-run`.
- `snapshot_download(repo_id, repo_type="dataset", allow_patterns=..., ignore_patterns=...)` downloads a repo, filtered with fnmatch-style globs. For Amazon Reviews 2023 never download the whole repo (750 GB); name one file.
- CLI forms: `hf download <repo> <file>` or a single URI `hf://datasets/<owner>/<name>[@revision][/path]`, e.g. `hf download hf://datasets/google/fleurs/data/`.
- Faster downloads: `hf_xet` is installed with `huggingface_hub` 0.32.0 and later (`pip install -U huggingface_hub`); `hf_transfer` is deprecated. Amazon files show "xet" on the Hub.
- Offline mode: set `HF_HUB_OFFLINE=1` after the file is cached.

## datasets library: loading files
- `load_dataset()` loads from the Hub, local or remote files. Supported file types in the guide include `csv`, `json`, `txt`, `parquet`, `arrow`.
- Hub repo with data files: `load_dataset("lhoestq/demo1")`; pin with `revision="main"` (tag, branch or commit hash).
- Restrict what is loaded with `data_files=` or `data_dir=`: "If you don't specify which data files to use, `load_dataset()` will return all the data files" (C4 is cited as about 13 TB).
- **JSON**: `load_dataset("json", data_files="my_file.json")`. "the most efficient format is to have multiple JSON objects; each line represents an individual row" (JSON Lines). For nested files pass `field="data"`. Remote: pass URLs in `data_files`.
- **Parquet**: `load_dataset("parquet", data_files={"train": "train.parquet", "test": "test.parquet"})`; remote parquet via `https://` or `hf://datasets/<owner>/<name>/<file>` URLs.
- Remote file schemes: `https://` and `hf://datasets/...` in `data_files`.
- Split slicing: `split="train[:10%]"`, `"train[10:20]"`, `"train+test"`; `streaming=True` avoids full download for supported formats.
- In-memory: `Dataset.from_list(list_of_dicts)`, `Dataset.from_pandas(df)`.
- Yelp example for this project: `load_dataset("Yelp/yelp_review_full")` (auto-converted parquet; no script).

## Dataset scripts and trust_remote_code
- The Amazon Reviews 2023 card's quick start uses `trust_remote_code=True`, and its Dataset Viewer banner reads: "The viewer is disabled because this dataset repo requires arbitrary Python code execution. Please consider removing the loading script ... and relying on automated data support (you can use `convert_to_parquet` from the `datasets` library)."
- The "Load" guide (v5.2.0) documents no script-based loading and no `trust_remote_code` option.
- Community reports (HF forum thread "Dataset scripts are no longer supported", GitHub issues, HF dataset discussions): `datasets` 4.0.0 removed support for custom loading scripts and the `trust_remote_code` parameter; the error is `RuntimeError: Dataset scripts are no longer supported`. Workarounds named there: `pip install "datasets<4.0.0"` (not recommended) or avoid the script and read the raw files. One issue says "datasets >= 4.5.0"; the exact release is therefore not settled by an official page I fetched (unverified). The release notes were not fetched.
- Practical rule: **do not rely on `load_dataset("McAuley-Lab/Amazon-Reviews-2023", ..., trust_remote_code=True)`**. Use `hf_hub_download` on `raw/review_categories/<Category>.jsonl`, then read with `json`/pandas (see 04).

## Project application
- Pin `huggingface_hub` and (if used) `datasets` versions in the curation script's requirements; the Netlify build must not need either, because only the sampled JSONL is committed.
- Curation script outline: `hf_hub_download(..., repo_type="dataset", revision=<commit hash>)` -> stream the file line by line (327 MB) -> filter -> sample -> write `data/reviews_sample.jsonl`.
- Record the commit hash and download date in `data/README.md` or `data/PROVENANCE.md`.

## Minimal curation download script (follows the documented calls)
```python
from huggingface_hub import hf_hub_download
REPO = "McAuley-Lab/Amazon-Reviews-2023"
reviews = hf_hub_download(REPO, "raw/review_categories/All_Beauty.jsonl", repo_type="dataset")
meta    = hf_hub_download(REPO, "raw/meta_categories/meta_All_Beauty.jsonl", repo_type="dataset")
print(reviews, meta)   # paths inside the HF cache; read-only use
```
Expected size on disk: about 327 MB and 213 MB (file sizes shown on the Hub tree). Run once, offline from the Netlify build.
