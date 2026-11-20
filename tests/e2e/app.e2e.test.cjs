// Playwright end-to-end tests for both tabs, the Pyodide cold start and a phone viewport.
// Owner: qa-engineer. Needs a built site (python pipeline/build.py && python scripts/fetch_pyodide.py).
//
//   node --test "tests/e2e/*.test.cjs"                   # serves site/ with `python -m http.server`
//   E2E_SERVER=netlify node --test "tests/e2e/*.test.cjs"   # serves site/ with netlify.toml headers (CSP, cache, wasm)
//   E2E_BASE_URL=https://<deploy-preview>.netlify.app node --test "tests/e2e/*.test.cjs"   # against a deploy preview
//
// Uses the `playwright` library (no trace, no video).
const { test, before, after } = require("node:test");
const assert = require("node:assert/strict");
const { spawn } = require("node:child_process");
const path = require("node:path");
const net = require("node:net");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "../..");
const PY = process.env.PYTHON || "python3";
let server, browser, BASE;
const timings = {};

function freePort() {
  return new Promise((resolve) => {
    const s = net.createServer().listen(0, "127.0.0.1", () => { const { port } = s.address(); s.close(() => resolve(port)); });
  });
}

async function waitForServer(url, ms = 15000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    try { const r = await fetch(url); if (r.ok) return; } catch (e) { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 150));
  }
  throw new Error(`server did not start: ${url}`);
}

before(async () => {
  if (process.env.E2E_BASE_URL) {
    BASE = process.env.E2E_BASE_URL.replace(/\/$/, "");
  } else {
    const port = await freePort();
    const args = process.env.E2E_SERVER === "netlify"
      ? [path.join(ROOT, "tests/support/serve_netlify.py"), "--port", String(port)]
      : ["-m", "http.server", String(port), "--bind", "127.0.0.1", "-d", path.join(ROOT, "site")];
    server = spawn(PY, args, { stdio: "ignore" });
    BASE = `http://127.0.0.1:${port}`;
    await waitForServer(`${BASE}/index.html`);
  }
  browser = await chromium.launch();
});

after(async () => {
  await browser?.close();
  server?.kill();
  console.log(`# e2e base=${BASE} server=${process.env.E2E_SERVER || (process.env.E2E_BASE_URL ? "remote" : "http.server")} timings=${JSON.stringify(timings)}`);
});

async function openPage(options = {}) {
  const context = await browser.newContext(options);
  const page = await context.newPage();
  const problems = [];
  const external = [];
  page.on("pageerror", (e) => problems.push(`pageerror: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error") problems.push(`console: ${m.text()}`); });
  page.on("request", (r) => { if (!r.url().startsWith(BASE) && !r.url().startsWith("data:")) external.push(r.url()); });
  return { context, page, problems, external };
}

test("dashboard renders every panel with a source badge and a legend", async () => {
  const { context, page, problems, external } = await openPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${BASE}/`);
  await page.waitForSelector("#lb-brands li button");
  const panels = await page.$$eval("#panel-dashboard .panel", (els) => els.map((el) => ({
    title: el.querySelector("h3")?.textContent, badge: el.querySelector(".panel-head .badge")?.textContent })));
  assert.equal(panels.length, 7);
  for (const p of panels) assert.ok(["NLTK", "spaCy", "NLTK + spaCy"].includes(p.badge), `${p.title} has badge ${p.badge}`);
  const badges = new Set(panels.map((p) => p.badge));
  assert.deepEqual([...badges].sort(), ["NLTK", "NLTK + spaCy", "spaCy"]);
  assert.equal(await page.locator(".legend .badge").count(), 3);
  // Charts drew and describe their data for screen readers.
  const labels = await page.$$eval("#panel-dashboard canvas", (cs) => cs.map((c) => c.getAttribute("aria-label")));
  assert.equal(labels.length, 6);
  for (const l of labels) assert.ok(l && !l.startsWith("Loading"), `canvas label: ${l}`);
  assert.match(await page.textContent("#overview"), /197/);
  assert.equal(await page.locator("#confusion td.match").count(), 5);
  // The dashboard first view must not download the large per-review file.
  const loaded = await page.evaluate(() => performance.getEntriesByType("resource").map((e) => e.name));
  assert.ok(!loaded.some((u) => u.endsWith("/data/reviews.json")), "reviews.json is lazy-loaded");
  assert.deepEqual(problems, []);
  assert.deepEqual(external, [], "no off-origin requests (no CDN)");
  await context.close();
});

