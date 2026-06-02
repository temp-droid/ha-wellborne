"""Constants for the Wellborne EV Charger integration."""

from __future__ import annotations

from typing import Final

# Integration domain
DOMAIN: Final = "wellborne"

# API Configuration
# Base URL without version - endpoints include their version prefix
API_BASE_URL: Final = "https://enerace-fr-api.atesspower.com"
API_TIMEOUT: Final = 30
API_USER_AGENT: Final = "okhttp/4.8.0"

# Default values
DEFAULT_SCAN_INTERVAL: Final = 30  # seconds
DEFAULT_VEHICLE_EFFICIENCY: Final = 6.0  # km per kWh
DEFAULT_SCHEDULE_DURATION_MINUTES: Final = 60
DEFAULT_SCHEDULE_CYCLE: Final = "1,2,3,4,5,6,7"
DEFAULT_SCHEDULE_TIME: Final = "22:00"

# Adaptive polling intervals
CHARGING_POLL_INTERVAL: Final = 30  # seconds when charging
IDLE_POLL_INTERVAL: Final = 120  # seconds when idle

# Offline detection
OFFLINE_TIMEOUT_COUNT: Final = 3  # Number of consecutive timeouts before marking offline
CONFIG_REFRESH_INTERVAL: Final = 900  # seconds; rarely-changing config/stats refresh cadence
OFFLINE_POLL_INTERVAL: Final = 300  # seconds; backoff polling cadence while charger is offline

# Coordinator fetch timeout: bounds the entire multi-request charger-data fetch
# (charger list ~30s + meter/config batch ~45s), so must exceed their aggregate worst case.
COORDINATOR_UPDATE_TIMEOUT: Final = 60  # seconds

# Configuration keys
CONF_EMAIL: Final = "email"
CONF_PASSWORD: Final = "password"  # noqa: S105
CONF_CHARGER_ID: Final = "charger_id"
CONF_END_OF_CHARGE_ENTITY: Final = "end_of_charge_entity"
CONF_VEHICLE_EFFICIENCY: Final = "vehicle_efficiency"
CONF_CHARGING_POLL_INTERVAL: Final = "charging_poll_interval"
CONF_IDLE_POLL_INTERVAL: Final = "idle_poll_interval"


