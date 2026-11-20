# 04 — Noun Chunks and Token Attributes

Sources:
- https://spacy.io/usage/linguistic-features#noun-chunks (also #pos-tagging, #lemmatization)
- https://spacy.io/api/doc (Doc.noun_chunks)
- https://spacy.io/api/token (Token attributes)

Fetched: 2026-11-20

## Noun chunks
- `doc.noun_chunks` iterates **base noun phrases** as `Span`s. Requires a dependency parse (the `parser`); if the language has no noun-chunk iterator, `NotImplementedError` is raised.
- Docs definition: a base noun phrase / "NP chunk" is a flat phrase with a noun as head; no nested NPs, so no NP-level coordination, no prepositional phrases, no relative clauses. Think "noun plus words describing the noun" (e.g. "the lavish green grass").
- Customize via `nlp.vocab.get_noun_chunks` (per the Doc API page).
- Check a parse exists: `doc.has_annotation("DEP")`.

```python
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)
```
Docs' output:
| chunk | root.text | root.dep_ | root.head.text |
| --- | --- | --- | --- |
| Autonomous cars | cars | `nsubj` | shift |
| insurance liability | liability | `dobj` | shift |
| manufacturers | manufacturers | `pobj` | toward |

- `chunk.root` = the head token of the chunk; `chunk.root.dep_` = its relation to the rest of the sentence; `chunk.root.head` = what it attaches to (often the verb — useful to find what is being said about the aspect).
- Span extras used in practice: `chunk.start`, `chunk.end`, `chunk.start_char`, `chunk.end_char`, `chunk.text`, iterate tokens in the chunk.

## Token attributes you will use (from the Token API page)
Add `_` for the string version (spaCy stores hashes; `token.lemma` is an int, `token.lemma_` a str).
| Attribute | Meaning |
| --- | --- |
| `text`, `text_with_ws`, `idx` | verbatim text; with trailing space; character offset in the doc |
| `i` | token index in the doc |
| `lemma_` | base form with no inflectional suffixes |
| `lower_` | lowercase text |
| `pos_` | coarse Universal POS tag (`NOUN`, `PROPN`, `VERB`, `ADJ`, `AUX`, `ADP`, `NUM`, `SYM`, ...) |
| `tag_` | fine-grained (Penn-style) tag (`NN`, `NNP`, `VBG`, `JJ`, ...) |
| `dep_` | syntactic dependency relation of this token to its head |
| `head` | syntactic parent ("governor") token |
| `is_stop` | in the stop list |
| `is_alpha` | all alphabetic (`text.isalpha()`) — False for "U.K.", "$", "1" |
| `is_punct`, `is_space`, `is_digit`, `like_num`, `is_currency` | other flags |
| `shape_` | orthographic shape (`Xxxxx`, `dd`, ...) |
| `ent_type_`, `ent_iob_` | entity label / IOB for the token |
| `sent` | the sentence `Span` containing the token |

Docs' example row output (`Apple is looking at buying U.K. startup for $1 billion`): `Apple apple PROPN NNP nsubj Xxxxx alpha=True stop=False`; `is be AUX VBZ aux xx True True`; `U.K. u.k. PROPN NNP compound X.X. False False`.

## Lemmatization (English)
- `lemmatizer` component is rule-based for English (`nlp.get_pipe("lemmatizer").mode == 'rule'`); needs POS from tagger/attribute_ruler to work well.
- Docs example: `"I was reading the paper."` → `['I', 'be', 'read', 'the', 'paper', '.']`.
- Lookup data comes from the `spacy-lookups-data` package; trained pipelines already include the tables.

## Normalizing chunks for aggregation (pattern, project-level — not from docs)
```python
def normalize_chunk(chunk):
    toks = [t for t in chunk if not t.is_stop and not t.is_punct and t.pos_ not in ("DET", "PRON")]
    return " ".join(t.lemma_.lower() for t in toks) or None
```
Pitfall: `is_stop` removes words like "not"/"very"; fine for aspect nouns, wrong for opinion phrases (keep `neg`, see `05-dependency-parse.md`).

## Merging chunks
- `nlp.add_pipe("merge_noun_chunks")` (and `"merge_entities"`) are built-in components used in the docs' MONEY example to turn chunks/entities into single tokens before parse analysis. Merging is destructive to tokenization (changes `len(doc)`), so do it on a copy/separate pass.
- Or merge manually: `with doc.retokenize() as r: r.merge(span)`.

## Project application
- Aspect candidates = noun chunks whose root has `pos_` in `{NOUN, PROPN}`; aggregate by normalized lemma text ("battery life", "customer service") for "most-discussed aspects".
- Use `chunk.root.dep_` to filter: subjects (`nsubj`, `nsubjpass`) and objects (`dobj`, `pobj`) are the aspects people comment on; `chunk.root.head` links to the verb/preposition for aspect↔opinion extraction.
- Exclude chunks that are entities already captured (e.g. "Sony", "Chicago") by comparing spans against `doc.ents` — avoids double counting brands as aspects.
- Drop chunks whose normalized form is empty (pronouns like "I", "it") or generic ("thing", "one") using a small project stoplist.
