// Shared Pyodide + NLTK setup. Owner: pyodide-engineer.
// Used by site/worker.mjs (browser) and tests/pyodide/parity.test.mjs (Node), so the
// browser path is the one that is tested. Everything is read from the same origin:
//   pyodide/manifest.json, pyodide/v<version>/ (runtime + wheels), vendor-py/regex/, nltk_data/,
//   py/nltk_analyzer.py

export const NLTK_DATA_FILES = [
  "tokenizers/punkt_tab/english/abbrev_types.txt",
  "tokenizers/punkt_tab/english/collocations.tab",
  "tokenizers/punkt_tab/english/ortho_context.tab",
  "tokenizers/punkt_tab/english/sent_starters.txt",
  "corpora/stopwords/english",
  "sentiment/vader_lexicon.zip",
];
export const SHIM_FILES = ["regex/__init__.py"];
export const NLTK_DATA_DIR = "/nltk_data";

function dirname(p) {
  return p.slice(0, p.lastIndexOf("/"));
}

/**
 * Install NLTK, the regex shim, the NLTK data and the shared analyzer into a loaded Pyodide.
 * @param pyodide  result of loadPyodide()
 * @param getBytes async (relativePath) => Uint8Array, relative to the site root
 * @param manifest parsed pyodide/manifest.json (see readManifest)
 * @param progress (stage, message) => void
 * @returns a JS function (text) => JSON string of nltk_analyzer.analyze(text)
 */
export async function readManifest(getBytes) {
  return JSON.parse(new TextDecoder().decode(await getBytes("pyodide/manifest.json")));
}

export async function setupNltk(pyodide, getBytes, manifest, progress = () => {}) {
  const sitePackages = pyodide.runPython("import sysconfig; sysconfig.get_paths()['purelib']");

  progress("nltk", "Installing NLTK");
  for (const wheel of manifest.wheels) {
    const bytes = await getBytes(`pyodide/${wheel.path}`);
    pyodide.unpackArchive(bytes, "wheel", { extractDir: sitePackages });
  }
  for (const f of SHIM_FILES) {
    const target = `${sitePackages}/${f}`;
    pyodide.FS.mkdirTree(dirname(target));
    pyodide.FS.writeFile(target, await getBytes(`vendor-py/${f}`));
  }

  progress("data", "Loading NLTK data (tokenizer, stopwords, VADER lexicon)");
  await Promise.all(
    NLTK_DATA_FILES.map(async (f) => {
      const bytes = await getBytes(`nltk_data/${f}`);
      const target = `${NLTK_DATA_DIR}/${f}`;
      pyodide.FS.mkdirTree(dirname(target));
      pyodide.FS.writeFile(target, bytes);
    }),
  );
  pyodide.FS.writeFile(`${sitePackages}/nltk_analyzer.py`, await getBytes("py/nltk_analyzer.py"));

  progress("warmup", "Warming up the analyzer");
  // NLTK 3.10 refuses data directories other accounts can write to (nltk/pathsec.py) and calls
  // os.geteuid(), which Emscripten does not provide. Give it getuid() and make /nltk_data private
  // (0755 dirs, 0644 files) so the check passes as designed instead of being switched off.
  pyodide.runPython(`
import importlib, os
if not hasattr(os, "geteuid"):
    os.geteuid = os.getuid
for root, dirs, files in os.walk(${JSON.stringify(NLTK_DATA_DIR)}):
    os.chmod(root, 0o755)
    for f in files:
        os.chmod(os.path.join(root, f), 0o644)
importlib.invalidate_caches()
`);
  const analyze = pyodide.runPython(`
import json
import nltk_analyzer
nltk_analyzer.configure(${JSON.stringify(NLTK_DATA_DIR)})
nltk_analyzer.analyze("Warm-up sentence. It works!")

def _analyze_json(text):
    return json.dumps(nltk_analyzer.analyze(str(text)))

_analyze_json
`);
  const versions = JSON.parse(
    pyodide.runPython(
      "import json, sys, nltk; json.dumps({'python': sys.version.split()[0], 'nltk': nltk.__version__})",
    ),
  );
  versions.pyodide = manifest.pyodide_version;
  return { analyze: (text) => analyze(text), versions };
}
