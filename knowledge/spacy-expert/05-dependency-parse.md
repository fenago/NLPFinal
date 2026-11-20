# 05 — Dependency Parse Navigation

Sources:
- https://spacy.io/usage/linguistic-features#dependency-parse (and #navigating)
- https://spacy.io/api/token (head, children, lefts, rights, subtree, ancestors, left_edge, right_edge, conjuncts)
- https://spacy.io/models/en (dependency label list for en_core_web_sm)
- https://spacy.io/usage/rule-based-matching#dependencymatcher

Fetched: 2026-11-20

## Concepts
- **head** and **child** = two words joined by a single arc; **dep** = the arc label (relation of the child to its head). `token.dep` is a hash; `token.dep_` is the string.
- Every token has **exactly one head**; the sentence root has `dep_ == "ROOT"` and is its own head (`token.head == token`).
- Parser also drives sentence boundaries and noun chunks. Needs `parser`; check with `doc.has_annotation("DEP")`. Disabling the parser makes loading/running much faster but removes all of this.

## Navigation API (Token)
| API | Returns |
| --- | --- |
| `token.head` | syntactic parent token |
| `token.children` | immediate children (`child.head == token`) |
| `token.lefts` / `token.rights` | immediate children before / after the token, in sentence order |
| `token.n_lefts` / `token.n_rights` | counts of those |
| `token.subtree` | token + all descendants, ordered |
| `token.ancestors` | parents, grandparents, ... |
| `token.is_ancestor(other)` | dominance check |
| `token.left_edge` / `token.right_edge` | first/last token of the subtree (right_edge is *inside* the subtree: slice with `+1`) |
| `token.conjuncts` | tuple of coordinated tokens, excluding itself |

```python
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
for t in doc:
    print(t.text, t.dep_, t.head.text, t.head.pos_, [c for c in t.children])
```
Docs' output excerpt: `Autonomous amod cars NOUN`; `cars nsubj shift VERB [Autonomous]`; `shift ROOT shift VERB [cars, liability, toward]`; `insurance compound liability NOUN`; `liability dobj shift VERB`; `toward prep shift ... [manufacturers]`; `manufacturers pobj toward ADP`.

```python
doc = nlp("bright red apples on the tree")
[t.text for t in doc[2].lefts]    # ['bright', 'red']
[t.text for t in doc[2].rights]   # ['on']
```
Phrase from a head: `span = doc[tok.left_edge.i : tok.right_edge.i + 1]`.

### Match from below (docs recommendation)
```python
from spacy.symbols import nsubj, VERB
verbs = {t.head for t in doc if t.dep == nsubj and t.head.pos == VERB}
```
Iterating every token and testing its own `dep_` + `head` is simpler than iterating heads and then children.

## Dependency labels in en_core_web_sm (full list from the models page)
`ROOT, acl, acomp, advcl, advmod, agent, amod, appos, attr, aux, auxpass, case, cc, ccomp, compound, conj, csubj, csubjpass, dative, dep, det, dobj, expl, intj, mark, meta, neg, nmod, npadvmod, nsubj, nsubjpass, nummod, oprd, parataxis, pcomp, pobj, poss, preconj, predet, prep, prt, punct, quantmod, relcl, xcomp`

Labels most useful for opinions/aspects (grammatical roles; docs only list the labels, the meanings below are standard ClearNLP-style usage and shown in docs' examples where noted):
| Label | Typical meaning | Example |
| --- | --- | --- |
| `amod` | adjectival modifier of a noun | *amazing* → noise cancelling (docs example: `Autonomous amod cars`) |
| `acomp` | adjectival complement of a (copular) verb | "battery life was *disappointing*" (meaning unverified from page) |
| `nsubj` / `nsubjpass` | (passive) subject | `cars nsubj shift` |
| `dobj` | direct object | `liability dobj shift` |
| `pobj` | object of a preposition | `manufacturers pobj toward` |
| `attr` | attribute after copula | `This is a sentence` → sentence `attr` (docs displaCy manual data) |
| `neg` | negation (e.g. "not", "n't") (unverified from page) | "was *not* good" |
| `advmod` | adverbial modifier ("very", "really") (unverified from page) | |
| `compound` | noun compound part | `insurance compound liability` |
| `conj` / `cc` | conjunct / coordinating conjunction | `account conj`, `and cc` |
| `prep`, `aux`, `poss`, `ROOT` | prepositional modifier; auxiliary; possessive; root | seen in docs tables |
Run `spacy.explain("acomp")` at build time to confirm any label description.

## Aspect ↔ opinion extraction (from project docs/03-spacy.md, built on these APIs)
```python
pairs = []
for tok in doc:
    # 1) adjectival modifier: "amazing noise cancelling"
    if tok.dep_ == "amod" and tok.head.pos_ in ("NOUN", "PROPN"):
        pairs.append((tok.head, tok))
    # 2) copular complement: "battery life was disappointing"
    elif tok.dep_ == "acomp":
        subj = [c for c in tok.head.children if c.dep_ in ("nsubj", "nsubjpass")]
        if subj:
            pairs.append((subj[0], tok))
# negation: any child with dep_ == "neg" flips polarity
negated = any(c.dep_ == "neg" for c in tok.children) or any(c.dep_ == "neg" for c in tok.head.children)
```
- Handle coordination: `tok.conjuncts` ("great screen and speaker").
- Expand the aspect to its compound: include children with `dep_ == "compound"` ("battery life").

## DependencyMatcher (declarative alternative)
- `spacy.matcher.DependencyMatcher` matches subtrees via Semgrex-style operators; first pattern node has only `RIGHT_ID` + `RIGHT_ATTRS`, later nodes add `LEFT_ID`, `REL_OP`, `RIGHT_ID`, `RIGHT_ATTRS`. Key operators: `A > B` (A is immediate head of B), `A < B` (A immediate dependent of B), `>>`/`<<` (chains).
Pattern shape (keys per the docs): `[{"RIGHT_ID": "anchor", "RIGHT_ATTRS": {...}}, {"LEFT_ID": "anchor", "REL_OP": ">", "RIGHT_ID": "child", "RIGHT_ATTRS": {"DEP": "amod"}}, ...]`; register with `matcher.add("NAME", [pattern])`.
Needs the parser. The loop above is easier to debug for a small project.

## Project application
- Core of aspect-based sentiment: `(aspect_lemma, opinion_lemma, negated, sentence_idx)` tuples per review; pass the covering sentence (`tok.sent.text`) to VADER for polarity; aggregate per aspect.
- Dependency accuracy of sm is DEP_LAS 0.90 on news-like text; informal, run-on, or all-caps reviews degrade it — keep rules conservative and cap output.
- Use `displacy` (`07-displacy.md`) to debug misparses on sample reviews at build time.
