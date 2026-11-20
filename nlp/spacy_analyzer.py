"""spaCy analysis for the Netlify build (never runs in the browser).

Owner: spacy-expert. Reviewers: build-pipeline-engineer, qa-engineer.

- Named entities from ``en_core_web_sm`` plus an EntityRuler (placed **before** ``ner`` so the
  model respects its spans) loaded from ``data/entity_patterns.jsonl``; spaCy labels are mapped to
  the app groups people / places / brands / products (docs/data-contract.md).
- Aspects: noun chunks normalised to lemmas without determiners, pronouns or adjectives
  ("the short battery life" -> "battery life").
- Aspect-opinion pairs from the dependency parse: ``amod`` (an evaluative adjective, i.e. one with
  a VADER valence, modifying the aspect noun) and ``acomp`` + ``nsubj`` (copular "the fries were cold"); conjoined adjectives are included and a
  ``neg`` dependent flips the opinion ("was not good").
- Aspect sentiment = NLTK VADER on the opinion phrase; review sentiment with entity names masked
  = NLTK VADER on the text with entity spans replaced by a neutral word.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token

try:  # package import (pipeline/build.py, tests)
    from nlp import nltk_analyzer as na
except ImportError:  # pragma: no cover - flat import when nlp/ itself is on sys.path
    import nltk_analyzer as na  # type: ignore

MODEL = "en_core_web_sm"
LABEL_TO_GROUP = {"PERSON": "people", "GPE": "places", "LOC": "places", "FAC": "places",
                  "ORG": "brands", "PRODUCT": "products"}
GROUPS = ("people", "places", "brands", "products")
MASK_WORD = "entity"  # not in the VADER lexicon, so it scores 0
_ASPECT_POS = {"NOUN", "PROPN"}
_COPULA_LEMMAS = {"be", "seem", "look", "taste", "smell", "feel", "sound", "remain", "get", "become", "stay"}
_BAD_ASPECTS = {"thing", "lot", "bit", "way", "time", "one", "kind", "sort", "place"}


def load_patterns(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def build_nlp(patterns_path: str | Path | None = None, use_ruler: bool = True, model: str = MODEL) -> Language:
    """Load the model and (optionally) add the EntityRuler before ``ner``."""
    nlp = spacy.load(model)
    if use_ruler and patterns_path:
        ruler = nlp.add_pipe("entity_ruler", before="ner",
                             config={"phrase_matcher_attr": "LOWER", "validate": True})
        with nlp.select_pipes(enable=[]):  # LOWER phrase patterns only need the tokenizer (avoids W012)
            ruler.add_patterns(load_patterns(patterns_path))
    return nlp


# ---------------------------------------------------------------- entities

def _is_noise(ent: Span) -> bool:
    """Drop obvious statistical-NER mistakes seen in Yelp text (ruler spans are never dropped)."""
    if ent.ent_id_:
        return False
    text = ent.text.strip()
    if "\n" in text or not any(ch.isalpha() for ch in text):
        return True
    if text[-1] in "&-/(" or text[0] in "&-/(":
        return True
    # Shouted single words ("AWESOME", "UNACCEPTABLE") get tagged ORG; short acronyms too (BBQ, ATM).
    if ent.label_ in ("ORG", "PRODUCT", "FAC", "PERSON") and len(ent) == 1 and text.isupper():
        return True
    # Lowercase single common nouns tagged as names ("mayo", "fig").
    if ent.label_ in LABEL_TO_GROUP and text.islower():
        return True
    return False


def entities(doc: Doc) -> list[dict]:
    out = []
    for ent in doc.ents:
        if _is_noise(ent):
            continue
        out.append({"text": ent.text, "label": ent.label_, "group": LABEL_TO_GROUP.get(ent.label_),
                    "start": ent.start_char, "end": ent.end_char,
                    "source": "ruler" if ent.ent_id_ else "ner"})
    return out


def entity_key(ent: dict, doc_text: str | None = None) -> str:
    """Normalised leaderboard key: lowercase, no leading 'the', no possessive 's."""
    t = ent["text"].strip().lower()
    if t.startswith("the "):
        t = t[4:]
    for suf in ("'s", "’s", "'"):
        if t.endswith(suf):
            t = t[: -len(suf)]
    return " ".join(t.split())


def masked_sentiment(doc: Doc, ents: list[dict]) -> dict:
    """VADER on the review with people/places/brands/products replaced by a neutral word."""
    text = doc.text
    for e in sorted((e for e in ents if e["group"]), key=lambda e: e["start"], reverse=True):
        text = text[: e["start"]] + MASK_WORD + text[e["end"]:]
    return na.sentiment(text)


# ------------------------------------------------------------------ aspects

def _chunk_of(token: Token) -> Span | None:
    for chunk in token.doc.noun_chunks:
        if chunk.start <= token.i < chunk.end:
            return chunk
    return None


