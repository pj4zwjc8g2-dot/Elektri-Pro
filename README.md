# Renov Pro — website

Tweetalige (NL/FR) Astro-site met interactieve Projectstudio (prijsconfigurator) voor leadgeneratie.

## Stack

- **Astro 5** + TypeScript — statische output, server-side API route voor lead-endpoint
- **Preact** — configurator island met `client:visible`
- **GitHub Pages** — statische hosting
- **Make.com webhook** — lead-routing naar Teamleader

## Lokale ontwikkeling

```bash
cp .env.example .env        # vul MAKE_WEBHOOK_URL in
pnpm install
pnpm dev                    # http://localhost:4321
```

## Tests

```bash
pnpm test                   # vitest — unit tests voor pricing.ts
```

## Build & deploy

Push naar `main` triggert de GitHub Actions workflow:
1. `pnpm test` — pricing unit tests
2. `pnpm build` — Astro build → `dist/`
3. Deploy naar GitHub Pages

### Secrets instellen in GitHub → Settings → Secrets

| Secret             | Waarde                                      |
|--------------------|---------------------------------------------|
| `MAKE_WEBHOOK_URL` | URL van je Make.com webhook (niet public)   |
| `GTM_ID`           | GTM container ID (bv. GTM-TGTKG654)         |

## Structuur

```
src/
  pages/
    index.astro            → redirect naar /nl/
    nl/index.astro         → NL home
    fr/index.astro         → FR home
    nl/studio/index.astro  → NL configurator
    fr/studio/index.astro  → FR configurator
    api/lead.ts            → POST endpoint → Make webhook
    sitemap.xml.ts
  components/
    studio/Studio.tsx      → Preact island (configurator)
    studio/Studio.css
    Header.astro  Hero.astro  Services.astro  Approach.astro
    Process.astro  Gallery.astro  Testimonial.astro  Contact.astro
    Footer.astro  ConsentBanner.astro  BaseHead.astro
  lib/
    pricing.ts             → prijsmodel (pure functies, getest)
    pricing.test.ts
    i18n.ts
  i18n/  nl.json  fr.json
  styles/ tokens.css
```

## TODO vóór launch

- [ ] FR copy laten nakijken door native speaker (zoek `// TODO: verify FR copy`)
- [ ] Echte projectfoto's aanleveren → `public/images/` (Gallery.astro `// TODO`)
- [ ] BTW-nummer: `[BTW BE 0000.000.000]`
- [ ] Telefoonnummer: `[TODO: telefoonnummer]`
- [ ] Erkenningen: `[erkenningen toe te voegen]`
- [ ] Eigen prijscalculatietarieven in `src/lib/pricing.ts` (RATES-object)
- [ ] `MAKE_WEBHOOK_URL` secret instellen in GitHub
- [ ] `GTM_ID` secret instellen in GitHub
- [ ] `CNAME` bijwerken naar `renovpro.be`
