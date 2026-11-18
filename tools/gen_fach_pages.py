"""Write the Tomelo Fach product pages: docs/fach/ (English), docs/cs/fach/, docs/de/fach/.

The app speaks Czech, Slovak, German and English, so the page exists in the site's languages
that match (the site has no Slovak). Texts live in T below; change them here, not in the pages.
Run, then fill header, footer and menus:

    python tools/gen_fach_pages.py
    python tools/apply_partials.py
    python tools/build_sitemap.py
"""
import html
import json
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "docs"
BASE = "https://tomelo.app"

ICON = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="0.75" y="0.75" width="62.5" height="62.5" rx="19.5" fill="#FFF6EC" stroke="#F3D3AE" stroke-width="1.5"/>'
        '<circle cx="20" cy="20" r="5.2" fill="#C2410C"/><circle cx="32" cy="20" r="5.2" fill="#C2410C"/><circle cx="44" cy="20" r="5.2" fill="#C2410C"/>'
        '<circle cx="20" cy="32" r="5.2" fill="#F3D3AE"/><circle cx="32" cy="32" r="5.2" fill="#C2410C"/><circle cx="44" cy="32" r="5.2" fill="#F3D3AE"/>'
        '<circle cx="20" cy="44" r="5.2" fill="#F3D3AE"/><circle cx="32" cy="44" r="5.2" fill="#C2410C"/><circle cx="44" cy="44" r="5.2" fill="#2457C5"/></svg>')
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>'
ICONS = [  # one per feature card, same order as T[...]["cards"]
    '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h4"/>',
    '<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M3 10h18M7 15h3"/>',
    '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.5 2.5-2.5-.5-.5-2.5z"/>',
    '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3 2.8-5 5.5-5s4.9 2 5.5 5"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.2c2.3.3 4 2 4.5 4.8"/>',
    '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    '<path d="M4 4h10l6 6v10H4z"/><path d="M14 4v6h6M8 14l3 3 5-5"/>',
]
TINTS = ["", "mint", "peach", "", "mint", "peach", "", "mint"]

