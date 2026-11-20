---
name: accessibility
description: "Meet WCAG 2.2 AA for the site and charts. Use when building UI, charts, colors or interactive widgets."
user-invocable: false
metadata:
  skill-id: S31
  owner: frontend-engineer
  shared-with: [dataviz-specialist, qa-engineer]
---

# Accessibility (S31)

**Owner:** `frontend-engineer` · **Shared with:** `dataviz-specialist`, `qa-engineer`

- Text contrast ≥ 4.5:1; UI component contrast ≥ 3:1.
- Everything keyboard-operable; visible focus; tabs follow the WAI-ARIA tabs pattern.
- Live results announced with `role="status"` / `aria-live="polite"`.
- Never use color alone for sentiment — add labels/icons.
- Every chart has a text alternative (summary or data table).
- Reference: knowledge/frontend-engineer/03-accessibility.md.
