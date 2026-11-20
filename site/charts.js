// Chart.js charts for the dashboard. Owner: dataviz-specialist. Reviewer: frontend-engineer.
// Chart.js 4.6.1 is self-hosted (site/vendor/chart.umd.min.js, global `Chart`); no CDN.
// Every canvas gets role="img" and a data-specific aria-label, plus a <details> data table.
// Sentiment colours come from CSS variables (colour-blind safe blue / grey / orange) and every
// chart also labels the categories in text, so colour is never the only cue.

const charts = new Map();

function css(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export function palette() {
  return { pos: css("--pos"), neu: css("--neu"), neg: css("--neg"), fg: css("--fg"), muted: css("--muted"),
           border: css("--border"), nltk: css("--nltk-fg"), spacy: css("--spacy-fg") };
}

function applyDefaults() {
  const p = palette();
  Chart.defaults.color = p.fg;
  Chart.defaults.borderColor = p.border;
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.maintainAspectRatio = false;
  Chart.defaults.animation = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? false : { duration: 300 };
  Chart.defaults.plugins.legend.labels.boxWidth = 14;
}

const pct = (n, total) => (total ? Math.round((100 * n) / total) : 0);

function addTable(canvas, caption, head, rows) {
  const box = canvas.closest(".chart-box");
  let details = box.nextElementSibling;
  if (!details || !details.matches("details.chart-data")) {
    details = document.createElement("details");
    details.className = "chart-data";
    box.after(details);
  }
  details.replaceChildren();
  const summary = document.createElement("summary");
  summary.textContent = `Show data table: ${caption}`;
  const wrap = document.createElement("div");
  wrap.className = "scroll-x";
  const table = document.createElement("table");
  table.className = "data";
  const thead = table.createTHead().insertRow();
  head.forEach((h) => { const th = document.createElement("th"); th.scope = "col"; th.textContent = h; thead.appendChild(th); });
  const tbody = table.createTBody();
  rows.forEach((r) => { const tr = tbody.insertRow(); r.forEach((c) => { tr.insertCell().textContent = String(c); }); });
  wrap.appendChild(table);
  details.append(summary, wrap);
}

function make(canvas, config, label) {
  if (!canvas || typeof Chart === "undefined") return null;
  charts.get(canvas.id)?.chart.destroy();
  canvas.setAttribute("role", "img");
  canvas.setAttribute("aria-label", label);
  const chart = new Chart(canvas, config);
  return chart;
}

function register(id, render) {
  charts.set(id, { render, chart: render() });
}

/** Re-render every chart (after a theme change: canvas does not read CSS). */
export function rerenderAll() {
  applyDefaults();
  for (const [id, entry] of charts) {
    entry.chart?.destroy();
    entry.chart = entry.render();
  }
}

export function init() {
  applyDefaults();
}

// ------------------------------------------------------------------ charts

export function sentimentDistribution(canvas, summary) {
  const c = summary.sentiment_counts;
  const total = summary.n_reviews;
  const labels = ["Negative", "Neutral", "Positive"];
  const data = [c.negative, c.neutral, c.positive];
  const aria = `Bar chart of VADER labels for ${total} reviews: ` +
    labels.map((l, i) => `${l} ${data[i]} (${pct(data[i], total)}%)`).join(", ");
  register(canvas.id, () => { const p = palette(); return make(canvas, {
    type: "bar",
    data: { labels: labels.map((l, i) => `${l} (${pct(data[i], total)}%)`),
            datasets: [{ label: "Reviews", data, backgroundColor: [p.neg, p.neu, p.pos] }] },
    options: { plugins: { legend: { display: false }, title: { display: true, text: "Reviews per VADER label" } },
               scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
  }, aria); });
  addTable(canvas, "reviews per VADER label", ["Label", "Reviews", "Share"], labels.map((l, i) => [l, data[i], `${pct(data[i], total)}%`]));
}

export function compoundHistogram(canvas, summary) {
  const { bin_edges: e, counts } = summary.compound_histogram;
  const labels = counts.map((_, i) => `${e[i].toFixed(1)} to ${e[i + 1].toFixed(1)}`);
  const colours = (p) => counts.map((_, i) => (e[i + 1] <= -0.05 + 1e-9 ? p.neg : e[i] >= 0.05 - 1e-9 ? p.pos : p.neu));
  const aria = `Histogram of VADER compound scores: ${labels.map((l, i) => `${l}: ${counts[i]}`).join("; ")}`;
  register(canvas.id, () => { const p = palette(); return make(canvas, {
    type: "bar",
    data: { labels, datasets: [{ label: "Reviews", data: counts, backgroundColor: colours(p), barPercentage: 1, categoryPercentage: 0.95 }] },
    options: { plugins: { legend: { display: false }, title: { display: true, text: "Compound score histogram (−1 to +1)" } },
               scales: { y: { beginAtZero: true, ticks: { precision: 0 } }, x: { ticks: { maxRotation: 60, autoSkip: true } } } },
  }, aria); });
  addTable(canvas, "compound score histogram", ["Compound range", "Reviews"], labels.map((l, i) => [l, counts[i]]));
}

export function meanByStars(canvas, summary) {
  const stars = ["1", "2", "3", "4", "5"];
  const means = stars.map((s) => summary.mean_compound_by_stars[s]);
  const aria = `Bar chart of mean VADER compound by star rating: ${stars.map((s, i) => `${s} stars ${means[i]}`).join(", ")}`;
  register(canvas.id, () => { const p = palette(); return make(canvas, {
    type: "bar",
    data: { labels: stars.map((s) => `${s}★ (n=${summary.stars_counts[s]})`),
            datasets: [{ label: "Mean compound", data: means, backgroundColor: means.map((m) => (m >= 0.05 ? p.pos : m <= -0.05 ? p.neg : p.neu)) }] },
    options: { plugins: { legend: { display: false }, title: { display: true, text: "Mean VADER compound per star rating" } },
               scales: { y: { min: -1, max: 1 } } },
  }, aria); });
  addTable(canvas, "mean compound per star rating", ["Stars", "Reviews", "Mean compound"],
    stars.map((s, i) => [s, summary.stars_counts[s], means[i]]));
}

/** Confusion matrix as an accessible HTML table heat map (rows = stars, columns = VADER label). */
export function confusionTable(container, summary) {
  const { stars, labels, counts } = summary.vader_vs_stars;
  const expected = (s) => (s <= 2 ? "negative" : s === 3 ? "neutral" : "positive");
  const max = Math.max(1, ...counts.flat());
  const table = document.createElement("table");
  const cap = table.createCaption();
  cap.textContent = `Star rating (rows) vs VADER label (columns). Outlined cells agree. Agreement: ${Math.round(summary.accuracy_vs_stars * 100)}%.`;
  const head = table.createTHead().insertRow();
  ["Stars", ...labels.map((l) => l[0].toUpperCase() + l.slice(1))].forEach((t) => {
    const th = document.createElement("th"); th.scope = "col"; th.textContent = t; head.appendChild(th);
  });
  const body = table.createTBody();
  const dark = css("color-scheme") === "dark";
  stars.forEach((s, i) => {
    const tr = body.insertRow();
    const th = document.createElement("th"); th.scope = "row"; th.textContent = `${s}★`; tr.appendChild(th);
    labels.forEach((l, j) => {
      const td = tr.insertCell();
      const v = counts[i][j];
      td.textContent = String(v);
      const a = v / max;
      td.style.background = dark ? `rgba(106, 174, 240, ${0.12 + 0.6 * a})` : `rgba(31, 99, 168, ${0.06 + 0.5 * a})`;
      if (l === expected(s)) td.classList.add("match");
    });
  });
  container.replaceChildren(table);
}

export function horizontalBars(canvas, items, { title, valueLabel, color, onSelect }) {
  const labels = items.map((d) => d.label);
  const values = items.map((d) => d.value);
  const aria = `${title}: ${items.slice(0, 10).map((d) => `${d.label} ${d.value}`).join(", ")}${items.length > 10 ? ", and more" : ""}`;
  register(canvas.id, () => make(canvas, {
    type: "bar",
    data: { labels, datasets: [{ label: valueLabel, data: values, backgroundColor: color() }] },
    options: {
      indexAxis: "y",
      plugins: { legend: { display: false }, title: { display: false } },
      scales: { x: { beginAtZero: true, ticks: { precision: 0 } }, y: { ticks: { autoSkip: false } } },
      onClick: onSelect ? (_e, els) => { if (els.length) onSelect(items[els[0].index]); } : undefined,
    },
  }, aria));
  addTable(canvas, title.toLowerCase(), ["Item", valueLabel], items.map((d) => [d.label, d.value]));
}

export function aspectSentiment(canvas, aspects, onSelect) {
  const top = aspects.slice(0, 15);
  const labels = top.map((a) => `${a.aspect} (${a.mentions})`);
  const aria = `Stacked bar chart of opinion sentiment for the ${top.length} most discussed aspects: ` +
    top.map((a) => `${a.aspect}: ${a.positive} positive, ${a.neutral} neutral, ${a.negative} negative`).join("; ");
  register(canvas.id, () => {
    const p = palette();
    return make(canvas, {
      type: "bar",
      data: { labels, datasets: [
        { label: "Negative", data: top.map((a) => a.negative), backgroundColor: p.neg },
        { label: "Neutral", data: top.map((a) => a.neutral), backgroundColor: p.neu },
        { label: "Positive", data: top.map((a) => a.positive), backgroundColor: p.pos },
      ] },
      options: {
        indexAxis: "y",
        plugins: { title: { display: true, text: "Opinion pairs per aspect, by VADER label" },
                   tooltip: { callbacks: { footer: (els) => `mean compound ${top[els[0].dataIndex].mean_compound}` } } },
        scales: { x: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }, y: { stacked: true, ticks: { autoSkip: false } } },
        onClick: (_e, els) => { if (els.length) onSelect(top[els[0].index]); },
      },
    }, aria);
  });
  addTable(canvas, "aspect sentiment", ["Aspect", "Pairs", "Positive", "Neutral", "Negative", "Mean compound", "Top opinions"],
    top.map((a) => [a.aspect, a.mentions, a.positive, a.neutral, a.negative, a.mean_compound,
                    a.top_opinions.map((o) => `${o.word} (${o.count})`).join(", ")]));
}

/** Small inline bar for a compound score in [-1, 1], used in review details and live results. */
export function scoreBar(compound) {
  const p = palette();
  const bar = document.createElement("div");
  bar.className = "scorebar";
  bar.setAttribute("aria-hidden", "true");
  const fill = document.createElement("span");
  const w = Math.abs(compound) * 50;
  fill.style.left = compound >= 0 ? "50%" : `${50 - w}%`;
  fill.style.width = `${w}%`;
  fill.style.background = compound >= 0.05 ? p.pos : compound <= -0.05 ? p.neg : p.neu;
  const mid = document.createElement("span");
  mid.style.left = "50%"; mid.style.width = "1px"; mid.style.background = p.fg;
  bar.append(fill, mid);
  return bar;
}
