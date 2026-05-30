"""Tests for the Wellborne time platform."""

from __future__ import annotations

from datetime import time
from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.time import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_off_peak_time = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


# =============================================================================
# Off-Peak Weekday Start Time Tests
# =============================================================================


async def test_off_peak_weekday_start_time_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak weekday start time reflects current value."""
    # Set mock off-peak data
    mock_coordinator.data.off_peak.weekday_start = "22:00"

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    assert len(entities_added) == 3  # weekday_start, weekday_end, scheduled_start
    weekday_start = next(e for e in entities_added if e.entity_description.key == "off_peak_weekday_start")
    assert weekday_start.native_value == time(22, 0)


async def test_off_peak_weekday_start_time_set_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak weekday start time calls API when set."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    weekday_start = next(e for e in entities_added if e.entity_description.key == "off_peak_weekday_start")

    await weekday_start.async_set_value(time(23, 30))

    mock_coordinator.async_set_off_peak_time.assert_called_once()
    call_kwargs = mock_coordinator.async_set_off_peak_time.call_args.kwargs
    assert call_kwargs["weekday_start"] == "23:30"


async def test_off_peak_weekday_start_time_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak weekday start time has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    weekday_start = next(e for e in entities_added if e.entity_description.key == "off_peak_weekday_start")
    assert weekday_start.unique_id == f"{TEST_CHARGER_ID}_off_peak_weekday_start"


# =============================================================================
# Off-Peak Weekday End Time Tests
# =============================================================================


async def test_off_peak_weekday_end_time_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak weekday end time reflects current value."""
    mock_coordinator.data.off_peak.weekday_end = "06:00"

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    weekday_end = next(e for e in entities_added if e.entity_description.key == "off_peak_weekday_end")
    assert weekday_end.native_value == time(6, 0)


async def test_off_peak_weekday_end_time_set_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak weekday end time calls API when set."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    weekday_end = next(e for e in entities_added if e.entity_description.key == "off_peak_weekday_end")

    await weekday_end.async_set_value(time(7, 0))

    mock_coordinator.async_set_off_peak_time.assert_called_once()
    call_kwargs = mock_coordinator.async_set_off_peak_time.call_args.kwargs
    assert call_kwargs["weekday_end"] == "07:00"


# =============================================================================
# Scheduled Charging Start Time Tests
# =============================================================================


async def test_scheduled_start_time_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled start time reflects current value."""
    mock_coordinator.data.scheduled_charging.cycle_time = "23:00"
    mock_coordinator.async_set_scheduled_time = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    assert len(entities_added) == 3  # 2 off-peak (weekday) + 1 scheduled
    scheduled_start = next(e for e in entities_added if e.entity_description.key == "scheduled_start_time")
    assert scheduled_start.native_value == time(23, 0)


async def test_scheduled_start_time_set_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled start time calls API when set."""
    mock_coordinator.async_set_scheduled_time = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_start = next(e for e in entities_added if e.entity_description.key == "scheduled_start_time")

    await scheduled_start.async_set_value(time(22, 30))

    mock_coordinator.async_set_scheduled_time.assert_called_once_with(cycle_time="22:30")


async def test_scheduled_start_time_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled start time has correct unique ID."""
    mock_coordinator.async_set_scheduled_time = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_start = next(e for e in entities_added if e.entity_description.key == "scheduled_start_time")
    assert scheduled_start.unique_id == f"{TEST_CHARGER_ID}_scheduled_start_time"
