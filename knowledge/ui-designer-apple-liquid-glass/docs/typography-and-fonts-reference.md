# Typography and fonts reference (HIG Typography + SF font license)

## Why this matters
Type size, weight and font choice drive legibility and hierarchy. Apple's
guidance is detailed, but Apple's San
Francisco font cannot be shipped on a website, so the site must use the
visitor's system font stack and borrow
only the sizing and hierarchy ideas.

## Official sources
- https://developer.apple.com/design/human-interface-guidelines/typography
- https://developer.apple.com/fonts/ (page embeds the "LICENSE AGREEMENT FOR THE
  APPLE SAN FRANCISCO FONT")
- Detail notes: ../04-typography.md, ../05-sf-fonts-license.md
- Fetched 2026-11-21 (Typography change log: Dec 16, 2025 added emphasized
  weights).

## Key rules (Typography)
- Defaults / minimums: iOS and iPadOS 17 pt / 11 pt; macOS 13 / 10; tvOS 29 /
  23; visionOS 17 / 12; watchOS 16 / 12.
- "In general, avoid light font weights": prefer Regular, Medium, Semibold,
  Bold; avoid Ultralight, Thin, Light.
- Show hierarchy with weight, size and colour; "Minimize the number of typefaces
  you use".
- Use built-in text styles (they bundle size, weight, leading). iOS Large
  defaults: Large Title 34/41, Title 1 28/34,
  Title 2 22/28, Title 3 20/25, Headline 17/22 semibold, Body 17/22, Callout
  16/21, Subhead 15/20, Footnote 13/18,
  Caption 1 12/16, Caption 2 11/13.
- Support text enlargement (Dynamic Type): adapt layout, stack inline items,
  avoid truncation, keep hierarchy.
- Loose leading helps long passages in wide columns.
- System fonts: SF (sans) and New York (serif); developer note: "don't embed
  system fonts in your app or game."

## Key rules (SF font license, as shown on the fonts page)
- "THE APPLE SAN FRANCISCO FONT IS TO BE USED SOLELY FOR CREATING MOCK-UPS OF
  USER INTERFACES TO BE USED IN
  SOFTWARE PRODUCTS RUNNING ON APPLE'S iOS, OS X OR tvOS OPERATING SYSTEMS, AS
  APPLICABLE."
- "You may not embed the Apple Font in any software programs or other products."
- Use is limited to registered Apple Developers "or as otherwise expressly
  permitted by Apple in writing".
- You may not "create, develop, display or otherwise distribute any
  documentation, artwork, website content or any
  other work product" with it; no redistribution, no use for non-Apple OS
  mock-ups.
- No separate SF Pro license PDF was found; the SF Pro .dmg's own license may
  differ (unverified). Not legal advice.

## Do / Don't
| Do | Don't |
|---|---|
| `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | `@font-face` with SF Pro files |
| Body about 17px / 1.0625rem, line-height ~1.3 | Body text below ~12px |
| Weights 400-700 | Weights 100-300 |
| One family; `ui-monospace` for code | Mix several display faces |
| Use `rem` so user text settings scale | Fixed px heights that clip enlarged text |

## Translate to the web
- Apple points are logical units; treating 17 pt as about 17 CSS px is a
  translation, not an Apple statement.
- Scale (px, from the iOS Large table, adapted): h1 34, h2 28, h3 22, h4 20,
  body 17, secondary 15, caption 12-13.
- Define `--font-sans` once; no font files, no Google Fonts links (also avoids
  third-party requests).
- Apple devices will render SF through the system stack; other platforms get
  their own UI font, so do not call the
  site "set in SF Pro".
- Verify at 200% zoom and 320px width with no clipped or truncated review text.

