# Apple HIG: Materials (Liquid Glass and standard materials)

Sources:
- https://developer.apple.com/design/human-interface-guidelines/materials
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/materials.json
Fetched: 2026-11-21
Page change log (as fetched): "September 9, 2025 - Updated guidance for Liquid Glass."; "June 9,
2025 - Added guidance for Liquid Glass."

## What a material is
- "A material is a visual effect that creates a sense of depth, layering, and hierarchy between
  foreground and background elements."
- Materials separate foreground (text, controls) from background (content, solid colors) by letting
  color pass through from background to foreground.
- Two kinds on Apple platforms: **Liquid Glass** (controls and navigation) and **standard
  materials** (differentiation inside the content layer).

## Liquid Glass: where it belongs
- Liquid Glass "forms a distinct functional layer for controls and navigation elements - like tab
  bars and sidebars - that floats above the content layer".
- Content scrolls and peeks through beneath it, giving depth while keeping controls legible.
- **Do not use Liquid Glass in the content layer.** It works best when it separates interactive
  elements from content; in the content layer it adds "unnecessary complexity and a confusing visual
  hierarchy". Use standard materials for content-layer elements such as app backgrounds.
- Exception: transient interactive controls in the content layer (sliders, toggles) take on a glass
  look while a person is activating them.
- **Use sparingly.** System components pick it up automatically. For custom controls, limit it to
  "the most important functional elements"; overuse "distract[s] from that content".

## Regular vs clear variants
- Two variants: **regular** and **clear**. Their look can change with system settings (a user-chosen
  Liquid Glass look, or accessibility settings that reduce transparency or increase contrast).
- **Regular**: blurs and adjusts the luminosity of background content to keep text and foreground
  legible. Scroll edge effects add legibility by blurring and reducing opacity of background
  content. Most system components use it.
  - Use regular "when background content might create legibility issues, or when components have a
    significant amount of text, such as alerts, sidebars, or popovers."
- **Clear**: "highly translucent", prioritises visibility of underlying content. "Only use clear
  Liquid Glass for components that appear over visually rich backgrounds" - best over media such as
  photos and videos for an immersive feel.

## Dimming guidance for clear glass
- Decide whether to add a dimming layer behind clear-glass components, for contrast and legibility:
  - Underlying content **bright**: "consider adding a dark dimming layer of 35% opacity".
  - Underlying content **sufficiently dark** (or standard AVKit playback controls that bring their
    own dimming): no dimming layer needed.
- The page points to "Liquid Glass color" (see 03-color.md) for colour use.

## Standard materials
- Use blur, vibrancy and blending "to convey a sense of structure in the content beneath Liquid Glass".
- Choose by **semantic meaning and recommended usage**, not by the colour it appears to produce
  (system settings can change appearance).
- Put **vibrant colors on top of materials** so legibility holds in any context.
- Thickness trade-off: thicker (more opaque) = better contrast for fine text; thinner (more
  translucent) = keeps context visible.
- iOS/iPadOS standard materials: ultra-thin, thin, regular (default), thick. Vibrancy levels for
  labels: label, secondary, tertiary, quaternary (avoid quaternary on thin/ultraThin: "contrast is
  too low"); fills: fill, secondary, tertiary; one separator level.
- macOS: several purpose-built materials and two blending modes (behind window, within window).
- tvOS table: ultraThin = full-screen, light scheme; thin = overlay, light; regular = overlay; thick
  = overlay, dark scheme.
- visionOS: system "glass"; prefer translucency to opaque colors in windows. watchOS: keep default
  modal material backgrounds.

## Project application
- This is a static HTML/CSS site; Apple's APIs do not apply, only the principles. Web approximation
  of glass is `backdrop-filter` (see 06-css-backdrop-filter.md) plus a semi-transparent background.
- Glass belongs on the **navigation layer only**: sticky site header and the tab strip
  (`role="tablist"` in `site/index.html`). Cards, chart panels, review text and the live-analyzer
  form stay on solid/standard surfaces.
- Prefer the **regular** (blur + higher-opacity tint) recipe: the dashboard has dense text and
  charts scrolling beneath the header. "Clear" glass is for photo/video backgrounds; this app has
  none, so do not use it.
- If a decorative gradient/image sits behind a glass bar and is bright, apply the HIG's idea of a
  ~35% dark dimming layer (translation: `rgb(0 0 0 / .35)` overlay behind the bar). Verify text
  contrast numerically instead of trusting the number.
- Always provide an opaque fallback when `backdrop-filter` is unsupported or the user asks for
  reduced transparency (see 07-css-user-preference-media.md).
- Limit glass to 1-2 elements; do not stack glass on glass.
