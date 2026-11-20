"""Minimal same-origin stand-in for the third-party ``regex`` package, for Pyodide only.

Owner: pyodide-engineer. Used by site/worker.mjs; never installed in the Netlify build.

Why: NLTK 3.10 routes every regular expression through ``nltk.redos``, which compiles with
``regex`` and passes ``timeout=`` to each match call. ``regex`` has no Emscripten wheel on PyPI
and the official Pyodide wheel is only in the 337 MB full distribution, so the browser gets this
shim instead. It maps the API surface NLTK uses (``compile``, module helpers, ``error``,
``Pattern`` and the flag constants) onto the standard library ``re`` and ignores ``timeout``.

Scope: the patterns used by ``nlp/nltk_analyzer.py`` (Punkt, Treebank word tokenizer, VADER,
stopwords). ``tests/test_regex_shim.py`` checks that ``analyze()`` gives identical output with this
shim and with the real ``regex`` engine over the whole review sample. ``regex``-only syntax is
handled in two ways: the Unicode-property classes NLTK uses at import time are translated to
``re`` equivalents (``[^\\p{L}\\p{N}]`` -> ``[\\W_]``, used by TweetTokenizer's HANG_RE), and any
other pattern ``re`` cannot compile becomes a deferred pattern that raises ``error`` only when it
is used, so importing an unrelated NLTK module never fails.
The ReDoS wall-clock timeout is not enforced in the browser: the browser only runs NLTK's own
fixed patterns on the user's own text, inside a Web Worker the page can terminate.
"""
import re as _re

__version__ = "0+shim"

error = _re.error
Pattern = _re.Pattern
Match = _re.Match

A = ASCII = _re.ASCII
I = IGNORECASE = _re.IGNORECASE
L = LOCALE = _re.LOCALE
M = MULTILINE = _re.MULTILINE
S = DOTALL = _re.DOTALL
U = UNICODE = _re.UNICODE
X = VERBOSE = _re.VERBOSE
V0 = VERSION0 = 0
DEFAULT_VERSION = V0

_METHODS = ("search", "match", "fullmatch", "findall", "finditer", "split", "sub", "subn")


class _ShimPattern:
    """Wraps an ``re.Pattern`` and drops the ``regex``-only keyword arguments."""

    __slots__ = ("_rx",)

    def __init__(self, rx):
        self._rx = rx

    def __getattr__(self, name):
        attr = getattr(self._rx, name)
        if name in _METHODS:
            def call(*args, timeout=None, concurrent=None, partial=False, **kwargs):
                return attr(*args, **kwargs)
            return call
        return attr

    def __repr__(self):
        return f"regex_shim.{self._rx!r}"

    def __eq__(self, other):
        return isinstance(other, _ShimPattern) and self._rx == other._rx

    def __hash__(self):
        return hash(self._rx)


#: regex-only Unicode property syntax -> stdlib ``re`` equivalent (str.isalnum-style classes).
_TRANSLATIONS = (
    ("[^\\p{L}\\p{N}]", "[\\W_]"),   # not a letter or number
    ("[\\p{L}\\p{N}]", "[^\\W_]"),   # letter or number
    ("\\p{L}", "[^\\W\\d_]"),        # letter
    ("\\p{N}", "\\d"),                 # number (decimal digits only: approximation)
)


class _DeferredPattern:
    """A pattern ``re`` cannot compile: fails with ``error`` when used, not when imported."""

    def __init__(self, src, flags, exc):
        self.pattern, self.flags, self._exc = src, flags, exc

    def __getattr__(self, name):
        if name in _METHODS:
            raise error(f"regex shim cannot run this pattern in the browser: {self._exc}")
        raise AttributeError(name)


def _translate(src):
    if isinstance(src, str) and "\\p{" in src:
        for old, new in _TRANSLATIONS:
            src = src.replace(old, new)
    return src


def compile(pattern, flags=0, ignore_unused=False, cache_pattern=None, **kwargs):
    src = _translate(getattr(pattern, "pattern", pattern))
    try:
        return _ShimPattern(_re.compile(src, flags))
    except _re.error as exc:
        return _DeferredPattern(src, flags, exc)


def _module_helper(name):
    def helper(pattern, *args, flags=0, timeout=None, concurrent=None, partial=False, **kwargs):
        return getattr(compile(pattern, flags), name)(*args, **kwargs)
    helper.__name__ = name
    return helper


search = _module_helper("search")
match = _module_helper("match")
fullmatch = _module_helper("fullmatch")
findall = _module_helper("findall")
finditer = _module_helper("finditer")
split = _module_helper("split")
sub = _module_helper("sub")
subn = _module_helper("subn")
escape = _re.escape
purge = _re.purge
