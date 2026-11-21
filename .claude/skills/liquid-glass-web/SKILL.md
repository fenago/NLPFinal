---
name: liquid-glass-web
description: "CSS recipes for Apple-style Liquid Glass (glassmorphism) on the web: regular and clear variants, used only on the navigation/controls layer. Use for any frosted/glass styling."
user-invocable: false
metadata:
  skill-id: S46
  owner: ui-designer-apple-liquid-glass
  shared-with: [frontend-engineer]
---

# Liquid Glass (Web) (S46)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `frontend-engineer`

Rule 1 — **glass is for the navigation and controls layer only** (tab bar, sidebar, toolbar, floating buttons, sheets). **Never** put glass on content (cards, charts, tables, review text).
Rule 2 — prefer the **regular** variant; use **clear** only over media-rich backgrounds and add a dim layer.
Rule 3 — every glass surface must pass the legibility check below and degrade under user preferences.

```css
:root {
  --glass-blur: 24px; --glass-sat: 180%;
  --glass-regular: color-mix(in srgb, var(--bg-elevated) 72%, transparent);
  --glass-clear:   color-mix(in srgb, var(--bg-elevated) 22%, transparent);
  --glass-stroke:  color-mix(in srgb, white 45%, transparent);
  --glass-shadow:  0 8px 32px rgb(0 0 0 / .18);
}
.glass {                                  /* regular variant */
  background: var(--glass-regular);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat));
          backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-sat));
  border: 1px solid var(--glass-stroke);
  box-shadow: var(--glass-shadow), inset 0 1px 0 rgb(255 255 255 / .35);
}
.glass--clear { background: var(--glass-clear); position: relative; isolation: isolate; }
.glass--clear::before {                   /* 35% dim layer over bright content */
  content: ""; position: absolute; inset: 0; border-radius: inherit;
  background: rgb(0 0 0 / .35); z-index: -1;
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass, .glass--clear { background: var(--bg-elevated); }
}
@media (prefers-reduced-transparency: reduce) {
  .glass, .glass--clear { background: var(--bg-elevated); backdrop-filter: none; -webkit-backdrop-filter: none; }
  .glass--clear::before { display: none; }
}
@media (prefers-contrast: more) {
  .glass, .glass--clear { background: var(--bg-elevated); backdrop-filter: none; -webkit-backdrop-filter: none;
    border: 2px solid var(--separator-strong); }
}
```

**Legibility check (required for every glass surface):**
1. Test text/icons on the glass over the **brightest** and **darkest** content that can scroll underneath (light and dark mode).
2. Contrast ≥ 4.5:1 for text, ≥ 3:1 for icons/controls, measured against the worst-case composited background.
3. If it fails: increase opacity (regular), add the 35% dim (clear), or switch that surface to the solid fallback.
4. Repeat with `prefers-reduced-transparency: reduce` and `prefers-contrast: more` emulated (Playwright `emulateMedia` / DevTools).

Reference: knowledge/ui-designer-apple-liquid-glass/01-materials-liquid-glass.md, 02-adopting-liquid-glass.md, 06-css-backdrop-filter.md, 07-css-user-preference-media.md.
