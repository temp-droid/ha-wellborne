"""Tests for the Wellborne services."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.services import (
    SERVICE_SET_MAX_CURRENT,
    SERVICE_SET_SOLAR_MODE,
    SERVICE_START_CHARGING,
    SERVICE_STOP_CHARGING,
    async_setup_services,
)

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_start_charging = AsyncMock()
    coordinator.async_stop_charging = AsyncMock()
    coordinator.async_set_max_current = AsyncMock()
    coordinator.async_set_solar_mode = AsyncMock()
    return coordinator


async def test_start_charging_service(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test start charging service calls coordinator."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    # Set up services
    await async_setup_services(hass)

    # Call the service
    await hass.services.async_call(
        DOMAIN,
        SERVICE_START_CHARGING,
        {"charger_id": TEST_CHARGER_ID},
        blocking=True,
    )

    # Verify coordinator method was called
    mock_coordinator.async_start_charging.assert_called_once()


async def test_stop_charging_service(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test stop charging service calls coordinator."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    await async_setup_services(hass)

    await hass.services.async_call(
        DOMAIN,
        SERVICE_STOP_CHARGING,
        {"charger_id": TEST_CHARGER_ID},
        blocking=True,
    )

    mock_coordinator.async_stop_charging.assert_called_once()


async def test_set_max_current_service(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test set max current service calls coordinator with value."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    await async_setup_services(hass)

    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_MAX_CURRENT,
        {"charger_id": TEST_CHARGER_ID, "current": 20},
        blocking=True,
    )

    mock_coordinator.async_set_max_current.assert_called_once_with(20)


async def test_set_solar_mode_service(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test set solar mode service calls coordinator with mode."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    await async_setup_services(hass)

    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_SOLAR_MODE,
        {"charger_id": TEST_CHARGER_ID, "mode": "eco"},
        blocking=True,
    )

    mock_coordinator.async_set_solar_mode.assert_called_once_with("1")


async def test_start_charging_service_raises_for_unknown_charger(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test start charging service raises ServiceValidationError for unknown charger."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    await async_setup_services(hass)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_START_CHARGING,
            {"charger_id": "does-not-exist"},
            blocking=True,
        )


async def test_stop_charging_service_raises_for_unknown_charger(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test stop charging service raises ServiceValidationError for unknown charger."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    await async_setup_services(hass)

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_STOP_CHARGING,
            {"charger_id": "does-not-exist"},
            blocking=True,
        )
