# Apple: Adopting Liquid Glass (technology overview)

Sources:
- https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- Data fetched from:
  https://developer.apple.com/tutorials/data/documentation/TechnologyOverviews/adopting-liquid-glass.json
  (HTTP 200)
Fetched: 2026-11-21
Note: the fetched JSON omits the code-API link lists; where the page says "using the following APIs"
the names are not in this text (unverified).

## Core idea
- "Adopting Liquid Glass doesn't mean reinventing your app from the ground up." Standard
  SwiftUI/UIKit/AppKit components get the new look automatically when built with the latest SDK.
- Liquid Glass "combines the optical properties of glass with a sense of fluidity" and "forms a
  distinct functional layer for controls and navigation elements".

## Visual refresh: key practices
- Reduce custom backgrounds in controls and navigation elements; they "might overlay or interfere
  with Liquid Glass or other effects", e.g. the scroll edge effect. Check split views, tab bars,
  toolbars.
- **Test with display and accessibility settings.** People can pick a preferred Liquid Glass look,
  or turn on settings that "reduce transparency or motion". "These settings can remove or modify
  certain effects." Test custom elements, colors and animations under those configurations.
- **Avoid overusing** glass on custom controls; limit it to "the most important functional elements".

## Controls
- Controls get rounder shapes (hardware-informed curvature); sliders/toggles' knobs become glass
  while interacting; buttons morph into menus/popovers; an extra-large control size exists.
- Be judicious with colour in controls and navigation. If colour is used, "leverage system colors,
  or define a custom color with light and dark variants, and an increased contrast option for each
  variant."
- **Avoid crowding or layering glass elements on top of each other**; use standard spacing metrics.
- **Legibility under scrolling content:** the scroll edge effect obscures content scrolling beneath
  controls to keep contrast.
- Use rounded shapes concentric with their containers for visual continuity.

## Navigation
- "Liquid Glass applies to the topmost layer of the interface, where you define your navigation."
  Tab bars and sidebars float in this layer.
- "Establish a clear navigation hierarchy ... clearly separate your content from navigation elements
  ... to establish a distinct functional layer above the content layer."
- A tab bar can adapt into a sidebar on larger contexts; split views suit sidebar + inspector
  layouts; a **background extension effect** mirrors and blurs adjacent content to appear to extend
  under a sidebar.
- iOS tab bars can minimise when scrolling and expand when scrolling the other way.

## Menus, toolbars, sheets, lists
- Menus/toolbars adopt glass; group toolbar items by function; do not mix text and icons within
  items sharing a background; "Provide an accessibility label for every icon."
- Half sheets are inset so content peeks through; expanded to full height they become "more opaque
  ... to help maintain focus on the task."
- Lists/forms have larger row height and padding; section headers use title-style capitalisation (no
  all-caps).
- Search: semantic search tab at trailing end of the tab bar; search field slides up with keyboard.

## Platform and performance
- Combine custom glass effects (GlassEffectContainer) for rendering performance; profile performance
  across platforms.
- `UIDesignRequiresCompatibility` Info key keeps the pre-Liquid-Glass look when shipping with the new SDK.

## Project application
- Translate the principles, not the APIs: a **distinct navigation layer** (header + tab strip) over
  a **content layer** (cards, charts) with clear separation; no custom heavy backgrounds fighting
  the glass; no glass-on-glass.
- "Test with accessibility settings" becomes: test with OS Reduce Transparency, Increase Contrast,
  Reduce Motion, light/dark, 200% text zoom, via the media queries in
  07-css-user-preference-media.md.
- Icon-only controls (e.g. a theme toggle) need an accessible name (`aria-label`), matching
  "accessibility label for every icon".
- Concentric rounding: inner radius = outer radius minus padding (CSS translation of the concentric guidance).
- Section headings: use sentence/title case rather than all caps, matching the title-style convention.
