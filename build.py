#!/usr/bin/env python3
# =====================================================================
#  build.py — genereert de volledige Elektri Pro site uit data.py
#  Gebruik:  python3 build.py
#  Output:   map  ./site/  met alle HTML, sitemap.xml en robots.txt
# =====================================================================
import os, shutil, html, datetime
from data import BUSINESS, SERVICES, CITIES, REVIEWS

OUT = "site"
B = BUSINESS
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()

def esc(s): return html.escape(s, quote=True)

# ---------- gedeelde HTML-onderdelen ----------
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
<link rel="stylesheet" href="{B['domain']}/style.css">
{schema}
</head>
<body>"""

def callbar():
    return f"""<header class="callbar"><div class="wrap">
<a class="brand" href="{B['domain']}/"><span class="spark">⚡</span> Elektri<span class="pro">Pro</span></a>
<a class="call-btn" href="tel:{B['phone_link']}" data-call="header">
<span class="ring">📞</span><span class="txt">Bel direct: {esc(B['phone_display'])}</span></a>
</div></header>"""

def mobile_call():
    return f"""<a class="mobile-call" href="tel:{B['phone_link']}" data-call="mobile-sticky">📞 Bel direct — {esc(B['phone_display'])}</a>"""

def footer():
    mail = f'<a href="mailto:{esc(B["email"])}">{esc(B["email"])}</a>' if B["email"] else ""
    vat = f'<p>{esc(B["vat"])}</p>' if B["vat"] else ""
    # links naar alle dienst+stad-pagina's voor interne linking (goed voor SEO)
    links = ""
    for skey, s in SERVICES.items():
        links += f'<a href="{B["domain"]}/{skey}/">{esc(s["label"])}</a>'
    return f"""<footer><div class="wrap">
<div class="col"><h4><span style="color:var(--accent)">⚡</span> {esc(B['name'])}</h4>
<p>{esc(B['tagline'])}.</p><p>Particulieren &amp; bedrijven.</p>{vat}</div>
<div class="col"><h4>Diensten</h4>{links}</div>
<div class="col"><h4>Werkgebied</h4><p>Vlaams-Brabant</p><p>Brussel</p><p>Waals-Brabant</p></div>
<div class="col"><h4>Contact</h4><a href="tel:{B['phone_link']}">📞 {esc(B['phone_display'])}</a>{mail}</div>
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

# ---------- pagina-bouwers ----------
def render(path, title, desc, canonical, schema, inner):
    full = head(title, desc, canonical, schema) + callbar() + inner + footer() + mobile_call() + TRACK + "\n</body></html>"
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)

def hero(h1, lead, badge="Beschikbaar voor noodinterventies"):
    return f"""<section class="hero"><div class="wrap">
<span class="tag"><span class="dot"></span> {esc(badge)}</span>
<h1>{h1}</h1><p class="lead">{esc(lead)}</p>
<div class="cta-row">
<a class="btn-primary" href="tel:{B['phone_link']}" data-call="hero">📞 Bel {esc(B['phone_display'])}</a>
<a class="btn-ghost" href="#info">Meer weten →</a></div>
<div class="regions"><span>📍 <b>Vlaams-Brabant</b></span><span>📍 <b>Brussel</b></span><span>📍 <b>Waals-Brabant</b></span></div>
</div></section>"""

def trust():
    return """<section class="trust"><div class="wrap">
<div class="item"><b>24/7</b><span>Bereikbaar voor nood</span></div>
<div class="item"><b>Snel</b><span>Vlot ter plaatse</span></div>
<div class="item"><b>Erkend</b><span>Vakkundig &amp; verzekerd</span></div>
<div class="item"><b>Helder</b><span>Prijs vooraf besproken</span></div>
</div></section>"""

def reviews_section():
    if not REVIEWS:
        return ""
    cards = ""
    for r in REVIEWS:
        sub = f" · {esc(r['city'])}" if r.get("city") else ""
        initial = esc(r["name"][:1].upper())
        n = int(r.get("stars", 5))
        stars = '<div class="stars" aria-label="' + str(n) + ' op 5 sterren">' + ("★"*n) + ("☆"*(5-n)) + '</div>'
        cards += f"""<figure class="review">
{stars}
<blockquote>{esc(r['text'])}</blockquote>
<figcaption><span class="avatar">{initial}</span><span>{esc(r['name'])}{sub}</span></figcaption>
</figure>"""
    return f"""<section class="section reviews-sec"><div class="wrap">
<h2 class="reveal">Wat klanten zeggen</h2>
<p class="sub reveal">Echte reacties van mensen die we hebben geholpen.</p>
<div class="reviewgrid reveal">{cards}</div></div></section>"""

def band(title="Een elektricien nodig?"):
    return f"""<section class="band"><div class="wrap"><h2>{esc(title)}</h2>
<p>Bel ons gerust — ook voor een vrijblijvende inschatting.</p>
<a class="big-call" href="tel:{B['phone_link']}" data-call="band">📞 {esc(B['phone_display'])}</a></div></section>"""

