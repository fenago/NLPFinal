# UI Designer (Apple / Liquid Glass) - Knowledge Index

Project: Customer Review Analyzer (static HTML/CSS/JS site on Netlify). Notes distilled from
official Apple Human Interface Guidelines pages, the Apple fonts page and MDN source markdown, all
fetched 2026-11-21. Apple guidance is for Apple platforms; every note ends with a "Project
application" translating it to CSS (pt to px is a translation, roughly 1:1, not an Apple statement).

| File | Read when you need to... | Key takeaways |
|---|---|---|
| 01-materials-liquid-glass.md | decide where and how to use glass | Glass = controls/navigation layer only, never content; regular vs clear; 35% dark dimming for clear over bright content; use sparingly |
| 02-adopting-liquid-glass.md | review a design against Apple's adoption guidance | Reduce custom backgrounds; test with reduce-transparency/motion; no glass-on-glass; clear nav hierarchy |
| 03-color.md | choose semantic colours, dark mode, contrast | Light + dark + increased-contrast variants; colour never the only cue; 4.5:1 min, 7:1 for small text; tint glass sparingly |
| 04-typography.md | set type sizes and weights | iOS body 17 pt (min 11 pt); avoid light weights; text styles table; support text enlargement |
| 05-sf-fonts-license.md | decide which font to use | SF licence: mock-ups only, no embedding, no website content; use system font stack |
| 06-css-backdrop-filter.md | write glass CSS | `backdrop-filter: blur() saturate()`; needs translucent background; backdrop-root pitfalls (opacity/filter/mask on ancestors) |
| 07-css-user-preference-media.md | add accessibility media queries | reduced-transparency (experimental), contrast more/less/custom, reduced-motion reduce |

## Quick facts
- SF licence wording: "SOLELY FOR CREATING MOCK-UPS OF USER INTERFACES" for Apple OSes; "You may not
  embed the Apple Font in any software programs or other products"; no "website content".
- Clear Liquid Glass: only over visually rich media; add a 35% dark dim layer if the content below is bright.
- Body text 17 pt on iOS (default), 44x44 pt controls (see UX folder).

## Related skills and folders
- Skills in the skills list: `liquid-glass-web`, `apple-color-dark-mode`, `apple-typography-web`,
  `design-tokens`, `accessibility-audit`.
- UX counterpart: knowledge/ux-designer-apple-hig/INDEX.md.
- Fetch limits: HIG pages came as JSON via developer.apple.com/tutorials/data; tables for individual
  colour hex values were not extracted; MDN Compat tables are not in the markdown source, so browser
  versions are (unverified).

## Key reference docs (docs/)
Standalone summaries with official links, Do/Don't tables and "Translate to the web" sections. Read these first.
- docs/liquid-glass-reference.md - HIG Materials + Adopting Liquid Glass: layers, regular vs clear, 35% dimming, accessibility settings
- docs/typography-and-fonts-reference.md - HIG Typography + the SF font license (exact restriction quoted)
- docs/color-and-dark-mode-reference.md - HIG Color + Dark Mode + increased contrast

## Worked examples (examples/) - study before working
- examples/README.md - how to use the examples
- examples/01-liquid-glass-tabbar-sidebar.html - glass tab bar and sidebar on the navigation layer
- examples/02-glass-legibility-good-vs-bad.html - legible vs illegible glass side by side
