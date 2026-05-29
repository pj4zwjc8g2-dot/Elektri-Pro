#!/usr/bin/env python3
# =====================================================================
#  build.py — Elektri Pro v3
#  Genereert: homepage, /diensten/, /faq/, /contact/, dienstpagina's,
#  dienst×stad-landingspagina's, sitemap.xml, robots.txt.
# =====================================================================
import os, shutil, html, datetime, json
from data import BUSINESS, SERVICES, CITIES, REVIEWS, MENU, FAQ, TRUST_POINTS

OUT = "site"
B = BUSINESS
D = B["domain"]
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()

def esc(s): return html.escape(s, quote=True)

# ========== gedeelde bouwstenen ==========
def head(title, desc, canonical, schema=""):
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_BE">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{D}/style.css">
{schema}
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-TGTKG654');</script>
<!-- End Google Tag Manager -->
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TGTKG654"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

def topbar(current_path=""):
    nav = ""
    for m in MENU:
        active = ' class="active"' if m["url"] == current_path else ""
        nav += f'<a href="{D}{m["url"]}"{active}>{esc(m["label"])}</a>'
    return f"""<header class="topbar"><div class="wrap">
<a class="brand" href="{D}/"><span class="spark">🔌</span> Elektri<span class="pro">Pro</span></a>
<nav class="mainnav">{nav}</nav>
<a class="call-btn" href="tel:{B['phone_link']}" data-call="header">
<span class="ring">📞</span><span class="txt">{esc(B['phone_display'])}</span></a>
<button class="burger" aria-label="Menu" onclick="document.querySelector('.mainnav').classList.toggle('open')">☰</button>
</div></header>"""

def mobile_call():
    return f"""<a class="mobile-call" href="tel:{B['phone_link']}" data-call="mobile-sticky">📞 Bel direct — {esc(B['phone_display'])}</a>"""

def footer():
    mail = f'<a href="mailto:{esc(B["email"])}">{esc(B["email"])}</a>' if B["email"] else ""
    vat = f'<p>{esc(B["vat"])}</p>' if B["vat"] else ""
    slinks = "".join(f'<a href="{D}/{k}/">{esc(s["label"])}</a>' for k, s in SERVICES.items())
    mlinks = "".join(f'<a href="{D}{m["url"]}">{esc(m["label"])}</a>' for m in MENU)
    return f"""<footer><div class="wrap">
<div class="col"><h4><span style="color:var(--accent)">🔌</span> {esc(B['name'])}</h4>
<p>{esc(B['tagline'])}.</p><p>Particulieren &amp; bedrijven.</p>{vat}</div>
<div class="col"><h4>Diensten</h4>{slinks}</div>
<div class="col"><h4>Navigatie</h4>{mlinks}</div>
<div class="col"><h4>Contact</h4><a href="tel:{B['phone_link']}">📞 {esc(B['phone_display'])}</a>{mail}
<p style="margin-top:8px">Werkgebied: Vlaams-Brabant, Brussel, Waals-Brabant</p></div>
</div><div class="copy">© {YEAR} {esc(B['name'])} — Alle rechten voorbehouden.</div></footer>"""

TRACK = """<script>
window.dataLayer=window.dataLayer||[];
document.querySelectorAll('a[href^="tel:"]').forEach(function(a){
 a.addEventListener('click',function(){window.dataLayer.push({event:'phone_call_click',call_location:a.getAttribute('data-call')||'unknown'});});});
</script>"""

def schema_localbusiness(area=None, page_url=None):
    areas = [c["name"] for c in CITIES] if not area else [area]
    served = ",".join(f'"{a}"' for a in areas)
    email = f'"email":"{B["email"]}",' if B["email"] else ""
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Electrician","name":"{B['name']}",
"telephone":"{B['phone_link']}",{email}"url":"{page_url or B['domain']}",
"areaServed":[{served}],"slogan":"{B['tagline']}"}}</script>"""

def schema_faq(items):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in items]}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def render(path, title, desc, canonical, schema, inner, current_path=""):
    full = head(title, desc, canonical, schema) + topbar(current_path) + inner + footer() + mobile_call() + TRACK + "\n</body></html>"
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)

# ========== herbruikbare secties ==========
def hero(h1, lead, badge="Beschikbaar voor noodinterventies"):
    return f"""<section class="hero"><div class="wrap">
