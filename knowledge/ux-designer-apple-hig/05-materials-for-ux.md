# Materials: legibility and hierarchy implications (UX view)

Sources:
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- https://developer.apple.com/design/human-interface-guidelines/layout
- Full technical notes: knowledge/ui-designer-apple-liquid-glass/01-materials-liquid-glass.md and
  02-adopting-liquid-glass.md
Fetched: 2026-11-21

## Navigation layer vs content layer
- Liquid Glass is "a distinct functional layer for controls and navigation elements" floating above
  content; **do not use it in the content layer** (it creates "a confusing visual hierarchy").
  Content-layer separation uses standard materials, spacing and grouping.
- "Establish a clear navigation hierarchy ... clearly separate your content from navigation
  elements" (Adopting Liquid Glass).
- Layout page: differentiate controls from content; extend backgrounds under bars; use scroll-edge
  effects rather than a solid/semi-opaque strip beneath controls.

## Legibility rules a UX reviewer should check
- **Regular variant** wherever text is substantial or backgrounds vary; **clear variant** only over
  rich media. For bright media beneath clear glass, consider a ~35% dark dimming layer.
- Thicker/more opaque = better contrast for fine text; thinner = more context. Text on any material
  needs vibrant/high-contrast colours and the standard 4.5:1 (3:1 large/bold) minimums.
- Resting state matters: "make sure its default or resting state ... maintains clear legibility",
  not only when scrolled.
- Avoid stacking or crowding glass elements; avoid colourful labels over colourful backgrounds;
  colour a primary action's background, not many controls.
- Glass "can adapt to people's needs": accessibility settings (Reduce Transparency, Increase
  Contrast, Reduce Motion) change or remove effects, so every design needs a solid-surface state
  that still works. Half sheets become "more opaque" when expanded to maintain focus.
- Overuse "distract[s] from that content": limit glass to the most important functional elements.

## Audit checklist (derived from the pages above)
1. Is glass confined to navigation/controls (header, tabs), not cards/charts/review text?
2. Does text over glass meet contrast over the worst-case background (light, dark, colourful, bright)?
3. Does the interface still look and work with transparency removed and contrast increased?
4. Are there <= 1-2 glass surfaces, none overlapping?
5. Is there a clear separation (shadow/hairline/spacing) between nav layer and content?
6. Are icon-only controls labelled for assistive tech?

## Project application
- Site targets: glass header + tab strip over solid content cards. Reject any design where chart
  panels, the review list or the live-analyzer result sit on translucent surfaces.
- Verify with Playwright/axe contrast checks in light, dark, and emulated `prefers-contrast: more` /
  `prefers-reduced-transparency: reduce` (Playwright `page.emulateMedia` supports `reducedMotion`,
  `colorScheme`, `contrast`/`forcedColors` options; exact option names unverified here - check the
  Playwright docs).
- Provide an opaque fallback for browsers without `backdrop-filter` (see 06-web-preference-media.md).
- Do not describe the design as "Apple's Liquid Glass": it is a web approximation inspired by the
  guidelines (no Apple assets or fonts are used; see UI note 05 on licence).
