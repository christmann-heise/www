/* Compare rendered typography with the preserved original, not CSS names alone.
 * Requires Playwright and Edge (Windows) or Playwright Chromium (other systems).
 * Run after build-site.py. Optional --base-url targets a published /www/ root.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {isDeepStrictEqual} = require('node:util');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../public');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.jpg':'image/jpeg','.png':'image/png','.ttf':'font/ttf','.woff2':'font/woff2'};
const server = http.createServer((req, res) => {
    const name = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/www\//, '/');
    let file = path.resolve(root, '.' + name);
    if (file !== root && !file.startsWith(root + path.sep)) return res.writeHead(403).end();
    try {
        if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        res.writeHead(200, {'Content-Type': types[path.extname(file)] || 'application/octet-stream'});
        res.end(fs.readFileSync(file));
    } catch { res.writeHead(404).end(); }
});
const slugs = ['', 'rechtsanwaeltinnen/', 'notarinnen/', 'mediatorin/', 'kontakt/', 'impressum/', 'datenschutz/'];
const themes = ['04-Arcana/', '05-Agnes/', '06-Blunix/'];
const results = [];
const differences = [];

async function typography(page) {
    await page.evaluate(() => document.fonts.ready);
    return page.locator('.module-header, .fw-page-builder-content').evaluateAll(roots => roots.flatMap(root =>
        [...root.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,label,blockquote,span,strong')]
            .filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && e.textContent.trim())
            .map(e => {
                const css = getComputedStyle(e);
                const style = Object.fromEntries(['fontSize','fontStyle','fontWeight','letterSpacing','lineHeight','textTransform','color'].map(k => [k, css[k]]));
                style.fontFamily = css.fontFamily.split(',')[0].replaceAll('"', '').trim();
                return {text:e.textContent.trim(), tag:e.tagName, style};
            })));
}

async function actualFont(page, cdp, selector, family) {
    const doc = await cdp.send('DOM.getDocument');
    const {nodeId} = await cdp.send('DOM.querySelector', {nodeId:doc.root.nodeId, selector});
    assert(nodeId, 'Missing font sample: ' + selector);
    const {fonts} = await cdp.send('CSS.getPlatformFontsForNode', {nodeId});
    assert(fonts.some(f => f.familyName === family && f.isCustomFont), 'Rendered font differs: ' + JSON.stringify({selector, fonts}));
}

async function navigation(page, selector) {
    return page.locator(selector).first().evaluate(e => {
        const c=getComputedStyle(e);
        return Object.fromEntries(['fontSize','fontStyle','fontWeight','letterSpacing','lineHeight','textTransform'].map(k=>[k,c[k]]));
    });
}

(async () => {
    const flag = process.argv.indexOf('--base-url');
    let base = flag >= 0 ? process.argv[flag + 1] : null;
    if (!base) {
        await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
        base = 'http://127.0.0.1:' + server.address().port + '/www/';
    }
    const browser = await chromium.launch(process.platform === 'win32' ? {channel:'msedge', headless:true} : {headless:true});
    try {
        const page = await browser.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push({url:page.url(), message:error.message}));
        const cdp = await page.context().newCDPSession(page);
        await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
        const design = base.replace(/\/?$/, '/') + 'christmann-heise-designs/';
        for (const width of [1440, 390]) {
            await page.setViewportSize({width, height:1000});
            for (const slug of slugs) {
                await page.goto(design + '03-Original/' + slug, {waitUntil:'networkidle'});
                const original = await typography(page);
                const originalNav = await navigation(page, '.inner-navigation a');
                const originalCopyright = await navigation(page, '.footer .copyright');
                const originalFooterLink = await navigation(page, '.social-text-list a');
                assert(original.length, 'Missing original text');
                for (const theme of themes) {
                    await page.goto(design + theme + slug, {waitUntil:'networkidle'});
                    const actual = await typography(page);
                    if (!isDeepStrictEqual(actual, original)) differences.push({width, route:theme + slug, items:actual.flatMap((item, i) => isDeepStrictEqual(item, original[i]) ? [] : [{text:item.text.slice(0,90), actual:item.style, original:original[i]?.style}])});
                    await actualFont(page, cdp, '.module-header h1', 'Dosis');
                    const navSelector = theme === '04-Arcana/' ? '#nav>ul>li>a' : theme === '05-Agnes/' ? '.site-header nav a' : '#topnav .navigation-menu>li>a';
                    assert.deepEqual(await navigation(page, navSelector), originalNav, 'Navigation typography differs: ' + theme);
                    assert.deepEqual(await navigation(page, theme === '04-Arcana/' ? '#footer p' : 'footer p'), originalCopyright, 'Copyright typography differs: ' + theme);
                    const footerLink = theme === '04-Arcana/' ? '#footer .links a' : theme === '05-Agnes/' ? '.site-footer .footer-links a' : '.footer-list a';
                    assert.deepEqual(await navigation(page, footerLink), originalFooterLink, 'Footer typography differs: ' + theme);
                    if (slug === 'mediatorin/') await actualFont(page, cdp, 'blockquote p', 'Libre Baskerville');
                    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, `Overflow: ${width} ${theme}${slug}`);
                    results.push({width, route:theme + slug, matchedTextElements:original.length});
                }
            }
            for (const legacy of ['01-Ruhig-Salbei.html', '02-Editorial-Bordeaux.html']) {
                await page.goto(design + legacy, {waitUntil:'networkidle'});
                assert.deepEqual(await navigation(page, '.nav a'), {fontSize:'10px', fontStyle:'normal', fontWeight:'400', letterSpacing:'2px', lineHeight:'18px', textTransform:'uppercase'});
                for (const slug of ['/', '/rechtsanwaeltinnen/', '/kontakt/', '/']) {
                    await page.evaluate(async slug => {
                        if (location.hash === '#' + slug) return;
                        const changed = new Promise(resolve => window.addEventListener('hashchange', () => setTimeout(resolve, 0), {once:true}));
                        location.hash = '#' + slug;
                        await changed;
                    }, slug);
                    await page.evaluate(() => document.fonts.ready);
                    const expected = slug === '/' || slug === '/rechtsanwaeltinnen/' ? 2 : 0;
                    await page.waitForFunction(expected => {
                        const images = [...document.querySelectorAll('.portrait img')];
                        return images.length === expected && images.every(x => x.complete && x.naturalWidth > 0 && x.naturalHeight > 0);
                    }, expected);
                    assert.equal(await page.locator('.portrait-letter').count(), 0, 'Router restored portrait placeholders');
                    await actualFont(page, cdp, 'h1', 'Dosis');
                    const style = await page.locator('h1').first().evaluate(e => {
                        const c=getComputedStyle(e);return {size:c.fontSize, weight:c.fontWeight, spacing:c.letterSpacing, casing:c.textTransform};
                    });
                    assert.deepEqual(style, {size:width === 390 ? '17px' : '25px', weight:'400', spacing:width === 390 ? '12px' : '24px', casing:'uppercase'});
                    results.push({width, route:legacy + '#' + slug, portraits:expected, heading:style});
                }
                const overflow = await page.evaluate(() => [...document.querySelectorAll('body *')].filter(e => {
                    const r=e.getBoundingClientRect();return r.right>innerWidth+1 && r.width>0 && getComputedStyle(e).position!=='fixed';
                }).slice(0,12).map(e=>({tag:e.tagName,classes:e.className,text:e.textContent.trim().slice(0,70),width:e.getBoundingClientRect().width})));
                if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)) differences.push({width, route:legacy, overflow});
            }
        }
        assert.deepEqual(errors, [], 'Browser script errors');
        console.log(JSON.stringify({checks:results, differences, errors}, null, 2));
        assert.deepEqual(differences, [], 'Typography differs from the original');
    } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;}).finally(() => server.close());
