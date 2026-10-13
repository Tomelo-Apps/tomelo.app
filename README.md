# tomelo.app: website for Tomelo Apps

A plain static site: HTML, one stylesheet, one self-hosted font and images.
No build step and no cookies. Hosted free on **GitHub Pages** (branch `main`,
folder `/docs`), domain and DNS at Cloudflare. Live at https://tomelo.app.

Rules for anyone editing (people and AI agents) are in [`CLAUDE.md`](CLAUDE.md).
Strategy, brand and decisions live in the private repo `tomelo-apps/workspace`.

```
docs/                     the published website
  index.html              home page (English)
  pillbell/               PillBell landing page, guide/ (10 languages + screenshots), privacy/
  help/  contact/         help centre, contact
  privacy/  legal/        website privacy notice, legal notice (English only)
  cs/ de/ fr/ es/ it/ pl/ nl/ pt/ uk/
                          home, PillBell, help and contact in the other 9 app languages
  assets/                 site.css, fonts/, badges/ (official Google Play), photos/, logo, favicon, og images
  404.html robots.txt sitemap.xml CNAME .nojekyll
partials/                 header, footer, product navigation (filled into every page)
tools/apply_partials.py   fills partials into every page in the page's language,
                          adds the language menu and hreflang links
tools/build_sitemap.py    regenerates docs/sitemap.xml from the pages
tools/check_site.cjs      pre-publish check: links, accessibility, overflow, font size, contrast
```

## Everyday work
1. Work on a branch. `main` is live.
2. Edit pages in `docs/`. When you change English copy, change the same place
   in every `docs/<lang>/` copy.
3. Header, footer, PillBell menu or language menu: edit `partials/` (texts per
   language in the `T` table in `tools/apply_partials.py`), then run
   `python3 tools/apply_partials.py`.
4. Added or removed a page: run `python3 tools/apply_partials.py` and
   `python3 tools/build_sitemap.py`.
5. Check: `python3 -m http.server 8765 -d docs &` then
   `node tools/check_site.cjs` (needs `npm i -g playwright axe-core` and
   `NODE_PATH=$(npm root -g)`). It must end with `OK`.
6. Show a preview, get approval, merge to `main`. GitHub Pages publishes in
   about a minute. After structural changes, resubmit
   `https://tomelo.app/sitemap.xml` in Google Search Console.

## Languages
English is the source. Pages in `docs/<lang>/` are translated copies; all
except English and Czech are machine drafts (`status: draft` comment in
`<head>`) until a native speaker approves them. App screenshots exist in
English, Czech and German (`docs/pillbell/guide/img/<lang>/`); the other
guides use the English ones and say so.

## Adding an app
Copy `docs/pillbell/` to `docs/<app>/` (and to each `docs/<lang>/<app>/`),
replace text and screenshots, copy `partials/product-pillbell.html` to
`product-<app>.html` and teach `tools/apply_partials.py` its marker, add a tile
on the home pages and a block on the help pages, then run both tools.

## Assets
- **Photos** (`docs/assets/photos/`): AI-generated scenes with real app
  screenshots composited in. Source images and the script are in the workspace
  repo, `podklady/znacka/fotky/`. Re-run it when screenshots change.
- **Google Play badges** (`docs/assets/badges/`): official artwork from the npm
  package `@rewilok/app-store-badges` (see `NOTICE.txt`). Never redraw,
  recolour or crop; keep the trademark line on `/legal/`.
- **Analytics**: Cloudflare Web Analytics (cookie-free), loaded from the footer
  partial and described on `/privacy/`.

## Open operations tasks
- [ ] Play Console (PillBell → Store settings): website `https://tomelo.app/pillbell/`,
      email `support@tomelo.app`, privacy policy `https://tomelo.app/pillbell/privacy/`.
- [ ] Old site (`tomashrbatik-coder.github.io/pillbell-legal`): turn each page into a
      redirect (`index.html` → `/pillbell/`, `guide.html` → `/pillbell/guide/`,
      `guide-xx.html` → `/pillbell/guide/xx.html`, `privacy-policy.html` → `/pillbell/privacy/`).
- [ ] When PillBell switches to free + one-time unlock: add a "Purchases" section to
      `docs/pillbell/privacy/` and every language's PillBell page, and update the
      `offers` price in the PillBell JSON-LD.
