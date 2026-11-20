# 03 — JSON Schema validation for the build's JSON output

Sources:
- https://json-schema.org/learn/getting-started-step-by-step
- https://python-jsonschema.readthedocs.io/en/stable/validate/ (jsonschema 4.26.0 per page title)

Fetched: 2026-11-20

## JSON Schema basics (getting-started page)
- `$schema`: which draft the schema follows. Use Draft 2020-12: `"$schema": "https://json-schema.org/draft/2020-12/schema"`.
- `$id`: a URI for the schema (lets other schemas `$ref` into it).
- `title`, `description`: annotations only; "don't add any constraints".
- `type`: first constraint (e.g. `"object"`).
- `properties`: an object whose keys are the allowed property names, each with its own sub-schema. Properties are optional unless listed in `required`.
- `required`: array of property names that must be present (page example: `productId` is required because it is the canonical identifier).
- Other keywords named in the guide (standard JSON Schema; details not re-quoted here): `minimum`, `exclusiveMinimum`, `items`, `minItems`, `uniqueItems`, `$ref`.
- Example skeleton from the page:
  ```json
  {"$schema": "https://json-schema.org/draft/2020-12/schema",
   "$id": "https://example.com/product.schema.json",
   "title": "Product", "description": "A product in the catalog", "type": "object"}
  ```

## python-jsonschema API (validate page)
- `jsonschema.validate(instance, schema, cls=None, *args, **kwargs)`
  - Raises `jsonschema.exceptions.ValidationError` if the instance is invalid, `SchemaError` if the schema itself is invalid.
  - It "will first verify that the provided schema is itself valid".
  - Without `cls`, if no `$schema` is present "the default validator class is the latest released draft"; with `$schema` it picks the matching validator.
  - Docs advice: validating many instances → use a validator object directly, e.g. `Draft202012Validator(schema).validate(instance)`.
- `Draft202012Validator.check_schema(schema)` validates the schema against its metaschema (raises `SchemaError`).
- `validator.iter_errors(instance)` lazily yields **every** `ValidationError` (doc example sorts by `key=str`); each has `.message`. Better than `validate()` for reporting all problems at once.
  ```python
  from jsonschema import Draft202012Validator
  v = Draft202012Validator(schema)
  for err in sorted(v.iter_errors(data), key=lambda e: list(e.path)):
      print(err.message)
  ```
  (`.path` / `.json_path` / `best_match` exist in the errors docs — page https://python-jsonschema.readthedocs.io/en/stable/errors/ was **not fetched**, unverified.)
- Formats: by default `format` is **not enforced**. Enable with
  `validate(instance=..., schema=..., format_checker=Draft202012Validator.FORMAT_CHECKER)` (or `jsonschema.FormatChecker`). Some formats need extras: `pip install jsonschema[format]` (e.g. `date-time` needs rfc3339-validator; `date`, `email`, `ipv4`, `uuid`, `regex` have no extra deps per the table).
- Types: JSON `number` accepts Python `int`, `float`, `Decimal`; `integer` = `int`, `object` = `dict` only.

## Example schema for a build artefact (proposed; field names illustrative)
```python
REVIEW_SUMMARY_SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "sentiment summary", "type": "object",
  "required": ["n_reviews", "sentiment", "top_aspects"],
  "properties": {
    "n_reviews": {"type": "integer", "minimum": 1},
    "sentiment": {
      "type": "object", "required": ["pos", "neu", "neg"],
      "properties": {k: {"type": "integer", "minimum": 0} for k in ("pos", "neu", "neg")}},
    "top_aspects": {"type": "array", "minItems": 1, "items": {
      "type": "object", "required": ["aspect", "count", "mean_compound"],
      "properties": {"aspect": {"type": "string", "minLength": 1},
                     "count": {"type": "integer", "minimum": 1},
                     "mean_compound": {"type": "number", "minimum": -1, "maximum": 1}}}}
  }
}
```

## pytest integration
```python
import json, pathlib, pytest
from jsonschema import Draft202012Validator

DATA = pathlib.Path("site/data")            # adjust to the real output dir
SCHEMAS = pathlib.Path("tests/schemas")

@pytest.mark.parametrize("name", ["summary", "aspects", "entities", "collocations"])
def test_output_matches_schema(name):
    schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)               # schema itself is sane
    data = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=str)
    assert not errors, "\n".join(e.message for e in errors[:10])
```

## Project application
- Keep schemas in `tests/schemas/*.schema.json`; the front-end team and the build team share them as the contract.
- Validate: required keys, `compound` within [-1, 1], counts are non-negative integers, label enums (`"enum": ["pos","neu","neg"]`), entity labels in the allowed set (`PERSON, GPE, LOC, FAC, ORG, PRODUCT`, from docs/03).
- Add `additionalProperties: false` on objects the browser code reads, so accidental renames are caught (standard keyword, not covered on the fetched page).
- Cross-checks JSON Schema cannot do (sum of sentiment counts == `n_reviews`, no `NaN`) go in plain pytest asserts.
- Ensure the JSON is strict: Python's `json.dumps` can emit `NaN`; set `allow_nan=False` in the build (stdlib behaviour, unverified against docs here).
