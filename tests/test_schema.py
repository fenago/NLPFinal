"""Every generated site/data file validates against its JSON Schema (data contract 1.x). Owner: qa-engineer."""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from conftest import DATA_FILES

ROOT = Path(__file__).resolve().parents[1]


def schema(name):
    s = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
    Draft202012Validator.check_schema(s)
    return s


@pytest.mark.parametrize("name", DATA_FILES)
def test_file_matches_schema(site_data, name):
    errors = sorted(Draft202012Validator(schema(name)).iter_errors(site_data[name]), key=lambda e: list(e.path))
    assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors[:10])


@pytest.mark.parametrize("name", DATA_FILES)
def test_contract_version(site_data, name):
    assert site_data[name]["contract_version"] == "1.0.0"


def test_live_output_matches_contract(na):
    """The Pyodide worker returns analyze() output: it must satisfy the same NltkAnalysis schema."""
    out = na.analyze("Loved the tacos. Hated the parking!\nWould not return.")
    Draft202012Validator(schema("nltk_analysis")).validate(out)


def test_review_nltk_equals_live_function(site_data, na):
    """reviews.json[*].nltk is exactly what analyze() returns (same shape as the live path)."""
    for r in site_data["reviews"]["reviews"][:20]:
        assert r["nltk"] == na.analyze(r["text"])


def test_summary_is_consistent(site_data):
    s, reviews = site_data["summary"], site_data["reviews"]["reviews"]
    assert s["n_reviews"] == len(reviews) == sum(s["stars_counts"].values())
    assert sum(map(sum, s["vader_vs_stars"]["counts"])) == len(reviews)
    assert sum(s["compound_histogram"]["counts"]) == len(reviews)


def test_examples_include_labelled_demo(site_data):
    ex = site_data["examples"]["examples"]
    demos = [e for e in ex if e["is_demo"]]
    assert demos and all(e["stars"] is None and e["title"].startswith("Demo") for e in demos)
    assert any(not e["is_demo"] for e in ex)
    assert all(e["spacy"]["tokens"] for e in ex)