test("entity leaderboard drills down to filtered reviews with spaCy highlights", async () => {
  const { context, page, problems } = await openPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${BASE}/`);
  await page.click("#lb-brands li:first-child button");
  await page.waitForSelector("#review-list li button");
  assert.ok(await page.isVisible("#panel-reviews"));
  assert.match(await page.textContent("#f-chip"), /Brands:/);
  const n = await page.locator("#review-list li").count();
  assert.ok(n >= 1 && n < 197, `filtered list has ${n} reviews`);
  await page.click("#review-list li:first-child button");
  await page.waitForSelector("#review-detail mark.ent");
  const heads = await page.$$eval("#review-detail h4", (hs) => hs.map((h) => h.textContent));
  assert.ok(heads.some((h) => h.includes("Text with entities") && h.includes("spaCy")));
  assert.ok(heads.some((h) => h.includes("Sentence by sentence") && h.includes("NLTK")));
  assert.ok(heads.some((h) => h.includes("Aspects and opinions") && h.includes("NLTK + spaCy")));
  // Curated demo example is clearly labelled.
  await page.click("#example-buttons .chip:first-child");
  assert.match(await page.textContent("#review-detail h3"), /Demo review \(hand-written/);
  assert.ok(await page.locator("#review-detail details table tbody tr").count() > 10, "token table present");
  assert.deepEqual(problems, []);
  await context.close();
});

test("live analysis (Pyodide + NLTK) returns sentence scores and explains spaCy is dataset-only", async () => {
  const { context, page, problems, external } = await openPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(`${BASE}/#live`);
  assert.match(await page.textContent("#panel-live .callout"), /spaCy cannot run in the browser/);
  const t0 = Date.now();
  await page.waitForFunction(() => /is ready in your browser/.test(document.querySelector("#live-status").textContent), null, { timeout: 120000 });
  timings.pyodide_cold_start_ms = Date.now() - t0;
  await page.fill("#live-text", "The pizza was great. The service was not good!");
  const t1 = Date.now();
  await page.click("#live-run");
  await page.waitForSelector("#live-results .sent-list li");
  timings.first_analysis_ms = Date.now() - t1;
  const sentences = await page.$$eval("#live-results .sent-list li", (lis) => lis.map((li) => li.textContent));
  assert.equal(sentences.length, 2);
  assert.match(sentences[0], /\+0\.\d{3}.*positive/);
  assert.match(sentences[1], /-0\.\d{3}.*negative/);
  const badges = await page.$$eval("#live-results .panel-head .badge", (bs) => bs.map((b) => b.textContent));
  assert.deepEqual(badges, ["NLTK", "NLTK", "NLTK", "spaCy"]);
  assert.match(await page.textContent("#live-results"), /not good × 1/);
  assert.match(await page.textContent("#live-results"), /Not available for your own text/);
  assert.match(await page.textContent("#live-status"), /NLTK 3\.10\.4/);
  assert.deepEqual(problems, []);
  assert.deepEqual(external, [], "Pyodide and wheels are served from the same origin");
  await context.close();
});

test("phone viewport: no horizontal scroll, tabs reachable, live analysis works", async () => {
  const { context, page, problems } = await openPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await page.goto(`${BASE}/`);
  await page.waitForSelector("#lb-people li");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  assert.ok(overflow <= 1, `page overflows horizontally by ${overflow}px`);
  await page.tap("#tab-live");
  await page.waitForFunction(() => /is ready in your browser/.test(document.querySelector("#live-status").textContent), null, { timeout: 120000 });
  await page.tap("button.sample >> nth=1");
  await page.waitForSelector("#live-results .sent-list li");
  assert.match(await page.textContent("#live-results"), /negative/);
  const overflow2 = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  assert.ok(overflow2 <= 1, `live tab overflows by ${overflow2}px`);
  assert.deepEqual(problems, []);
  await context.close();
});

test("keyboard: arrow keys move between tabs; dark theme keeps badge contrast >= 4.5:1", async () => {
  const { context, page } = await openPage({ viewport: { width: 1280, height: 900 }, colorScheme: "dark" });
  await page.goto(`${BASE}/`);
  await page.focus("#tab-dashboard");
  await page.keyboard.press("ArrowRight");
  assert.equal(await page.evaluate(() => document.activeElement.id), "tab-reviews");
  assert.equal(await page.getAttribute("#tab-reviews", "aria-selected"), "true");
  for (const scheme of ["dark", "light"]) {
    await page.emulateMedia({ colorScheme: scheme });
    const ratios = await page.evaluate(() => {
      const lum = (c) => { const [r, g, b] = c.match(/\d+(\.\d+)?/g).slice(0, 3).map(Number).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
      const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };
      const out = {};
      for (const sel of [".badge-nltk", ".badge-spacy", ".badge-both"]) { const s = getComputedStyle(document.querySelector(sel)); out[sel] = ratio(s.color, s.backgroundColor); }
      const panelBg = getComputedStyle(document.querySelector(".panel")).backgroundColor;
      for (const v of ["--pos", "--neg", "--neu", "--muted"]) out[v] = ratio(getComputedStyle(document.documentElement).getPropertyValue(v).trim().replace(/^#(..)(..)(..)$/, (_, r, g, b) => `rgb(${parseInt(r, 16)},${parseInt(g, 16)},${parseInt(b, 16)})`), panelBg);
      return out;
    });
    for (const [k, v] of Object.entries(ratios)) assert.ok(v >= 4.5, `${scheme} ${k} contrast ${v.toFixed(2)} < 4.5`);
  }
  await context.close();
});
