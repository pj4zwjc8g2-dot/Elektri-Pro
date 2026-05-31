import { describe, it, expect } from 'vitest';
import {
  calculatePricing, deriveArea, effectiveModules, RATES, REGION_FACTOR, roundTo500,
} from './pricing';

// helper re-export for test
function r500(n: number) { return Math.round(n / 500) * 500; }

describe('deriveArea', () => {
  it('dak = woonopp * 0.55', () => expect(deriveArea('dak', 100)).toBeCloseTo(55, 5));
  it('gevel = woonopp * 0.9', () => expect(deriveArea('gevel', 100)).toBeCloseTo(90, 5));
  it('interieur = woonopp', () => expect(deriveArea('interieur', 100)).toBe(100));
  it('totaal = woonopp', () => expect(deriveArea('totaal', 100)).toBe(100));
  it('uitbreiding = uitbreidingopp', () => expect(deriveArea('uitbreiding', 100, 30)).toBe(30));
});

describe('effectiveModules', () => {
  it('totaal alone', () => expect(effectiveModules(['totaal'])).toEqual(['totaal']));
  it('totaal supersedes dak/gevel/interieur', () =>
    expect(effectiveModules(['totaal', 'dak', 'interieur'])).toEqual(['totaal']));
  it('totaal + uitbreiding keeps both', () =>
    expect(effectiveModules(['totaal', 'uitbreiding'])).toEqual(['totaal', 'uitbreiding']));
  it('no totaal returns as-is', () =>
    expect(effectiveModules(['dak', 'gevel'])).toEqual(['dak', 'gevel']));
});

describe('calculatePricing — single module dak', () => {
  it('computes correct low/high rounded to 500', () => {
    const res = calculatePricing({ scope: ['dak'], woonopp: 100, niveau: 'essentieel', regio: 'vlb' });
    const area = 55;
    expect(res.lines).toHaveLength(1);
    expect(res.lines[0].area).toBeCloseTo(area, 5);
    expect(res.low).toBe(r500(area * RATES.dak.essentieel[0] * 1));
    expect(res.high).toBe(r500(area * RATES.dak.essentieel[1] * 1));
  });
});

describe('calculatePricing — region factor', () => {
  it('bru is 3% higher than vlb', () => {
    const vlb = calculatePricing({ scope: ['interieur'], woonopp: 100, niveau: 'comfort', regio: 'vlb' });
    const bru = calculatePricing({ scope: ['interieur'], woonopp: 100, niveau: 'comfort', regio: 'bru' });
    expect(bru.low).toBeGreaterThanOrEqual(vlb.low);
  });
  it('wab is cheaper than vlb', () => {
    const vlb = calculatePricing({ scope: ['gevel'], woonopp: 100, niveau: 'comfort', regio: 'vlb' });
    const wab = calculatePricing({ scope: ['gevel'], woonopp: 100, niveau: 'comfort', regio: 'wab' });
    expect(wab.low).toBeLessThanOrEqual(vlb.low);
  });
});

describe('calculatePricing — totaal supersedes', () => {
  it('totaal+dak = totaal only', () => {
    const combined = calculatePricing({ scope: ['totaal', 'dak'], woonopp: 100, niveau: 'comfort', regio: 'vlb' });
    const totaalOnly = calculatePricing({ scope: ['totaal'], woonopp: 100, niveau: 'comfort', regio: 'vlb' });
    expect(combined.low).toBe(totaalOnly.low);
    expect(combined.high).toBe(totaalOnly.high);
  });
  it('totaal + uitbreiding adds both', () => {
    const totaal = calculatePricing({ scope: ['totaal'], woonopp: 100, niveau: 'comfort', regio: 'vlb' });
    const withExt = calculatePricing({ scope: ['totaal', 'uitbreiding'], woonopp: 100, uitbreidingopp: 30, niveau: 'comfort', regio: 'vlb' });
    expect(withExt.low).toBeGreaterThan(totaal.low);
  });
});

describe('calculatePricing — doorlooptijd', () => {
  it('returns positive week range', () => {
    const res = calculatePricing({ scope: ['totaal'], woonopp: 130, niveau: 'comfort', regio: 'vlb' });
    expect(res.weeksLow).toBeGreaterThan(0);
    expect(res.weeksHigh).toBeGreaterThan(res.weeksLow);
  });
  it('sizeFactor clamps: small house (60m²) ≥ 0.8 of baseline', () => {
    const small = calculatePricing({ scope: ['interieur'], woonopp: 60, niveau: 'comfort', regio: 'vlb' });
    const base = calculatePricing({ scope: ['interieur'], woonopp: 130, niveau: 'comfort', regio: 'vlb' });
    expect(small.weeksLow).toBeLessThanOrEqual(base.weeksLow);
  });
});

describe('calculatePricing — impacts', () => {
  it('dak scope includes energy impacts', () => {
    const res = calculatePricing({ scope: ['dak'], woonopp: 100, niveau: 'essentieel', regio: 'vlb' });
    expect(res.impacts).toContain('tot 30% minder energieverlies');
    expect(res.impacts).toContain('hogere woningwaarde');
  });
  it('uitbreiding scope includes extra leefruimte', () => {
    const res = calculatePricing({ scope: ['uitbreiding'], woonopp: 100, uitbreidingopp: 30, niveau: 'essentieel', regio: 'vlb' });
    expect(res.impacts).toContain('extra leefruimte');
  });
  it('max 4 impacts', () => {
    const res = calculatePricing({ scope: ['totaal', 'uitbreiding'], woonopp: 150, uitbreidingopp: 25, niveau: 'comfort', regio: 'vlb' });
    expect(res.impacts.length).toBeLessThanOrEqual(4);
  });
});
