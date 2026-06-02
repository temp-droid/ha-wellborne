// Minimal Home Assistant frontend typings — enough for this card, no @types dependency.

export interface HassEntityState {
  entity_id: string;
  state: string;
  attributes: Record<string, unknown> & {
    unit_of_measurement?: string;
    friendly_name?: string;
    device_class?: string;
  };
  last_changed?: string;
  last_updated?: string;
}

export interface HassEntityRegistryEntry {
  entity_id: string;
  device_id: string | null;
  platform: string;
  unique_id?: string;
  disabled_by?: string | null;
}

export interface HassDeviceRegistryEntry {
  id: string;
  name: string | null;
  name_by_user?: string | null;
  identifiers: [string, string][];
}

export interface HomeAssistant {
  states: Record<string, HassEntityState>;
  // Entity registry cache (modern HA exposes this keyed by entity_id).
  entities?: Record<string, HassEntityRegistryEntry>;
  devices?: Record<string, HassDeviceRegistryEntry>;
  config: {
    currency?: string;
  };
  locale: {
    language: string;
  };
  themes?: unknown;
  callApi: <T>(method: string, path: string, parameters?: unknown) => Promise<T>;
  callWS: <T>(msg: Record<string, unknown>) => Promise<T>;
}

export interface WellborneCardConfig {
  type: string;
  device?: string;
  name?: string;

  // Optional explicit entity overrides (per-key). e.g. power_entity, status_entity ...
  [key: `${string}_entity`]: string | undefined;

  // Optional car SoC / range
  battery_entity?: string;
  range_entity?: string;

  // Cost source
  price_entity?: string;
  price?: number;
  use_energy_prefs?: boolean;
  currency?: string;

  // Display toggles
  show_curve?: boolean;
  show_totals?: boolean;
  show_cost?: boolean;
  curve_hours?: number;
}

export type CardState = 'charging' | 'idle' | 'offline';

export interface HistoryPoint {
  t: number; // epoch ms
  v: number; // value (W)
}

// LovelaceCard registration shape used by the picker.
export interface CustomCardEntry {
  type: string;
  name: string;
  description: string;
  preview?: boolean;
  documentationURL?: string;
}

declare global {
  interface Window {
    customCards?: CustomCardEntry[];
  }
}
