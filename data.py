# =====================================================================
#  ELEKTRI PRO — CONTENT & DATA
#  Dit is het ENIGE bestand dat je normaal hoeft aan te passen.
#  Voeg steden toe, pas teksten aan, wijzig diensten — daarna build.py draaien.
# =====================================================================

BUSINESS = {
    "name": "Elektri Pro",
    "phone_display": "+32 498 06 03 77",
    "phone_link": "+32498060377",          # zonder spaties, voor tel:-links
    "email": "",                            # vul in, bv. "info@elektri-pro.be"
    "domain": "https://pj4zwjc8g2-dot.github.io/Elektri-Pro",  # je definitieve domein (voor sitemap + canonical)
    "vat": "",                              # BTW-nummer voor de footer, bv. "BE 0123.456.789"
    "tagline": "Erkend elektricien voor noodinterventies en alle elektriciteitswerken",
}

# ---------------------------------------------------------------------
#  REVIEWS — alleen ECHTE beoordelingen. Voeg er nieuwe toe naarmate ze
#  binnenkomen via je QR-kaarten of e-mailautomatisering.
#  Laat 'city' leeg ("") als de review geen stad vermeldt.
# ---------------------------------------------------------------------
REVIEWS = [
    {"name": "Evans", "city": "", "stars": 5,
     "text": "Uitstekende service! De elektricien kwam snel, zelfs op een feestdag, en loste "
             "het probleem efficiënt op. Zeer professioneel en betrouwbaar — absoluut een aanrader!"},
    {"name": "Kristine", "city": "", "stars": 5,
     "text": "Sammy heeft ons heel goede en snelle service gegeven. Een zeer vriendelijke man."},
    {"name": "Wilfried", "city": "", "stars": 5,
     "text": "Toffe kerel, heeft zijn best gedaan en mij uit de nood geholpen."},
    {"name": "Nicolas", "city": "", "stars": 5,
     "text": "Sammy is heel correct geweest. Vlotte afhandeling, correct!"},
]

# ---------------------------------------------------------------------
#  DIENSTEN
#  'slug' = stuk van de URL.  'kw' = hoofd-zoekwoord (komt in title/H1).
#  'intro' en 'body' mag je per dienst zo uniek en uitgebreid maken als je wilt.
#  Hoe meer eigen, kwalitatieve tekst, hoe beter voor SEO.
# ---------------------------------------------------------------------
SERVICES = {
    "noodelektricien": {
        "label": "Noodinterventies",
        "kw": "Noodelektricien",
        "icon": "🚨",
        "intro": "Een plotse stroompanne, kortsluiting of een installatie die uitvalt? "
                 "Elektri Pro komt snel ter plaatse en lost het op.",
        "body": [
            "Een elektrisch defect wacht niet op een geschikt moment. Een doorgeslagen "
            "differentieel midden in de nacht, een kortsluiting die uw zekeringkast platlegt, "
            "of een stopcontact dat plots verschroeit — het zijn situaties waarbij u snel een "
            "vakman nodig hebt die weet wat hij doet.",
            "Wij sporen de oorzaak op in plaats van enkel het symptoom weg te nemen. Zo voorkomt "
            "u dat hetzelfde probleem zich enkele dagen later opnieuw voordoet. De prijs bespreken "
            "we vooraf, ook bij een dringende interventie, zodat u nooit voor verrassingen staat.",
        ],
        "points": [
            "Stroomuitval en volledige pannes",
            "Kortsluiting en doorgeslagen zekeringen",
            "Differentieel die blijft afspringen",
            "Oververhitte of beschadigde stopcontacten",
            "Defecte verdeelkast na onweer of overspanning",
        ],
    },
    "zekeringkast": {
        "label": "Zekeringkast & verdeelbord",
        "kw": "Zekeringkast vervangen",
        "icon": "⚙️",
        "intro": "Een verouderde of overbelaste zekeringkast vervangen, uitbreiden of in orde "
                 "brengen volgens de huidige normen.",
        "body": [
            "Het verdeelbord is het hart van uw elektrische installatie. Een verouderde kast met "
            "smeltzekeringen, te weinig differentieels of geen ruimte voor uitbreiding is niet "
            "alleen onpraktisch, maar ook een veiligheidsrisico. Bij een renovatie of zwaardere "
            "verbruikers zoals een laadpaal is een aangepaste kast vaak noodzakelijk.",
            "Wij vernieuwen of breiden uw zekeringkast uit met de juiste automaten en "
            "differentieelschakelaars, netjes gelabeld en conform de regelgeving — klaar voor de "
            "keuring. U krijgt een overzichtelijk bord waarvan u zelf begrijpt hoe het werkt.",
        ],
        "points": [
            "Oude smeltzekeringen vervangen door automaten",
            "Differentieelschakelaars plaatsen of bijplaatsen",
            "Verdeelbord uitbreiden voor extra kringen",
            "Voorbereiding voor laadpaal of zonnepanelen",
            "In orde brengen voor de keuring",
        ],
    },
}

