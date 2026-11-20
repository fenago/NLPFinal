"""Netlify build step: run NLTK + spaCy over the review sample and write static JSON.

Owner: build-pipeline-engineer. Reviewers: netlify-engineer, qa-engineer.

Usage:  python pipeline/build.py [--sample data/reviews_sample.jsonl] [--out site]

Writes (contract: docs/data-contract.md, schemas/*.schema.json):
  site/data/{meta,summary,reviews,collocations,aspects,entities,examples}.json
Copies for the browser (Pyodide runs the same NLTK code):
  nltk_data/ -> site/nltk_data/      nlp/nltk_analyzer.py -> site/py/nltk_analyzer.py
Python runs only here, at build time (netlify-guardrail): nothing in this file is served.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import platform
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONTRACT_VERSION = "1.0.0"
MAX_FILE_BYTES = 10 * 1024 * 1024  # Netlify CDN guidance: files over 10 MB may fail to upload
STARS = (1, 2, 3, 4, 5)
LABELS = ("negative", "neutral", "positive")
N_DATASET_EXAMPLES = 3
LEADERBOARD_SIZE = 25
MAX_ASPECTS = 40


def expected_label(stars: int) -> str:
    return "negative" if stars <= 2 else ("neutral" if stars == 3 else "positive")


def r3(x: float) -> float:
    return round(float(x), 3) + 0.0


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_json(path: Path, obj: dict) -> int:
    data = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    path.write_text(data + "\n", encoding="utf-8")
    return len(data.encode("utf-8")) + 1


class Timer:
    def __init__(self) -> None:
        self.t0 = self.last = time.perf_counter()

    def stage(self, name: str) -> None:
        now = time.perf_counter()
        print(f"[build] {name:<28} {now - self.last:6.2f}s", flush=True)
        self.last = now


# --------------------------------------------------------------- aggregates

def summarise(reviews: list[dict]) -> dict:
    stars_counts = collections.Counter(r["stars"] for r in reviews)
    sent_counts = collections.Counter(r["nltk"]["sentiment"]["label"] for r in reviews)
    by_star: dict[int, list[float]] = collections.defaultdict(list)
    matrix = [[0, 0, 0] for _ in STARS]
    hist = [0] * 10
    correct = 0
    for r in reviews:
        c = r["nltk"]["sentiment"]["compound"]
        lab = r["nltk"]["sentiment"]["label"]
        by_star[r["stars"]].append(c)
        matrix[r["stars"] - 1][LABELS.index(lab)] += 1
        hist[min(int((c + 1) / 0.2), 9)] += 1
        correct += lab == expected_label(r["stars"])
    return {
        "contract_version": CONTRACT_VERSION,
        "n_reviews": len(reviews),
        "stars_counts": {str(s): stars_counts.get(s, 0) for s in STARS},
        "sentiment_counts": {lab: sent_counts.get(lab, 0) for lab in LABELS},
        "mean_compound_by_stars": {str(s): (r3(sum(by_star[s]) / len(by_star[s])) if by_star[s] else None) for s in STARS},
        "vader_vs_stars": {"stars": list(STARS), "labels": list(LABELS), "counts": matrix},
        "compound_histogram": {"bin_edges": [r3(-1 + 0.2 * i) for i in range(11)], "counts": hist},
        "accuracy_vs_stars": r3(correct / len(reviews)) if reviews else 0.0,
    }


def aggregate_aspects(reviews: list[dict]) -> dict:
    acc: dict[str, dict] = {}
    for r in reviews:
        for p in r["spacy"]["aspects"]:
            a = acc.setdefault(p["aspect"], {"compounds": [], "labels": collections.Counter(),
                                             "opinions": collections.Counter(), "ids": set()})
            a["compounds"].append(p["compound"])
            a["labels"][p["label"]] += 1
            a["opinions"][("not " if p["negated"] else "") + p["opinion"]] += 1
            a["ids"].add(r["id"])
    rows = []
    for name, a in acc.items():
        n = len(a["compounds"])
        if n < 2:
            continue
        rows.append({
            "aspect": name, "mentions": n, "mean_compound": r3(sum(a["compounds"]) / n),
            "positive": a["labels"]["positive"], "neutral": a["labels"]["neutral"], "negative": a["labels"]["negative"],
            "top_opinions": [{"word": w, "count": c} for w, c in sorted(a["opinions"].items(), key=lambda kv: (-kv[1], kv[0]))[:5]],
            "review_ids": sorted(a["ids"]),
        })
    rows.sort(key=lambda x: (-x["mentions"], x["aspect"]))
    return {"contract_version": CONTRACT_VERSION, "aspects": rows[:MAX_ASPECTS]}


def aggregate_entities(reviews: list[dict], entity_key) -> dict:
    groups: dict[str, dict] = {g: {} for g in ("people", "places", "brands", "products")}
    for r in reviews:
        for e in r["spacy"]["entities"]:
            if not e["group"]:
                continue
            key = entity_key(e)
            if not key:
                continue
            slot = groups[e["group"]].setdefault(key, {"surface": collections.Counter(), "count": 0, "ids": set(),
                                                       "sources": collections.Counter()})
            slot["surface"][e["text"].strip()] += 1
            slot["count"] += 1
            slot["ids"].add(r["id"])
            slot["sources"][e["source"]] += 1
    out = {}
    for g, items in groups.items():
        rows = [{
            "text": sorted(v["surface"].items(), key=lambda kv: (-kv[1], kv[0]))[0][0],
            "count": v["count"], "n_reviews": len(v["ids"]), "review_ids": sorted(v["ids"]),
            "sources": {"ner": v["sources"]["ner"], "ruler": v["sources"]["ruler"]},
        } for v in items.values()]
        rows.sort(key=lambda x: (-x["count"], -x["n_reviews"], x["text"].lower()))
        out[g] = rows[:LEADERBOARD_SIZE]
    return {"contract_version": CONTRACT_VERSION, "groups": out}


def pick_dataset_examples(reviews: list[dict], n: int) -> list[dict]:
    """Entity- and aspect-rich dataset reviews, one per star level where possible, short enough to read."""
    def richness(r: dict) -> tuple:
        grouped = sum(1 for e in r["spacy"]["entities"] if e["group"])
        return (-(grouped + len(r["spacy"]["aspects"])), r["id"])
    picked, used_stars = [], set()
    for r in sorted((r for r in reviews if len(r["text"]) <= 900), key=richness):
        if r["stars"] in used_stars:
            continue
        picked.append(r)
        used_stars.add(r["stars"])
        if len(picked) == n:
            break
    return picked


# ------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sample", type=Path, default=ROOT / "data/reviews_sample.jsonl")
    ap.add_argument("--patterns", type=Path, default=ROOT / "data/entity_patterns.jsonl")
    ap.add_argument("--demos", type=Path, default=ROOT / "data/demo_reviews.jsonl")
    ap.add_argument("--out", type=Path, default=ROOT / "site")
    args = ap.parse_args()

    timer = Timer()
    from nlp import nltk_analyzer as na
    from nlp import spacy_analyzer as sa
    import nltk
    import spacy

    na.configure(os.environ.get("NLTK_DATA_DIR", str(ROOT / "nltk_data")))
    timer.stage("import nltk + spacy")

    rows = read_jsonl(args.sample)
    demos = read_jsonl(args.demos) if args.demos.exists() else []
    nlp = sa.build_nlp(args.patterns)
    timer.stage(f"load model ({len(rows)} reviews)")

    texts = [r["text"] for r in rows]
    nltk_out = [na.analyze(t) for t in texts]
    timer.stage("NLTK per review")
    colloc = na.corpus_collocations(texts)
    timer.stage("NLTK collocations")
    spacy_out = sa.analyze_texts(nlp, texts)
    timer.stage("spaCy nlp.pipe")

    reviews = [{"id": r["id"], "stars": r["stars"], "text": r["text"], "nltk": n, "spacy": s}
               for r, n, s in zip(rows, nltk_out, spacy_out)]

    examples = []
    for d in demos:
        examples.append({"id": d["id"], "title": d["title"], "is_demo": True, "stars": None, "text": d["text"]})
    for r in pick_dataset_examples(reviews, N_DATASET_EXAMPLES):
        examples.append({"id": r["id"], "title": f"Dataset review {r['id']} ({r['stars']} stars)",
                         "is_demo": False, "stars": r["stars"], "text": r["text"]})
    full = sa.analyze_texts(nlp, [e["text"] for e in examples], full=True)
    for e, s in zip(examples, full):
        e["nltk"] = na.analyze(e["text"])
        e["spacy"] = s
    timer.stage("examples (full spaCy)")

    meta = {
        "contract_version": CONTRACT_VERSION,
        "dataset": {
            "name": "Yelp Review Full (sample)", "source": "https://huggingface.co/datasets/Yelp/yelp_review_full",
            "mode": "restaurant/business", "n_reviews": len(reviews),
            "license_note": "Yelp Dataset terms: academic and non-commercial use only.",
            "citation": "Zhang, Zhao & LeCun (2015). Character-level Convolutional Networks for Text Classification. NeurIPS 28.",
        },
        "versions": {"python": platform.python_version(), "nltk": nltk.__version__, "spacy": spacy.__version__,
                     "en_core_web_sm": nlp.meta.get("version", "unknown")},
        "sentiment_thresholds": {"positive": na.POSITIVE_THRESHOLD, "negative": na.NEGATIVE_THRESHOLD},
        "entity_groups": {g: sorted(l for l, gg in sa.LABEL_TO_GROUP.items() if gg == g) for g in sa.GROUPS},
        "commit": os.environ.get("COMMIT_REF") or None,
    }

    data_dir = args.out / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "meta.json": meta,
        "summary.json": summarise(reviews),
        "reviews.json": {"contract_version": CONTRACT_VERSION, "reviews": reviews},
        "collocations.json": {"contract_version": CONTRACT_VERSION, **colloc},
        "aspects.json": aggregate_aspects(reviews),
        "entities.json": aggregate_entities(reviews, sa.entity_key),
        "examples.json": {"contract_version": CONTRACT_VERSION, "examples": examples},
    }
    for name, obj in outputs.items():
        size = write_json(data_dir / name, obj)
        print(f"[build]   wrote data/{name:<18} {size / 1024:8.1f} KB")
    timer.stage("write site/data")

    # Browser copies: same NLTK module and data the build used.
    shutil.rmtree(args.out / "nltk_data", ignore_errors=True)
    shutil.copytree(ROOT / "nltk_data", args.out / "nltk_data",
                    ignore=shutil.ignore_patterns("README"))
    (args.out / "py").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "nlp/nltk_analyzer.py", args.out / "py/nltk_analyzer.py")
    timer.stage("copy nltk_data + analyzer")

    big = [(p.stat().st_size, p) for p in args.out.rglob("*") if p.is_file() and p.stat().st_size > MAX_FILE_BYTES]
    for size, p in big:
        print(f"[build] WARNING {p.relative_to(args.out)} is {size / 1e6:.1f} MB (> 10 MB Netlify guidance)", file=sys.stderr)
    files = [p for p in args.out.rglob("*") if p.is_file()]
    print(f"[build] site/: {len(files)} files, {sum(p.stat().st_size for p in files) / 1e6:.2f} MB; "
          f"total {time.perf_counter() - timer.t0:.1f}s; accuracy vs stars {outputs['summary.json']['accuracy_vs_stars']}")
    return 1 if big else 0


if __name__ == "__main__":
    sys.exit(main())
