# Apple HIG: Accessibility

Sources:
- https://developer.apple.com/design/human-interface-guidelines/accessibility
- Also referenced: https://developer.apple.com/design/human-interface-guidelines/dark-mode (Increase
  Contrast / Reduce Transparency testing)
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
Fetched: 2026-11-21
Not found on this page: a dedicated "Reduce Transparency" section (it appears only in Materials,
Dark Mode and Adopting Liquid Glass notes); a dedicated VoiceOver section (the page only links to
VoiceOver) (unverified detail).

## Three qualities
- Accessible interfaces are **intuitive** (familiar, consistent interactions), **perceivable** (no
  single method conveys information) and **adaptable** (supports system accessibility features, lets
  people personalise).

## Vision
- **Larger text:** "give people the option to enlarge text by at least 200 percent (or 140 percent
  in watchOS apps)", via custom UI or Dynamic Type.
- Default/minimum text sizes: iOS/iPadOS 17 pt / 11 pt; macOS 13 / 10; tvOS 29 / 23; visionOS 17 /
  12; watchOS 16 / 12. Thin custom weights need larger sizes.
- **Contrast minimums** (WCAG AA values used by Accessibility Inspector): text up to 17 pt, all
  weights: **4.5:1**; 18 pt, all weights: **3:1**; any size, bold: **3:1**. WCAG and APCA are both
  named as measures; use standard calculators.
- "If your app doesn't provide this minimum contrast by default, ensure it at least provides a
  higher contrast color scheme when the system setting **Increase Contrast** is turned on." Check
  both light and dark appearances.
- Prefer system-defined colours (built-in accessible variants for Increase Contrast and dark).
- **Colour is not the sole indicator:** offer shapes or icons in addition to colour; red-green and
  blue-orange pairings are hard for colour-blind people; consider customisable chart colours.
- **VoiceOver:** "Describe your app's interface and content for VoiceOver" (details on a separate page).

## Hearing (brief)
- Provide captions, subtitles, audio descriptions, transcripts; pair audio cues with haptics and visual cues.

## Mobility
- **Control size:** iOS/iPadOS default 44x44 pt, minimum 28x28 pt; macOS 28x28 / 20x20; tvOS 66x66 /
  56x56; visionOS 60x60 / 28x28; watchOS 44x44 / 28x28.
- Spacing matters as much as size: about **12 pt padding** around elements with a bezel, about **24
  pt** around elements without a bezel.
- Prefer simple gestures; offer alternatives to gestures (e.g. a button besides swipe-to-dismiss).
- Support Voice Control (label elements), Full Keyboard Access, Switch Control; "avoid overriding
  system-defined keyboard shortcuts".

## Cognitive
- Keep actions simple and consistent; "Minimize use of time-boxed interface elements" (auto-dismiss
  timers harm people needing more time); prefer explicit dismissal.
- Give controls for audio/video playback; avoid autoplay without controls.
- **Reduce Motion:** when set, "reduce automatic and repetitive animations, including zooming,
  scaling, and peripheral motion". Tips: tighter springs (less bounce); track gestures directly;
  avoid animating depth changes in z-axis layers; replace x/y/z transitions with fades; "Avoiding
  animating into and out of blurs".
- Assistive Access: remove noncritical workflows; one interaction per screen; confirm twice for
  hard-to-undo actions.

## Related (other pages)
- Materials and Adopting Liquid Glass: reduce-transparency and increase-contrast settings change
  glass appearance; test custom elements under them.
- Dark Mode: test with Increase Contrast and Reduce Transparency on separately and together; 4.5:1
  minimum, strive 7:1 for small text.

## Project application (web translation)
- **Translation note:** Apple "pt" are logical units; for CSS use px/rem approximately 1:1 (44 pt ~
  44 CSS px). This is a translation, not an Apple statement. WCAG target-size numbers are not on the
  fetched Apple page (unverified here).
- Hit targets: tabs, buttons, chart toggles, checkboxes >= 44x44 CSS px on touch viewports
  (`min-height: 44px; min-width: 44px`), with >= ~12px spacing between bezelled controls. The 28 pt
  minimum is a floor for dense desktop UI, not a target.
- Text: use `rem`; verify 200% browser zoom and text-only enlargement with no loss of content or
  horizontal scroll at 320px width.
- Contrast: body text >= 4.5:1; large (>= 18 pt, i.e. ~24px regular) or bold >= 3:1; verify in
  light, dark and `prefers-contrast: more`. Use the `accessibility` skill for the WCAG 2.2 AA
  checklist.
- Never rely on colour alone for sentiment: label ("Positive"), icon or pattern in charts (see
  `sentiment-visuals` skill).
- Honour `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-contrast` (see
  06-web-preference-media.md).
- Keep Pyodide loading states non-time-boxed: no auto-dismissing toasts for errors; use persistent
  `role="status"`/`role="alert"` messages.
- Provide accessible names for icon-only controls; keyboard navigation for the tablist (arrow keys,
  per the existing WAI-ARIA tabs pattern).
