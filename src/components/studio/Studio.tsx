import { useState, useEffect } from 'preact/hooks';
import './Studio.css';
import type { Module, Level, Region, PricingResult } from '../../lib/pricing';
import { calculatePricing } from '../../lib/pricing';

type Timing = 'asap' | '3m' | '6m' | 'later';

interface StudioStrings {
  step1tag: string; step1h: string; step1lead: string;
  step2tag: string; step2h: string; step2lead: string;
  step3tag: string; step3h: string; step3lead: string;
  step4tag: string; step4h: string; step4lead: string;
  step5tag: string; step5h: string; step5lead: string;
  step6tag: string; step6h: string;
  modules: Record<Module, { label: string; desc: string }>;
  levels: Record<Level, { n: string; label: string; desc: string }>;
  regions: Record<Region, string>;
  timing: Record<Timing, string>;
  dockInvestering: string; dockDoorlooptijd: string;
  dockNiveau: string; dockRegio: string; dockEmpty: string;
  formTitle: string; formLead: string;
  formName: string; formPhone: string; formEmail: string; formAddress: string; formSubmit: string;
  formFeatures: string[];
  successTitle: string; successMsg: string; errorMsg: string;
  disclaimer: string;
  prevBtn: string; nextBtn: string; startBtn: string; backBtn: string;
  weeks: string; weekRange: string;
}

interface StudioProps {
  strings: StudioStrings;
  locale: string;
  leadEndpoint: string;
}

const ALL_MODULES: Module[] = ['totaal', 'dak', 'gevel', 'interieur', 'uitbreiding'];

