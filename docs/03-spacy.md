# 03 — What spaCy Does Best in the Customer Review Analyzer

> Role in the app: **the "linguistic structure" engine.** spaCy owns named entities (people, places, brands, products), noun chunks (aspect candidates), lemmas, and dependency parsing (linking aspects to opinions).

Verified with **spaCy 3.8.18** + **`en_core_web_sm`** (≈15 MB installed) on Python 3.13, 2026‑11‑20.

---

## 1. Named entities — "who and what is mentioned"

`doc.ents` with the `en_core_web_sm` (or `_md`/`_lg`) model. Labels that matter for reviews:

| spaCy label | App category |
|---|---|
| `PERSON` | People (staff, chefs, reps) |
| `GPE`, `LOC`, `FAC` | Places (cities, malls, airports, restaurants as buildings) |
| `ORG` | Brands / companies / stores |
| `PRODUCT` | Products (often weak in `sm`; see EntityRuler) |
| `MONEY`, `DATE`, `TIME`, `QUANTITY` | Prices, visit dates, wait times |

### Verified smoke test (same review as doc 02)

```text
ents:   ('Sony','ORG') ('Best Buy','PERSON')  ← wrong  ('Chicago','GPE') ('Maria','PERSON')
missed: 'WH-1000XM5' (product model number)
```

The small model mislabels a famous retailer and misses the product. **Fix with an `EntityRuler`** placed *before* the statistical NER — a pattern list of brands/products (can be auto‑generated from the dataset's product metadata, e.g. Amazon `store`/`title` fields or Yelp business names):

```python
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([
    {"label": "ORG", "pattern": "Best Buy"},
    {"label": "PRODUCT", "pattern": [{"TEXT": {"REGEX": r"^[A-Z]{1,4}-?\d{2,5}[A-Z0-9]*$"}}]},
])
```

## 2. Noun chunks — key‑phrase / aspect candidates

`doc.noun_chunks` returned: `the Sony WH-1000XM5 headphones`, `Best Buy`, `Chicago`, `The noise cancelling`, `the battery life`, `Customer service rep Maria`.

Normalize for display/aggregation: drop determiners and pronouns, lemmatize, lowercase → `battery life`, `noise cancelling`, `customer service rep`. Counting normalized chunks across a corpus gives **"most‑discussed aspects"**, complementing NLTK's statistical collocations.

## 3. Lemmas — merge word variants

`token.lemma_` maps `headphones → headphone`, `ordered → order`, `was → be`. Use lemmas (not raw tokens) for aspect counts so "battery", "batteries" aggregate together. NLTK has `WordNetLemmatizer`, but it needs POS tags passed in; spaCy's is context‑aware and free once the doc is parsed.

## 4. Dependency parsing — aspect ↔ opinion

`token.dep_` and `token.head` let us attach opinion words to the thing they describe — the core of **aspect‑based sentiment**, which is what makes this more than a VADER demo. Two rules caught all three pairs in the test review:

| Pattern | Example | Rule |
|---|---|---|
| Adjectival modifier | "*amazing* noise cancelling" | `tok.dep_ == "amod"` → (head, tok) |
| Copular complement | "battery life was *disappointing*" | `tok.dep_ == "acomp"` → (nsubj of head, tok) |

```text
aspect-opinion: ('cancelling','amazing') ('life','disappointing') ('Maria','helpful')
```

Expand the subject to its full noun chunk (`life` → `battery life`), then score each opinion word with VADER → per‑aspect sentiment table. Also handle `neg` children ("was **not** helpful") by flipping the sign.

## 5. Reference code

```python
import spacy
nlp = spacy.load("en_core_web_sm")          # add EntityRuler as above
ENT_GROUPS = {"PERSON": "people", "GPE": "places", "LOC": "places", "FAC": "places",
              "ORG": "brands", "PRODUCT": "products"}

def chunk_for(tok):
    for nc in tok.doc.noun_chunks:
        if nc.start <= tok.i < nc.end:
            return " ".join(t.lemma_.lower() for t in nc if t.pos_ not in ("DET", "PRON"))
    return tok.lemma_.lower()

def spacy_analyze(text):
    doc = nlp(text)
    ents = {}
    for e in doc.ents:
        if e.label_ in ENT_GROUPS:
            ents.setdefault(ENT_GROUPS[e.label_], []).append(e.text)
    chunks = [chunk_for(nc.root) for nc in doc.noun_chunks if nc.root.pos_ != "PRON"]
    pairs = []
    for t in doc:
        neg = any(c.dep_ == "neg" for c in t.children) or any(c.dep_ == "neg" for c in t.head.children)
        if t.dep_ == "amod" and t.pos_ == "ADJ":
            pairs.append((chunk_for(t.head), t.text, neg))
        if t.dep_ == "acomp":
            for s in t.head.children:
                if s.dep_ in ("nsubj", "nsubjpass"):
                    pairs.append((chunk_for(s), t.text, neg))
    return {"entities": ents, "noun_chunks": chunks, "aspects": pairs,
            "lemmas": [t.lemma_ for t in doc if t.is_alpha and not t.is_stop]}
```

Performance: use `nlp.pipe(texts, batch_size=256)` for the dataset at build time; disable unused components if needed (`nlp.select_pipes`). `en_core_web_sm` handles thousands of reviews per minute on a single CPU — fine for a Netlify build on a few‑thousand‑review sample.

## 6. Division of labour with NLTK (why use both)

| Task | Owner | Why |
|---|---|---|
| Sentence split, tokens for counting | NLTK | Simple, available in the browser via Pyodide |
| Stopwords | NLTK | Editable list (keep negations) |
| Sentiment | NLTK VADER | No training, review‑tuned, browser‑capable |
| Frequencies, collocations | NLTK | `FreqDist`, PMI / likelihood‑ratio finders |
| Entities (people/places/brands/products) | spaCy | Statistical NER + EntityRuler |
| Noun chunks / aspects | spaCy | Needs a parser |
| Lemmas | spaCy | Context‑aware, no manual POS |
| Aspect ↔ opinion linking | spaCy deps + NLTK VADER | Structure from spaCy, polarity from VADER |

## 7. Gotchas

- **Model is a separate download** (`python -m spacy download en_core_web_sm`). In `requirements.txt` pin the wheel URL so builds are reproducible:
  `en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl`
- **spaCy does not run in Pyodide** (it is not in the Pyodide package list; its C‑extension deps — thinc, blis, cymem, preshed, murmurhash, srsly — have no official WebAssembly builds). See doc 05 for how the architecture handles this.
- `sm` model accuracy on brands/products is modest; `en_core_web_md`/`lg` are better but bigger (≈40 MB / ≈560 MB). `sm` + EntityRuler is the recommended trade‑off.
- Pin Python **3.12** at build time for widest spaCy wheel compatibility (3.13 also verified working).

## Sources

- spaCy linguistic features (NER, noun chunks, dependency parse): https://spacy.io/usage/linguistic-features
- EntityRuler: https://spacy.io/api/entityruler
- English models: https://spacy.io/models/en
- spaCy on PyPI: https://pypi.org/project/spacy/
- Pyodide package list (no spaCy): https://pyodide.org/en/stable/usage/packages-in-pyodide.html
