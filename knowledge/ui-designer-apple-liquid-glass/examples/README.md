# Worked examples: UI designer (Sable)

Study these **before** any design work. They define this team's quality bar.

| File | What it shows |
|---|---|
| [01-liquid-glass-tabbar-sidebar.html](01-liquid-glass-tabbar-sidebar.html) | A working, annotated Liquid Glass **tab bar (phone)** and **sidebar (desktop)** with the same destinations. Glass is used only on the navigation layer, with solid content cards, 44 px targets and the system font stack. It includes fallbacks for **reduce transparency**, **increase contrast**, **reduce motion** and missing `backdrop-filter` support. Open it in a browser and resize across 1024 px. |
| [02-glass-legibility-good-vs-bad.html](02-glass-legibility-good-vs-bad.html) | Three bad and three good glass treatments over a worst-case bright background. The bad ones are clear glass with no dim, glass on content, and text that relies on blur. The good ones are the regular variant, clear glass with a 35 % dim, and the solid fallback. Each comes with its contrast verdict. |

Key takeaways: glass goes on controls, never on content. Use the regular variant first, and add a dim layer if you use the clear variant. Measure legibility against the worst case, and make sure every glass surface has a solid fallback.