function fmt(n: number) {
  return new Intl.NumberFormat('nl-BE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
}

function weekRange(low: number, high: number, str: StudioStrings) {
  return str.weekRange.replace('{low}', String(low)).replace('{high}', String(high));
}

export default function Studio({ strings: s, locale, leadEndpoint }: StudioProps) {
  const [step, setStep] = useState(0);
  const [scope, setScope] = useState<Module[]>([]);
  const [woonopp, setWoonopp] = useState(120);
  const [uitbreidingopp, setUitbreidingopp] = useState(25);
  const [niveau, setNiveau] = useState<Level>('comfort');
  const [regio, setRegio] = useState<Region>('vlb');
  const [timing, setTiming] = useState<Timing | null>(null);
  const [pricing, setPricing] = useState<PricingResult | null>(null);

  // Form state
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [honeypot, setHoneypot] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState(false);

  // Recalculate pricing whenever inputs change
  useEffect(() => {
    if (scope.length === 0) { setPricing(null); return; }
    const needsExt = scope.includes('uitbreiding');
    setPricing(calculatePricing({
      scope,
      woonopp,
      uitbreidingopp: needsExt ? uitbreidingopp : 0,
      niveau,
      regio,
    }));
  }, [scope, woonopp, uitbreidingopp, niveau, regio]);

  function toggleModule(mod: Module) {
    setScope(prev => prev.includes(mod) ? prev.filter(m => m !== mod) : [...prev, mod]);
  }

  function goStep(n: number) {
    setStep(n);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function handleStart() {
    goStep(1);
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (honeypot) return;
    if (!name || !email || !email.includes('@')) return;

    setSubmitting(true);
    setSubmitError(false);

    const payload = {
      brand: 'Renov Pro',
      locale,
      timestamp: new Date().toISOString(),
      contact: { name, phone, email, address },
      project: {
        scope,
        woonopp,
        uitbreidingopp: scope.includes('uitbreiding') ? uitbreidingopp : undefined,
        niveau,
        regio,
        timing: timing ?? '',
      },
      estimate: pricing ? {
        currency: 'EUR',
        low: pricing.low,
        high: pricing.high,
        weeksLow: pricing.weeksLow,
        weeksHigh: pricing.weeksHigh,
        lines: pricing.lines,
      } : null,
      meta: { source: 'projectstudio', referrer: document.referrer, userAgent: navigator.userAgent },
    };

    try {
      const res = await fetch(leadEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error();
      setSubmitted(true);
    } catch {
      setSubmitError(true);
    } finally {
      setSubmitting(false);
    }
  }

  const showExt = scope.includes('uitbreiding') && !scope.includes('totaal');

  // Dock values
  const levelLabel = s.levels[niveau].label;
  const regionLabel = s.regions[regio];

  return (
    <div class="studio">
      {/* Live pricing dock */}
      {step > 0 && (
        <div class="dock">
          <div class="dock__item">
            <span class="dock__label">{s.dockInvestering}</span>
            <span class="dock__value dock__value--price">
              {pricing ? `${fmt(pricing.low)} – ${fmt(pricing.high)}` : s.dockEmpty}
            </span>
          </div>
          <div class="dock__divider" />
          <div class="dock__item">
            <span class="dock__label">{s.dockDoorlooptijd}</span>
            <span class="dock__value">
              {pricing ? weekRange(pricing.weeksLow, pricing.weeksHigh, s) : s.dockEmpty}
            </span>
          </div>
          <div class="dock__divider" />
          <div class="dock__item">
            <span class="dock__label">{s.dockNiveau}</span>
            <span class="dock__value">{levelLabel}</span>
          </div>
          <div class="dock__divider" />
          <div class="dock__item">
            <span class="dock__label">{s.dockRegio}</span>
            <span class="dock__value">{regionLabel}</span>
          </div>
        </div>
      )}

      <div class="studio__body">
        {/* Step 0 — intro */}
        {step === 0 && (
          <div class="studio__step studio__step--intro">
            <span class="studio-tag">{s.step1tag.split('—')[0].trim()}</span>
            <button class="btn-start" onClick={handleStart}>
              {s.startBtn} →
            </button>
          </div>
        )}

        {/* Step 1 — scope */}
        {step === 1 && (
          <div class="studio__step">
            <p class="step-tag">{s.step1tag}</p>
            <h2>{s.step1h}</h2>
            <p class="step-lead">{s.step1lead}</p>
            <div class="module-grid">
              {ALL_MODULES.map(mod => (
                <button
                  key={mod}
                  class={`module-card ${scope.includes(mod) ? 'module-card--active' : ''} ${mod === 'totaal' ? 'module-card--featured' : ''}`}
                  onClick={() => toggleModule(mod)}
                  aria-pressed={scope.includes(mod)}
                >
                  <span class="module-card__label">{s.modules[mod].label}</span>
                  <span class="module-card__desc">{s.modules[mod].desc}</span>
                </button>
              ))}
            </div>
            <div class="step-nav">
              <button
                class="btn-primary"
                disabled={scope.length === 0}
                onClick={() => goStep(2)}
              >
                {s.nextBtn} →
              </button>
            </div>
          </div>
        )}

        {/* Step 2 — surface */}
        {step === 2 && (
          <div class="studio__step">
            <p class="step-tag">{s.step2tag}</p>
            <h2>{s.step2h}</h2>
            <p class="step-lead">{s.step2lead}</p>

            <div class="slider-block">
              <div class="slider-header">
                <label for="woonopp-slider">{s.woonoppLabel}</label>
                <span class="slider-value">{woonopp} m²</span>
              </div>
              <input
                id="woonopp-slider"
                type="range"
                min={40} max={400} step={5}
                value={woonopp}
                onInput={(e) => setWoonopp(Number((e.target as HTMLInputElement).value))}
              />
              <p class="slider-note">{s.woonoppNote}</p>
            </div>

            {showExt && (
              <div class="slider-block">
                <div class="slider-header">
                  <label for="ext-slider">{s.uitbreidingoppLabel}</label>
                  <span class="slider-value">{uitbreidingopp} m²</span>
                </div>
                <input
                  id="ext-slider"
                  type="range"
                  min={10} max={150} step={5}
                  value={uitbreidingopp}
                  onInput={(e) => setUitbreidingopp(Number((e.target as HTMLInputElement).value))}
                />
              </div>
            )}

            <div class="step-nav">
              <button class="btn-ghost" onClick={() => goStep(1)}>{s.prevBtn}</button>
              <button class="btn-primary" onClick={() => goStep(3)}>{s.nextBtn} →</button>
            </div>
          </div>
        )}

        {/* Step 3 — niveau */}
        {step === 3 && (
          <div class="studio__step">
            <p class="step-tag">{s.step3tag}</p>
            <h2>{s.step3h}</h2>
            <p class="step-lead">{s.step3lead}</p>
            <div class="level-grid">
              {(['essentieel', 'comfort', 'exclusief'] as Level[]).map(lv => (
                <button
                  key={lv}
                  class={`level-card ${niveau === lv ? 'level-card--active' : ''}`}
                  onClick={() => setNiveau(lv)}
                  aria-pressed={niveau === lv}
                >
                  <span class="level-card__n">{s.levels[lv].n}</span>
                  <span class="level-card__label">{s.levels[lv].label}</span>
                  <span class="level-card__desc">{s.levels[lv].desc}</span>
                </button>
              ))}
            </div>
            <div class="step-nav">
              <button class="btn-ghost" onClick={() => goStep(2)}>{s.prevBtn}</button>
              <button class="btn-primary" onClick={() => goStep(4)}>{s.nextBtn} →</button>
            </div>
          </div>
        )}

        {/* Step 4 — region */}
        {step === 4 && (
          <div class="studio__step">
            <p class="step-tag">{s.step4tag}</p>
            <h2>{s.step4h}</h2>
            <p class="step-lead">{s.step4lead}</p>
            <div class="region-grid">
              {(['vlb', 'bru', 'wab'] as Region[]).map(r => (
                <button
                  key={r}
                  class={`region-card ${regio === r ? 'region-card--active' : ''}`}
                  onClick={() => setRegio(r)}
                  aria-pressed={regio === r}
                >
                  {s.regions[r]}
                </button>
              ))}
            </div>
            <div class="step-nav">
              <button class="btn-ghost" onClick={() => goStep(3)}>{s.prevBtn}</button>
              <button class="btn-primary" onClick={() => goStep(5)}>{s.nextBtn} →</button>
            </div>
          </div>
        )}

        {/* Step 5 — timing */}
        {step === 5 && (
          <div class="studio__step">
            <p class="step-tag">{s.step5tag}</p>
            <h2>{s.step5h}</h2>
            <p class="step-lead">{s.step5lead}</p>
            <div class="timing-grid">
              {(['asap', '3m', '6m', 'later'] as Timing[]).map(tm => (
                <button
                  key={tm}
                  class={`timing-card ${timing === tm ? 'timing-card--active' : ''}`}
                  onClick={() => setTiming(tm)}
                  aria-pressed={timing === tm}
                >
                  {s.timing[tm]}
                </button>
              ))}
            </div>
            <div class="step-nav">
              <button class="btn-ghost" onClick={() => goStep(4)}>{s.prevBtn}</button>
              <button
                class="btn-primary"
                disabled={timing === null}
                onClick={() => { goStep(6); pushEvent('estimate_view', { locale }); }}
              >
                {s.nextBtn} →
              </button>
            </div>
          </div>
        )}

        {/* Step 6 — result + form */}
        {step === 6 && (
          <div class="studio__step">
            <p class="step-tag">{s.step6tag}</p>
            <h2>{s.step6h}</h2>

            {pricing && (
              <div class="result-card">
                <div class="result-card__main">
                  <div class="result-metric">
                    <span class="result-metric__label">{s.dockInvestering}</span>
                    <span class="result-metric__value">{fmt(pricing.low)} – {fmt(pricing.high)}</span>
                  </div>
                  <div class="result-metric">
                    <span class="result-metric__label">{s.dockDoorlooptijd}</span>
                    <span class="result-metric__value">{weekRange(pricing.weeksLow, pricing.weeksHigh, s)}</span>
                  </div>
                </div>
                <div class="result-card__impacts">
                  {pricing.impacts.map(imp => (
                    <span key={imp} class="impact-chip">{imp}</span>
                  ))}
                </div>
                <p class="disclaimer">{s.disclaimer}</p>
              </div>
            )}

            {submitted ? (
              <div class="success-block">
                <h3>{s.successTitle}</h3>
                <p>{s.successMsg}</p>
                <button class="btn-ghost" onClick={() => { setStep(0); setScope([]); setSubmitted(false); }}>
                  ← {s.backBtn}
                </button>
              </div>
            ) : (
              <form class="lead-form" onSubmit={handleSubmit} noValidate>
                <h3>{s.formTitle}</h3>
                <p class="lead-form__lead">{s.formLead}</p>

                <input type="text" name="hp" class="honeypot" tabIndex={-1} value={honeypot} onInput={e => setHoneypot((e.target as HTMLInputElement).value)} />

                <div class="lead-form__grid">
                  <div class="field">
                    <label>{s.formName} *</label>
                    <input type="text" required value={name} onInput={e => setName((e.target as HTMLInputElement).value)} autocomplete="name" />
                  </div>
                  <div class="field">
                    <label>{s.formPhone}</label>
                    <input type="tel" value={phone} onInput={e => setPhone((e.target as HTMLInputElement).value)} autocomplete="tel" />
                  </div>
                  <div class="field field--full">
                    <label>{s.formEmail} *</label>
                    <input type="email" required value={email} onInput={e => setEmail((e.target as HTMLInputElement).value)} autocomplete="email" />
                  </div>
                  <div class="field field--full">
                    <label>{s.formAddress}</label>
                    <input type="text" value={address} onInput={e => setAddress((e.target as HTMLInputElement).value)} autocomplete="address-level2" />
                  </div>
                </div>

                <div class="lead-form__footer">
                  <button type="submit" class="btn-primary" disabled={submitting}>
                    {submitting ? '…' : `${s.formSubmit} →`}
                  </button>
                  <ul class="form-features">
                    {s.formFeatures.map(f => <li key={f}>✓ {f}</li>)}
                  </ul>
                </div>

                {submitError && <p class="form-error">{s.errorMsg}</p>}
              </form>
            )}

            <button class="btn-ghost btn-back" onClick={() => goStep(5)}>← {s.prevBtn}</button>
          </div>
        )}
      </div>
    </div>
  );
}
