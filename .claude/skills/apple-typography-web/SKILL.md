---
name: apple-typography-web
description: "Apple-style typography on the web with the system font stack and a 17px body type scale. Use when choosing fonts, sizes, weights or line heights."
user-invocable: false
metadata:
  skill-id: S47
  owner: ui-designer-apple-liquid-glass
  shared-with: [frontend-engineer, ux-designer-apple-hig]
---

# Apple Typography (Web) (S47)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `frontend-engineer`, `ux-designer-apple-hig`

```css
:root {
  --font-text: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;   /* name only — never embed */
  --fs-caption: 0.75rem;  /* 12 */  --fs-footnote: 0.8125rem; /* 13 */
  --fs-subhead: 0.9375rem;/* 15 */  --fs-body: 1.0625rem;     /* 17 */
  --fs-title3: 1.25rem;   /* 20 */  --fs-title2: 1.375rem;    /* 22 */
  --fs-title1: 1.75rem;   /* 28 */  --fs-large: 2.125rem;     /* 34 */
  --lh-body: 1.47; --lh-title: 1.2;
}
body { font: 400 var(--fs-body)/var(--lh-body) var(--font-text); -webkit-font-smoothing: antialiased; }
```
- **Never embed or self-host SF Pro / SF Compact / New York.** Apple's font license limits them to creating mock-ups of user interfaces for Apple platforms — not websites. `-apple-system` / `BlinkMacSystemFont` shows the system font on Apple devices without shipping the file.
- Body 17px (HIG default body is 17 pt on iOS; pt→px is a web translation). Minimum 12px for captions only.
- Use `rem` so 200% browser zoom / text scaling works; never fix heights on text containers.
- Weights: 400 body, 600 headings/labels, 700 large titles. Avoid light/thin weights for small text.
- Reference: knowledge/ui-designer-apple-liquid-glass/04-typography.md, 05-sf-fonts-license.md.
