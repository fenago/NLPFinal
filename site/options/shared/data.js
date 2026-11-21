// Shared by the three design options. Fetches the REAL /data/*.json (same files as the live app)
// and fills the dashboard containers by id. Markup and styling stay in each option.
// Same-origin only (CSP default-src 'self'). No network access except /data/*.json.

export const NAV = [
  { id: "dashboard", label: "Dashboard", href: "/#dashboard", current: true },
  { id: "reviews", label: "Reviews & examples", href: "/#reviews" },
  { id: "analyze", label: "Analyze", href: "/#live" },
  { id: "about", label: "About", href: "/#about" },
];

export async function loadAll() {
  const names = ["meta", "summary", "collocations", "aspects", "entities"];
  const res = await Promise.all(names.map((n) => fetch(`/data/${n}.json`).then((r) => {
    if (!r.ok) throw new Error(`${n}.json: HTTP ${r.status}`);
    return r.json();
  })));
  return Object.fromEntries(names.map((n, i) => [n, res[i]]));
}

export function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === "style") el.setAttribute("style", v); else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) if (kid != null) el.append(kid);
  return el;
}
const $ = (s) => document.querySelector(s);
const pct = (x, n) => Math.round((100 * x) / n);
const signed = (x) => (x < 0 ? "−" : "+") + Math.abs(x).toFixed(2);
const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export function setStatus(el, msg, isError = false) {
  el.textContent = msg;
  el.classList.toggle("is-error", isError);
}

export function fillDataset(meta) {
  const d = meta.dataset, v = meta.versions;
  $("#dataset-line").textContent = `${d.n_reviews} ${d.name.split(" ")[0]} reviews, analysed with NLTK and spaCy.`;
}

export function fillOverview(summary) {
  const n = summary.n_reviews, sc = summary.sentiment_counts;
  const meanAll = Object.entries(summary.mean_compound_by_stars)
    .reduce((acc, [s, m]) => acc + (m ?? 0) * summary.stars_counts[s], 0) / n;
  const rows = [["Reviews", n], ["Positive", `${pct(sc.positive, n)}%`], ["Negative", `${pct(sc.negative, n)}%`],
    ["Neutral", `${pct(sc.neutral, n)}%`], ["Mean compound", signed(meanAll)],
    ["Agrees with stars", `${Math.round(summary.accuracy_vs_stars * 100)}%`]];
  $("#overview").replaceChildren(...rows.map(([k, v]) => h("div", {}, h("dt", {}, k), h("dd", {}, String(v)))));
}

// Sentiment: text list (always shown, the chart's text alternative) + Chart.js bar chart.
const SENT = [["negative", "Negative", "−", "--neg"], ["neutral", "Neutral", "○", "--neu"], ["positive", "Positive", "+", "--pos"]];

export function fillSentimentList(summary) {
  const n = summary.n_reviews, c = summary.sentiment_counts;
  $("#sentiment-list").replaceChildren(...SENT.map(([key, label, sym, tok]) => h("li", {},
    h("span", { class: "sym", "aria-hidden": "true", style: `color:var(${tok})` }, sym),
    h("span", { class: "lbl" }, label), h("span", { class: "val" }, `${c[key]} ${c[key] === 1 ? "review" : "reviews"} (${pct(c[key], n)}%)`))));
}

let chart = null;
export function drawSentimentChart(summary, opts = {}) {
  const canvas = $("#chart-sentiment");
  const n = summary.n_reviews, c = summary.sentiment_counts;
  canvas.setAttribute("aria-label", `Bar chart of VADER labels for ${n} reviews: ` +
    SENT.map(([k, l]) => `${l} ${c[k]} (${pct(c[k], n)}%)`).join(", ") + ". The same numbers are listed below the chart.");
  if (typeof Chart === "undefined") return; // text list still shows the numbers
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const text = cssVar("--chart-text"), grid = cssVar("--chart-grid");
  chart?.destroy();
  chart = new Chart(canvas, {
    type: "bar",
    data: { labels: SENT.map(([k, l]) => `${l} (${pct(c[k], n)}%)`),
      datasets: [{ data: SENT.map(([k]) => c[k]), backgroundColor: SENT.map(([, , , t]) => cssVar(t)),
        borderRadius: opts.barRadius ?? 6, borderSkipped: false, maxBarThickness: 72 }] },
    options: { responsive: true, maintainAspectRatio: false, animation: reduce ? false : { duration: 250 },
      plugins: { legend: { display: false }, tooltip: { enabled: true } },
      scales: { x: { ticks: { color: text, font: { size: 13 } }, grid: { display: false }, border: { color: grid } },
                y: { beginAtZero: true, ticks: { color: text, font: { size: 12 } }, grid: { color: grid }, border: { display: false },
                     title: { display: true, text: "Reviews", color: text } } } },
  });
}
export function redrawOnPreferenceChange(fn) {
  for (const q of ["(prefers-color-scheme: dark)", "(prefers-contrast: more)", "(prefers-reduced-motion: reduce)"]) {
    matchMedia(q).addEventListener("change", fn);
  }
}

