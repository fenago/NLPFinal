---
name: nltk-data-packaging
description: "Package NLTK data (punkt_tab, stopwords, vader_lexicon) so the build and the browser never download it at runtime. Use when setting up nltk_data/, NLTK_DATA, or loading lexicons into Pyodide."
user-invocable: false
metadata:
  skill-id: S11
  owner: nltk-expert
  shared-with: [build-pipeline-engineer, pyodide-engineer, netlify-engineer]
---

# NLTK Data Packaging (S11)

**Owner:** `nltk-expert` · **Shared with:** `build-pipeline-engineer`, `pyodide-engineer`, `netlify-engineer`

- Commit `nltk_data/` with exactly: `tokenizers/punkt_tab`, `corpora/stopwords`, `sentiment/vader_lexicon`.
- Build: `NLTK_DATA` env var (netlify.toml) points at the repo's `nltk_data/`.
- Build copies the same files to `site/nltk_data/`; the Pyodide worker fetches them and writes them into its virtual FS, then `nltk.data.path.insert(0, "/nltk_data")`.
- NLTK 3.10 refuses `nltk.download()` through an HTTP proxy unless `NLTK_ALLOW_PROXIED_URLOPEN=1` — another reason to vendor.
- Verify with `nltk.data.find("sentiment/vader_lexicon.zip")` (or unzipped path).
- Reference: knowledge/nltk-expert/06-data-downloads.md.
