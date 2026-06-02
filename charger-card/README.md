# Wellborne Charger Card

A monitoring-focused (read-only) Home Assistant Lovelace card for the
[Wellborne EV charger integration](../custom_components/wellborne). Lit 3 +
TypeScript, bundled to a single file, HACS-installable.

Shows live charging status, WiFi/charger online state, energy totals, an optional
car battery state-of-charge ring, and the **cost of the last charge** derived from
energy × a resolved price.

| Charging | Idle | Offline |
| --- | --- | --- |
| Big live kW + power sparkline (bright leading-edge pulse), SoC ring, chip row | Calm recap of last session, status greys out | Card dims, values become `—`, last-known totals/cost stay |

See `dev/preview.html` for a standalone visual preview (no Home Assistant needed).

---

## Install

### HACS (recommended)

1. HACS → Frontend → ⋮ → Custom repositories → add this repo, category **Lovelace**.
2. Install **Wellborne Charger Card**.
3. HACS adds the resource automatically. (Manual: Settings → Dashboards → ⋮ →
   Resources → add `/hacsfiles/wellborne-charger-card/wellborne-charger-card.js`
   as a **JavaScript Module**.)

### Manual

1. Copy `dist/wellborne-charger-card.js` to `<config>/www/wellborne-charger-card.js`.
2. Add it as a dashboard resource (JavaScript Module): `/local/wellborne-charger-card.js`.

---

## Configuration

Add via the card picker (a GUI editor with a device picker + toggles is included),
or in YAML:

```yaml
type: custom:wellborne-charger-card
device: <your wellborne device id>   # auto-resolves all charger sensors

# --- optional: car battery SoC ring (from your vehicle integration) ---
battery_entity: sensor.ioniq5_battery_level
range_entity: sensor.ioniq5_range        # optional; else uses charger added_range

# --- optional: cost source (resolved in order, first hit wins) ---
price_entity: sensor.wallonia_ev_price   # CREG CSV sensor (recommended, see below)
price: 0.3783                            # static €/kWh fallback
use_energy_prefs: true                   # read HA Energy dashboard price
# currency: EUR                          # default = hass.config.currency

# --- optional display toggles ---
name: "Wellborne Garage"
show_curve: true        # power sparkline hero
show_totals: true       # month/year row
show_cost: true         # last-charge cost block
show_wifi: true         # footer wifi-connected icon (boolean, no SSID name)
curve_hours: 4          # sparkline lookback window
```

Every binding auto-resolves from `device:`. To override one explicitly, set
`<key>_entity:`, e.g. `power_entity: sensor.my_power`.

### Options

| Option | Type | Default | Notes |
| --- | --- | --- | --- |
| `device` | string | — | Wellborne device; auto-resolves all charger entities |
| `battery_entity` | string | — | Car SoC % from your vehicle integration → SoC ring |
| `range_entity` | string | — | Car range; falls back to charger added-range |
| `price_entity` | string | — | €/kWh price entity (normalizes €/MWh, €/Wh) |
| `price` | number | — | Static €/kWh fallback |
| `use_energy_prefs` | bool | `false` | Read the HA Energy dashboard grid price |
| `currency` | string | `hass.config.currency` | ISO currency for cost formatting |
| `name` | string | device name | Card title |
| `show_curve` | bool | `true` | Power sparkline |
| `show_totals` | bool | `true` | Month / year energy totals |
| `show_cost` | bool | `true` | Last-charge cost block |
| `show_wifi` | bool | `true` | Footer WiFi-connected icon |
| `curve_hours` | number | `4` | Sparkline lookback window |

### Cost derivation

`cost = last_session_energy_kWh × resolved_price`, prefixed with `~` and a small
`est. · source:` caption (per-session time-of-use cost cannot be exactly
reconstructed from cumulative kWh sensors). Price resolution order: `price_entity`
→ `price` → `use_energy_prefs` → **hidden** (the cost block disappears rather than
ever showing `€0.00` or `NaN`).

---

## ⚠️ Enable the WiFi sensor

The WiFi indicator reads `sensor.*_wifi_ssid`, which is **disabled by default** in
the integration. To get the WiFi-connected icon: Settings → Devices & Services →
Wellborne → the WiFi Network entity → enable it. The card only uses it as a
boolean (connected = non-empty value); **the SSID name is never displayed**.

`vehicle_connected` reads *unknown* when the charger is idle (REST API
limitation) and is rendered honestly as `—`, never "disconnected".

---

## 📈 Recommended price source — CREG Wallonia CSV

CREG publishes an all-in residential €/kWh price per Belgian region, quarterly, as
a CSV designed for EV home-charging reimbursement:

```
https://www.creg.be/sites/default/files/assets/Prices/CREG_Tariff_EV.csv
```

All-in = energy + transport + distribution + taxes/levies + VAT — do **not** add
grid fees/VAT on top. Wallonia Q2-2026 = **0.3783 €/kWh**.

`examples/creg-price-sensor.yaml` ships a `command_line` sensor that curls the CSV,
handles its quirks (semicolon delimiter, comma decimals, UTF-8 BOM, sparse
"Average 3 months" column), divides c€ by 100 → €/kWh, polls daily, and fails soft
on a 404. A dependency-averse alternative (an `input_number` bumped 4×/year) is in
the same file.

> CWaPE and the social tariff have no machine-readable feed (PDF/comparator only);
> the CREG CSV is the canonical structured source.

---

## Develop / preview

```bash
cd charger-card
npm install
npm run build      # -> dist/wellborne-charger-card.js (Lit bundled in)
npm run typecheck  # tsc --noEmit
```

Open `dev/preview.html` in a browser to see the three states in dark + light
themes with mock data — `file://` works because the bundle is self-contained. If
your browser blocks ES modules over `file://`, run `npx serve .` and open
`http://localhost:3000/dev/preview.html`.

The bundle is ~14 KB gzipped (no chart library — the sparkline is hand-rolled SVG).
```bash
npm run dev        # rebuild on change
```
