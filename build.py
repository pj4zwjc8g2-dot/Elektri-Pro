#!/usr/bin/env python3
# =====================================================================
#  build.py — Elektri Pro v4 (NL / FR / EN)
# =====================================================================
import os, shutil, html, datetime, json
from data import BUSINESS, SERVICES, CITIES, REVIEWS, MENU, FAQ, TRUST_POINTS, UI, LANG_CONFIG, FAQ_KEURING, CITY_KEURING

OUT   = "site"
B     = BUSINESS
D     = B["domain"]
YEAR  = datetime.date.today().year
TODAY = datetime.date.today().isoformat()
LANGS = ["nl", "fr", "en"]

def esc(s): return html.escape(str(s), quote=True)

# ── head ──────────────────────────────────────────────────────────────
def head(title, desc, canonical, schema, lang, canon_path):
    cfg   = LANG_CONFIG[lang]
    hrefl = ""
    for l, c in LANG_CONFIG.items():
        hrefl += f'<link rel="alternate" hreflang="{c["hreflang"]}" href="{D}{c["prefix"]}{canon_path}">\n'
    hrefl += f'<link rel="alternate" hreflang="x-default" href="{D}{canon_path}">\n'
    return f"""<!DOCTYPE html>
<html lang="{cfg['lang_attr']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{cfg['locale']}">
<meta property="og:url" content="{canonical}">
{hrefl}<link rel="preconnect" href="https://fonts.googleapis.com">
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

# ── topbar ────────────────────────────────────────────────────────────
def topbar(lang, canon_path):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    nav = ""
    for m in MENU[lang]:
        full = f"{D}{pfx}{m['url']}"
        act  = ' class="active"' if m["url"] == canon_path else ""
        nav += f'<a href="{full}"{act}>{esc(m["label"])}</a>'
    drop = ""
    lang_mobile = ""
    for l in LANGS:
        lp  = LANG_CONFIG[l]["prefix"]
        url = f"{D}{lp}{canon_path}"
        act_drop   = ' class="lang-active"' if l == lang else ""
        act_mob    = " lang-mob-active" if l == lang else ""
        drop       += f'<a href="{url}"{act_drop}>{LANG_CONFIG[l]["label"]}</a>'
        lang_mobile += f'<a href="{url}" class="lang-mob-item{act_mob}">{LANG_CONFIG[l]["label"]}</a>'
    current_label = LANG_CONFIG[lang]["label"]
    lsw = f'<div class="lang-sw"><button class="lang-trigger" aria-haspopup="true">{current_label} <span class="lang-arrow">▾</span></button><div class="lang-drop">{drop}</div></div>'
    return f"""<header class="topbar"><div class="wrap">
<a class="brand" href="{D}{pfx}/">🔌 Elektri<span class="pro">Pro</span></a>
<nav class="mainnav">{nav}<div class="lang-mobile">{lang_mobile}</div></nav>
{lsw}
<a class="call-btn" href="tel:{B['phone_link']}" data-call="header">
<span class="ring">📞</span><span class="txt">{esc(B['phone_display'])}</span></a>
<button class="burger" aria-label="Menu" onclick="document.querySelector('.mainnav').classList.toggle('open')">☰</button>
</div></header>"""

# ── footer / mobile call ──────────────────────────────────────────────
def mobile_call(lang):
    u = UI[lang]
    return f'<a class="mobile-call" href="tel:{B["phone_link"]}" data-call="mobile-sticky">📞 {esc(u["mob_prefix"])} {esc(B["phone_display"])}</a>'

def footer(lang):
    u     = UI[lang]
    pfx   = LANG_CONFIG[lang]["prefix"]
    slinks = "".join(f'<a href="{D}{pfx}/{k}/">{esc(s["label"])}</a>' for k, s in SERVICES[lang].items())
    mlinks = "".join(f'<a href="{D}{pfx}{m["url"]}">{esc(m["label"])}</a>' for m in MENU[lang])
    return f"""<footer><div class="wrap">
