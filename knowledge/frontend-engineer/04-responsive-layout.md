# 04 - Responsive layout (MDN)

Sources:
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Basic_concepts
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://www.w3.org/WAI/WCAG22/quickref/ (1.4.10 Reflow)

Fetched: 2026-11-20

## Viewport meta
```html
<meta name="viewport" content="width=device-width" />
```
- Tells mobile browsers to use the device width instead of a default like iPhone's 980px.
- Other `content` keys: `height`, `initial-scale`, `maximum-scale`, `minimum-scale`, `user-scalable`, `interactive-widget`, `viewport-fit`.
- Accessibility: do NOT set `user-scalable=no` (or a restrictive `maximum-scale`); it blocks zoom for low-vision users. WCAG requires at least 2x scaling; MDN says best practice is to allow 5x.
- Many projects write `width=device-width, initial-scale=1` (the MDN responsive page's own page metadata shows this form).

## Media queries and mobile-first
- Mobile first: start with a simple single-column layout, then add columns at wider widths.
- Range syntax used by MDN:
```css
@media screen and (width >= 600px) {
  .wrapper { display: flex; }
  .col1 { flex: 1; margin-right: 5%; }
  .col2 { flex: 2; }
}
@media (width >= 1200px) { h1 { font-size: 4rem; } }
```
- Classic `(min-width: 600px)` syntax is equivalent (older browsers; not on fetched page, unverified).
- Media never larger than container: `img, picture, video { max-width: 100%; }`.
- Responsive type: `h1 { font-size: calc(1.5rem + 4vw); }`. Never size text in `vw` alone (breaks zoom).

## Grid (MDN basics)
```css
.wrapper { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; grid-auto-rows: minmax(100px, auto); }
```
- `fr` distributes free space; `repeat(n, 1fr)`; `minmax(min, max)`; `gap`.
- `auto-fill` / `auto-fit` were not on the fetched Basic concepts page. Common responsive card grid: `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));` (unverified here; documented on MDN's repeat() page).

## Flexbox (MDN basics)
```css
.box { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: flex-start; align-items: flex-start; }
.item { flex: 1 1 auto; }   /* flex-grow flex-shrink flex-basis */
```
- Flexbox is one-dimensional (row OR column); grid is two-dimensional. Use flex for toolbars/tab lists, grid for dashboard cards.

## prefers-color-scheme
- Values: `light` (also when no preference expressed) and `dark`.
```css
:root { --bg: #fff; --fg: #1a1a1a; }
@media (prefers-color-scheme: dark) { :root { --bg: #121212; --fg: #eaeaea; } }
body { background: var(--bg); color: var(--fg); }
```
- The `color-scheme` CSS property and `<meta name="color-scheme">` exist so built-in form controls/scrollbars match (pages linked on MDN; contents not fetched, unverified).
- Canvas charts do not read CSS variables automatically; set Chart.js colors from computed style (see dataviz folder).

## Reflow (WCAG 1.4.10, AA)
- No two-dimensional scrolling at 320 CSS px wide for vertically scrolling content, except where 2-D layout is essential (wide tables). Wrap wide tables in a container with `overflow-x: auto` and keep the rest single-column.

## Project application
- Layout: single column on phones; at ~`width >= 48rem` put dashboard cards in a 2-column grid; at `>= 72rem` 3 columns. Tabs row uses flex with `flex-wrap: wrap`.
- Charts sit in a `position: relative` container with a set height (Chart.js requirement) and `min-width: 0` inside grid.
- Define theme tokens as CSS custom properties with a dark-mode media query; test both.
- Test at 320px, 768px, 1280px and with browser zoom 200%.
- Touch targets at least 24x24 px (WCAG 2.5.8); aim for 44px for buttons.
- Keep `<meta name="viewport" content="width=device-width, initial-scale=1">` and never disable zoom.
