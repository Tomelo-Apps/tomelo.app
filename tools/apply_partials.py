"""Copy the shared header and footer into every page of the site.

Pages mark where they go with <!--#header--> ... <!--/header--> and
<!--#footer--> ... <!--/footer-->. Run after editing anything in partials/:

    python tools/apply_partials.py

The header gets a "skip to content" link in the page's language, and the
main navigation marks the current section with aria-current="page".
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
PARTS = {name: (ROOT / "partials" / f"{name}.html").read_text(encoding="utf-8").strip()
         for name in ("header", "footer")}
SKIP = {"en": "Skip to content", "cs": "Přeskočit na obsah", "de": "Zum Inhalt springen",
        "fr": "Aller au contenu", "es": "Saltar al contenido", "it": "Vai al contenuto",
        "pl": "Przejdź do treści", "nl": "Naar de inhoud", "pt": "Saltar para o conteúdo",
        "uk": "Перейти до змісту"}


def section(page):
    rel = page.relative_to(SITE).as_posix()
    if rel.startswith("pillbell/guide/"):
        return "/pillbell/guide/"
    if rel.startswith("pillbell/"):
        return "/pillbell/"
    return None


changed = 0
for page in SITE.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    lang = (re.search(r'<html lang="([a-z]+)', text) or [None, "en"])[1]
    header = PARTS["header"].replace("{{skip}}", SKIP.get(lang, SKIP["en"]))
    current = section(page)
    if current:
        header = header.replace(f'<a href="{current}">', f'<a href="{current}" aria-current="page">', 1)
    new = re.sub(r"<!--#header-->.*?<!--/header-->", lambda m: f"<!--#header-->\n{header}\n<!--/header-->", text, flags=re.S)
    new = re.sub(r"<!--#footer-->.*?<!--/footer-->", lambda m: f"<!--#footer-->\n{PARTS['footer']}\n<!--/footer-->", new, flags=re.S)
    new = re.sub(r"<main(?![^>]*\bid=)", '<main id="main"', new)
    if new != text:
        page.write_text(new, encoding="utf-8")
        changed += 1
print(f"updated {changed} page(s)")
