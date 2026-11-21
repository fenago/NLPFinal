# Color and Dark Mode reference (HIG Color + Dark Mode + increased contrast)

## Why this matters
Colour carries status, hierarchy and interactivity. Apple's guidance centres on
semantic colours that adapt to
light, dark and increased-contrast settings, and on never using colour as the
only signal. This site shows
sentiment (positive, neutral, negative), so those rules apply directly.

## Official sources
- https://developer.apple.com/design/human-interface-guidelines/color
- https://developer.apple.com/design/human-interface-guidelines/dark-mode
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
- Detail notes: ../03-color.md, ../07-css-user-preference-media.md
- Fetched 2026-11-21.

## Key rules
- "Avoid using the same color to mean different things."
- "Make sure all your app's colors work well in light, dark, and increased
  contrast contexts." Custom colours need
  light, dark, and an increased-contrast option for each; "even if your app
  ships in a single appearance mode,
  provide both light and dark colors".
- "Avoid relying solely on color to differentiate between objects, indicate
  interactivity, or communicate essential
  information"; add text labels or glyph shapes.
- Prefer semantic system colours defined by purpose (background levels, label
  levels, separator, link); do not
  redefine their meaning; do not hard-code Apple's documented values (they "may
  fluctuate").
- Liquid Glass colour: no inherent colour; apply colour sparingly; tint the
  background of a primary action, not many
  controls; avoid similar colours between control labels and colourful
  backgrounds.
- Dark Mode: "Avoid offering an app-specific appearance setting"; honour the
  system and Auto switching.
- Dark palette: dimmer backgrounds, brighter foregrounds; not simple inversions;
  soften glowing white image backgrounds.
- Contrast: "no lower than 4.5:1"; "strive for a contrast ratio of 7:1,
  especially in small text".
- Test Dark Mode with Increase Contrast and Reduce Transparency on (separately
  and together): dark-on-dark can fail.
- Text colour hierarchy: primary, secondary, tertiary, quaternary labels; avoid
  quaternary where contrast is too low.
- Not found on fetched pages: exact hex values for system colours (table not
  extracted) (unverified).

## Do / Don't
| Do | Don't |
|---|---|
| Name tokens by role (`--text`, `--surface`) | Name tokens by hue (`--blue`) |
| Provide light, dark and `prefers-contrast: more` values | Ship only one palette |
| Pair sentiment colour with a word or icon | Use red/green alone |
| Check 4.5:1 for text, 7:1 where small text allows | Trust that a colour "looks fine" |
| Default theme to the system setting | Force a theme by default |
| Reserve the accent for the primary action | Tint every control |

## Translate to the web
- Tokens on `:root`, overridden under `@media (prefers-color-scheme: dark)`
  (guarded for a manual
  `data-theme`), and again under `@media (prefers-contrast: more)` with stronger
  borders and text.
- Keep `<meta name="color-scheme" content="light dark">` (already present in
  `site/index.html`).
- Sentiment: colour-blind-safe palette plus label text ("Positive"), icon or
  pattern in charts (see the
  `sentiment-visuals` skill).
- An existing in-app theme toggle is tolerable only if "system" stays the
  default (HIG discourages app-specific modes).
- Build the palette yourself and verify contrast; do not copy Apple values or
  brand colours.

