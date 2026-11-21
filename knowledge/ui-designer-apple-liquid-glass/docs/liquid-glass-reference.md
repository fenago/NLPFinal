# Liquid Glass reference (HIG Materials + Adopting Liquid Glass)

## Why this matters
Liquid Glass is the translucent material Apple uses for the controls and
navigation layer. Used well it keeps
content in focus; used everywhere it hurts legibility and hierarchy. This site's
header and tab strip are the
only places a web "glass" effect belongs, and it must degrade to an opaque
surface for accessibility settings.

## Official sources
- https://developer.apple.com/design/human-interface-guidelines/materials
-
  https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- MDN backdrop-filter:
  https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter
- Detail notes: ../01-materials-liquid-glass.md, ../02-adopting-liquid-glass.md,
  ../06-css-backdrop-filter.md
- Fetched 2026-11-21 (HIG materials change log: Sept 9, 2025 "Updated guidance
  for Liquid Glass").

## Key rules
- Two layers: a functional layer of controls and navigation (glass) floating
  above a content layer.
  Liquid Glass "forms a distinct functional layer for controls and navigation
  elements - like tab bars and sidebars".
- "Don't use Liquid Glass in the content layer." Use standard materials (blur,
  vibrancy) for content-layer surfaces.
  Only exception: transient controls such as sliders and toggles while being
  used.
- Use sparingly: limit to "the most important functional elements"; overuse
  distracts from content.
- Do not layer or crowd glass elements; remove custom backgrounds that fight the
  system effect.
- Regular variant: blurs and adjusts luminosity to keep text legible. Use when
  backgrounds vary or components
  hold a lot of text (alerts, sidebars, popovers).
- Clear variant: highly translucent. "Only use clear Liquid Glass for components
  that appear over visually rich
  backgrounds" such as photos and video.
- Dimming: over bright content under clear glass "consider adding a dark dimming
  layer of 35% opacity"; not
  needed over sufficiently dark content.
- Legibility: scroll edge effects blur and fade content scrolling under
  controls; resting state must be legible.
- Colour: glass has no inherent colour; tint only primary actions, and tint the
  background rather than the label.
- Accessibility: Reduce Transparency, Increase Contrast and Reduce Motion "can
  remove or modify certain effects";
  test custom elements under them. Larger glass (sidebars) appears more opaque
  for legibility.
- Navigation: clearly separate navigation from content; background extension
  effect mirrors/blurs content under a sidebar.

## Do / Don't
| Do | Don't |
|---|---|
| Put glass on header, tab strip, a sidebar | Put glass on cards, charts, review text or forms |
| Use regular variant over scrolling text | Use clear variant without rich media behind it |
| Add ~35% dark dim behind clear glass over bright imagery | Rely on blur alone for contrast |
| Test with reduced transparency / increased contrast | Assume the translucent look is always visible |
| Keep 1-2 glass surfaces | Stack glass on glass |
| Tint one primary action | Tint every control or label |

## Translate to the web
- The HIG gives no CSS; this is a project translation. Regular glass:
  semi-opaque tint plus
  `backdrop-filter: blur(20px) saturate(160%)` (values are project starting
  points), plus `-webkit-` prefix.
- Never put `opacity`, `filter`, `mask` or `will-change: opacity` on an
  ancestor: it becomes a "backdrop root" and
  the blur samples the wrong pixels (MDN).
- Provide fallbacks: `@supports not (backdrop-filter: blur(1px))`, `@media
  (prefers-reduced-transparency: reduce)`,
  `@media (prefers-contrast: more)` all switch to an opaque surface token.
- 35% dim becomes an overlay `rgb(0 0 0 / .35)`; still verify contrast
  numerically (4.5:1 text).
- Keep glass on `.site-header` / the tablist only; verify in light, dark and the
  emulated preference states.
- Examples to study: ../examples/01-liquid-glass-tabbar-sidebar.html,
  ../examples/02-glass-legibility-good-vs-bad.html.

