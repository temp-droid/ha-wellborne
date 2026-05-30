"""The Wellborne EV Charger integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ApiConnectionError, AuthenticationError, WellborneApiClient
from .const import CONF_CHARGER_ID, DOMAIN, PLATFORMS
from .coordinator import WellborneDataUpdateCoordinator
from .services import async_setup_services, async_unload_services

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wellborne from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create API client
    session = async_get_clientsession(hass)
    client = WellborneApiClient(
        email=entry.data[CONF_EMAIL],
        session=session,
    )

    # Authenticate
    try:
        await client.async_login(entry.data[CONF_PASSWORD])
    except AuthenticationError as err:
        raise ConfigEntryAuthFailed("Invalid credentials") from err
    except ApiConnectionError as err:
        raise ConfigEntryNotReady(f"Cannot connect to API: {err}") from err

    # Get charger ID (use first charger if not specified)
    charger_id = entry.data.get(CONF_CHARGER_ID)
    if not charger_id:
        chargers = await client.async_get_chargers()
        if not chargers:
            raise ConfigEntryNotReady("No chargers found for this account")
        charger_id = chargers[0].charger_id

    # Create coordinator
    coordinator = WellborneDataUpdateCoordinator(
        hass=hass,
        client=client,
        charger_id=charger_id,
        config_entry=entry,
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator (client accessible via coordinator.client)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up services (only once, when first entry is added)
    if len(hass.data[DOMAIN]) == 1:
        await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        # Logout from API — must not fail unload
        try:
            await coordinator.client.async_logout()
        except Exception as err:  # unload must not fail on logout
            _LOGGER.debug("Logout during unload failed: %s", err)

        # Unload services when last entry is removed
        if not hass.data[DOMAIN]:
            await async_unload_services(hass)

    return unload_ok
