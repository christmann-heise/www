/* Playwright check: synthetic events only; never call submit/requestSubmit.
 * --directory selects a local build; --base-url checks a deployment.
 * A widget constructor stub checks our Notara loader without contacting Notara.
 * All external requests and all non-read requests are blocked.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const slugs = ['', 'rechtsanwaeltinnen', 'notarinnen', 'mediatorin', 'kontakt', 'impressum', 'datenschutz'];
const arg = name => process.argv.includes(name) ? process.argv[process.argv.indexOf(name) + 1] : undefined;

// dispatchEvent has no native form-submission action; no values/action are set.
async function probe(page, injectOldBlocker = false) {
  return page.evaluate(broken => {
    const blocker = event => { event.preventDefault(); event.stopImmediatePropagation(); };
    if (broken) document.addEventListener('submit', blocker, true);
    const form = document.createElement('form');
    let targetReached = false, delegatedReached = false;
    const delegated = event => { if (event.target === form) delegatedReached = true; };
    form.addEventListener('submit', () => { targetReached = true; });
    document.addEventListener('submit', delegated);
    document.body.appendChild(form);
    try {
      const event = new Event('submit', { bubbles: true, cancelable: true });
      const accepted = form.dispatchEvent(event);
      return { accepted, defaultPrevented: event.defaultPrevented, targetReached, delegatedReached };
    } finally {
      form.remove();
      document.removeEventListener('submit', delegated);
      if (broken) document.removeEventListener('submit', blocker, true);
    }
  }, injectOldBlocker);
}

function assertUnblocked(result) {
  assert(result.accepted && !result.defaultPrevented && result.targetReached && result.delegatedReached,
    'Form event was blocked: ' + JSON.stringify(result));
}

(async () => {
  let server, browser;
  try {
    let base = arg('--base-url');
    if (!base) {
      const directory = path.resolve(root, arg('--directory') || 'public');
      assert(directory.startsWith(root + path.sep), 'Build must be inside the repository');
      const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript',
        '.css': 'text/css', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf' };
      server = http.createServer((request, response) => {
        let file = path.resolve(directory, '.' + decodeURIComponent(new URL(request.url, 'http://localhost').pathname));
        if (file !== directory && !file.startsWith(directory + path.sep)) return response.writeHead(403).end();
        try {
          if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
          response.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
          response.end(fs.readFileSync(file));
        } catch { response.writeHead(404).end(); }
      });
      await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
      base = `http://127.0.0.1:${server.address().port}/`;
    }
    base = base.replace(/\/?$/, '/');
    browser = await chromium.launch({ headless: true,
      ...(process.env.BROWSER_CHANNEL ? { channel: process.env.BROWSER_CHANNEL } : {}) });
    const context = await browser.newContext();
    let blockedWrites = 0;
    await context.route('**/*', route => {
      const request = route.request();
      if (!['GET', 'HEAD'].includes(request.method())) { blockedWrites++; return route.abort(); }
      if (new URL(request.url()).origin !== new URL(base).origin) return route.abort();
      return route.continue();
    });
    await context.addInitScript(() => {
      window.__notaraCalls = [];
      window.NotaryDatasheetWidget = function (container, id, mode) {
        window.__notaraCalls.push({ container, id, mode });
      };
    });
    const page = await context.newPage();
    const paths = ['', 'christmann-heise-designs/03-Original/'].flatMap(prefix =>
      slugs.map(slug => prefix + (slug ? slug + '/' : '')));
    const checks = [];
    for (const route of paths) {
      const url = new URL(route, base).href;
      const response = await page.goto(url, { waitUntil: 'load' });
      assert.equal(response.status(), 200, 'Page unavailable: ' + url);
      const scripts = await page.locator('script[src]').evaluateAll(elements => elements.map(e => e.src));
      assert(!scripts.some(src => new URL(src).pathname.endsWith('/preview-runtime.js')), 'Preview blocker loaded');
      if (route.endsWith('kontakt/')) assert.equal(await page.locator('form').count(), 0, 'Old contact form remains');
      await page.waitForFunction(() => window.__notaraCalls.some(call => call.id === '1499'));
      const result = await probe(page);
      assertUnblocked(result);
      checks.push({ route, notara_id: '1499', ...result });
    }
    const broken = await probe(page, true);
    assert.throws(() => assertUnblocked(broken), /Form event was blocked/);
    assert.equal(blockedWrites, 0, 'Unexpected non-read request attempted');
    const report = { base, pages: checks.length, checks, old_blocker_rejected: true,
      outgoing_submissions: 0, widget_test: 'public loader with constructor stub; no vendor form submission' };
    const output = path.join(root, 'preview-review/form-runtime');
    fs.mkdirSync(output, { recursive: true });
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ base, pages: checks.length, old_blocker_rejected: true, outgoing_submissions: 0 }));
    await context.close();
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
