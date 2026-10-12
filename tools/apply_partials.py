"""Copy the shared header, footer and product navigation into every page.

Pages mark where they go with <!--#header--> ... <!--/header-->,
<!--#footer--> ... <!--/footer--> and, on product pages,
<!--#product-pillbell--> ... <!--/product-pillbell-->. Run after editing
anything in partials/:

    python tools/apply_partials.py

The header gets a "skip to content" link in the page's language, the main
navigation marks the current section with aria-current="page", and the product
navigation is translated into the page's language.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
PART = {p.stem: p.read_text(encoding="utf-8").strip() for p in (ROOT / "partials").glob("*.html")}
SKIP = {"en": "Skip to content", "cs": "Přeskočit na obsah", "de": "Zum Inhalt springen",
        "fr": "Aller au contenu", "es": "Saltar al contenido", "it": "Vai al contenuto",
        "pl": "Przejdź do treści", "nl": "Naar de inhoud", "pt": "Saltar para o conteúdo",
        "uk": "Перейти до змісту"}
PRODUCT = {  # overview, guide, privacy
    "en": ("Overview", "Guide", "Privacy"), "cs": ("Přehled", "Návod", "Soukromí"),
    "de": ("Überblick", "Anleitung", "Datenschutz"), "fr": ("Aperçu", "Guide", "Confidentialité"),
    "es": ("Resumen", "Guía", "Privacidad"), "it": ("Panoramica", "Guida", "Privacy"),
    "pl": ("Przegląd", "Instrukcja", "Prywatność"), "nl": ("Overzicht", "Handleiding", "Privacy"),
    "pt": ("Visão geral", "Guia", "Privacidade"), "uk": ("Огляд", "Посібник", "Конфіденційність")}


def section(rel):
    if rel.startswith(("help/", "pillbell/guide/")):
        return "/help/"
    if rel.startswith("contact/"):
        return "/contact/"
    if rel.startswith("pillbell/") or rel == "index.html":
        return "/#apps" if rel != "index.html" else None
    return None


def mark(html, href):
    return html.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">', 1)


changed = 0
for page in SITE.rglob("*.html"):
    rel = page.relative_to(SITE).as_posix()
    text = page.read_text(encoding="utf-8")
    lang = (re.search(r'<html lang="([a-z]+)', text) or [None, "en"])[1]
    header = PART["header"].replace("{{skip}}", SKIP.get(lang, SKIP["en"]))
    if section(rel):
        header = mark(header, section(rel))
    ov, gd, pr = PRODUCT.get(lang, PRODUCT["en"])
    guide_href = "/pillbell/guide/" + ("" if lang == "en" else f"{lang}.html")
    product = (PART["product-pillbell"].replace("{{overview}}", ov).replace("{{guide}}", gd)
               .replace("{{privacy}}", pr).replace("{{guide_href}}", guide_href))
    here = {"pillbell/index.html": "/pillbell/", "pillbell/privacy/index.html": "/pillbell/privacy/"}.get(rel)
    product = mark(product, here or guide_href) if (here or rel.startswith("pillbell/guide/")) else product
    new = re.sub(r"<!--#header-->.*?<!--/header-->", lambda m: f"<!--#header-->\n{header}\n<!--/header-->", text, flags=re.S)
    new = re.sub(r"<!--#footer-->.*?<!--/footer-->", lambda m: f"<!--#footer-->\n{PART['footer']}\n<!--/footer-->", new, flags=re.S)
    new = re.sub(r"<!--#product-pillbell-->.*?<!--/product-pillbell-->", lambda m: f"<!--#product-pillbell-->\n{product}\n<!--/product-pillbell-->", new, flags=re.S)
    new = re.sub(r"<main(?![^>]*\bid=)", '<main id="main"', new)
    if new != text:
        page.write_text(new, encoding="utf-8")
        changed += 1
print(f"updated {changed} page(s)")
