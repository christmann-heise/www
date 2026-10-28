/* Requires Playwright. Checks actual rendered glyph fonts, including a broken-font counterexample.
 * Default: serve public/ locally. --base-url https://example.org/ checks a deployment.
 * Set BROWSER_CHANNEL=msedge to use an installed Edge instead of bundled Chromium.
 * External requests and all submissions are blocked; Notara forms are never opened.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const output = path.join(root, 'preview-review/linea-icons');
const cases = [
  { slug: 'rechtsanwaeltinnen', selector: '.icon-basic-info', count: 5 },
  { slug: 'mediatorin', selector: '.icon-basic-message-multiple', count: 1 },
];
const viewports = [{ width: 1440, height: 1000 }, { width: 390, height: 844 }];
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css',
  '.js': 'application/javascript', '.woff': 'font/woff', '.ttf': 'font/ttf',
  '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png' };

function serve() {
  const directory = path.join(root, 'public');
  return http.createServer((request, response) => {
    let file = path.resolve(directory, '.' + decodeURIComponent(new URL(request.url, 'http://localhost').pathname));
    if (!file.startsWith(directory + path.sep)) return response.writeHead(403).end();
    try {
      if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
      response.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
      response.end(fs.readFileSync(file));
    } catch { response.writeHead(404).end(); }
  });
}

async function inspect(page, item, url) {
  const response = await page.goto(url, { waitUntil: 'load' });
  assert.equal(response.status(), 200, 'Page unavailable: ' + url);
  await page.locator('.page-loader').waitFor({ state: 'hidden' });
  const dismiss = page.locator('.cc-dismiss');
  if (await dismiss.count() && await dismiss.isVisible()) {
    await dismiss.click();
    await page.waitForFunction(() => [...document.querySelectorAll('.cc-window')].every(element =>
      getComputedStyle(element).display === 'none' || Number(getComputedStyle(element).opacity) < 0.01));
  }
  await page.evaluate(() => document.fonts.ready);
  const loaded = await page.evaluate(() => document.fonts.check('42px "linea-basic-10"', '0'));
  assert(loaded, 'Icon font not loaded: ' + url);
  assert.equal(await page.locator(item.selector).count(), item.count, 'Original icon count changed');
  const session = await page.context().newCDPSession(page);
  try {
    await session.send('DOM.enable');
    await session.send('CSS.enable');
    const { root: document } = await session.send('DOM.getDocument', { depth: -1, pierce: true });
    const { nodeIds } = await session.send('DOM.querySelectorAll', { nodeId: document.nodeId, selector: item.selector });
    const rendered = [];
    for (const nodeId of nodeIds) {
      const { node } = await session.send('DOM.describeNode', { nodeId, depth: 1 });
      const before = node.pseudoElements?.find(element => element.pseudoType === 'before');
      assert(before?.nodeId, 'Missing original icon pseudo-element');
      const { fonts } = await session.send('CSS.getPlatformFontsForNode', { nodeId: before.nodeId });
      assert(fonts.some(font => font.isCustomFont && font.familyName === 'linea-basic-10' && font.glyphCount > 0),
        'Icon font not used: ' + JSON.stringify(fonts));
      rendered.push(fonts);
    }
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false,
      'Horizontal overflow: ' + url);
    return { url, viewport: page.viewportSize(), count: rendered.length, rendered };
  } finally { await session.detach(); }
}

async function contextFor(browser, base, viewport, broken = false) {
  const context = await browser.newContext({ viewport });
  await context.route('**/*', route => {
    const request = route.request();
    const url = new URL(request.url());
    if (!['GET', 'HEAD'].includes(request.method()) || url.origin !== new URL(base).origin ||
        (broken && url.pathname.includes('/fonts/linea-basic-10.'))) return route.abort();
    return route.continue();
  });
  return context;
}

(async () => {
  let server, browser;
  try {
    fs.mkdirSync(output, { recursive: true });
    const option = process.argv.indexOf('--base-url');
    let base;
    if (option !== -1) {
      assert(process.argv[option + 1], '--base-url needs a URL');
      base = process.argv[option + 1].replace(/\/?$/, '/');
    } else {
      server = serve();
      await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
      base = `http://127.0.0.1:${server.address().port}/`;
    }
    browser = await chromium.launch({ headless: true,
      ...(process.env.BROWSER_CHANNEL ? { channel: process.env.BROWSER_CHANNEL } : {}) });
    const report = { base, checks: [], missing_font_rejected: false };
    for (const viewport of viewports) {
      const context = await contextFor(browser, base, viewport);
      try {
        const page = await context.newPage();
        for (const prefix of ['', 'christmann-heise-designs/03-Original/']) {
          for (const item of cases) {
            report.checks.push(await inspect(page, item, new URL(prefix + item.slug + '/', base).href));
            if (!prefix) {
              const section = page.locator(item.selector).first().locator('xpath=ancestor::section').first();
              await section.screenshot({ path: path.join(output, `${item.slug}-${viewport.width}.png`) });
            }
          }
        }
      } finally { await context.close(); }
    }
    const broken = await contextFor(browser, base, viewports[0], true);
    try {
      await assert.rejects(() => broken.newPage().then(page => inspect(page, cases[0],
        new URL('rechtsanwaeltinnen/', base).href)), /Icon font (?:not loaded|not used)/);
      report.missing_font_rejected = true;
    } finally { await broken.close(); }
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ base, browser_checks: report.checks.length,
      rendered_icons: report.checks.reduce((sum, check) => sum + check.count, 0),
      missing_font_rejected: report.missing_font_rejected }));
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
