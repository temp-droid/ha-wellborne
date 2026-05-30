"""Tests for the Wellborne select platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.select import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_solar_mode = AsyncMock()
    return coordinator


@pytest.fixture
def mock_coordinator_eco_mode(mock_wellborne_data):
    """Create a mock coordinator with Eco solar mode."""
    mock_wellborne_data.status.solar_mode = "1"
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_solar_mode = AsyncMock()
    return coordinator


async def test_solar_mode_value_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test solar mode select shows Off when mode is 0."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the solar mode select
    solar_mode = next((e for e in entities_added if "solar_mode" in e.unique_id), None)
    assert solar_mode is not None

    # Should show "Off" for mode "0"
    assert solar_mode.current_option == "Off"


async def test_solar_mode_value_eco(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_eco_mode,
) -> None:
    """Test solar mode select shows Eco when mode is 1."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_eco_mode

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    solar_mode = next((e for e in entities_added if "solar_mode" in e.unique_id), None)
    assert solar_mode is not None

    # Should show "Eco" for mode "1"
    assert solar_mode.current_option == "Eco"


async def test_solar_mode_select(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test solar mode select calls API with new mode."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    solar_mode = next((e for e in entities_added if "solar_mode" in e.unique_id), None)
    assert solar_mode is not None

    # Select "Pure Solar" mode
    await solar_mode.async_select_option("Pure Solar")

    # Verify API was called with mode "2"
    mock_coordinator.async_set_solar_mode.assert_called_once_with("2")


async def test_solar_mode_options(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test solar mode select has Off/Eco/Pure Solar options."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    solar_mode = next((e for e in entities_added if "solar_mode" in e.unique_id), None)
    assert solar_mode is not None

    # Check available options
    assert solar_mode.options == ["Off", "Eco", "Pure Solar"]


async def test_select_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test select has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    solar_mode = next((e for e in entities_added if "solar_mode" in e.unique_id), None)
    assert solar_mode is not None

    assert solar_mode.unique_id == f"{TEST_CHARGER_ID}_solar_mode"
