# MDN: `backdrop-filter`

Sources:
- https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter (human-facing URL; slug in
  source: Web/CSS/Reference/Properties/backdrop-filter; developer.mozilla.org itself was not
  fetchable)
-
  https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/properties/backdrop-filter/index.md
  (fetched)
Fetched: 2026-11-21
Browser support: the markdown source only embeds a `{{Compat}}` table (key
`css.properties.backdrop-filter`); no support statement is in the text, so version numbers are
(unverified). Check
https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter#browser_compatibility or caniuse
before relying on it.

## What it does
- Applies "graphical effects such as blurring or color shifting to the area behind an element".
  Because it affects what is *behind*, "the element or its background needs to be transparent or
  partially transparent" to see the effect.
- Page-type: CSS property.

## Syntax
- `none` - no filter.
- A space-separated `<filter-value-list>` of filter functions or an SVG filter `url(...)`.
- Functions: `blur()`, `brightness()`, `contrast()`, `drop-shadow()`, `grayscale()`, `hue-rotate()`,
  `invert()`, `opacity()`, `sepia()`, `saturate()`.
- Multiple filters are space-separated: `backdrop-filter: url("filters.svg#filter") blur(4px) saturate(150%);`
- Global values inherit/initial/revert/revert-layer/unset.
- Doc examples: `backdrop-filter: blur(2px);` `backdrop-filter: saturate(80%);` and the main example:
```css
.box {
  background-color: rgb(255 255 255 / 30%);
  backdrop-filter: blur(10px);
}
```

## Backdrop root (stacking/containing notes)
- The effect covers pixels painted behind the element **up to the nearest ancestor that is a
  "backdrop root"**; content above the root is not affected.
- Backdrop roots: the `html` root; an element with `filter` other than `none`; `opacity` < 1;
  `mask`/`mask-image`/`mask-border`/`clip-path` other than `none`; `backdrop-filter` other than
  `none`; `mix-blend-mode` other than `normal`; or `will-change` naming any of those.
- Consequence quoted from the page: if a parent has `opacity: 0.9`, it becomes a backdrop root, so a
  child's blur only covers content between that parent and the child, "not the content behind the
  parent. This is a common source of confusion when `backdrop-filter` appears to have no visible
  effect despite being correctly applied."
- Nested glass (an element with `backdrop-filter` inside another) therefore blurs only up to the outer one.
- The page does not discuss containing-block/fixed-position effects separately beyond backdrop roots
  (unverified for other side effects).

## Project application
- Recipe for a regular-variant navigation bar (values are project starting points, not from MDN):
```css
.site-nav {
  position: sticky; top: 0;
  background: rgb(255 255 255 / 0.72);          /* use a dark token in dark mode */
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  backdrop-filter: blur(20px) saturate(160%);
}
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .site-nav { background: var(--surface); }       /* opaque fallback */
}
@media (prefers-reduced-transparency: reduce) { .site-nav { background: var(--surface); -webkit-backdrop-filter: none; backdrop-filter: none; } }
```
- The `-webkit-` prefix is a historical Safari need (unverified on these pages); keep both lines.
- Do not put `opacity`, `filter`, `mask` or `will-change: opacity` on any ancestor of the glass
  element, or the blur will sample the wrong backdrop. Animate with `transform` on siblings instead
  of fading the parent.
- Cost: large blur radii on full-width sticky elements can be expensive on low-end phones (general
  knowledge, (unverified) in these docs). Keep blur modest, one or two glass surfaces, and test on a
  mid-range phone.
- Text on glass still needs contrast: choose the tint so body text meets 4.5:1 against both light
  and dark content scrolling underneath, check the worst case, and add the opaque fallback.
