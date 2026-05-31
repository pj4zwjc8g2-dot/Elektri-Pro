import type { APIRoute } from 'astro';
import { z } from 'zod';

// Rate limiting: simple in-memory store (resets on cold start)
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 60_000;

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    rateLimitMap.set(ip, { count: 1, resetAt: now + RATE_WINDOW_MS });
    return false;
  }
  if (entry.count >= RATE_LIMIT) return true;
  entry.count++;
  return false;
}

const ContactSchema = z.object({
  name: z.string().min(1).max(120),
  phone: z.string().max(30).optional().default(''),
  email: z.string().email().max(200),
  address: z.string().max(200).optional().default(''),
});

const ProjectSchema = z.object({
  scope: z.array(z.string()).min(1),
  woonopp: z.number().min(1).max(2000).optional(),
  uitbreidingopp: z.number().min(0).max(1000).optional(),
  niveau: z.enum(['essentieel', 'comfort', 'exclusief']).optional(),
  regio: z.enum(['vlb', 'bru', 'wab']).optional(),
  timing: z.string().optional(),
});

const EstimateSchema = z.object({
  currency: z.literal('EUR'),
  low: z.number().nonnegative(),
  high: z.number().nonnegative(),
  weeksLow: z.number().nonnegative(),
  weeksHigh: z.number().nonnegative(),
  lines: z.array(z.object({
    module: z.string(),
    area: z.number(),
    low: z.number(),
    high: z.number(),
  })),
}).nullable().optional();

const LeadSchema = z.object({
  brand: z.literal('Renov Pro'),
  locale: z.enum(['nl', 'fr']),
  timestamp: z.string(),
  contact: ContactSchema,
  project: ProjectSchema,
  estimate: EstimateSchema,
  meta: z.object({
    source: z.string(),
    referrer: z.string().optional().default(''),
    userAgent: z.string().optional().default(''),
  }).optional(),
  // honeypot — must be absent or empty
  honeypot: z.string().max(0).optional(),
  hp: z.string().max(0).optional(),
});

export const POST: APIRoute = async ({ request }) => {
  const webhookUrl = import.meta.env.MAKE_WEBHOOK_URL;
  if (!webhookUrl) {
    return new Response(JSON.stringify({ error: 'Webhook not configured' }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Rate limiting by IP
  const ip = request.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (isRateLimited(ip)) {
    return new Response(JSON.stringify({ error: 'Too many requests' }), {
      status: 429,
      headers: { 'Content-Type': 'application/json', 'Retry-After': '60' },
    });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const parsed = LeadSchema.safeParse(body);
  if (!parsed.success) {
    return new Response(JSON.stringify({ error: 'Validation failed', issues: parsed.error.issues }), {
      status: 422,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Honeypot check
  if (parsed.data.honeypot || parsed.data.hp) {
    // Silently accept to not tip off bots
    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const webhookRes = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsed.data),
    });

    if (!webhookRes.ok) {
      throw new Error(`Webhook returned ${webhookRes.status}`);
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('[lead] webhook error:', err);
    return new Response(JSON.stringify({ error: 'Upstream error' }), {
      status: 502,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
