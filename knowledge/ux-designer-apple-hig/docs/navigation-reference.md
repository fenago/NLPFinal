# Navigation reference (HIG Tab bars + Sidebars + Layout)

## Why this matters
Navigation structure decides whether people can find the four sections of this
app on a phone and on a wide
desktop. The HIG favours a small set of persistent top-level sections, a sidebar
only when space and structure
justify it, and layouts that adapt by available space without changing
functionality.

## Official sources
- https://developer.apple.com/design/human-interface-guidelines/tab-bars
- https://developer.apple.com/design/human-interface-guidelines/sidebars
- https://developer.apple.com/design/human-interface-guidelines/layout
- Detail notes: ../02-layout.md, ../03-tab-bars.md, ../04-sidebars.md
- Fetched 2026-11-21 (tab bars and sidebars changelogs both list June 8, 2026
  updates).

## Key rules
- Tab bar: "navigate between top-level sections"; "to support navigation, not to
  provide actions" (use a toolbar).
- Keep the tab bar visible; hiding it makes people forget where they are.
- Few tabs: "easier to navigate among fewer tabs"; avoid overflow "More" tabs.
  No exact iPhone maximum was on the page (unverified).
- "Don't disable or hide tab bar buttons, even when their content is
  unavailable"; explain empty sections.
- Labels: "Use single words whenever possible"; filled icons; badges only for
  critical information.
- Avoid tab labels coloured like content backgrounds.
- iOS: tab bar floats at the bottom on glass; iPadOS: top tab bar convertible to
  a sidebar; customisable tabs: five or fewer.
- Sidebar: leading side; for areas or top-level collections; needs a lot of
  space, so "a tab bar may provide a better
  navigation experience" when space is limited; "Consider using a tab bar first"
  on iOS/iPadOS.
- Sidebar structure: no more than two levels; disclosure groups; let people hide
  it, but "Avoid hiding the sidebar by
  default"; keep critical actions away from the bottom edge (macOS).
- Layout: important content near top and leading side; align, group, progressive
  disclosure; differentiate controls
  from content; extend backgrounds beneath bars.
- Adaptability: "Determine layout based on size classes, not device type or
  orientation"; "Keep functionality the same
  as size classes change"; larger space may swap a tab bar for a sidebar.
- Safe areas: keep content clear of hardware features and bars; system guides
  also limit text width for readability.

## Do / Don't
| Do | Don't |
|---|---|
| Keep four peer sections as tabs | Put actions (Analyze, filters) in the tab bar |
| Shorten visible tab labels, keep long names in `aria-label` | Rely on a truncated long label |
| Keep every tab enabled and explain loading states | Disable "Analyze" tab until Pyodide loads |
| Reflow by width, same features everywhere | Remove features on phones |
| Make nav sticky and visible | Hide nav on scroll without a way back |
| Cap sidebar nesting at two levels | Nest filters inside navigation |

## Translate to the web
- Phones: sticky tab strip with >= 44px targets; wrap or scroll with a visible
  overflow cue at 320px.
- Wide screens: keep the top tab strip; add a left `<nav>` sidebar only if
  sections grow, with `aria-current="page"`,
  an `aria-expanded` toggle, and not shown collapsed by default at desktop
  width.
- Use media/container queries as the "size class" translation; breakpoints are a
  project choice, not Apple's.
- Keep the existing ARIA tablist pattern (`role=tab`, roving tabindex); preserve
  per-tab state and use URL hashes.
- Cap prose width around 65ch (typographic convention, not Apple) and use
  `env(safe-area-inset-*)` only with `viewport-fit=cover`.
- Related skills: `apple-navigation-patterns`, `apple-layout-spacing`.

