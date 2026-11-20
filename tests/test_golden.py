"""Golden (saved expected output) tests. Owner: qa-engineer.

Regenerate after an intended change:  UPDATE_GOLDEN=1 pytest tests/test_golden.py
then review the diff of tests/golden/*.json in the pull request.
"""
import json
import os
from pathlib import Path

GOLDEN = Path(__file__).parent / "golden"
NLTK_TEXTS = [
    "The pizza was great. The service was not good!",
    "I can't believe how bland the pasta was. Never again.",
    "Absolutely loved it! Best tacos in town and the service was quick.",
    "The burger was good but not great.\nPrices are fair, parking is a pain.",
]
SPACY_TEXTS = [
    "I bought the Sony WH-1000XM5 headphones at Best Buy in Chicago. The battery life is not great.",
    "Our barista, Marco, made the best latte in Pittsburgh. The pastries were stale and the music was too loud.",
    "We had the Big Mac at McDonald's and a delicious fish sandwich at Papa J's.",
]


def check(name, actual):
    path = GOLDEN / f"{name}.json"
    if os.environ.get("UPDATE_GOLDEN") or not path.exists():
        path.write_text(json.dumps(actual, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    assert json.loads(path.read_text(encoding="utf-8")) == actual, f"golden mismatch: {path.name}"


def test_nltk_golden(na):
    check("nltk", [na.analyze(t) for t in NLTK_TEXTS])


def test_spacy_golden(nlp, sa):
    check("spacy", sa.analyze_texts(nlp, SPACY_TEXTS))


def test_collocations_golden(site_data):
    check("collocations_top10", site_data["collocations"]["bigrams"][:10])
