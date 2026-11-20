# NLTK Collocations (key phrases)

Sources:
- https://www.nltk.org/howto/collocations.html
- https://www.nltk.org/api/nltk.collocations.html (query extraction)
- https://www.nltk.org/api/nltk.metrics.association.html (query extraction)
- https://www.nltk.org/book/ch01.html (query extraction, `text.collocations()` example)

Fetched: 2026-11-20

## Concept
Collocations are multi-word expressions that commonly co-occur. Score candidate n-grams with an association measure, filter, then take the best.

## Setup (from the howto)
```python
import nltk
from nltk.collocations import *
bigram_measures  = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
fourgram_measures = nltk.collocations.QuadgramAssocMeasures()
```

## Finders
- `BigramCollocationFinder.from_words(words, window_size=2)`; `window_size > 2` counts non-contiguous bigrams (Church and Hanks style); scores are scaled by 1/(window_size - 1).
- `TrigramCollocationFinder.from_words(words, window_size=3)`.
- `QuadgramCollocationFinder.from_words(tokens)` also exists.
- Manual construction from frequency distributions: `BigramCollocationFinder(word_fd, bigram_fd)` with `word_fd = nltk.FreqDist(tokens)` and `bigram_fd = nltk.FreqDist(nltk.bigrams(tokens))`.
- Attributes: `finder.ngram_fd` (FreqDist of n-grams), `finder.word_fd`.
- `from_documents(...)` exists on the class family (unverified signature; not shown in fetched extracts).

## Scoring and selection
- `finder.nbest(measure, n)` -> top n n-grams by that measure.
- `finder.score_ngrams(measure)` -> list of `(ngram, score)` sorted best first.
- `finder.above_score(measure, min_score)` -> n-grams scoring at least min_score.
- `finder.score_ngram(score_fn, w1, w2)` scores a single bigram (trigram version takes `w1, w2, w3`).

## Filtering candidates
```python
finder.apply_freq_filter(3)                       # drop n-grams seen fewer than 3 times
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)   # drop any n-gram containing a bad word
finder.apply_ngram_filter(lambda w1, w2, w3: 'and' in (w1, w3))                # filter on the whole n-gram
```
- Howto warning: raw PMI favors rare, highly-collocated but infrequent items, so ignore bigrams occurring fewer than three times; the top-PMI list changes from rare proper-name pairs to sensible phrases (`'gray','hairs'`, `'burnt','offering'`) after `apply_freq_filter(3)`.
- Filters mutate the finder in place.

## Association measures (BigramAssocMeasures; also on NgramAssocMeasures)
| method | description |
|---|---|
| `raw_freq` | frequency of the n-gram |
| `pmi` | pointwise mutual information (Manning and Schutze 5.4) |
| `likelihood_ratio` | likelihood ratios (M&S 5.3.4; Dunning 1993) |
| `chi_sq` | chi-square (phi-sq times number of bigrams; M&S 5.3.3) |
| `student_t` | Student's t (M&S 5.3.1) |
| `phi_sq`, `dice`, `jaccard`, `poisson_stirling`, `mi_like` | other measures |
| `fisher` | Fisher's exact test; needs scipy; less sensitive to small counts but costly |
- Marginal-argument convention for bigram measures: `(n_ii, (n_ix, n_xi), n_xx)`; e.g. `bigram_measures.pmi(20, (42, 20), 14307668)` -> 18.38 (howto example).
- Use `nltk.metrics.ContingencyMeasures(bigram_measures)` if you have contingency-table cells instead.
- Compare two rankings with `nltk.metrics.spearman` (`ranks_from_sequence`, `ranks_from_scores`, `spearman_correlation`).

## Worked examples
```python
text = "I do not like green eggs and ham, I do not like them Sam I am!"
tokens = nltk.wordpunct_tokenize(text)
finder = BigramCollocationFinder.from_words(tokens)
finder.nbest(bigram_measures.raw_freq, 3)

# spanning intervening words + stopwords filter + likelihood ratio (howto example)
finder = BigramCollocationFinder.from_words(corpus_words, window_size=20)
finder.apply_freq_filter(2)
ignored = nltk.corpus.stopwords.words('english')
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored)
finder.nbest(bigram_measures.likelihood_ratio, 10)
```
- Book shortcut: `text4.collocations()` prints top bigram collocations of an `nltk.Text` (output like `United States; fellow citizens; four years ...`).
- Keyword analysis trick: use `likelihood_ratio(romance[w], (freq[w], romance.N()), freq.N())` per word to rank terms that characterize a subcorpus (e.g. 1-star reviews vs all reviews).

## Project application
- Key phrases per product: lowercase alphabetic tokens (no stopword removal beyond the word filter), `BigramCollocationFinder` and `TrigramCollocationFinder`, `apply_freq_filter(3..5)` scaled to the sample size, stopword/short-word `apply_word_filter`, rank with `likelihood_ratio` (stable on small counts) or `pmi` after the freq filter; export `nbest(...)` or `score_ngrams(...)[:k]` as JSON.
- Run separately on positive and negative review groups to show "what people praise vs complain about" (e.g. "battery life", "customer service").
- Use the keyword-analysis recipe to rank words distinctive to negative reviews.
- Cost is small enough for the browser, but the dashboard data comes from build time; live "analyze your review" is usually too short for collocations to be meaningful.
