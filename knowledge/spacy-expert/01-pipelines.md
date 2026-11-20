# 01 — spaCy Processing Pipelines

Sources:
- https://spacy.io/usage/processing-pipelines (sections: Processing text, Multiprocessing, Pipelines and built-in components, Disabling/excluding/modifying components, Custom components)
- https://spacy.io/models/en (pipeline component names of en_core_web_sm)

Fetched: 2026-11-20

## Core idea
- `doc = nlp(text)` tokenizes, then calls each pipeline component on the `Doc` in order; each returns the modified `Doc`.
- Under the hood (docs' abstract example): `doc = nlp.make_doc(text)` then `for name, proc in nlp.pipeline: doc = proc(doc)`.
- `spacy.load("en_core_web_sm")` reads `config.cfg`/`meta.json`, builds the `English` language class, adds each component, then loads weights (`from_disk`).
- Inspect: `nlp.pipeline` = list of `(name, component)`; `nlp.pipe_names` = names of *active* components only.

```python
print(nlp.pipe_names)
# ['tok2vec', 'tagger', 'parser', 'ner', 'attribute_ruler', 'lemmatizer']   (docs' example output)
```

Other inspection attributes (docs table):
| Attribute | Meaning |
| --- | --- |
| `nlp.pipeline` | `(name, component)` tuples of the active pipeline, in order |
| `nlp.pipe_names` | active component names |
| `nlp.components` | all `(name, component)` incl. disabled |
| `nlp.component_names` | all names incl. disabled |
| `nlp.disabled` | names currently disabled |

## Batch processing: `nlp.pipe`
- Use `nlp.pipe(texts)` instead of `[nlp(t) for t in texts]`; it takes an iterable, yields `Doc`s, batches internally (a generator, good for streams).
- Default batch size is `nlp.batch_size` (docs say "typically 1000").
- `as_tuples=True`: input is `(text, context)` tuples, output `(doc, context)` tuples (pass review IDs/metadata through).
- `nlp.pipe(texts, disable=[...])` disables components for that call only.

```python
for doc in nlp.pipe(texts, batch_size=256, disable=["lemmatizer"]):
    ...

for doc, ctx in nlp.pipe(((r["text"], {"id": r["id"]}) for r in reviews), as_tuples=True):
    ctx["id"]
```

### Multiprocessing (`n_process`)
```python
docs = nlp.pipe(texts, n_process=4)                 # 4 processes
docs = nlp.pipe(texts, n_process=-1)                # all CPUs ("use with caution")
docs = nlp.pipe(texts, n_process=2, batch_size=2000)
```
- Docs warn that starting many processes can add large overhead; the default `spawn` start method on macOS/Windows is slow for larger models because model data is copied per process.
- For short tasks, fewer processes with a bigger `batch_size` can be faster; optimum depends on components, doc length, #processes, memory.

## Built-in component string names (for `add_pipe`)
`tagger`, `parser`, `ner`, `entity_linker`, `entity_ruler`, `textcat`, `textcat_multilabel`, `lemmatizer`, `trainable_lemmatizer`, `morphologizer`, `attribute_ruler`, `senter`, `sentencizer`, `tok2vec`, `transformer`.

## Disable vs exclude
- **Disable**: loaded but not run; can be turned on later with `nlp.enable_pipe(name)`. Saved with the pipeline but disabled.
- **Exclude**: not loaded at all; no reference afterward (smaller/faster load).

```python
nlp = spacy.load("en_core_web_sm", exclude=["ner"])                 # not loaded
nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser"])    # loaded, inactive
nlp.enable_pipe("tagger")
nlp = spacy.load("en_core_web_sm", enable=["tok2vec", "tagger"])    # everything else disabled
# enable and disable conflicting on same name -> error
```

### `nlp.select_pipes` (temporary)
```python
with nlp.select_pipes(disable=["tagger", "parser", "lemmatizer"]):
    doc = nlp("not tagged/parsed")          # restored on exit

disabled = nlp.select_pipes(disable="ner")  # manual form
...
disabled.restore()

with nlp.select_pipes(enable="parser"):     # only the parser runs
    doc = nlp("I will only be parsed")
```

### Remove / rename / replace
```python
nlp.remove_pipe("parser")
nlp.rename_pipe("ner", "entityrecognizer")
nlp.replace_pipe("tagger", "my_custom_tagger")
```

## Dependencies between components (important for this project)
- The docs' own NER-only example disables `["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]` and keeps `ner`. In `en_core_web_sm` the `ner` has its own internal listener setup; whether `ner` works without `tok2vec` in this exact package is **(unverified)** from the fetched pages — the docs example does it with `en_core_web_sm`, so it is shown to work for NER-only extraction.
- Noun chunks, dependency navigation (`head`, `children`, `dep_`) need `parser` (and `tagger`/`attribute_ruler` for `pos_`, `lemmatizer` needs POS). Do not disable those for the aspect-opinion step.

## Adding a component: `nlp.add_pipe` position arguments
| Argument | Meaning |
| --- | --- |
| `last=True` | add at end (default) |
| `first=True` | add at start |
| `before="name"` / index | add before that component |
| `after="name"` / index | add after that component |
| `name=` | custom instance name |
| `source=source_nlp` | copy a trained component from another loaded pipeline (first arg is then its name in the source) |

```python
nlp.add_pipe("info_component", name="print_info", last=True)
nlp.add_pipe("custom_sentencizer", before="parser")
ruler = nlp.add_pipe("entity_ruler", before="ner")   # see 06-entityruler.md
```
- Custom stateless component: `@Language.component("name")` on a function `(doc) -> doc`.

## Project application
- Build-time script: load once, `nlp.pipe(review_texts, batch_size=..., n_process=...)` over the sampled dataset; use `as_tuples=True` to carry `review_id`/`stars` along and write per-review JSON.
- Use `nlp.pipe_names` to log/assert the pipeline in the build log (`tok2vec, tagger, parser, attribute_ruler, lemmatizer, ner` expected, plus `entity_ruler` once added before `ner`).
- If only entity counts are needed for a pass, `select_pipes(enable="ner")`-style speedups are possible; but the aspect-opinion pass needs `parser`+`tagger`+`lemmatizer`, so keep one full pass and avoid disabling.
- On Netlify, `n_process>1` is limited by build container CPUs; start with `n_process=1` and tune (unverified for Netlify specifically).
