"""Unit tests for nlp/nltk_analyzer.py (owner: nltk-expert)."""
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("compound,label", [(0.05, "positive"), (0.049, "neutral"), (-0.049, "neutral"),
                                            (-0.05, "negative"), (0.0, "neutral")])
def test_label_thresholds(na, compound, label):
    assert na.label_for(compound) == label


def test_analyze_shape_and_rounding(na):
    out = na.analyze("The pizza was great. The service was not good!")
    assert set(out) == {"n_chars", "n_sentences", "n_tokens", "sentiment", "sentences", "top_words", "key_phrases"}
    assert out["n_sentences"] == 2
    floats = [out["sentiment"][k] for k in ("compound", "pos", "neu", "neg")]
    floats += [s[k] for s in out["sentences"] for k in ("compound", "pos", "neu", "neg")]
    assert all(round(f, 3) == f for f in floats)
    json.dumps(out)  # JSON-serialisable


def test_sentence_scores_and_negation(na):
    out = na.analyze("The pizza was great. The service was not good!")
    assert [s["label"] for s in out["sentences"]] == ["positive", "negative"]
    assert {"phrase": "not good", "count": 1} in out["key_phrases"]


def test_negations_kept_for_phrases_but_not_top_words(na):
    out = na.analyze("I can't recommend it. Not worth it, never again.")
    words = {w["word"] for w in out["top_words"]}
    phrases = {p["phrase"] for p in out["key_phrases"]}
    assert "not" not in words and "never" not in words
    assert "not recommend" in phrases          # "ca n't" -> "can not"; "can" is a stopword
    assert "ca" not in words


def test_vader_sees_raw_text_not_stopword_filtered(na):
    # "but" and "not" drive VADER; they must reach it.
    assert na.analyze("It was not good.")["sentiment"]["label"] == "negative"


def test_line_breaks_split_sentences(na):
    out = na.analyze("Pros\n- great coffee\n- friendly staff")
    assert out["n_sentences"] == 3


def test_empty_text(na):
    out = na.analyze("")
    assert out["n_sentences"] == 0 and out["top_words"] == [] and out["sentiment"]["label"] == "neutral"


def test_deterministic(na):
    t = "Great food, great service, great prices. Bad parking."
    assert na.analyze(t) == na.analyze(t)


def test_corpus_collocations(na):
    texts = ["The fish sandwich was great."] * 3 + ["Customer service was slow. The fish sandwich again."] * 3
    out = na.corpus_collocations(texts, min_freq=3)
    phrases = [b["phrase"] for b in out["bigrams"]]
    assert "fish sandwich" in phrases and "customer service" in phrases
    assert all(b["count"] >= 3 for b in out["bigrams"])
    assert out["measure"] == "likelihood_ratio"


def test_module_is_pyodide_safe():
    """No downloads, no file/network IO in the module shared with the browser."""
    src = (ROOT / "nlp/nltk_analyzer.py").read_text()
    for banned in ("nltk.download", "urllib", "requests", "open(", "subprocess", "import spacy"):
        assert banned not in src, banned
