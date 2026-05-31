import { defineConfig } from "astro/config";
import preact from "@astrojs/preact";

// NOTE: output is "static" for GitHub Pages hosting.
// The /api/lead endpoint requires a server runtime. Options:
//   A) Set PUBLIC_LEAD_ENDPOINT env var to a Cloudflare Worker or other external URL.
//   B) Switch hosting to Netlify/Cloudflare Pages and change output to "hybrid".
// See README.md → "Lead endpoint & GitHub Pages".
export default defineConfig({
  integrations: [preact({ compat: true })],
  i18n: {
    defaultLocale: "nl",
    locales: ["nl", "fr"],
    routing: { prefixDefaultLocale: true },
  },
  output: "static",
  trailingSlash: "always",
});
