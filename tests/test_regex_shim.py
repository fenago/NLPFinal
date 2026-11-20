"""The browser's `regex` shim gives identical NLTK results to the real `regex` engine. Owner: qa-engineer.

Runs in a subprocess so the shim (site/vendor-py) is imported instead of the installed `regex`.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPT = r"""
import json, sys
sys.path.insert(0, sys.argv[1])        # site/vendor-py first -> shim wins
sys.path.insert(1, sys.argv[2])        # repo root
import regex
assert regex.__version__ == "0+shim", regex.__file__
from nlp import nltk_analyzer as na
na.configure(sys.argv[3])
texts = [json.loads(l)["text"] for l in open(sys.argv[4], encoding="utf-8")]
texts += ["hey!!!!!! :) :-( lol", "Price: $12.99 (tax incl.) -- e-mail me at [EMAIL]!", "Ünïcödé café naïve résumé."]
print(json.dumps([na.analyze(t) for t in texts]))
"""


def test_shim_matches_real_regex(na):
    sample = ROOT / "data/reviews_sample.jsonl"
    proc = subprocess.run([sys.executable, "-c", SCRIPT, str(ROOT / "site/vendor-py"), str(ROOT),
                           str(ROOT / "nltk_data"), str(sample)], capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr[-2000:]
    shim_out = json.loads(proc.stdout)
    texts = [json.loads(l)["text"] for l in sample.read_text(encoding="utf-8").splitlines()]
    texts += ["hey!!!!!! :) :-( lol", "Price: $12.99 (tax incl.) -- e-mail me at [EMAIL]!", "Ünïcödé café naïve résumé."]
    real_out = [na.analyze(t) for t in texts]
    import regex
    assert regex.__version__ != "0+shim"
    mismatches = [i for i, (a, b) in enumerate(zip(shim_out, real_out)) if a != b]
    assert not mismatches, f"{len(mismatches)} texts differ, first: {texts[mismatches[0]][:200]}"


def test_shim_translates_unicode_property_class():
    # Load the shim module directly from its file without replacing sys.modules["regex"].
    import importlib.util
    spec = importlib.util.spec_from_file_location("regex_shim", ROOT / "site/vendor-py/regex/__init__.py")
    shim = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shim)
    rx = shim.compile(r"([^\p{L}\p{N}])\1{3,}")
    assert rx.sub(r"\1\1\1", "wow!!!!!!", timeout=1.0) == "wow!!!"
    deferred = shim.compile(r"\p{Lu}\p{Ll}+")
    try:
        deferred.search("Abc")
    except shim.error:
        pass
    else:
        raise AssertionError("unsupported pattern should raise regex.error when used")
