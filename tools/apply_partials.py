"""Copy the shared header and footer into every page of the site.

Pages mark where they go with <!--#header--> ... <!--/header--> and
<!--#footer--> ... <!--/footer-->. Run after editing anything in partials/:

    python tomelo/tools/apply_partials.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
PARTS = {name: (ROOT / "partials" / f"{name}.html").read_text(encoding="utf-8").strip()
         for name in ("header", "footer")}

changed = 0
for page in SITE.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    new = text
    for name, body in PARTS.items():
        new = re.sub(rf"<!--#{name}-->.*?<!--/{name}-->",
                     f"<!--#{name}-->\n{body}\n<!--/{name}-->", new, flags=re.S)
    if new != text:
        page.write_text(new, encoding="utf-8")
        changed += 1
print(f"updated {changed} page(s)")