<div class="col"><h4><span style="color:var(--accent)">🔌</span> {esc(B['name'])}</h4>
<p>{esc(B['tagline'][lang])}.</p><p>{esc(u['ft_both'])}</p></div>
<div class="col"><h4>{esc(u['ft_srv'])}</h4>{slinks}</div>
<div class="col"><h4>{esc(u['ft_nav'])}</h4>{mlinks}</div>
<div class="col"><h4>{esc(u['ft_cnt'])}</h4><a href="tel:{B['phone_link']}">📞 {esc(B['phone_display'])}</a>
{"<a href='mailto:" + esc(B['email']) + "'>✉ " + esc(B['email']) + "</a>" if B['email'] else ""}
<p style="margin-top:8px">{esc(u['ft_area'])}</p></div>
</div><div class="copy">© {YEAR} {esc(B['name'])}{"  t.a.v. Triple A Trading" if lang == "nl" else ("  à l'att. de Triple A Trading" if lang == "fr" else "  attn. Triple A Trading")}{" — " + esc(B['vat']) if B['vat'] else ""} — {esc(u['ft_rights'])}</div></footer>"""

# ── schema ────────────────────────────────────────────────────────────
def schema_localbusiness(lang, area=None, page_url=None):
    areas = [c["name"][lang] for c in CITIES] if not area else [area]
    total_reviews = len(REVIEWS)
    avg_rating    = sum(r.get("stars", 5) for r in REVIEWS) / total_reviews
    data  = {
        "@context": "https://schema.org",
        "@type":    "Electrician",
        "name":      B["name"],
        "telephone": B["phone_link"],
        "url":       page_url or B["domain"],
        "areaServed": areas,
        "slogan":    B["tagline"][lang],
        "aggregateRating": {
            "@type":       "AggregateRating",
            "ratingValue": f"{avg_rating:.1f}",
            "reviewCount": total_reviews,
            "bestRating":  5,
            "worstRating": 1,
        },
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def schema_service(lang, service_type, area, page_url):
    data = {
        "@context":   "https://schema.org",
        "@type":      "Service",
        "serviceType": service_type,
        "provider": {"@type": "Electrician", "name": B["name"], "telephone": B["phone_link"]},
        "areaServed": area,
        "url":        page_url,
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

def schema_faq(items):
    data = {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q["q"],
                           "acceptedAnswer":{"@type":"Answer","text":q["a"]}} for q in items]}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

TRACK = """<script>
window.dataLayer=window.dataLayer||[];
document.querySelectorAll('a[href^="tel:"]').forEach(function(a){
 a.addEventListener('click',function(){window.dataLayer.push({event:'phone_call_click',call_location:a.getAttribute('data-call')||'unknown'});});});
</script>"""

# ── render ────────────────────────────────────────────────────────────
def render(path, title, desc, canonical, schema, inner, lang, canon_path):
    full = (head(title, desc, canonical, schema, lang, canon_path)
            + topbar(lang, canon_path)
            + inner
            + footer(lang)
            + mobile_call(lang)
            + TRACK + "\n</body></html>")
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)

# ── shared sections ───────────────────────────────────────────────────
def hero(lang, h1, lead, badge=None):
    u = UI[lang]
    b = esc(badge) if badge else esc(u["avail_badge"])
    regions = "".join(f'<span>📍 <b>{esc(r)}</b></span>' for r in u["regions"])
    return f"""<section class="hero"><div class="wrap">
<span class="tag"><span class="dot"></span> {b}</span>
<h1>{h1}</h1><p class="lead">{esc(lead)}</p>
<div class="cta-row">
<a class="btn-primary" href="tel:{B['phone_link']}" data-call="hero">📞 Bel {esc(B['phone_display'])}</a>
<a class="btn-ghost" href="#info">→</a></div>
<div class="regions">{regions}</div>
</div></section>"""

def trust_strip(lang):
    u = UI[lang]
    return f"""<section class="trust"><div class="wrap">
<div class="item"><b>{esc(u['t24'])}</b><span>{esc(u['t24s'])}</span></div>
<div class="item"><b>{esc(u['tfast'])}</b><span>{esc(u['tfasts'])}</span></div>
<div class="item"><b>{esc(u['tcert'])}</b><span>{esc(u['tcerts'])}</span></div>
<div class="item"><b>{esc(u['tclear'])}</b><span>{esc(u['tclears'])}</span></div>
</div></section>"""

def trust_grid(lang):
    cards = ""
    for t in TRUST_POINTS[lang]:
        cards += f'<div class="tp-card"><div class="tp-ic">{t["icon"]}</div><h3>{esc(t["title"])}</h3><p>{esc(t["text"])}</p></div>'
    u = UI[lang]
    return f"""<section class="section trust-section"><div class="wrap">
