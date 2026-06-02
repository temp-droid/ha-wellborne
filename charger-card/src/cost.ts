import { UNAVAILABLE_STATES } from './const.js';
import type { HomeAssistant, WellborneCardConfig } from './types.js';

export type PriceSource = 'static' | 'CREG' | 'energy-prefs';

export interface ResolvedPrice {
  /** €/kWh */
  price: number;
  source: PriceSource;
}

/**
 * Resolve a €/kWh price following the doc's chain (first non-null wins):
 *  1. price_entity (normalize €/kWh | €/MWh | €/Wh -> €/kWh)
 *  2. price (static)
 *  3. use_energy_prefs -> WS energy/get_prefs -> grid flow_from price
 *  4. null -> caller hides the cost block
 */
export async function resolvePrice(
  hass: HomeAssistant,
  config: WellborneCardConfig,
): Promise<ResolvedPrice | null> {
  const fromEntity = priceFromEntity(hass, config.price_entity);
  if (fromEntity !== null) {
    return { price: fromEntity, source: 'CREG' };
  }

  if (typeof config.price === 'number' && Number.isFinite(config.price) && config.price > 0) {
    return { price: config.price, source: 'static' };
  }

  if (config.use_energy_prefs) {
    const fromPrefs = await priceFromEnergyPrefs(hass);
    if (fromPrefs !== null) {
      return { price: fromPrefs, source: 'energy-prefs' };
    }
  }

  return null;
}

/** Read a price entity and normalize its unit to €/kWh. */
export function priceFromEntity(hass: HomeAssistant, entityId?: string): number | null {
  if (!entityId) {
    return null;
  }
  const st = hass.states[entityId];
  if (!st || UNAVAILABLE_STATES.has(st.state)) {
    return null;
  }
  const raw = Number(st.state);
  if (!Number.isFinite(raw)) {
    return null;
  }
  const unit = String(st.attributes.unit_of_measurement ?? '').toLowerCase();
  return normalizeToKwh(raw, unit);
}

/** Normalize €/MWh and €/Wh to €/kWh; default assume already €/kWh. */
export function normalizeToKwh(value: number, unit: string): number {
  const u = unit.replace(/\s+/g, '');
  if (u.includes('/mwh')) {
    return value / 1000;
  }
  if (u.includes('/wh') && !u.includes('/kwh')) {
    return value * 1000;
  }
  return value; // €/kWh or unitless
}

interface EnergyPrefs {
  energy_sources?: Array<{
    type?: string;
    flow_from?: Array<{
      entity_energy_price?: string | null;
      number_energy_price?: number | null;
    }>;
  }>;
}

async function priceFromEnergyPrefs(hass: HomeAssistant): Promise<number | null> {
  let prefs: EnergyPrefs;
  try {
    prefs = await hass.callWS<EnergyPrefs>({ type: 'energy/get_prefs' });
  } catch {
    return null;
  }
  const grid = prefs.energy_sources?.find((s) => s.type === 'grid');
  const flow = grid?.flow_from?.[0];
  if (!flow) {
    return null;
  }
  if (flow.entity_energy_price) {
    const st = hass.states[flow.entity_energy_price];
    if (st && !UNAVAILABLE_STATES.has(st.state)) {
      const n = Number(st.state);
      if (Number.isFinite(n)) {
        return n;
      }
    }
  }
  if (typeof flow.number_energy_price === 'number' && Number.isFinite(flow.number_energy_price)) {
    return flow.number_energy_price;
  }
  return null;
}

/** cost = kWh * €/kWh; returns null when energy is missing. */
export function computeCost(energyKwh: number | null, price: number): number | null {
  if (energyKwh === null || !Number.isFinite(energyKwh)) {
    return null;
  }
  return energyKwh * price;
}

export function formatCurrency(hass: HomeAssistant, config: WellborneCardConfig, amount: number): string {
  const currency = config.currency ?? hass.config.currency ?? 'EUR';
  try {
    return new Intl.NumberFormat(hass.locale.language, {
      style: 'currency',
      currency,
    }).format(amount);
  } catch {
    return `${amount.toFixed(2)} ${currency}`;
  }
}

export function sourceLabel(source: PriceSource): string {
  return source;
}
