"""NLTK analysis shared by the Netlify build and the in-browser Pyodide worker.

Owner: nltk-expert. Reviewers: pyodide-engineer, qa-engineer.

The same file runs in two places:
- Netlify build (CPython 3.12, nltk 3.10.4): ``pipeline/build.py`` imports it.
- Browser (Pyodide 314.0.8, nltk 3.10.4 wheel): ``site/worker.mjs`` loads a copy from ``/py/``.

Rules that keep it Pyodide-safe:
- No downloads, no file or network IO. NLTK data must already be on ``nltk.data.path``
  (call ``configure(path)`` once, or set ``NLTK_DATA``).
- Only long-standing NLTK APIs: ``sent_tokenize``, ``word_tokenize``, VADER,
  ``FreqDist``, ``BigramCollocationFinder``, the stopwords corpus.
- Pure data in, JSON-serialisable dicts out; every float rounded to 3 decimals.

Output shape of ``analyze()`` = ``NltkAnalysis`` in docs/data-contract.md.
"""
from __future__ import annotations

from functools import lru_cache

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords as _stopwords
from nltk.metrics.association import BigramAssocMeasures
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize

__all__ = [
    "POSITIVE_THRESHOLD", "NEGATIVE_THRESHOLD", "NEGATIONS", "configure", "label_for",
    "split_sentences", "content_tokens", "sentiment", "valence", "analyze", "corpus_collocations",
]

#: VADER compound thresholds (Hutto & Gilbert 2014; the values the VADER authors recommend).
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

#: Negations are removed from the stoplist: "not good" must survive as a key phrase.
NEGATIONS = frozenset({
    "no", "nor", "not", "never", "none", "nothing", "nobody", "neither", "nowhere", "cannot",
    "without", "ain", "aren", "couldn", "didn", "doesn", "don", "hadn", "hasn", "haven", "isn",
    "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn",
})

#: Review filler words that crowd out useful terms in "top words" and key phrases.
DOMAIN_STOPWORDS = frozenset({
    "would", "could", "also", "get", "got", "us", "one", "even", "really", "go", "went",
    "said", "ve", "ll", "re", "im", "ive", "dont", "didnt", "lol", "ok", "okay", "oh",
})

#: Tokens the Treebank tokenizer produces for contractions, mapped to words.
_CONTRACTIONS = {"n't": "not", "ca": "can", "wo": "will", "sha": "shall", "'m": "am", "'re": "are", "'ve": "have", "'ll": "will", "'d": "would"}

TOP_N = 10

#: Review-domain additions to the VADER lexicon (valence on VADER's -4..+4 scale). Added after the
#: error analysis in reports/evaluation.md: these unambiguous food/service words are missing from
#: VADER, so "the food was bland" scored 0. Context-dependent words (cold, slow, cheap, small, dry)
#: are deliberately left out. Applied identically in the build and in Pyodide (same module).
DOMAIN_LEXICON = {
    "bland": -1.5, "stale": -1.5, "soggy": -1.6, "greasy": -1.0, "overcooked": -1.5, "undercooked": -1.5,
    "overpriced": -1.6, "wilted": -1.4, "tasteless": -1.8, "mediocre": -1.2, "filthy": -2.2, "lukewarm": -1.0,
    "burnt": -1.4, "inedible": -2.3, "watery": -1.0, "overrated": -1.4, "surly": -1.6, "unhelpful": -1.5,
    "tasty": 1.8, "flavorful": 1.8, "attentive": 1.6, "crispy": 0.8, "juicy": 1.0, "decent": 0.9, "authentic": 1.2,
}


def configure(data_path: str | None = None) -> None:
    """Put a vendored ``nltk_data`` directory first on NLTK's search path (no download)."""
    if data_path and data_path not in nltk.data.path:
        nltk.data.path.insert(0, data_path)


def _r(x: float) -> float:
    return round(float(x), 3) + 0.0  # + 0.0 turns -0.0 into 0.0


def label_for(compound: float) -> str:
    if compound >= POSITIVE_THRESHOLD:
        return "positive"
    if compound <= NEGATIVE_THRESHOLD:
        return "negative"
    return "neutral"


@lru_cache(maxsize=1)
def _sia() -> SentimentIntensityAnalyzer:
    sia = SentimentIntensityAnalyzer()
    sia.lexicon.update(DOMAIN_LEXICON)
    return sia


def valence(word: str) -> float:
    """VADER lexicon valence of one lowercase word (0.0 if the word is not in the lexicon)."""
    return float(_sia().lexicon.get(word.lower(), 0.0))


