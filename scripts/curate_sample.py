"""Build the committed review sample from the raw Yelp Review Full rows.

Owner: dataset-curator. Input: data/raw/yelp_rows.jsonl. Output: data/reviews_sample.jsonl.

Steps (documented in data/SOURCES.md):
1. Unescape the literal ``\\n`` and ``\\"`` sequences that the Yelp CSV export keeps in the text.
2. Scrub e-mail addresses, phone numbers and URLs (replaced by [EMAIL], [PHONE], [URL]).
3. Drop unusable rows: empty/very short text (< 20 chars) and exact duplicate texts.
4. Keep every usable review (the pool is only 200 rows, so balancing by down-sampling to the
   smallest class would leave about 130 reviews). Output is ordered by stars, then split, then row.

Usage: python scripts/curate_sample.py [--raw PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
URL_RE = re.compile(r"\b(?:https?://|www\.)\S+|\b[\w-]+\.(?:com|net|org|biz|info)(?:/\S*)?\b", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\w)")
MIN_CHARS = 20


def clean(text: str) -> str:
    text = text.replace("\\n", "\n").replace('\\"', '"').replace("\\t", " ")
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = URL_RE.sub("[URL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=ROOT / "data/raw/yelp_rows.jsonl", type=Path)
    ap.add_argument("--out", default=ROOT / "data/reviews_sample.jsonl", type=Path)
    args = ap.parse_args()

    rows = [json.loads(line) for line in args.raw.read_text(encoding="utf-8").splitlines() if line.strip()]
    seen: set[str] = set()
    kept, dropped = [], collections.Counter()
    scrubbed = collections.Counter()
    for r in rows:
        raw = r["text"]
        text = clean(raw)
        for tag in ("[EMAIL]", "[URL]", "[PHONE]"):
            scrubbed[tag] += text.count(tag)
        if len(text) < MIN_CHARS:
            dropped["too_short"] += 1
            continue
        key = re.sub(r"\s+", " ", text.lower())
        if key in seen:
            dropped["duplicate"] += 1
            continue
        seen.add(key)
        kept.append({
            "id": f"yelp-{r['split']}-{int(r['row_idx']):03d}",
            "stars": int(r["label"]) + 1,
            "text": text,
            "source": {"dataset": "Yelp/yelp_review_full", "split": r["split"], "row_idx": int(r["row_idx"])},
        })
    kept.sort(key=lambda x: (x["stars"], x["source"]["split"], x["source"]["row_idx"]))
    with args.out.open("w", encoding="utf-8") as f:
        for k in kept:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    print(f"raw={len(rows)} kept={len(kept)} dropped={dict(dropped)} scrubbed={dict(scrubbed)}")
    print("stars:", dict(sorted(collections.Counter(k["stars"] for k in kept).items())))


if __name__ == "__main__":
    main()
