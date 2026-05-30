# Wellborne/ATESS EV Charger API Documentation

Documents the Wellborne/ATESS cloud API as used by the official Wellborne Plus mobile app (v1.0.4). This integration is unofficial and not affiliated with Wellborne or ATESS — see the project [Disclaimer](../README.md#disclaimer).

## Overview

| Property | Value |
|----------|-------|
| **Base URL** | `https://enerace-fr-api.atesspower.com/v1` |
| **Protocol** | HTTPS REST API |
| **Auth** | JWT Bearer Token |
| **Content-Type** | `application/json; charset=UTF-8` |
| **Real-time** | OCPP over WebSocket (separate connection) |

## Authentication

### Headers (Required for all requests)

```http
Authorization: Bearer <token>
Content-Type: application/json; charset=UTF-8
Accept-Language: en-US
phoneModel: SM-S928B
appVersion: 1.0.4
appOS: android
User-Agent: okhttp/4.8.0
```

### Password Hashing

Passwords are sent as **MD5 hash** (lowercase hex):
```python
import hashlib
password_hash = hashlib.md5("your_password".encode()).hexdigest()
```

---

## Endpoints with Full Parameters

### 1. User Management

#### POST `/user/login`
Authenticate and get JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "md5_hash_of_password",
  "phoneOs": "0",
  "phoneModel": "samsung",
  "appVersion": "1.0.4"
}
```

**Response:**
```json
{
  "result": 0,
  "msg": "Login successful",
  "obj": {
    "id": 12345,
    "email": "user@example.com",
    "country": "Example Country",
    "timezone": "Region/City(UTC+00:00)",
    "installerCode": "",
    "token": "Bearer eyJhbGciOiJIUzUxMiJ9...",
    "address": null,
    "postCode": "0000",
    "detailedAddress": "123 Main Street"
  }
}
```

#### POST `/user/register`
Register new account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "md5_hash_of_password",
  "passwordAgain": "md5_hash_of_password",
  "country": "Example Country",
  "installerCode": "",
  "verificationCode": "123456",
  "timezoneId": 123,
  "detailedAddress": "123 Main St",
  "postCode": "0000"
}
```

#### POST `/user/sendEmailCode`
Send email verification code.

**Request:**
```json
{
  "email": "user@example.com"
}
```

#### POST `/user/logout`
End session.

**Request:**
```json
{}
```

#### POST `/user/updatePostCodeAndAddress`
Update user address.

**Request:**
```json
{
  "postCode": "0000",
  "detailedAddress": "123 Main St"
}
```

---

### 2. Charger Management

#### POST `/charger/chargerList`
List all user's chargers.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "result": 0,
  "msg": "operate successfully",
  "obj": [
    {
      "owner": 1,
      "isVa1NovoNano": false,
      "createTime": "2024-10-18 16:47:07",
      "bluetoothEnable": 0,
      "chargerId": "ABC1234567",
      "connectorStandard": {"country": "", "connector": ""},
      "connectorModel": ["AC"],
      "alias": "Demo Charger",
      "model": "AC",
      "connectorNum": 1,
      "chargePointModelPower": 22
    }
  ]
}
```

#### POST `/charger/addChargerV2`
Bind/add a new charger.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/charger/isCharging`
Check if currently charging.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/charger/unlockConnector`
Unlock the connector.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

---

### 3. Charging Control

#### POST `/transaction/remoteStartTransaction`
**Start charging session.**

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1"
}
```

#### POST `/transaction/remoteStopTransaction`
**Stop charging session.**

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1"
}
```

#### POST `/promptCharge`
Immediate/quick charge (bypasses delay).

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1"
}
```

---

### 4. Meter Values & Transaction History

#### POST `/meterValue/getValues`
**Get real-time meter data during charging.**

**IMPORTANT:** Requires `transactionId`, NOT `chargerId`!

**Request:**
```json
{
  "transactionId": "12345"
}
```

