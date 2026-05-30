# Wellborne EV Charger - Home Assistant Integration

[![Tests](https://github.com/temp-droid/ha-wellborne/actions/workflows/test.yml/badge.svg)](https://github.com/temp-droid/ha-wellborne/actions/workflows/test.yml)
[![Validate](https://github.com/temp-droid/ha-wellborne/actions/workflows/validate.yml/badge.svg)](https://github.com/temp-droid/ha-wellborne/actions/workflows/validate.yml)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant custom integration for Wellborne/ATESS EV chargers.

> **Unofficial integration.** Not affiliated with, endorsed by, or supported by Wellborne or ATESS. It can start/stop charging and change charger settings on real hardware — **use at your own risk**. See the [Disclaimer](#disclaimer).

## Quick Start

1. **Prepare:** Ensure your Wellborne charger is set up in the **Wellborne Plus** mobile app and shows as **online**.
2. **Install:** Open HACS in Home Assistant → Integrations → Custom Repositories → Add `https://github.com/temp-droid/ha-wellborne` as an Integration → Search for "Wellborne EV Charger" → Install.
3. **Restart:** Restart Home Assistant.
4. **Add:** Go to **Settings → Devices & Services → Create Integration** → Search for **Wellborne EV Charger** → Enter your Wellborne Plus email and password.
5. **Done:** The integration creates a device with sensors, switches, buttons, and more for your charger.

## Requirements

- **Home Assistant** 2025.1 or newer
- **HACS** (install via custom repository)
- **Wellborne Plus account** — use the same email and password you use in the mobile app
- **Internet connection** — the integration polls the Wellborne cloud API

## Table of Contents

- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Features](#features)
- [Supported Devices](#supported-devices)
- [Installation](#installation)
- [Configuration](#configuration)
- [Entities](#entities)
- [Energy Dashboard](#energy-dashboard)
- [Services](#services)
- [Troubleshooting](#troubleshooting)
- [Documentation & Advanced Use](#documentation--advanced-use)
- [Reporting Issues](#reporting-issues)
- [Development](#development)
- [Disclaimer](#disclaimer)
- [License](#license)

## Features

- **Real-time monitoring**: Charging status, power, and per-phase voltage/current (live while charging)
- **Energy & statistics**: Current-session energy, monthly and yearly totals (Energy-dashboard ready), and estimated range added
- **Household power monitoring**: Reads the charger's external meter (e.g. Eastron SDM630) used for load balancing
- **Remote control**: Start/stop charging, unlock connector, charge now (bypass delayed charging)
- **Configuration**: Max current, max power, solar charging mode, LCD, low-power reserve, load balancing
- **Scheduling**: Delayed charging, scheduled charging, and off-peak windows

## Supported Devices

- Wellborne EVA-22S and compatible ATESS chargers

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add `https://github.com/temp-droid/ha-wellborne` as an Integration
5. Search for "Wellborne" and install
6. Restart Home Assistant
7. Go to Settings → Devices & Services → Add Integration → Wellborne

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/temp-droid/ha-wellborne/releases)
2. Extract and copy `custom_components/wellborne` to your `config/custom_components/` directory
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration → Wellborne

## Configuration

This is a **cloud-polling** integration — it talks to the Wellborne/ATESS cloud, so
Home Assistant needs internet access and the charger must be online in the app.

### Initial setup

1. Go to **Settings → Devices & Services → Add Integration** and search for **Wellborne**.
2. Enter your **Wellborne Plus app credentials**:
   - **Email** — your Wellborne Plus account email
   - **Password** — your Wellborne Plus account password
3. Submit. The integration validates the credentials against the cloud and creates a
   device with all the entities listed below.

> The same account used by the mobile app is fine — the integration logs in alongside it.

### Options

After setup, open the integration and click **Configure** to adjust:

| Option | Default | Range | What it does |
|--------|---------|-------|--------------|
| **Vehicle Efficiency** (km/kWh) | `6.0` | 3.0–10.0 | Used to compute the *Estimated Range Added* sensor (typically 4–8 km/kWh) |
| **Polling Interval When Charging** (s) | `30` | 10–300 | How often to poll while a session is active |
| **Polling Interval When Idle** (s) | `120` | 30–600 | How often to poll when idle (higher = fewer cloud API calls) |
| **End of Charge Sensor** (optional) | — | any entity | Select your car's "end of charge" sensor to display time remaining |

### Updating credentials

If your password changes, use **Reconfigure** (or the automatic **re-authentication**
prompt) on the integration entry — no need to delete and re-add it.

**Energy dashboard:** to track EV charging over time, add the **Monthly Energy** sensor
as a consumption source — see the [Energy Dashboard](#energy-dashboard) section below.

## Entities

> **Note:** Live meter values (charging power, per-phase voltage/current, session
> energy, session duration, range added) only report **while a vehicle is actively
> charging** — they are `unavailable` when the charger is idle. This is a limitation
> of the cloud API, which only exposes meter data during an active session.

### Sensors
- Charging Power (W) — *live during a session*
- Energy Delivered (kWh) — current session, *live during a session*
- Voltage L1/L2/L3 (V), Current L1/L2/L3 (A) — *live during a session*
- Session Duration (min) — *live during a session*
- Estimated Range Added (km) — uses a configurable efficiency (km/kWh)
- Status (idle / charging / pending)
- Last Session Energy (kWh) / Last Session Duration (min)
- Monthly Energy (kWh) — resets monthly, **Energy-dashboard ready** (see below)
- Yearly Energy (kWh)
- Max Current Setting (A)
- WiFi Network (SSID)
- Household Power (W), Household Current L1/L2/L3 (A), Household Voltage L1/L2/L3 (V) — from the external (load-balancing) meter

### Binary Sensors
- Charging
- Vehicle Connected — *only reports while charging; the API can't detect plug status when idle*
- Charger Online (connectivity)
- Bluetooth Enabled *(disabled by default)*

### Switches
- Charging (Start/Stop)
- Connector Lock
- Delayed Charging
- Scheduled Charging
- Off-Peak Charging
- LCD Display
- Low Power Reserve
- Load Balancing

### Buttons
- Start Charging
- Stop Charging
- Unlock Connector
- Charge Now (bypass delayed charging)

### Numbers
- Maximum Current (A)
- Maximum Power (W)
- Delay Time (min)
- Load Balancing Power (kW)

### Selects
- Solar Charging Mode (Off / Eco / Pure Solar)

### Times
- Off-Peak Weekday Start / End
- Scheduled Start Time

## Energy Dashboard

Add the **Monthly Energy** sensor (`sensor.<name>_monthly_energy`) as a consumption
source under **Settings → Energy**. It comes straight from the charger's cloud
statistics (so it matches your billing) and carries a `last_reset` of the 1st of the
month, which lets Home Assistant track it correctly across month boundaries.

> Statistics are only recorded from the moment you add the sensor — energy charged
> earlier in the current month won't backfill. From the next full month onward,
> totals are complete.

## Services

Most users won't need services — the **Charging** switch, **Start/Stop/Unlock/Charge Now** buttons, and **Maximum Current/Solar Mode** selectors cover the same actions through the UI. Services are mainly for **automations** that need to control charging programmatically.

To use a service in an automation, find your **Charger ID** on the integration's device page (Settings → Devices & Services → select the Wellborne device → look for the charger identifier).

| Service | Description | Parameters |
|---------|-------------|------------|
| `wellborne.start_charging` | Start a charging session | **charger_id** (text, required) — your charger ID |
| `wellborne.stop_charging` | Stop the current charging session | **charger_id** (text, required) — your charger ID |
| `wellborne.set_max_current` | Set the maximum charging current | **charger_id** (text, required), **current** (number, required, 6–32 A) |
| `wellborne.set_solar_mode` | Set the solar charging mode | **charger_id** (text, required), **mode** (select, required) — `off`, `eco`, or `pure_solar` |

## Troubleshooting

### Entities show as `unavailable`

**Live meter values** (charging power, voltage/current, session energy, session duration, range added) only report **while the vehicle is actively charging**. When idle, these sensors are `unavailable` — this is a limitation of the cloud API, which only exposes meter data during an active session. This is normal and expected.

All other entities (status, monthly/yearly energy, settings, etc.) remain available when idle.

### Invalid credentials error during setup

The integration uses the **same credentials as the Wellborne Plus mobile app**:
- Double-check your email and password.
- If you've changed your password in the Wellborne Plus app recently, use **Reconfigure** on the integration entry (or delete and re-add it).
- Ensure you're using the **Wellborne Plus account email**, not a nickname or phone number.

### Charger shows as offline in Home Assistant

- Check the Wellborne Plus mobile app — if the charger is offline there too, it has lost internet or power.
- Ensure Home Assistant has internet access (the integration polls the cloud).
- Try restarting Home Assistant: **Settings → System → Restart**.

### Integration created but no entities appear

- The integration may still be initializing. Wait 30–60 seconds, then refresh Home Assistant.
- Check **Settings → Devices & Services → Wellborne** — click the device to see if any entities are present.
- If the device exists but has no entities, check Home Assistant's logs for errors (Settings → System → Logs).

## Documentation & Advanced Use

For detailed information about the Wellborne/ATESS API (endpoints, request/response format, WebSocket real-time updates), see [docs/WELLBORNE_API.md](docs/WELLBORNE_API.md).

### Region Limitation

This integration currently targets the **France API endpoint** (`enerace-fr-api.atesspower.com`), which is the same region as the official Wellborne Plus app. If you are located outside France or your charger uses a different regional endpoint, the integration may not work correctly — silent authentication failures or connection timeouts are common symptoms. Users in other regions should verify that the Wellborne Plus app uses the same endpoint before installing this integration.

## Reporting Issues

Found a bug or want to request a feature? Visit the [GitHub issue tracker](https://github.com/temp-droid/ha-wellborne/issues) and open an issue. Please include:
- Your Home Assistant version
- Any error messages from the logs (Settings → System → Logs)
- Steps to reproduce the problem

## Development

Contributions are welcome. This project enforces strict quality gates: all changes must pass `ruff`, `pyright`, and the test suite with **≥80% coverage** before merging (`./script/check` runs everything).

### Quick Start

```bash
# Clone the repository
git clone https://github.com/temp-droid/ha-wellborne.git
cd ha-wellborne

# Bootstrap development environment
./script/setup/bootstrap

# Activate virtual environment
source .venv/bin/activate

# Run tests
./script/test

# Run all checks
./script/check
```

### Testing

This project follows **Test-Driven Development (TDD)**: write a failing test first, implement the minimal code to pass, then refactor. New code requires tests, and coverage must stay at or above 80%.

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=custom_components/wellborne --cov-report=term-missing
```

## Disclaimer

This integration is **unofficial** and is **not affiliated with, endorsed by, supported by, or in any way associated with Wellborne, ATESS Power Technology Co., Ltd., or any of their subsidiaries or affiliates.**

"Wellborne" and "ATESS" are trademarks of their respective owners. They are used here solely to identify the hardware and cloud service this integration is compatible with (nominative use). No sponsorship or endorsement is implied.

This integration communicates with the Wellborne/ATESS cloud API (`enerace-fr-api.atesspower.com`), the same service used by the official Wellborne Plus mobile app. The vendor may change or discontinue this API at any time and without notice, which may break the integration. Your use is also subject to the vendor's Terms of Service, and the integration transmits your account credentials and charger data to that cloud service — review the vendor's privacy policy. Accessing this API with unofficial software may be contrary to the vendor's terms; you are responsible for your own compliance, and your account is used at your own risk.

**Use at your own risk.** This software can remotely start and stop charging sessions and change hardware settings (including maximum charging current) on a real EV charger connected to the electrical grid. The authors are **not responsible** for any damage to hardware, vehicles, property, or electrical installations; for energy costs; for data loss; or for any other direct or indirect loss arising from use of (or inability to use) this integration. The software is provided **"AS IS"**, without warranty of any kind — see the [LICENSE](LICENSE) for the full warranty disclaimer and limitation of liability.

This integration is intended for personal, non-commercial, interoperability use only.

## License

MIT License - see [LICENSE](LICENSE) for details.
