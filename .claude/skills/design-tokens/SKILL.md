---
name: design-tokens
description: "Define and use design tokens (CSS custom properties) for color, type, spacing, radius, elevation, glass and motion. Use whenever writing styles so themes stay consistent."
user-invocable: false
metadata:
  skill-id: S52
  owner: ui-designer-apple-liquid-glass
  shared-with: [frontend-engineer, dataviz-specialist]
---

# Design Tokens (S52)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `frontend-engineer`, `dataviz-specialist`

- Tokens live in one file per theme (e.g. `tokens.css`), consumed via `var(--token)` only.
- Groups: `--bg*`, `--label*`, `--separator*`, `--tint`, `--pos/--neu/--neg`; `--font-*`, `--fs-*`, `--lh-*`; `--space-*`; `--radius-sm/md/lg/pill`; `--shadow-*`; `--glass-*`; `--dur-fast/med`, `--ease-standard`.
- Motion tokens collapse under reduced motion:
```css
:root { --dur-fast: 150ms; --dur-med: 250ms; --ease-standard: cubic-bezier(.2,.8,.2,1); }
@media (prefers-reduced-motion: reduce) { :root { --dur-fast: 0ms; --dur-med: 0ms; } }
```
- Charts read tokens at runtime (`getComputedStyle(document.documentElement).getPropertyValue('--pos')`).
- No raw hex/px in components except inside token files.
