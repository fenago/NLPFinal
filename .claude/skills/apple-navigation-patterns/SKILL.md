---
name: apple-navigation-patterns
description: "Apple-style navigation for the web: bottom tab bar on phones, sidebar on desktop/tablet. Use when designing or reviewing app navigation."
user-invocable: false
metadata:
  skill-id: S54
  owner: ux-designer-apple-hig
  shared-with: [ui-designer-apple-liquid-glass, frontend-engineer]
---

# Apple Navigation Patterns (S54)

**Owner:** `ux-designer-apple-hig` · **Shared with:** `ui-designer-apple-liquid-glass`, `frontend-engineer`

- **Phone (< 700px):** bottom tab bar, 3–5 top-level destinations, icon + short label each, always visible, current tab clearly selected. Tabs switch sections; they never trigger actions.
- **Desktop/tablet (≥ 1024px, optionally ≥ 700px):** leading sidebar listing the same destinations (adapts from the tab bar), collapsible, current item highlighted.
- Same destinations, same order, same names across sizes.
- Floating glass tab bar: inset from edges (8–16px), pill shape, `env(safe-area-inset-bottom)`; content scrolls beneath with bottom padding.
- Semantics: `<nav aria-label="Main">`; tabs follow the WAI-ARIA tabs pattern when panels are on one page (arrow keys move, Enter/Space activates) or use links with `aria-current="page"`.
- Reference: knowledge/ux-designer-apple-hig/03-tab-bars.md, 04-sidebars.md.
