# NLTK Tokenizers: sent_tokenize, word_tokenize, Punkt, TweetTokenizer, RegexpTokenizer

Sources:
- https://www.nltk.org/api/nltk.tokenize.html
- https://www.nltk.org/api/nltk.tokenize.casual.html
- https://www.nltk.org/api/nltk.tokenize.regexp.html
- https://www.nltk.org/api/nltk.tokenize.punkt.html (partial, via query extraction)

Fetched: 2026-11-20

## Overview
- Tokenizers divide strings into lists of substrings. Import from `nltk.tokenize`.
- Optional "span" methods (`span_tokenize`) return `(start, end)` offsets with string-slice semantics; implemented as generators.
- Caution from the docs: tokenize real `str` (decoded Unicode), not encoded bytes.

## sent_tokenize
Signature: `nltk.tokenize.sent_tokenize(text, language='english')`
- Returns a list of sentences using NLTK's recommended sentence tokenizer, currently `PunktSentenceTokenizer` for the given language.
- `language` = "the model name in the Punkt corpus".

```python
from nltk.tokenize import sent_tokenize, word_tokenize
s = '''Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\n\nThanks.'''
sent_tokenize(s)
# ['Good muffins cost $3.88\nin New York.', 'Please buy me\ntwo of them.', 'Thanks.']
[word_tokenize(t) for t in sent_tokenize(s)]
```

## word_tokenize
Signature: `nltk.tokenize.word_tokenize(text, language='english', preserve_line=False)`
- Uses an improved `TreebankWordTokenizer` plus `PunktSentenceTokenizer` for the language.
- `preserve_line=True` skips sentence splitting first (treat the text as one line).
- Docs state this tokenizer "requires the Punkt sentence tokenization models to be installed".
- Example output: `['Good','muffins','cost','$','3.88','in','New','York','.',...]` (currency symbol split off, `3.88` kept whole).

## Punkt classes (punkt.html)
- `PunktSentenceTokenizer.tokenize(text: str, realign_boundaries: bool = True) -> List[str]`.
- Also `span_tokenize(text, realign_boundaries=True)` -> iterator of `(int, int)`, `text_contains_sentbreak(text) -> bool`, `train(...)`.
- `PunktTokenizer(lang='english')` with `load_lang(lang='english')` and `save_params()`; this is the class that loads per-language parameters.
- `load_punkt_params(lang_dir)` and `save_punkt_params(params, dir='/tmp/punkt_tab')` exist; the default save directory name `punkt_tab` is the only appearance of "punkt_tab" in the fetched API page.
- (unverified from fetched pages) That the downloadable data package is named `punkt_tab` and replaces the older pickled `punkt` package. The release notes page (https://www.nltk.org/news.html) says only that a release "avoid[s] need for pickled models, resolves security vulnerability CVE-2024-39705" without naming the version in the extracted text. The project doc `docs/02-nltk.md` states `punkt_tab` is required for NLTK >= 3.8.2; treat that as project-internal, not confirmed here.
- Practical implication: if `sent_tokenize`/`word_tokenize` raises `LookupError`, the Punkt data is missing; see 06-data-downloads.md.

## TweetTokenizer (nltk.tokenize.casual)
Signature: `TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False, match_phone_numbers=True)`
- Twitter-aware; core logic is `WORD_RE.findall(s)` inside `tokenize(text) -> List[str]`.
- `preserve_case=False` lowercases everything except emoticons.
- `reduce_len=True` collapses runs of 3+ identical characters to exactly 3.
- `strip_handles=True` removes `@username` handles.
- Needs no downloaded data (regex based; no Punkt dependency stated).
- Helpers: `casual_tokenize(text, preserve_case=True, reduce_len=False, strip_handles=False, match_phone_numbers=True)`, `reduce_lengthening(text)`, `remove_handles(text)`.

```python
from nltk.tokenize import TweetTokenizer
TweetTokenizer().tokenize("This is a cooool #dummysmiley: :-) :-P <3")
# ['This','is','a','cooool','#dummysmiley',':',':-)',':-P','<3']
TweetTokenizer(strip_handles=True, reduce_len=True).tokenize('@remy: This is waaaaayyyy too much for you!!!!!!')
# [':','This','is','waaayyy','too','much','for','you','!','!','!']
```

## RegexpTokenizer (nltk.tokenize.regexp)
Signature: `RegexpTokenizer(pattern, gaps=False, discard_empty=True, flags=re.UNICODE|re.MULTILINE|re.DOTALL)`
- Pattern must not contain capturing groups; use `(?:...)`.
- `gaps=False`: pattern matches the tokens. `gaps=True`: pattern matches the separators.
- Function forms: `regexp_tokenize(text, pattern, gaps=False, discard_empty=True, flags=...)` (note text first, pattern second, unlike `re`), `wordpunct_tokenize(text)`, `blankline_tokenize(text)`.
- `WordPunctTokenizer` uses `\w+|[^\w\s]+` (splits `$3.88` into `$`, `3`, `.`, `88`).
- `WhitespaceTokenizer` splits on whitespace; docs say prefer `str.split()`.

```python
from nltk.tokenize import RegexpTokenizer
RegexpTokenizer(r'\w+|\$[\d\.]+|\S+').tokenize("Good muffins cost $3.88")
# ['Good','muffins','cost','$3.88']
RegexpTokenizer(r"[A-Za-z']+").tokenize("don't love it!")   # word-only, keeps apostrophes
```

## Other tokenizers worth knowing (names seen in the package index)
`ToktokTokenizer`, `MWETokenizer` (`add_mwe`), `TreebankWordTokenizer`, `NLTKWordTokenizer`, `LineTokenizer`, `SpaceTokenizer`.

## Project application
- Per-sentence VADER: `sent_tokenize(review)` then `polarity_scores` on each sentence. Requires Punkt data both at build time and in Pyodide.
- Keyword/frequency views: `RegexpTokenizer(r"[A-Za-z']+")` avoids Punkt entirely and is cheaper in the browser; `word_tokenize` splits `don't` into `do`, `n't`, which interacts with stopword lists (see 02-stopwords.md).
- Informal reviews (emoticons, `soooo good`, handles): `TweetTokenizer(reduce_len=True)`. Do not lowercase or strip text before feeding VADER (see 03-vader.md).
