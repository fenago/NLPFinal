# VADER Sentiment in NLTK

Sources:
- https://www.nltk.org/api/nltk.sentiment.vader.html
- https://github.com/cjhutto/vaderSentiment (README: scoring, thresholds, examples, paper citation)

Fetched: 2026-11-20

## Citation / what it is
- Hutto, C.J. & Gilbert, E.E. (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." ICWSM-14, Ann Arbor, MI. NLTK's docs ask users to cite it.
- VADER = Valence Aware Dictionary and sEntiment Reasoner: lexicon + rule based, "specifically attuned to sentiments expressed in social media", MIT licensed. No training needed.
- Lexicon: tab-delimited `vader_lexicon.txt` (token, mean valence, SD, raw ratings; the algorithm uses only the first two). About 7,500 features after filtering (rated by 10 humans, scale -4..+4, SD < 2.5). Examples from the README: okay 0.9, good 1.9, great 3.1, horrible -2.5, `:(` -2.2, sucks/sux -1.5. Includes emoticons, acronyms (lol, wtf) and slang (nah, meh).

## NLTK API
```python
import nltk
nltk.download('vader_lexicon')            # data package id (used in lexicon_file path below)
from nltk.sentiment import SentimentIntensityAnalyzer      # also: nltk.sentiment.vader.SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
sia.polarity_scores("The book was good.")
# {'neg': 0.0, 'neu': 0.508, 'pos': 0.492, 'compound': 0.4404}
```
- `SentimentIntensityAnalyzer.__init__(lexicon_file='sentiment/vader_lexicon.zip/vader_lexicon/vader_lexicon.txt')` loads the lexicon from NLTK data, so `vader_lexicon` must be installed.
- `polarity_scores(text)` returns a dict with keys `neg`, `neu`, `pos`, `compound`.
- Other methods: `make_lex_dict()`, `score_valence(sentiments, text)`, `sentiment_valence(valence, sentitext, item, i, sentiments)`.
- `sia.lexicon` (attribute built by `make_lex_dict`) is a dict you can extend, e.g. `sia.lexicon.update({'battery-hog': -2.0})` (attribute name `lexicon` is from general use, not shown on the fetched API page: unverified).
- Docs note: hashtags are not considered (`#BAD` is neutral); strip the `#` first.

## Output fields (README "About the Scoring")
- `compound`: sum of lexicon valences adjusted by the rules, then normalized to [-1, +1]. The most useful single measure.
- `pos`, `neu`, `neg`: proportions of the text in each class; sum to about 1.
- Important: pos/neu/neg are the raw per-token categorization and do NOT include rule effects (word order, degree modifiers, caps, punctuation, negation flips, "but").
- Normalization in code: `VaderConstants.normalize(score, alpha=15)` squashes the raw sum to [-1,1].

## Standard thresholds (README)
| label | rule |
|---|---|
| positive | compound >= 0.05 |
| neutral | -0.05 < compound < 0.05 |
| negative | compound <= -0.05 |

## Rules implemented (evidence from NLTK constants + README)
- Negation: `VaderConstants.NEGATE` is a set of words/contractions (`not`, `never`, `no`-like items such as `nothing`, `neither`, `nor`, `without`, `n't` forms like `don't`, `isn't`, plus `rarely`, `seldom`, `despite`). `N_SCALAR = -0.74` flips and dampens valence. `negated(input_words, include_nt=True)` also detects `n't`.
- Degree modifiers: `BOOSTER_DICT` (`very`, `extremely`, `incredibly`, `absolutely`, ... = +0.293; `slightly`, `kind of`, `barely`, `somewhat`, `hardly`, `less` ... = -0.293). `B_INCR = 0.293`, `B_DECR = -0.293`. README: "extremely good" raises intensity by about 0.293 on the 1..4 scale; "marginally good" lowers it.
- ALL-CAPS emphasis: `C_INCR = 0.733`; applied when some but not all words are caps (`SentiText.allcap_differential(words)` -> True if some but not all items are ALL CAPS).
- Punctuation: `PUNC_LIST` (`!`, `?`, `!!`, `!!!`, `?!?` ...). README example: "funny!" scores higher than "funny." (compound 0.8439 vs 0.8316). Exact exclamation boost size is not on the fetched pages (unverified).
- Special idioms: `SPECIAL_CASE_IDIOMS` includes `the bomb` 3, `cut the mustard` 2, `kiss of death` -1.5, `yeah right` -2, `hand to mouth` -2, `badass` 1.5, `the shit` 3.
- Contrastive "but": README lists "contrastive conjunction sensitivity" as one of the rule enhancements and gives the example "The plot was good, but the characters are uncompelling and the dialog is not great." -> compound -0.7042. The weighting factors for text after vs before "but" are not on the fetched pages (unverified; commonly described as clause after "but" dominates).
- Emoticons, emoji (UTF-8, translated to text descriptions), slang, initialisms handled via lexicon.

## README example scores (verbatim outputs)
| text | compound |
|---|---|
| VADER is smart, handsome, and funny. | 0.8316 |
| ...funny! | 0.8439 |
| VADER is very smart, handsome, and funny. | 0.8545 |
| VADER is VERY SMART, handsome, and FUNNY. | 0.9227 |
| VADER is not smart, handsome, nor funny. | -0.7424 |
| The book was only kind of good. | 0.3832 |
| Today SUX! | -0.5461 |
| Not bad at all | 0.431 |

## Limitations (documented or evident)
- Lexicon/rule based and context-light: sarcasm and domain terms are not understood (general knowledge; not stated in the fetched README).
- Scores sentence-level text; the README demo decomposes longer text into sentences with NLTK before scoring.
- English only; the README demo translates non-English text first and says VADER "does not inherently provide its own translation".
- Hashtags ignored; neutral tokens dilute `pos/neg` proportions.

## Project application
- Score per sentence (`sent_tokenize`), then aggregate (mean compound, or share of sentences by label); show the three classes with the 0.05 thresholds above.
- Feed raw sentences: no stopword removal, no lowercasing of ALL-CAPS, keep `!`.
- Mask product or brand names before scoring if they collide with lexicon words (e.g. "Best Buy": `best`).
- Extend `sia.lexicon` for domain words (e.g. "broke", "refund") after validating against star ratings; star-rating bins make a good evaluation.
- Pyodide: `vader_lexicon` is a data file that must be placed in an `nltk_data` path in the virtual filesystem (07-pyodide-notes.md).
