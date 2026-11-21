# Apple HIG: Tab bars

Sources:
- https://developer.apple.com/design/human-interface-guidelines/tab-bars
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/tab-bars.json
Fetched: 2026-11-21
Page change log (as fetched): "June 8, 2026 - Updated terminology and art."; "December 16, 2025 -
Updated guidance for Liquid Glass."; "July 28, 2025 - Added guidance for Liquid Glass."
Not found (unverified): any exact maximum number of tabs for iPhone (the page says "appropriate
number" and mentions a More tab on overflow); text of the tab bar height on iOS.

## Definition and when to use
- "A tab bar lets people navigate between top-level sections of your app" and preserves navigation
  state within each section.
- **Navigation, not actions:** for controls acting on the current view, use a toolbar.

## Best practices
- Keep the tab bar **visible** while moving between sections; hiding it makes people forget where
  they are (exception: a modal covering it).
- **Number of tabs:** weigh the complexity of added tabs against the need to reach each section;
  fewer is easier. For complex structures consider a sidebar or a tab bar that adapts to a sidebar.
- **Avoid overflow tabs:** when space is short the trailing tab becomes a "More" tab (iOS/iPadOS)
  that hides content; limit this.
- **Do not disable or hide tab buttons** when content is unavailable ("makes your app's interface
  appear unstable and unpredictable"); explain why a section is empty.
- **Labels:** include tab labels; "Use single words whenever possible."
- **Icons:** SF Symbols; in compact views icons sit above labels, in regular views side by side;
  prefer filled symbols for consistency.
- **Badges** (red oval, white number or "!") only for critical information.
- **Colour:** "Avoid applying a similar color to tab labels and content layer backgrounds"; over
  colourful content prefer a monochrome tab bar or a clearly different accent (see Liquid Glass
  color).

## Platform behaviour
- **iOS:** the tab bar "floats above content at the bottom of the screen", items rest on a Liquid
  Glass background; it can minimise on scroll (with an accessory such as a MiniPlayer moving inline)
  and reopen on tab tap or scroll to top; a trailing search tab is possible.
- **iPadOS:** tab bar near the top; either fixed or with a button converting it to a sidebar
  (`sidebarAdaptable`). "Prefer a tab bar for navigation"; let people customise tabs (default list
  of **five or fewer** for continuity between compact and regular sizes). To get a sidebar only, use
  a navigation split view.
- **macOS:** no additional considerations. **watchOS:** not supported.
- **tvOS:** translucent, highly customisable; height 68 pt; top edge 46 pt from the screen top.
- **visionOS:** vertical, floating at the window's leading side, expands when looked at; supply
  symbol and short text label per tab; a sidebar inside a tab is allowed for deep hierarchies
  without changing the open tab.

## Project application
- The site's four tabs (Dashboard, Reviews & examples, Analyze your own review, About & method) fit
  "top-level sections": keep exactly these as peers; actions (Analyze, theme toggle, filters) belong
  in the panels or header, not as tabs.
- Count is within the HIG's "fewer is easier" spirit (4). If a 5th appears, reconsider before
  adding; avoid horizontally scrolling "More" patterns on phones.
- **Labels are long** ("Analyze your own review"). HIG says single words where possible: consider
  shorter visible labels (e.g. "Dashboard", "Reviews", "Analyze", "About") with the long wording
  kept in `aria-label`/panel headings. Visible label text must still contain the accessible name
  start (WCAG label-in-name).
- Keep all tabs enabled at all times; if "Analyze" is waiting on Pyodide, keep the tab and show a
  loading/empty-state explanation inside the panel (HIG: don't disable tabs, explain why).
- Always visible: make the tablist sticky (top on desktop, optionally bottom on phones) with solid
  or regular-variant glass background; do not colour the labels the same as card backgrounds.
- Mobile: tab targets >= 44px high; if four labels do not fit at 320px, wrap or horizontally scroll
  the strip with visible overflow cue rather than hiding items. Icon + short label on phone,
  label-only on desktop mirrors compact vs regular.
- Desktop adaptation: at wide widths a left sidebar listing the same four sections is allowed (see
  04-sidebars.md), but it must expose identical functionality; start with the simple top tab bar.
- Preserve per-tab state (scroll position, selected filters) when switching, as the HIG says tab
  bars "preserv[e] the current navigation state within each section". Use the URL hash (`#live`) so
  tabs are linkable.
- Keep the existing ARIA tabs pattern (`role=tablist/tab/tabpanel`, roving tabindex).
