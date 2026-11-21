# San Francisco fonts: what Apple's fonts page and licence say

Sources:
- https://developer.apple.com/fonts/ (HTML fetched with curl; embeds the licence text for SF)
- Typography guidance: https://developer.apple.com/design/human-interface-guidelines/typography
- Downloads listed on the page (not downloaded):
  https://devimages-cdn.apple.com/design/resources/download/SF-Pro.dmg (also SF-Compact, SF-Mono,
  SF-Arabic, SF-Armenian, SF-Georgian, SF-Hebrew, NY .dmg)
Fetched: 2026-11-21
Not found: a separate stand-alone SF Pro licence PDF link. The licence text is shown in-page in
"LICENSE AGREEMENT FOR THE APPLE SAN FRANCISCO FONT" (subtitle "For iOS, OS X and tvOS application
uses only") and a second one for SF Compact (watchOS). The SF Pro .dmg's own licence may differ
(unverified).

## What the fonts page says
- Describes San Francisco as "the system font for Apple platforms"; SF Pro has "nine weights,
  variable optical sizes ... four widths, and includes a rounded variant" and "supports over 150
  languages across Latin, Greek, and Cyrillic scripts".
- Purpose of the download: "Get the typefaces you need to design interfaces for your apps on Apple platforms."
- Also lists SF Compact, SF Mono, New York (NY), and script extensions (Arabic, Armenian, Georgian, Hebrew).

## Exact licence restriction (quoted from the page)
- Headline: "THE APPLE SAN FRANCISCO FONT IS TO BE USED SOLELY FOR CREATING MOCK-UPS OF USER
  INTERFACES TO BE USED IN SOFTWARE PRODUCTS RUNNING ON APPLE'S iOS, OS X OR tvOS OPERATING SYSTEMS,
  AS APPLICABLE."
- Section 2: "...you may use the Apple Font solely for creating mock-ups of user interfaces to be
  used in software products running on Apple's iOS, OS X or tvOS operating systems..."
- "You may use this Apple Font only for the purposes described in this License and only if you are a
  registered Apple Developer, or as otherwise expressly permitted by Apple in writing."
- "...you agree not to, install, use or run the Apple Font for the purpose of creating mock-ups of
  user interfaces to be used in software products running on any non-Apple operating system or to
  enable others to do so. **You may not embed the Apple Font in any software programs or other
  products.** Except as expressly provided for herein, you may not use the Apple Font to, create,
  develop, display or otherwise distribute any documentation, artwork, **website content** or any
  other work product."
- Also: may not make it "available over a network where it could be run or used by multiple
  computers at the same time"; may not "rent, lease, lend, trade, transfer, sell, sublicense or
  otherwise redistribute" it; no reverse engineering or derivative works.
- Typography page developer note: "don't embed system fonts in your app or game."

## Why the web project must use the system font stack
- Self-hosting SF Pro (e.g. an `@font-face` pointing at a `.woff2` in `site/`) means
  embedding/redistributing it in website content on a non-Apple-only deployment: the licence above
  forbids that. Do not copy SF files from the .dmg, from macOS, or from third-party mirrors.
- The system font stack is not embedding: the browser asks the OS for its own installed font. On
  Apple devices this renders San Francisco; elsewhere it falls back to the platform UI font.
- Recommended stack (CSS convention; the Apple pages do not prescribe it, so this exact string is a
  project choice):
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
/* or: font-family: system-ui, -apple-system, ...; */
font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; /* code/numeric */
```
- Notes: `-apple-system` (Safari/WebKit, Firefox on Apple) and `BlinkMacSystemFont` (Chrome on
  macOS) map to the system font; `system-ui` is the generic keyword. Browser mapping details are
  (unverified) - not on the fetched pages.
- Never use a `src: local("SF Pro")` plus a bundled fallback of SF; local() is fine technically but
  offers no benefit over the stack.
- If a distinctive typeface is wanted on all platforms, choose an open-licensed font (e.g. under the
  SIL OFL) and self-host it with its licence file; that is a separate decision with the Netlify
  no-external-requests rule.

## Project application
- Add one CSS custom property `--font-sans` with the stack above; do not add font files or Google
  Fonts links (also avoids third-party requests, in keeping with the "no outside servers" rule).
- Document in the About/credits page: "Typeset in the visitor's system font" - no font attribution needed.
- Do not describe the site as using "SF Pro" in marketing text; on non-Apple devices it will not.
- Mockups/screenshots of the site for the report are fine to produce on any system font, but do not
  publish design files that embed SF (the licence is for Apple-platform UI mockups only).
- This is a summary of licence text, not legal advice; escalate to the orchestrator if a legal
  question remains.
