# NLTK FreqDist and ConditionalFreqDist

Sources:
- https://www.nltk.org/api/nltk.probability.FreqDist.html
- https://www.nltk.org/api/nltk.probability.html (ConditionalFreqDist section, query extraction)
- https://www.nltk.org/book/ch01.html (query extraction of FreqDist table and examples)

Fetched: 2026-11-20

## FreqDist
- `nltk.probability.FreqDist` subclasses `collections.Counter`; also importable as `nltk.FreqDist`.
- Construction: `FreqDist(samples=None)`; `FreqDist()` is empty. Equivalent forms:

```python
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
fdist = FreqDist()
for w in word_tokenize("This is an example sentence"):
    fdist[w.lower()] += 1
fdist = FreqDist(w.lower() for w in word_tokenize("This is an example sentence"))
```

### Methods (from the API page)
| call | meaning |
|---|---|
| `N()` | total number of outcomes recorded (sum of counts) |
| `B()` | number of distinct samples ("bins") with count > 0; equals `len(fdist)` |
| `freq(sample)` | count / N, a float in [0, 1] |
| `fdist[sample]` | raw count (Counter indexing) |
| `most_common(n=None)` | list of `(sample, count)` pairs, most common first; `None` = all |
| `max()` | sample with the greatest count (ties: undefined which; `None` if empty) |
| `hapaxes()` | list of samples occurring exactly once |
| `Nr(r, bins=None)` / `r_Nr(bins=None)` | number of samples with frequency r; dict r -> Nr |
| `plot(*args, title='', cumulative=False, percents=False, show=True, **kwargs)` | plot most frequent first; an integer arg limits samples; needs Matplotlib; `show=False` returns the axes |
| `tabulate(*args, **kwargs)` | print table; takes `samples` list and `cumulative` flag |
| `copy()`, `pprint(maxlen=10, stream=None)`, `pformat(maxlen=10)` | utilities |
| `update`, `setdefault` | overridden to invalidate the cached N |
| inherited Counter: `elements()`, `subtract()`, `items()`, `keys()`, `values()`, `get()` | standard |

### Book examples (ch01, Moby Dick)
```python
fdist1 = FreqDist(text1)            # <FreqDist with 19317 samples and 260819 outcomes>
fdist1.most_common(50)              # [(',', 18713), ('the', 13721), ...]
fdist1['whale']                     # 906
fdist1.plot(50, cumulative=True)
fdist1.hapaxes()
```
The book table of FreqDist functions: `fdist[x]`, `fdist.freq(x)`, `fdist.N()`, `fdist.most_common(n)`, iteration over samples, `fdist.max()`, `fdist.tabulate()`, `fdist.plot()`, `fdist.plot(cumulative=True)`.

## ConditionalFreqDist
- `nltk.probability.ConditionalFreqDist` subclasses `defaultdict`: a mapping condition -> `FreqDist`.
- Constructor: `ConditionalFreqDist(cond_samples=None)`, where `cond_samples` is a sequence of `(condition, sample)` pairs.
- Accessing an unseen condition creates an empty `FreqDist` for it.

```python
from nltk.probability import ConditionalFreqDist
cfd = ConditionalFreqDist()
for word in tokens:
    cfd[len(word)][word] += 1
# equivalent
cfd = ConditionalFreqDist((len(w), w) for w in tokens)
cfd[3]['dog']          # count
cfd[3].freq('the')     # relative freq within condition 3
```
- Methods: `N()` (total outcomes across conditions), `conditions()` (list of accessed conditions), `plot(*args, samples=None, title='', cumulative=False, percents=False, conditions=None, show=False, **kwargs)`, `tabulate(*args, **kwargs)` (params `samples`, `conditions`, `cumulative`), `copy()`, `deepcopy()`.
- Release notes mention "add mathematical operators to ConditionalFreqDist" (3.2) and a later performance optimization; operator details were not fetched (unverified).
- `ConditionalProbDist(cfdist, probdist_factory, *factory_args)` builds probabilities from a CFD (not needed for this app).

## Idiom: tokens per rating bucket
```python
cfd = ConditionalFreqDist((label, tok) for label, toks in reviews for tok in toks)
cfd['neg'].most_common(20)
cfd.tabulate(conditions=['neg','pos'], samples=['broke','love','refund'])
```

## Project application
- Top words per product/star-bucket: build one `FreqDist` per product or a `ConditionalFreqDist` keyed by sentiment label, then export `most_common(n)` as JSON for the static dashboard. Plain `Counter` JSON export is trivial: `dict(fdist.most_common(50))` or a list of pairs.
- `hapaxes()` and `B()/N()` give a vocabulary-richness stat for the report.
- Skip `plot()` in production: Matplotlib is not needed in the browser; render charts from JSON instead (07-pyodide-notes.md: avoid loading Matplotlib).
- Compute frequencies after stopword removal and lowercasing, but keep a separate unfiltered token stream for VADER.
