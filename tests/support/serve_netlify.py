"""Static server for site/ that applies the [[headers]] rules from netlify.toml. Owner: qa-engineer.

Local stand-in for the Netlify CDN so e2e tests also exercise our CSP, cache and .wasm headers.
Path rules follow Netlify's documented syntax: `*` wildcard, `:placeholder` = one path segment.
It is NOT Netlify: verify headers on a real deploy preview with `curl -sI`.

Usage: python tests/support/serve_netlify.py [--port 8000] [--dir site]
"""
from __future__ import annotations

import argparse
import functools
import http.server
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def compile_rules(toml_path: Path) -> list[tuple[re.Pattern, dict]]:
    cfg = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    rules = []
    for rule in cfg.get("headers", []):
        pat = re.escape(rule["for"]).replace(r"\*", ".*")
        pat = re.sub(r"/:([A-Za-z_]+)", r"/[^/]+", pat)
        rules.append((re.compile(f"^{pat}$"), rule.get("values", {})))
    return rules


class Handler(http.server.SimpleHTTPRequestHandler):
    rules: list = []
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".mjs": "text/javascript", ".js": "text/javascript", ".wasm": "application/wasm",
                      ".json": "application/json", ".whl": "application/zip"}

    def _rule_headers(self) -> dict:
        path = self.path.split("?", 1)[0]
        merged: dict = {}
        for rx, values in self.rules:
            if rx.match(path):
                merged.update({k.lower(): (k, v) for k, v in values.items()})
        return merged

    def send_header(self, keyword, value):
        # A netlify.toml value replaces the server default (e.g. Content-Type) instead of duplicating it.
        if keyword.lower() in self._rule_headers():
            return
        super().send_header(keyword, value)

    def end_headers(self):
        for k, v in self._rule_headers().values():
            super().send_header(k, v)
        super().end_headers()

    def log_message(self, *args):  # keep test output quiet
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--dir", default=str(ROOT / "site"))
    args = ap.parse_args()
    Handler.rules = compile_rules(ROOT / "netlify.toml")
    handler = functools.partial(Handler, directory=args.dir)
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as srv:
        print(f"serving {args.dir} with netlify.toml headers on http://127.0.0.1:{args.port}", flush=True)
        srv.serve_forever()


if __name__ == "__main__":
    main()