T = {
    "en": {
        "title": "Tomelo Fach: quotes, jobs and invoices for tradespeople",
        "desc": "An Android app for tradespeople, from the first call to the paid invoice: quotes, jobs, invoices with the right VAT, receipts and tools for your trade. Works without signal. Your data stays in your own Google Drive.",
        "locale": "en_GB",
        "sub": "From the first call to the paid invoice.",
        "lead": "One app for the whole job: the enquiry, the quote, the work and the payment. Made for the van and the building site, so it works without signal. Your data stays on your phone and in your own Google Drive.",
        "soon": "Coming soon to Google Play",
        "see": "See what it does",
        "trust": ["Works without signal", "Data in your own Google Drive", "No account with us", "Czech, Slovak, German, English"],
        "flow_label": "One job in four steps",
        "flow": [("Enquiry", "Customer, place, date and what they need."),
                 ("Quote", "From your price list. The customer agrees by message."),
                 ("Job", "Plan it, do it, add photos and extra work."),
                 ("Payment", "Invoice or receipt, paid on the spot or later.")],
        "feat_title": "Everything a small firm needs",
        "feat_lead": "For one person or a small team. Pick your trade, and the app sets up the price list, the tools and the kinds of jobs.",
        "cards": [
            ("Quotes that become jobs", "Build a quote from your price list and send it as a PDF. When the customer agrees, it becomes the job with the same items."),
            ("Invoices with the right VAT", "Invoices, deposits and credit notes with the rules of your country, including the reverse charge in construction. Numbering and due dates are set once."),
            ("Paid on the spot", "A quick receipt for small jobs paid in cash or by card, where your country allows it. Reminders for invoices that are overdue."),
            ("Talk instead of typing", "Dictate what you did while it is fresh. The phone turns speech into text without internet, and you check it before anything is saved."),
            ("Tools for your trade", "Calculators for materials and cables, a level, a ruler and a light meter. Handover and test reports the customer signs on the screen."),
            ("A team that sees its part", "Owner, office and technician. A technician sees the jobs assigned to them and the prices, never your invoices and payments."),
            ("Messages to the customer", "Ready texts for WhatsApp, SMS or e-mail: on my way, quote ready, invoice sent. You send them yourself, from your phone."),
            ("Export for your accountant", "Invoices and payments for a month, a quarter or a year in one ZIP file: tables for Excel and every PDF."),
        ],
        "band_title": "Your data stays yours.",
        "band": "Tomelo Fach has no server, and we never see your jobs, customers or invoices. Everything is on your phone. If you work with a team, the firm's data is kept in your own Google Drive, in a folder the app creates, and shared only with the people you invite. The app can open only the files it made itself.",
        "band_link": "Read the privacy policy",
        "lim_title": "What Tomelo Fach doesn't do",
        "lim_lead": "Better to hear it from us before you install.",
        "limits": [
            ("Android only.", "There is no iPhone version and no computer version yet."),
            ("Not accounting software.", "It issues invoices and receipts and exports them for your accountant. Bookkeeping and tax returns stay with your accountant."),
            ("Not tax advice.", "The VAT rules follow the law of each country. If you are unsure about a case, ask your tax adviser."),
            ("Six countries.", "Czechia, Slovakia, Germany, Austria, the United Kingdom and Ireland."),
            ("A team needs Google accounts.", "Everyone signs in with their own Google account. On your own you can work without one."),
        ],
        "faq_title": "Questions",
        "faq": [
            ("offline", "Does it work without signal?", "Yes. Everything works offline. Changes reach the others the next time the phone is online."),
            ("data", "Where is my data?", "On your phone. With a team, also in a folder in the owner's Google Drive. We have no server and never receive your data."),
            ("lost-phone", "What if I lose my phone?", "If your Google Drive is connected, install the app on the new phone and choose that you are the owner and already have the business on another device. Working alone without Google Drive, make a backup in the settings now and then and keep the file safe."),
            ("team", "How do I add my team?", "In Settings, open People, add a person with their Google e-mail and send the invite. They install the app, choose “Join an existing business” and paste the link from the message."),
            ("price", "How much does it cost?", "The first 30 days are free, without a card. After that it is a subscription through Google Play, monthly or yearly, and Google Play shows the price in your currency. Without a subscription you can still read your data, issued invoices stay valid, and backup and export keep working."),
            ("when", "When can I get it?", "Tomelo Fach is not on Google Play yet. It will be there soon."),
            ("help", "How do I get help?", 'Write to <a href="mailto:support@tomelo.app">support@tomelo.app</a>. A person reads every message.'),
        ],
        "end_title": "One job, from the first call to the paid invoice.",
        "end": "Tomelo Fach comes to Google Play soon. The first 30 days are free, no card needed.",
    },
    "cs": {
        "title": "Tomelo Fach: nabídky, zakázky a faktury pro řemeslníky",
        "desc": "Aplikace pro řemeslníky na Android, od první poptávky po zaplacenou fakturu: nabídky, zakázky, faktury se správným DPH, účtenky a nástroje pro vaše řemeslo. Funguje i bez signálu. Data zůstávají na vašem Google Disku.",
        "locale": "cs_CZ",
        "sub": "Od první poptávky po zaplacenou fakturu.",
        "lead": "Jedna aplikace na celou zakázku: poptávka, nabídka, práce i platba. Dělaná do auta a na stavbu, takže funguje i bez signálu. Vaše data zůstávají v telefonu a na vašem vlastním Google Disku.",
        "soon": "Brzy na Google Play",
        "see": "Co umí",
        "trust": ["Funguje i bez signálu", "Data na vašem Google Disku", "Žádný účet u nás", "Česky, slovensky, německy, anglicky"],
        "flow_label": "Jedna zakázka ve čtyřech krocích",
        "flow": [("Poptávka", "Zákazník, místo, termín a co potřebuje."),
                 ("Nabídka", "Z vašeho ceníku. Zákazník souhlasí zprávou."),
                 ("Zakázka", "Naplánovat, udělat, přidat fotky a vícepráce."),
                 ("Platba", "Faktura nebo účtenka, zaplaceno hned nebo později.")],
        "feat_title": "Vše, co malá firma potřebuje",
        "feat_lead": "Pro jednoho člověka i malou partu. Vyberete řemeslo a aplikace podle něj nachystá ceník, nástroje a druhy zakázek.",
        "cards": [
            ("Nabídka, ze které je zakázka", "Nabídku složíte z ceníku a pošlete jako PDF. Když zákazník souhlasí, stane se z ní zakázka se stejnými položkami."),
            ("Faktury se správným DPH", "Faktury, zálohy a opravné doklady podle pravidel vaší země, včetně přenesené daňové povinnosti ve stavebnictví. Číslování a splatnost nastavíte jednou."),
            ("Zaplaceno na místě", "Rychlá účtenka u drobných zakázek placených hotově nebo kartou, kde to vaše země dovoluje. Upomínky u faktur po splatnosti."),
            ("Mluvit místo psaní", "Nadiktujte, co jste udělali, dokud to máte v hlavě. Telefon převede řeč na text bez internetu a vy to zkontrolujete, než se cokoli uloží."),
            ("Nástroje pro vaše řemeslo", "Výpočty materiálu a kabelů, vodováha, pravítko a luxmetr. Předávací protokol a protokol o zkoušce, které zákazník podepíše na displeji."),
            ("Parta vidí svou část", "Šéf, kancelář a technik. Technik vidí zakázky přidělené jemu a ceny, nikdy vaše faktury a platby."),
            ("Zprávy zákazníkovi", "Hotové texty do WhatsAppu, SMS nebo e-mailu: jsem na cestě, nabídka je hotová, faktura odeslaná. Posíláte je sami ze svého telefonu."),
            ("Export pro účetní", "Faktury a platby za měsíc, čtvrtletí nebo rok v jednom souboru ZIP: tabulky pro Excel a všechna PDF."),
        ],
        "band_title": "Vaše data zůstávají vaše.",
        "band": "Tomelo Fach nemá žádný server a my vaše zakázky, zákazníky ani faktury nikdy nevidíme. Všechno je ve vašem telefonu. Když pracujete s partou, data firmy jsou na vašem vlastním Google Disku, ve složce, kterou aplikace založí, a sdílí se jen s lidmi, které pozvete. Aplikace otevře jen soubory, které sama vytvořila.",
        "band_link": "Přečíst zásady ochrany soukromí (anglicky)",
        "lim_title": "Co Tomelo Fach neumí",
        "lim_lead": "Ať to víte od nás dřív, než si ji nainstalujete.",
        "limits": [
            ("Jen Android.", "Verze pro iPhone ani pro počítač zatím není."),
            ("Není to účetní program.", "Vystavuje faktury a účtenky a exportuje je pro účetní. Účetnictví a daňová přiznání zůstávají u vaší účetní."),
            ("Není to daňové poradenství.", "Pravidla DPH odpovídají zákonům jednotlivých zemí. Když si u nějakého případu nejste jistí, zeptejte se daňového poradce."),
            ("Šest zemí.", "Česko, Slovensko, Německo, Rakousko, Velká Británie a Irsko."),
            ("Parta potřebuje účty Google.", "Každý se přihlásí svým účtem Google. Když pracujete sami, účet nepotřebujete."),
        ],
        "faq_title": "Otázky",
        "faq": [
            ("offline", "Funguje bez signálu?", "Ano. Všechno jde i bez internetu. Změny se ostatním pošlou, jakmile je telefon zase online."),
            ("data", "Kde jsou moje data?", "Ve vašem telefonu. S partou navíc ve složce na Google Disku šéfa. Nemáme žádný server a vaše data nikdy nedostáváme."),
            ("lost-phone", "Co když ztratím telefon?", "Když máte připojený Google Disk, nainstalujte aplikaci do nového telefonu a zvolte, že jste majitel a firmu už máte v jiném zařízení. Když pracujete sami bez Google Disku, dělejte občas v nastavení zálohu a soubor si dobře uložte."),
            ("team", "Jak přidám partu?", "V Nastavení otevřete Lidé, přidejte člověka s jeho e-mailem Google a pošlete pozvánku. On si nainstaluje aplikaci, zvolí „Připojit se k firmě, která už existuje“ a vloží odkaz ze zprávy."),
            ("price", "Kolik to stojí?", "Prvních 30 dní je zdarma, bez karty. Potom je to předplatné přes Google Play, měsíční nebo roční, a cenu ve vaší měně ukáže Google Play. Bez předplatného svá data dál přečtete, vystavené faktury platí a záloha i export fungují."),
            ("when", "Kdy ji dostanu?", "Tomelo Fach na Google Play ještě není. Bude tam brzy."),
            ("help", "Kde najdu pomoc?", 'Napište na <a href="mailto:support@tomelo.app">support@tomelo.app</a>. Každou zprávu čte člověk.'),
        ],
        "end_title": "Jedna zakázka, od první poptávky po zaplacenou fakturu.",
        "end": "Tomelo Fach bude brzy na Google Play. Prvních 30 dní je zdarma, bez karty.",
    },
    "de": {
        "title": "Tomelo Fach: Angebote, Aufträge und Rechnungen für Handwerker",
        "desc": "Eine Android-App für Handwerker, von der ersten Anfrage bis zur bezahlten Rechnung: Angebote, Aufträge, Rechnungen mit der richtigen Umsatzsteuer, Belege und Werkzeuge für Ihr Gewerk. Funktioniert ohne Empfang. Ihre Daten bleiben in Ihrem eigenen Google Drive.",
        "locale": "de_DE",
        "sub": "Von der ersten Anfrage bis zur bezahlten Rechnung.",
        "lead": "Eine App für den ganzen Auftrag: Anfrage, Angebot, Arbeit und Zahlung. Gemacht für den Transporter und die Baustelle, deshalb funktioniert sie auch ohne Empfang. Ihre Daten bleiben auf Ihrem Handy und in Ihrem eigenen Google Drive.",
        "soon": "Bald bei Google Play",
        "see": "Was sie kann",
        "trust": ["Funktioniert ohne Empfang", "Daten in Ihrem Google Drive", "Kein Konto bei uns", "Deutsch, Englisch, Tschechisch, Slowakisch"],
        "flow_label": "Ein Auftrag in vier Schritten",
        "flow": [("Anfrage", "Kunde, Ort, Termin und was gebraucht wird."),
                 ("Angebot", "Aus Ihrer Preisliste. Der Kunde stimmt per Nachricht zu."),
                 ("Auftrag", "Planen, erledigen, Fotos und Zusatzarbeiten erfassen."),
                 ("Zahlung", "Rechnung oder Beleg, sofort bezahlt oder später.")],
        "feat_title": "Alles, was ein kleiner Betrieb braucht",
        "feat_lead": "Für eine Person oder ein kleines Team. Sie wählen Ihr Gewerk, und die App richtet danach Preisliste, Werkzeuge und Auftragsarten ein.",
        "cards": [
            ("Aus dem Angebot wird der Auftrag", "Stellen Sie das Angebot aus Ihrer Preisliste zusammen und senden Sie es als PDF. Stimmt der Kunde zu, wird daraus der Auftrag mit denselben Positionen."),
            ("Rechnungen mit der richtigen Steuer", "Rechnungen, Anzahlungen und Korrekturen nach den Regeln Ihres Landes, auch mit Steuerschuldnerschaft des Leistungsempfängers am Bau. Nummern und Zahlungsziele stellen Sie einmal ein."),
            ("Bezahlt vor Ort", "Ein schneller Beleg für kleine Aufträge, bar oder mit Karte bezahlt, wo Ihr Land das erlaubt. Mahnungen für überfällige Rechnungen."),
            ("Sprechen statt tippen", "Diktieren Sie, was Sie gemacht haben, solange es frisch ist. Das Handy macht ohne Internet Text daraus, und Sie prüfen ihn, bevor etwas gespeichert wird."),
            ("Werkzeuge für Ihr Gewerk", "Rechner für Material und Kabel, Wasserwaage, Lineal und Luxmeter. Übergabe- und Prüfprotokolle, die der Kunde auf dem Display unterschreibt."),
            ("Ein Team sieht seinen Teil", "Inhaber, Büro und Techniker. Ein Techniker sieht die ihm zugewiesenen Aufträge und die Preise, nie Ihre Rechnungen und Zahlungen."),
            ("Nachrichten an Kunden", "Fertige Texte für WhatsApp, SMS oder E-Mail: bin unterwegs, Angebot fertig, Rechnung verschickt. Sie senden sie selbst von Ihrem Handy."),
            ("Export für die Steuerberatung", "Rechnungen und Zahlungen für einen Monat, ein Quartal oder ein Jahr in einer ZIP-Datei: Tabellen für Excel und alle PDFs."),
        ],
        "band_title": "Ihre Daten bleiben Ihre.",
        "band": "Tomelo Fach hat keinen Server, und wir sehen Ihre Aufträge, Kunden und Rechnungen nie. Alles liegt auf Ihrem Handy. Arbeiten Sie im Team, liegen die Daten der Firma in Ihrem eigenen Google Drive, in einem Ordner, den die App anlegt, geteilt nur mit den Personen, die Sie einladen. Die App kann nur Dateien öffnen, die sie selbst erstellt hat.",
        "band_link": "Datenschutzerklärung lesen (Englisch)",
        "lim_title": "Was Tomelo Fach nicht kann",
        "lim_lead": "Besser, Sie hören es von uns, bevor Sie installieren.",
        "limits": [
            ("Nur Android.", "Es gibt noch keine Version für das iPhone oder den Computer."),
            ("Keine Buchhaltung.", "Die App stellt Rechnungen und Belege aus und exportiert sie für Ihre Steuerberatung. Buchhaltung und Steuererklärung bleiben dort."),
            ("Keine Steuerberatung.", "Die Steuerregeln folgen dem Recht des jeweiligen Landes. Sind Sie bei einem Fall unsicher, fragen Sie Ihre Steuerberatung."),
            ("Sechs Länder.", "Tschechien, Slowakei, Deutschland, Österreich, das Vereinigte Königreich und Irland."),
            ("Ein Team braucht Google-Konten.", "Jede Person meldet sich mit dem eigenen Google-Konto an. Allein geht es auch ohne."),
        ],
        "faq_title": "Fragen",
        "faq": [
            ("offline", "Funktioniert es ohne Empfang?", "Ja. Alles geht auch offline. Änderungen erreichen die anderen, sobald das Handy wieder online ist."),
            ("data", "Wo sind meine Daten?", "Auf Ihrem Handy. Im Team zusätzlich in einem Ordner im Google Drive des Inhabers. Wir haben keinen Server und erhalten Ihre Daten nie."),
            ("lost-phone", "Was, wenn ich mein Handy verliere?", "Ist Ihr Google Drive verbunden, installieren Sie die App auf dem neuen Handy und wählen, dass Sie der Inhaber sind und die Firma schon auf einem anderen Gerät haben. Arbeiten Sie allein ohne Google Drive, erstellen Sie ab und zu in den Einstellungen eine Sicherung und bewahren die Datei gut auf."),
            ("team", "Wie füge ich mein Team hinzu?", "Öffnen Sie in den Einstellungen Personen, legen Sie eine Person mit ihrer Google-E-Mail an und senden Sie die Einladung. Sie installiert die App, wählt „Einer bestehenden Firma beitreten“ und fügt den Link aus der Nachricht ein."),
            ("price", "Was kostet es?", "Die ersten 30 Tage sind kostenlos, ohne Karte. Danach ist es ein Abo über Google Play, monatlich oder jährlich, und Google Play zeigt den Preis in Ihrer Währung. Ohne Abo können Sie Ihre Daten weiter lesen, ausgestellte Rechnungen bleiben gültig, Sicherung und Export funktionieren."),
            ("when", "Wann gibt es die App?", "Tomelo Fach ist noch nicht bei Google Play. Bald ist sie dort."),
            ("help", "Wo bekomme ich Hilfe?", 'Schreiben Sie an <a href="mailto:support@tomelo.app">support@tomelo.app</a>. Jede Nachricht liest ein Mensch.'),
        ],
        "end_title": "Ein Auftrag, von der ersten Anfrage bis zur bezahlten Rechnung.",
        "end": "Tomelo Fach kommt bald zu Google Play. Die ersten 30 Tage sind kostenlos, ohne Karte.",
    },
}
LANGS = {"en": "", "cs": "/cs", "de": "/de"}


