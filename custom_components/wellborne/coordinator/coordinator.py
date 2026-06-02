"""DataUpdateCoordinator for Wellborne integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..api import (
    ApiConnectionError,
    AuthenticationError,
    ChargerOfflineError,
    SessionExpiredError,
    WellborneApiClient,
    WellborneData,
    WellborneError,
)
from ..const import (
    CHARGING_POLL_INTERVAL,
    CONF_CHARGING_POLL_INTERVAL,
    CONF_IDLE_POLL_INTERVAL,
    COORDINATOR_UPDATE_TIMEOUT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCHEDULE_CYCLE,
    DEFAULT_SCHEDULE_DURATION_MINUTES,
    DEFAULT_SCHEDULE_TIME,
    DOMAIN,
    IDLE_POLL_INTERVAL,
    OFFLINE_POLL_INTERVAL,
    OFFLINE_TIMEOUT_COUNT,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class WellborneDataUpdateCoordinator(DataUpdateCoordinator[WellborneData]):
    """Coordinator for fetching Wellborne charger data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: WellborneApiClient,
        charger_id: str,
        config_entry: ConfigEntry,
        update_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{charger_id}",
            update_interval=timedelta(seconds=update_interval),
            config_entry=config_entry,
        )
        self._client = client
        self._charger_id = charger_id

        # Adaptive polling intervals from options
        self._charging_interval = config_entry.options.get(CONF_CHARGING_POLL_INTERVAL, CHARGING_POLL_INTERVAL)
        self._idle_interval = config_entry.options.get(CONF_IDLE_POLL_INTERVAL, IDLE_POLL_INTERVAL)

        # Offline detection state
        self._consecutive_timeouts = 0
        self._is_online = True

        # Conditional logging state: track endpoints with recent failures
        self._endpoint_failure_counts: dict[str, int] = {}

    @property
    def client(self) -> WellborneApiClient:
        """Return the API client."""
        return self._client

    @property
    def charger_id(self) -> str:
        """Return the charger ID."""
        return self._charger_id

    @property
    def is_online(self) -> bool:
        """Return True if the charger is considered online."""
        return self._is_online

    def _log_failure(self, endpoint: str, message: str, exc: Exception | None = None) -> None:
        """Log a failure with conditional warning/debug based on repeat count.

        First failure for an endpoint logs as warning, subsequent failures log as debug
        to reduce log spam during extended outages.
        """
        self._endpoint_failure_counts[endpoint] = self._endpoint_failure_counts.get(endpoint, 0) + 1
        count = self._endpoint_failure_counts[endpoint]

        if count == 1:
            # First failure - log as warning
            if exc:
                _LOGGER.warning("%s: %s", message, exc)
            else:
                _LOGGER.warning("%s", message)
        # Subsequent failures - log as debug to reduce noise
        elif exc:
            _LOGGER.debug("%s (failure #%d): %s", message, count, exc)
        else:
            _LOGGER.debug("%s (failure #%d)", message, count)

    def _log_success(self, endpoint: str) -> None:
        """Reset failure count on success for an endpoint."""
        if endpoint in self._endpoint_failure_counts:
            del self._endpoint_failure_counts[endpoint]

    def _update_polling_interval(self, is_charging: bool) -> None:
        """Update the polling interval based on charging state."""
        new_interval = self._charging_interval if is_charging else self._idle_interval
        current_interval = int(self.update_interval.total_seconds()) if self.update_interval else None

        if new_interval != current_interval:
            self.update_interval = timedelta(seconds=new_interval)
            _LOGGER.debug(
                "Polling interval adjusted to %d seconds (charging=%s)",
                new_interval,
                is_charging,
            )

    async def _async_update_data(self) -> WellborneData:
        """Fetch data from the API."""
        try:
            async with asyncio.timeout(COORDINATOR_UPDATE_TIMEOUT):
                data = await self._client.async_get_charger_data(self._charger_id)

            # Success - reset offline detection
            if self._consecutive_timeouts > 0:
                _LOGGER.info("Connection restored after %d timeouts", self._consecutive_timeouts)
            self._consecutive_timeouts = 0
            self._is_online = True
            self._log_success("charger_data")

            # Adaptive polling: adjust interval based on charging state
            self._update_polling_interval(data.status.is_charging)

        except (AuthenticationError, SessionExpiredError) as err:
            # Trigger re-authentication flow
            raise ConfigEntryAuthFailed("Authentication failed") from err

        except (ChargerOfflineError, ApiConnectionError, TimeoutError) as err:
            # All three signal the charger is unreachable from the cloud.
            # ChargerOfflineError: upstream error message marked the charger offline.
            # ApiConnectionError / TimeoutError: transport-level failure (TimeoutError is
            # asyncio.TimeoutError in Python 3.11+).
            return self._handle_offline(err)

        except WellborneError as err:
            self._log_failure("charger_data", "Error fetching data", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

        else:
            return data

    def _handle_offline(self, err: Exception) -> WellborneData:
        """Handle an offline signal: count failures, flip offline at threshold, keep entities alive.

        Returns the last-known data when available (so entities stay populated during a backoff),
        otherwise raises UpdateFailed with the same messages as the prior implementation.
        """
        self._consecutive_timeouts += 1
        self._log_failure("charger_data", f"Charger unreachable (failure #{self._consecutive_timeouts})", err)

        if self._consecutive_timeouts >= OFFLINE_TIMEOUT_COUNT:
            if self._is_online:
                _LOGGER.warning(
                    "Charger marked offline after %d consecutive failures",
                    self._consecutive_timeouts,
                )
            self._is_online = False
            # Back off polling while offline to stop hammering the vendor cloud.
            self.update_interval = timedelta(seconds=OFFLINE_POLL_INTERVAL)

        # Keep entities alive with the last known values when we have them.
        if self.data is not None:
            return self.data

        # No cached data yet: surface the failure (messages preserved for existing tests).
        if isinstance(err, TimeoutError):
            raise UpdateFailed(f"Charger data fetch timed out after {COORDINATOR_UPDATE_TIMEOUT}s") from err
        if isinstance(err, ApiConnectionError):
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        raise UpdateFailed(f"Charger offline: {err}") from err

    async def async_start_charging(self, connector_id: str = "1") -> None:
        """Start a charging session."""
        await self._client.async_start_charging(self._charger_id, connector_id)
        await self.async_request_refresh()

    async def async_stop_charging(self, connector_id: str = "1") -> None:
        """Stop the current charging session."""
        await self._client.async_stop_charging(self._charger_id, connector_id)
        await self.async_request_refresh()

    async def async_set_max_current(self, current: int) -> None:
        """Set maximum charging current."""
        await self._client.async_set_max_current(self._charger_id, current)
        await self.async_request_refresh()

    async def async_set_solar_mode(self, mode: str) -> None:
        """Set solar charging mode."""
        await self._client.async_set_solar_mode(self._charger_id, mode)
        await self.async_request_refresh()

    async def async_unlock_connector(self) -> None:
        """Unlock the connector."""
        await self._client.async_unlock_connector(self._charger_id)

    async def async_prompt_charge(self, connector_id: str = "1") -> None:
        """Start immediate charge (bypasses delay)."""
        await self._client.async_prompt_charge(self._charger_id, connector_id)
        await self.async_request_refresh()

    async def async_set_connector_lock(self, *, enabled: bool) -> None:
        """Enable or disable the connector lock."""
        await self._client.async_set_connector_lock(self._charger_id, enabled=enabled)
        await self.async_request_refresh()

    async def async_set_delayed_charging_enabled(self, *, enabled: bool) -> None:
        """Enable or disable delayed charging."""
        # Get current delay time to preserve it when toggling
        delay_seconds = 0
        if self.data and self.data.delayed_charging:
            delay_seconds = self.data.delayed_charging.delay_time
        await self._client.async_set_delayed_charging(self._charger_id, enabled=enabled, delay_seconds=delay_seconds)
        await self.async_request_refresh()

    async def async_set_delay_time(self, delay_minutes: int) -> None:
        """Set the delayed charging delay time in minutes."""
        # Convert minutes to seconds and preserve enabled state
        enabled = False
        if self.data and self.data.delayed_charging:
            enabled = self.data.delayed_charging.enabled
        await self._client.async_set_delayed_charging(
            self._charger_id, enabled=enabled, delay_seconds=delay_minutes * 60
        )
        await self.async_request_refresh()

    async def async_set_scheduled_charging_enabled(self, *, enabled: bool) -> None:
        """Enable or disable scheduled charging."""
        if not (self.data and self.data.scheduled_charging):
            raise HomeAssistantError("Scheduled charging data not available yet")
        schedule = self.data.scheduled_charging
        await self._client.async_set_scheduled_by_time(
            self._charger_id,
            connector_id="1",
            minutes=DEFAULT_SCHEDULE_DURATION_MINUTES,
            cycle=schedule.cycle or DEFAULT_SCHEDULE_CYCLE,
            cycle_time=schedule.cycle_time or DEFAULT_SCHEDULE_TIME,
            enabled=enabled,
        )
        await self.async_request_refresh()

    async def async_set_off_peak_enabled(self, *, enabled: bool) -> None:
        """Enable or disable off-peak charging."""
        await self._client.async_set_off_peak_enabled(self._charger_id, enabled=enabled)
        await self.async_request_refresh()

    async def async_set_off_peak_time(
        self,
        *,
        weekday_start: str | None = None,
        weekday_end: str | None = None,
        weekend_start: str | None = None,
        weekend_end: str | None = None,
    ) -> None:
        """Set off-peak time settings."""
        # Get current values for any not provided
        current = self.data.off_peak if self.data else None
        await self._client.async_set_off_peak_time(
            self._charger_id,
            weekday_start=weekday_start or (current.weekday_start if current else "00:00"),
            weekday_end=weekday_end or (current.weekday_end if current else "00:00"),
            weekend_start=weekend_start or (current.weekend_start if current else "00:00"),
            weekend_end=weekend_end or (current.weekend_end if current else "00:00"),
        )
        await self.async_request_refresh()

    async def async_set_scheduled_time(self, *, cycle_time: str) -> None:
        """Set scheduled charging start time."""
        if not (self.data and self.data.scheduled_charging):
            raise HomeAssistantError("Scheduled charging data not available yet")
        schedule = self.data.scheduled_charging
        await self._client.async_set_scheduled_by_time(
            self._charger_id,
            connector_id="1",
            minutes=DEFAULT_SCHEDULE_DURATION_MINUTES,
            cycle=schedule.cycle or DEFAULT_SCHEDULE_CYCLE,
            cycle_time=cycle_time,
            enabled=schedule.enabled,
        )
        await self.async_request_refresh()

    async def async_set_lcd_enabled(self, *, enabled: bool) -> None:
        """Enable or disable the LCD display."""
        await self._client.async_set_lcd_enabled(self._charger_id, enabled=enabled)
        await self.async_request_refresh()

    async def async_set_low_power_reserve_enabled(self, *, enabled: bool) -> None:
        """Enable or disable low power reserve mode."""
        await self._client.async_set_low_power_reserve(self._charger_id, enabled=enabled)
        await self.async_request_refresh()

    async def async_set_load_balancing_enabled(self, *, enabled: bool) -> None:
        """Enable or disable load balancing."""
        # Preserve current max current setting
        max_current = 32
        if self.data and self.data.load_balancing:
            max_current = self.data.load_balancing.max_current
        await self._client.async_set_load_balancing(self._charger_id, enabled=enabled, max_current=max_current)
        await self.async_request_refresh()

    async def async_set_load_balancing_current(self, current: int) -> None:
        """Set load balancing maximum current."""
        # Preserve enabled state
        enabled = False
        if self.data and self.data.load_balancing:
            enabled = self.data.load_balancing.enabled
        await self._client.async_set_load_balancing(self._charger_id, enabled=enabled, max_current=current)
        await self.async_request_refresh()

    async def async_set_max_power(self, power_watts: int) -> None:
        """Set maximum charging power in Watts."""
        await self._client.async_set_max_power(self._charger_id, power_watts)
        await self.async_request_refresh()
