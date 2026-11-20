// Module Web Worker that runs NLTK live in the browser with self-hosted Pyodide.
// Owner: pyodide-engineer. Start with: new Worker("./worker.mjs", { type: "module" })
// (Pyodide 314.x ships pyodide.asm.mjs as an ES module; classic importScripts workers are unsupported.)
//
// Protocol
//   page -> worker: { id, type: "analyze", text }
//   worker -> page: { type: "progress", stage, message }
//                   { type: "ready", ms, versions }
//                   { type: "init-error", error }
//                   { id, ok: true, data, ms }  |  { id, ok: false, error }
// spaCy is NOT available here (no WebAssembly build); this worker runs NLTK only.

import { readManifest, setupNltk } from "./pyodide-setup.mjs";

const SITE_ROOT = new URL("./", import.meta.url);

function progress(stage, message) {
  self.postMessage({ type: "progress", stage, message });
}

async function getBytes(path) {
  const res = await fetch(new URL(path, SITE_ROOT));
  if (!res.ok) throw new Error(`Could not load ${path} (HTTP ${res.status})`);
  return new Uint8Array(await res.arrayBuffer());
}

async function init() {
  const t0 = performance.now();
  progress("runtime", "Loading the Python runtime (Pyodide, about 13 MB on first visit)");
  const manifest = await readManifest(getBytes);
  const indexURL = new URL(`pyodide/${manifest.base}`, SITE_ROOT).href; // versioned, immutable cache
  const { loadPyodide } = await import(`${indexURL}pyodide.mjs`);
  const pyodide = await loadPyodide({ indexURL });
  const api = await setupNltk(pyodide, getBytes, manifest, progress);
  const ms = Math.round(performance.now() - t0);
  self.postMessage({ type: "ready", ms, versions: api.versions });
  return api;
}

const ready = init().catch((err) => {
  self.postMessage({ type: "init-error", error: String(err && err.message ? err.message : err) });
  throw err;
});

self.onmessage = async (event) => {
  const { id, type, text } = event.data || {};
  if (type !== "analyze") return;
  try {
    const api = await ready;
    const t0 = performance.now();
    const json = api.analyze(String(text ?? "")); // text is passed as data, never spliced into code
    self.postMessage({ id, ok: true, data: JSON.parse(json), ms: Math.round(performance.now() - t0) });
  } catch (err) {
    self.postMessage({ id, ok: false, error: String(err && err.message ? err.message : err) });
  }
};
