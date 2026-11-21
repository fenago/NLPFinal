# MDN: user-preference media features (reduced transparency, contrast, reduced motion)

Sources:
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
  raw:
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/at-rules/@media/prefers-reduced-transparency/index.md
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
  raw:
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/at-rules/@media/prefers-contrast/index.md
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
  raw:
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/at-rules/@media/prefers-reduced-motion/index.md
(all three raw paths returned 200; developer.mozilla.org not fetched directly)
Fetched: 2026-11-21
Support: each page embeds a `{{Compat}}` table only; versions not in the text (unverified). The only
status flag in the sources: **prefers-reduced-transparency is marked `status: experimental`** (shows
the compat banner) - treat it as not universally supported.

## prefers-reduced-transparency
- Detects whether the user enabled a setting "to reduce the transparent or translucent layer
  effects"; it "can help improve contrast and readability for some users".
- Values: `no-preference` (evaluates false in boolean context), `reduce`.
- OS settings listed: Windows 10/11 Settings > Personalization > Colors > Transparency effects;
  macOS System Settings > Accessibility > Display > Reduce transparency; iOS Settings >
  Accessibility > Display & Text Size > Reduce Transparency.
- MDN example: `.translucent{opacity:.4}` then `@media (prefers-reduced-transparency){
  .translucent{opacity:.8} }`.

## prefers-contrast
- Detects whether the user asked for lower or higher contrast.
- Values: `no-preference` (false in boolean context); `more` (wants higher contrast); `less` (lower
  contrast); `custom` (user uses a specific colour set whose contrast matches neither more nor less;
  "will match the color palette specified by users of `forced-colors: active`").
- Relies on OS settings (page does not list them).
- MDN example: `.contrast{outline:2px dashed black}` then `@media (prefers-contrast: more){
  .contrast{outline:2px solid black} }`.
- See also: `forced-colors` media query.

## prefers-reduced-motion
- Detects a setting to "minimize the amount of non-essential motion"; user agents "remove, reduce,
  or replace motion-based animations". Scaling or panning large objects can trigger vestibular
  disorders.
- Values: `no-preference`; `reduce`. `@media (prefers-reduced-motion)` equals `@media
  (prefers-reduced-motion: reduce)`.
- Settings listed: GNOME/KDE animation settings, Windows 10 "Show animations in Windows", Windows 11
  Animation Effects, macOS (up to 15) Accessibility > Display > Reduce motion, macOS Tahoe onwards
  Accessibility > Motion, iOS Settings > Accessibility > Motion, Android 9+ Remove animations,
  Firefox `ui.prefersReducedMotion` (0 or 1).
- MDN pattern: put the reduced rules later with the same specificity; replace `pulse` scaling with a
  gentle `dissolve` opacity animation.
- See also: WebKit "Responsive design for motion".

## Project application
- Tokenise glass so each media feature flips tokens, not every selector:
```css
:root { --glass-bg: rgb(255 255 255 / .72); --glass-blur: 20px; --hairline: rgb(0 0 0 / .08); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --glass-bg: rgb(28 28 30 / .72); --hairline: rgb(255 255 255 / .12); } }
@media (prefers-reduced-transparency: reduce) { :root { --glass-bg: var(--surface); --glass-blur: 0px; } }
@media (prefers-contrast: more) { :root { --glass-bg: var(--surface); --glass-blur: 0px; --hairline: currentColor; } }
@media (prefers-reduced-motion: reduce) { *, ::before, ::after { animation-duration: .01ms !important; transition-duration: .01ms !important; scroll-behavior: auto !important; } }
```
- Because reduced-transparency is experimental, `prefers-contrast: more` is also used to drop glass
  so users on browsers without the former still get an opaque bar; unknown media features are simply
  ignored by browsers (general CSS behaviour, (unverified) on these pages).
- Keep chart animations (Chart.js) and the Pyodide progress indicator working under `reduce`:
  replace motion with fades/instant states, but keep progress feedback (non-essential motion only).
- Test with OS settings or Chrome DevTools > Rendering > "Emulate CSS media feature ..." (DevTools
  feature is general knowledge, (unverified) here).
- `custom`/forced-colors: do not rely on background colours for meaning (borders, outlines, text
  labels must remain).
