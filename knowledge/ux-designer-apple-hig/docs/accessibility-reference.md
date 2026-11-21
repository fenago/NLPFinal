# Accessibility reference (HIG Accessibility + MDN preference media features)

## Why this matters
The audience includes people with low vision, motor limits, vestibular
sensitivity and colour blindness. The HIG
gives concrete numbers (text size, contrast, target size) and names the system
settings (Increase Contrast, Reduce
Transparency, Reduce Motion) that a design must survive. The web exposes the
same settings as media queries.

## Official sources
- https://developer.apple.com/design/human-interface-guidelines/accessibility
- https://developer.apple.com/design/human-interface-guidelines/dark-mode
  (testing with Increase Contrast / Reduce Transparency)
-
  https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Raw MDN sources:
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/at-rules/@media/<feature>/index.md
- Detail notes: ../01-accessibility.md, ../06-web-preference-media.md
- Fetched 2026-11-21.

## Key rules
- Text size: let people enlarge text "by at least 200 percent". Default 17 pt /
  minimum 11 pt on iOS.
- Contrast (WCAG AA values): 4.5:1 up to 17 pt; 3:1 at 18 pt; 3:1 for bold. If
  not met by default, provide a
  higher-contrast scheme when Increase Contrast is on; check light and dark.
- "Convey information with more than color alone": shapes, icons, labels;
  red-green and blue-orange are hard pairs.
- Target size: iOS default 44x44 pt, minimum 28x28 pt; padding about 12 pt
  around bezelled elements, about 24 pt
  around elements without a bezel.
- Gestures: prefer simple gestures; always offer an on-screen alternative.
- Keyboard: support Full Keyboard Access; "avoid overriding system-defined
  keyboard shortcuts".
- VoiceOver: describe the interface and content (the page only links to deeper
  VoiceOver guidance) (unverified detail).
- Cognitive: avoid time-boxed UI; explicit dismissal; keep actions simple;
  confirm destructive actions.
- Reduce Motion: reduce "automatic and repetitive animations, including zooming,
  scaling, and peripheral motion";
  replace transitions with fades; avoid depth animation and animating into and
  out of blurs.
- Reduce Transparency: no dedicated Accessibility-page section; Materials and
  Adopting Liquid Glass say such settings
  "can remove or modify certain effects" and need testing.
- MDN: `prefers-reduced-transparency` (`no-preference`, `reduce`; experimental),
  `prefers-contrast`
  (`no-preference`, `more`, `less`, `custom`), `prefers-reduced-motion`
  (`no-preference`, `reduce`). Browser versions
  are not in the MDN source markdown (unverified).

## Do / Don't
| Do | Don't |
|---|---|
| 44px minimum touch targets with ~12px gaps | Pack small icon buttons together |
| Label sentiment with text plus colour | Encode status by colour alone |
| Support 200% zoom, reflow at 320px | Fix heights that clip text |
| Replace motion with fades under `reduce` | Disable progress feedback entirely |
| Opaque surfaces for reduced transparency / more contrast | Leave text on blurred imagery |
| Persistent status messages | Auto-dismiss errors on a timer |

## Translate to the web
- pt to CSS px is roughly 1:1 as a translation (44 pt about 44px); WCAG target
  sizes are not on the Apple page (unverified).
- Flip tokens, not selectors, inside the three media queries; tie the
  reduced-transparency fallback to
  `prefers-contrast: more` too, since the former is experimental.
- Use `role="status"` / `role="alert"` for Pyodide loading and errors; keep the
  ARIA tabs pattern with arrow keys.
- Test matrix: light, dark, reduced transparency, contrast more, reduced motion,
  dark + more + reduced, 200% zoom.
- Checklist skill: `accessibility-audit`.

