# Technical Writer Knowledge Index

Fetched: 2026-11-20. Notes from the Google developer documentation style guide, Diataxis, and the dataset and software citation sources.

| File | Use it when | Sources |
|---|---|---|
| 01-google-dev-style.md | Setting voice, tense, headings, lists, code font, link text for README, Method page, report | developers.google.com/style (highlights, tone, voice, tense, headings, lists, code-in-text, cross-references) |
| 02-readme-and-docs-structure.md | Deciding what goes where: tutorial, how-to, reference, explanation; mapping to README, data contract, Method page, report | diataxis.fr (start-here, reference) |
| 03-citations.md | Writing the credits: Amazon 2023 BibTeX (verbatim), Yelp (Zhang et al. 2015), NLTK book, spaCy CITATION.cff, VADER (Hutto and Gilbert 2014) | HF dataset cards; nltk.org; spaCy repo; vaderSentiment README |

Quick facts
- Second person, present tense, active voice, sentence-case headings, descriptive link text, code font for filenames and function names.
- Four doc kinds: tutorial (learning by doing), how-to (goal steps), reference (describe and only describe), explanation (why).
- NLTK asks you to cite the 2009 book; spaCy's CITATION.cff gives Honnibal, Montani, Van Landeghem, Boyd 2020, doi 10.5281/zenodo.1212303; VADER is Hutto and Gilbert, ICWSM-14, 2014 (MIT licence).
- Amazon card states no licence; Yelp points to the Yelp dataset agreement. Credit both in the footer and report.
- BibTeX entries marked "constructed" in 03 should be checked against publisher pages before the final report.

Project docs: docs/README.md, docs/04-dataset.md, docs/expert-roster.md (DOC agent, skills S43-S45).
