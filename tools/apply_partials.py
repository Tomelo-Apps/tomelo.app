"""Copy the shared header, footer and product navigation into every page.

Pages mark where they go with <!--#header--> ... <!--/header-->,
<!--#footer--> ... <!--/footer--> and, on product pages,
<!--#product-pillbell--> ... <!--/product-pillbell-->. Run after editing
anything in partials/ or adding a translated page:

    python tools/apply_partials.py

Everything is filled in the page's language (<html lang>): the skip link, the
main navigation (aria-current marks the section), the product navigation and
the footer. Pages in other languages live under /<lang>/ (home, PillBell,
help, contact); the guide stays at /pillbell/guide/<lang>.html; legal and
privacy pages are English only. The footer gets a language switcher that links
to the same page in every language that exists, and translated page groups get
hreflang alternates in <head> (between <!--#alternates--> markers).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
BASE = "https://tomelo.app"
PART = {p.stem: p.read_text(encoding="utf-8").strip() for p in (ROOT / "partials").glob("*.html")}
LANGS = ["en", "cs", "de", "fr", "es", "it", "pl", "nl", "pt", "uk"]
NAMES = {"en": "English", "cs": "Čeština", "de": "Deutsch", "fr": "Français", "es": "Español",
         "it": "Italiano", "pl": "Polski", "nl": "Nederlands", "pt": "Português", "uk": "Українська"}
GROUPS = ["index.html", "pillbell/index.html", "pillbell/care/index.html", "help/index.html", "contact/index.html"]

T = {  # skip, home_label, main_label, apps, help, contact, tagline, note, help_centre,
       # pillbell_guide, company, legal, web_privacy, pb_privacy, language, overview, guide, privacy
    "en": ["Skip to content", "Tomelo Apps home", "Main", "Apps", "Help", "Contact",
           "Simple apps that do one job reliably.",
           "This website uses no cookies and no ads. Visits are counted without cookies.",
           "Help centre", "PillBell guide", "Company", "Legal notice", "Website privacy",
           "PillBell privacy policy", "Language", "Overview", "Guide", "Privacy", "For care services"],
    "cs": ["Přeskočit na obsah", "Tomelo Apps, úvod", "Hlavní", "Aplikace", "Nápověda", "Kontakt",
           "Jednoduché aplikace, které spolehlivě dělají jednu věc.",
           "Tento web nepoužívá cookies ani reklamy. Návštěvy počítáme bez cookies.",
           "Centrum nápovědy", "Návod k PillBell", "Firma", "Právní informace (anglicky)",
           "Soukromí na webu (anglicky)", "Zásady soukromí PillBell (anglicky)", "Jazyk",
           "Přehled", "Návod", "Soukromí", "Pro pečovatele"],
    "de": ["Zum Inhalt springen", "Tomelo Apps Startseite", "Hauptmenü", "Apps", "Hilfe", "Kontakt",
           "Einfache Apps, die eine Aufgabe zuverlässig erledigen.",
           "Diese Website nutzt keine Cookies und keine Werbung. Besuche werden ohne Cookies gezählt.",
           "Hilfe", "PillBell-Anleitung", "Unternehmen", "Impressum (Englisch)",
           "Datenschutz der Website (Englisch)", "PillBell-Datenschutzerklärung (Englisch)", "Sprache",
           "Überblick", "Anleitung", "Datenschutz", "Für Pflegedienste"],
    "fr": ["Aller au contenu", "Accueil Tomelo Apps", "Principal", "Applications", "Aide", "Contact",
           "Des applications simples qui font une seule chose, de façon fiable.",
           "Ce site n'utilise ni cookies ni publicité. Les visites sont comptées sans cookies.",
           "Centre d'aide", "Guide PillBell", "Entreprise", "Mentions légales (anglais)",
           "Confidentialité du site (anglais)", "Politique de confidentialité PillBell (anglais)", "Langue",
           "Aperçu", "Guide", "Confidentialité", "Services d'aide"],
    "es": ["Saltar al contenido", "Inicio de Tomelo Apps", "Principal", "Apps", "Ayuda", "Contacto",
           "Apps sencillas que hacen una sola cosa, y la hacen bien.",
           "Este sitio no usa cookies ni anuncios. Las visitas se cuentan sin cookies.",
           "Centro de ayuda", "Guía de PillBell", "Empresa", "Aviso legal (inglés)",
           "Privacidad del sitio (inglés)", "Política de privacidad de PillBell (inglés)", "Idioma",
           "Resumen", "Guía", "Privacidad", "Servicios de cuidados"],
    "it": ["Vai al contenuto", "Home di Tomelo Apps", "Principale", "App", "Aiuto", "Contatti",
           "App semplici che fanno una cosa sola, in modo affidabile.",
           "Questo sito non usa cookie né pubblicità. Le visite vengono contate senza cookie.",
           "Centro assistenza", "Guida di PillBell", "Azienda", "Note legali (inglese)",
           "Privacy del sito (inglese)", "Informativa privacy di PillBell (inglese)", "Lingua",
           "Panoramica", "Guida", "Privacy", "Servizi di assistenza"],
    "pl": ["Przejdź do treści", "Strona główna Tomelo Apps", "Główne", "Aplikacje", "Pomoc", "Kontakt",
           "Proste aplikacje, które niezawodnie robią jedną rzecz.",
           "Ta strona nie używa plików cookie ani reklam. Wizyty liczymy bez plików cookie.",
           "Centrum pomocy", "Instrukcja PillBell", "Firma", "Informacje prawne (po angielsku)",
           "Prywatność strony (po angielsku)", "Polityka prywatności PillBell (po angielsku)", "Język",
           "Przegląd", "Instrukcja", "Prywatność", "Dla opiekunów"],
    "nl": ["Naar de inhoud", "Tomelo Apps home", "Hoofdmenu", "Apps", "Hulp", "Contact",
           "Eenvoudige apps die één ding betrouwbaar doen.",
           "Deze website gebruikt geen cookies en geen advertenties. Bezoeken worden zonder cookies geteld.",
           "Helpcentrum", "PillBell-handleiding", "Bedrijf", "Juridische informatie (Engels)",
           "Privacy van de website (Engels)", "Privacybeleid PillBell (Engels)", "Taal",
           "Overzicht", "Handleiding", "Privacy", "Zorgorganisaties"],
    "pt": ["Saltar para o conteúdo", "Início da Tomelo Apps", "Principal", "Apps", "Ajuda", "Contacto",
           "Apps simples que fazem uma só coisa, de forma fiável.",
           "Este site não usa cookies nem anúncios. As visitas são contadas sem cookies.",
           "Centro de ajuda", "Guia do PillBell", "Empresa", "Informação legal (inglês)",
           "Privacidade do site (inglês)", "Política de privacidade do PillBell (inglês)", "Idioma",
           "Visão geral", "Guia", "Privacidade", "Apoio domiciliário"],
    "uk": ["Перейти до змісту", "Tomelo Apps, головна", "Головне", "Застосунки", "Допомога", "Контакти",
           "Прості застосунки, які надійно роблять одну справу.",
           "Цей сайт не використовує cookies і рекламу. Відвідування рахуються без cookies.",
           "Центр допомоги", "Посібник PillBell", "Компанія", "Правова інформація (англійською)",
           "Конфіденційність сайту (англійською)", "Політика конфіденційності PillBell (англійською)", "Мова",
           "Огляд", "Посібник", "Конфіденційність", "Для служб догляду"],
}
KEYS = ["skip", "home_label", "main_label", "apps", "help", "contact", "tagline", "note", "help_centre",
        "pillbell_guide", "company", "legal", "web_privacy", "pb_privacy", "language", "overview", "guide", "privacy", "care"]


def url(rel):
    """docs-relative file path -> public path."""
    return "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def split(rel):
    """'cs/help/index.html' -> ('cs', 'help/index.html'); English pages have no prefix."""
    first = rel.split("/", 1)[0]
    if first in LANGS and first != "en" and "/" in rel:
        return first, rel.split("/", 1)[1]
    return "en", rel


def variant(lang, base):
    return base if lang == "en" else f"{lang}/{base}"


def guide_rel(lang):
    return "pillbell/guide/" + ("index.html" if lang == "en" else f"{lang}.html")


def equivalents(rel):
    """{lang: rel} of existing pages that are the same page in other languages."""
    lang, base = split(rel)
    if rel.startswith("pillbell/guide/"):
        cands = {l: guide_rel(l) for l in LANGS}
    elif base in GROUPS:
        cands = {l: variant(l, base) for l in LANGS}
    else:
        cands = {l: variant(l, "index.html") for l in LANGS}
    return {l: r for l, r in cands.items() if (SITE / r).exists()}


def section(base, rel):
    if rel.startswith("pillbell/guide/") or base.startswith("help/"):
        return "/help/"
    if base.startswith("contact/"):
        return "/contact/"
    if base.startswith("pillbell/"):
        return "/#apps"
    return None


def fill(tpl, values):
    for k, v in values.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl


def mark(html, href):
    return html.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">', 1)


changed = 0
for page in sorted(SITE.rglob("*.html")):
    rel = page.relative_to(SITE).as_posix()
    text = page.read_text(encoding="utf-8")
    lang = (re.search(r'<html lang="([a-z]+)', text) or [None, "en"])[1]
    lang = lang if lang in T else "en"
    _, base = split(rel)
    p = "" if lang == "en" else f"/{lang}"
    v = dict(zip(KEYS, T[lang]))
    v["p"] = p
    v["guide_href"] = url(guide_rel(lang))


    product = fill(PART["product-pillbell"], v)
    here = {"pillbell/index.html": f"{p}/pillbell/", "pillbell/care/index.html": f"{p}/pillbell/care/", "pillbell/privacy/index.html": "/pillbell/privacy/"}.get(base)
    if rel.startswith("pillbell/guide/"):
        here = v["guide_href"]
    if here:
        product = mark(product, here)

    eq = equivalents(rel)
    links = "".join(
        f'<a href="{url(r)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if r == rel else "") + f">{NAMES[l]}</a>"
        for l, r in eq.items())
    v["langs"] = (f'<nav class="foot-langs wrap" aria-label="{v["language"]}"><span>{v["language"]}:</span> {links}</nav>'
                  if len(eq) > 1 else "")
    menu = {l: r for l, r in equivalents(rel).items()} if len(eq) > 1 else {l: variant(l, "index.html") for l in LANGS if (SITE / variant(l, "index.html")).exists()}
    items = "".join(
        f'<li><a href="{url(r)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lang else "") + f">{NAMES[l]}</a></li>"
        for l, r in menu.items())
    v["langmenu"] = (f'<details class="lang-menu"><summary aria-label="{v["language"]}: {NAMES[lang]}">'
                     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                     '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>'
                     f'<span>{lang.upper()}</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary><ul>{items}</ul></details>') if len(menu) > 1 else ""
    footer = fill(PART["footer"], v)
    header = fill(PART["header"], v)
    if section(base, rel):
        header = mark(header, p + section(base, rel))

    new = re.sub(r"<!--#header-->.*?<!--/header-->", lambda m: f"<!--#header-->\n{header}\n<!--/header-->", text, flags=re.S)
    new = re.sub(r"<!--#footer-->.*?<!--/footer-->", lambda m: f"<!--#footer-->\n{footer}\n<!--/footer-->", new, flags=re.S)
    new = re.sub(r"<!--#product-pillbell-->.*?<!--/product-pillbell-->", lambda m: f"<!--#product-pillbell-->\n{product}\n<!--/product-pillbell-->", new, flags=re.S)
    new = re.sub(r"<main(?![^>]*\bid=)", '<main id="main"', new)

    # hreflang alternates for translated page groups (the guide has its own)
    if base in GROUPS and not rel.startswith("pillbell/guide/"):
        alts = {l: r for l, r in equivalents(rel).items()}
        block = ""
        if len(alts) > 1:
            block = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{url(r)}">' for l, r in alts.items())
            block += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{url(base)}">'
        if "<!--#alternates-->" in new:
            new = re.sub(r"<!--#alternates-->.*?<!--/alternates-->\n?", (f"<!--#alternates-->\n{block}\n<!--/alternates-->\n" if block else ""), new, flags=re.S)
        elif block:
            new = re.sub(r'(<link rel="canonical"[^>]*>\n)', lambda m: m.group(1) + f"<!--#alternates-->\n{block}\n<!--/alternates-->\n", new, count=1)

    if new != text:
        page.write_text(new, encoding="utf-8")
        changed += 1
print(f"updated {changed} page(s)")
