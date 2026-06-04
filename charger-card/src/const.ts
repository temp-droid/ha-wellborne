import type { WellborneCardConfig } from './types.js';

export const CARD_TAG = 'wellborne-charger-card';
export const EDITOR_TAG = 'wellborne-charger-card-editor';
export const CARD_VERSION = '1.0.0';

// Integration domain (custom_components/wellborne/const.py -> DOMAIN).
export const WELLBORNE_DOMAIN = 'wellborne';

// Logical card binding -> Wellborne entity unique_id suffix (the `key` in the
// platform EntityDescription). unique_id pattern = `${charger_id}_${key}`
// (see custom_components/wellborne/sensor/__init__.py::WellborneSensor.__init__
//  and entity/base.py). The entity_id slug itself is built from the *translated
// name* (e.g. sensor.<device>_charging_power), so we MUST resolve via the entity
// registry by unique_id, never by guessing the entity_id string.
//
// platform = 'sensor' unless listed in BINARY_KEYS below.
export const ENTITY_KEYS = {
  // sensor.*_power            (key="power",            name "Charging Power")
  power: 'power',
  // sensor.*_energy           (key="energy",           name "Energy Delivered")
  energy: 'energy',
  // sensor.*_current          (key="current",          name "Current L1")
  current: 'current',
  // sensor.*_max_current      (key="max_current",      name "Max Current") — configured limit (A)
  max_current: 'max_current',
  // sensor.*_session_duration (key="session_duration", name "Session Duration")
  session_duration: 'session_duration',
  // sensor.*_status           (key="status",           name "Status", enum: idle|charging|pending)
  status: 'status',
  // sensor.*_added_range      (key="added_range",      name "Added Range")
  added_range: 'added_range',
  // sensor.*_monthly_energy   (key="monthly_energy",   name "Monthly Energy")
  monthly_energy: 'monthly_energy',
  // sensor.*_yearly_energy    (key="yearly_energy",    name "Yearly Energy")
  yearly_energy: 'yearly_energy',
  // sensor.*_last_session_energy   (key="last_session_energy",   name "Last Session Energy")
  last_session_energy: 'last_session_energy',
  // sensor.*_last_session_duration (key="last_session_duration", name "Last Session Duration")
  last_session_duration: 'last_session_duration',
  // sensor.*_session_cost   (key="session_cost", name "Session Cost") — live session cost (€) from SSE
  session_cost: 'session_cost',
  // sensor.*_wifi_ssid        (key="wifi_ssid", name "WiFi Network") — DISABLED by default
  wifi_ssid: 'wifi_ssid',
  // binary_sensor.*_charging          (key="charging",          name "Charging")
  charging: 'charging',
  // binary_sensor.*_charger_online    (key="charger_online",    name "Charger Online")
  charger_online: 'charger_online',
  // binary_sensor.*_vehicle_connected (key="vehicle_connected", name "Vehicle Connected") — UNKNOWN when idle
  vehicle_connected: 'vehicle_connected',
} as const;

export type EntityKey = keyof typeof ENTITY_KEYS;

// Which logical keys live on the binary_sensor platform (everything else = sensor).
export const BINARY_KEYS: ReadonlySet<EntityKey> = new Set([
  'charging',
  'charger_online',
  'vehicle_connected',
]);

export const UNAVAILABLE_STATES: ReadonlySet<string> = new Set([
  'unavailable',
  'unknown',
  'none',
  '',
]);

export const PLACEHOLDER = '—';

export const DEFAULT_CONFIG: Partial<WellborneCardConfig> = {
  show_curve: true,
  show_totals: true,
  show_cost: true,
  curve_hours: 4,
};
