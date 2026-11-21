# Dashboard design options (A, B, C)

Author: Sable (`ui-designer-apple-liquid-glass`). Previews live at `/options/` (board), `/options/a/`, `/options/b/`, `/options/c/`.
No live-app file was changed. All three use the real `/data/*.json` (overview, VADER distribution, top words, key phrases,
top aspects with sentiment, people / places / brands / products leaderboards), the NLTK / spaCy / NLTK + spaCy badges and the
live app's legend wording (shown once, as a disclosure). Navigation: Dashboard, Reviews, Analyze, About (one-word labels per
Wren's `docs/ux-review.md`), linking to `/#dashboard`, `/#reviews`, `/#live`, `/#about`. Bottom tab bar under 700px, sidebar from 1024px
(700-1023px keeps the tab bar). Files: `site/options/{index.html,shared/data.js,ICONS.md}` and `a|b|c/{index.html,styles.css,app.js}`.

## Intent
- **A "Liquid Glass"**: frosted floating pill tab bar (phone) and floating sidebar (desktop) over a soft colourful backdrop. Regular variant only
  (80-82% tint + blur 24px + saturate), so the 35% dim layer is not needed. Cards are solid.
- **B "Clean Apple Light"**: solid white cards on a light grouped background, flat, no shadows. Glass only on the full-width bottom tab bar; the desktop
  sidebar is solid. Full dark mode included.
- **C "Dark Pro"**: dark by default (macOS style): glass sidebar attached to the left edge on desktop, glass tab bar on phones, dark grouped surfaces,
  gradient accent bars. It follows the system: when the system asks for light, a light palette is used (not dark-only).

## Audit results (Chromium, light and dark, phone 390x844 and desktop 1280x800, plus contrast:more + reduced motion, plus reduced transparency)
| Check | A | B | C |
|---|---|---|---|
| Minimum text contrast (all 12 modes; glass measured over both white and black worst-case backdrops; text on the gradient backdrop measured per pixel) | 5.28:1 | 4.99:1 | 4.81:1 |
| Contrast failures (text 4.5, icons 3) | 0 | 0 | 0 |
| Smallest interactive target | 44 px | 44 px | 44 px |
| Console errors / HTTP >= 400 | 0 / 0 | 0 / 0 | 0 / 0 |
| Off-origin requests | 0 | 0 | 0 |
| 320 px width with `html{font-size:200%}`: horizontal scroll | none | none | none |
| Tab bar at 320 px / 200%: clipped labels, last content hidden by bar | none, none | none, none | none, none |
| Overview numbers above the fold at 390x844 | yes (bottom 612 px) | yes (608 px) | yes (618 px) |
| Keyboard: visible focus ring on first 8 stops | 3 px solid | 3 px solid | 3 px solid |
| Landmarks / headings | nav x2, main, one h1, h2 per card, h3 for entity groups | same | same |
| Chart text alternative | canvas `role=img` + aria-label, and a visible counts list | same | same |
| `prefers-contrast: more` | solid nav, 2 px borders, secondary text = primary | same | same |
| `prefers-reduced-motion` | motion tokens 0ms, Chart.js animation off | same | same |
| `prefers-reduced-transparency` | solid nav (rule present, verified below) | solid tab bar | solid nav |

Notes on method: `audit.js` (kept in the session scratchpad) computes contrast from computed colours, composites every translucent
layer, and for glass surfaces takes the worse of white and black behind. Text sitting on the A/C backdrop gradient was measured on screenshot
pixels with the text hidden. Chromium cannot emulate `prefers-reduced-transparency`, so the audit re-applies each stylesheet with that media query
forced to `all` (the same rule body that ships) and re-measures; it passed. Chart.js canvas labels are not DOM text and were not measured; their colours use
`--chart-text` (>= 7:1 on the card colour by token choice, not measured on canvas).

Screenshots: `docs/design-options-assets/` (light phone, dark desktop and contrast+reduced-motion phone per option, plus A with reduced transparency).

## Trade-offs
- **A** is the most "Apple 2025" and shows glass where it belongs, but the backdrop adds noise behind the page title, glass legibility depends on
  high tint opacity (so the look is subtle), and the floating bar costs ~100 px of space on phones.
- **B** is the safest for legibility and the smallest change to the live CSS; the look is plainer and the glass is barely visible.
- **C** suits a data-heavy view and gives the strongest visual identity; it needs two palettes maintained and the light fallback is the less polished side.
Wren's guidance applied: one-word tabs, badge text >= 4.5:1 in the same spot on every card, legend collapsed to one disclosure, control borders >= 3:1
(`--control-border`), rem-based 17px body, `prefers-contrast: more` changes borders and text, glass limited to one or two nav surfaces, no stacked glass.
Not applied: top tabs for the 700-1023px range (the options keep the tab bar there). Only the Dashboard is designed; other tabs link to the live app.
Entity and aspect rows are not clickable here (the live app opens filtered reviews).

## Recommendation
Adopt **B as the base and borrow A's tab bar treatment only if the team wants glass**: B has the lowest risk and effort and still looks Apple-like.
If the team wants a visible design statement, choose **A**, since it meets every check, keeps glass on two navigation surfaces and degrades to solid.
C is best kept as a future dark theme rather than the default. Next: orchestrator picks; frontend-engineer implements in the live app; dataviz-specialist maps chart colours to the tokens; Wren re-audits.
