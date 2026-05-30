"""Tests for the Wellborne configuration switches (LCD, Low Power Reserve)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import WellborneData
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.switch import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data: WellborneData):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_lcd_enabled = AsyncMock()
    coordinator.async_set_low_power_reserve_enabled = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


# =============================================================================
# LCD Enable Switch Tests
# =============================================================================


async def test_lcd_switch_reflects_current_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test LCD switch reflects current LCD enabled state."""
    # LCD is enabled by default in mock_charger_status
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lcd_switch = next(e for e in entities_added if e.entity_description.key == "lcd_enabled")
    assert lcd_switch.is_on is True


async def test_lcd_switch_turn_on_calls_coordinator(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turning on LCD switch calls coordinator method."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lcd_switch = next(e for e in entities_added if e.entity_description.key == "lcd_enabled")

    await lcd_switch.async_turn_on()

    mock_coordinator.async_set_lcd_enabled.assert_called_once_with(enabled=True)


async def test_lcd_switch_turn_off_calls_coordinator(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turning off LCD switch calls coordinator method."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lcd_switch = next(e for e in entities_added if e.entity_description.key == "lcd_enabled")

    await lcd_switch.async_turn_off()

    mock_coordinator.async_set_lcd_enabled.assert_called_once_with(enabled=False)


async def test_lcd_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test LCD switch has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lcd_switch = next(e for e in entities_added if e.entity_description.key == "lcd_enabled")
    assert lcd_switch.unique_id == f"{TEST_CHARGER_ID}_lcd_enabled"


# =============================================================================
# Low Power Reserve Switch Tests
# =============================================================================


async def test_low_power_reserve_switch_reflects_current_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test Low Power Reserve switch reflects current state."""
    # Low power reserve is disabled by default in mock_charger_status
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lpr_switch = next(e for e in entities_added if e.entity_description.key == "low_power_reserve")
    assert lpr_switch.is_on is False


async def test_low_power_reserve_switch_turn_on_calls_coordinator(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turning on Low Power Reserve switch calls coordinator method."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lpr_switch = next(e for e in entities_added if e.entity_description.key == "low_power_reserve")

    await lpr_switch.async_turn_on()

    mock_coordinator.async_set_low_power_reserve_enabled.assert_called_once_with(enabled=True)


async def test_low_power_reserve_switch_turn_off_calls_coordinator(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turning off Low Power Reserve switch calls coordinator method."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lpr_switch = next(e for e in entities_added if e.entity_description.key == "low_power_reserve")

    await lpr_switch.async_turn_off()

    mock_coordinator.async_set_low_power_reserve_enabled.assert_called_once_with(enabled=False)


async def test_low_power_reserve_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test Low Power Reserve switch has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lpr_switch = next(e for e in entities_added if e.entity_description.key == "low_power_reserve")
    assert lpr_switch.unique_id == f"{TEST_CHARGER_ID}_low_power_reserve"