<span class="tag"><span class="dot"></span> {esc(badge)}</span>
<h1>{h1}</h1><p class="lead">{esc(lead)}</p>
<div class="cta-row">
<a class="btn-primary" href="tel:{B['phone_link']}" data-call="hero">📞 Bel {esc(B['phone_display'])}</a>
<a class="btn-ghost" href="#info">Meer weten →</a></div>
<div class="regions"><span>📍 <b>Vlaams-Brabant</b></span><span>📍 <b>Brussel</b></span><span>📍 <b>Waals-Brabant</b></span></div>
</div></section>"""

def trust_strip():
    return """<section class="trust"><div class="wrap">
<div class="item"><b>24/7</b><span>Bereikbaar voor nood</span></div>
<div class="item"><b>Snel</b><span>Vlot ter plaatse</span></div>
<div class="item"><b>Erkend</b><span>Vakkundig &amp; verzekerd</span></div>
<div class="item"><b>Helder</b><span>Prijs vooraf besproken</span></div>
</div></section>"""

def trust_grid():
    cards = ""
    for t in TRUST_POINTS:
        cards += f"""<div class="tp-card"><div class="tp-ic">{t['icon']}</div>
<h3>{esc(t['title'])}</h3><p>{esc(t['text'])}</p></div>"""
    return f"""<section class="section trust-section"><div class="wrap">
<h2 class="reveal">Waarom Elektri Pro</h2>
<p class="sub reveal">Zes redenen waarom klanten ons opnieuw bellen.</p>
<div class="tp-grid reveal">{cards}</div></div></section>"""

def reviews_section():
    if not REVIEWS: return ""
    cards = ""
    for r in REVIEWS:
        sub = f" · {esc(r['city'])}" if r.get("city") else ""
        initial = esc(r["name"][:1].upper())
        n = int(r.get("stars", 5))
        stars = '<div class="stars" aria-label="' + str(n) + ' op 5 sterren">' + ("★" * n) + ("☆" * (5 - n)) + '</div>'
        cards += f"""<figure class="review">{stars}
<blockquote>{esc(r['text'])}</blockquote>
<figcaption><span class="avatar">{initial}</span><span>{esc(r['name'])}{sub}</span></figcaption>
</figure>"""
    return f"""<section class="section reviews-sec"><div class="wrap">
<h2 class="reveal">Wat klanten zeggen</h2>
<p class="sub reveal">Echte reacties van mensen die we hebben geholpen.</p>
<div class="reviewgrid reveal">{cards}</div></div></section>"""

def band(title="Een elektricien nodig?", subtitle="Bel ons gerust — ook voor een vrijblijvende inschatting."):
    return f"""<section class="band"><div class="wrap"><h2>{esc(title)}</h2>
<p>{esc(subtitle)}</p>
<a class="big-call" href="tel:{B['phone_link']}" data-call="band">📞 {esc(B['phone_display'])}</a></div></section>"""

# ========== pagina-bouwers ==========
def build_home():
    cards = ""
    for skey, s in SERVICES.items():
        cls = "card urgent" if skey == "noodelektricien" else "card"
        extra = f'<a class="mini" href="tel:{B["phone_link"]}" data-call="card-{skey}">📞 Bel nu</a>' if skey == "noodelektricien" else ""
        cards += f"""<a class="{cls}" href="{D}/{skey}/"><div class="ic">{s['icon']}</div>
<h3>{esc(s['label'])}</h3><p>{esc(s['intro'])}</p>{extra}</a>"""
    inner = hero(
        'Uw elektricien, <em>snel ter plaatse</em> wanneer het nodig is.',
        "Van een plotse stroompanne tot een complete zekeringkast — Elektri Pro staat klaar voor "
        "particulieren en bedrijven in Vlaams-Brabant, Brussel en Waals-Brabant."
    ) + trust_strip() + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">Onze diensten</h2>
<p class="sub reveal">Gespecialiseerd in waar het op aankomt.</p>
<div class="grid">{cards}</div></div></section>""" + trust_grid() + reviews_section() + band()
    render(f"{OUT}/index.html",
           f"{B['name']} — Elektricien & Noodinterventies | Vlaams-Brabant, Brussel, Waals-Brabant",
           f"{B['name']}: erkend elektricien voor noodinterventies en zekeringkasten in Vlaams-Brabant, "
           f"Brussel en Waals-Brabant. Snel ter plaatse. Bel {B['phone_display']}.",
           f"{D}/", schema_localbusiness(), inner, "/")

