---
name: accessibility-audit
description: "Run an accessibility audit: 4.5:1 contrast, 44px targets, 200% text zoom, reduce motion, reduce transparency, increase contrast, keyboard and screen reader. Use before shipping any screen or design option."
user-invocable: false
metadata:
  skill-id: S55
  owner: ux-designer-apple-hig
  shared-with: [ui-designer-apple-liquid-glass, qa-engineer, frontend-engineer]
---

# Accessibility Audit (S55)

**Owner:** `ux-designer-apple-hig` · **Shared with:** `ui-designer-apple-liquid-glass`, `qa-engineer`, `frontend-engineer`

Checklist (record Pass/Fail + evidence for each, light AND dark):
1. **Contrast** text ≥ 4.5:1 (≥ 3:1 for ≥ 24px or 19px bold); icons/controls/focus rings ≥ 3:1 — including text on glass over worst-case backgrounds.
2. **Targets** ≥ 44×44 CSS px for every tappable control (HIG 44×44 pt, translated).
3. **200% text zoom** (browser zoom 200% and `html { font-size: 200% }` test): no clipped or overlapping text, no horizontal scroll at 320px CSS width.
4. **Reduce motion** (`prefers-reduced-motion: reduce`): no parallax/slide/scale animations; fades ≤ 150ms or none.
5. **Reduce transparency** (`prefers-reduced-transparency: reduce`): all glass becomes solid.
6. **Increase contrast** (`prefers-contrast: more`): stronger borders/separators, secondary text → primary.
7. **Keyboard**: everything reachable, visible focus, logical order, no traps.
8. **Screen reader**: landmarks, headings, labels, live region for async results, charts with text alternatives.
9. **Color not alone** for sentiment or state.
Automate with Playwright `page.emulateMedia({ colorScheme, reducedMotion, contrast })` plus `forcedColors`; for reduced transparency inject a test class if the browser can't emulate it. Reference: knowledge/ux-designer-apple-hig/01-accessibility.md, 06-web-preference-media.md.
