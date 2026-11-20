"""Shared pytest fixtures. Owner: qa-engineer.

The `built_site` fixture runs the real Netlify build command (pipeline/build.py) into a temporary
directory once per session, so tests never depend on a stale site/data/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DATA_FILES = ["meta", "summary", "reviews", "collocations", "aspects", "entities", "examples"]


@pytest.fixture(scope="session")
def na():
    from nlp import nltk_analyzer
    nltk_analyzer.configure(str(ROOT / "nltk_data"))
    return nltk_analyzer


@pytest.fixture(scope="session")
def sa(na):
    from nlp import spacy_analyzer
    return spacy_analyzer


@pytest.fixture(scope="session")
def nlp(sa):
    return sa.build_nlp(ROOT / "data/entity_patterns.jsonl")


def run_build(out: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ROOT / "pipeline/build.py"), "--out", str(out)],
                          capture_output=True, text=True, cwd=ROOT, check=False)


@pytest.fixture(scope="session")
def built_site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("site")
    proc = run_build(out)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return out


@pytest.fixture(scope="session")
def site_data(built_site) -> dict:
    return {name: json.loads((built_site / "data" / f"{name}.json").read_text(encoding="utf-8")) for name in DATA_FILES}