def page(lang):
    t = T[lang]
    p = LANGS[lang]
    url = f"{BASE}{p}/fach/"
    e = html.escape
    app_ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Tomelo Fach", "operatingSystem": "Android",
              "applicationCategory": "BusinessApplication", "description": t["desc"], "url": url,
              "inLanguage": ["cs", "sk", "de", "en"], "publisher": {"@id": "https://tomelo.app/#org"}}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a.replace('<a href="mailto:support@tomelo.app">', "").replace("</a>", ""))}}
        for _, q, a in t["faq"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Tomelo Apps", "item": f"{BASE}{p}/"},
        {"@type": "ListItem", "position": 2, "name": "Tomelo Fach", "item": url}]}
    ld = lambda o: '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False) + "\n</script>"
    trust = "\n".join(f"          <li>{CHECK}{e(x)}</li>" for x in t["trust"])
    flow = "\n".join(f"          <li><strong>{e(a)}</strong><span>{e(b)}</span></li>" for a, b in t["flow"])
    cards = "\n".join(
        f'        <div class="card">\n          <div class="icon{(" " + TINTS[i]) if TINTS[i] else ""}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[i]}</svg></div>\n'
        f"          <h3>{e(h)}</h3>\n          <p>{e(b)}</p>\n        </div>" for i, (h, b) in enumerate(t["cards"]))
    limits = "\n".join(f"        <li><strong>{e(a)}</strong> {e(b)}</li>" for a, b in t["limits"])
    faq = "\n".join(f'        <details id="{i}"><summary>{e(q)}</summary><p>{a if "<a " in a else e(a)}</p></details>' for i, q, a in t["faq"])
    soon = f'<span class="pill-soon">{CLOCK}{e(t["soon"])}</span>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tomelo Apps">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://tomelo.app/assets/og-tomelo.png">
