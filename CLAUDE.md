# tomelo.app: web Tomelo Apps

Statický web (HTML, jeden CSS, vlastní písmo, obrázky) na GitHub Pages.
Bez build kroku, bez frameworku. Publikuje se složka `docs/` z větve `main`.
Strategie, značka a rozhodnutí jsou ve vedlejším repozitáři
`tomelo-apps/workspace` (začni jeho `CLAUDE.md`); tady je jen web.

## Klíčová pravidla
1. **Push do `main` = web je okamžitě veřejný.** Pracuj ve větvi. Do `main`
   slučuj až po souhlasu partnera nebo Tomáše; předtím jim ukaž náhled nebo
   screenshoty (desktop i mobil 360 px).
2. **Před každým sloučením spusť kontrolu** (dole). Musí skončit `OK`.
3. **Hlavička, patička, menu PillBell a přepínač jazyků se needitují ve
   stránkách**, ale v `partials/` a pak `python3 tools/apply_partials.py`.
4. **Jazyky:** angličtina je zdroj (kořen `docs/`), ostatních 9 jazyků je
   v `docs/<jazyk>/` (cs de fr es it pl nl pt uk). Když měníš text v angličtině,
   uprav stejné místo ve všech jazycích. Návody jsou v
   `docs/pillbell/guide/<jazyk>.html`. Právní stránky (`/legal/`, `/privacy/`,
   `/pillbell/privacy/`) jsou jen anglicky.
5. **Po přidání nebo smazání stránky:** `python3 tools/apply_partials.py`
   a `python3 tools/build_sitemap.py`.
6. **Psaní:** jednoduše, krátké věty, bez dlouhých pomlček (—), bez vykřičníků,
   žádné zdravotní sliby (PillBell je „připomínka a osobní deník, ne zdravotnický
   prostředek“), nikdy „senioři“, nevymýšlet recenze ani čísla. Podrobně skill
   `tomelo-voice` ve workspace (`.claude/skills/tomelo-voice/`).
7. **Čitelnost:** text nikdy pod 16 px, kontrast textu aspoň 4,5 : 1 (cíl 7 : 1),
   dotykové cíle aspoň 44 px. Barvy a mezery jen přes proměnné v
   `docs/assets/site.css` (`--brand`, `--ink`, …); funguje i tmavý režim.
8. **Tlačítka Google Play** jsou oficiální grafika v `docs/assets/badges/`
   (jedna na jazyk). Nikdy je nepřekreslovat, nebarvit ani neořezávat.
9. **Fotky lidí** v `docs/assets/photos/` jsou vygenerované AI se skutečnými
   snímky aplikace. Alt text vždy začíná „Illustrative photo:“ (v jazyce
   stránky). Nikdy je nevydávat za zákazníky. Skládá je skript
   `podklady/znacka/fotky/sestav_fotky.py` ve workspace.
10. **Bez cookies a bez sledování.** Jediný skript třetí strany je Cloudflare
    Web Analytics (bez cookies) v patičce; je popsaný v `/privacy/`. Nic dalšího
    nepřidávat bez změny `/privacy/` a rozhodnutí v `workspace/rozhodnuti.md`.
11. **Tajné údaje** (hesla, klíče) nikdy do repozitáře.

## Jak na běžné úkoly
| Úkol | Kde |
|---|---|
| Změna textu na stránce | `docs/…/index.html` + stejné místo v `docs/<jazyk>/…` |
| Menu, patička, přepínač jazyků | `partials/*.html`, texty v `tools/apply_partials.py` (slovník `T`) |
| Vzhled | `docs/assets/site.css` |
| Nová aplikace | viz `README.md`, oddíl *Adding an app* |
| Nová fotka | workspace `podklady/znacka/fotky/` → výstup do `docs/assets/photos/` |

## Kontrola před sloučením
```
python3 -m http.server 8765 -d docs &
node tools/check_site.cjs
```
Potřebuje Playwright a axe-core (`npm i -g playwright axe-core`,
`NODE_PATH=$(npm root -g)`). Hlídá rozbité odkazy, chyby přístupnosti
(WCAG 2.2 AA), vodorovné posouvání na 320 px, písmo pod 16 px a kontrast.
