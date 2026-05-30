"""Wellborne/ATESS API Client."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
import hashlib
import logging
from typing import TYPE_CHECKING, Any

import aiohttp

from ..const import API_BASE_URL, API_TIMEOUT, API_USER_AGENT, ApiResult, Endpoints
from .exceptions import ApiConnectionError, ApiResponseError, AuthenticationError, SessionExpiredError, WellborneError

if TYPE_CHECKING:
    from collections.abc import Mapping

_LOGGER = logging.getLogger(__name__)

# Keys whose values must never reach debug logs (credentials / session tokens).
_SENSITIVE_KEYS = frozenset({"password", "token", "wifiPassword"})


def _redact_sensitive(value: Any) -> Any:
    """Recursively mask sensitive values so debug logs never leak secrets."""
    if isinstance(value, dict):
        return {key: ("***" if key in _SENSITIVE_KEYS else _redact_sensitive(val)) for key, val in value.items()}
    if isinstance(value, list):
        return [_redact_sensitive(item) for item in value]
    return value


@dataclass(slots=True, kw_only=True)
class ChargerInfo:
    """Charger information from the API."""

    charger_id: str
    alias: str
    model: str
    owner: int
    connector_num: int
    max_power: float
    bluetooth_enabled: bool = False
    create_time: str = ""


@dataclass(slots=True, kw_only=True)
class ChargerStatus:
    """Charger status data."""

    is_charging: bool = False
    solar_mode: str = "0"
    max_current: float = 32.0
    max_power: int = 22000  # Maximum power limit in Watts
    connector_lock: bool = False
    lcd_enabled: bool = True
    low_power_reserve: bool = False


@dataclass(slots=True, kw_only=True)
class MeterValues:
    """Real-time meter values during charging."""

    voltage: float = 0.0
    voltage_l2: float = 0.0
    voltage_l3: float = 0.0
    current: float = 0.0
    current_l2: float = 0.0
    current_l3: float = 0.0
    energy: float = 0.0
    power: float = 0.0
    phase: str = "1-phase"
    timestamp: str = ""


@dataclass(slots=True, kw_only=True)
class DelayedChargingSettings:
    """Delayed charging configuration."""

    enabled: bool = False
    delay_time: int = 0  # seconds
    select_status: int = 0  # 0=time-based, 1=off-peak


@dataclass(slots=True, kw_only=True)
class ScheduledChargingTask:
    """Scheduled charging task configuration."""

    enabled: bool = False
    cycle: str = ""  # Days of week
    cycle_time: str = ""  # Start time
    expiry_date: str | None = None
    connection_type: str = "1"  # 1=when plugged in, 2=specific time


@dataclass(slots=True, kw_only=True)
class OffPeakSettings:
    """Off-peak charging configuration."""

    enabled: bool = False
    weekday_start: str = "00:00"
    weekday_end: str = "00:00"
    weekend_start: str = "00:00"
    weekend_end: str = "00:00"


@dataclass(slots=True, kw_only=True)
class LastSessionData:
    """Data from the last completed charging session."""

    energy: float = 0.0  # kWh delivered in last session
    duration_minutes: int = 0  # Duration in minutes
    start_time: str = ""  # Start time as string
    end_time: str = ""  # End time as string


@dataclass(slots=True, kw_only=True)
class MonthlyStatistics:
    """Monthly charging statistics."""

    total_energy: float = 0.0  # Total kWh for the month
    session_count: int = 0  # Number of sessions this month
    month: str = ""  # Month in format YYYY-MM


@dataclass(slots=True, kw_only=True)
class YearlyStatistics:
    """Yearly charging statistics."""

    total_energy: float = 0.0  # Total kWh for the year
    session_count: int = 0  # Number of sessions this year
    year: str = ""  # Year in format YYYY


@dataclass(slots=True, kw_only=True)
class FirmwareStatus:
    """Firmware update status."""

    update_available: bool = False
    current_version: str = ""
    latest_version: str = ""


@dataclass(slots=True, kw_only=True)
class WifiInfo:
    """WiFi connection information."""

    ssid: str = ""
    signal: int = 0  # Signal strength in dBm


@dataclass(slots=True, kw_only=True)
class ExternalMeterData:
    """External meter data from load balancing."""

    current_l1: float = 0.0  # Phase U current in Amps
    current_l2: float = 0.0  # Phase V current in Amps
    current_l3: float = 0.0  # Phase W current in Amps
    voltage_l1: float = 0.0  # Phase U voltage in Volts
    voltage_l2: float = 0.0  # Phase V voltage in Volts
    voltage_l3: float = 0.0  # Phase W voltage in Volts
    power: float = 0.0  # Total power in Watts


@dataclass(slots=True, kw_only=True)
class LoadBalancingSettings:
    """Load balancing configuration."""

    enabled: bool = False
    max_current: int = 32  # Total domestic power in kW (stored as int)
    external_meter: ExternalMeterData | None = None


@dataclass(slots=True, kw_only=True)
class WellborneData:
    """Combined data from the Wellborne API."""

    charger: ChargerInfo
    status: ChargerStatus
    meter_values: MeterValues | None = None
    delayed_charging: DelayedChargingSettings = field(default_factory=DelayedChargingSettings)
    scheduled_charging: ScheduledChargingTask = field(default_factory=ScheduledChargingTask)
    off_peak: OffPeakSettings = field(default_factory=OffPeakSettings)
    transaction_id: str | None = None
    lifetime_energy: float = 0.0  # Total kWh from all transactions
    session_start_time: datetime | None = None  # Start time of current session
    last_session: LastSessionData | None = None  # Data from last completed session
    monthly_statistics: MonthlyStatistics | None = None  # Current month statistics
    yearly_statistics: YearlyStatistics | None = None  # Current year statistics
    firmware: FirmwareStatus | None = None  # Firmware update status
    wifi_info: WifiInfo | None = None  # WiFi connection info
    load_balancing: LoadBalancingSettings = field(default_factory=LoadBalancingSettings)


class WellborneApiClient:
    """Client for the Wellborne/ATESS EV Charger API."""

    def __init__(
        self,
        email: str,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the API client."""
        self._email = email
        self._session = session
        self._token: str | None = None
        self._own_session = session is None

    @property
    def is_authenticated(self) -> bool:
        """Return True if authenticated."""
        return self._token is not None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            self._own_session = True
        return self._session

    async def close(self) -> None:
        """Close the session if we own it."""
        if self._own_session and self._session and not self._session.closed:
            await self._session.close()

    def _get_headers(self, *, with_auth: bool = True) -> dict[str, str]:
        """Get request headers."""
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Language": "en-US",
            "phoneModel": "HomeAssistant",
            "appVersion": "1.0.4",
            "appOS": "android",
            "User-Agent": API_USER_AGENT,
        }
        if with_auth and self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using MD5 (required by ATESS API)."""
        return hashlib.md5(password.encode()).hexdigest()  # noqa: S324

    async def _request(
        self,
        endpoint: str,
        payload: Mapping[str, Any] | None = None,
        *,
        with_auth: bool = True,
    ) -> dict[str, Any]:
        """Make an API request."""
        session = await self._get_session()
        url = f"{API_BASE_URL}{endpoint}"
        headers = self._get_headers(with_auth=with_auth)

        _LOGGER.debug("API request: %s %s", endpoint, _redact_sensitive(payload))

        try:
            async with asyncio.timeout(API_TIMEOUT):
                async with session.post(url, json=payload or {}, headers=headers) as response:
                    data = await response.json()
                    _LOGGER.debug("API response: %s", _redact_sensitive(data))

                    # Check for session expired
                    result = data.get("result", data.get("ret"))
                    if result == ApiResult.SESSION_EXPIRED:
                        raise SessionExpiredError("Session expired, please re-authenticate")

                    return data

        except TimeoutError as err:
            raise ApiConnectionError(f"Timeout connecting to {url}") from err
        except aiohttp.ClientError as err:
            raise ApiConnectionError(f"Error connecting to {url}: {err}") from err

    def _check_response(self, data: dict[str, Any], operation: str) -> None:
        """Check API response for errors."""
        result = data.get("result", data.get("ret", -1))
        if result != ApiResult.SUCCESS:
            msg = data.get("msg", data.get("errMsg", "Unknown error"))
            raise ApiResponseError(f"{operation} failed: {msg}", result_code=result)

    # =========================================================================
    # Authentication
    # =========================================================================

    async def async_login(self, password: str) -> dict[str, Any]:
        """Authenticate with the API and get token."""
        payload = {
            "email": self._email,
            "password": self._hash_password(password),
            "phoneModel": "HomeAssistant",
            "appVersion": "1.0.4",
            "phoneOs": "0",
        }

        data = await self._request(Endpoints.LOGIN, payload, with_auth=False)

        result = data.get("result", -1)
        if result != ApiResult.SUCCESS:
            msg = data.get("msg", "Invalid credentials")
            raise AuthenticationError(f"Login failed: {msg}")

        obj = data.get("obj", {})
        token = obj.get("token", "")
        self._token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token

        _LOGGER.debug("Login successful for %s", self._email)
        return obj

    async def async_logout(self) -> None:
        """End the session."""
        if self._token:
            try:
                await self._request(Endpoints.LOGOUT)
            except WellborneError:
                pass  # Ignore logout errors
            finally:
                self._token = None

    # =========================================================================
    # Charger Management
    # =========================================================================

    async def async_get_chargers(self) -> list[ChargerInfo]:
        """Get list of chargers for this account."""
        data = await self._request(Endpoints.CHARGER_LIST, {"email": self._email})
        self._check_response(data, "Get chargers")

        return [
            ChargerInfo(
                charger_id=item.get("chargerId", ""),
                alias=item.get("alias", ""),
                model=item.get("model", ""),
                owner=item.get("owner", 0),
                connector_num=item.get("connectorNum", 1),
                max_power=item.get("chargePointModelPower", 0),
                bluetooth_enabled=bool(item.get("bluetoothEnable", 0)),
                create_time=item.get("createTime", ""),
            )
            for item in data.get("obj", [])
        ]

    async def async_is_charging(self, charger_id: str) -> bool:
        """Check if charger is currently charging."""
        data = await self._request(Endpoints.IS_CHARGING, {"chargerId": charger_id})
        self._check_response(data, "Check charging status")
        return bool(data.get("obj", False))

    async def async_unlock_connector(self, charger_id: str) -> None:
        """Unlock the connector."""
        data = await self._request(Endpoints.UNLOCK_CONNECTOR, {"chargerId": charger_id})
        self._check_response(data, "Unlock connector")

    # =========================================================================
    # Charging Control
    # =========================================================================

    async def async_start_charging(self, charger_id: str, connector_id: str = "1") -> None:
        """Start a charging session."""
        data = await self._request(
            Endpoints.REMOTE_START,
            {"chargerId": charger_id, "connectorId": connector_id},
        )
        self._check_response(data, "Start charging")

    async def async_stop_charging(self, charger_id: str, connector_id: str = "1") -> None:
        """Stop the current charging session."""
        data = await self._request(
            Endpoints.REMOTE_STOP,
            {"chargerId": charger_id, "connectorId": connector_id},
        )
        self._check_response(data, "Stop charging")

    async def async_prompt_charge(self, charger_id: str, connector_id: str = "1") -> None:
        """Start immediate charge (bypasses delayed charging)."""
        data = await self._request(
            Endpoints.PROMPT_CHARGE,
            {"chargerId": charger_id, "connectorId": connector_id},
        )
        self._check_response(data, "Prompt charge")

    # =========================================================================
    # Meter Values
    # =========================================================================

    @staticmethod
    def _safe_float(value: Any, default: float = 0.0) -> float:
        """Safely convert a value to float."""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    async def async_get_meter_values(self, transaction_id: str) -> MeterValues:
        """Get real-time meter values for an active transaction."""
        data = await self._request(Endpoints.GET_VALUES, {"transactionId": transaction_id})
        self._check_response(data, "Get meter values")

        values = data.get("obj", [{}])
        if isinstance(values, list) and values:
            item = values[0]
        else:
            item = values if isinstance(values, dict) else {}

        # Safely convert all values to float
        voltage_l1 = self._safe_float(item.get("voltage"))
        voltage_l2 = self._safe_float(item.get("voltageL2"))
        voltage_l3 = self._safe_float(item.get("voltageL3"))
        current_l1 = self._safe_float(item.get("current"))
        current_l2 = self._safe_float(item.get("currentL2"))
        current_l3 = self._safe_float(item.get("currentL3"))
        energy = self._safe_float(item.get("energy"))

        # Calculate total power (sum of all phases)
        power = (voltage_l1 * current_l1) + (voltage_l2 * current_l2) + (voltage_l3 * current_l3)

        return MeterValues(
            voltage=voltage_l1,
            voltage_l2=voltage_l2,
            voltage_l3=voltage_l3,
            current=current_l1,
            current_l2=current_l2,
            current_l3=current_l3,
            energy=energy,
            power=power,
            phase=item.get("phase", "1-phase"),
            timestamp=item.get("time", ""),
        )

    # =========================================================================
    # Configuration
    # =========================================================================

    async def async_get_charger_config(self, charger_id: str) -> dict[str, Any]:
        """Get full charger configuration."""
        data = await self._request(Endpoints.GET_CHARGER_CONFIG, {"chargerId": charger_id})
        self._check_response(data, "Get charger config")
        return data.get("obj", {})

    async def async_get_home_config(self, charger_id: str) -> dict[str, Any]:
        """Get home configuration (delayed charging, solar mode)."""
        data = await self._request(Endpoints.GET_HOME_CONFIG, {"chargerId": charger_id})
        self._check_response(data, "Get home config")
        return data.get("obj", {})

    async def async_set_max_current(self, charger_id: str, current: int) -> None:
        """Set maximum charging current (Amperes)."""
        data = await self._request(
            Endpoints.UPDATE_MAX_CURRENT,
            {"chargerId": charger_id, "value": str(current)},
        )
        self._check_response(data, "Set max current")

    async def async_set_solar_mode(self, charger_id: str, mode: str) -> None:
        """Set solar charging mode (0=off, 1=eco, 2=pure solar)."""
        data = await self._request(
            Endpoints.SAVE_SOLAR_MODE,
            {"chargerId": charger_id, "solarChargingMode": mode},
        )
        self._check_response(data, "Set solar mode")

    async def async_set_connector_lock(self, charger_id: str, *, enabled: bool) -> None:
        """Enable or disable connector lock."""
        data = await self._request(
            Endpoints.UPDATE_CONNECTOR_LOCK,
            {"chargerId": charger_id, "value": str(enabled).lower()},
        )
        self._check_response(data, "Set connector lock")

    # =========================================================================
    # Scheduled Charging
    # =========================================================================

    async def async_get_scheduled_charging(
        self,
        charger_id: str,
        connector_id: str = "1",
    ) -> ScheduledChargingTask:
        """Get scheduled charging task."""
        data = await self._request(
            Endpoints.GET_SCHEDULED_TASK,
            {"chargerId": charger_id, "connectorId": connector_id},
        )
        self._check_response(data, "Get scheduled charging")

        obj = data.get("obj", {})
        return ScheduledChargingTask(
            enabled=obj.get("status") == 1,
            cycle=obj.get("cycle", ""),
            cycle_time=obj.get("cycleTime", ""),
            expiry_date=obj.get("expiryDate"),
            connection_type=obj.get("connectionType", "1"),
        )

    async def async_set_scheduled_by_time(
        self,
        charger_id: str,
        connector_id: str,
        *,
        minutes: int,
        cycle: str,
        cycle_time: str,
        enabled: bool = True,
    ) -> None:
        """Set scheduled charging by duration."""
        data = await self._request(
            Endpoints.SET_SCHEDULED_BY_TIME,
            {
                "chargerId": charger_id,
                "connectorId": connector_id,
                "minute": str(minutes),
                "cycle": cycle,
                "cycleTime": cycle_time,
                "status": "1" if enabled else "2",
                "expiryDateType": "1",
                "connectionType": "1",
            },
        )
        self._check_response(data, "Set scheduled charging")

    # =========================================================================
    # Delayed Charging
    # =========================================================================

    async def async_get_delayed_charging(
        self,
        charger_id: str,
        connector_id: str = "1",
    ) -> DelayedChargingSettings:
        """Get delayed charging settings."""
        data = await self._request(
            Endpoints.GET_DELAYED_CHARGING,
            {"chargerId": charger_id, "connectorId": connector_id},
        )
        self._check_response(data, "Get delayed charging")

        obj = data.get("obj", {})
        return DelayedChargingSettings(
            enabled=obj.get("status") == 1,
            delay_time=obj.get("delayTime", 0),
            select_status=obj.get("selectStatus", 0),
        )

    async def async_set_delayed_charging(
        self,
        charger_id: str,
        *,
        enabled: bool,
        delay_seconds: int = 0,
    ) -> None:
        """Update delayed charging settings."""
        data = await self._request(
            Endpoints.UPDATE_DELAYED_CHARGING,
            {
                "chargerId": charger_id,
                "delayTime": str(delay_seconds),
                "status": 1 if enabled else 2,
                "selectStatus": 0,
            },
        )
        self._check_response(data, "Set delayed charging")

    # =========================================================================
    # Transaction History
    # =========================================================================

    async def async_get_transactions(
        self,
        charger_id: str,
        *,
        page: int = 1,
        page_size: int = 20,
        start_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get transaction history."""
        payload: dict[str, Any] = {
            "chargerId": charger_id,
            "pageNum": str(page),
            "pageSize": str(page_size),
        }
        if start_date:
            payload["startDate"] = start_date

        data = await self._request(Endpoints.TRANSACTION_LIST, payload)
        self._check_response(data, "Get transactions")

        # API returns paginated response with dataList key
        obj = data.get("obj", {})
        if isinstance(obj, dict):
            result = obj.get("dataList", obj.get("list", []))
        else:
            result = obj if isinstance(obj, list) else []

        return result

    # =========================================================================
    # Combined Data Fetch
    # =========================================================================

    async def async_set_max_power(self, charger_id: str, power_watts: int) -> None:
        """Set maximum charging power (Watts)."""
        data = await self._request(
            Endpoints.UPDATE_MAX_POWER,
            {"chargerId": charger_id, "value": str(power_watts)},
        )
        self._check_response(data, "Set max power")

    async def async_set_lcd_enabled(self, charger_id: str, *, enabled: bool) -> None:
        """Enable or disable LCD display."""
        data = await self._request(
            Endpoints.UPDATE_LCD,
            {"chargerId": charger_id, "value": "enable" if enabled else "disable"},
        )
        self._check_response(data, "Set LCD")

    async def async_set_low_power_reserve(self, charger_id: str, *, enabled: bool) -> None:
        """Enable or disable low power reserve mode."""
        data = await self._request(
            Endpoints.UPDATE_LOW_POWER,
            {"chargerId": charger_id, "value": "Enable" if enabled else "Disable"},
        )
        self._check_response(data, "Set low power reserve")

    async def async_get_wifi_info(self, charger_id: str) -> dict[str, Any]:
        """Get WiFi information."""
        data = await self._request(Endpoints.GET_WIFI_INFO, {"chargerId": charger_id})
        self._check_response(data, "Get WiFi info")
        return data.get("obj", {})

    # =========================================================================
    # Load Balancing
    # =========================================================================

    async def async_get_load_balancing(self, charger_id: str) -> dict[str, Any]:
        """Get load balancing configuration."""
        data = await self._request(Endpoints.GET_LOAD_BALANCING, {"chargerId": charger_id})
        self._check_response(data, "Get load balancing")
        return data.get("obj", {})

    async def async_set_load_balancing(
        self,
        charger_id: str,
        *,
        enabled: bool,
        max_current: int,
    ) -> None:
        """Set load balancing configuration."""
        data = await self._request(
            Endpoints.SET_LOAD_BALANCING,
            {
                "chargerId": charger_id,
                "enabled": enabled,
                "maxCurrent": str(max_current),
            },
        )
        self._check_response(data, "Set load balancing")

    # =========================================================================
    # Time Rates
    # =========================================================================

    async def async_get_time_rate(self, charger_id: str) -> dict[str, Any]:
        """Get time rate configuration."""
        data = await self._request(Endpoints.GET_TIME_RATE, {"chargerId": charger_id})
        self._check_response(data, "Get time rate")
        return data.get("obj", {})

    async def async_save_time_rate(
        self,
        charger_id: str,
        rates: list[dict[str, Any]],
    ) -> None:
        """Save time rate configuration."""
        data = await self._request(
            Endpoints.SAVE_TIME_RATE,
            {"chargerId": charger_id, "rates": rates},
        )
        self._check_response(data, "Save time rate")

    # =========================================================================
    # Off-Peak Charging (v2 API)
    # =========================================================================

    async def async_get_off_peak_time(self, charger_id: str) -> dict[str, Any]:
        """Get off-peak time settings."""
        data = await self._request(Endpoints.GET_OFF_PEAK_TIME, {"chargerId": charger_id})
        self._check_response(data, "Get off-peak time")
        return data.get("obj", {})

    async def async_set_off_peak_time(
        self,
        charger_id: str,
        *,
        weekday_start: str,
        weekday_end: str,
        weekend_start: str = "00:00",
        weekend_end: str = "00:00",
    ) -> None:
        """Set off-peak time periods."""
        data = await self._request(
            Endpoints.SET_OFF_PEAK_TIME,
            {
                "chargerId": charger_id,
                "weekdayStart": weekday_start,
                "weekdayEnd": weekday_end,
                "weekendStart": weekend_start,
                "weekendEnd": weekend_end,
            },
        )
        self._check_response(data, "Set off-peak time")

    async def async_set_off_peak_enabled(self, charger_id: str, *, enabled: bool) -> None:
        """Enable or disable off-peak charging mode."""
        endpoint = Endpoints.SET_OFF_PEAK_ENABLE if enabled else Endpoints.SET_OFF_PEAK_DISABLE
        data = await self._request(endpoint, {"chargerId": charger_id})
        self._check_response(data, "Set off-peak enabled")

    # =========================================================================
    # Firmware
    # =========================================================================

    async def async_get_firmware_status(self, charger_id: str) -> dict[str, Any]:
        """Get firmware update status."""
        data = await self._request(Endpoints.GET_FIRMWARE_STATUS, {"chargerId": charger_id})
        self._check_response(data, "Get firmware status")
        return data.get("obj", {})

    # =========================================================================
    # Transaction Statistics
    # =========================================================================

    async def async_get_transactions_month(
        self,
        charger_id: str,
        month: str,
    ) -> dict[str, Any]:
        """Get monthly transaction statistics.

        Args:
            charger_id: The charger ID.
            month: Month in format 'YYYY-MM'.

        """
        data = await self._request(
            Endpoints.TRANSACTION_MONTH,
            {"chargerId": charger_id, "date": month},
        )
        self._check_response(data, "Get monthly transactions")

        _LOGGER.debug("Monthly stats for %s: %s", month, _redact_sensitive(data))

        return data.get("obj", {})

    async def async_get_transactions_year(
        self,
        charger_id: str,
        year: str,
    ) -> dict[str, Any]:
        """Get yearly transaction statistics.

        Args:
            charger_id: The charger ID.
            year: Year in format 'YYYY'.

        """
        data = await self._request(
            Endpoints.TRANSACTION_YEAR,
            {"chargerId": charger_id, "date": year},
        )
        self._check_response(data, "Get yearly transactions")

        _LOGGER.debug("Yearly stats for %s: %s", year, _redact_sensitive(data))

        return data.get("obj", {})

    # =========================================================================
    # Additional Scheduled Charging Methods
    # =========================================================================

    async def async_set_scheduled_by_energy(
        self,
        charger_id: str,
        connector_id: str,
        *,
        energy_kwh: float,
        cycle: str,
        cycle_time: str,
        enabled: bool = True,
    ) -> None:
        """Set scheduled charging by energy amount (kWh)."""
        data = await self._request(
            Endpoints.SET_SCHEDULED_BY_ENERGY,
            {
                "chargerId": charger_id,
                "connectorId": connector_id,
                "electric": str(energy_kwh),
                "cycle": cycle,
                "cycleTime": cycle_time,
                "status": "1" if enabled else "2",
                "expiryDateType": "1",
                "connectionType": "1",
            },
        )
        self._check_response(data, "Set scheduled charging by energy")

    async def async_set_scheduled_by_full(
        self,
        charger_id: str,
        connector_id: str,
        *,
        cycle: str,
        cycle_time: str,
        enabled: bool = True,
    ) -> None:
        """Set scheduled charging until full."""
        data = await self._request(
            Endpoints.SET_SCHEDULED_BY_FULL,
            {
                "chargerId": charger_id,
                "connectorId": connector_id,
                "cycle": cycle,
                "cycleTime": cycle_time,
                "status": "1" if enabled else "2",
                "expiryDateType": "1",
                "connectionType": "1",
            },
        )
        self._check_response(data, "Set scheduled charging by full")

    async def async_set_scheduled_by_end_time(
        self,
        charger_id: str,
        connector_id: str,
        *,
        end_time: str,
        cycle: str,
        cycle_time: str,
        enabled: bool = True,
    ) -> None:
        """Set scheduled charging by end time."""
        data = await self._request(
            Endpoints.SET_SCHEDULED_BY_END_TIME,
            {
                "chargerId": charger_id,
                "connectorId": connector_id,
                "endTime": end_time,
                "cycle": cycle,
                "cycleTime": cycle_time,
                "status": "1" if enabled else "2",
                "expiryDateType": "1",
                "connectionType": "1",
            },
        )
        self._check_response(data, "Set scheduled charging by end time")

    # =========================================================================
    # Combined Data Fetch
    # =========================================================================

    async def async_get_charger_data(self, charger_id: str) -> WellborneData:
        """Get all data for a charger in one call."""
        # Get charger info first
        chargers = await self.async_get_chargers()
        charger_info = next((c for c in chargers if c.charger_id == charger_id), None)

        if not charger_info:
            raise ApiResponseError(f"Charger {charger_id} not found")

        # Fetch status and config concurrently with error handling
        # Use shorter timeout for the batch to prevent blocking
        try:
            async with asyncio.timeout(45):  # Total timeout for core data
                results = await asyncio.gather(
                    self.async_is_charging(charger_id),
                    self.async_get_charger_config(charger_id),
                    self.async_get_home_config(charger_id),
                    self.async_get_delayed_charging(charger_id),
                    self.async_get_scheduled_charging(charger_id),
                    self.async_get_off_peak_time(charger_id),
                    return_exceptions=True,
                )
        except TimeoutError:
            _LOGGER.warning("Timeout fetching core charger data, using defaults")
            results = [
                False,
                {},
                {},
                DelayedChargingSettings(),
                ScheduledChargingTask(),
                {},
            ]

        # Handle results - use defaults for any failed calls.
        # gather(return_exceptions=True) yields T | BaseException, so narrow
        # against BaseException to exclude e.g. CancelledError from the value.
        is_charging = results[0] if not isinstance(results[0], BaseException) else False
        config = results[1] if not isinstance(results[1], BaseException) else {}
        home_config = results[2] if not isinstance(results[2], BaseException) else {}
        delayed = results[3] if not isinstance(results[3], BaseException) else DelayedChargingSettings()
        scheduled = results[4] if not isinstance(results[4], BaseException) else ScheduledChargingTask()
        off_peak_data = results[5] if not isinstance(results[5], BaseException) else {}

        # Log any errors
        for i, result in enumerate(results):
            if isinstance(result, BaseException):
                endpoint_names = [
                    "is_charging",
                    "config",
                    "home_config",
                    "delayed",
                    "scheduled",
                    "off_peak",
                ]
                _LOGGER.warning("Failed to fetch %s: %s", endpoint_names[i], result)

        # Parse off-peak settings
        # The GET endpoint returns offPeakTimes array, while SET uses top-level fields.
        # Read from offPeakTimes (what GET returns) as primary source.
        _LOGGER.debug("Off-peak settings: %s", _redact_sensitive(off_peak_data))
        off_peak_enabled = str(off_peak_data.get("offPeakEnable", "")).lower() == "enable"

        # Read from offPeakTimes array (GET response format)
        weekday_start = "00:00"
        weekday_end = "00:00"
        off_peak_times = off_peak_data.get("offPeakTimes", [])
        if off_peak_times and isinstance(off_peak_times, list) and len(off_peak_times) > 0:
            first_period = off_peak_times[0]
            if isinstance(first_period, dict):
                weekday_start = first_period.get("startTime") or "00:00"
                weekday_end = first_period.get("endTime") or "00:00"

        off_peak = OffPeakSettings(
            enabled=off_peak_enabled,
            weekday_start=weekday_start,
            weekday_end=weekday_end,
            weekend_start=off_peak_data.get("weekendStart", "00:00"),
            weekend_end=off_peak_data.get("weekendEnd", "00:00"),
        )

        status = ChargerStatus(
            is_charging=is_charging,
            solar_mode=str(home_config.get("solarChargingMode", "0")),
            max_current=self._safe_float(config.get("maximumOutputCurrent"), 32.0),
            connector_lock=str(config.get("connectorLock", "")).lower() == "true",
            lcd_enabled=str(config.get("lcd", "")).lower() == "enable",
            low_power_reserve=str(config.get("lowPowerReserve", "")).lower() == "enable",
        )

        # Get meter values if charging and calculate lifetime energy
        meter_values = None
        transaction_id = None
        lifetime_energy = 0.0
        session_start_time = None
        last_session = None

        # Fetch transactions for lifetime energy calculation and active transaction
        try:
            # Fetch a larger page to get more transaction history
            transactions_raw = await self.async_get_transactions(charger_id, page_size=100)

            # Ensure transactions is a list of dicts (API may return different formats)
            transactions: list[dict[str, Any]] = []
            if isinstance(transactions_raw, list):
                # Filter to only include dict items (skip any strings or other types)
                transactions = [t for t in transactions_raw if isinstance(t, dict)]
            elif isinstance(transactions_raw, dict):
                # API might return paginated data with 'list' or 'records' key
                transactions = transactions_raw.get("list", transactions_raw.get("records", []))
                if not isinstance(transactions, list):
                    transactions = []

            # Calculate lifetime energy from all fetched transactions
            # API uses 'energyKWH' field for energy
            lifetime_energy = sum(self._safe_float(t.get("energyKWH", t.get("energy"))) for t in transactions)

            if is_charging and transactions:
                # API uses 'transactionId' not 'id'
                transaction_id = str(transactions[0].get("transactionId", transactions[0].get("id", "")))
                # Parse session start time from the active transaction
                # API format: startDate='01/10 2026', startTime='20:01:22'
                start_date_str = transactions[0].get("startDate", "")
                start_time_str = transactions[0].get("startTime", "")
                if start_date_str and start_time_str:
                    try:
                        # Parse date in MM/DD YYYY format
                        full_start = f"{start_date_str} {start_time_str}"
                        session_start_time = datetime.strptime(full_start, "%m/%d %Y %H:%M:%S").replace(tzinfo=UTC)
                    except ValueError:
                        _LOGGER.debug(
                            "Could not parse session start time: %s %s",
                            start_date_str,
                            start_time_str,
                        )

                if transaction_id:
                    try:
                        meter_values = await self.async_get_meter_values(transaction_id)
                    except WellborneError as err:
                        _LOGGER.warning("Could not get meter values: %s", err)

            # Find the last completed session (first transaction with stopTime)
            # If charging, skip the first transaction (it's the active one)
            completed_transactions = transactions[1:] if is_charging else transactions
            for t in completed_transactions:
                # API uses 'stopTime' not 'endTime'
                stop_time = t.get("stopTime")
                if stop_time:  # Has stop time = completed session
                    energy = self._safe_float(t.get("energyKWH", t.get("energy")))
                    start_date = t.get("startDate", "")
                    start_time = t.get("startTime", "")
                    # Parse duration from 'chargingTime' field (format: HH:MM:SS)
                    charging_time = t.get("chargingTime", "")
                    duration_minutes = 0
                    if charging_time:
                        try:
                            parts = charging_time.split(":")
                            if len(parts) == 3:
                                duration_minutes = int(parts[0]) * 60 + int(parts[1])
                        except (ValueError, IndexError):
                            _LOGGER.debug("Could not parse charging time: %s", charging_time)

                    last_session = LastSessionData(
                        energy=energy,
                        duration_minutes=duration_minutes,
                        start_time=f"{start_date} {start_time}",
                        end_time=f"{start_date} {stop_time}",
                    )
                    break  # Take only the first completed session

        except WellborneError as err:
            _LOGGER.warning("Could not get transactions: %s", err)

        # Fetch secondary data in parallel with timeout to prevent blocking
        # Get current month and year for statistics
        now = datetime.now(tz=UTC)
        current_month = now.strftime("%Y-%m")
        current_year = now.strftime("%Y")

        # Initialize defaults
        monthly_statistics = None
        yearly_statistics = None
        firmware = None
        wifi_info = None
        load_balancing = LoadBalancingSettings()

        try:
            async with asyncio.timeout(30):  # Timeout for secondary data
                secondary_results = await asyncio.gather(
                    self.async_get_transactions_month(charger_id, current_month),
                    self.async_get_transactions_year(charger_id, current_year),
                    self.async_get_firmware_status(charger_id),
                    self.async_get_wifi_info(charger_id),
                    self.async_get_load_balancing(charger_id),
                    return_exceptions=True,
                )
        except TimeoutError:
            _LOGGER.warning("Timeout fetching secondary charger data, using defaults")
            secondary_results = [None, None, None, None, None]

        # Process monthly statistics
        month_data = secondary_results[0]
        if isinstance(month_data, BaseException):
            _LOGGER.warning("Could not get monthly statistics: %s", month_data)
        elif month_data:
            monthly_statistics = MonthlyStatistics(
                total_energy=self._safe_float(month_data.get("energyTotal")),
                session_count=int(month_data.get("sessionCount", 0) or 0),
                month=current_month,
            )

        # Process yearly statistics
        year_data = secondary_results[1]
        if isinstance(year_data, BaseException):
            _LOGGER.warning("Could not get yearly statistics: %s", year_data)
        elif year_data:
            yearly_statistics = YearlyStatistics(
                total_energy=self._safe_float(year_data.get("energyTotal")),
                session_count=int(year_data.get("sessionCount", 0) or 0),
                year=current_year,
            )

        # Process firmware status
        firmware_data = secondary_results[2]
        if isinstance(firmware_data, BaseException):
            _LOGGER.warning("Could not get firmware status: %s", firmware_data)
        elif firmware_data:
            firmware = FirmwareStatus(
                update_available=bool(firmware_data.get("updateAvailable", False)),
                current_version=str(firmware_data.get("currentVersion", "")),
                latest_version=str(firmware_data.get("latestVersion", "")),
            )

        # Process WiFi info
        wifi_data = secondary_results[3]
        if isinstance(wifi_data, BaseException):
            _LOGGER.warning("Could not get WiFi info: %s", wifi_data)
        elif wifi_data:
            wifi_info = WifiInfo(
                ssid=str(wifi_data.get("wifiSsid", wifi_data.get("ssid", ""))),
                signal=int(wifi_data.get("signal", wifi_data.get("rssi", 0)) or 0),
            )

        # Process load balancing settings
        lb_data = secondary_results[4]
        if isinstance(lb_data, BaseException):
            _LOGGER.warning("Could not get load balancing settings: %s", lb_data)
        elif lb_data:
            # API returns enablePowerAllocationCharge as string '0' or '1'
            enabled_str = lb_data.get("enablePowerAllocationCharge", "0")
            enabled = enabled_str == "1"
            # API returns totalDomesticPower in kW, we store it as the max_current field
            # (this is the domestic power limit, not current, but we use the same field)
            total_power = int(float(lb_data.get("totalDomesticPower", "32") or "32"))

            # Parse external meter data if available
            external_meter = None
            ext_data = lb_data.get("externalCurrent")
            if ext_data and isinstance(ext_data, dict):
                # Helper to parse values like '30A', '225V', '14344W'
                def parse_value(val: Any) -> float:
                    if val is None:
                        return 0.0
                    if isinstance(val, (int, float)):
                        return float(val)
                    # Remove unit suffix (A, V, W) and convert
                    val_str = str(val).rstrip("AVWavw")
                    try:
                        return float(val_str)
                    except ValueError:
                        return 0.0

                external_meter = ExternalMeterData(
                    current_l1=parse_value(ext_data.get("ucurrent")),
                    current_l2=parse_value(ext_data.get("vcurrent")),
                    current_l3=parse_value(ext_data.get("wcurrent")),
                    voltage_l1=parse_value(ext_data.get("uvoltage")),
                    voltage_l2=parse_value(ext_data.get("vvoltage")),
                    voltage_l3=parse_value(ext_data.get("wvoltage")),
                    power=parse_value(ext_data.get("power")),
                )

            load_balancing = LoadBalancingSettings(
                enabled=enabled,
                max_current=total_power,  # Note: This is actually kW, not Amps
                external_meter=external_meter,
            )

        return WellborneData(
            charger=charger_info,
            status=status,
            meter_values=meter_values,
            delayed_charging=delayed,
            scheduled_charging=scheduled,
            off_peak=off_peak,
            transaction_id=transaction_id,
            lifetime_energy=lifetime_energy,
            session_start_time=session_start_time,
            last_session=last_session,
            monthly_statistics=monthly_statistics,
            yearly_statistics=yearly_statistics,
            firmware=firmware,
            wifi_info=wifi_info,
            load_balancing=load_balancing,
        )
