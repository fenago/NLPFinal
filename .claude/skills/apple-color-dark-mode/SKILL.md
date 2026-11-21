---
name: apple-color-dark-mode
description: "Semantic color tokens in the Apple style for light, dark and increased-contrast modes. Use for any color choice, theme, or dark-mode work."
user-invocable: false
metadata:
  skill-id: S48
  owner: ui-designer-apple-liquid-glass
  shared-with: [frontend-engineer, dataviz-specialist, ux-designer-apple-hig]
---

# Apple Color Dark Mode (S48)

**Owner:** `ui-designer-apple-liquid-glass` · **Shared with:** `frontend-engineer`, `dataviz-specialist`, `ux-designer-apple-hig`

Use **semantic** tokens, never raw hex in components. Values approximate Apple's system palette (translation for the web — check contrast yourself).

```css
:root { color-scheme: light dark;
  --bg: #f2f2f7; --bg-elevated: #ffffff; --bg-grouped: #ffffff;
  --label: #000000; --label-2: rgb(60 60 67 / .78); --label-3: rgb(60 60 67 / .6);
  --separator: rgb(60 60 67 / .29); --separator-strong: #3c3c43;
  --tint: #0066cc;   /* link/accent, 4.5:1+ on white */
  --pos: #1f6fb2; --neu: #6b6b70; --neg: #b8460b;   /* sentiment: blue/gray/orange, CVD-safe */
}
@media (prefers-color-scheme: dark) { :root {
  --bg: #000000; --bg-elevated: #1c1c1e; --bg-grouped: #2c2c2e;
  --label: #ffffff; --label-2: rgb(235 235 245 / .78); --label-3: rgb(235 235 245 / .6);
  --separator: rgb(84 84 88 / .65); --separator-strong: #d1d1d6;
  --tint: #4da3ff; --pos: #64a8ff; --neu: #a1a1a6; --neg: #ff9f5a; } }
@media (prefers-contrast: more) { :root {
  --label-2: var(--label); --label-3: var(--label); --separator: var(--separator-strong);
  --tint: #004c99; } }
```
- Respect an explicit page theme switch too (`:root[data-theme="dark"]` mirrors the dark block).
- Never color alone for meaning: pair sentiment color with a label or symbol.
- Secondary label tokens must still reach 4.5:1 for body-size text; verify in both modes.
- Reference: knowledge/ui-designer-apple-liquid-glass/03-color.md.
