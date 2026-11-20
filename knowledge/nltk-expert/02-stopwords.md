# NLTK Stopwords Corpus

Sources:
- https://www.nltk.org/book/ch02.html (query extraction of the stopwords passage)
- https://www.nltk.org/howto/corpus.html (query extraction; stopword snippet only)
- https://www.nltk.org/data.html

Fetched: 2026-11-20

## Usage
```python
from nltk.corpus import stopwords
stopwords.words('english')
```
- The NLTK book shows the English list as a plain Python list of lowercase strings, beginning `'i', 'me', 'my', 'myself', 'we', 'our', ...` and ending `... 'don', 'should', 'now'`.
- The list includes negation-bearing words: `no`, `nor`, `not`, plus `but`, `very`, `only`, `too`, `don`, `can`, `just`. (Verified by reading the printed list in the book; note the book's printed list is the older, shorter edition and does not show contractions such as `don't`. Newer NLTK versions ship more entries; the project docs measured 198 words in 3.10.4.)
- The corpus howto lists available languages through `stopwords.fileids()` and shows `stopwords.words('portuguese')`. Output seen: `['arabic', 'azerbaijani', 'bengali', 'danish', 'dutch', 'english', 'finnish', 'french', ...]` (list truncated in the extraction; the full language list was not verified).
- Data package id used by the downloader: `stopwords` (corpus; installs under `nltk_data/corpora/stopwords`). Package id inferred from the downloader conventions in data.html (`corpora` subfolder); the exact id string `stopwords` is standard NLTK usage but not spelled out on the fetched pages (unverified).

## Content-fraction idiom (from the book, ch02)
```python
def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)
# content_fraction(nltk.corpus.reuters.words()) -> 0.7364374824583169
```
Performance note (general Python, not from the docs): `words()` returns a list; wrap in `set(...)` once for O(1) membership instead of calling it per token.

## Customizing
```python
from nltk.corpus import stopwords
sw = set(stopwords.words('english'))
sw -= {'no', 'nor', 'not', 'but', 'very', 'too', "don't", "isn't"}   # keep sentiment-bearing words
sw |= {'product', 'item', 'order', 'would', 'get'}                   # domain noise
tokens = [t for t in tokens if t.lower() not in sw]
```
- Always compare against lowercase tokens (`w.lower()`), as the book idiom does.
- The corpus is plain text; `nltk.corpus.stopwords.words(lang)` returns a fresh list each call.
- Tokenization mismatch to watch: `word_tokenize("don't")` gives `['do', "n't"]`, so list entries like `don't` never match and `n't` is not in the default list. Filter `n't` explicitly or tokenize with a regex that keeps apostrophes (see 01-tokenizers.md).

## Project application
- Never remove stopwords before VADER; it needs negations, intensifiers and `but` (03-vader.md).
- For the keyword and collocation views, subtract negations from the stoplist and add review-domain noise words, then apply the stoplist as an `apply_word_filter` on collocation finders (05-collocations.md uses exactly this pattern: `apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)`).
- The stopwords corpus must be downloaded at build time and, for live analysis in the browser, shipped or fetched into Pyodide's `nltk_data` (06-data-downloads.md, 07-pyodide-notes.md). A cheap alternative for the browser: export the final stopword set as a JSON/Python literal at build time and avoid the corpus lookup entirely.
