# 01 - Pyodide getting started (loadPyodide, running Python, type conversion)

Sources:
- https://pyodide.org/en/stable/usage/index.html
- https://pyodide.org/en/stable/usage/quickstart.html
- https://pyodide.org/en/stable/usage/type-conversions.html
- https://pyodide.org/en/stable/usage/api/js-api.html

Fetched: 2026-11-20 (docs version shown on pages: **314.0.8**, "stable")

## Loading Pyodide

- `pyodide.js` defines one async function, `loadPyodide()`. It sets up the Python environment and returns the Pyodide top-level namespace.
- Browser (main thread, classic script):
  ```html
  <script src="https://cdn.jsdelivr.net/pyodide/v314.0.8/full/pyodide.js"></script>
  <script>
    async function main(){
      let pyodide = await loadPyodide();
      console.log(pyodide.runPython("1 + 2"));
    }
    main();
  </script>
  ```
- ES module form (used by the official web-worker page): `import { loadPyodide } from ".../pyodide.mjs";`. `pyodide.js` "exports loadPyodide on globalThis" and is described as legacy; "Prefer pyodide.mjs" (downloading page).
- Supported/tested browsers: Firefox 112, Chrome 112, Safari 16.4 or newer.
- Node.js: `npm install pyodide`, then `import { loadPyodide } from "pyodide"`.
- Note from docs: `cdn.jsdelivr.net/pyodide/` serves the runtime plus built packages; `cdn.jsdelivr.net/npm/pyodide@x/` is only the NPM mirror (runtime without wheels).

### loadPyodide config (`PyodideConfig`, all optional)
- `indexURL` (string): URL from which Pyodide loads the runtime and packages. Set it when self-hosting or when loading `pyodide.mjs` from a different location than the files.
- `lockFileURL`: URL of `pyodide-lock.json`.
- `packageCacheDir`: package cache path (node only).
- `packages` (string[]): packages to load during initialization.
- `stdin()`, `stdout(msg)`, `stderr(msg)`: override IO callbacks. Also `pyodide.setStdout(...)` / `setStderr(...)` later.
- `args` (string[]), `env` ({[k]: string}): Python argv and environment variables.
- `jsglobals` (object): object used for the Python `js` module.
- `checkAPIVersion` (default true): throws if pyodide core version differs from the JS package version.
- `fullStdLib`: deprecated, no effect. `convertNullToNone`, `pyproxyToStringRepr`: deprecated opt-ins to old behaviour.

## Running Python

- `pyodide.runPython(code, {globals, locals, filename})` runs a string synchronously via `eval_code`. If the code ends in an expression, that value is returned, translated to JS.
- `await pyodide.runPythonAsync(code, {globals, locals, filename})` is the same but supports **top-level await** (uses `eval_code_async`); returns a Promise. Use it whenever the Python uses `await` (e.g. `micropip.install`) or `loadPackage` is needed first.
- Only the standard library exists after startup; other packages must be loaded (see 02-loading-packages.md).
- `pyodide.pyimport("mod")` imports a Python module and returns it (a PyProxy).
- `pyodide.version` gives the runtime version string.

## Python globals from JS

- `pyodide.globals` is a PyProxy of the global Python namespace.
  ```js
  pyodide.runPython(`x = [3, 4]`);
  pyodide.globals.get('x').toJs();   // [3, 4]
  pyodide.globals.set("x", 'now a string');
  pyodide.globals.set("square", x => x*x);   // JS function visible to Python
  pyodide.runPython("square(3)");
  ```
- Python can reach JS via `import js` (e.g. `js.document`; not available in workers for DOM). `pyodide.registerJsModule(name, obj)` registers a JS object as importable module.

## Type conversions

Implicit (immutable primitives are copied):

| Python | JavaScript |
|---|---|
| int | Number or BigInt |
| float | Number |
| str | String |
| bool | Boolean |
| None | undefined |
| `pyodide.ffi.jsnull` | null |

JS to Python: Number to int/float, BigInt to `JsBigInt`, String to str, Boolean to bool, undefined to None, **null to `pyodide.ffi.jsnull`** (not None, unless deprecated `convertNullToNone`).

Everything else (list, dict, set, objects) becomes a **PyProxy** when sent to JS.
- Proxy ops: `proxy.get(k)` = `x[k]`, `proxy.set(k,v)`, `proxy.has(k)`, `proxy.length` = `len(x)`, `proxy.foo` = `x.foo`, `proxy(...)` = call, `proxy.toString()` = `str(x)`, `await proxy`, iteration via `Symbol.iterator`.
- `proxy.toJs(options)` converts recursively ("deep") to JS objects. Options: `depth` (e.g. `{depth: 1}` shallow), `dict_converter`, `default_converter`, `eager_converter`, `create_pyproxies` (false => `ConversionError` if a proxy would be needed), `pyproxies` (array that collects proxies created).
- **Python dict becomes a JS `Map` by default.** To get a plain Object: `proxy.toJs({dict_converter: Object.fromEntries})`.
- `pyodide.toPy(obj, {depth, defaultConverter})` converts a JS object to Python (JS Array to list, Object to dict, etc.). Python side equivalent: `pyodide.ffi.to_js`.
- JS typed arrays proxied into Python; call `.to_py()` to get a memoryview.

## PyProxy memory management

- Any Py-to-JS translation may create a PyProxy; you must `proxy.destroy()` when done, or declare with `using`. After destroy, use throws `Error: Object has already been destroyed`.
- `toJs()` can create many nested proxies; pass `{pyproxies: arr}` and destroy each entry afterwards. `proxy.copy()` makes another proxy to the same object.
- **Simplest leak-free pattern for this project:** return JSON from Python (`json.dumps(...)` string, a primitive that is copied) and `JSON.parse` in JS, or have Python call `to_js(..., dict_converter=js.Object.fromEntries)`.

## Project application

- The analyzer worker should: `loadPyodide({indexURL})`, load nltk, copy NLTK data into the FS, then expose one Python function `analyze(text) -> json str` through `pyodide.globals.get("analyze")`; call it, `JSON.parse` the string, `destroy()` the function proxy once if not reused (keeping it for the worker lifetime is fine).
- Use `runPythonAsync` for setup (it may await), `runPython` for fast per-review calls once loaded.
- Passing review text into Python: `pyodide.globals.set("review", text)` (a JS string becomes a Python str, copied) or call the proxied function with the string as argument.
- Beware: Python dict returned directly via `runPython` arrives as a **Map** or PyProxy, not a plain object; avoid by returning JSON text.
