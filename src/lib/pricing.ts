// Indicative Belgian market prices 2025 incl. VAT — replace with own rates after site launch
export const RATES = {
  dak:         { essentieel: [75, 120],   comfort: [120, 175],   exclusief: [175, 250]  },
  gevel:       { essentieel: [80, 140],   comfort: [140, 220],   exclusief: [220, 320]  },
  interieur:   { essentieel: [400, 700],  comfort: [700, 1100],  exclusief: [1100, 1600] },
  uitbreiding: { essentieel: [1800, 2300],comfort: [2300, 2900], exclusief: [2900, 3600] },
  totaal:      { essentieel: [1000, 1400],comfort: [1500, 2000], exclusief: [2100, 2800] },
} as const;

export const WEEKS = {
  dak: [1, 3], gevel: [2, 4], interieur: [4, 9],
  uitbreiding: [8, 15], totaal: [12, 26],
} as const;

export const REGION_FACTOR = { vlb: 1.00, bru: 1.03, wab: 0.96 } as const;

export type Module = keyof typeof RATES;
export type Level = 'essentieel' | 'comfort' | 'exclusief';
export type Region = keyof typeof REGION_FACTOR;

export interface PricingInput {
  scope: Module[];
  woonopp: number;
  uitbreidingopp?: number;
  niveau: Level;
  regio: Region;
}

export interface PricingLine {
  module: Module;
  area: number;
  low: number;
  high: number;
}

export interface PricingResult {
  low: number;
  high: number;
  weeksLow: number;
  weeksHigh: number;
  lines: PricingLine[];
  impacts: string[];
}

function clamp(val: number, min: number, max: number) {
  return Math.max(min, Math.min(max, val));
}

function roundTo500(n: number) {
  return Math.round(n / 500) * 500;
}

/** Derive area for each module from woonopp */
export function deriveArea(module: Module, woonopp: number, uitbreidingopp = 0): number {
  switch (module) {
    case 'dak': return woonopp * 0.55;
    case 'gevel': return woonopp * 0.9;
    case 'interieur': return woonopp;
    case 'totaal': return woonopp;
    case 'uitbreiding': return uitbreidingopp;
  }
}

/** Effective module list: totaal supersedes dak/gevel/interieur */
export function effectiveModules(scope: Module[]): Module[] {
  if (scope.includes('totaal')) {
    // totaal covers dak/gevel/interieur; uitbreiding remains additive
    return scope.includes('uitbreiding') ? ['totaal', 'uitbreiding'] : ['totaal'];
  }
  return scope;
}

export function calculatePricing(input: PricingInput): PricingResult {
  const { woonopp, uitbreidingopp = 0, niveau, regio } = input;
  const modules = effectiveModules(input.scope);
  const rf = REGION_FACTOR[regio];

  const lines: PricingLine[] = modules.map((mod) => {
    const area = deriveArea(mod, woonopp, uitbreidingopp);
    const [rLow, rHigh] = RATES[mod][niveau];
    return {
      module: mod,
      area,
      low: roundTo500(area * rLow * rf),
      high: roundTo500(area * rHigh * rf),
    };
  });

  const totalLow = roundTo500(lines.reduce((s, l) => s + l.low, 0));
  const totalHigh = roundTo500(lines.reduce((s, l) => s + l.high, 0));

  // Doorlooptijd
  const sizeFactor = clamp(woonopp / 130, 0.8, 1.5);
  const weekPairs = modules.map((mod) => WEEKS[mod] as readonly [number, number]);
  const dominant = weekPairs.reduce((a, b) => (b[1] > a[1] ? b : a));
  const others = weekPairs.filter((w) => w !== dominant);
  const extraLow = others.reduce((s, w) => s + w[0] * 0.45, 0);
  const extraHigh = others.reduce((s, w) => s + w[1] * 0.45, 0);
  const weeksLow = Math.round((dominant[0] + extraLow) * sizeFactor);
  const weeksHigh = Math.round((dominant[1] + extraHigh) * sizeFactor);

  // Impact chips
  const impacts = new Set<string>();
  const hasEnergy = modules.some((m) => ['dak', 'gevel', 'totaal'].includes(m));
  const hasComfort = modules.some((m) => ['interieur', 'totaal'].includes(m));
  const hasExt = modules.includes('uitbreiding');
  if (hasEnergy) {
    impacts.add('tot 30% minder energieverlies');
    impacts.add('sterkere EPC-score');
  }
  if (hasComfort) impacts.add('meer wooncomfort');
  if (hasExt) impacts.add('extra leefruimte');
  impacts.add('hogere woningwaarde');

  return {
    low: totalLow,
    high: totalHigh,
    weeksLow,
    weeksHigh,
    lines,
    impacts: [...impacts].slice(0, 4),
  };
}
