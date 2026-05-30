"""Tests for the Wellborne Last Session sensors."""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfTime
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import LastSessionData, WellborneData
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.sensor import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_last_session() -> LastSessionData:
    """Create mock last session data."""
    return LastSessionData(
        energy=15.5,
        duration_minutes=120,
        start_time="2024-01-10 08:00:00",
        end_time="2024-01-10 10:00:00",
    )


@pytest.fixture
def mock_coordinator_with_last_session(
    mock_wellborne_data: WellborneData,
    mock_last_session: LastSessionData,
):
    """Create a mock coordinator with last session data."""
    mock_wellborne_data.last_session = mock_last_session
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


# =============================================================================
# Last Session Energy Tests
# =============================================================================


async def test_last_session_energy_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session energy reflects the value from last completed session."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_energy = next(e for e in entities_added if e.entity_description.key == "last_session_energy")
    assert last_session_energy.native_value == 15.5


async def test_last_session_energy_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session energy has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_energy = next(e for e in entities_added if e.entity_description.key == "last_session_energy")
    assert last_session_energy.unique_id == f"{TEST_CHARGER_ID}_last_session_energy"


async def test_last_session_energy_attributes(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session energy has correct device class and unit."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_energy = next(e for e in entities_added if e.entity_description.key == "last_session_energy")
    assert last_session_energy.device_class == SensorDeviceClass.ENERGY
    assert last_session_energy.native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR
    # device_class=energy forbids measurement; a per-session snapshot has no state_class
    assert last_session_energy.state_class is None


async def test_last_session_energy_none_when_no_session(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test last session energy returns None when no last session data."""
    mock_config_entry.add_to_hass(hass)

    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data  # No last_session set
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_energy = next(e for e in entities_added if e.entity_description.key == "last_session_energy")
    assert last_session_energy.native_value is None


# =============================================================================
# Last Session Duration Tests
# =============================================================================


async def test_last_session_duration_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session duration reflects the value from last completed session."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_duration = next(e for e in entities_added if e.entity_description.key == "last_session_duration")
    assert last_session_duration.native_value == 120


async def test_last_session_duration_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session duration has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_duration = next(e for e in entities_added if e.entity_description.key == "last_session_duration")
    assert last_session_duration.unique_id == f"{TEST_CHARGER_ID}_last_session_duration"


async def test_last_session_duration_attributes(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_last_session,
) -> None:
    """Test last session duration has correct device class and unit."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_last_session

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_duration = next(e for e in entities_added if e.entity_description.key == "last_session_duration")
    assert last_session_duration.device_class == SensorDeviceClass.DURATION
    assert last_session_duration.native_unit_of_measurement == UnitOfTime.MINUTES
    assert last_session_duration.state_class == SensorStateClass.MEASUREMENT


async def test_last_session_duration_none_when_no_session(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test last session duration returns None when no last session data."""
    mock_config_entry.add_to_hass(hass)

    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data  # No last_session set
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    last_session_duration = next(e for e in entities_added if e.entity_description.key == "last_session_duration")
    assert last_session_duration.native_value is None
