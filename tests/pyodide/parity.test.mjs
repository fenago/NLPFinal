// Headless proof that the browser NLTK path works and matches the Netlify build.
// Owner: qa-engineer (with pyodide-engineer). Run: node --test "tests/pyodide/*.test.mjs"
// Needs a built site: python pipeline/build.py && python scripts/fetch_pyodide.py
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../site");
const { readManifest, setupNltk } = await import(pathToFileURL(path.join(SITE, "pyodide-setup.mjs")).href);
const getBytes = async (rel) => new Uint8Array(await readFile(path.join(SITE, rel)));
const manifest = await readManifest(getBytes);
const PYODIDE_DIR = path.join(SITE, "pyodide", manifest.base);
const { loadPyodide } = await import(pathToFileURL(path.join(PYODIDE_DIR, "pyodide.mjs")).href);

let api;
const timings = {};

test("Pyodide boots and installs NLTK from same-origin files only", async () => {
  const t0 = performance.now();
  const pyodide = await loadPyodide({ indexURL: PYODIDE_DIR });
  timings.runtime_ms = Math.round(performance.now() - t0);
  const t1 = performance.now();
  api = await setupNltk(pyodide, getBytes, manifest);
  timings.nltk_setup_ms = Math.round(performance.now() - t1);
  assert.equal(api.versions.nltk, "3.10.4");
  assert.equal(api.versions.pyodide, "314.0.8");
  // The regex shim must be what is imported (no real regex wheel is shipped).
  assert.equal(pyodide.runPython("import regex; regex.__version__"), "0+shim");
  console.log(`# timings ${JSON.stringify(timings)} versions ${JSON.stringify(api.versions)}`);
});

test("live analyze() returns per-sentence VADER scores", () => {
  const out = JSON.parse(api.analyze("The pizza was great. The service was not good!"));
  assert.equal(out.n_sentences, 2);
  assert.equal(out.sentences[0].label, "positive");
  assert.equal(out.sentences[1].label, "negative");
  assert.ok(out.key_phrases.some((p) => p.phrase === "not good"));
});

test("browser output is identical to the build output for every dataset review", async () => {
  const { reviews } = JSON.parse(await readFile(path.join(SITE, "data/reviews.json"), "utf8"));
  const t0 = performance.now();
  let mismatches = 0;
  for (const r of reviews) {
    const live = JSON.parse(api.analyze(r.text));
    try {
      assert.deepEqual(live, r.nltk);
    } catch (e) {
      mismatches += 1;
      if (mismatches <= 3) console.log(`# mismatch ${r.id}: ${e.message.slice(0, 400)}`);
    }
  }
  console.log(`# analyzed ${reviews.length} reviews in Pyodide in ${Math.round(performance.now() - t0)} ms`);
  assert.equal(mismatches, 0);
});