def normalise_chunk(tokens: Iterable[Token]) -> str:
    """Lemmas of the nouns (and noun compounds) of a chunk: 'The short battery life' -> 'battery life'."""
    words = [t.lemma_.lower() for t in tokens if t.pos_ in _ASPECT_POS and t.is_alpha and not t.is_stop]
    return " ".join(words)


def aspect_term(noun: Token) -> str:
    """Aspect for a head noun: its compounds + itself, normalised (falls back to the noun chunk)."""
    parts = [c for c in noun.lefts if c.dep_ == "compound"] + [noun]
    term = normalise_chunk(parts)
    if not term:
        chunk = _chunk_of(noun)
        term = normalise_chunk(chunk) if chunk is not None else ""
    return term


def noun_chunk_aspects(doc: Doc) -> list[str]:
    out = []
    for chunk in doc.noun_chunks:
        if chunk.root.pos_ == "PRON":
            continue
        term = normalise_chunk(chunk)
        if term:
            out.append(term)
    return out


def _has_neg(tok: Token) -> bool:
    return any(c.dep_ == "neg" for c in tok.children)


def _opinion_phrase(adj: Token) -> str:
    mods = [c.text.lower() for c in adj.lefts if c.dep_ == "advmod" and c.pos_ == "ADV" and c.is_alpha]
    return " ".join(mods + [adj.text.lower()])


def _is_opinion(adj: Token) -> bool:
    """Evaluative adjective = has a VADER valence (word or lemma). Filters classifier adjectives in
    amod pairs ("french fries", "iced tea", "same day", "few minutes"); see reports/evaluation.md."""
    return na.valence(adj.text) != 0.0 or na.valence(adj.lemma_) != 0.0


def _pair(aspect: str, adj: Token, negated: bool, rule: str, sent_index: int) -> dict:
    opinion = _opinion_phrase(adj)
    s = na.sentiment(("not " if negated else "") + opinion)
    return {"aspect": aspect, "opinion": opinion, "negated": negated, "rule": rule,
            "compound": s["compound"], "label": s["label"], "sentence_index": sent_index}


def aspect_pairs(doc: Doc) -> list[dict]:
    """Aspect-opinion pairs from the dependency parse (amod; acomp + nsubj; neg flips)."""
    sent_index = {s.start: i for i, s in enumerate(doc.sents)}
    pairs, seen = [], set()

    def sidx(tok: Token) -> int:
        return sent_index[tok.sent.start]

    def add(noun: Token, adj: Token, negated: bool, rule: str) -> None:
        if noun.pos_ not in _ASPECT_POS or noun.ent_type_ in ("PERSON",):
            return
        aspect = aspect_term(noun)
        if not aspect or aspect in _BAD_ASPECTS:
            return
        key = (noun.i, adj.i)
        if key in seen:
            return
        seen.add(key)
        pairs.append(_pair(aspect, adj, negated, rule, sidx(adj)))

    for tok in doc:
        if tok.pos_ != "ADJ":
            continue
        if tok.dep_ == "amod" and tok.head.pos_ in _ASPECT_POS and _is_opinion(tok):
            noun = tok.head
            negated = _has_neg(tok) or (noun.dep_ in ("attr", "dobj") and _has_neg(noun.head))
            add(noun, tok, negated, "amod")
        elif tok.dep_ == "acomp" and tok.head.lemma_ in _COPULA_LEMMAS:
            verb = tok.head
            subjects = [c for c in verb.children if c.dep_ in ("nsubj", "nsubjpass")]
            negated = _has_neg(verb) or _has_neg(tok)
            for subj in subjects:
                nouns = [subj] + [c for c in subj.conjuncts if c.pos_ in _ASPECT_POS]
                adjs = [tok] + [c for c in tok.conjuncts if c.pos_ == "ADJ"]
                for n in nouns:
                    for a in adjs:
                        add(n, a, negated, "acomp")
    pairs.sort(key=lambda p: (p["sentence_index"], p["aspect"], p["opinion"]))
    return pairs


# ------------------------------------------------------------------ public

def analyze_doc(doc: Doc, full: bool = False) -> dict:
    ents = entities(doc)
    out = {"entities": ents, "aspects": aspect_pairs(doc), "masked_sentiment": masked_sentiment(doc, ents)}
    if full:
        out["noun_chunks"] = noun_chunk_aspects(doc)
        out["tokens"] = [{"i": t.i, "text": t.text, "lemma": t.lemma_, "pos": t.pos_, "dep": t.dep_,
                          "head": t.head.i} for t in doc]
    return out


def analyze_texts(nlp: Language, texts: list[str], full: bool = False, batch_size: int = 32) -> list[dict]:
    return [analyze_doc(doc, full=full) for doc in nlp.pipe(texts, batch_size=batch_size)]
