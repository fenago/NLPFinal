---
name: apple-layout-spacing
description: "Apple-style layout, spacing and grouping for the web: 8-pt grid, margins, readable widths, adaptive breakpoints. Use when arranging screens, cards, lists or forms."
user-invocable: false
metadata:
  skill-id: S49
  owner: ui-designer-apple-liquid-glass
  shared-with: [ux-designer-apple-hig, frontend-engineer]
---

# Apple Layout Spacing (S49)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `ux-designer-apple-hig`, `frontend-engineer`

- Spacing scale (px): 4, 8, 12, 16, 20, 24, 32, 44, 64. Tokens `--space-1 … --space-9`.
- Page margins: 16px phones, 20–24px tablets, 32px+ desktop; respect `env(safe-area-inset-*)` with `viewport-fit=cover`.
- Readable text width ≤ 70ch. Content max width ~1200px, centered.
- Group related items in inset grouped cards (radius 12–16px, 16px padding); separate groups with 24–32px.
- Hierarchy: one large title per screen, then section headers (title3/headline), then content. Align to a shared leading edge.
- Breakpoints: < 700px phone (bottom tab bar), 700–1023px tablet, ≥ 1024px desktop (sidebar).
- Nothing important under floating glass bars: add bottom/left padding equal to the bar size.
- Reference: knowledge/ux-designer-apple-hig/02-layout.md.