@lru_cache(maxsize=1)
def stoplist() -> frozenset[str]:
    return frozenset(_stopwords.words("english")) - NEGATIONS | DOMAIN_STOPWORDS


def split_sentences(text: str) -> list[str]:
    """Punkt sentences, also breaking at line breaks (reviews often list items one per line)."""
    out: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            out.extend(s.strip() for s in sent_tokenize(line) if s.strip())
    return out


def _words(sentence: str) -> list[str]:
    """Lowercased word tokens of one sentence; contraction pieces mapped to words."""
    toks = []
    for t in word_tokenize(sentence):
        t = t.lower()
        t = _CONTRACTIONS.get(t, t)
        if t.isalpha():
            toks.append(t)
    return toks


def content_tokens(sentence: str) -> list[str]:
    """Words of one sentence with stopwords removed (negations kept), length >= 2."""
    sw = stoplist()
    return [t for t in _words(sentence) if len(t) >= 2 and t not in sw]


def _is_top_word(w: str) -> bool:
    """Top words: content words only. Negations stay in phrases ("not good") but would
    dominate a single-word list without telling the reader anything."""
    return len(w) >= 2 and w not in stoplist() and w not in NEGATIONS


def _is_phrase_word(w: str) -> bool:
    return len(w) >= 2 and (w in NEGATIONS or w not in stoplist())


def sentiment(text: str) -> dict:
    """VADER polarity of raw text (never stopword-filtered: VADER needs negations and 'but')."""
    s = _sia().polarity_scores(text)
    return {"compound": _r(s["compound"]), "pos": _r(s["pos"]), "neu": _r(s["neu"]),
            "neg": _r(s["neg"]), "label": label_for(s["compound"])}


def _ranked(counter, key_name: str, n: int) -> list[dict]:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
    return [{key_name: k, "count": int(v)} for k, v in items]


def analyze(text: str, top_n: int = TOP_N) -> dict:
    """Full NLTK analysis of one review (shape: NltkAnalysis in docs/data-contract.md)."""
    text = text or ""
    sentences = split_sentences(text)
    words_fd: FreqDist = FreqDist()
    phrases_fd: FreqDist = FreqDist()
    n_tokens = 0
    sent_out = []
    for i, s in enumerate(sentences):
        words = _words(s)
        n_tokens += len(words)
        for w in words:
            if _is_top_word(w):
                words_fd[w] += 1
        for a, b in zip(words, words[1:]):  # adjacent words inside one sentence
            if _is_phrase_word(a) and _is_phrase_word(b) and not (a in NEGATIONS and b in NEGATIONS):
                phrases_fd[f"{a} {b}"] += 1
        sent_out.append({"index": i, "text": s, **{k: v for k, v in sentiment(s).items()}})
    return {
        "n_chars": len(text),
        "n_sentences": len(sentences),
        "n_tokens": n_tokens,
        "sentiment": sentiment(text),
        "sentences": sent_out,
        "top_words": _ranked(words_fd, "word", top_n),
        "key_phrases": _ranked(phrases_fd, "phrase", top_n),
    }


def corpus_collocations(texts: list[str], min_freq: int = 3, top_n: int = 30) -> dict:
    """Corpus-level key phrases: bigram collocations ranked by likelihood ratio.

    Bigrams are built per review (``from_documents``) on all lowercase words, so phrases are
    really adjacent in the text; pairs with a stopword (other than a negation) or a short word
    are removed with ``apply_word_filter``, and pairs seen fewer than ``min_freq`` times with
    ``apply_freq_filter`` (raw association scores over-rate rare pairs).
    """
    docs = [[w for s in split_sentences(t) for w in _words(s)] for t in texts]
    finder = BigramCollocationFinder.from_documents(docs)
    finder.apply_freq_filter(min_freq)
    finder.apply_word_filter(lambda w: not _is_phrase_word(w))
    finder.apply_ngram_filter(lambda a, b: a in NEGATIONS and b in NEGATIONS)
    scored = finder.score_ngrams(BigramAssocMeasures.likelihood_ratio)
    scored.sort(key=lambda kv: (-round(kv[1], 6), kv[0]))
    bigrams = [{"phrase": f"{a} {b}", "count": int(finder.ngram_fd[(a, b)]), "score": _r(score)}
               for (a, b), score in scored[:top_n]]
    words_fd: FreqDist = FreqDist(w for d in docs for w in d if _is_top_word(w))
    return {"top_words": _ranked(words_fd, "word", top_n), "bigrams": bigrams,
            "measure": "likelihood_ratio", "min_freq": min_freq}
