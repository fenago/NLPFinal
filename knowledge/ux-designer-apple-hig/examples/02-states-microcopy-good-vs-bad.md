# Worked example 02: empty, loading and error states, good vs bad (with microcopy)

> Study this before reviewing or writing any state. The examples use **our** app's live analyzer ("Analyze your own review", NLTK in the browser through Pyodide) so they transfer directly.

Principles (skill `states-and-microcopy`): say **what is happening**, **why**, and **what to do next**. Use sentence case, plain words, a verb on every button and no blame. Explain jargon once. Announce async results politely.

---

## 1. Empty state (nothing analyzed yet)

**❌ Bad**
```text
No data.
[Submit]
```
- It doesn't say what the box is for, gives no example, and "Submit" doesn't say what happens.

**✅ Good**
```text
Paste a review to see its sentiment, sentence by sentence.
Try an example: “The pad thai was great but we waited 45 minutes.”   [Use this example]
[Analyze review]
Runs in your browser with NLTK. People, places, brands and products (spaCy) are shown for dataset reviews.
```
```html
<label for="review">Your review</label>
<textarea id="review" placeholder="Paste or type a review…"></textarea>
<button type="button" class="link">Use this example</button>
<button type="submit">Analyze review</button>
<p class="hint">Runs in your browser with NLTK. People, places, brands and products (spaCy) are shown for dataset reviews.</p>
```
Why it's better: it states the purpose, offers a one-tap example, labels the action with a verb, and sets honest expectations about NLTK vs spaCy once.

---

## 2. Loading state (Pyodide cold start, ~4 s locally, longer on slow networks)

**❌ Bad**
```text
[spinner]   Loading…
```
- No progress, no estimate and no reason. The button stays enabled, so users click it 3 times. A spinning animation also ignores reduce motion.

**✅ Good**
```text
Getting the analyzer ready (first time only, about 15 MB)…
● Downloading Python   ✓
● Loading NLTK         …
● Ready
[Analyze review]  (disabled until ready; your text stays editable)
```
```html
<div role="status" aria-live="polite">Getting the analyzer ready (first time only)… Loading NLTK</div>
<progress max="3" value="2" aria-label="Analyzer setup progress">2 of 3</progress>
<button type="submit" disabled aria-disabled="true">Analyze review</button>
```
Why it's better: staged progress explains the wait, says it's a one-time cost, and prevents double submits. The status is announced to screen readers without stealing focus, and the static step list works under reduce motion.

---

## 3. Error state (setup failed / offline)

**❌ Bad**
```text
Error: PythonError: Traceback (most recent call last) … ModuleNotFoundError
```
- It shows a raw stack trace, blames nobody but helps nobody, and offers no way forward.

**✅ Good**
```text
The analyzer couldn’t start. This usually means the connection dropped while downloading.
[Try again]   or   [Browse analyzed example reviews]
Details (for your instructor or a bug report) ▸
```
```html
<div role="alert">
  <p><strong>The analyzer couldn’t start.</strong> This usually means the connection dropped while downloading.</p>
  <button type="button">Try again</button>
  <a href="#reviews">Browse analyzed example reviews</a>
  <details><summary>Details</summary><pre>ModuleNotFoundError: …</pre></details>
</div>
```
Why it's better: it says what happened in plain words with a likely cause, gives two ways forward (retry, or a path that works offline), and keeps technical details available but collapsed. It uses `role="alert"` because this is urgent and the user needs to act.

---

## 4. Success state (result ready)

**❌ Bad:** the result appears silently above the fold while the user is scrolled down, and a compound score like "0.8639" is shown with no meaning.

**✅ Good**
```text
Mostly positive (+0.86)   NLTK
3 sentences: 2 positive, 1 negative. “…but the battery life was disappointing” is negative (−0.51).
What does +0.86 mean? VADER scores run from −1 (very negative) to +1 (very positive).
```
Why it's better: it leads with a plain-language verdict and shows the number second. It explains the scale once, points to the mixed sentence, and is announced through the same polite status region.

---

## Checklist used to judge any state

- [ ] Purpose or what's happening is clear in the first line
- [ ] There is a next step (button or link) with a verb
- [ ] No jargon without a one-line explanation
- [ ] It's announced to assistive tech (`status` for info, `alert` for errors)
- [ ] It works with reduce motion (no spinner-only feedback)
- [ ] It doesn't block input unnecessarily, and prevents double submits
