# 03 - Accessibility (WCAG 2.2, WAI-ARIA, APG tabs)

Sources:
- https://www.w3.org/WAI/WCAG22/quickref/
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/status_role
- https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

Fetched: 2026-11-20

## WCAG 2.2 success criteria relevant here
| SC | Name | Level | Requirement (short) |
|---|---|---|---|
| 1.1.1 | Non-text Content | A | Non-text content has a text alternative serving the equivalent purpose. |
| 1.3.1 | Info and Relationships | A | Structure/relationships conveyed visually can be programmatically determined or are in text. (Use real headings, lists, `<table>`, `<label>`.) |
| 1.4.1 | Use of Color | A | Color is not the only visual means of conveying information. |
| 1.4.3 | Contrast (Minimum) | AA | Text and images of text have contrast ratio of at least 4.5:1 (exceptions: large text, incidental, logotypes; large text threshold 3:1 per the full SC, unverified on the fetched summary). |
| 1.4.10 | Reflow | AA | No loss of content/function and no two-dimensional scrolling at 320 CSS px width (vertical-scroll content). Exception: content needing 2-D layout (e.g. wide data tables). |
| 1.4.11 | Non-text Contrast | AA | UI components and graphical objects have at least 3:1 contrast against adjacent colors. |
| 2.1.1 | Keyboard | A | All functionality operable via keyboard. |
| 2.4.7 | Focus Visible | AA | Keyboard focus indicator is visible. |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Focused component is not entirely hidden by author-created content (sticky headers!). |
| 2.5.8 | Target Size (Minimum) | AA | Pointer targets at least 24x24 CSS px (with exceptions: spacing, equivalent, inline, UA control, essential). |
| 3.3.2 | Labels or Instructions | A | Labels or instructions are provided when content requires user input. |
| 4.1.3 | Status Messages | AA | Status messages can be programmatically determined through role/properties so AT announces them without receiving focus. |

## Live regions (MDN)
- `aria-live` values: `off` (default), `polite`, `assertive`.
- Pattern: put `aria-live` on an EMPTY element, then update its text with a brief message. Do not move focus to it.
```html
<div id="announce" aria-live="polite"></div>
```
- Live region = the element and its descendants. If the attribute is absent/`off` on the updated element and all ancestors, users are not informed.
- Do not use `assertive` unless interruption is imperative.
- Screen readers buffer content at page load; content inserted together with its live region after load may not be noticed. Create the region in the initial HTML, then change its text.
- `aria-atomic` makes the whole region be read; `aria-relevant` limits which changes are re-read.
- `role="status"`: live region for advisory info not important enough for `alert`. Implicit `aria-live="polite"` and `aria-atomic="true"`. Do not give it focus. Naming it (`aria-label` / `aria-labelledby`) is optional.
- `role="alert"` is the interrupting counterpart (assertive) - use for errors (role details not fetched here, unverified).

## Tabs pattern (WAI-ARIA APG)
Roles:
- `tablist` (container), `tab` (each tab, inside the tablist), `tabpanel` (content for a tab).
Required attributes:
- `aria-selected="true"` on the active tab, `"false"` on others.
- Each `tab` has `aria-controls` -> its `tabpanel` id.
- `tablist` has `aria-labelledby` (visible label) or `aria-label`.
- Each `tabpanel` has `aria-labelledby` -> its tab id.
- If a tabpanel has no focusable content at the start, give it `tabindex="0"`.
Keyboard:
- `Tab`: into the tablist focuses the ACTIVE tab; next `Tab` moves out to the tabpanel (or first focusable inside it).
- `Left Arrow` / `Right Arrow` (horizontal): previous/next tab, wrapping first<->last; optionally activates.
- `Space` / `Enter`: activate tab (if not auto-activated).
- `Home` / `End` (optional): first/last tab.
- `Delete` only if tabs are closable.
- Automatic activation (panel shows on focus) is recommended if panels show without noticeable latency. With two tabs and a heavy Analyze panel (Pyodide), use MANUAL activation or lazy-init on first activation.
- Roving tabindex: active tab `tabindex="0"`, other tabs `tabindex="-1"` (standard APG technique; the fetched summary mentions tabindex only for the panel - unverified).
Skeleton:
```html
<div role="tablist" aria-label="Analyzer views">
  <button role="tab" id="tab-dash" aria-selected="true"  aria-controls="panel-dash" tabindex="0">Dashboard</button>
  <button role="tab" id="tab-live" aria-selected="false" aria-controls="panel-live" tabindex="-1">Analyze your review</button>
</div>
<section role="tabpanel" id="panel-dash" aria-labelledby="tab-dash" tabindex="0">...</section>
<section role="tabpanel" id="panel-live" aria-labelledby="tab-live" tabindex="0" hidden>...</section>
```

## Project application
- Tabs: implement exactly the APG roles/keys above; toggle the `hidden` attribute on inactive panels.
- Form: visible `<label for>` on the review textarea; "Analyze" is a real `<button>`; keep native focus outline or a visible custom one (2.4.7) with a 3:1 contrast against the page (1.4.11).
- Sentiment labels (Positive/Neutral/Negative) must show text or icons in addition to color (1.4.1).
- Results area and Pyodide loading messages: one `role="status"` region ("Loading Python... 40%", "Analysis complete: Positive, compound 0.82"); errors via `role="alert"`.
- Charts/tables: see knowledge/dataviz-specialist for chart alternatives.
- Check light and dark theme contrast separately (4.5:1 text, 3:1 graphics).
- Sticky header must not cover focused elements (2.4.11); add `scroll-margin-top` to focusable targets (technique, unverified).
