# Apple HIG: Typography

Sources:
- https://developer.apple.com/design/human-interface-guidelines/typography
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/typography.json
Fetched: 2026-11-21
Page change log (as fetched): "December 16, 2025 - Added emphasized weights to the Dynamic Type
style specifications"; "March 7, 2025 - Expanded guidance for Dynamic Type."

## Legibility: default and minimum sizes
| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |
- Follow these for custom and system fonts. A thin custom weight needs sizes larger than the recommendation.
- "In general, avoid light font weights": prefer Regular, Medium, Semibold or Bold; avoid
  Ultralight, Thin, Light, "which can be difficult to see, especially when text is small."
- If text is hard to read: larger size, more contrast, or typefaces designed for legibility "like
  the system fonts".

## Hierarchy
- Use weight, size and colour to show importance and keep relative hierarchy when text size changes.
- "Minimize the number of typefaces you use"; too many obscure hierarchy.
- When people enlarge text they do not expect everything to grow (e.g. tab titles in a tabbed window
  should not grow).

## System fonts
- Two families: **San Francisco (SF)** sans serif (SF Pro, SF Compact, SF
  Arabic/Armenian/Georgian/Hebrew, SF Mono; rounded variants exist) and **New York (NY)** serif.
- SF Pro is the system font on iOS, iPadOS, macOS, tvOS and visionOS; SF Compact on watchOS.
- Variable fonts with **dynamic optical sizes** (Text/Display merged into one continuous design);
  weights Ultralight to Black; SF has several widths.
- Developer note (verbatim idea): use Font.Design constants to get system fonts - "don't embed
  system fonts in your app or game."
- In mockups you may need to adjust **tracking** manually; a running app adjusts tracking at every point size.

## Text styles and Dynamic Type
- Text styles bundle weight, size and leading; they scale with Dynamic Type. Use built-in styles;
  modify with symbolic traits (bold, looser or tighter leading; loose leading helps long passages in
  wide columns).
- Dynamic Type: iOS, iPadOS, tvOS, visionOS, watchOS (not macOS). Verify layouts at all sizes incl.
  Larger Accessibility sizes; scale meaningful icons; keep truncation minimal; stack inline items
  under text at large sizes; reduce columns; keep primary elements near the top.
- iOS/iPadOS **Large (default)** sizes (pt size / leading): Large Title 34/41 Regular; Title 1
  28/34; Title 2 22/28; Title 3 20/25; Headline 17/22 Semibold; **Body 17/22 Regular**; Callout
  16/21; Subhead 15/20; Footnote 13/18; Caption 1 12/16; Caption 2 11/13.
- Smaller iOS size (xSmall) body is 14/19; the largest standard size (xxxLarge) body is 23/29;
  accessibility sizes reach body 53/62 (AX5).
- macOS built-in styles: Body 13/16; Headline 13/16 Bold; Large Title 26/32; Title 1 22/26; Caption 1 10/13.
- Tracking table (SF Pro) exists: e.g. 17 pt = -26/1000 em (-0.43 pt); 12 pt = 0; 11 pt = +6/1000
  em; large sizes loosen again. Useful only for matching mockups.

## Custom fonts
- Must remain legible; implement the accessibility behaviours system fonts get (Dynamic Type, Bold Text).

## Project application
- **Translation, not equivalence:** an Apple point is a logical unit like a CSS pixel; treat 17 pt
  as roughly 17 CSS px = `1.0625rem` at a 16px root. Prefer `rem` so browser text-size settings work
  (HIG: support >= 200% enlargement, see UX note 01).
- Body copy: 16-17px (`1rem`-`1.0625rem`), line-height ~1.3 (22/17). Small captions not below
  ~11-12px; the HIG minimum of 11 pt is a floor, not a target.
- Use weights 400/500/600/700 only; no 100-300.
- Heading scale suggestion from the iOS Large table: 34/28/22/20 for h1-h4 (ratio-adapted for
  desktop), body 17, secondary 15, caption 12-13.
- Font stack: system fonts only (see 05-sf-fonts-license.md); a single family, with `ui-monospace`
  for any code/numeric tables.
- Do not shrink tab labels or critical controls when text scales; let layout reflow instead (stack,
  wrap), and avoid truncating review text.
