---
name: icon-style
description: "Icon rules: open-source line icons in a style similar to Apple's, never Apple logos or SF Symbols. Use when adding or drawing any icon."
user-invocable: false
metadata:
  skill-id: S50
  owner: ui-designer-apple-liquid-glass
  shared-with: [frontend-engineer]
---

# Icon Style (S50)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `frontend-engineer`

- **Do not use** the Apple logo, Apple product images, or SF Symbols glyphs/exports (SF Symbols are licensed for Apple-platform apps; not for websites).
- Use an open-source set with a similar rounded, line style — e.g. **Lucide** (ISC) or **Phosphor** (MIT) — or hand-drawn inline SVG. Record name + license in `site/vendor/ICONS.md`.
- Inline SVG, `stroke="currentColor"`, 1.75–2px stroke, rounded caps/joins, 20–24px in tab bars/sidebars, 17px inline with text.
- Every icon-only control has an accessible name (`aria-label`); decorative icons get `aria-hidden="true"`.
- Self-host: no icon CDNs (netlify-guardrail).
