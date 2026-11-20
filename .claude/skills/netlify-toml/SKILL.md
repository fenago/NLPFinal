---
name: netlify-toml
description: "Own netlify.toml: build command, publish dir, Python version, env vars, headers. Use when changing any Netlify configuration."
user-invocable: false
metadata:
  skill-id: S35
  owner: netlify-engineer
  shared-with: [build-pipeline-engineer, pyodide-engineer]
---

# netlify.toml (S35)

**Owner:** `netlify-engineer` · **Shared with:** `build-pipeline-engineer`, `pyodide-engineer`

```toml
[build]
  command = "python pipeline/build.py"
  publish = "site"
[build.environment]
  PYTHON_VERSION = "3.12"
  NLTK_DATA = "/opt/build/repo/nltk_data"
[[headers]]
  for = "/pyodide/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/data/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"
```
- No `[functions]` section: the project has no functions (netlify-guardrail).
- Reference: knowledge/netlify-engineer/.