# ---------- 1. homepage ----------
def build_home():
    cards = ""
    for skey, s in SERVICES.items():
        cls = "card urgent" if skey == "noodelektricien" else "card"
        extra = f'<a class="mini" href="tel:{B["phone_link"]}" data-call="card-{skey}">📞 Bel nu</a>' if skey=="noodelektricien" else ""
        cards += f"""<a class="{cls}" href="{B['domain']}/{skey}/"><div class="ic">{s['icon']}</div>
<h3>{esc(s['label'])}</h3><p>{esc(s['intro'])}</p>{extra}</a>"""
    inner = hero(
        'Uw elektricien, <em>snel ter plaatse</em> wanneer het nodig is.',
        "Van een plotse stroompanne tot een complete zekeringkast — Elektri Pro staat klaar voor "
        "particulieren en bedrijven in Vlaams-Brabant, Brussel en Waals-Brabant. Erkend werk, duidelijke prijzen."
    ) + trust() + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">Onze diensten</h2>
<p class="sub reveal">Gespecialiseerd in waar het op aankomt, met diepgaande kennis per domein.</p>
<div class="grid">{cards}</div></div></section>""" + reviews_section() + band()
    render(f"{OUT}/index.html",
        f"{B['name']} — Elektricien & Noodinterventies | Vlaams-Brabant, Brussel, Waals-Brabant",
        f"{B['name']}: erkend elektricien voor noodinterventies en zekeringkasten in Vlaams-Brabant, "
        f"Brussel en Waals-Brabant. Snel ter plaatse. Bel {B['phone_display']}.",
        f"{B['domain']}/", schema_localbusiness(), inner)

# ---------- 2. dienst-overzichtspagina ----------
def build_service(skey, s):
    pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    citylinks = "".join(
        f'<a class="citychip" href="{B["domain"]}/{skey}/{c["slug"]}/">{esc(s["kw"])} {esc(c["name"])}</a>'
        for c in CITIES)
    h1 = f"{esc(s['kw'])} in Vlaams-Brabant, Brussel &amp; Waals-Brabant"
    inner = hero(h1, s["intro"]) + trust() + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['label'])}</h2><div class="prose reveal">{body}</div>
<div class="checks reveal"><h3>Waarvoor u ons kunt bellen</h3><ul>{pts}</ul></div>
<h2 class="reveal" style="margin-top:54px">{esc(s['kw'])} per stad</h2>
<p class="sub reveal">Selecteer uw stad voor meer informatie over onze dienstverlening daar.</p>
<div class="citygrid reveal">{citylinks}</div></div></section>""" + band()
    render(f"{OUT}/{skey}/index.html",
        f"{s['kw']} | {B['name']} — Vlaams-Brabant, Brussel & Waals-Brabant",
        f"{s['intro']} Bel {B['phone_display']}.",
        f"{B['domain']}/{skey}/", schema_localbusiness(), inner)

# ---------- 3. dienst × stad landingspagina ----------
def build_service_city(skey, s, c):
    pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    h1 = f"{esc(s['kw'])} in {esc(c['name'])}"
    lead = f"{s['intro']} Actief in {c['name']} en omgeving ({c['province']})."
    canonical = f"{B['domain']}/{skey}/{c['slug']}/"
    inner = hero(h1, lead) + trust() + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['kw'])} in {esc(c['name'])}</h2>
<div class="prose reveal"><p class="localnote">{esc(c['local'])}</p>{body}</div>
<div class="checks reveal"><h3>Waarvoor u ons kunt bellen in {esc(c['name'])}</h3><ul>{pts}</ul></div>
</div></section>""" + reviews_section() + band(f"{s['kw']} nodig in {c['name']}?")
    render(f"{OUT}/{skey}/{c['slug']}/index.html",
        f"{s['kw']} {c['name']} | {B['name']}",
        f"{s['kw']} in {c['name']} ({c['province']})? {s['intro']} Bel {B['phone_display']}.",
        canonical, schema_localbusiness(c['name'], canonical), inner)

# ---------- 4. sitemap + robots ----------
def build_sitemap():
    urls = [f"{B['domain']}/"]
    for skey in SERVICES:
        urls.append(f"{B['domain']}/{skey}/")
        for c in CITIES:
            urls.append(f"{B['domain']}/{skey}/{c['slug']}/")
    items = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    with open(f"{OUT}/sitemap.xml","w",encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    with open(f"{OUT}/robots.txt","w",encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {B['domain']}/sitemap.xml\n")
    host = B['domain'].replace("https://","").replace("http://","").split("/")[0]
    if "github.io" not in host:
        with open(f"{OUT}/CNAME","w",encoding="utf-8") as f:
            f.write(host)

# ---------- run ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy("style.css", f"{OUT}/style.css")
build_home()
n = 1
for skey, s in SERVICES.items():
    build_service(skey, s); n += 1
    for c in CITIES:
        build_service_city(skey, s, c); n += 1
build_sitemap()
print(f"Klaar. {n} pagina's gegenereerd in ./{OUT}/")
print(f"  - 1 homepage")
print(f"  - {len(SERVICES)} dienstpagina's")
print(f"  - {len(SERVICES)*len(CITIES)} dienst×stad landingspagina's")
print(f"  - sitemap.xml, robots.txt, CNAME")
