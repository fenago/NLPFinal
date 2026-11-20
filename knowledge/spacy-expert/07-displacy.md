# 07 — displaCy Visualizers (HTML/SVG export at build time)

Sources:
- https://spacy.io/usage/visualizers
- https://spacy.io/api/top-level#displacy

Fetched: 2026-11-20

## Overview
- displaCy is part of core spaCy. Styles: `"dep"` (dependency parse, POS tags + arcs, rendered as **SVG**), `"ent"` (entity highlights, rendered as **HTML**), `"span"` (overlapping spans from `doc.spans`; `style="span"` since v3.3).
- `displacy.serve(...)` starts a local web server (default port 5000, host `0.0.0.0`, `auto_select_port` v3.5) — for interactive debugging, not for static builds.
- `displacy.render(...)` **returns the markup string** — use this at build time.
- Accepts a `Doc`, a `Span`, or a list of `Doc`/`Span` (e.g. `list(doc.sents)` for one visualization per sentence).

## displacy.render signature (API page)
| Param | Meaning | Default |
| --- | --- | --- |
| `docs` | Doc(s)/Span(s)/dict(s) | — |
| `style` | `"dep"`, `"ent"`, `"span"` | `"dep"` |
| `page` | wrap as a full HTML page | `False` (note: `serve` defaults to `True`) |
| `minify` | minify the HTML | `False` |
| `options` | visualizer options dict | `{}` |
| `manual` | pass displaCy-format dicts instead of Docs | `False` |
| `jupyter` | force/disable notebook mode; auto-detected when `None` | `None` |
| returns | rendered markup | `str` |

- In a script/CI there is no Jupyter, but pass `jupyter=False` explicitly so you always get a plain string (docs' SVG export example does this).

## Entity visualizer (`style="ent"`)
```python
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.")
html = displacy.render(doc, style="ent", jupyter=False)                 # HTML fragment
page = displacy.render(doc, style="ent", page=True, jupyter=False)      # full <html> page
```
Options (`options={...}`):
| Option | Meaning |
| --- | --- |
| `ents` | list of labels to highlight; `None` = all (default) |
| `colors` | `{label: color}`; any CSS `background` value works (names, hex, rgb(), even gradients/images) |
| `template` | custom HTML template string using `{bg}`, `{text}`, `{label}` |
| `kb_url_template` (v3.2.1) | link entities with `kb_id` to a URL, e.g. `https://www.wikidata.org/wiki/{}` |
```python
options = {"ents": ["PERSON", "ORG", "GPE", "PRODUCT"],
           "colors": {"PRODUCT": "linear-gradient(90deg, #aa9cfc, #fc9ce7)", "ORG": "#7aecec"}}
displacy.render(doc, style="ent", options=options, jupyter=False)
```
- The visualizer "knows nothing about available entity types" — it renders whichever labels it gets, so **custom labels** (e.g. `BRAND`, `ASPECT`) work; supply `colors` for them (defaults only cover the trained pipelines' labels).
- Add a heading per document: `doc.user_data["title"] = "Review 12 (5 stars)"`.

## Dependency visualizer (`style="dep"`)
```python
svg = displacy.render(doc, style="dep", jupyter=False,
                      options={"compact": True, "bg": "#fff", "color": "#222", "add_lemma": False})
Path("out/review-12.svg").write_text(svg, encoding="utf-8")   # docs write SVG with open(..., "w", encoding="utf-8")
```
Options: `compact` (square arrows, less space), `color`, `bg`, `font`, `offset_x` (px left spacing; raise for long texts), `fine_grained` (use `tag_` instead of `pos_`), `add_lemma` (lemma row), `collapse_punct` (default True), `collapse_phrases` (merge noun phrases into one token), `arrow_stroke`, `arrow_width`, `arrow_spacing`, `word_spacing`, `distance`.
- Long texts are hard to read in one row: render sentence by sentence: `displacy.render(list(doc.sents), style="dep", jupyter=False)`.
- With `page=True` and a list of docs the output is one HTML page; for SVG export use a single Doc/Span per call (docs' example loops over sentences and saves one `.svg` each).
- `minify=True` for compact HTML.

## Span visualizer (`style="span"`)
Reads `doc.spans[spans_key]` (default `"sc"`); options `spans_key`, `templates`, `kb_url_template`, `colors`. Useful if aspect spans overlap (they can in `doc.spans`, not in `doc.ents`).

## Manual mode (`manual=True`)
Render data from other sources by passing displaCy dicts; helpers `displacy.parse_deps`, `displacy.parse_ents`, `displacy.parse_spans` convert Docs to that format.
```python
{"text": "But Google is starting from behind.",
 "ents": [{"start": 4, "end": 10, "label": "ORG"}], "title": None}              # ENT (char offsets)
{"words": [{"text": "This", "tag": "DT"}, ...], "arcs": [{"start": 0, "end": 1, "label": "nsubj", "dir": "left"}]}  # DEP
```
This lets you render precomputed JSON (entities with `start_char/end_char`) without spaCy.

## Web app guidance (docs)
- Do **not** wrap and serve the displaCy renderer in a web app; use the server only for spaCy processing and render JSON client-side with `displaCy.js` (https://github.com/explosion/displacy) — or here, since spaCy is build-time only, ship precomputed HTML/SVG or JSON.
- Jupyter: displaCy auto-detects and returns renderable markup (`displacy.render(doc, style="dep")` in a cell).

## Static-site export recipe (project-level, built from the documented calls)
```python
from pathlib import Path
out = Path("site/static/viz"); out.mkdir(parents=True, exist_ok=True)
for review in sample_reviews:                       # small number (e.g. 20 showcase reviews)
    doc = nlp(review["text"])
    (out / f"{review['id']}-ents.html").write_text(
        displacy.render(doc, style="ent", options=options, jupyter=False), encoding="utf-8")
    (out / f"{review['id']}-dep.svg").write_text(
        displacy.render(list(doc.sents)[0], style="dep", jupyter=False), encoding="utf-8")
```
(Rendering a `Span`, e.g. one sentence, is supported per the docs.)

## Project application
- Pre-render displaCy ENT HTML for a showcase set of reviews at build time and embed via `<iframe>` or `innerHTML`; outputs are static files for Netlify (no runtime spaCy).
- Prefer exporting **JSON + custom CSS highlighting** for the main dashboard (smaller, themeable, uses `start_char/end_char`), and use displaCy HTML/SVG only for the "how it works" page and aspect↔opinion parse illustrations.
- Fix label colors (`ORG` brand, `PERSON`, `GPE` place, `PRODUCT`) through `options["colors"]` so the legend matches the site theme; do it once in a shared constant.
- Size: dep SVGs for long sentences get very wide; keep to one sentence per file and use `compact=True`.