<h2 class="reveal">{esc(u['why_title'])}</h2>
<p class="sub reveal">{esc(u['why_sub'])}</p>
<div class="tp-grid reveal">{cards}</div></div></section>"""

def reviews_section(lang):
    u = UI[lang]
    cards = ""
    for r in REVIEWS:
        n = int(r.get("stars", 5))
        stars = f'<div class="stars" aria-label="{n}/5">{"★"*n}{"☆"*(5-n)}</div>'
        init  = esc(r["name"][:1].upper())
        cards += f"""<figure class="review">{stars}
<blockquote>{esc(r['text'])}</blockquote>
<figcaption><span class="avatar">{init}</span><span>{esc(r['name'])}</span></figcaption>
</figure>"""
    return f"""<section class="section reviews-sec"><div class="wrap">
<h2 class="reveal">{esc(u['rev_title'])}</h2>
<p class="sub reveal">{esc(u['rev_sub'])}</p>
<div class="reviewgrid reveal">{cards}</div></div></section>"""

def band(lang, title=None, subtitle=None):
    u = UI[lang]
    t = esc(title)    if title    else esc(u["cta_title"])
    s = esc(subtitle) if subtitle else esc(u["cta_sub"])
    return f"""<section class="band"><div class="wrap"><h2>{t}</h2>
<p>{s}</p>
<a class="big-call" href="tel:{B['phone_link']}" data-call="band">📞 {esc(B['phone_display'])}</a></div></section>"""

def faq_block(lang, items):
    u = UI[lang]
    rows = "".join(
        f'<details class="faq-item"{" open" if i == 0 else ""}>'
        f'<summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>'
        for i, q in enumerate(items)
    )
    titles = {"nl": "Veelgestelde vragen over de elektriciteitskeuring",
              "fr": "Questions fréquentes sur le contrôle électrique",
              "en": "Frequently asked questions about electrical inspection"}
    return (f'<section class="section" id="faq"><div class="wrap">'
            f'<h2 class="reveal">{esc(titles[lang])}</h2>'
            f'<div class="faq-list reveal">{rows}</div></div></section>')

def crosslink_block(lang, skey, pfx, cname, slug):
    PAIR = {"keuring": "zekeringkast", "zekeringkast": "keuring"}
    if skey not in PAIR:
        return ""
    target = PAIR[skey]
    target_url = f"{pfx}/{target}/{slug}/"
    INTRO = {
        "keuring": {
            "nl": f"Na de keuring moet de zekeringkast soms worden vernieuwd of uitgebreid.",
            "fr": f"Après le contrôle, le tableau électrique doit parfois être mis à jour.",
            "en": f"After an inspection, the fuse box sometimes needs to be upgraded.",
        },
        "zekeringkast": {
            "nl": f"Een nieuwe zekeringkast vereist vaak een elektriciteitskeuring.",
            "fr": f"Un nouveau tableau nécessite souvent un contrôle électrique.",
            "en": f"A new fuse box often requires an electrical inspection.",
        },
    }
    ANCHOR = {
        "keuring": {
            "nl": f"Zekeringkast vervangen in {cname}",
            "fr": f"Remplacement du tableau électrique à {cname}",
            "en": f"Fuse box replacement in {cname}",
        },
        "zekeringkast": {
            "nl": f"Elektriciteitskeuring in {cname}",
            "fr": f"Contrôle électrique à {cname}",
            "en": f"Electrical inspection in {cname}",
        },
    }
    intro  = INTRO[skey][lang]
    anchor = ANCHOR[skey][lang]
    return (f'<div class="crosslink reveal">'
            f'<p>{esc(intro)} <a href="{esc(target_url)}">{esc(anchor)}</a>.</p>'
            f'</div>')

# ── page builders ─────────────────────────────────────────────────────
def build_home(lang):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    S   = SERVICES[lang]
    cards = ""
    for skey, s in S.items():
        cls   = "card urgent" if skey == "noodelektricien" else "card"
        extra = f'<a class="mini" href="tel:{B["phone_link"]}" data-call="card-{skey}">📞 {esc(u["call_now"])}</a>' if skey == "noodelektricien" else ""
        cards += f'<a class="{cls}" href="{D}{pfx}/{skey}/"><div class="ic">{s["icon"]}</div><h3>{esc(s["label"])}</h3><p>{esc(s["intro"])}</p>{extra}</a>'
    inner = (hero(lang, u["hero_h1"], u["hero_lead"])
             + trust_strip(lang)
             + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(u['our_services'])}</h2>
<p class="sub reveal">{esc(u['specialized'])}</p>
<div class="grid">{cards}</div></div></section>"""
             + trust_grid(lang) + reviews_section(lang) + band(lang))
    canon = "/"
    render(f"{OUT}{pfx}/index.html",
           u["home_title"], u["home_desc"],
           f"{D}{pfx}/", schema_localbusiness(lang), inner, lang, canon)