def build_diensten_overview():
    cards = ""
    for skey, s in SERVICES.items():
        pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"][:3])
        cards += f"""<div class="d-card"><div class="d-ic">{s['icon']}</div>
<h3>{esc(s['label'])}</h3><p>{esc(s['intro'])}</p>
<ul>{pts}</ul>
<a class="d-link" href="{D}/{skey}/">Meer over {esc(s['label']).lower()} →</a></div>"""
    inner = hero("Onze diensten",
                 "Elektri Pro biedt vakkundige oplossingen voor noodinterventies en zekeringkasten "
                 "in Vlaams-Brabant, Brussel en Waals-Brabant.") + f"""
<section class="section"><div class="wrap">
<div class="d-grid">{cards}</div></div></section>""" + trust_grid() + reviews_section() + band()
    render(f"{OUT}/diensten/index.html",
           f"Diensten | {B['name']}",
           f"Ontdek de diensten van {B['name']}: noodinterventies en zekeringkasten in "
           f"Vlaams-Brabant, Brussel en Waals-Brabant.",
           f"{D}/diensten/", schema_localbusiness(), inner, "/diensten/")

def build_faq():
    items = ""
    for i, fq in enumerate(FAQ):
        items += f"""<details class="faq-item"{' open' if i == 0 else ''}>
<summary>{esc(fq['q'])}</summary><p>{esc(fq['a'])}</p></details>"""
    inner = hero("Veelgestelde vragen",
                 "Antwoorden op de vragen die we het vaakst krijgen. Staat uw vraag er niet bij? "
                 "Bel gerust, we beantwoorden ze graag.",
                 badge="Veelgestelde vragen") + f"""
<section class="section"><div class="wrap">
<div class="faq-list reveal">{items}</div></div></section>""" + band("Nog een vraag?", "Bel ons en we helpen u meteen verder.")
    render(f"{OUT}/faq/index.html",
           f"FAQ — Veelgestelde vragen | {B['name']}",
           f"Veelgestelde vragen over noodinterventies, zekeringkasten, prijzen en werkgebied "
           f"van {B['name']}. Bel {B['phone_display']} voor uw specifieke situatie.",
           f"{D}/faq/",
           schema_localbusiness() + schema_faq(FAQ),
           inner, "/faq/")

def build_contact():
    email_block = f'<p><strong>E-mail:</strong> <a href="mailto:{esc(B["email"])}">{esc(B["email"])}</a></p>' if B["email"] else ""
    vat_block = f'<p><strong>BTW-nummer:</strong> {esc(B["vat"])}</p>' if B["vat"] else ""
    inner = hero("Contact",
                 "Bel ons rechtstreeks voor een afspraak, een dringende interventie of gewoon "
                 "om uw situatie even toe te lichten.",
                 badge="Direct bereikbaar") + f"""
<section class="section"><div class="wrap">
<div class="contact-grid">
  <div class="contact-card">
    <h2>Telefonisch</h2>
    <p>De snelste manier om ons te bereiken — zeker bij een noodgeval.</p>
    <a class="big-call" href="tel:{B['phone_link']}" data-call="contact-page">📞 {esc(B['phone_display'])}</a>
  </div>
  <div class="contact-card">
    <h2>Gegevens</h2>
    <p><strong>Bedrijf:</strong> {esc(B['name'])}</p>
    {email_block}{vat_block}
    <p><strong>Werkgebied:</strong> Vlaams-Brabant, Brussels Hoofdstedelijk Gewest, Waals-Brabant.</p>
  </div>
</div></div></section>""" + trust_grid() + band("Liever vandaag nog langskomen?")
    render(f"{OUT}/contact/index.html",
           f"Contact | {B['name']}",
           f"Neem contact op met {B['name']}: bel {B['phone_display']} voor noodinterventies "
           f"en elektriciteitswerken in Vlaams-Brabant, Brussel en Waals-Brabant.",
           f"{D}/contact/", schema_localbusiness(), inner, "/contact/")

