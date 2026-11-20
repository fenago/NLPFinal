# NLTK Expert Knowledge Index

Sources: all files below cite their own URLs (nltk.org API/howto/book/data/news pages, github.com/cjhutto/vaderSentiment, pyodide.org packages page).

Fetched: 2026-11-20

## Read me first
- Notes are paraphrased from the official docs and tagged "(unverified)" wherever a detail could not be confirmed from a fetched page. Trust untagged statements; double-check tagged ones against the installed NLTK before relying on them.
- Start with 06 (data downloads): most runtime failures (`LookupError` for punkt_tab, stopwords, vader_lexicon) are data problems.
- Then 03 (VADER) for sentiment behaviour and the do-not-preprocess rule, and 07 (Pyodide) for what runs in the browser.
- Version note: build-time NLTK (project docs: 3.10.4) differs from Pyodide's NLTK (3.9.4 on Pyodide 314.0.8). Test both.
- Page extraction used query-style fetches for some long pages, so details outside the quoted passages were not checked.

## Files
| file | summary |
|---|---|
| 01-tokenizers.md | `sent_tokenize`, `word_tokenize`, Punkt classes, `TweetTokenizer`, `RegexpTokenizer` signatures, options and examples. |
| 02-stopwords.md | `nltk.corpus.stopwords.words('english')`, the book's content-fraction idiom, how to customize (keep negations, add domain words). |
| 03-vader.md | `SentimentIntensityAnalyzer.polarity_scores`, output fields, 0.05 thresholds, rule constants (negation, boosters, caps, punctuation), limitations. |
| 04-freqdist.md | `FreqDist` and `ConditionalFreqDist` APIs: `most_common`, `N`, `B`, `freq`, `hapaxes`, `plot`, `tabulate`. |
| 05-collocations.md | Bigram/Trigram finders, association measures (`pmi`, `likelihood_ratio`, `chi_sq`), filters, `nbest`, `score_ngrams`. |
| 06-data-downloads.md | `nltk.download`, the downloader CLI, `NLTK_DATA`, `nltk.data.path`, index URL, manual/offline install, proxy, security notes. |
| 07-pyodide-notes.md | Pyodide 314.0.8 ships NLTK 3.9.4; how to load it and get data files into the virtual filesystem. |

## Quick reference
```python
import nltk
from nltk.tokenize import sent_tokenize, TweetTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder, BigramAssocMeasures
# data: punkt_tab, stopwords, vader_lexicon
```

## Failed fetches
- None failed. Several long pages (probability, downloader, data, collocations API, corpus howto, ch01, ch02, news, Pyodide packages) were read through query extraction rather than full markdown.