**Response (ChargingData):**
```json
{
  "result": 0,
  "obj": [
    {
      "chargerId": "ABC1234567",
      "current": 16.5,
      "currentL2": 16.4,
      "currentL3": 16.3,
      "voltage": 230.1,
      "voltageL2": 230.2,
      "voltageL3": 230.0,
      "energy": 12.5,
      "phase": "3-phase",
      "time": "2024-01-10 12:30:00"
    }
  ]
}
```

#### POST `/transaction/transactionList`
Get paginated transaction history.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "pageNum": "1",
  "pageSize": "20",
  "startDate": "2024-01-01"
}
```

#### POST `/transaction/transactionRecordMonth`
Get monthly charging records.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "date": "2024-01"
}
```

#### POST `/transaction/transactionRecordYear`
Get yearly charging records.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "date": "2024"
}
```

#### POST `/transaction/sendDownloadEmail`
Email transaction records.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "email": "user@example.com"
}
```

---

### 5. Charger Configuration

#### POST `/getConfiguration/getChargerConfiguration`
Get full charger configuration.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/getConfiguration/getHomeConfig`
Get delayed charging & solar mode settings.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

**Response:**
```json
{
  "result": 0,
  "obj": {
    "delayedCharging": {
      "delayTime": 0,
      "status": 2,
      "chargerId": "ABC1234567",
      "selectStatus": 0
    },
    "solarChargingMode": "0"
  }
}
```

#### POST `/getConfiguration/updateChargerMode`
Update charger operating mode.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "1"
}
```

#### POST `/getConfiguration/updateMaxCurrent`
Set maximum charging current (A).

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "32"
}
```

#### POST `/getConfiguration/updateMaxPower`
Set maximum charging power (kW).

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "power": "22"
}
```

#### POST `/getConfiguration/updateAllowChargingTime`
Set allowed charging time.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "480"
}
```

#### POST `/getConfiguration/saveSolarChargingMode`
Set solar charging mode.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "solarChargingMode": "1"
}
```

Values: `0` = Off, `1` = Eco, `2` = Pure Solar

#### POST `/getConfiguration/updateSolarLimitChargingPower`
Set solar limit charging power.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "6"
}
```

#### POST `/getConfiguration/updateConnectorLock`
Enable/disable connector lock.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "true"
}
```

#### POST `/getConfiguration/updateLcd`
Enable/disable LCD display.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "Enable"
}
```

#### POST `/getConfiguration/updateLowPower`
Enable/disable low power mode.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "Enable"
}
```

#### POST `/getConfiguration/updatePreHeat`
Enable/disable pre-heat function.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "Enable"
}
```

#### POST `/getConfiguration/updateChargeLanguage`
Set charger display language.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "value": "en"
}
```

#### POST `/getConfiguration/getWifiInfo`
Get charger WiFi information.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/getConfiguration/getChargerLanguageList`
Get list of supported languages.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/getConfiguration/getWsList`
Get WebSocket server list.

**Request:**
```json
{}
```

**Response:**
```json
{
  "result": 0,
  "obj": [
    {"id": 49, "value": "ws://charge.wellborneplus.com/ocpp/ws"},
    {"id": 56, "value": "wss://charge.wellborneplus.com:443/ocpp/ws"}
  ]
}
```

---

### 6. Delayed Charging

#### POST `/delayedCharging/getDelayedCharging`
Get delayed charging settings.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1"
}
```

#### POST `/delayedCharging/updateDelayedCharging`
Update delayed charging settings.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "delayTime": "3600",
  "status": 1,
  "selectStatus": 0
}
```

- `delayTime`: Delay in seconds (e.g., "3600" = 1 hour)
- `status`: 1 = enabled, 2 = disabled
- `selectStatus`: 0 = time-based, 1 = off-peak

---

### 7. Scheduled Charging

