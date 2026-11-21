# Apple HIG: Layout

Sources:
- https://developer.apple.com/design/human-interface-guidelines/layout
- Data fetched from: https://developer.apple.com/tutorials/data/design/human-interface-guidelines/layout.json
Fetched: 2026-11-21
Not found on this page (unverified): numeric standard margin values for iPhone/iPad (the page refers
to system layout guides and Apple Design Resources templates rather than listing them in the
extracted text).

## Visual hierarchy
- **Order by importance:** people read top to bottom and leading to trailing, so "place the most
  important items near the top and leading side".
- **Align** elements to ease scanning; "People assume that aligned items are related to each other";
  indentation signals subordination.
- **Group related items** with negative space, container shapes or separator lines.
- **Progressive disclosure:** reduce initial content with disclosure controls, menus, nested views,
  or scrollable sections.
- **Differentiate controls from content:** use Liquid Glass for controls; "Instead of applying a
  solid or semi-opaque background color beneath controls, use a scroll edge effect to visually
  elevate controls above content." Extend full-screen background content beneath sidebars, toolbars
  and tab bars. A background extension effect flips and blurs an image to appear to extend under
  adjacent components.

## Adaptability
- Layouts must adapt to screen size, orientation, window size, multitasking, text-size changes, and
  locale (LTR/RTL, date/number formats, text length).
- "Design a layout that adapts gracefully and consistently" by respecting system-defined safe areas,
  margins and guides.
- **Text-size changes:** horizontally adjacent views may need to stack vertically; table rows grow
  in height so text is not cropped or overlapped; single-line rows may need multiple lines.
- Preview on multiple devices, size classes, localisations and text sizes; test the largest and
  smallest layouts first.
- Scale background art to fill, never change its aspect ratio.

## Size classes (iOS/iPadOS)
- Two classes per dimension: compact or regular (narrow vs wide, short vs tall).
- "Determine layout based on size classes, not device type or orientation" - size classes describe
  the actual space available.
- "Keep functionality the same as size classes change": change how much is visible, not what the app
  can do. Larger spaces can switch a tab bar to a sidebar or expose items otherwise in an overflow
  menu. Keep layout recognisable and familiar when resizing.

## Guides and safe areas
- A **layout guide** is a rectangular region for positioning, aligning and spacing; system guides
  give standard margins and "restrict the width of text for optimal readability".
- A **safe area** is the part of a window not covered by hardware features or by bars (toolbar, tab
  bar, status bar). "Respecting the safe area is essential" so the Dynamic Island etc. do not
  obstruct content.

## Platform notes (relevant bits)
- macOS: avoid placing controls or critical info at the bottom of a window (windows are often
  dragged below the screen edge); avoid content behind the camera housing.
- tvOS safe area: 60 pt top/bottom, 80 pt sides (irrelevant to this web app).

## Project application
- Page structure mirrors the two-layer model: sticky nav (header + tablist) as the **navigation
  layer**, panels as the **content layer**. Keep content visible beneath/behind the nav only if text
  contrast survives (see UI note 01).
- Hierarchy: put the key result (overall sentiment, top phrases) at the top-left of the dashboard;
  the live-analyzer result directly under its input; group NLTK vs spaCy outputs with the existing
  badges and headings rather than extra colour.
- Layout by **available width (CSS media/container queries), not device type**: translation of "size
  classes". Suggested: compact < ~600px (stacked, tab strip scrolls or wraps), regular >= ~600-900px
  (multi-column grids). Breakpoint numbers are a project choice, not Apple's.
- Keep functionality identical at every width (all four tabs, same data); only reflow.
- Safe areas on the web: add `<meta name="viewport" content="width=device-width, initial-scale=1,
  viewport-fit=cover">` only if the design extends under the iPhone notch/home bar, and then pad
  with `env(safe-area-inset-*)`. The current page uses a plain viewport meta, which already keeps
  content inside the safe area (browser behaviour, (unverified) on Apple page).
- Readable line length: cap prose/review text at about 60-75 characters (`max-width: 65ch`) - the
  HIG says guides restrict text width but gives no number (the number is a general typographic rule,
  (unverified)).
- Text growth: let cards grow vertically, stack label + value at large text sizes, avoid fixed
  heights and truncating reviews.
- Use `gap`/spacing tokens (e.g. 4/8/12/16/24) to keep consistent alignment; 16px side gutter at phone width.
