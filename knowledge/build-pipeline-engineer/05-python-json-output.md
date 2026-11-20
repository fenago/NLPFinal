# 05 - Writing JSON from Python (json + pathlib)

Sources:
- https://docs.python.org/3/library/json.html (page header: Python 3.15.2 documentation)
- https://docs.python.org/3/library/pathlib.html

Fetched: 2026-11-20

## json.dump / json.dumps signature (verbatim)

```python
json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True,
          allow_nan=True, cls=None, indent=None, separators=None, default=None,
          sort_keys=False, **kw)
json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
           allow_nan=True, cls=None, indent=None, separators=None, default=None,
           sort_keys=False, **kw)
```
All options after `obj`/`fp` are keyword-only.

## Options that matter here

- **`ensure_ascii`** (default `True`): all non-ASCII and non-printable characters are escaped (`\uXXXX`), so output is pure ASCII. With `False`, characters are output as-is except those that must be escaped (quote, backslash, control chars U+0000-U+001F). For reviews with accents/emoji, `ensure_ascii=False` gives smaller, readable files; then **write the file as UTF-8** (`encoding="utf-8"`) and serve with a UTF-8 charset (Netlify serves `.json` as `application/json`; JSON is UTF-8 by spec).
- **`separators`**: compact encoding example from the docs:
  ```python
  >>> json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
  '[1,2,3,{"4":5,"6":7}]'
  ```
  Default separators are `(', ', ': ')` when `indent` is `None` and `(',', ': ')` when `indent` is set (default values per the docs; the fetched extract showed only the compact example, so the defaults are (unverified) here but standard).
- **`indent`**: pretty printing example from the docs:
  ```python
  >>> print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
  {
      "4": 5,
      "6": 7
  }
  ```
  Use `indent=None` + compact `separators` for production data files; `indent=2` for small committed fixtures that people diff.
- **`sort_keys=True`**: deterministic key order (keys sorted before string conversion; numeric keys sort numerically). Good for reproducible builds / clean diffs.
- **`allow_nan`** (default `True`): the module writes `NaN`, `Infinity`, `-Infinity`, which are **not valid JSON** (the RFC forbids them) and `JSON.parse` in the browser **will throw**. Docs example: `json.dumps(float('nan'))` -> `'NaN'`. Use `allow_nan=False` in the build so bad values raise `ValueError`, and sanitize first (e.g. replace NaN with `None`).
- **Key coercion**: dict keys are always converted to strings; `loads(dumps(x)) != x` if keys weren't strings (e.g. int keys come back as str).
- Tuples are serialized as arrays; sets, `numpy` scalars, `datetime`, spaCy objects are **not** serializable: pass `default=` (a function returning a serializable form, raising `TypeError` otherwise) or convert manually to `str/int/float/list`.
- Binary file objects are accepted for `json.load` (UTF-8/16/32 input); for `json.dump` use a text file opened with `encoding="utf-8"`.

## pathlib basics for writing files (signatures verbatim from the docs)

```python
Path.mkdir(mode=0o777, parents=False, exist_ok=False, *, parent_mode=None)   # parent_mode: added 3.15
Path.write_text(data, encoding=None, errors=None, newline=None)             # newline param: added 3.10
Path.read_text(encoding=None, errors=None, newline=None)                    # newline param: added 3.13
Path.write_bytes(data)
Path.open(mode='r', buffering=-1, encoding=None, errors=None, newline=None)
Path.exists(*, follow_symlinks=True)
Path.iterdir(); Path.glob(pattern, ...); Path.rglob(pattern, ...)
Path.unlink(missing_ok=False)
Path.rename(target)
PurePath.with_suffix(suffix); PurePath.name / .stem / .suffix; PurePath.parent / .parents
Path.cwd(); Path.resolve()
```
- `/` joins paths: `PurePath('/etc') / 'init.d' / 'apache2'` -> `/etc/init.d/apache2`.
- Idiom for the script location (not a verbatim docs snippet; composed from `resolve()` and `.parent`): `ROOT = Path(__file__).resolve().parent.parent`.
- `write_text` default encoding is the locale's; **always pass `encoding="utf-8"`** (Windows dev machines differ).

## Recommended build output code

```python
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data"
OUT.mkdir(parents=True, exist_ok=True)

def write_json(name, obj, *, pretty=False):
    path = OUT / name
    text = json.dumps(
        obj,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
    )
    path.write_text(text, encoding="utf-8")
    return path.stat().st_size
```
- Write to a temp name then `Path.replace()` for atomic writes if needed (`replace` exists; semantics not fetched, (unverified)).
- Print each file's size at the end of the build to keep an eye on payload (large per-review JSON can be split into shards, e.g. `reviews-000.json`).

## Project application

- Files likely emitted: `summary.json` (counts, VADER vs stars), `aspects.json`, `entities.json`, `collocations.json`, `reviews-*.json` (drill-down). Keep top-level objects (not bare arrays) so fields can be added later.
- Convert spaCy/NLTK outputs to plain `str/int/float/list/dict` before dumping; round floats (`round(x, 4)`) to shrink files.
- Validate in the build with `json.loads(text)` after dumping and with `allow_nan=False` so the front end never sees invalid JSON.
- Netlify `[[headers]]` for `/data/*` can set `Cache-Control` (see 01).
