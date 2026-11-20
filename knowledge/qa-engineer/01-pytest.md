# 01 — pytest essentials (discovery, assert, fixtures, parametrize, tmp_path, skip)

Sources:
- https://docs.pytest.org/en/stable/explanation/goodpractices.html
- https://docs.pytest.org/en/stable/how-to/assert.html
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.pytest.org/en/stable/how-to/parametrize.html
- https://docs.pytest.org/en/stable/how-to/tmp_path.html
- https://docs.pytest.org/en/stable/how-to/skipping.html
- https://docs.pytest.org/en/stable/example/simple.html

Fetched: 2026-11-20 (docs "stable", pytest 9.x in the examples)

## Test discovery (goodpractices)
- Files: `test_*.py` or `*_test.py`.
- Inside them: `test`-prefixed functions/methods outside classes, and `test`-prefixed methods inside `Test`-prefixed classes (no `__init__`). `@staticmethod`/`@classmethod` methods are also collected.
- Layout: docs show "tests outside application code" and recommend a `src` layout, especially with the default import mode `prepend`. "For new projects, we recommend to use importlib import mode."
- Run: `pytest` (whole tree), `pytest tests/test_build.py::test_name`, `pytest -q`, `pytest -k "ner"`, `pytest -x` (stop at first failure) (the `-k/-x` flags are standard pytest CLI, not re-verified on the pages above).

## assert (how-to/assert)
- Plain `assert expr`; pytest rewrites asserts to show intermediate values. Failing set comparisons print "Extra items in the left set / right set"; dict/list diffs are also introspected; add `-v` for more diff.
- Floats: `assert (0.1 + 0.2) == pytest.approx(0.3)`. `pytest.approx` works with scalars, lists, dictionaries and NumPy arrays (also NaN) — use it for VADER compound scores.
- Exceptions:
  ```python
  with pytest.raises(ValueError, match=r".* 123 .*"):   # match uses re.search on str(exc)
      myfunc()
  ```
  `with pytest.raises(RuntimeError) as excinfo:` then `excinfo.type`, `.value`, `.traceback`. It matches subclasses; check `excinfo.type is X` for exact type.

## Fixtures (how-to/fixtures)
- Possible `scope` values: `function` (default), `class`, `module`, `package`, `session`.
  "scope='module' ... only be invoked once per test module (the default is to invoke once per test function)."
- Shared fixtures go in `conftest.py` so every test module in the directory can use them:
  ```python
  # tests/conftest.py
  import pytest, spacy

  @pytest.fixture(scope="session")
  def nlp():                      # load spaCy ONCE for the whole run
      return spacy.load("en_core_web_sm")
  ```
  (pattern adapted from the docs' `smtp_connection` `scope="module"` example; the spaCy loading itself is project-specific.)
- Note from docs: "Pytest only caches one instance of a fixture at a time" — parametrized fixtures may be re-invoked within a scope.
- Dynamic scope (v5.2+): `scope=callable(fixture_name, config)` returning a scope string.
- Teardown: prefer `yield` fixtures — code after `yield` runs at teardown, in reverse order of setup. Alternative: `request.addfinalizer(fn)`. If a fixture raises before `yield`, its own teardown is skipped.
- Safe structure: "limit fixtures to only making one state-changing action each".

## parametrize (how-to/parametrize)
```python
@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```
- Each tuple becomes its own test case (3 runs).
- Per-case marks: `pytest.param("6*9", 42, marks=pytest.mark.xfail)`.
- (`ids=` to name cases is a standard parametrize argument; not shown in the excerpt fetched — unverified here.)

## tmp_path / tmp_path_factory (how-to/tmp_path)
- `tmp_path` = unique `pathlib.Path` temp dir per test function.
  ```python
  def test_create_file(tmp_path):
      p = tmp_path / "sub" / "hello.txt"; p.parent.mkdir()
      p.write_text("content", encoding="utf-8")
  ```
- `tmp_path_factory` is session-scoped: `tmp_path_factory.mktemp("data") / "img.png"` for expensive shared artefacts.
- Default layout `{temproot}/pytest-of-{user}/pytest-{num}/{testname}/`; last 3 runs retained (`tmp_path_retention_count`, `tmp_path_retention_policy`).

## skip / xfail / markers (how-to/skipping, example/simple)
- `@pytest.mark.skip(reason=...)`, `pytest.skip("msg")` inside a test, module-level `pytest.skip(..., allow_module_level=True)`.
- `@pytest.mark.skipif(cond, reason=...)`; `pytestmark = pytest.mark.skipif(...)` skips a whole module.
- `docutils = pytest.importorskip("docutils", minversion="0.3")` skips if a dependency is missing.
- `@pytest.mark.xfail(reason=..., raises=..., run=False, strict=True)`; `xfail_strict = true` in `[pytest]` config makes unexpected passes fail.
- Custom CLI flag pattern: `pytest_addoption(parser)` + `request.config.getoption("--opt")` in `conftest.py`; `pytest_collection_modifyitems` can auto-skip tests marked `slow` unless `--runslow`.

## Project application
- Layout proposal: `tests/` with `conftest.py` (session-scoped `nlp`, `vader`, `sample_reviews` fixtures), `test_build_pipeline.py`, `test_schema.py`, `test_golden.py`.
- Load spaCy once with a `scope="session"` fixture; `en_core_web_sm` load is the slow step.
- Use `pytest.approx(..., abs=1e-3)` for VADER scores; plain `==` for labels/entities.
- Parametrize over the three review sentences from docs/02 and docs/03 (Best Buy / Sony WH-1000XM5 / "not helpful" negation).
- `@pytest.mark.slow` for full-corpus builds; skip by default, run in CI with `--runslow`.
- Use `tmp_path` for the build output dir so tests never write into `site/data`.