# ---------------------------------------------------------------------
#  STEDEN
#  'local' = UNIEKE lokale zin(nen). DIT IS CRUCIAAL VOOR SEO.
#  Schrijf voor elke stad iets eigen: een wijk, de afstand, lokale context.
#  Kopieer NOOIT dezelfde tekst met enkel de naam veranderd — dat straft Google af.
# ---------------------------------------------------------------------
CITIES = [
    {"name": "Leuven", "slug": "leuven", "province": "Vlaams-Brabant",
     "local": "Van het centrum binnen de ring tot Heverlee, Kessel-Lo en Wilsele — "
              "in en rond Leuven zijn we vlot ter plaatse voor zowel studentenkoten als gezinswoningen."},
    {"name": "Halle", "slug": "halle", "province": "Vlaams-Brabant",
     "local": "In Halle en de omliggende gemeenten zoals Beersel en Sint-Pieters-Leeuw "
              "staan we klaar voor dringende interventies en geplande werken."},
    {"name": "Vilvoorde", "slug": "vilvoorde", "province": "Vlaams-Brabant",
     "local": "Vilvoorde, Machelen en de Brusselse rand: een regio met veel oudere installaties "
              "die toe zijn aan vernieuwing. Wij kennen het type woningen hier goed."},
    {"name": "Tienen", "slug": "tienen", "province": "Vlaams-Brabant",
     "local": "In het Hageland, met Tienen als centrum, bedienen we zowel de stadskern "
              "als de landelijkere omgeving errond."},
    {"name": "Aarschot", "slug": "aarschot", "province": "Vlaams-Brabant",
     "local": "Voor Aarschot en omstreken combineren we snelle bereikbaarheid met "
              "vakkundig werk aan zowel nieuwbouw als oudere woningen."},
    {"name": "Asse", "slug": "asse", "province": "Vlaams-Brabant",
     "local": "Asse en de gemeenten richting Brussel: een gebied waar we regelmatig "
              "zekeringkasten vernieuwen in woningen uit de jaren '70 en '80."},
    {"name": "Brussel", "slug": "brussel", "province": "Brussel",
     "local": "In het Brussels Hoofdstedelijk Gewest, van de vijfhoek tot de randgemeenten, "
              "werken we voor appartementen, handelszaken en kantoren — vaak met de uitdagingen "
              "van oudere stadsbebouwing."},
    {"name": "Waver", "slug": "waver", "province": "Waals-Brabant",
     "local": "In Waver (Wavre) en omgeving zijn we tweetalig ter plaatse voor zowel "
              "particulieren als bedrijven in Waals-Brabant."},
    {"name": "Nijvel", "slug": "nijvel", "province": "Waals-Brabant",
     "local": "Nijvel (Nivelles) en de zuidelijke rand van Waals-Brabant: ook hier "
              "verzorgen we noodinterventies en installatiewerk."},
    {"name": "Eigenbrakel", "slug": "eigenbrakel", "province": "Waals-Brabant",
     "local": "Eigenbrakel (Braine-l'Alleud) en omstreken bedienen we voor dringende "
              "herstellingen en geplande elektriciteitswerken."},
]
