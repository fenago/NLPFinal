# spaCy Expert Knowledge — Index

Reference notes distilled from the official spaCy docs (spacy.io), fetched 2026-11-20, for the Customer Review Analyzer. spaCy runs ONLY at build time (not in Pyodide); outputs are static JSON/HTML/SVG.

**Read me first:** start with `02-en-core-web-sm.md` (what the model gives you and how to pin/install it), then `03-named-entities.md` + `06-entityruler.md` (people/places/brands/products) and `04-noun-chunks.md` + `05-dependency-parse.md` (aspects and aspect↔opinion pairs). Anything marked "(unverified)" was not confirmed on a fetched page — check with `spacy.explain(...)` or a local smoke test before relying on it. Each file ends with a "Project application" section.

| File | One-line summary |
| --- | --- |
| `01-pipelines.md` | `nlp.pipe` batching (`batch_size`, `n_process`, `as_tuples`), disable vs exclude, `select_pipes`, `pipe_names`, `add_pipe(before/after/first/last)`. |
| `02-en-core-web-sm.md` | English model family, sm components and 18 NER labels, listed accuracy (ENTS_F 0.84), `spacy download` vs pip wheel URL, `spacy.load`, versions. |
| `03-named-entities.md` | `doc.ents`, `label_`, `start_char/end_char`, IOB, label scheme, `spacy.explain`, setting entities with `Span`/`char_span`. |
| `04-noun-chunks.md` | `doc.noun_chunks`, `root`/`root.dep_`/`root.head`, token attributes (`lemma_`, `pos_`, `dep_`, `is_stop`, `is_alpha`), chunk normalization. |
| `05-dependency-parse.md` | `head`, `children`, `lefts/rights`, `subtree`, dependency label list, aspect↔opinion rules (`amod`, `acomp`, `nsubj`, `neg`), DependencyMatcher. |
| `06-entityruler.md` | `entity_ruler` before `ner`, phrase vs token patterns, `overwrite_ents`, `add_patterns`, JSONL `to_disk`/`from_disk`, ids. |
| `07-displacy.md` | `displacy.render` for `ent`/`dep`/`span`, `jupyter=False`, `page=True`, `options` colors/ents, static HTML/SVG export. |

## Pages fetched
https://spacy.io/usage/processing-pipelines, https://spacy.io/models/en, https://spacy.io/usage/linguistic-features, https://spacy.io/api/entityruler, https://spacy.io/usage/rule-based-matching, https://spacy.io/usage/visualizers, https://spacy.io/api/top-level, https://spacy.io/api/doc, https://spacy.io/api/token, https://spacy.io/usage/models (all succeeded).

## Known gaps
- "Built-in entity types" glossary table on the linguistic-features page did not render in the scrape; label descriptions beyond ORG/GPE/MONEY are not quoted from docs.
- Meanings of `acomp`, `neg`, `advmod` come from the label list only (standard usage), not from an explanatory table on the fetched pages.