<meta name="twitter:card" content="summary_large_image">
{ld(app_ld)}
{ld(faq_ld)}
{ld(crumbs)}
</head>
<body>
<!--#header-->
<!--/header-->
<!--#product-fach-->
<!--/product-fach-->

<main id="main">
  <div class="hero">
    <div class="wrap">
      <div class="hero-panel">
      <div class="hero-copy">
        <h1 class="wg-title">{ICON}<span>Tomelo Fach</span></h1>
        <p class="wg-sub">{e(t["sub"])}</p>
        <p class="lead">{e(t["lead"])}</p>
        <div class="actions">
          {soon}
          <a class="btn btn-ghost" href="#features">{e(t["see"])}</a>
        </div>
        <ul class="trust">
{trust}
        </ul>
      </div>
      <ol class="fach-flow" aria-label="{e(t["flow_label"])}">
{flow}
      </ol>
      </div>
    </div>
  </div>

  <section id="features">
    <div class="wrap">
      <h2 class="section-title">{e(t["feat_title"])}</h2>
      <p class="section-lead">{e(t["feat_lead"])}</p>
      <div class="cards">
{cards}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="band">
        <div class="badge">{SHIELD}</div>
        <div>
        <h2>{e(t["band_title"])}</h2>
        <p>{e(t["band"])}</p>
        <p><a class="band-link" href="/fach/privacy/" hreflang="en">{e(t["band_link"])}</a></p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap narrow">
      <h2 class="section-title">{e(t["lim_title"])}</h2>
      <p class="section-lead">{e(t["lim_lead"])}</p>
      <ul class="limits">
{limits}
      </ul>
    </div>
  </section>

  <section>
    <div class="wrap narrow">
      <h2 class="section-title">{e(t["faq_title"])}</h2>
      <div class="faq">
{faq}
      </div>
      <div class="cta-end">
        <h2>{e(t["end_title"])}</h2>
        <p>{e(t["end"])}</p>
        <div class="actions">
          {soon}
        </div>
      </div>
    </div>
  </section>
</main>
<script>(function(){{function o(){{var d=location.hash&&document.getElementById(location.hash.slice(1));if(d&&d.tagName==="DETAILS")d.open=true}}o();window.addEventListener("hashchange",o)}})();</script>

<!--#footer-->
<!--/footer-->
</body>
</html>
"""


for lang, prefix in LANGS.items():
    out = SITE / prefix.strip("/") / "fach" / "index.html" if prefix else SITE / "fach" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang), encoding="utf-8", newline="\n")
    print("wrote", out.relative_to(SITE).as_posix())
