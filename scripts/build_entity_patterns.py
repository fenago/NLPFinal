"""Build data/entity_patterns.jsonl for the spaCy EntityRuler.

Owner: dataset-curator. Yelp Review Full has no business metadata, so the names below were found by
reading en_core_web_sm ORG/PRODUCT/FAC candidates over the sample plus a keyword scan for common
chains, then checking each one in context by hand (method in data/SOURCES.md). This script keeps only
names that really occur in data/reviews_sample.jsonl (case-insensitive) and adds one model-number
token pattern. Patterns are phrase patterns; spacy_analyzer.py matches them on LOWER.

Usage: python scripts/build_entity_patterns.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# label -> list of (canonical id, surface variants). ORG = brands/businesses, PRODUCT = named products.
CURATED: dict[str, list[tuple[str, list[str]]]] = {
    "ORG": [
        ("starbucks", ["Starbucks"]),
        ("mcdonalds", ["McDonald's", "McDonalds", "McDonald"]),
        ("costco", ["Costco"]),
        ("sams-club", ["Sam's"]),
        ("walmart", ["Walmart"]),
        ("toyota", ["Toyota"]),
        ("pepsi", ["Pepsi"]),
        ("applebees", ["Applebee's", "Applebees"]),
        ("kfc", ["Kentucky Fried Chicken", "KFC"]),
        ("cpk", ["CPK", "California Pizza Kitchen"]),
        ("pf-changs", ["PF Chang's", "P.F. Chang's", "PF Changs"]),
        ("panera", ["Panera"]),
        ("dennys", ["Denny's"]),
        ("giant-eagle", ["Giant Eagle"]),
        ("whole-foods", ["Whole Foods", "WF"]),
        ("trader-joes", ["Trader Joe's"]),
        ("long-john-silvers", ["LJS", "Long John Silver's"]),
        ("papa-js", ["Papa J's", "PaPa J's"]),
        ("papa-johns", ["Papa Johns", "Papa John's"]),
        ("pour-house", ["Riley's Pour House", "Murphy's Pour House", "Sullivan's Pour House", "Pour House"]),
        ("bar-louie", ["Bar Louie"]),
        ("smoke-taqueria", ["Smoke Taqueria"]),
        ("east-end-food-coop", ["East End Food Co-op"]),
        ("tazza-doro", ["Tazza D'oro"]),
        ("la-prima", ["La Prima"]),
        ("spak-brothers", ["Spak Brothers"]),
        ("milkshake-factory", ["The Milkshake Factory", "Milkshake Factory"]),
        ("park-house", ["The Park House", "Park House"]),
        ("point-brugge", ["Point Brugge Cafe", "Point Brugge"]),
        ("barbs-country-junction", ["Barb's Country Junction"]),
        ("big-burrito", ["Big Burrito"]),
        ("izzazu", ["Izzazu"]),
        ("flynns", ["Flynn's"]),
        ("rockys", ["Rocky's"]),
        ("millers", ["Miller's"]),
        ("china-palace", ["China Palace"]),
        ("google", ["Google"]),
        ("yelp", ["Yelp"]),
        ("carnegie-museum", ["Carnegie Museum of Art", "Carnegie Museum"]),
    ],
    "PRODUCT": [
        ("big-mac", ["Big Mac"]),
        ("coors-light", ["Coors Light"]),
        ("coors", ["Coors"]),
        ("guinness", ["Guinness"]),
        ("fruit-ninja", ["Fruit Ninja"]),
        ("gobbler-club", ["Gobbler Club"]),
        ("yoshida-sauce", ["Yoshida Sauce"]),
        ("google-offer", ["Google Offer"]),
    ],
}
# Model-number style tokens (e.g. "XR-500", "QC35", "WH-1000XM5"): 1-4 capitals, optional hyphen,
# 2-5 digits, optional 1-3 capital suffix with up to 2 digits.
MODEL_RE = r"^[A-Z]{1,4}-?\d{2,5}(?:[A-Z]{1,3}\d{0,2})?$"


def main() -> None:
    sample = (ROOT / "data/reviews_sample.jsonl").read_text(encoding="utf-8")
    texts = "\n".join(json.loads(l)["text"] for l in sample.splitlines() if l.strip()).lower()
    out, missing = [], []
    for label, entries in CURATED.items():
        for pid, variants in entries:
            for v in variants:
                if re.search(r"(?<!\w)" + re.escape(v.lower()) + r"(?!\w)", texts):
                    out.append({"label": label, "pattern": v, "id": pid})
                else:
                    missing.append(v)
    out.append({"label": "PRODUCT", "pattern": [{"TEXT": {"REGEX": MODEL_RE}}], "id": "model-number"})
    path = ROOT / "data/entity_patterns.jsonl"
    path.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in out), encoding="utf-8")
    print(f"wrote {len(out)} patterns to {path.relative_to(ROOT)}; variants not in sample (skipped): {missing}")


if __name__ == "__main__":
    main()
