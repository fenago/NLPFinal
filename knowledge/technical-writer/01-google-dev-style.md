# Google Developer Documentation Style Guide: Highlights

Sources:
- https://developers.google.com/style/highlights (last updated 2026-10-09 UTC per the page)
- https://developers.google.com/style/tone
- https://developers.google.com/style/voice
- https://developers.google.com/style/tense
- https://developers.google.com/style/headings
- https://developers.google.com/style/lists
- https://developers.google.com/style/code-in-text
- https://developers.google.com/style/link-text (redirects to https://developers.google.com/style/cross-references)

Fetched: 2026-11-20

The guide's content is licensed CC BY 4.0 (per the page footer). Quotes below are short excerpts.

## The highlights page (summary list)
- Tone and content: be conversational and friendly without being frivolous; do not pre-announce anything; use descriptive link text; write accessibly; write for a global audience.
- Language and grammar: use second person ("you" rather than "we"); use active voice; use standard American spelling and punctuation; put conditions before instructions; check the word list for specific words.
- Formatting: sentence case for titles and headings; numbered lists for sequences; bulleted lists for most other lists; description lists for pairs of related data; serial commas; code-related text in code font; UI elements in bold; unambiguous date formatting.
- Images: provide alt text; provide high-resolution or vector images when practical.

## Voice and tone
- Tone: "casual, natural, and approachable, not pedantic or pushy"; avoid slang, jargon, cliches and culture-specific references. Do not overuse "please": Recommended "To view the document, click View." Not recommended "please click View."
- Tone examples: too informal "Dude! This API is totally awesome!"; about right "This API lets you collect data about what your users like."; too formal "The API documented by this page may enable the acquisition of information pertaining to user preferences."
- If unsure about phrasing or tone, ask a colleague to read it.
- Active voice: make clear who performs the action. Recommended "Send a query to the service. The server sends an acknowledgment." Not recommended "The service is queried, and an acknowledgment is sent." Passive is acceptable to emphasize the object, de-emphasize the actor, or when the actor is irrelevant (example: "Over 50 conflicts were found in the file.").

## Tense
- "Use present tense for statements that describe general behavior that's not associated with a particular time." Recommended "Send a query to the service." Not recommended "...The server will send an acknowledgment."
- Future tense is appropriate for genuinely asynchronous or later events (the page's Pub/Sub example).

## Headings and titles
- Sentence case for all headings and titles; descriptive and unique.
- Task-based headings start with a bare infinitive verb ("Create an instance", not "Creating an instance"); conceptual headings use a noun phrase that does not start with an -ing verb ("Migration to Google Cloud").
- Avoid -ing as the first word, numbers to show sequence, links in headings, code items in headings (add a descriptive noun if you must), and punctuation.
- Do not repeat the exact page title in a heading; no empty headings (a heading must be followed by content, and an H2 should not be directly followed by an H3 with no intro text); use one unique H1 per page; do not skip levels.
- To introduce a group of subsections, write "The following sections describe..." not "this section" or "these sections".
- Use "Optional:" as a prefix for optional sections ("Optional: Customize your alias").

## Lists
- Numbered lists for sequences, bulleted for most others, description lists for term-definition pairs.
- Introduce a list with a complete sentence, ending in a colon (usually) or period. Recommended "To get the USB driver, follow these steps:"; not "To get the USB driver:".
- Keep list items parallel in structure. Start each item with a capital letter; end with a period unless the item is a single word, has no verb, is entirely code font, or is entirely a link or title. If punctuation becomes inconsistent, rewrite or punctuate every item.
- Do not add an explanatory phrase to one item only; use a description list.
- In running text use serial commas; avoid ending a list with "etc." or "and so on".

## Code in text
- Use code font (backticks in Markdown) for text meant to be entered verbatim, and to separate the entity from surrounding text. Items listed: attribute names and values, class names, command output, command-line utility names, data types, database elements, element names, environment variable names, filenames and paths, folders, HTTP status codes and verbs, language keywords, method and function names, package names, placeholders, port numbers, query parameter names, strings used in commands and code.
- Not in code font: domain names in prose, product or service or organization names, URLs the reader follows in a browser (make these links with descriptive text).
- Do not use code elements as verbs or nouns or inflect them: "To add the data, send a POST request." not "POST the data."; "The ADDRESS constant's value is defined in the settings.h file." not "ADDRESS's value is defined in settings.h."
- Method names: omit the class name unless needed to avoid ambiguity.
- Do not put quotation marks around code unless the quotes are part of the code.

## Link text
- Use short, unique, descriptive phrases; put important words first; write link text that makes sense out of context. Not recommended: "click here", "this document", "this blog post".
- Do not use a URL as link text in general.
- Introduce a stand-alone cross-reference with "For more information, see [Title]." or "For more information about X, see [Title]." Use "see", and include "about..." when the link text does not make the reason clear.
- Put punctuation outside the link (`see [Test your code].`).
- If a link downloads a file or opens email, say so and name the file type ("download the security features PDF"). If it opens in a new tab, say so.
- Include the long form with the abbreviation inside the link: `[Google Kubernetes Engine (GKE)](...)`.
- Do not wrap link text in quotation marks or italics when linking to a title.

## Project application
- Apply to `README.md`, the in-app "About / Method" page, dataset credits and the final report: second person ("you can paste a review"), present tense ("the pipeline writes JSON to `site/data/`"), active voice, sentence-case headings.
- Task headings in how-to sections: "Run the build locally", "Add a review to the sample". Concept headings: "How sentiment is scored".
- Put file names, commands, function names (`SentimentIntensityAnalyzer`), config keys in backticks; do not backtick product names (NLTK, spaCy, Netlify) or plain URLs.
- Links read "see [Amazon Reviews 2023 dataset card]", never "click here".
- Use bulleted lists with a full-sentence lead-in; keep items parallel.
- Use "VADER compound score" consistently; define abbreviations (VADER, NER) on first use.
