# 04 — Playwright (end-to-end tests for the static site)

Sources:
- https://playwright.dev/docs/writing-tests
- https://playwright.dev/docs/locators
- https://playwright.dev/docs/test-assertions
- https://playwright.dev/docs/actionability
- https://playwright.dev/docs/emulation
- https://playwright.dev/docs/test-webserver
- https://playwright.dev/docs/trace-viewer-intro

Fetched: 2026-11-20 (pages are Docusaurus "stable"; examples are JS/TS Playwright Test. pytest-playwright was **not** fetched — unverified; recommend Playwright Test for JS because the site is JS.)

## Test basics (writing-tests)
```js
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);        // substring/regex
});
test('get started link', async ({ page }) => {
  await page.getByRole('link', { name: 'Get started' }).click();
  await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});
```
- Hooks: `test.describe`, `test.beforeEach` / `afterEach` (per test), `test.beforeAll` / `afterAll` (once per worker).

## Locators
Recommended built-ins: `page.getByRole()` (preferred — "prioritizing user-facing attributes and explicit contracts"), `getByText()`, `getByLabel()`, `getByPlaceholder()`, `getByTestId()` (matches `data-testid`).
`await page.getByRole('button').click();` Locators are strict: an action on a locator that resolves to several elements errors (strictness; standard behaviour, "exactly one element" is in the actionability list).

## Assertions & waiting
- Web-first assertions **auto-retry** until they pass or the assertion timeout is hit; they are async, so always `await`.
- Verified retrying assertions: `toBeVisible()`, `toBeHidden()`, `toBeAttached()`, `toBeEnabled()/Disabled()`, `toBeInViewport()`, `toHaveText()` (element matches text), `toContainText()`, `toHaveCount()` (list has exact number of children), `toHaveValue()`, `toHaveTitle()`/`toHaveURL()` (page), `toMatchAriaSnapshot()`.
- Custom timeout: `const slowExpect = expect.configure({ timeout: 10000 }); await slowExpect(locator).toHaveText('Submit');`
- Soft assertions (do not stop the test): `await expect.soft(locator).toHaveText('Success');` (runner only).
- **Auto-waiting (actionability)**: before an action, Playwright waits until the locator resolves to exactly one element that is Visible, Stable (not animating), Receives Events (not obscured), Enabled (and Editable/Not Inert where relevant); otherwise the action fails with `TimeoutError`.
- Implication: do not use fixed `waitForTimeout` sleeps; wait with `expect(...)` on something the page renders (e.g. the results table) — important because Pyodide takes seconds to load.

## Mobile / device projects (emulation)
```js
// playwright.config.js
import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  projects: [
    { name: 'chromium',      use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 13'] } },
  ],
});
```
- Override size with `use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 720 } }`.
- Run one project: `npx playwright test --project="Mobile Safari"` (`--project` is a standard CLI flag; not on the page fetched). Other device names (e.g. `Pixel 5`) come from the same `devices` registry (unverified here).

## Serving the static folder (webServer)
```js
export default defineConfig({
  webServer: {
    command: 'npx http-server site -p 3000 -s',   // http-server is an assumption, any static server works
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore', stderr: 'pipe',
    // timeout: 60000 (default) = how long to wait for the server to be up
  },
  use: { baseURL: 'http://localhost:3000' },
});
```
- With `baseURL` set, `await page.goto('./')` / `page.goto('/')` resolves relative to it (docs: `page.goto('./login')` → `http://localhost:3000/login`). Docs say `page.route`, `waitForURL`, `waitForRequest/Response` also honour baseURL.
- The server command's `url` is polled until it responds before tests start.

## Tracing (trace-viewer-intro)
- Config default: `use: { trace: 'on-first-retry' }` (traces recorded on first retry of a failed test; retries typically 2 on CI, 0 locally).
- Force locally: `npx playwright test --trace on`. Open via `npx playwright show-report` and click the trace icon for a test.
- A `trace.zip` holds actions, DOM snapshots and network — attach it to bug reports.

## Project application
- Smoke test list: page loads with no console errors; dashboard charts/tables render from `data/*.json` (`toHaveCount(>0)` via `expect.poll` or `toBeVisible` on a row); "Analyze your own review" box: type a review, click Analyze, expect a sentiment badge to be visible within a generous timeout (e.g. `expect(...).toBeVisible({ timeout: 60_000 })`) because Pyodide + NLTK data must download first.
- Assertions on text: `toHaveText(/positive/i)` for the doc-02 sample ("amazing ... disappointing" must show a mixed per-sentence result).
- Projects: `Desktop Chrome` + one phone (`iPhone 13` from the docs). Check no horizontal scroll: `expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)` (plain DOM, project suggestion).
- Use `getByRole` / `getByTestId` — add `data-testid` hooks to dashboard widgets for stability.
- CI: `reuseExistingServer: !process.env.CI`, `trace: 'on-first-retry'`, upload `playwright-report/`.
