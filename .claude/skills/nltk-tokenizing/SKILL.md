---
name: nltk-tokenizing
description: "Split review text into sentences and words with NLTK. Use when writing or calling tokenization code in the build pipeline or in Pyodide."
user-invocable: false
metadata:
  skill-id: S07
  owner: nltk-expert
  shared-with: [pyodide-engineer, build-pipeline-engineer]
---

# NLTK Tokenizing (S07)

**Owner:** `nltk-expert` · **Shared with:** `pyodide-engineer`, `build-pipeline-engineer`

- `nltk.sent_tokenize(text)` → sentences (needs data package `punkt_tab`).
- `nltk.word_tokenize(text)` → Treebank-style tokens (also uses `punkt_tab`).
- `nltk.tokenize.TweetTokenizer(preserve_case=False)` for informal text with emoticons/hashtags.
- Lowercase only for counting, never before VADER (caps carry sentiment).
- Keep tokens for counting with `t.isalpha()`; keep negations.
- Same function must run unchanged at build time and in Pyodide — no file or network access inside it.
- Reference: knowledge/nltk-expert/01-tokenizers.md.