#### POST `/scheduledChargingTask/getScheduledChargingTask`
Get scheduled charging task.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1"
}
```

#### POST `/scheduledChargingTask/setScheduledByTime`
Schedule charging by duration (minutes).

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1",
  "minute": "60",
  "cycle": "1,2,3,4,5",
  "status": "1",
  "expiryDateType": "1",
  "expiryDate": "2024-12-31",
  "cycleTime": "08:00",
  "connectionType": "1"
}
```

- `minute`: Duration in minutes
- `cycle`: Days of week (1=Mon, 7=Sun), comma-separated
- `expiryDateType`: "1" = no expiry, "2" = has expiry date
- `connectionType`: "1" = when plugged in, "2" = specific time

#### POST `/scheduledChargingTask/setScheduledByFullTime`
Schedule charging until full.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1",
  "cycle": "1,2,3,4,5",
  "status": "1",
  "expiryDateType": "1",
  "expiryDate": "2024-12-31",
  "cycleTime": "08:00",
  "connectionType": "1"
}
```

#### POST `/scheduledChargingTask/setScheduledByEndTime`
Schedule charging until specific end time.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1",
  "cycle": "1,2,3,4,5",
  "status": "1",
  "expiryDateType": "1",
  "expiryDate": "2024-12-31",
  "cycleTime": "08:00",
  "connectionType": "1",
  "endTime": "07:00"
}
```

#### POST `/scheduledChargingTask/setScheduledByElectric`
Schedule charging by energy amount (kWh).

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1",
  "energy": "30",
  "cycle": "1,2,3,4,5",
  "status": "1",
  "expiryDateType": "1",
  "expiryDate": "2024-12-31",
  "cycleTime": "08:00",
  "connectionType": "1"
}
```

#### POST `/scheduledChargingTask/setScheduledByAccount`
Schedule charging by cost amount.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "connectorId": "1",
  "amount": "10",
  "cycle": "1,2,3,4,5",
  "status": "1",
  "expiryDateType": "1",
  "expiryDate": "2024-12-31",
  "cycleTime": "08:00",
  "connectionType": "1"
}
```

---

### 8. Load Balancing

#### POST `/getConfiguration/getLoadBalancing`
Get load balancing settings.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/getConfiguration/setLoadBalancing`
Set load balancing parameters.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "key": "G_ExternalLimitPower",
  "value": "11000"
}
```

Known keys:
- `G_ExternalLimitPowerEnable`: Enable/disable ("0"/"1")
- `G_ExternalLimitPower`: Limit in Watts
- `G_ExternalSamplingCurWring`: Current wiring
- `G_PowerMeterType`: Meter type
- `G_PowerMeterAddr`: Meter address

---

### 9. Time-of-Use Rates

#### POST `/getConfiguration/getTimeRate`
Get time-of-use rate settings.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/getConfiguration/saveTimeRate`
Save time-of-use rates.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "monetaryUnit": "EUR",
  "timeRates": [
    {"startTime": "00:00", "endTime": "06:00", "rate": "0.15"},
    {"startTime": "06:00", "endTime": "22:00", "rate": "0.25"},
    {"startTime": "22:00", "endTime": "00:00", "rate": "0.15"}
  ]
}
```

