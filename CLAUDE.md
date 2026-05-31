# Renov Pro — project rules

## Stack
Astro 5 + TypeScript · Preact islands · Static output → GitHub Pages
Node ≥ 20, pnpm. Run `pnpm dev` / `pnpm build` / `pnpm test`.

## Design tokens
All CSS custom properties live in `src/styles/tokens.css`.
**Never use Inter, Roboto or Arial.** Fonts: Fraunces (display/serif) + Hanken Grotesk (body).
Logo lockup: `Renov` (serif) + `Pro` (brass italic).

## Pricing model
Pure functions in `src/lib/pricing.ts` with unit tests in `pricing.test.ts`.
Numbers are indicative Belgian market prices 2025 incl. VAT — Renov Pro replaces them with own rates.
Run `pnpm test` before touching this file.

## i18n
All UI strings in `src/i18n/nl.json` and `src/i18n/fr.json`.
FR copy is AI-generated and marked `// TODO: verify FR copy` — have a native speaker review before launch.
Never hardcode user-facing text in components.

## Lead endpoint
`src/pages/api/lead.ts` — validates with zod, checks honeypot, rate-limits, forwards to Make webhook.
Webhook URL is **server-side only** via `MAKE_WEBHOOK_URL` env var. Never expose it client-side.

## Legal
- Claim only services for which Renov Pro holds the required professional access ("toegang tot het beroep").
- Roofing/waterproofing and structural work are regulated in Brussels and Walloon Brabant — do not add certifications without confirmation. Use placeholder: `[erkenningen toe te voegen]`.
- Always show the indicative-price disclaimer (§7 of briefing) near any estimate.
- Cookie/consent banner must fire before GTM/GA4 loads.
