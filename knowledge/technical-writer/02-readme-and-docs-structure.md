# Documentation Structure with Diataxis

Sources:
- https://diataxis.fr/start-here/
- https://diataxis.fr/reference/
- https://diataxis.fr/ (home; description only)

Fetched: 2026-11-20

## The four kinds of documentation
Diataxis (by Daniele Procida) says there are "fundamentally four identifiable kinds of documentation, that respond to four different needs": tutorials, how-to guides, reference, explanation. "Each has a different purpose, and needs to be written in a different way." Blurring the boundaries "is at the heart of a vast number of problems in documentation."

| Kind | What it is (quoted or close paraphrase) | Reader is | Key rules |
|---|---|---|---|
| Tutorial | "a lesson, that takes a student by the hand through a learning experience"; always practical | studying (learning) | The user learns by doing; the learner must be able to succeed; give minimal explanation and link out. |
| How-to guide | "addresses a real-world goal or problem, by providing practical directions" | working, already competent | About work, not study; a goal-focused sequence of steps. Examples: "How to configure frame profiling", "Troubleshooting deployment problems". |
| Reference | "the technical description - facts - that a user needs in order to do things correctly: accurate, complete, reliable information, free of distraction and interpretation" | working | "Describe and only describe." Adopt standard patterns. Mirror the structure of the thing described. Link out for instruction and explanation. |
| Explanation | "provide context and background"; answers "why?" | studying | Can circle the topic, give opinions and perspectives; not instructions. |

## The compass (decide which kind you are writing)
| If the content... | ...and serves the user's... | ...then it is |
|---|---|---|
| informs action | acquisition of skill | a tutorial |
| informs action | application of skill | a how-to guide |
| informs cognition | application of skill | reference |
| informs cognition | acquisition of skill | explanation |
- Action vs cognition: tutorials and how-tos are about what the user does; reference and explanation are about what the user knows.
- Study vs work: tutorials and explanation serve study; how-tos and reference serve work.

## Reference rules (from the Reference page)
- "The only purpose of a reference guide is to describe, as succinctly as possible, and in an orderly way."
- "Neutral description is the key imperative"; reference "demands accuracy, precision, completeness and clarity".
- Tempting to add instruction or explanation: "Instead, link to how-to guides, explanation and introductory tutorials."
- Consistency matters: "place the material that your user needs where they expect to find it, in a format that they are familiar with." Short usage examples are acceptable illustration.
- List commands, options, operations, features, flags, limitations, error messages.

## Practical workflow (from "Start here")
1. Look at the documentation in front of you (even if empty).
2. Ask whether it could be improved.
3. Pick one small thing that would improve it.
4. Do it, then repeat.
"The best way to get started with Diataxis is by applying it - to something, however small." You do not need to adopt the whole theory.

## Mapping to this project
| Deliverable | Diataxis kind | What goes in it |
|---|---|---|
| `README.md` | Entry point; links out to each kind | One-paragraph purpose, live URL, screenshot, quick start (3-5 commands), links to the sections below, citations and licence. Keep it short; do not put the whole method in it. |
| "Run it locally" section or `docs/run-locally.md` | How-to | Goal-based steps: install, run the build (`python pipeline/build.py`), serve `site/`, add a review to the sample. Assumes a competent reader. |
| "Try it" walk-through (optional) | Tutorial | A guided first session: open the page, paste a review, read the result. The reader succeeds if they follow along. |
| `docs/data-contract.md`, JSON schema, CLI options, file ownership table | Reference | Field names, types, ranges (VADER compound -1 to 1), file paths, version numbers. Facts only. |
| In-app "About / Method" page | Explanation (with reference tables) | Why VADER and spaCy are used for which feature, how aspects are linked to opinions, known limits (sarcasm, negation), why spaCy output is not live. |
| Final report | Explanation first, reference second | Problem, method, results (numbers from EVAL), limitations, citations. Link to reference rather than pasting schemas. |
| Demo script | Tutorial-like | Ordered script that always works with the committed sample. |

Rules to apply while writing:
- One purpose per page: do not mix a how-to with a long "why" digression; move the digression to Explanation and link.
- Keep reference pages in a fixed order (same columns for every field table).
- Put the numbers from `reports/evaluation.md` in one place and link to it from the README and the Method page so they cannot drift.
- Use the compass on any paragraph that feels out of place.
