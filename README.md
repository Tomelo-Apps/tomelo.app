# tomelo.app: website for Tomelo Apps

A plain static site: HTML, one stylesheet, one self-hosted font and images.
No build step, no server, no cookies, no analytics, and nothing loaded from
other companies. Logo source files and brand rules live in the workspace repo
(`podklady/znacka/`).
It's hosted free on **GitHub Pages**. The only cost is the domain.

```
docs/                    ← the published website (GitHub Pages: branch main, folder /docs)
  index.html             Tomelo Apps home page
  pillbell/index.html    PillBell landing page
  pillbell/guide/        PillBell guide in 10 languages (moved from pillbell-legal) + screenshots
  pillbell/privacy/      PillBell app privacy policy
  privacy/               website privacy notice
  legal/                 legal notice (sole-trader details)
  404.html, robots.txt, sitemap.xml, CNAME, .nojekyll
  assets/                site.css, logo.svg (Tomelo mark), favicon.svg, fonts/ (Figtree, OFL, self-hosted)
partials/                shared header + footer
tools/apply_partials.py  copies the header/footer into every page
```

Editing the header or footer: change `partials/*.html`, then run
`python tools/apply_partials.py`.

Adding app #2: copy `docs/pillbell/` to `docs/<app>/`, replace the text and
screenshots, add a tile on `docs/index.html` and links in
`partials/footer.html`, run the script, and add the new pages to `sitemap.xml`.

---

## Going live: about 1 hour, once

### 1. Buy the domains (≈ €40/year)

| Domain | Where | Why |
|---|---|---|
| `tomelo.app` | **Cloudflare Registrar** (sold at cost) or Porkbun | Main site. Cloudflare also gives free DNS and free email forwarding (step 4). |
| `tomelo.cz` | A Czech registrar: WEDOS, Forpsi or Active24 | Protects the name; set it to redirect to tomelo.app. Cloudflare doesn't sell `.cz`. |
| `tomelo.eu` | The same Czech registrar, or Porkbun | Protects the name; redirect to tomelo.app. |

Register them in **Tomáš's name** (he's the legal owner as a sole trader),
from the shared brand Google account, with 2-step verification on.

### 2. Put the site on GitHub

1. Create a free **GitHub organisation** named `tomelo-apps` from the brand
   account, with both of you as owners.
2. Create a public repository in it called `tomelo.app`.
3. Done: this repository holds the site in `docs/`.
4. Repository → **Settings → Pages** → Source: *Deploy from a branch*,
   branch `main`, folder **`/docs`**.

### 3. Connect the domain (DNS at Cloudflare)

1. GitHub: **Organisation settings → Pages → Add a verified domain** →
   `tomelo.app`. GitHub shows a TXT record. Add it at Cloudflare, then click
   *Verify*. This stops anyone else using your domain on GitHub.
2. Cloudflare DNS for `tomelo.app`, with every record set to **DNS only**
   (grey cloud):
   - `A` `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `AAAA` `@` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `CNAME` `www` → `tomelo-apps.github.io`
3. Repository → Settings → Pages → Custom domain: `tomelo.app` (the `CNAME`
   file in the site already says this) → wait for the certificate → tick
   **Enforce HTTPS**.
   Browsers only open `.app` sites over HTTPS, so the site appears once
   GitHub has issued the certificate. That usually takes minutes, sometimes
   up to an hour.

### 4. Email addresses: must work before the site goes live

The site shows `support@tomelo.app` and `hello@tomelo.app`.

1. Cloudflare → **Email Routing** (free) → forward `support@`, `hello@`
   and `press@` to the brand Gmail.
2. Gmail → Settings → *Accounts → Send mail as* → add `support@tomelo.app`,
   using Gmail's own SMTP with an app password, so replies come from the
   brand address.
3. Use Gmail delegation to give both personal accounts access.

### 5. After it's live

- [ ] Replace `[DATE THE SITE GOES LIVE]` in `docs/privacy/index.html`.
- [ ] **Google Search Console**: add a *Domain* property for `tomelo.app`
      (verified with a TXT record at Cloudflare) and submit
      `https://tomelo.app/sitemap.xml`.
- [ ] **Play Console** (PillBell → Store settings): set the website to
      `https://tomelo.app/pillbell/`, the email to `support@tomelo.app`, the
      privacy policy to `https://tomelo.app/pillbell/privacy/`, and remove
      the personal phone number.
- [ ] **Old site** (`tomashrbatik-coder.github.io/pillbell-legal`): keep it
      online and turn every page into a redirect to its new address. The app
      or older listings may still link there. Each old page becomes:
      ```html
      <!DOCTYPE html><meta charset="utf-8">
      <link rel="canonical" href="https://tomelo.app/pillbell/guide/de.html">
      <meta http-equiv="refresh" content="0; url=https://tomelo.app/pillbell/guide/de.html">
      <a href="https://tomelo.app/pillbell/guide/de.html">PillBell guide moved here</a>
      ```
      Mapping: `index.html` → `/pillbell/`, `guide.html` → `/pillbell/guide/`,
      `guide-xx.html` → `/pillbell/guide/xx.html`,
      `privacy-policy.html` → `/pillbell/privacy/`.
- [ ] If the app itself links to the old guide or privacy URLs, point them
      to tomelo.app in the next release. The redirects cover older versions.

### On the day PillBell switches to free + one-time unlock

Apply the same wording as `pillbell/site-patches/0002-*`: a "Purchases"
section in `docs/pillbell/privacy/index.html`, and check the "pay once"
wording on the landing page.
