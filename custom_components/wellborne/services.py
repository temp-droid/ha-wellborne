"""Services for Wellborne EV Charger."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN, SOLAR_MODE_SERVICE_TO_API, SolarMode
from .coordinator import WellborneDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

# Service names
SERVICE_START_CHARGING = "start_charging"
SERVICE_STOP_CHARGING = "stop_charging"
SERVICE_SET_MAX_CURRENT = "set_max_current"
SERVICE_SET_SOLAR_MODE = "set_solar_mode"

# Service schema attributes
# BREAKING CHANGE: Renamed from device_id to charger_id for consistency
ATTR_CHARGER_ID = "charger_id"
ATTR_CURRENT = "current"
ATTR_MODE = "mode"

# Service schemas
SERVICE_START_CHARGING_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CHARGER_ID): cv.string,
    }
)

SERVICE_STOP_CHARGING_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CHARGER_ID): cv.string,
    }
)

SERVICE_SET_MAX_CURRENT_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CHARGER_ID): cv.string,
        vol.Required(ATTR_CURRENT): vol.All(vol.Coerce(int), vol.Range(min=6, max=32)),
    }
)

SERVICE_SET_SOLAR_MODE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CHARGER_ID): cv.string,
        vol.Required(ATTR_MODE): vol.In(["off", "eco", "pure_solar"]),
    }
)


def _get_coordinator(hass: HomeAssistant, charger_id: str) -> WellborneDataUpdateCoordinator:
    """Get coordinator for a charger ID, raising ServiceValidationError if not found."""
    for coordinator in hass.data.get(DOMAIN, {}).values():
        if coordinator.charger_id == charger_id:
            return coordinator
    raise ServiceValidationError(f"Charger {charger_id} not found")


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Wellborne services."""

    async def async_start_charging(call: ServiceCall) -> None:
        """Handle start charging service call."""
        coordinator = _get_coordinator(hass, call.data[ATTR_CHARGER_ID])
        await coordinator.async_start_charging()

    async def async_stop_charging(call: ServiceCall) -> None:
        """Handle stop charging service call."""
        coordinator = _get_coordinator(hass, call.data[ATTR_CHARGER_ID])
        await coordinator.async_stop_charging()

    async def async_set_max_current(call: ServiceCall) -> None:
        """Handle set max current service call."""
        coordinator = _get_coordinator(hass, call.data[ATTR_CHARGER_ID])
        await coordinator.async_set_max_current(call.data[ATTR_CURRENT])

    async def async_set_solar_mode(call: ServiceCall) -> None:
        """Handle set solar mode service call."""
        charger_id = call.data[ATTR_CHARGER_ID]
        api_mode = SOLAR_MODE_SERVICE_TO_API.get(call.data[ATTR_MODE], SolarMode.OFF)
        coordinator = _get_coordinator(hass, charger_id)
        await coordinator.async_set_solar_mode(api_mode)

    # Register services
    hass.services.async_register(
        DOMAIN, SERVICE_START_CHARGING, async_start_charging, schema=SERVICE_START_CHARGING_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_STOP_CHARGING, async_stop_charging, schema=SERVICE_STOP_CHARGING_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SET_MAX_CURRENT, async_set_max_current, schema=SERVICE_SET_MAX_CURRENT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SET_SOLAR_MODE, async_set_solar_mode, schema=SERVICE_SET_SOLAR_MODE_SCHEMA
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Wellborne services."""
    hass.services.async_remove(DOMAIN, SERVICE_START_CHARGING)
    hass.services.async_remove(DOMAIN, SERVICE_STOP_CHARGING)
    hass.services.async_remove(DOMAIN, SERVICE_SET_MAX_CURRENT)
    hass.services.async_remove(DOMAIN, SERVICE_SET_SOLAR_MODE)