#### POST `/getConfiguration/saveTimeRateUnit`
Save currency unit only.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "monetaryUnit": "EUR"
}
```

---

### 10. Off-Peak/Peak Valley Charging

#### POST `/v2/getConfiguration/getOffPeakTime`
Get off-peak time settings.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/v2/getConfiguration/setOffPeakTime`
Set off-peak charging times.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "offPeakTimes": [
    {
      "startTime": "22:00",
      "endTime": "06:00",
      "current": "32",
      "dayType": "1"
    }
  ]
}
```

- `dayType`: "1" = weekday, "2" = weekend

#### POST `/v2/getConfiguration/setOffPeakEnable`
Enable off-peak charging with time settings.

**Request:**
```json
{
  "chargerId": "ABC1234567",
  "offPeakTimes": [...]
}
```

#### POST `/v2/getConfiguration/setOffPeakDisable`
Disable off-peak charging.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

---

### 11. Firmware

#### POST `/updateFirmware/getUpdateFirmwareStatus`
Check firmware update status.

**Request:**
```json
{
  "chargerId": "ABC1234567"
}
```

#### POST `/appVersion/getAppVersion`
Get app version info.

**Request:**
```json
{
  "appOS": "Android"
}
```

---

### 12. System

#### POST `/sysTimezone/getCityTimeZone`
Get list of timezones.

**Request:**
```json
{}
```

---

## Response Format

All responses follow this structure:

```json
{
  "result": 0,         // 0 = success, non-zero = error
  "msg": "message",    // Human-readable message
  "obj": { }           // Response data (object, array, or null)
}
```

Alternative format (some endpoints):
```json
{
  "ret": 0,
  "errMsg": "message",
  "data": { }
}
```

---

## WebSocket / OCPP

Real-time charger communication uses **OCPP 1.6** over WebSocket.

**Known WebSocket Servers:**
- `wss://charge.wellborneplus.com:443/ocpp/ws`
- `ws://charge.wellborneplus.com/ocpp/ws`
- `ws://charge.wellborne.fr:80/ocpp/ws`

The charger connects to these servers for:
- Real-time status updates
- Remote start/stop commands
- Meter value streaming

---

## Key Workflow: Getting Meter Values

1. **Login** to get auth token
2. **Get charger list** to find your charger ID
3. **Check isCharging** to see if actively charging
4. **If charging:** Get `transactionId` from transaction list
5. **Call getValues** with `transactionId` to get real-time data

**Important:** `getValues` requires an active `transactionId`, NOT a `chargerId`.

---

## Home Assistant Integration Notes

### Sensors to Create
- **Charging status** (binary_sensor): From isCharging
- **Current power** (W): Calculate from getValues (voltage * current)
- **Energy delivered** (kWh): From getValues
- **Voltage L1/L2/L3** (V): From getValues
- **Current L1/L2/L3** (A): From getValues
- **Connector status**: From charger status

### Services to Create
- `start_charging`: remoteStartTransaction
- `stop_charging`: remoteStopTransaction
- `unlock_connector`: unlockConnector
- `set_max_current`: updateMaxCurrent
- `set_solar_mode`: saveSolarChargingMode

### Polling Strategy
- **Status check**: Every 30-60 seconds via REST API
- **Meter values**: Only when charging is active
- **Configuration**: On-demand or hourly

---

## Discovered From

- **App:** Wellborne Plus v1.0.4 (com.gurui.charge)
- **Manufacturer:** ATESS Power / Project EV
- **Charger Model:** EVA-22S (22kW AC)
- **Charger ID Example:** ABC1234567
- **Date:** January 2025

---

## Python Example

```python
import requests
import hashlib

BASE_URL = "https://enerace-fr-api.atesspower.com/v1"

# Login
password_hash = hashlib.md5("your_password".encode()).hexdigest()
login_response = requests.post(f"{BASE_URL}/user/login", json={
    "email": "your@email.com",
    "password": password_hash,
    "phoneOs": "0",
    "phoneModel": "Python",
    "appVersion": "1.0.0"
})
token = login_response.json()["obj"]["token"]

# Headers for subsequent requests
headers = {
    "Authorization": token,
    "Content-Type": "application/json; charset=UTF-8"
}

# Get charger list
chargers = requests.post(f"{BASE_URL}/charger/chargerList",
    headers=headers,
    json={"email": "your@email.com"}
)
charger_id = chargers.json()["obj"][0]["chargerId"]

# Check charging status
status = requests.post(f"{BASE_URL}/charger/isCharging",
    headers=headers,
    json={"chargerId": charger_id}
)

# Start charging
start = requests.post(f"{BASE_URL}/transaction/remoteStartTransaction",
    headers=headers,
    json={"chargerId": charger_id, "connectorId": "1"}
)

# Stop charging
stop = requests.post(f"{BASE_URL}/transaction/remoteStopTransaction",
    headers=headers,
    json={"chargerId": charger_id, "connectorId": "1"}
)
```