def build_service(skey, s):
    pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    by_prov = {}
    for c in CITIES:
        by_prov.setdefault(c["province"], []).append(c)
    province_blocks = ""
    for prov, cs in by_prov.items():
        chips = "".join(f'<a class="citychip" href="{D}/{skey}/{c["slug"]}/">{esc(s["kw"])} {esc(c["name"])}</a>' for c in cs)
        province_blocks += f'<div class="prov-block"><h3>{esc(prov)}</h3><div class="citygrid">{chips}</div></div>'
    h1 = f"{esc(s['kw'])} in Vlaams-Brabant, Brussel &amp; Waals-Brabant"
    inner = hero(h1, s["intro"]) + trust_strip() + f"""
<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['label'])}</h2>
<div class="prose reveal">{body}</div>
<div class="checks reveal"><h3>Waarvoor u ons kunt bellen</h3><ul>{pts}</ul></div>
<h2 class="reveal" style="margin-top:54px">{esc(s['kw'])} per stad</h2>
<p class="sub reveal">Selecteer uw stad voor meer informatie over onze dienstverlening daar.</p>
{province_blocks}
</div></section>""" + trust_grid() + reviews_section() + band()
    render(f"{OUT}/{skey}/index.html",
           f"{s['kw']} | {B['name']} — Vlaams-Brabant, Brussel & Waals-Brabant",
           f"{s['intro']} Bel {B['phone_display']}.",
           f"{D}/{skey}/", schema_localbusiness(), inner)

def build_service_city(skey, s, c):
    pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    nearby_chips = "".join(f'<span class="nb-chip">{esc(n)}</span>' for n in c.get("nearby", []))
    nearby_block = ""
    if nearby_chips:
        nearby_block = f"""<div class="nearby reveal">
<h3>Ook actief in de omliggende gemeenten van {esc(c['name'])}</h3>
<p>We bedienen niet alleen {esc(c['name'])} zelf, maar ook deze gemeenten errond:</p>
<div class="nb-list">{nearby_chips}</div>
<p class="nb-note">Niet zeker of we bij u langskomen? <a href="tel:{B['phone_link']}" data-call="nearby">Bel {esc(B['phone_display'])}</a> en we kijken het meteen na.</p>
</div>"""
    h1 = f"{esc(s['kw'])} in {esc(c['name'])}"
    lead = f"{s['intro']} Actief in {c['name']} en omliggende gemeenten ({c['province']})."
    canonical = f"{D}/{skey}/{c['slug']}/"
    inner = hero(h1, lead) + trust_strip() + f"""
<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['kw'])} in {esc(c['name'])}</h2>
<div class="prose reveal"><p class="localnote">{esc(c['local'])}</p>{body}</div>
<div class="checks reveal"><h3>Waarvoor u ons kunt bellen in {esc(c['name'])}</h3><ul>{pts}</ul></div>
{nearby_block}
</div></section>""" + trust_grid() + reviews_section() + band(f"{s['kw']} nodig in {c['name']}?")
    render(f"{OUT}/{skey}/{c['slug']}/index.html",
           f"{s['kw']} {c['name']} | {B['name']}",
           f"{s['kw']} in {c['name']} en omliggende gemeenten ({c['province']})? {s['intro']} Bel {B['phone_display']}.",
           canonical, schema_localbusiness(c['name'], canonical), inner)

def build_sitemap():
    urls = [f"{D}/", f"{D}/diensten/", f"{D}/faq/", f"{D}/contact/"]
    for skey in SERVICES:
        urls.append(f"{D}/{skey}/")
        for c in CITIES:
            urls.append(f"{D}/{skey}/{c['slug']}/")
    items = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    with open(f"{OUT}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    with open(f"{OUT}/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {D}/sitemap.xml\n")
    host = D.replace("https://", "").replace("http://", "").strip("/")
    if "github.io" not in host:
        with open(f"{OUT}/CNAME", "w", encoding="utf-8") as f:
            f.write(host)

# ========== run ==========
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy("style.css", f"{OUT}/style.css")
build_home()
build_diensten_overview()
build_faq()
build_contact()
n = 4
for skey, s in SERVICES.items():
    build_service(skey, s); n += 1
    for c in CITIES:
        build_service_city(skey, s, c); n += 1
build_sitemap()
print(f"Klaar. {n} pagina's gegenereerd in ./{OUT}/")
print(f"  - 4 hoofdpagina's (home, diensten, faq, contact)")
print(f"  - {len(SERVICES)} dienstpagina's")
print(f"  - {len(SERVICES) * len(CITIES)} dienst×stad landingspagina's")
print(f"  - sitemap.xml, robots.txt")
