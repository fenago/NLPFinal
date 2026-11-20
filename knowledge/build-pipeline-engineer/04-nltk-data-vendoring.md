# 04 - NLTK data: download, NLTK_DATA, vendoring into the repo

Sources:
- https://www.nltk.org/data.html ("Installing NLTK Data")
- Repo docs: `docs/05-netlify-architecture.md` (commit `nltk_data/`, copy to `site/nltk_data/`)

Fetched: 2026-11-20

## Downloading (official page)

```python
>>> import nltk
>>> nltk.download()          # interactive downloader
```
- Command line: `python -m nltk.downloader <ids>`; `-d <dir>` selects the download directory; collection ids exist such as `all-corpora`.
- Proxy (verbatim from the page):
  ```python
  nltk.set_proxy('http://proxy.example.com:3128', ('USERNAME', 'PASSWORD'))
  nltk.download()
  ```
- Programmatic with target dir (general NLTK API, not spelled out on this page, (unverified)): `nltk.download("vader_lexicon", download_dir="nltk_data")`.

## Where NLTK looks for data

- `NLTK_DATA` environment variable: "Set your `NLTK_DATA` environment variable to point to your top level `nltk_data` folder."
- Default search locations on the page: `C:\nltk_data` (Windows), `/usr/local/share/nltk_data` (Mac), `/usr/share/nltk_data` (Unix) (the page lists these; it also lists home-dir style paths in the full text, see page).
- `nltk.data.path`: the page text does **not** mention `nltk.data.path`; it is the documented Python list of search directories in the NLTK API (https://www.nltk.org/api/nltk.data.html, not fetched; (unverified)). Usage: `nltk.data.path.insert(0, "/abs/path/nltk_data")` or `.append`. Directories are searched in list order.
- Folder layout: a top-level `nltk_data` with subfolders `chunkers, grammars, misc, sentiment, taggers, corpora, help, models, stemmers, tokenizers`.

## Manual installation (documented)

1. Create `nltk_data` and the subfolders above.
2. Download individual packages from https://www.nltk.org/nltk_data/ (the "download" links), e.g. `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/brown.zip`.
3. Unzip to the matching subfolder: "the Brown Corpus ... is to be unzipped to `nltk_data/corpora/brown`."
4. Set `NLTK_DATA`.
Many loaders can also read the `.zip` directly if left zipped next to where the unzipped folder would be (general behaviour; (unverified) for each corpus).

## Packages this project needs and their locations

| Resource | Download id | Typical path |
|---|---|---|
| VADER lexicon | `vader_lexicon` | `nltk_data/sentiment/vader_lexicon.zip` (contains `vader_lexicon/vader_lexicon.txt`) |
| English stopwords | `stopwords` | `nltk_data/corpora/stopwords.zip` -> `stopwords/` |
| Punkt tokenizer (3.9+) | `punkt_tab` | `nltk_data/tokenizers/punkt_tab.zip` -> `punkt_tab/english/...` |

(Paths are standard NLTK layout; confirm with `nltk.data.find("sentiment/vader_lexicon.zip")` after download.) NLTK 3.9+ replaced pickled `punkt` with `punkt_tab`; the repo docs already use `punkt_tab`.

## Vendoring strategy (matches docs/05)

1. One-time locally: `python -m nltk.downloader -d nltk_data vader_lexicon stopwords punkt_tab`.
2. Commit `nltk_data/` (few MB) so Netlify never needs to reach the NLTK download server (network flakiness; docs/05 also notes an NLTK 3.10 proxy-download guard (unverified)).
3. At build: `nltk.data.path.insert(0, str(REPO / "nltk_data"))` (or set `NLTK_DATA` in `[build.environment]`).
4. Copy the same files to `site/nltk_data/` (`shutil.copytree`) so the browser worker can fetch them for Pyodide.
5. Prefer shipping the **zips** to the browser (smaller transfer) and have the Pyodide worker write them to `/nltk_data/...` (see Pyodide notes 04). If the loader can't find zipped data, unpack with `pyodide.unpackArchive`.

## Verification snippet

```python
import nltk
nltk.data.path.insert(0, "nltk_data")
for res in ("sentiment/vader_lexicon.zip", "corpora/stopwords.zip", "tokenizers/punkt_tab/english"):
    print(res, "->", nltk.data.find(res))   # raises LookupError if missing
```

## Project application

- Build script must **fail fast** with a clear message if a resource is missing (`LookupError`), rather than silently calling `nltk.download` (which would hit the network, may hang on Netlify).
- Add a test/CI check that `site/nltk_data/` contains exactly the three resources and that total size is small (target < 10 MB (opinion)).
- Keep a `nltk_data/README.md`-free layout: only data; document the download command in the pipeline README instead.
- Data licences: NLTK data packages carry their own licences; VADER lexicon is MIT-licensed upstream (unverified; check before redistributing).
