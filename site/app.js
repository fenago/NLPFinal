// Customer Review Analyzer UI. Owner: frontend-engineer. Reviewers: dataviz-specialist, qa-engineer.
// Plain ES module, no framework, no server. Reads site/data/*.json (docs/data-contract.md) and talks
// to the Pyodide worker (worker.mjs) for live NLTK analysis. All review text is inserted with
// textContent (never innerHTML) because it is untrusted input.

import * as charts from "./charts.js";

const CONTRACT_MAJOR = "1";
const LIVE_TIMEOUT_MS = 120000;
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/** Tiny DOM builder: h("p", {class: "x"}, "text", child) */
function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "dataset") Object.assign(el.dataset, v);
    else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? "" : String(v));
  }
  for (const c of children.flat()) {
    if (c === null || c === undefined || c === false) continue;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

const BADGES = { nltk: ["badge-nltk", "NLTK"], spacy: ["badge-spacy", "spaCy"], both: ["badge-both", "NLTK + spaCy"] };
const badge = (src) => h("span", { class: `badge ${BADGES[src][0]}` }, BADGES[src][1]);
const labelSpan = (label) => h("span", { class: `label label-${label}` }, label);
const fmt = (x) => (x > 0 ? `+${x.toFixed(3)}` : x.toFixed(3));

function setStatus(el, msg, isError = false) {
  el.textContent = msg;
  el.classList.toggle("error", isError);
}

async function fetchJSON(name) {
  const res = await fetch(`data/${name}`);
  if (!res.ok) throw new Error(`Could not load data/${name} (HTTP ${res.status}). Run python pipeline/build.py first.`);
  const data = await res.json();
  if (!String(data.contract_version || "").startsWith(`${CONTRACT_MAJOR}.`)) {
    throw new Error(`data/${name} has contract version ${data.contract_version}; this page expects ${CONTRACT_MAJOR}.x`);
  }
  return data;
}

// ------------------------------------------------------------------ tabs + theme

const TABS = ["dashboard", "reviews", "live", "about"];
const tabHooks = {};

function selectTab(name, { focus = false, push = true } = {}) {
  if (!TABS.includes(name)) name = "dashboard";
  for (const t of TABS) {
    const tab = $(`#tab-${t}`);
    const on = t === name;
    tab.setAttribute("aria-selected", String(on));
    tab.tabIndex = on ? 0 : -1;
    $(`#panel-${t}`).hidden = !on;
  }
  if (focus) $(`#tab-${name}`).focus();
  if (push && location.hash !== `#${name}`) history.replaceState(null, "", `#${name}`);
  tabHooks[name]?.();
}

function initTabs() {
  const list = $('[role="tablist"]');
  list.addEventListener("click", (e) => {
    const tab = e.target.closest('[role="tab"]');
    if (tab) selectTab(tab.id.replace("tab-", ""));
  });
  list.addEventListener("keydown", (e) => {
    const i = TABS.indexOf(document.activeElement.id.replace("tab-", ""));
    if (i < 0) return;
    const next = { ArrowRight: (i + 1) % TABS.length, ArrowLeft: (i - 1 + TABS.length) % TABS.length, Home: 0, End: TABS.length - 1 }[e.key];
    if (next === undefined) return;
    e.preventDefault();
    selectTab(TABS[next], { focus: true });
  });
  document.addEventListener("click", (e) => {
    const link = e.target.closest("[data-goto]");
    if (link) { e.preventDefault(); selectTab(link.dataset.goto, { focus: true }); }
  });
  window.addEventListener("hashchange", () => selectTab(location.hash.slice(1), { push: false }));
}

function initTheme() {
  const btn = $("#theme-toggle");
  const order = ["system", "light", "dark"];
  const current = () => document.documentElement.dataset.theme || "system";
  const show = () => {
    btn.textContent = `Theme: ${current()}`;
    btn.setAttribute("aria-label", `Colour theme: ${current()}. Activate to change.`);
  };
  btn.addEventListener("click", () => {
    const next = order[(order.indexOf(current()) + 1) % order.length];
    if (next === "system") delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = next;
    try { next === "system" ? localStorage.removeItem("theme") : localStorage.setItem("theme", next); } catch (e) { /* private mode */ }
    show();
    refreshThemed();
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", refreshThemed);
  show();
}

let summaryCache = null;
function refreshThemed() {
  if (typeof Chart !== "undefined") charts.rerenderAll();
  if (summaryCache) charts.confusionTable($("#confusion"), summaryCache);
}

// ------------------------------------------------------------------ dashboard

async function loadDashboard() {
  const status = $("#global-status");
  setStatus(status, "Loading dashboard data…");
  try {
    const [meta, summary, colloc, aspects, entities] = await Promise.all(
      ["meta.json", "summary.json", "collocations.json", "aspects.json", "entities.json"].map(fetchJSON));
    summaryCache = summary;
    renderDashboard(meta, summary, colloc, aspects, entities);
    setStatus(status, "");
  } catch (err) {
    setStatus(status, `The dashboard could not load: ${err.message}`, true);
  }
}

function renderDashboard(meta, summary, colloc, aspects, entities) {
  const d = meta.dataset;
  $("#dataset-line").textContent = `${d.n_reviews} reviews from ${d.name}, ${d.mode} mode. ` +
    `Built with Python ${meta.versions.python}, NLTK ${meta.versions.nltk}, spaCy ${meta.versions.spacy} (${"en_core_web_sm"} ${meta.versions.en_core_web_sm}).`;
  $("#versions").textContent = `Data contract ${meta.contract_version}. Build: Python ${meta.versions.python}, NLTK ${meta.versions.nltk}, spaCy ${meta.versions.spacy}, en_core_web_sm ${meta.versions.en_core_web_sm}.`;

  const n = summary.n_reviews;
  const sc = summary.sentiment_counts;
  const p = (x) => `${Math.round((100 * x) / n)}%`;
  const meanAll = Object.entries(summary.mean_compound_by_stars).reduce((acc, [s, m]) => acc + (m ?? 0) * summary.stars_counts[s], 0) / n;
  $("#overview").replaceChildren(
    ...[["Reviews", n], ["Positive", p(sc.positive)], ["Negative", p(sc.negative)], ["Neutral", p(sc.neutral)],
        ["Mean compound", fmt(meanAll)], ["Agrees with stars", `${Math.round(summary.accuracy_vs_stars * 100)}%`]]
      .map(([k, v]) => h("div", {}, h("dt", {}, k), h("dd", {}, v))));

  if (typeof Chart === "undefined") {
    setStatus($("#global-status"), "Charts could not load (vendor/chart.umd.min.js missing). Data tables are still shown.", true);
  }
  charts.init?.();
  charts.sentimentDistribution($("#chart-sentiment"), summary);
  charts.compoundHistogram($("#chart-histogram"), summary);
  charts.meanByStars($("#chart-stars"), summary);
  charts.confusionTable($("#confusion"), summary);
  charts.horizontalBars($("#chart-words"), colloc.top_words.slice(0, 15).map((w) => ({ label: w.word, value: w.count })),
    { title: "Top 15 words by frequency", valueLabel: "Count", color: () => charts.palette().nltk,
      onSelect: (item) => openReviews({ text: item.label }) });
  charts.horizontalBars($("#chart-phrases"), colloc.bigrams.slice(0, 15).map((b) => ({ label: b.phrase, value: b.count, score: b.score })),
    { title: "Top 15 key phrases (likelihood-ratio ranked)", valueLabel: "Count", color: () => charts.palette().nltk,
      onSelect: (item) => openReviews({ text: item.label }) });
  charts.aspectSentiment($("#chart-aspects"), aspects.aspects,
    (a) => openReviews({ ids: a.review_ids, chip: `Aspect: ${a.aspect}` }));

  for (const g of ["people", "places", "brands", "products"]) {
    const list = entities.groups[g];
    const max = Math.max(1, ...list.map((e) => e.count));
    $(`#lb-${g}`).replaceChildren(...(list.length ? list.slice(0, 10).map((e) => h("li", {},
      h("button", { type: "button", "aria-label": `${e.text}: ${e.count} mentions in ${e.n_reviews} reviews${e.sources.ruler ? ", EntityRuler match" : ""}. Show reviews.`,
                    onclick: () => openReviews({ ids: e.review_ids, chip: `${g[0].toUpperCase() + g.slice(1)}: ${e.text}` }) },
        h("span", {}, e.text, e.sources.ruler ? h("span", { class: "ruler-dot", "aria-hidden": "true" }, "●") : null,
          h("span", { class: "bar", style: `width:${(100 * e.count) / max}%` })),
        h("span", { class: "count" }, e.count)))) : [h("li", { class: "muted" }, "None found")]));
  }
}

// ------------------------------------------------------------------ reviews + examples

const reviewState = { reviews: null, examples: null, filter: {}, loading: null };

async function ensureReviews() {
  if (reviewState.reviews) return;
  if (!reviewState.loading) {
    const count = $("#review-count");
    setStatus(count, "Loading reviews…");
    reviewState.loading = Promise.all([fetchJSON("reviews.json"), fetchJSON("examples.json")])
      .then(([r, e]) => {
        reviewState.reviews = r.reviews;
        reviewState.examples = e.examples;
        renderExampleButtons();
      })
      .catch((err) => { setStatus(count, `Reviews could not load: ${err.message}`, true); reviewState.loading = null; throw err; });
  }
  await reviewState.loading;
}

function openReviews(filter) {
  reviewState.filter = { ...filter };
  $("#f-text").value = filter.text || "";
  $("#f-stars").value = "";
  $("#f-label").value = "";
  selectTab("reviews");
}

tabHooks.reviews = async () => {
  try { await ensureReviews(); renderReviewList(); } catch (e) { /* status already shown */ }
};

function currentReviews() {
  const f = reviewState.filter;
  const stars = $("#f-stars").value;
  const label = $("#f-label").value;
  const text = $("#f-text").value.trim().toLowerCase();
  const ids = f.ids ? new Set(f.ids) : null;
  return reviewState.reviews.filter((r) =>
    (!ids || ids.has(r.id)) && (!stars || r.stars === Number(stars)) &&
    (!label || r.nltk.sentiment.label === label) && (!text || r.text.toLowerCase().includes(text)));
}

function renderReviewList() {
  if (!reviewState.reviews) return;
  const chip = $("#f-chip");
  if (reviewState.filter.chip) {
    chip.hidden = false;
    chip.replaceChildren(h("span", {}, reviewState.filter.chip),
      h("button", { type: "button", "aria-label": `Remove filter ${reviewState.filter.chip}`,
                    onclick: () => { reviewState.filter = {}; renderReviewList(); $("#f-text").focus(); } }, "✕"));
  } else {
    chip.hidden = true;
    chip.replaceChildren();
  }
  const rows = currentReviews();
  setStatus($("#review-count"), `${rows.length} of ${reviewState.reviews.length} reviews`);
  $("#review-list").replaceChildren(...rows.map((r) => h("li", {},
    h("button", { type: "button", dataset: { id: r.id }, onclick: (e) => { markCurrent(e.currentTarget); showReview(r); } },
      h("span", { class: "meta" }, h("span", { "aria-label": `${r.stars} stars` }, "★".repeat(r.stars)),
        labelSpan(r.nltk.sentiment.label), h("span", {}, fmt(r.nltk.sentiment.compound))),
      h("span", { class: "snippet" }, r.text)))));
}

function markCurrent(btn) {
  $$("#review-list button[aria-current]").forEach((b) => b.removeAttribute("aria-current"));
  btn.setAttribute("aria-current", "true");
}

function renderExampleButtons() {
  $("#example-buttons").replaceChildren(...reviewState.examples.map((ex) =>
    h("button", { type: "button", class: "chip", "aria-pressed": "false",
                  onclick: (e) => {
                    $$("#example-buttons .chip").forEach((c) => c.setAttribute("aria-pressed", "false"));
                    e.currentTarget.setAttribute("aria-pressed", "true");
                    showReview(ex, { example: true });
                  } },
      ex.is_demo ? h("span", { class: "tag" }, "Demo") : null, ex.title.replace(/^Demo \(hand-written\): /, ""))));
}

/** Review text with spaCy entity spans highlighted. Offsets are Python code points. */
function highlightedText(text, entities) {
  const cps = Array.from(text);
  const out = h("div", { class: "review-text" });
  let pos = 0;
  for (const e of [...entities].sort((a, b) => a.start - b.start)) {
    if (e.start < pos) continue;
    out.append(cps.slice(pos, e.start).join(""));
    const group = e.group || "other";
    out.append(h("mark", { class: `ent ent-${group}`, title: `${e.label} → ${e.group || "not in a leaderboard"} (${e.source === "ruler" ? "EntityRuler" : "statistical NER"})` },
      cps.slice(e.start, e.end).join(""), h("sup", {}, e.label)));
    pos = e.end;
  }
  out.append(cps.slice(pos).join(""));
  return out;
}

function sentenceList(sentences) {
  return h("ol", { class: "sent-list" }, sentences.map((s) => h("li", {},
    h("div", {}, h("span", { class: "score" }, fmt(s.compound)), charts.scoreBar(s.compound), labelSpan(s.label)),
    h("div", {}, s.text))));
}

function wordsAndPhrases(nltk) {
  return [
    h("h4", {}, "Top words ", badge("nltk")),
    nltk.top_words.length ? h("ul", { class: "kv" }, nltk.top_words.map((w) => h("li", {}, `${w.word} × ${w.count}`))) : h("p", { class: "muted" }, "No content words."),
    h("h4", {}, "Key phrases ", badge("nltk")),
    nltk.key_phrases.length ? h("ul", { class: "kv" }, nltk.key_phrases.map((p) => h("li", {}, `${p.phrase} × ${p.count}`))) : h("p", { class: "muted" }, "No two-word phrases."),
  ];
}

function overallLine(sent, title) {
  return h("p", {}, `${title}: `, h("span", { class: "score" }, fmt(sent.compound)), " ", labelSpan(sent.label),
    h("span", { class: "muted" }, ` (pos ${sent.pos}, neu ${sent.neu}, neg ${sent.neg})`));
}

function showReview(r, { example = false } = {}) {
  const detail = $("#review-detail");
  const sp = r.spacy;
  const grouped = sp.entities.filter((e) => e.group);
  const parts = [
    h("h3", {}, example ? (r.is_demo ? "Demo review (hand-written, not from the dataset)" : r.title) : `Review ${r.id}`),
    r.stars ? h("p", { class: "muted" }, `${r.stars} stars`) : h("p", { class: "muted" }, "No star rating (demo)."),
    h("h4", {}, "Text with entities ", badge("spacy")),
    highlightedText(r.text, sp.entities),
    h("p", { class: "note" }, "Highlights: yellow people, green places, blue brands, pink products, grey other entity types (dates, numbers…). The superscript is the spaCy label."),
    h("h4", {}, "Overall sentiment ", badge("nltk")),
    overallLine(r.nltk.sentiment, "VADER on the full text"),
    h("h4", {}, "Sentiment with entity names masked ", badge("both")),
    overallLine(sp.masked_sentiment, `VADER after masking ${grouped.length} entity name${grouped.length === 1 ? "" : "s"}`),
    h("h4", {}, "Sentence by sentence ", badge("nltk")),
    sentenceList(r.nltk.sentences),
    h("h4", {}, "Aspects and opinions ", badge("both")),
    sp.aspects.length
      ? h("div", { class: "scroll-x" }, h("table", { class: "data" },
          h("thead", {}, h("tr", {}, ["Aspect", "Opinion", "Rule", "VADER", "Label"].map((t) => h("th", { scope: "col" }, t)))),
          h("tbody", {}, sp.aspects.map((a) => h("tr", {}, h("td", {}, a.aspect), h("td", {}, (a.negated ? "not " : "") + a.opinion),
            h("td", {}, a.rule), h("td", { class: "score" }, fmt(a.compound)), h("td", {}, labelSpan(a.label)))))))
      : h("p", { class: "muted" }, "No aspect–opinion pairs found by the dependency rules."),
    ...wordsAndPhrases(r.nltk),
  ];
  if (example && sp.tokens) {
    parts.push(
      h("h4", {}, "Noun-chunk aspects ", badge("spacy")),
      h("ul", { class: "kv" }, sp.noun_chunks.map((c) => h("li", {}, c))),
      h("details", {}, h("summary", {}, `Tokens, lemmas, part-of-speech and dependencies (${sp.tokens.length} tokens) `),
        h("div", { class: "scroll-x" }, h("table", { class: "data" },
          h("thead", {}, h("tr", {}, ["#", "Token", "Lemma", "POS", "Dep", "Head"].map((t) => h("th", { scope: "col" }, t)))),
          h("tbody", {}, sp.tokens.map((t) => h("tr", {}, h("td", {}, t.i), h("td", {}, t.text), h("td", {}, t.lemma),
            h("td", {}, t.pos), h("td", {}, t.dep), h("td", {}, `${sp.tokens[t.head].text} (${t.head})`))))))),
    );
  }
  detail.replaceChildren(...parts);
  detail.focus({ preventScroll: true });
  if (window.matchMedia("(max-width: 800px)").matches) detail.scrollIntoView({ block: "start" });
}

function initFilters() {
  for (const id of ["#f-stars", "#f-label"]) $(id).addEventListener("change", renderReviewList);
  let t;
  $("#f-text").addEventListener("input", () => { clearTimeout(t); t = setTimeout(renderReviewList, 150); });
}

// ------------------------------------------------------------------ live (Pyodide worker)

const live = { worker: null, ready: null, nextId: 1, pending: new Map(), versions: null };
const STAGES = { runtime: 1, nltk: 2, data: 3, warmup: 4 };

function startWorker() {
  if (live.ready) return live.ready;
  const status = $("#live-status");
  const bar = $("#live-progress");
  bar.hidden = false;
  bar.value = 0;
  setStatus(status, "Starting NLTK in your browser…");
  live.ready = new Promise((resolve, reject) => {
    let worker;
    try {
      worker = new Worker("./worker.mjs", { type: "module" });
    } catch (err) {
      reject(new Error(`This browser cannot start a module Web Worker (${err.message}).`));
      return;
    }
    live.worker = worker;
    const timer = setTimeout(() => reject(new Error("Loading Python took longer than 2 minutes. Check your connection and reload the page.")), LIVE_TIMEOUT_MS);
    worker.onmessage = ({ data }) => {
      if (data.type === "progress") {
        bar.value = STAGES[data.stage] ? STAGES[data.stage] - 0.5 : bar.value;
        setStatus(status, `${data.message}…`);
      } else if (data.type === "ready") {
        clearTimeout(timer);
        bar.value = bar.max;
        bar.hidden = true;
        live.versions = data.versions;
        setStatus(status, `NLTK ${data.versions.nltk} is ready in your browser (Pyodide ${data.versions.pyodide}, loaded in ${(data.ms / 1000).toFixed(1)} s).`);
        resolve();
      } else if (data.type === "init-error") {
        clearTimeout(timer);
        reject(new Error(data.error));
      } else if (data.id && live.pending.has(data.id)) {
        const { resolve: res, reject: rej } = live.pending.get(data.id);
        live.pending.delete(data.id);
        data.ok ? res(data) : rej(new Error(data.error));
      }
    };
    worker.onerror = (e) => { clearTimeout(timer); reject(new Error(e.message || "The analysis worker failed to load.")); };
  });
  live.ready.catch((err) => {
    bar.hidden = true;
    setStatus(status, `Live analysis is unavailable: ${err.message} The dashboard and dataset reviews still work.`, true);
    $("#live-run").disabled = false;
    live.ready = null;
    live.worker?.terminate();
  });
  return live.ready;
}

function analyzeLive(text) {
  const id = live.nextId++;
  return new Promise((resolve, reject) => {
    live.pending.set(id, { resolve, reject });
    live.worker.postMessage({ id, type: "analyze", text });
  });
}

async function runLive() {
  const text = $("#live-text").value.trim();
  const status = $("#live-status");
  const btn = $("#live-run");
  if (!text) { setStatus(status, "Type or paste a review first.", true); $("#live-text").focus(); return; }
  btn.disabled = true;
  try {
    await startWorker();
    setStatus(status, "Analyzing…");
    const { data, ms } = await analyzeLive(text);
    renderLive(data);
    setStatus(status, `Analyzed ${data.n_sentences} sentence${data.n_sentences === 1 ? "" : "s"} in ${ms} ms with NLTK ${live.versions?.nltk ?? ""} in your browser.`);
  } catch (err) {
    setStatus(status, `Analysis failed: ${err.message}`, true);
  } finally {
    btn.disabled = false;
  }
}

function renderLive(d) {
  const panel = (id, title, src, ...body) => h("section", { class: "panel", "aria-labelledby": id, dataset: { source: src } },
    h("header", { class: "panel-head" }, h("h3", { id }, title), badge(src)), ...body);
  $("#live-results").replaceChildren(
    panel("lr-overall", "Overall sentiment (VADER)", "nltk",
      overallLine(d.sentiment, "Compound score"), charts.scoreBar(d.sentiment.compound),
      h("p", { class: "note" }, `${d.n_sentences} sentences, ${d.n_tokens} word tokens, ${d.n_chars} characters.`)),
    panel("lr-sentences", "Sentence by sentence", "nltk", sentenceList(d.sentences)),
    panel("lr-words", "Top words and key phrases", "nltk", ...wordsAndPhrases(d)),
    panel("lr-spacy", "Entities and aspects", "spacy",
      h("p", {}, "Not available for your own text: spaCy runs only in the Netlify build, not in the browser, and this site has no server."),
      h("p", {}, h("a", { href: "#reviews", "data-goto": "reviews" }, "See spaCy entities and aspects for dataset reviews and curated examples."))),
  );
}

function initLive() {
  $("#live-run").addEventListener("click", runLive);
  $("#live-text").addEventListener("keydown", (e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) runLive(); });
  $$(".sample").forEach((b) => b.addEventListener("click", () => { $("#live-text").value = b.dataset.sample; runLive(); }));
}
// Warm up Pyodide as soon as the live tab is opened, so the first click is fast.
tabHooks.live = () => { startWorker().catch(() => {}); };

// ------------------------------------------------------------------ boot

function boot() {
  initTheme();
  initTabs();
  initFilters();
  initLive();
  loadDashboard();
  selectTab(location.hash.slice(1) || "dashboard", { push: false });
}

boot();
