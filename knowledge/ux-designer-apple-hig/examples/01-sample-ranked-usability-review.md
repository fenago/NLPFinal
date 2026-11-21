# Worked example 01: a ranked usability review (what good looks like)

> Study this before writing `docs/ux-review.md`. It's a **sample** about a fictional "Recipe Finder" web app, not our app. It shows the structure, evidence and ranking the team expects. Copy the shape, not the findings.

## Summary

Recipe Finder makes its main task (find a recipe from ingredients) easy to start, but hard to finish. Results are slow with no feedback, filters are hidden on phones, and two colour-only signals fail accessibility. **Fix the top 3 first**: together they cover the main flow for every user.

**Scope:** first visit → search → filter → open a recipe → save it. Phone (390×844) and desktop (1280×800), light and dark, with reduce motion / reduce transparency / increase contrast emulated.
**Method:** Nielsen's 10 heuristics + HIG principles (hierarchy, consistency, clarity, feedback) + the accessibility-audit checklist.

## Ranked problems

Rank = severity (0–4) × how often users hit it (1 = rare, 2 = some flows, 3 = every visit).

| # | Problem | Where (evidence) | Heuristic / HIG | Sev | Freq | Score | Fix | Owner | Effort |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Search shows nothing for 3–6 s, so users click again and run the search twice | `#search` submit; screenshot `ux/01-search-blank.png`; network shows 2 identical requests | Visibility of system status · HIG feedback | 3 | 3 | **9** | Show an inline progress row ("Finding recipes with *chicken, rice*…"), disable the button while busy, announce results via `role="status"` | frontend-engineer | S |
| 2 | Filters are behind an unlabeled "⋯" icon on phones | `.filters-toggle` has no text and no `aria-label` | Recognition over recall · HIG clarity | 3 | 3 | **9** | Visible "Filters (2)" button with icon + label; 44×44 px target | frontend-engineer | S |
| 3 | "Vegetarian" is shown only as a green dot | `.diet-dot` | Accessibility: colour not sole indicator | 3 | 2 | **6** | Add a text tag "Vegetarian" plus an icon; keep the colour as a secondary cue | ui-designer | S |
| 4 | Glass header makes the page title unreadable over food photos | `header.glass` over the hero image; measured 2.1:1 | HIG materials (glass on controls, legibility) | 2 | 3 | **6** | Use the regular variant, add a 35% dim over images, solid fallback under reduce transparency | ui-designer | S |
| 5 | Empty results say only "0 results" | `.results-empty` | Help users recover · HIG clarity | 2 | 2 | **4** | "No recipes use all 5 ingredients. Try removing *saffron*." + one-tap remove chip | ux-designer → frontend | S |
| 6 | Desktop has a bottom tab bar instead of a sidebar | ≥ 1024px layout | Consistency & standards · HIG navigation | 1 | 3 | **3** | Sidebar on ≥ 1024px with the same 4 destinations in the same order | frontend-engineer | M |
| 7 | Card hover animation scales 1.08 even with reduce motion | `.card:hover` | Accessibility: reduce motion | 1 | 2 | **2** | Wrap in `@media (prefers-reduced-motion: no-preference)` | frontend-engineer | S |

## Accessibility audit snapshot

| Check | Light | Dark | Notes |
|---|---|---|---|
| Text contrast ≥ 4.5:1 | ❌ | ✅ | #4 header over photos |
| Targets ≥ 44 px | ❌ | ❌ | #2 filter icon is 28 px |
| 200 % text zoom | ✅ | ✅ | no clipping at 320 px |
| Reduce motion | ❌ | ❌ | #7 |
| Reduce transparency | ❌ | ❌ | glass stays translucent; add fallback |
| Increase contrast | ✅ | ✅ | |
| Keyboard / focus | ✅ | ✅ | focus ring visible |
| Colour not alone | ❌ | ❌ | #3 |

## What works (keep it)

- Clear single primary action on the home screen.
- Recipe page hierarchy: title → time/servings → ingredients → steps.

## Next steps

1. Orchestrator schedules #1–#3 for this sprint (all S effort).
2. QA adds Playwright checks: no double submit; filters button has an accessible name; reduced-motion snapshot.
3. Re-audit after fixes; update this file with ✅/❌.

---
**Why this is good:** every row has evidence, a heuristic, a severity, a concrete fix, an owner and an effort; the list is ranked; the summary tells a busy reader what to do first; accessibility is measured, not guessed.
