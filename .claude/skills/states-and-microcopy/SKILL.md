---
name: states-and-microcopy
description: "Design empty, loading, error and success states and the microcopy for them, Apple-style (short, plain, helpful). Use for any state or UI text."
user-invocable: false
metadata:
  skill-id: S57
  owner: ux-designer-apple-hig
  shared-with: [frontend-engineer, technical-writer]
---

# States And Microcopy (S57)

**Owner:** `ux-designer-apple-hig` · **Shared with:** `frontend-engineer`, `technical-writer`

- Every async view has 4 states: **loading** (skeleton or progress with what's happening), **empty** (why + what to do + example), **error** (what happened, what to do, retry), **success**.
- Live analyzer cold start: staged progress "Getting Python ready… Loading NLTK… Ready", with an estimate; keep the textarea usable while loading.
- Microcopy: sentence case, verbs on buttons ("Analyze review"), no blame, no jargon without a one-line explanation (VADER, compound score, entity).
- Explain the NLTK/spaCy split once, near where it matters; don't repeat it in every panel.
- Announce results with a polite live region; move focus only when the user asked for it.