def build_diensten(lang):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    S   = SERVICES[lang]
    cards = ""
    for skey, s in S.items():
        pts = "".join(f"<li>{esc(p)}</li>" for p in s["points"][:3])
        cards += f"""<div class="d-card"><div class="d-ic">{s['icon']}</div>
<h3>{esc(s['label'])}</h3><p>{esc(s['intro'])}</p>
<ul>{pts}</ul>
<a class="d-link" href="{D}{pfx}/{skey}/">{esc(u['more_on'])} {esc(s['label']).lower()} →</a></div>"""
    inner = (hero(lang, u["srv_pg_title"].split("|")[0].strip(), u["srv_lead"])
             + f'<section class="section"><div class="wrap"><div class="d-grid">{cards}</div></div></section>'
             + trust_grid(lang) + reviews_section(lang) + band(lang))
    canon = "/diensten/"
    render(f"{OUT}{pfx}/diensten/index.html",
           u["srv_pg_title"], u["srv_pg_desc"],
           f"{D}{pfx}/diensten/", schema_localbusiness(lang), inner, lang, canon)

def build_faq(lang):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    items = ""
    for i, fq in enumerate(FAQ[lang]):
        items += f"""<details class="faq-item"{' open' if i==0 else ''}>
<summary>{esc(fq['q'])}</summary><p>{esc(fq['a'])}</p></details>"""
    inner = (hero(lang, u["faq_title"], u["faq_lead"], badge=u["faq_badge"])
             + f'<section class="section"><div class="wrap"><div class="faq-list reveal">{items}</div></div></section>'
             + band(lang, u["still_q"], u["call_help"]))
    canon = "/faq/"
    render(f"{OUT}{pfx}/faq/index.html",
           u["faq_pg_title"], u["faq_pg_desc"],
           f"{D}{pfx}/faq/",
           schema_localbusiness(lang) + schema_faq(FAQ[lang]),
           inner, lang, canon)

def build_contact(lang):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    inner = (hero(lang, u["cnt_title"], u["cnt_lead"], badge=u["cnt_badge"])
             + f"""<section class="section"><div class="wrap">
<div class="contact-grid">
  <div class="contact-card">
    <h2>{esc(u['by_phone'])}</h2>
    <p>{esc(u['phone_fast'])}</p>
    <a class="big-call" href="tel:{B['phone_link']}" data-call="contact-page">📞 {esc(B['phone_display'])}</a>
  </div>
  <div class="contact-card">
    <h2>{esc(u['details'])}</h2>
    <p><strong>{esc(u['co_label'])}:</strong> {esc(B['name'])}</p>
    <p><strong>{esc(u['area_label'])}:</strong> {esc(u['area_val'])}</p>
  </div>
</div></div></section>"""
             + trust_grid(lang) + band(lang, u["prefer"]))
    canon = "/contact/"
    render(f"{OUT}{pfx}/contact/index.html",
           u["cnt_pg_title"], u["cnt_pg_desc"],
           f"{D}{pfx}/contact/", schema_localbusiness(lang), inner, lang, canon)

