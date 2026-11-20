# 07 - Build limits, build cache, deploy size and file-count limits

Sources:
- https://docs.netlify.com/build/configure-builds/troubleshooting-tips.md (large files, build cache)
- https://docs.netlify.com/deploy/deploy-overview.md (54,000 files per directory)
- https://docs.netlify.com/build/configure-builds/manage-dependencies.md (dependency cache)
- https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview.md (retry without cache, deletion)
- https://docs.netlify.com/manage/monitoring/monitor-builds.md (build minutes, concurrent builds)
- https://answers.netlify.com/t/support-guide-how-long-should-netlify-builds-take/151 (Netlify Support guide, last updated July 2025; forum, NOT official docs pages)

Fetched: 2026-11-20

## Build time limit / timeout

- **Not found on docs.netlify.com.** No official docs page fetched states a numeric per-build timeout.
- Netlify Support guide (forum, staff-authored): "You should count on your builds having only **15 minutes** to complete their build command." Additional time for post-processing and upload is added on top and is not counted in the 15 minutes; a Support post says this is "likely the reason for timeouts happening in 30 minutes instead of 15".
- Forum threads show staff raising specific sites' build timeout to **30 minutes** on request (support ticket). Business/Enterprise reportedly can have much longer (a staff post mentions a 3 hour timeout for some customers).
- Treat as: ~15 min for the build command by default, ~30 min overall ceiling for typical accounts. All of this is **(unverified against official docs)**; confirm in the deploy log and the Netlify UI/plan page.
- Manual/CLI deploys have no build step, so no build timeout (Support post).
- Hung builds: builds "legitimately" end when the command exits; a left-running process (server started in build) makes Netlify think the build has not finished.

## Build resources

- Support guide posts conflict: one says "Your build is guaranteed only 4 CPUs and 8 GiB memory"; an older post says free and Pro get "approximately 1 CPU and around 2Gb of memory". (unverified; treat memory as potentially as low as about 2 GB.) Relevant for loading spaCy plus a corpus: process in batches with `nlp.pipe(..., batch_size=...)`, avoid holding the whole corpus in memory.
- Queuing: builds can queue up to about 15 minutes under load on lower tiers (Support guide). With many quick pushes, only the first and last queued deploys build; intermediate ones become "skipped".

## Build minutes / concurrency

- Monitor builds page: shows concurrent builds running/available/waiting and build minutes used and available per billing period. Numeric plan allotments are on the billing/pricing pages (not fetched; unverified). Deleting deploys does not return build minutes.
- Netlify is moving to credit-based plans (referenced across docs). Exact build-minute or credit cost per build: not found (unverified). Check https://www.netlify.com/pricing/.

## Build cache

- Netlify caches directories created while installing dependencies (documented under "Dependency cache"); list lives in `$NETLIFY_CACHE_DIR` handling in the build image's `run-build-functions.sh` (not published in docs). pip's cache location specifics: not documented (unverified).
- After the first build, installs are faster. Changing requirements re-runs install, "not guaranteed" to change cached content if requirements are still satisfied.
- Clear it: Deploys page > retry deploy from latest branch commit with "Retry without cache" (clear cache option). Use it when a build fails oddly (stale wheels, corrupted venv).
- Product caches such as `.cache` for spaCy models or generated results across builds are NOT a documented feature for Python; assume each build must regenerate `site/` from scratch (the build plugin API could persist cache, but not needed here).

## Deploy size and file limits

- **Files per directory: 54,000** max, otherwise the deploy fails (deploy overview; "no limit on the number of files per deploy").
- **Files over 10 MB** (troubleshooting tips, "Large files or sites"): "not well-supported by our CDN and may fail to upload to our system, causing your entire deploy to fail." Docs suggest hosting large content elsewhere (e.g. embedded YouTube).
  - **RISK FOR THIS PROJECT:** Pyodide's main WebAssembly binary (`pyodide.asm.wasm`, typically several MB to over 10 MB depending on version) and some wheels may approach 10 MB. Check sizes of every file under `site/` in the build script (fail the build or warn if any file > 10 MB). The "outside servers" rule means external hosting is not an option, so keep to compressed/slimmed packages or split data files.
  - Whether the 10 MB statement is a hard cap or a recommendation is ambiguous ("not well-supported ... may fail"). Mark as (unverified hard limit); test with the real files in a Deploy Preview early.
- Tens of thousands of HTML files cause long processing (many minutes) but should not fail.
- Total deploy size cap: not found in fetched docs (unverified).
- Deploy upload is incremental: only changed files are uploaded; keep `site/data/*.json` deterministic (stable ordering, no timestamps) so unchanged files are not re-uploaded.
- Deploy retention: 30 days (90 on paid) for old deploys, except published/latest ones.

## Other limits relevant to a static site

- Functions/Edge/Server limits: see file 05 (not used).
- Bandwidth and request quotas depend on plan/credits (not fetched; unverified).
- Support guide: processing/upload time after the build can be long for tens of thousands of new files.

## Suggested guardrails in `pipeline/build.py`

```python
import os, sys
MAX = 10 * 1024 * 1024
big = [(os.path.getsize(p), p) for r, _, fs in os.walk("site") for f in fs
       for p in [os.path.join(r, f)] if os.path.getsize(p) > MAX]
if big:
    print("WARNING: files over 10 MB (Netlify CDN guidance):", sorted(big, reverse=True), file=sys.stderr)
```
Also print total build seconds, `site/` size and file count at the end of the build to track against the 15/30 minute figures above.

## Project application

- Target a build that finishes in a few minutes: sample of 1 to 3k reviews, `nlp.pipe`, commit `nltk_data/`, avoid network downloads (docs/05 estimates about a minute of spaCy time for 3k reviews).
- First priority check on the first preview: file sizes of Pyodide wasm and wheels against the 10 MB guidance, and the pip install time on a cold cache.
- If the build ever approaches 15 minutes, reduce the sample size or ask Netlify Support for a timeout increase (per forum practice); do not move work to a function.
