"""Size budgets (data-size-budget S22), Netlify limits and the netlify-guardrail (S05). Owner: qa-engineer."""
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from conftest import run_build

ROOT = Path(__file__).resolve().parents[1]
MB = 1024 * 1024
FIRST_VIEW = ["meta", "summary", "collocations", "aspects", "entities"]  # what the dashboard loads first


def test_data_file_budgets(built_site):
    for p in (built_site / "data").glob("*.json"):
        limit = 3 * MB if p.name == "reviews.json" else 1 * MB
        assert p.stat().st_size <= limit, f"{p.name} is {p.stat().st_size} bytes (limit {limit})"


def test_first_view_budget(built_site):
    total = sum((built_site / "data" / f"{n}.json").stat().st_size for n in FIRST_VIEW)
    assert total <= 500 * 1024, f"dashboard first view loads {total} bytes"


def test_no_file_over_10mb_in_site():
    site = ROOT / "site"
    big = [str(p) for p in site.rglob("*") if p.is_file() and p.stat().st_size > 10 * 1000 * 1000]
    assert not big, f"Netlify warns about files over 10 MB: {big}"


def test_pyodide_payload_budget():
    pyo = ROOT / "site/pyodide"
    if not pyo.exists():
        pytest.skip("run python scripts/fetch_pyodide.py first")
    total = sum(p.stat().st_size for p in pyo.rglob("*") if p.is_file())
    assert total <= 20 * 1000 * 1000, f"self-hosted Pyodide is {total / 1e6:.1f} MB (budget 20 MB)"


def test_build_is_deterministic(built_site, tmp_path):
    proc = run_build(tmp_path)
    assert proc.returncode == 0, proc.stderr
    for p in (built_site / "data").glob("*.json"):
        assert p.read_bytes() == (tmp_path / "data" / p.name).read_bytes(), f"{p.name} differs between builds"


def test_netlify_toml_guardrail():
    cfg = tomllib.loads((ROOT / "netlify.toml").read_text())
    assert cfg["build"]["publish"] == "site"
    assert cfg["build"]["environment"]["PYTHON_VERSION"] == "3.12"
    assert "pipeline/build.py" in cfg["build"]["command"] and "fetch_pyodide.py" in cfg["build"]["command"]
    assert "functions" not in cfg and "edge_functions" not in cfg and "redirects" not in cfg
    assert not (ROOT / "netlify/functions").exists()


def test_no_header_set_twice_for_one_path():
    """Overlapping [[headers]] rules that set the same header can combine into an invalid value
    (seen locally: 'application/wasm, application/wasm' broke WebAssembly compilation)."""
    sys.path.insert(0, str(ROOT / "tests/support"))
    from serve_netlify import compile_rules
    rules = compile_rules(ROOT / "netlify.toml")
    paths = ["/", "/index.html", "/app.js", "/worker.mjs", "/pyodide/manifest.json", "/pyodide/v314.0.8/pyodide.asm.wasm",
             "/pyodide/v314.0.8/pyodide.mjs", "/pyodide/v314.0.8/wheels/nltk-3.10.4-py3-none-any.whl",
             "/data/reviews.json", "/nltk_data/sentiment/vader_lexicon.zip", "/py/nltk_analyzer.py", "/vendor/chart.umd.min.js"]
    for path in paths:
        seen = {}
        for rx, values in rules:
            if rx.match(path):
                for k in values:
                    assert k.lower() not in seen, f"{path}: header {k} set by two rules ({seen[k.lower()]} and {rx.pattern})"
                    seen[k.lower()] = rx.pattern


def test_requirements_pinned():
    lines = [l.strip() for l in (ROOT / "requirements.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]
    assert "nltk==3.10.4" in lines and "spacy==3.8.18" in lines
    assert any(l.startswith("en_core_web_sm @ https://github.com/explosion/spacy-models/") and "3.8.0" in l for l in lines)


def test_no_runtime_cdn_or_external_urls():
    """Everything the browser loads must come from the Netlify origin."""
    pattern = re.compile(r"""(?:src|href|import\s*\(?|from|fetch\()\s*=?\s*["'`]https?://""", re.I)
    banned = ("cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com", "googleapis.com")
    for p in [*(ROOT / "site").glob("*.html"), *(ROOT / "site").glob("*.js"), *(ROOT / "site").glob("*.mjs")]:
        text = p.read_text(encoding="utf-8")
        assert not pattern.search(text), f"external load in {p.name}"
        assert not any(b in text for b in banned), f"CDN reference in {p.name}"


def test_spacy_never_shipped_to_browser():
    for p in [*(ROOT / "site").glob("*.js"), *(ROOT / "site").glob("*.mjs")]:
        assert "spacy_analyzer" not in p.read_text(encoding="utf-8")
