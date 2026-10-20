"""Write docs/sitemap.xml from the pages in docs/.

Every public page is listed with today's date as lastmod (pass a date to
override: python tools/build_sitemap.py 2026-10-13). Pages that exist in
several languages get hreflang alternates, the same ones apply_partials.py
puts in <head>. 404.html is left out.
"""
import datetime
import pathlib
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "docs"
BASE = "https://tomelo.app"
LANGS = ["en", "cs", "de", "fr", "es", "it", "pl", "nl", "pt", "uk"]
GROUPS = ["index.html", "pillbell/index.html", "widgets/index.html", "help/index.html", "contact/index.html"]
day = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()


def url(rel):
    return BASE + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def alternates(rel):
    first, _, rest = rel.partition("/")
    base = rest if first in LANGS and first != "en" and rest else rel
    if rel.startswith("pillbell/guide/"):
        cands = {l: "pillbell/guide/" + ("index.html" if l == "en" else f"{l}.html") for l in LANGS}
        default = "pillbell/guide/index.html"
    elif base in GROUPS:
        cands = {l: base if l == "en" else f"{l}/{base}" for l in LANGS}
        default = base
    else:
        return {}, None
    found = {l: r for l, r in cands.items() if (SITE / r).exists()}
    return (found, default) if len(found) > 1 else ({}, None)


def order(rel):
    first = rel.split("/", 1)[0]
    lang = first if first in LANGS and "/" in rel else "en"
    return (LANGS.index(lang) if not rel.startswith("pillbell/guide/") else 0, rel.count("/"), rel)


pages = sorted((p.relative_to(SITE).as_posix() for p in SITE.rglob("*.html") if p.name != "404.html"), key=order)
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for rel in pages:
    alts, default = alternates(rel)
    if not alts:
        out.append(f"  <url><loc>{url(rel)}</loc><lastmod>{day}</lastmod></url>")
        continue
    out.append(f"  <url>\n    <loc>{url(rel)}</loc><lastmod>{day}</lastmod>")
    out += [f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url(r)}"/>' for l, r in alts.items()]
    out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url(default)}"/>\n  </url>')
out.append("</urlset>")
(SITE / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"sitemap: {len(pages)} URLs")
