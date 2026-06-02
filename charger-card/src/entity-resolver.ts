import { BINARY_KEYS, ENTITY_KEYS, WELLBORNE_DOMAIN } from './const.js';
import type { EntityKey } from './const.js';
import type { HomeAssistant, WellborneCardConfig } from './types.js';

export type ResolvedEntities = Partial<Record<EntityKey, string>>;

/**
 * Resolve all logical card bindings to concrete entity_ids.
 *
 * Strategy (most -> least specific):
 *  1. Explicit per-key override in config (`<key>_entity`).
 *  2. Auto-discovery from `device:` via the entity registry. We read the
 *     Wellborne charger_id from the device's identifiers, then exact-match each
 *     binding's unique_id = `${chargerId}_${key}`. Exact match avoids the
 *     `current` vs `max_current` / `household_current_l1` suffix collision.
 *
 * If the entity registry isn't populated (older HA / preview harness), we fall
 * back to a heuristic entity_id suffix scan over `hass.states`.
 */
export function resolveEntities(hass: HomeAssistant, config: WellborneCardConfig): ResolvedEntities {
  const out: ResolvedEntities = {};
  const keys = Object.keys(ENTITY_KEYS) as EntityKey[];

  // 1) explicit overrides win for every key.
  for (const key of keys) {
    const override = config[`${key}_entity`];
    if (typeof override === 'string' && override.length > 0) {
      out[key] = override;
    }
  }

  if (!config.device) {
    return out;
  }

  const chargerId = chargerIdForDevice(hass, config.device);

  // 2a) registry-based exact unique_id match (the correct path in real HA).
  if (hass.entities && chargerId) {
    for (const entry of Object.values(hass.entities)) {
      if (entry.device_id !== config.device) {
        continue;
      }
      if (entry.platform !== WELLBORNE_DOMAIN) {
        continue;
      }
      if (!entry.unique_id) {
        continue;
      }
      for (const key of keys) {
        if (out[key]) {
          continue;
        }
        if (entry.unique_id === `${chargerId}_${ENTITY_KEYS[key]}`) {
          out[key] = entry.entity_id;
        }
      }
    }
  }

  // 2b) fallback: registry present but no unique_id, match by device + platform + entity_id suffix.
  if (hass.entities) {
    for (const entry of Object.values(hass.entities)) {
      if (entry.device_id !== config.device) {
        continue;
      }
      assignBySuffix(out, keys, entry.entity_id, entry.platform);
    }
  }

  // 2c) last resort (preview harness / no registry): scan states by entity_id suffix.
  if (!hass.entities) {
    for (const entityId of Object.keys(hass.states)) {
      assignBySuffix(out, keys, entityId);
    }
  }

  return out;
}

function chargerIdForDevice(hass: HomeAssistant, deviceId: string): string | undefined {
  const device = hass.devices?.[deviceId];
  if (!device) {
    return undefined;
  }
  for (const ident of device.identifiers) {
    if (ident[0] === WELLBORNE_DOMAIN) {
      return ident[1];
    }
  }
  return undefined;
}

/**
 * Heuristic suffix assignment. Picks the right platform and guards against the
 * `_current` collision by requiring the segment before `_<key>` not to itself
 * end with another known key fragment ("max", "household_*").
 */
function assignBySuffix(out: ResolvedEntities, keys: EntityKey[], entityId: string, platform?: string): void {
  const dot = entityId.indexOf('.');
  if (dot < 0) {
    return;
  }
  const domain = entityId.slice(0, dot);
  const objectId = entityId.slice(dot + 1);

  for (const key of keys) {
    if (out[key]) {
      continue;
    }
    const wantBinary = BINARY_KEYS.has(key);
    const expectedDomain = wantBinary ? 'binary_sensor' : 'sensor';
    if (domain !== expectedDomain) {
      continue;
    }
    if (platform && platform !== WELLBORNE_DOMAIN) {
      continue;
    }
    const suffix = ENTITY_KEYS[key];
    if (!matchesSuffix(objectId, suffix)) {
      continue;
    }
    out[key] = entityId;
  }
}

function matchesSuffix(objectId: string, suffix: string): boolean {
  if (!objectId.endsWith(`_${suffix}`)) {
    return false;
  }
  const head = objectId.slice(0, objectId.length - suffix.length - 1);
  // Reject collisions: `current` must not match `max_current` / `household_current_l1`.
  if (suffix === 'current' && (head.endsWith('_max') || head.includes('household'))) {
    return false;
  }
  if (suffix === 'energy' && head.endsWith('_last_session')) {
    return false;
  }
  return true;
}
