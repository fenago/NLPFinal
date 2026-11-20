# NLTK Data: download, locations, NLTK_DATA, offline use

Sources:
- https://www.nltk.org/data.html
- https://www.nltk.org/api/nltk.downloader.html (query extraction)
- https://www.nltk.org/api/nltk.data.html (query extraction)
- https://www.nltk.org/news.html (query extraction, release notes)

Fetched: 2026-11-20

## Basics
- NLTK ships corpora, grammars and trained models as separate "data packages"; full list at https://www.nltk.org/nltk_data/.
- Collection ids: `all`, `book` (data for the book), `all-corpora` (corpora only, no grammars/models).

```python
import nltk
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt_tab')        # see caveat below
```
- Command line: `python -m nltk.downloader [-d DATADIR] [-q] [-f] [-k] PACKAGE_IDS` (also `python nltk/downloader.py ...`). Example: `python -m nltk.downloader -d ./nltk_data stopwords vader_lexicon`.
- The docs' flags in the usage line: `-d` data dir, `-q` quiet, `-f` force, `-k` keep (meaning of `-q/-f/-k` inferred from the signature; only `-d` is explained in data.html).
- `nltk.download()` with no argument opens an interactive downloader (GUI if Tkinter exists, otherwise text).

## Programmatic API
- `nltk.downloader.Downloader(server_index_url=None, download_dir=None)`.
- `Downloader.download(info_or_id=None, download_dir=None, quiet=False, force=False, prefix='[nltk_data]', halt_on_error=True, raise_on_error=False, print_error_to=...)`.
- Helpers: `is_installed(info_or_id, download_dir=None)`, `status(...)` (INSTALLED / NOT_INSTALLED / STALE / PARTIAL), `is_stale`, `update()`, `list()`, `info(id)`, `index()`, `url` property, `default_download_dir()`, `download_dir` property, `incr_download`.
- `Downloader.DEFAULT_URL = 'https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml'`: the data index XML. Before any download the downloader fetches this index; you can point a `Downloader` at another index URL.
- Release notes (3.9.2, Oct 2025): "Update download checksums to use SHA256 in built index."

## Where data goes and where NLTK looks
- Default download dir (non-Windows): the first of `/usr/share/nltk_data`, `/usr/local/share/nltk_data`, `/usr/lib/nltk_data`, `/usr/local/lib/nltk_data`, `~/nltk_data` that exists or can be created with write permission. Windows: `PYTHONHOME/lib/nltk`.
- Central install suggestions in data.html: `C:\nltk_data` (Windows), `/usr/local/share/nltk_data` (Mac), `/usr/share/nltk_data` (Unix).
- Search path: `nltk.data.path` is a list of directories checked in order (it contains the locations above plus per-environment ones). You can append your own: `nltk.data.path.append('/app/nltk_data')`.
- `NLTK_DATA` environment variable: set it to your top-level `nltk_data` folder whenever data is not in a default location (required when you use `-d`/`download_dir`).
- Data lives in typed subfolders: `chunkers`, `grammars`, `misc`, `sentiment`, `taggers`, `corpora`, `help`, `models`, `stemmers`, `tokenizers` (e.g. `corpora/stopwords`, `sentiment/vader_lexicon.zip`; `tokenizers/punkt_tab` for Punkt: folder name inferred, unverified).
- `nltk.data.find(resource_name)` searches `nltk.data.path` and raises `LookupError` (with a pointer to the installation instructions) if missing; paths containing a `.zip` component are looked up inside the zip, and zip files in the path are supported.
- `nltk.data.load(resource_url, format='auto', cache=True, ...)` supports `file:`, `https:` and default `nltk:` protocols; formats include pickle, json, yaml, text, raw.

```python
import os, nltk
os.environ['NLTK_DATA'] = '/app/nltk_data'     # set before first lookup; or:
nltk.data.path.insert(0, '/app/nltk_data')
nltk.download('stopwords', download_dir='/app/nltk_data')
nltk.data.find('corpora/stopwords')
```

## Manual / offline installation (data.html)
1. Create `nltk_data` with the subfolders listed above.
2. Download individual zips from https://www.nltk.org/nltk_data/ (raw files at `https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/<category>/<name>.zip`).
3. Unzip into the matching subfolder (Brown example: `corpora/brown.zip` -> `nltk_data/corpora/brown`).
4. Set `NLTK_DATA` to the top-level folder.
- This is the vendoring route: commit or cache only the needed packages (`vader_lexicon`, `stopwords`, `punkt_tab`) in the repo or build cache and point `NLTK_DATA` at it.
- Several modules read zipped data directly, so keeping the `.zip` for `vader_lexicon` is fine; `stopwords` is normally unzipped under `corpora/stopwords` by the downloader ("Unzipping corpora/treebank.zip" in the downloader examples).

## Proxy
- Behind an HTTP proxy: `nltk.set_proxy('http://proxy.example.com:3128', ('USERNAME', 'PASSWORD'))` before `nltk.download()`. If proxy is `None` it tries to detect the system proxy.
- In sandboxed environments with an agent proxy, downloads from `raw.githubusercontent.com` must be allowed (project-specific; not from the docs).

## Security / newer behaviour (as documented)
- Release notes: a release "avoid[s] need for pickled models, resolves security vulnerability CVE-2024-39705" (the pickle-based Punkt/tagger models were replaced with non-pickle formats; version number not captured in the extracted text, unverified).
- Release notes: the 3.9.2 line also changes the index checksums to SHA256.
- `nltk.data.load` still lists `pickle` as a supported format, so never load untrusted data packages.
- No documentation page fetched describes a new proxy-specific behaviour beyond `nltk.set_proxy`. (Nothing further verified.)

## Project application
- Needed packages: `punkt_tab` (sent/word tokenization), `stopwords`, `vader_lexicon`.
- Netlify build: run `python -m nltk.downloader -d $NLTK_DATA punkt_tab stopwords vader_lexicon` in the build command, with `NLTK_DATA` set as a Netlify env var (e.g. `./nltk_data`), or vendor the three packages in the repo for deterministic, network-free builds.
- Always `nltk.download(..., quiet=True)` guarded by `nltk.data.find` so repeated builds are cheap.
- Pyodide needs the same files placed into its virtual FS; see 07-pyodide-notes.md.
