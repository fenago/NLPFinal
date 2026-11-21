# Apple HIG: Color (and Dark Mode)

Sources:
- https://developer.apple.com/design/human-interface-guidelines/color
- https://developer.apple.com/design/human-interface-guidelines/dark-mode
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/color.json and
  .../dark-mode.json
Fetched: 2026-11-21

## Best practices (Color page)
- Do not use the same colour to mean different things; keep colour use consistent for status and
  interactivity (e.g. brand colour for interactive text must not also style non-interactive text).
- "Make sure all your app's colors work well in **light, dark, and increased contrast** contexts."
  For custom colours supply light and dark variants and an increased-contrast option for each, "that
  provides a significantly higher amount of visual differentiation". "Even if your app ships in a
  single appearance mode, provide both light and dark colors to support Liquid Glass adaptivity."
- Test under different lighting (bright surroundings make colours look darker/muted; dark
  surroundings make them look bright/saturated) and on different devices/colour profiles (sRGB vs
  Display P3).
- Colours behind or on translucent elements (toolbars) can look different.

## Inclusive color
- "Avoid relying solely on color to differentiate between objects, indicate interactivity, or
  communicate essential information." Add text labels or glyph shapes.
- Avoid low-contrast combinations that blend with the background; red/green and blue/orange are
  named elsewhere (Accessibility page) as hard pairings for colour-blind people.
- Colours carry different meanings across cultures.

## System colors
- Do not hard-code system colour values; documented values "may fluctuate from release to release".
  Use semantic dynamic colors defined by purpose (background hierarchy, label, separator, link).
- "Avoid redefining the semantic meanings of dynamic system colors" (e.g. do not use the separator
  colour for text).
- iOS background hierarchy: primary (overall view), secondary (grouping inside), tertiary (grouping
  inside secondary). Label levels: label, secondary, tertiary, quaternary, placeholder; separator
  and opaque separator; link.
- The page has a System colors specification table with default/increased-contrast values for light
  and dark; individual hex values not reproduced here (unverified in this fetch; table rows were not
  fully extracted).

## Liquid Glass color
- By default glass "has no inherent color" and takes colour from content behind it. Tint sparingly
  (e.g. primary call to action).
- Small elements (toolbars, tab bars) can flip between light/dark appearance; symbols/text are
  monochrome by default (darker over light content, lighter over dark). Larger elements such as
  sidebars look more opaque for legibility.
- "Apply color sparingly"; reserve for status indicators or primary actions. For primary actions,
  "apply color to the background rather than to symbols or text". Do not tint the background of
  multiple controls.
- Avoid similar colours in control labels over a colourful background; prefer a monochrome bar or an
  accent with enough differentiation.
- Keep the **resting state** (e.g. top of a scrolled view) legible even if coloured content scrolls
  beneath controls.

## Dark Mode page
- "Avoid offering an app-specific appearance setting"; respect the system setting (Auto can switch
  while the app runs).
- Test with Increase Contrast and Reduce Transparency on, separately and together: dark text on dark
  backgrounds can lose legibility.
- Dark palette has dimmer backgrounds and brighter foregrounds; not simple inversions.
- Contrast: "make sure the contrast ratio between colors is **no lower than 4.5:1**. For custom
  foreground and background colors, strive for a contrast ratio of **7:1**, especially in small
  text."
- Soften large white image backgrounds in dark contexts so they do not glow.

## Project application
- Define semantic CSS custom properties on `:root` (`--bg`, `--surface`, `--text`, `--text-muted`,
  `--border`, `--accent`) with dark overrides under `prefers-color-scheme: dark` and the existing
  manual theme attribute; add an increased-contrast override under `@media (prefers-contrast:
  more)`. The site already declares `<meta name="color-scheme" content="light dark">`.
- Sentiment colours (positive/neutral/negative) must never be the only cue: pair with text label or
  icon/shape, per "not solely colour". See the `sentiment-visuals` skill.
- Do not hard-code values copied from Apple's tables (they say values fluctuate); pick project
  tokens and verify contrast: text >= 4.5:1 (7:1 for small text where feasible), per Dark Mode page.
- Keep accent colour for the primary action (e.g. "Analyze") only; avoid tinting several controls.
- Offering an in-app theme toggle conflicts with the HIG's "avoid app-specific appearance setting";
  the existing toggle defaults to "system" which is acceptable, but keep system as the default.
