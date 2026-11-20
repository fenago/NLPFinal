"""Evaluation for reports/evaluation.md. Owner: nlp-evaluator.

  python scripts/evaluate.py --dump     # write candidates to judge into reports/annotations/*.jsonl
  python scripts/evaluate.py            # compute metrics (VADER vs stars; judged entity + aspect precision)

The aspect-pair sample in reports/annotations/aspect_pairs.jsonl was drawn and judged BEFORE the
amod opinion filter and the VADER domain lexicon were added (baseline: annotations/baseline_metrics.json);
the "aspects_current_on_judged" block re-scores those same pairs with the current pipeline.

Sampling is deterministic (seed 13). Judgements live in reports/annotations/ with a `correct`
field filled in by hand; entities are judged once per (review, span, group) so the with- and
without-EntityRuler runs share one set of judgements.
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ANN = ROOT / "reports/annotations"
LABELS = ["negative", "neutral", "positive"]
SEED = 13
N_ENTITY_REVIEWS = 30
N_PAIRS = 30


def expected(stars: int) -> str:
    return "negative" if stars <= 2 else ("neutral" if stars == 3 else "positive")


def metrics(gold: list[str], pred: list[str], labels=LABELS) -> dict:
    cm = [[sum(1 for g, p in zip(gold, pred) if g == a and p == b) for b in labels] for a in labels]
    per = {}
    for i, l in enumerate(labels):
        tp = cm[i][i]
        fp = sum(cm[j][i] for j in range(len(labels))) - tp
        fn = sum(cm[i]) - tp
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        per[l] = {"precision": prec, "recall": rec, "f1": f1, "support": sum(cm[i])}
    acc = sum(cm[i][i] for i in range(len(labels))) / len(gold)
    return {"accuracy": acc, "macro_f1": sum(v["f1"] for v in per.values()) / len(labels), "per_class": per, "confusion": cm}


def load():
    from nlp import nltk_analyzer as na, spacy_analyzer as sa
    na.configure(str(ROOT / "nltk_data"))
    rows = [json.loads(l) for l in (ROOT / "data/reviews_sample.jsonl").read_text().splitlines() if l.strip()]
    return na, sa, rows


def run_spacy(sa, rows):
    with_r = sa.analyze_texts(sa.build_nlp(ROOT / "data/entity_patterns.jsonl"), [r["text"] for r in rows])
    without = sa.analyze_texts(sa.build_nlp(None, use_ruler=False), [r["text"] for r in rows])
    return with_r, without


def entity_sample(rows):
    rng = random.Random(SEED)
    return sorted(rng.sample(range(len(rows)), N_ENTITY_REVIEWS))


def ctx(text, s, e, w=45):
    return (text[max(0, s - w):s] + "[[" + text[s:e] + "]]" + text[e:e + w]).replace("\n", " ")


def dump(na, sa, rows):
    ANN.mkdir(parents=True, exist_ok=True)
    with_r, without = run_spacy(sa, rows)
    seen, out = set(), []
    for i in entity_sample(rows):
        for run in (with_r, without):
            for e in run[i]["entities"]:
                if not e["group"]:
                    continue
                key = (rows[i]["id"], e["start"], e["end"], e["group"])
                if key in seen:
                    continue
                seen.add(key)
                out.append({"review_id": rows[i]["id"], "start": e["start"], "end": e["end"], "text": e["text"],
                            "label": e["label"], "group": e["group"], "context": ctx(rows[i]["text"], e["start"], e["end"]),
                            "correct": None})
    path = ANN / "entities.jsonl"
    old = {}
    if path.exists():
        for l in path.read_text().splitlines():
            d = json.loads(l)
            old[(d["review_id"], d["start"], d["end"], d["group"])] = d
    with path.open("w") as f:
        for d in out:
            prev = old.get((d["review_id"], d["start"], d["end"], d["group"]))
            if prev:
                d["correct"], d["note"] = prev["correct"], prev.get("note", "")
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    pairs = [(rows[i]["id"], p, rows[i]["text"]) for i, s in enumerate(with_r) for p in s["aspects"]]
    rng = random.Random(SEED)
    picked = rng.sample(pairs, N_PAIRS)
    with (ANN / "aspect_pairs.jsonl").open("w") as f:
        for rid, p, text in picked:
            f.write(json.dumps({"review_id": rid, **p, "correct_pair": None, "correct_polarity": None}, ensure_ascii=False) + "\n")
    print(f"wrote {len(out)} entity candidates and {len(picked)} aspect pairs to {ANN}")


def report(na, sa, rows):
    out = {}
    gold = [expected(r["stars"]) for r in rows]
    raw = [na.sentiment(r["text"])["label"] for r in rows]
    with_r, without = run_spacy(sa, rows)
    masked = [s["masked_sentiment"]["label"] for s in with_r]
    out["vader_raw"] = metrics(gold, raw)
    out["vader_masked"] = metrics(gold, masked)
    changed = [(rows[i]["id"], raw[i], masked[i]) for i in range(len(rows)) if raw[i] != masked[i]]
    out["masked_changed"] = changed
    # binary view (1-2 vs 4-5 stars, 3 stars dropped; VADER neutral counts as wrong)
    idx = [i for i, r in enumerate(rows) if r["stars"] != 3]
    out["binary_raw_acc"] = sum(raw[i] == gold[i] for i in idx) / len(idx)
    out["binary_n"] = len(idx)
    # thresholds sweep: is a higher positive threshold better on long reviews?
    comp = [na.sentiment(r["text"])["compound"] for r in rows]
    sweep = {}
    for t in (0.05, 0.3, 0.5, 0.7):
        pred = ["positive" if c >= t else "negative" if c <= -0.05 else "neutral" for c in comp]
        m = metrics(gold, pred)
        sweep[t] = (m["accuracy"], m["macro_f1"])
    out["threshold_sweep"] = sweep
    # error analysis material: most confident misses
    misses = sorted(((abs(comp[i]), rows[i]["id"], rows[i]["stars"], comp[i], rows[i]["text"][:160].replace("\n", " "))
                     for i in range(len(rows)) if raw[i] != gold[i] and gold[i] != "neutral"), reverse=True)[:6]
    out["top_misses"] = misses

    ents = [json.loads(l) for l in (ANN / "entities.jsonl").read_text().splitlines()]
    judged = {(d["review_id"], d["start"], d["end"], d["group"]): d["correct"] for d in ents}
    sample = entity_sample(rows)
    for name, run in (("with_ruler", with_r), ("without_ruler", without)):
        n = ok = 0
        by_group = collections.defaultdict(lambda: [0, 0])
        for i in sample:
            for e in run[i]["entities"]:
                if not e["group"]:
                    continue
                c = judged[(rows[i]["id"], e["start"], e["end"], e["group"])]
                assert c is not None, f"unjudged entity {e}"
                n += 1; ok += bool(c)
                by_group[e["group"]][0] += 1; by_group[e["group"]][1] += bool(c)
        out[f"entities_{name}"] = {"n": n, "precision": ok / n if n else 0.0, "correct": ok,
                                   "by_group": {g: {"n": v[0], "correct": v[1], "precision": v[1] / v[0]} for g, v in sorted(by_group.items())}}
    # recall proxy: correct spans found by either run = pooled gold
    pooled = {k for k, c in judged.items() if c}
    for name, run in (("with_ruler", with_r), ("without_ruler", without)):
        found = {(rows[i]["id"], e["start"], e["end"], e["group"]) for i in sample for e in run[i]["entities"] if e["group"]}
        out[f"entities_{name}"]["pooled_recall"] = len(found & pooled) / len(pooled) if pooled else 0.0
    out["entities_pooled_gold"] = len(pooled)

    pairs = [json.loads(l) for l in (ANN / "aspect_pairs.jsonl").read_text().splitlines()]
    assert all(p["correct_pair"] is not None for p in pairs), "unjudged aspect pairs"
    good = [p for p in pairs if p["correct_pair"]]
    out["aspects"] = {"n": len(pairs), "pair_precision": len(good) / len(pairs),
                      "polarity_acc_on_correct": sum(p["label"] == p["human_polarity"] for p in good) / len(good) if good else 0.0,
                      "end_to_end": sum(p["label"] == p["human_polarity"] for p in good) / len(pairs),
                      "by_rule": {r: f"{sum(bool(p['correct_pair']) for p in pairs if p['rule'] == r)}/{sum(1 for p in pairs if p['rule'] == r)}" for r in ("amod", "acomp")}}
    # Same judged pairs, current pipeline: which survive the amod opinion filter, and their polarity now.
    cur = {rows[i]["id"]: with_r[i]["aspects"] for i in range(len(rows))}
    kept = [p for p in pairs if any(q["aspect"] == p["aspect"] and q["opinion"] == p["opinion"] for q in cur[p["review_id"]])]
    def now_label(p):
        return next(q["label"] for q in cur[p["review_id"]] if q["aspect"] == p["aspect"] and q["opinion"] == p["opinion"])
    kept_ok = [p for p in kept if p["correct_pair"]]
    out["aspects_current_on_judged"] = {
        "retained": len(kept), "retained_correct": len(kept_ok),
        "pair_precision": len(kept_ok) / len(kept) if kept else 0.0,
        "correct_pairs_lost": sum(1 for p in pairs if p["correct_pair"]) - len(kept_ok),
        "polarity_acc_on_correct": sum(now_label(p) == p["human_polarity"] for p in kept_ok) / len(kept_ok) if kept_ok else 0.0,
        "end_to_end": sum(now_label(p) == p["human_polarity"] for p in kept_ok) / len(kept) if kept else 0.0,
    }
    out["aspect_pairs_total"] = sum(len(a) for a in cur.values())
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", action="store_true")
    a = ap.parse_args()
    na, sa, rows = load()
    dump(na, sa, rows) if a.dump else report(na, sa, rows)
