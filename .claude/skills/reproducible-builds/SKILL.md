---
name: reproducible-builds
description: "Make the Netlify Python build deterministic and pinned. Use when editing requirements.txt, netlify.toml build settings or the build script."
user-invocable: false
metadata:
  skill-id: S24
  owner: build-pipeline-engineer
  shared-with: [netlify-engineer, spacy-expert]
---

# Reproducible Builds (S24)

**Owner:** `build-pipeline-engineer` · **Shared with:** `netlify-engineer`, `spacy-expert`

- `requirements.txt` at repo root with exact pins (`nltk==3.10.4`, `spacy==3.8.18`, model wheel URL).
- `PYTHON_VERSION = "3.12"` in netlify.toml.
- Vendored `nltk_data/`; no runtime downloads except pinned wheels.
- Same input → byte-identical `site/data/*.json` (sorted keys, fixed seeds). QA checks by building twice.
- Local parity: `python pipeline/build.py && python -m http.server -d site`.
