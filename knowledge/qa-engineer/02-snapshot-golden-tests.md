# 02 — Snapshot / golden-file tests with pytest

Sources:
- https://docs.pytest.org/en/stable/how-to/assert.html (dict/list comparison, `pytest.approx`)
- https://docs.pytest.org/en/stable/how-to/tmp_path.html (`tmp_path`, `tmp_path_factory`)
- https://docs.pytest.org/en/stable/example/simple.html (custom `--option` via `pytest_addoption` / `config.getoption`)
- https://docs.pytest.org/en/stable/how-to/fixtures.html (session-scoped fixtures, `conftest.py`)
- https://docs.pytest.org/en/stable/how-to/skipping.html (`xfail`, `skipif`)

Fetched: 2026-11-20

## What the pytest docs give us (and do not)
- pytest core has **no built-in snapshot/golden feature** (nothing about it on the pages above). Snapshot plugins exist (e.g. syrupy, pytest-regressions) but were **not fetched — unverified**; the approach below uses only core pytest.
- Core building blocks that are verified:
  - Plain `assert actual == expected` on dicts/lists prints a structured diff ("comparing dicts: different entries"; `-v` for more).
  - `pytest.approx` handles floats inside scalars, lists, **dictionaries** and NumPy arrays: `assert actual_scores == pytest.approx(golden_scores, abs=1e-3)` (flat dicts of numbers).
  - `tmp_path` gives a per-test `pathlib.Path`; `tmp_path_factory` (session scope) for build outputs shared across tests.
  - A CLI flag can be added in `conftest.py` with `parser.addoption(...)`, read with `request.config.getoption("--opt")`.

## Golden-file approach (project convention, built from the primitives above)
Layout (proposed): `tests/golden/<case>.json` committed to git; code under test writes to `tmp_path`.

```python
# tests/conftest.py
import json, pathlib, pytest

GOLDEN = pathlib.Path(__file__).parent / "golden"

def pytest_addoption(parser):
    parser.addoption("--update-golden", action="store_true", default=False,
                     help="rewrite tests/golden/*.json from current output")

@pytest.fixture
def golden(request):
    update = request.config.getoption("--update-golden")
    def check(name, actual):
        path = GOLDEN / f"{name}.json"
        text = json.dumps(actual, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if update or not path.exists():
            path.parent.mkdir(exist_ok=True); path.write_text(text, encoding="utf-8")
            if not update:
                pytest.fail(f"golden {name} did not exist; created - review and commit")
            return
        expected = json.loads(path.read_text(encoding="utf-8"))
        assert actual == expected     # pytest prints the dict diff
    return check
```

```python
# tests/test_golden.py
def test_smoke_review_analysis(golden, nlp, analyze):    # analyze = project function
    out = analyze("I ordered the Sony WH-1000XM5 headphones from Best Buy in Chicago. ...")
    golden("smoke_review", round_floats(out, 3))
```

## Rules for stable goldens
1. **Deterministic input**: fixed small texts or a fixed seed-sampled fixture file (docs/04 uses `random.seed(42)`); never the full dataset.
2. **Normalize before comparing**: `sort_keys=True`, sort lists that have no meaningful order (entities by `(start,end)`), round floats (VADER to 3 dp), drop timestamps / absolute paths / library version strings.
3. **Pin versions**: golden content depends on NLTK / spaCy / `en_core_web_sm` versions (docs: NLTK 3.10.4, spaCy 3.8.18, model 3.8.0). Store them in the golden file's `_meta` or compare version separately; a model bump is an expected golden update.
4. **Review diffs, don't blindly update**: `pytest --update-golden`, then `git diff tests/golden` must be read by a human (or the nlp-evaluator) before commit.
5. **Compare floats tolerantly** with `pytest.approx` when exact equality is flaky across platforms; compare labels/entities exactly.
6. Keep each golden small (<~20 KB) so diffs are reviewable.
7. Known-wrong outputs can be pinned with `@pytest.mark.xfail(strict=True, reason="en_core_web_sm tags Best Buy as PERSON")` so the suite flips red when the bug gets fixed (strict xfail verified in skipping docs).

## Project application
- Goldens to create: `smoke_review.json` (doc 02/03 test review: doc VADER, 3 sentence scores, ents, noun chunks, aspect-opinion pairs), `entityruler_bestbuy.json`, `negation_not_helpful.json`.
- Also a **built-output golden**: run the build on a 20-review fixture into `tmp_path` and compare file list + key set (schema covers shape, see 03-json-schema-validation.md).
- Do not golden the full `site/data/*.json` — use schema + stats checks there.
