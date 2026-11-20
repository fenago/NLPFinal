"""Fetch a pinned, minimal, self-hosted Pyodide + NLTK into site/pyodide/ (Netlify build step).

Owner: pyodide-engineer. Reviewers: netlify-engineer, qa-engineer.

Nothing is loaded from a CDN at runtime: the browser gets every file from the Netlify origin.
- Pyodide core runtime: npm tarball ``pyodide@314.0.8`` (verified against the pinned sha512
  ``integrity`` value published by the npm registry). Only the files needed to boot are copied.
- NLTK: the PyPI wheel ``nltk-3.10.4-py3-none-any.whl`` (verified against the pinned sha256), the
  same NLTK version the build uses, so live results match the dashboard. The worker unpacks it
  into site-packages; no micropip and no dependency resolution are needed.
- ``regex``: no Emscripten wheel exists on PyPI, so the worker installs the same-origin shim in
  ``site/vendor-py/regex/`` (see its docstring). NLTK's other dependencies (click, joblib, tqdm)
  are only imported by the CLI and parallel helpers, which the analyzer never touches.

Standard library only, so it runs before or after ``pip install``. Downloads are cached in
``.cache/fetch/`` (gitignored); set ``FETCH_CACHE_DIR`` to override.

Layout: site/pyodide/manifest.json (short cache) and site/pyodide/v<version>/ (immutable cache).

Usage: python scripts/fetch_pyodide.py [--out site/pyodide]
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import shutil
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PYODIDE_VERSION = "314.0.8"
PYODIDE_TGZ = f"https://registry.npmjs.org/pyodide/-/pyodide-{PYODIDE_VERSION}.tgz"
PYODIDE_SHA512 = "74Wq1kXOC+CCEzAfxuRAO701nAcCMLjf8NrwvWpu8S41dVMXwXmLQ05dYB+F4e46AdnGo0oq7YHSVUpHsoarLQ=="
CORE_FILES = ["pyodide.mjs", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]

WHEELS = [
    {
        "name": "nltk",
        "version": "3.10.4",
        "file": "nltk-3.10.4-py3-none-any.whl",
        "url": "https://files.pythonhosted.org/packages/a2/04/e7816813e409ca874ba2fcc35455db0e4130b79eb277e1f9edd270ca3c69/nltk-3.10.4-py3-none-any.whl",
        "sha256": "769ba5413f265b7d3e87cd163cc28efa01e29eeef8bb6080bc907949d9fcfb51",
    },
]
MAX_FILE_BYTES = 10 * 1024 * 1024


def download(url: str, cache: Path, attempts: int = 4) -> bytes:
    cached = cache / url.rsplit("/", 1)[-1]
    if cached.exists():
        return cached.read_bytes()
    last: Exception | None = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "review-analyzer-build/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            cache.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(data)
            return data
        except Exception as exc:  # network hiccup: retry with backoff
            last = exc
            wait = 2 ** (i + 1)
            print(f"[pyodide] download failed ({exc}); retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"[pyodide] could not download {url}: {last}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "site/pyodide")
    args = ap.parse_args()
    cache = Path(os.environ.get("FETCH_CACHE_DIR", ROOT / ".cache/fetch"))
    t0 = time.perf_counter()

    tgz = download(PYODIDE_TGZ, cache)
    got = base64.b64encode(hashlib.sha512(tgz).digest()).decode()
    if got != PYODIDE_SHA512:
        raise SystemExit(f"[pyodide] sha512 mismatch for {PYODIDE_TGZ}: {got}")

    # Versioned directory, so Netlify can serve it with a one-year immutable cache; only the small
    # manifest.json at site/pyodide/ (short cache) says which directory is current.
    base = f"v{PYODIDE_VERSION}/"
    shutil.rmtree(args.out, ignore_errors=True)
    vdir = args.out / base
    (vdir / "wheels").mkdir(parents=True)
    manifest = {"pyodide_version": PYODIDE_VERSION, "base": base, "files": {}, "wheels": []}
    with tarfile.open(fileobj=io.BytesIO(tgz), mode="r:gz") as tar:
        for name in CORE_FILES:
            member = tar.getmember(f"package/{name}")
            data = tar.extractfile(member).read()  # type: ignore[union-attr]
            (vdir / name).write_bytes(data)
            manifest["files"][name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    for w in WHEELS:
        data = download(w["url"], cache)
        digest = hashlib.sha256(data).hexdigest()
        if digest != w["sha256"]:
            raise SystemExit(f"[pyodide] sha256 mismatch for {w['file']}: {digest}")
        (vdir / "wheels" / w["file"]).write_bytes(data)
        manifest["wheels"].append({"name": w["name"], "version": w["version"],
                                   "path": f"{base}wheels/{w['file']}", "bytes": len(data), "sha256": digest})

    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    files = [p for p in args.out.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    for p in files:
        print(f"[pyodide]   {p.relative_to(args.out)}  {p.stat().st_size / 1e6:6.2f} MB")
    big = [p for p in files if p.stat().st_size > MAX_FILE_BYTES]
    for p in big:
        print(f"[pyodide] WARNING {p.name} is over 10 MB (Netlify CDN guidance)", file=sys.stderr)
    print(f"[pyodide] {len(files)} files, {total / 1e6:.2f} MB in {time.perf_counter() - t0:.1f}s")
    return 1 if big else 0


if __name__ == "__main__":
    sys.exit(main())