def build_service(lang, skey, s):
    u   = UI[lang]
    pfx = LANG_CONFIG[lang]["prefix"]
    pts  = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    by_prov = {}
    for c in CITIES:
        pname = c["province"][lang]
        by_prov.setdefault(pname, []).append(c)
    pblocks = ""
    for prov, cs in by_prov.items():
        chips = "".join(
            f'<a class="citychip" href="{D}{pfx}/{skey}/{c["slug"]}/">{esc(s["kw"])} {esc(c["name"][lang])}</a>'
            for c in cs)
        pblocks += f'<div class="prov-block"><h3>{esc(prov)}</h3><div class="citygrid">{chips}</div></div>'
    faq_section = faq_block(lang, FAQ_KEURING[lang]) + schema_faq(FAQ_KEURING[lang]) if skey == "keuring" else ""
    inner = (hero(lang, f'{esc(s["kw"])} — Brabant &amp; Brussel', s["intro"])
             + trust_strip(lang)
             + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['label'])}</h2>
<div class="prose reveal">{body}</div>
<div class="checks reveal"><h3>{esc(u['why_call'])} …</h3><ul>{pts}</ul></div>
<h2 class="reveal" style="margin-top:54px">{esc(s['kw'])} {esc(u['per_city'])}</h2>
<p class="sub reveal">{esc(u['sel_city'])}</p>
{pblocks}
</div></section>"""
             + faq_section + trust_grid(lang) + reviews_section(lang) + band(lang))
    canon = f"/{skey}/"
    keuring_subtitle = {"nl": "Installaties conform AREI", "fr": "Mise en conformité RGIE", "en": "AREI Compliance"}
    keuring_svc_type = {"nl": "Elektriciteitskeuring", "fr": "Contrôle électrique", "en": "Electrical Inspection"}
    title = (f"{s['kw']} | {keuring_subtitle[lang]} | {B['name']}" if skey == "keuring"
             else f"{s['kw']} | {B['name']}")
    page_url = f"{D}{pfx}/{skey}/"
    extra_schema = (schema_service(lang, keuring_svc_type[lang], B["tagline"][lang], page_url)
                    if skey == "keuring" else "")
    render(f"{OUT}{pfx}/{skey}/index.html",
           title,
           f"{s['intro']} {B['phone_display']}.",
           page_url, schema_localbusiness(lang) + extra_schema, inner, lang, canon)

def build_service_city(lang, skey, s, c):
    u     = UI[lang]
    pfx   = LANG_CONFIG[lang]["prefix"]
    cname = c["name"][lang]
    pts   = "".join(f"<li>{esc(p)}</li>" for p in s["points"])
    body  = "".join(f"<p>{esc(par)}</p>" for par in s["body"])
    nearby_chips = "".join(f'<span class="nb-chip">{esc(n)}</span>' for n in c.get("nearby", []))
    nearby_block = ""
    if nearby_chips:
        nearby_block = f"""<div class="nearby reveal">
<h3>{esc(u['also_active'])} {esc(cname)}</h3>
<p>{esc(u['not_only1'])} {esc(cname)} {esc(u['not_only2'])}</p>
<div class="nb-list">{nearby_chips}</div>
<p class="nb-note">{esc(u['not_sure'])} <a href="tel:{B['phone_link']}" data-call="nearby">{esc(u['call_ch'])} {esc(B['phone_display'])}</a> {esc(u['call_ch2'])}</p>
</div>"""
    lead   = f"{s['intro']} {c['province'][lang]}."
    canon  = f"/{skey}/{c['slug']}/"
    city_faq = faq_block(lang, FAQ_KEURING[lang]) + schema_faq(FAQ_KEURING[lang]) if skey == "keuring" else ""
    localnote = CITY_KEURING.get(c["slug"], {}).get(lang, c["local"][lang]) if skey == "keuring" else c["local"][lang]
    xlink  = crosslink_block(lang, skey, pfx, cname, c["slug"])
    inner  = (hero(lang, f'{esc(s["kw"])} {esc(cname)}', lead)
              + trust_strip(lang)
              + f"""<section class="section" id="info"><div class="wrap">
