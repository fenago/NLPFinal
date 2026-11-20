"""Vendor Chart.js from the npm registry into site/vendor/ (pinned, integrity-checked).

Owner: dataviz-specialist. The output file is committed, so the Netlify build does not need this
script; rerun it only to upgrade Chart.js (update VERSION and SHA512 together).
No runtime CDN: the page loads /vendor/chart.umd.min.js from the Netlify origin.

Usage: python scripts/fetch_vendor_js.py
"""
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "4.6.1"
URL = f"https://registry.npmjs.org/chart.js/-/chart.js-{VERSION}.tgz"
SHA512 = "hJyniucsFmq//EvXYvJ6c6mahPoI3kaxdjVH8awTaJ/fDNWeSqqqArixMJWkWNN6fcYvPU3HneSANFNYtRi61g=="


def main() -> None:
    with urllib.request.urlopen(URL, timeout=120) as resp:
        tgz = resp.read()
    got = base64.b64encode(hashlib.sha512(tgz).digest()).decode()
    if got != SHA512:
        raise SystemExit(f"sha512 mismatch: {got}")
    out = ROOT / "site/vendor"
    out.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(tgz), mode="r:gz") as tar:
        names = tar.getnames()
        src = "package/dist/chart.umd.min.js" if "package/dist/chart.umd.min.js" in names else "package/dist/chart.umd.js"
        js = tar.extractfile(src).read()  # type: ignore[union-attr]
        lic = tar.extractfile("package/LICENSE.md").read()  # type: ignore[union-attr]
    (out / "chart.umd.min.js").write_bytes(js)
    (out / "chart.js.LICENSE.md").write_bytes(lic)
    print(f"chart.js {VERSION}: {src} -> site/vendor/chart.umd.min.js ({len(js) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