function barList(el, items, max) {
  el.replaceChildren(...items.map((it) => h("li", {},
    h("span", { class: "lbl" }, it.label),
    h("span", { class: "bar", "aria-hidden": "true" }, h("i", { style: `width:${Math.max(2, (100 * it.value) / max)}%` })),
    h("span", { class: "val" }, String(it.value)))));
}
export function fillWords(colloc, limit = 12) {
  const items = colloc.top_words.slice(0, limit).map((w) => ({ label: w.word, value: w.count }));
  barList($("#list-words"), items, Math.max(...items.map((i) => i.value)));
}
export function fillPhrases(colloc, limit = 12) {
  const items = colloc.bigrams.slice(0, limit).map((b) => ({ label: b.phrase, value: b.count }));
  barList($("#list-phrases"), items, Math.max(...items.map((i) => i.value)));
}

export function fillAspects(aspects, limit = 10) {
  const list = [...aspects.aspects].sort((a, b) => b.mentions - a.mentions).slice(0, limit);
  $("#list-aspects").replaceChildren(...list.map((a) => {
    const t = a.positive + a.neutral + a.negative || 1;
    const alt = `${a.positive} positive, ${a.neutral} neutral, ${a.negative} negative`;
    const opinions = a.top_opinions.slice(0, 3).map((o) => o.word).join(", ");
    return h("li", {},
      h("div", { class: "asp-head" }, h("span", { class: "lbl" }, a.aspect),
        h("span", { class: "val" }, `${a.mentions} mentions`)),
      h("div", { class: "stack", role: "img", "aria-label": `${a.aspect}: ${alt}` },
        h("i", { class: "s-pos", style: `flex:${a.positive}` }), h("i", { class: "s-neu", style: `flex:${a.neutral}` }),
        h("i", { class: "s-neg", style: `flex:${a.negative}` })),
      h("p", { class: "asp-meta" }, `${a.positive} + · ${a.neutral} ○ · ${a.negative} − · mean ${signed(a.mean_compound)}`,
        opinions ? ` · opinions: ${opinions}` : ""));
  }));
}

export function fillEntities(entities, limit = 8) {
  for (const g of ["people", "places", "brands", "products"]) {
    const list = entities.groups[g].slice(0, limit);
    const max = Math.max(1, ...list.map((e) => e.count));
    $(`#lb-${g}`).replaceChildren(...(list.length ? list.map((e) => h("li", {},
      h("span", { class: "lbl" }, e.text, e.sources.ruler ? h("span", { class: "ruler-dot", title: "EntityRuler match", "aria-label": " (EntityRuler match)" }, " ●") : null),
      h("span", { class: "bar", "aria-hidden": "true" }, h("i", { style: `width:${(100 * e.count) / max}%` })),
      h("span", { class: "val", "aria-label": `${e.count} mentions in ${e.n_reviews} reviews` }, String(e.count))))
      : [h("li", { class: "empty" }, "None found")]));
  }
}

// Floating bars cover the end of the page: reserve exactly their height (works at 200% text too).
export function reserveNavSpace() {
  const bars = [...document.querySelectorAll(".tabbar")];
  const set = () => {
    const bar = bars.find((b) => b.offsetParent !== null || getComputedStyle(b).position === "fixed" && getComputedStyle(b).display !== "none");
    const hgt = bar && getComputedStyle(bar).display !== "none" ? Math.ceil(bar.getBoundingClientRect().height) : 0;
    document.documentElement.style.setProperty("--tabbar-h", `${hgt}px`);
  };
  set();
  if ("ResizeObserver" in window) { const ro = new ResizeObserver(set); bars.forEach((b) => ro.observe(b)); }
  addEventListener("resize", set);
}

export async function run(opts = {}) {
  const status = $("#global-status");
  reserveNavSpace();
  try {
    const d = await loadAll();
    fillDataset(d.meta); fillOverview(d.summary); fillSentimentList(d.summary);
    fillWords(d.collocations, opts.words ?? 12); fillPhrases(d.collocations, opts.words ?? 12);
    fillAspects(d.aspects, opts.aspects ?? 10); fillEntities(d.entities, opts.entities ?? 8);
    const draw = () => drawSentimentChart(d.summary, opts);
    draw(); redrawOnPreferenceChange(draw);
    document.documentElement.dataset.ready = "true";
  } catch (err) {
    setStatus(status, `The dashboard could not load: ${err.message}`, true);
  }
}
