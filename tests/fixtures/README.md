# API Response Fixtures

These JSON files are **representative example responses** that match the real Wellborne/ATESS API response shapes. All identifiers and values are synthetic/anonymized. Use these as reference when writing tests to ensure mocks match actual API behavior.

## Important Notes

1. **Use these exact formats in tests** - Don't simplify or assume field names
2. **Field names matter** - e.g., `transactionId` not `id`, `energyKWH` not `energy`
3. **Response wrappers matter** - e.g., transaction list uses `{obj: {dataList: [...]}}` not `{obj: [...]}`

## Files

| File | Endpoint | Notes |
|------|----------|-------|
| `charger_list.json` | `/v1/charger/chargerList` | List of user's chargers |
| `charger_configuration.json` | `/v1/getConfiguration/getChargerConfiguration` | Charger settings |
| `home_config.json` | `/v1/getConfiguration/getHomeConfig` | Delayed charging & solar mode |
| `transaction_list.json` | `/v1/transaction/transactionList` | Paginated with `dataList` wrapper |
| `off_peak_time.json` | `/v2/getConfiguration/getOffPeakTime` | Note: v2 endpoint |
| `delayed_charging.json` | `/v1/delayedCharging/getDelayedCharging` | Delay settings |
| `scheduled_charging.json` | `/v1/scheduledChargingTask/getScheduledChargingTask` | Schedule settings |
| `wifi_info.json` | `/v1/getConfiguration/getWifiInfo` | Uses `wifiSsid` not `ssid` |
| `load_balancing.json` | `/v1/getConfiguration/getLoadBalancing` | External meter data |
| `firmware_status.json` | `/v1/updateFirmware/getUpdateFirmwareStatus` | May return `obj: null` |

## Common Gotchas

### Transaction List
- Response is paginated: `{obj: {pageNow, pageTotal, dataList: [...]}}`
- Fields: `transactionId`, `energyKWH`, `startDate`, `startTime`, `stopTime`, `chargingTime`
- NOT: `id`, `energy`, `startTime` (as datetime), `endTime`

### Monthly/Yearly Stats
- Parameter must be `date`, not `month`/`year`
- Monthly: `{"chargerId": "...", "date": "2026-01"}`
- Yearly: `{"chargerId": "...", "date": "2026"}`

### Off-Peak Settings
- Uses `offPeakEnable: "Enable"/"Disable"` not `status: 0/1`
- Times in `offPeakTimes` array, not flat fields

### WiFi Info
- Field is `wifiSsid`, not `ssid`
- No `signal` field in response
