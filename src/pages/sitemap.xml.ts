import type { APIRoute } from 'astro';

const SITE = 'https://renovpro.be';

const pages = [
  { loc: '/nl/', changefreq: 'monthly', priority: '1.0' },
  { loc: '/fr/', changefreq: 'monthly', priority: '1.0' },
  { loc: '/nl/studio/', changefreq: 'monthly', priority: '0.9' },
  { loc: '/fr/studio/', changefreq: 'monthly', priority: '0.9' },
];

export const GET: APIRoute = () => {
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${pages.map(p => `  <url>
    <loc>${SITE}${p.loc}</loc>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
    <xhtml:link rel="alternate" hreflang="nl" href="${SITE}/nl/"/>
    <xhtml:link rel="alternate" hreflang="fr" href="${SITE}/fr/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="${SITE}/nl/"/>
  </url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
