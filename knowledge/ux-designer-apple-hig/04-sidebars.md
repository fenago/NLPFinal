# Apple HIG: Sidebars

Sources:
- https://developer.apple.com/design/human-interface-guidelines/sidebars
- Data fetched from:
  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/sidebars.json
Fetched: 2026-11-21
Page change log (as fetched): "June 8, 2026 - Updated guidance for sidebar icon colors, and
clarified guidance for the adaptable sidebar style."; "June 9, 2025 - Added guidance for extending
content beneath the sidebar."

## Definition and when to use
- "A sidebar appears on the leading side of a view and lets people navigate between areas of your
  app or top-level collections of content, like folders and playlists."
- It "requires a large amount of vertical and horizontal space". When space is limited, or you want
  more room for content, a tab bar may be better. For many apps you need not choose: a tab bar style
  that provides both (adaptable).

## Best practices
- **Extend visually rich content beneath the sidebar:** in iOS, iPadOS and macOS sidebars can float
  above content in the Liquid Glass layer; let content scroll horizontally beneath or apply a
  background extension effect (mirrors adjacent content to look stretched under the sidebar).
- **Customisation:** where possible let people choose which areas appear and their order.
- **Hierarchy:** group with disclosure controls for large content sets; "show no more than **two
  levels** of hierarchy"; for deeper data use a split view with a content list between sidebar and
  detail. With two levels use succinct group labels.
- **Icons:** familiar symbols (SF Symbols or custom symbols rather than bitmaps). Icons use the app
  accent colour by default; honour the system accent colour on macOS; fixed colours only when they
  clarify meaning (example: Mail's yellow VIP icon).
- **Hiding:** let people hide/show the sidebar using platform interactions (iPadOS edge swipe; macOS
  show/hide button or View menu commands); "Avoid hiding the sidebar by default to ensure that it
  remains discoverable."

## Platform considerations
- **iOS/iPadOS:** `sidebarAdaptable` tab view lets you choose to open with a sidebar or tab bar,
  with a button to switch, and it responds to rotation and window resizing. Sidebar only:
  NavigationSplitView or UISplitViewController. "Consider using a tab bar first" - more room for
  content, flexible enough for many apps; the convertible sidebar exposes less-used content.
- **macOS:** row height, text and glyph size depend on sidebar size (small, medium, large),
  user-changeable in General settings; consider auto-hiding when the window shrinks; "Avoid putting
  critical information or actions at the bottom of a sidebar" (windows move off-screen).
- **visionOS:** for deep hierarchies use a sidebar inside a tab, and make sure sidebar selection
  does not change which tab is open.
- **tvOS:** nothing extra; **watchOS:** not supported.

## Project application
- This site is a four-section app, so a sidebar is unnecessary on phones; HIG says "consider a tab
  bar first". Use a sidebar only at large desktop widths if the nav ever grows, and keep identical
  sections/functionality (HIG: functionality must not change with space).
- If one is built: web translation of the glass-layer idea = sticky `<nav>` column with
  regular-variant glass over a solid page background; do not place the primary chart grid under
  translucency.
- At most two nav levels; do not nest filters inside it. Use real `<nav aria-label="...">` with a
  list of links, a visible `aria-current="page"` state, and not colour alone for the active item.
- Provide a show/hide toggle (button with `aria-expanded`) and do not hide the sidebar by default at
  desktop widths so it stays discoverable; on narrow widths collapse to the tab strip (the
  "adaptable" pattern).
- Do not put critical actions at the bottom of the sidebar (the page can be viewed in short windows).
- Any icons need text labels (not icon-only), and must keep contrast >= 3:1 for graphical objects
  (WCAG; not stated on the Apple page).