<h2 class="reveal">{esc(s['kw'])} {esc(cname)}</h2>
<div class="prose reveal"><p class="localnote">{esc(localnote)}</p>{body}</div>
<div class="checks reveal"><h3>{esc(u['why_call'])} {esc(cname)}</h3><ul>{pts}</ul></div>
{nearby_block}
{xlink}
</div></section>"""
              + city_faq + trust_grid(lang) + reviews_section(lang) + band(lang, f"{s['kw']} — {cname}?"))
    if skey == "keuring":
        keuring_suf = {"nl": "Conform & klaar voor keuring", "fr": "Mise en conformité électrique", "en": "Electrical Compliance"}
        keuring_desc = {
            "nl": f"Elektriciteitskeuring in {cname}? Wij bereiden uw installatie voor op de keuring of werken inbreuken weg. AREI-conform. Bel {B['phone_display']}.",
            "fr": f"Contrôle électrique à {cname} ? Mise en conformité RGIE rapide et professionnelle. Appelez le {B['phone_display']}.",
            "en": f"Electrical inspection in {cname}? We prepare your installation for compliance or rectify violations from a negative report. Call {B['phone_display']}.",
        }
        keuring_svc_type = {"nl": "Elektriciteitskeuring", "fr": "Contrôle électrique", "en": "Electrical Inspection"}
        pg_title   = f"{s['kw']} {cname} — {keuring_suf[lang]} | {B['name']}"
        pg_desc    = keuring_desc[lang]
        page_url_c = f"{D}{pfx}{canon}"
        extra_sc   = schema_service(lang, keuring_svc_type[lang], cname, page_url_c)
    else:
        pg_title   = f"{s['kw']} {cname} | {B['name']}"
        pg_desc    = f"{s['kw']} {cname} ({c['province'][lang]}). {s['intro']} {B['phone_display']}."
        page_url_c = f"{D}{pfx}{canon}"
        extra_sc   = ""
    render(f"{OUT}{pfx}/{skey}/{c['slug']}/index.html",
           pg_title, pg_desc,
           page_url_c,
           schema_localbusiness(lang, cname, page_url_c) + extra_sc,
           inner, lang, canon)

def build_sitemap():
    # Canonical paths (lang-neutral; NL prefix is empty so these are the NL URLs)
    canon_paths = ["/", "/diensten/", "/faq/", "/contact/"]
    for skey in SERVICES["nl"]:
        canon_paths.append(f"/{skey}/")
        for c in CITIES:
            canon_paths.append(f"/{skey}/{c['slug']}/")

    def xhtml_alts(cp):
        alts = ""
        for l, c in LANG_CONFIG.items():
            alts += f'<xhtml:link rel="alternate" hreflang="{c["hreflang"]}" href="{D}{c["prefix"]}{cp}"/>'
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{D}{cp}"/>'
        return alts

    items = ""
    for lang, cfg in LANG_CONFIG.items():
        pfx = cfg["prefix"]
        for cp in canon_paths:
            items += f"<url><loc>{D}{pfx}{cp}</loc><lastmod>{TODAY}</lastmod>{xhtml_alts(cp)}</url>"

    with open(f"{OUT}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
            ' xmlns:xhtml="http://www.w3.org/1999/xhtml">'
            f"{items}</urlset>"
        )
    with open(f"{OUT}/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {D}/sitemap.xml\n")
    host = D.replace("https://", "").replace("http://", "").strip("/")
    if "github.io" not in host:
        with open(f"{OUT}/CNAME", "w", encoding="utf-8") as f:
            f.write(host)

# ── run ───────────────────────────────────────────────────────────────
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy("style.css", f"{OUT}/style.css")

total = 0
for lang in LANGS:
    pfx = LANG_CONFIG[lang]["prefix"]
    if pfx:
        os.makedirs(f"{OUT}{pfx}", exist_ok=True)
    build_home(lang);     total += 1
    build_diensten(lang); total += 1
    build_faq(lang);      total += 1
    build_contact(lang);  total += 1
    for skey, s in SERVICES[lang].items():
        build_service(lang, skey, s); total += 1
        for c in CITIES:
            build_service_city(lang, skey, s, c); total += 1

build_sitemap()
print(f"Klaar. {total} pagina's gegenereerd in ./{OUT}/ ({len(LANGS)} talen)")