# API Endpoints
class Endpoints:
    """API endpoint paths."""

    # User Management (v1)
    LOGIN: Final = "/v1/user/login"
    LOGOUT: Final = "/v1/user/logout"
    REGISTER: Final = "/v1/user/register"
    SEND_EMAIL_CODE: Final = "/v1/user/sendEmailCode"

    # Charger Management (v1)
    CHARGER_LIST: Final = "/v1/charger/chargerList"
    IS_CHARGING: Final = "/v1/charger/isCharging"
    UNLOCK_CONNECTOR: Final = "/v1/charger/unlockConnector"
    ADD_CHARGER: Final = "/v1/charger/addChargerV2"

    # Charging Control (v1)
    REMOTE_START: Final = "/v1/transaction/remoteStartTransaction"
    REMOTE_STOP: Final = "/v1/transaction/remoteStopTransaction"
    PROMPT_CHARGE: Final = "/v1/promptCharge"

    # Meter Values (v1)
    GET_VALUES: Final = "/v1/meterValue/getValues"

    # Transaction History (v1)
    TRANSACTION_LIST: Final = "/v1/transaction/transactionList"
    TRANSACTION_MONTH: Final = "/v1/transaction/transactionRecordMonth"
    TRANSACTION_YEAR: Final = "/v1/transaction/transactionRecordYear"

    # Configuration endpoints (v1)
    GET_CHARGER_CONFIG: Final = "/v1/getConfiguration/getChargerConfiguration"
    GET_HOME_CONFIG: Final = "/v1/getConfiguration/getHomeConfig"
    UPDATE_MAX_CURRENT: Final = "/v1/getConfiguration/updateMaxCurrent"
    UPDATE_MAX_POWER: Final = "/v1/getConfiguration/updateMaxPower"
    SAVE_SOLAR_MODE: Final = "/v1/getConfiguration/saveSolarChargingMode"
    UPDATE_CONNECTOR_LOCK: Final = "/v1/getConfiguration/updateConnectorLock"
    UPDATE_LCD: Final = "/v1/getConfiguration/updateLcd"
    UPDATE_LOW_POWER: Final = "/v1/getConfiguration/updateLowPower"
    GET_WIFI_INFO: Final = "/v1/getConfiguration/getWifiInfo"
    GET_WS_LIST: Final = "/v1/getConfiguration/getWsList"

    # Scheduled Charging (v1)
    GET_SCHEDULED_TASK: Final = "/v1/scheduledChargingTask/getScheduledChargingTask"
    SET_SCHEDULED_BY_TIME: Final = "/v1/scheduledChargingTask/setScheduledByTime"
    SET_SCHEDULED_BY_ENERGY: Final = "/v1/scheduledChargingTask/setScheduledByElectric"
    SET_SCHEDULED_BY_FULL: Final = "/v1/scheduledChargingTask/setScheduledByFullTime"
    SET_SCHEDULED_BY_END_TIME: Final = "/v1/scheduledChargingTask/setScheduledByEndTime"

    # Delayed Charging (v1)
    GET_DELAYED_CHARGING: Final = "/v1/delayedCharging/getDelayedCharging"
    UPDATE_DELAYED_CHARGING: Final = "/v1/delayedCharging/updateDelayedCharging"

    # Load Balancing (v1)
    GET_LOAD_BALANCING: Final = "/v1/getConfiguration/getLoadBalancing"
    SET_LOAD_BALANCING: Final = "/v1/getConfiguration/setLoadBalancing"

    # Time Rates (v1)
    GET_TIME_RATE: Final = "/v1/getConfiguration/getTimeRate"
    SAVE_TIME_RATE: Final = "/v1/getConfiguration/saveTimeRate"

    # Off-Peak Charging (v2)
    GET_OFF_PEAK_TIME: Final = "/v2/getConfiguration/getOffPeakTime"
    SET_OFF_PEAK_TIME: Final = "/v2/getConfiguration/setOffPeakTime"
    SET_OFF_PEAK_ENABLE: Final = "/v2/getConfiguration/setOffPeakEnable"
    SET_OFF_PEAK_DISABLE: Final = "/v2/getConfiguration/setOffPeakDisable"

    # Firmware endpoints (v1)
    GET_FIRMWARE_STATUS: Final = "/v1/updateFirmware/getUpdateFirmwareStatus"

    # System endpoints (v1)
    GET_TIMEZONE: Final = "/v1/sysTimezone/getCityTimeZone"
    GET_APP_VERSION: Final = "/v1/appVersion/getAppVersion"


# Solar Charging Modes
class SolarMode:
    """Solar charging mode values."""

    OFF: Final = "0"
    ECO: Final = "1"
    PURE_SOLAR: Final = "2"


# API value -> Display name (for UI display)
SOLAR_MODE_API_TO_NAME: Final = {
    SolarMode.OFF: "Off",
    SolarMode.ECO: "Eco",
    SolarMode.PURE_SOLAR: "Pure Solar",
}

# Display name -> API value (reverse mapping)
SOLAR_MODE_NAME_TO_API: Final = {v: k for k, v in SOLAR_MODE_API_TO_NAME.items()}

# Service parameter -> API value (for services.yaml lowercase values)
SOLAR_MODE_SERVICE_TO_API: Final = {
    "off": SolarMode.OFF,
    "eco": SolarMode.ECO,
    "pure_solar": SolarMode.PURE_SOLAR,
}


# Delayed Charging Status
class DelayedChargingStatus:
    """Delayed charging status values."""

    ENABLED: Final = 1
    DISABLED: Final = 2


# Scheduled Charging Status
class ScheduledChargingStatus:
    """Scheduled charging status values."""

    ENABLED: Final = "1"
    DISABLED: Final = "2"


# Connection Types for Scheduling
class ConnectionType:
    """Connection type for scheduled charging."""

    WHEN_PLUGGED_IN: Final = "1"
    SPECIFIC_TIME: Final = "2"


# Day Types for Off-Peak
class DayType:
    """Day type for off-peak charging."""

    WEEKDAY: Final = "1"
    WEEKEND: Final = "2"


# API Response codes
class ApiResult:
    """API response result codes."""

    SUCCESS: Final = 0
    SESSION_EXPIRED: Final = 10000  # Account logged in elsewhere


# Platforms
PLATFORMS: Final = [
    "binary_sensor",
    "button",
    "number",
    "select",
    "sensor",
    "switch",
    "time",
]

# Attribution
ATTRIBUTION: Final = "Data provided by Wellborne/ATESS"
