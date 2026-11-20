---
name: pyodide-runtime
description: "Run Python in the browser with Pyodide: load it, load nltk, run code and exchange data with JS. Use for any change to site/worker.mjs or browser-side Python."
user-invocable: false
metadata:
  skill-id: S26
  owner: pyodide-engineer
  shared-with: [qa-engineer]
---

# Pyodide Runtime (S26)

**Owner:** `pyodide-engineer` · **Shared with:** `qa-engineer`

```js
// inside a MODULE worker: new Worker("/worker.mjs", { type: "module" })
import { loadPyodide } from "/pyodide/pyodide.mjs";
const py = await loadPyodide({ indexURL: "/pyodide/" });
await py.loadPackage("nltk");
py.globals.set("review", text);
const out = await py.runPythonAsync("json.dumps(analyze(review))");
```
- Pyodide 314.x requires a module-type worker; classic `importScripts()` workers are not supported.
- Return JSON strings across the boundary; avoid leaking PyProxies (call `.destroy()` if used).
- Load `nlp/nltk_analyzer.py` source into the FS and import it — same code as the build.
- spaCy is NOT available; never try `micropip.install("spacy")`.
- Reference: knowledge/pyodide-engineer/.
