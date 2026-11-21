---
name: design-options-board
description: "Produce 2\u20133 side-by-side design options of a real screen as separate preview pages, with an index to compare them. Use when exploring visual directions before committing."
user-invocable: false
metadata:
  skill-id: S51
  owner: ui-designer-apple-liquid-glass
  shared-with: [ux-designer-apple-hig]
---

# Design Options Board (S51)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `ux-designer-apple-hig`

- Location: `site/options/` → `/options/` (index) and `/options/<a|b|c>/`. Never modify the live app files to build options.
- Use the **real** app content and data (`/data/*.json`, the same labels, NLTK/spaCy badges) — no lorem ipsum, no fake numbers.
- Each option: one-line intent, what changed, trade-offs; same information architecture so options are comparable.
- Index page: thumbnails or cards linking to each option, plus a comparison table (look, legibility, accessibility result, effort to adopt).
- Each option passes the accessibility-audit skill and supports reduce transparency, increase contrast, reduce motion, light/dark.
- Self-contained per option (own CSS/JS file) so a choice can be adopted later without untangling.
