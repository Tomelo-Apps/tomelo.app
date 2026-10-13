// Check every page in docs/ before publishing.
//
//   python3 -m http.server 8765 -d docs &      (serve the site locally)
//   node tools/check_site.cjs                   (needs: npm i -g playwright axe-core)
//
// Reports, per page: broken internal links, axe-core WCAG 2.2 AA violations,
// horizontal overflow at 320 px, text smaller than 16 px and text with too
// little contrast (4.5:1, 3:1 for large text). Exit code 1 if anything fails.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const BASE = process.env.BASE || 'http://localhost:8765';
const DOCS = path.join(__dirname, '..', 'docs');
let axeSrc = null;
try { axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8'); } catch (e) {
  console.warn('axe-core not found: accessibility rules skipped (npm i -g axe-core, NODE_PATH=$(npm root -g))');
}

const pages = [];
(function walk(dir) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if (f.endsWith('.html')) pages.push('/' + path.relative(DOCS, p).replace(/\\/g, '/').replace(/index\.html$/, ''));
  }
})(DOCS);
pages.sort();

function exists(href) {
  const clean = decodeURIComponent(href.split('#')[0].split('?')[0]);
  let p = path.join(DOCS, clean);
  if (clean.endsWith('/')) p = path.join(p, 'index.html');
  return fs.existsSync(p);
}

(async () => {
  const browser = await chromium.launch();
  let failures = 0;
  const report = (page, msg) => { failures++; console.log(`✗ ${page}: ${msg}`); };
  for (const [width, a11y] of [[1280, true], [320, false]]) {
    const p = await browser.newPage({ viewport: { width, height: 900 } });
    await p.route(r => !r.href.startsWith(BASE), r => r.abort()); // no external requests (analytics)
    for (const u of pages) {
      await p.goto(BASE + u, { waitUntil: 'load' });
      if (width === 1280) {
        const hrefs = await p.evaluate(() => [...document.querySelectorAll('[href^="/"],[src^="/"]')]
          .map(e => e.getAttribute('href') || e.getAttribute('src')));
        for (const h of new Set(hrefs)) if (!exists(h)) report(u, `broken link ${h}`);
      }
      const sw = await p.evaluate(() => document.documentElement.scrollWidth);
      if (sw > width + 1) report(u, `page is ${sw}px wide at ${width}px (horizontal scroll)`);
      if (a11y && axeSrc) {
        await p.addScriptTag({ content: axeSrc });
        const v = await p.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag',
          values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } })).violations
          .map(x => `${x.id} (${x.nodes.length}×) e.g. ${x.nodes[0].target.join(' ')}`));
        v.forEach(m => report(u, `axe: ${m}`));
      }
      if (a11y) {
        const t = await p.evaluate(() => {
          const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
          const lum = ({ r, g, b }) => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
          const bgOf = el => { for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.9) return c; } return { r: 255, g: 255, b: 255 }; };
          const out = [], seen = new Set();
          const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          while (w.nextNode()) {
            const n = w.currentNode, el = n.parentElement;
            if (!n.textContent.trim() || seen.has(el) || el.closest('svg')) continue; seen.add(el);
            const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
            if (cs.visibility === 'hidden' || r.width === 0) continue;
            const fs = parseFloat(cs.fontSize), fg = parse(cs.color), bg = bgOf(el);
            if (!fg) continue;
            const L1 = lum(fg), L2 = lum(bg), cr = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
            const need = (fs >= 24 || (fs >= 18.66 && parseInt(cs.fontWeight) >= 700)) ? 3 : 4.5;
            if (fs < 16 || cr < need) out.push(`"${n.textContent.trim().slice(0, 30)}" ${fs}px contrast ${cr.toFixed(1)}`);
          }
          return out.slice(0, 5);
        });
        t.forEach(m => report(u, `text: ${m}`));
      }
    }
    await p.close();
  }
  await browser.close();
  console.log(failures ? `\n${failures} problem(s) on ${pages.length} pages` : `OK: ${pages.length} pages, no problems`);
  process.exit(failures ? 1 : 0);
})();
