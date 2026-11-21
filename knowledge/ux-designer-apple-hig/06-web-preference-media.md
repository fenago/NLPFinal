# Web user-preference media features: audit summary

Sources:
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Raw sources:
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/at-rules/@media/{prefers-reduced-transparency,prefers-contrast,prefers-reduced-motion}/index.md
- Details and code: knowledge/ui-designer-apple-liquid-glass/07-css-user-preference-media.md
Fetched: 2026-11-21

## Summary table
| Feature | Values | Apple counterpart (HIG) | Notes |
|---|---|---|---|
| prefers-reduced-transparency | `no-preference`, `reduce` | Reduce Transparency | Marked **experimental** on MDN; support limited (unverified versions) |
| prefers-contrast | `no-preference`, `more`, `less`, `custom` | Increase Contrast | `custom` pairs with forced colours |
| prefers-reduced-motion | `no-preference`, `reduce` | Reduce Motion | Long-established; plain `@media (prefers-reduced-motion)` means `reduce` |

## UX audit angle
- These are the web equivalents of the settings the HIG says to test (Accessibility, Dark Mode,
  Adopting Liquid Glass): "Test your interface with a variety of display and accessibility
  settings."
- **Reduce transparency:** replace translucent surfaces with opaque ones; legibility over
  decoration. Because support is partial, tie the same fallback to `prefers-contrast: more` too.
- **Increase contrast:** stronger borders/outlines (MDN example turns a dashed outline solid),
  higher text contrast; HIG: provide an increased-contrast variant of every custom colour.
- **Reduce motion:** replace scale/pan/zoom with fades or nothing; HIG list: avoid depth (z-axis)
  animations and "animating into and out of blurs" - relevant to glass that animates blur.
- Settings can change mid-session; use CSS media queries (live) rather than one-time JS checks, or
  listen with `matchMedia(...).addEventListener('change', ...)` (general API, (unverified) on these
  pages).

## Test matrix (each should still be usable and legible)
1. Light / dark / (system default).
2. reduced-transparency: reduce (nav opaque, no blur).
3. contrast: more (borders visible, tint removed, text >= 4.5:1, ideally 7:1 in small text per Dark
   Mode page).
4. reduced-motion: reduce (no parallax/zoom; progress feedback still present).
5. Combination of dark + contrast more + reduced transparency (Dark Mode page warns dark-on-dark
   legibility can fail here).
6. 200% zoom and 320px width.

## Project application
- Add one "Preferences" block in `site/styles.css` that flips design tokens (see the UI note for
  code) instead of scattering overrides.
- Add Playwright checks: emulate `reducedMotion: 'reduce'` and `colorScheme: 'dark'` (names from
  Playwright API, unverified here), assert computed `backdrop-filter` is `none` where required, and
  run an accessibility scan (axe) in each state.
- Document in the About page that the site respects system motion, contrast and transparency
  preferences; no manual toggle is needed (HIG Dark Mode: avoid app-specific appearance settings).
- Do not hide information that relies on colour/transparency in the fallback states.
