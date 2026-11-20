"""Unit tests for nlp/spacy_analyzer.py (owner: spacy-expert)."""


def test_ruler_runs_before_ner(nlp):
    names = nlp.pipe_names
    assert names.index("entity_ruler") < names.index("ner")


def test_entity_groups_and_ruler(nlp, sa):
    doc = nlp("Sarah from Starbucks in Chicago loved the Big Mac and her new XR-500.")
    ents = {e["text"]: e for e in sa.entities(doc)}
    assert ents["Starbucks"]["group"] == "brands" and ents["Starbucks"]["source"] == "ruler"
    assert ents["Big Mac"]["group"] == "products" and ents["Big Mac"]["source"] == "ruler"
    assert ents["XR-500"]["group"] == "products"
    assert ents["Chicago"]["group"] == "places"
    assert ents["Sarah"]["group"] == "people"


def test_ruler_is_case_insensitive(nlp, sa):
    ents = sa.entities(nlp("we went to starbucks and then papa j's"))
    assert {e["text"].lower() for e in ents if e["source"] == "ruler"} >= {"starbucks", "papa j's"}


def test_noise_filter_drops_shouted_words(nlp, sa):
    ents = sa.entities(nlp("The food was AWESOME and the staff were UNACCEPTABLE."))
    assert not [e for e in ents if e["text"] in ("AWESOME", "UNACCEPTABLE")]


def test_amod_pair(nlp, sa):
    pairs = sa.aspect_pairs(nlp("They serve a delicious fish sandwich."))
    assert any(p["aspect"] == "fish sandwich" and p["opinion"] == "delicious" and p["rule"] == "amod"
               and p["label"] == "positive" for p in pairs)


def test_acomp_pair_with_negation_flip(nlp, sa):
    pairs = sa.aspect_pairs(nlp("The battery life is not great."))
    p = next(p for p in pairs if p["aspect"] == "battery life")
    assert p["rule"] == "acomp" and p["negated"] is True and p["label"] == "negative"


def test_conjoined_adjectives(nlp, sa):
    pairs = sa.aspect_pairs(nlp("The staff were friendly and helpful."))
    assert {p["opinion"] for p in pairs if p["aspect"] == "staff"} == {"friendly", "helpful"}


def test_noun_chunk_normalisation(nlp, sa):
    assert sa.noun_chunk_aspects(nlp("The short battery life annoyed me.")) == ["battery life"]


def test_masked_sentiment_removes_name_polarity(nlp, sa):
    doc = nlp("I picked it up at Best Buy.")
    ents = sa.entities(doc)
    raw = sa.na.sentiment(doc.text)["compound"]
    masked = sa.masked_sentiment(doc, ents)["compound"]
    assert raw > 0 and masked == 0.0  # "Best" is a name here, not praise


def test_full_output_has_tokens(nlp, sa):
    out = sa.analyze_doc(nlp("Great pizza."), full=True)
    assert {"noun_chunks", "tokens"} <= set(out)
    assert out["tokens"][0]["lemma"] == "great"
