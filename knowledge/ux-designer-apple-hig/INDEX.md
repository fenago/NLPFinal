# UX Designer (Apple HIG) - Knowledge Index

Project: Customer Review Analyzer (static HTML/CSS/JS site on Netlify, four tabs: Dashboard, Reviews
& examples, Analyze your own review, About & method). Notes distilled from official Apple Human
Interface Guidelines pages and MDN source markdown, fetched 2026-11-21. Each note ends with "Project
application" (pt to CSS px is a translation).

| File | Read when you need to... | Key takeaways |
|---|---|---|
| 01-accessibility.md | audit a screen for accessibility | 44x44 pt default controls (28 pt min); 4.5:1 / 3:1 contrast; enlarge text >= 200%; colour not sole cue; Reduce Motion; Increase Contrast |
| 02-layout.md | arrange hierarchy and adapt layouts | Important content top/leading; group, align, progressive disclosure; layout by available space, not device; safe areas |
| 03-tab-bars.md | design or review the tab navigation | Navigation not actions; few tabs; single-word labels; never disable tabs; keep visible; adapts to sidebar |
| 04-sidebars.md | consider a desktop sidebar | Leading side; max two levels; do not hide by default; tab bar first when space limited |
| 05-materials-for-ux.md | check legibility/hierarchy of glass | Nav layer vs content layer; regular variant for text; opaque fallback for accessibility settings |
| 06-web-preference-media.md | test accessibility preference queries | reduced-transparency (experimental), contrast, reduced-motion; test matrix |

## Quick facts
- Controls: iOS default 44x44 pt, minimum 28x28 pt; padding about 12 pt around bezelled elements,
  about 24 pt without bezel.
- Text: iOS default 17 pt, minimum 11 pt; users should be able to enlarge text at least 200 percent.
- Contrast (WCAG AA values used by Apple's Accessibility Inspector): 4.5:1 up to 17 pt; 3:1 at 18 pt or bold.
- Do not disable or hide tab bar buttons; explain empty sections instead.

## Related skills and folders
- Skills in the skills list: `accessibility-audit`, `apple-layout-spacing`,
  `apple-navigation-patterns`, `hig-principles-review`, `usability-heuristic-review`,
  `states-and-microcopy`.
- Visual counterpart: knowledge/ui-designer-apple-liquid-glass/INDEX.md (materials, colour, type,
  fonts licence, CSS).
- Gaps (unverified): exact iPhone tab count limit; numeric layout margins; dedicated VoiceOver and
  Reduce Transparency sections were not on the fetched Accessibility page.

## Key reference docs (docs/)
Standalone summaries with official links, Do/Don't tables and "Translate to the web" sections. Read these first.
- docs/accessibility-reference.md - HIG Accessibility (contrast, targets, text size, motion, transparency, contrast settings, VoiceOver) + MDN media features
- docs/navigation-reference.md - HIG Tab bars + Sidebars + Layout
- (no hig-principles-reference.md: the fetched pages state no separate overarching principles beyond Layout's hierarchy rules)

## Worked examples (examples/) - study before working
- examples/README.md - how to use the examples
- examples/01-sample-ranked-usability-review.md - a ranked usability review with severities and fixes
- examples/02-states-microcopy-good-vs-bad.md - empty/loading/error states and microcopy, good vs bad
