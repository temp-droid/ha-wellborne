"""Tests for the Wellborne number platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.components.number import NumberDeviceClass
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.number import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_max_current = AsyncMock()
    return coordinator


async def test_max_current_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current number shows current setting."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the max current number entity
    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    # Should show the current max current value (16.0 from mock_charger_status)
    assert max_current.native_value == 16.0


async def test_max_current_set(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current number calls API with new value."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    # Set a new value
    await max_current.async_set_native_value(20.0)

    # Verify API was called with correct value
    mock_coordinator.async_set_max_current.assert_called_once_with(20)


async def test_max_current_bounds(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current number respects 6-32A limits."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    # Check min and max values
    assert max_current.native_min_value == 6
    assert max_current.native_max_value == 32


async def test_max_current_step(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current number has 1A step."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    # Check step value
    assert max_current.native_step == 1


async def test_max_current_device_class(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current number has correct device class."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    assert max_current.device_class == NumberDeviceClass.CURRENT
    assert max_current.native_unit_of_measurement == UnitOfElectricCurrent.AMPERE


async def test_number_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test number has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_current = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current is not None

    assert max_current.unique_id == f"{TEST_CHARGER_ID}_max_current"


# =============================================================================
# Delay Time Number Entity Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_delay(mock_wellborne_data):
    """Create a mock coordinator with delay time set."""
    mock_wellborne_data.delayed_charging.delay_time = 3600  # 60 minutes in seconds (API stores seconds)
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_max_current = AsyncMock()
    coordinator.async_set_delay_time = AsyncMock()
    return coordinator


async def test_delay_time_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delay,
) -> None:
    """Test delay time number shows current setting."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delay

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 4 number entities: max_current, delay_time, max_power, load_balancing_current
    assert len(entities_added) == 4

    # Find the delay time number entity
    delay_time = next((e for e in entities_added if "delay_time" in e.unique_id), None)
    assert delay_time is not None

    # Should show the current delay time value (60 minutes)
    assert delay_time.native_value == 60


async def test_delay_time_set(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delay,
) -> None:
    """Test delay time number calls API with new value."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delay

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delay_time = next((e for e in entities_added if "delay_time" in e.unique_id), None)
    assert delay_time is not None

    # Set a new value
    await delay_time.async_set_native_value(120.0)

    # Verify API was called with correct value (in minutes)
    mock_coordinator_with_delay.async_set_delay_time.assert_called_once_with(120)


async def test_delay_time_bounds(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delay,
) -> None:
    """Test delay time number respects 0-1440 minute limits (24 hours)."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delay

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delay_time = next((e for e in entities_added if "delay_time" in e.unique_id), None)
    assert delay_time is not None

    # Check min and max values
    assert delay_time.native_min_value == 0
    assert delay_time.native_max_value == 1440  # 24 hours


async def test_delay_time_step(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delay,
) -> None:
    """Test delay time number has 1 minute step."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delay

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delay_time = next((e for e in entities_added if "delay_time" in e.unique_id), None)
    assert delay_time is not None

    # Check step value
    assert delay_time.native_step == 1


async def test_delay_time_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delay,
) -> None:
    """Test delay time number has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delay

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delay_time = next((e for e in entities_added if "delay_time" in e.unique_id), None)
    assert delay_time is not None

    assert delay_time.unique_id == f"{TEST_CHARGER_ID}_delay_time"


# =============================================================================
# Max Power Number Entity Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_max_power(mock_wellborne_data):
    """Create a mock coordinator with max power set."""
    mock_wellborne_data.status.max_power = 7400  # 7.4 kW
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_max_current = AsyncMock()
    coordinator.async_set_delay_time = AsyncMock()
    coordinator.async_set_max_power = AsyncMock()
    coordinator.async_set_load_balancing_current = AsyncMock()
    return coordinator


async def test_max_power_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_max_power,
) -> None:
    """Test max power number shows current setting."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_max_power

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 4 number entities: max_current, delay_time, max_power, load_balancing_current
    assert len(entities_added) == 4

    # Find the max power number entity
    max_power = next((e for e in entities_added if "max_power" in e.unique_id), None)
    assert max_power is not None

    # Should show the current max power value (7400 W)
    assert max_power.native_value == 7400


async def test_max_power_set(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_max_power,
) -> None:
    """Test max power number calls API with new value."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_max_power

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_power = next((e for e in entities_added if "max_power" in e.unique_id), None)
    assert max_power is not None

    # Set a new value
    await max_power.async_set_native_value(11000.0)

    # Verify API was called with correct value
    mock_coordinator_with_max_power.async_set_max_power.assert_called_once_with(11000)


async def test_max_power_bounds(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_max_power,
) -> None:
    """Test max power number respects 0-22000W limits."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_max_power

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_power = next((e for e in entities_added if "max_power" in e.unique_id), None)
    assert max_power is not None

    # Check min and max values
    assert max_power.native_min_value == 0
    assert max_power.native_max_value == 22000


async def test_max_power_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_max_power,
) -> None:
    """Test max power number has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_max_power

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    max_power = next((e for e in entities_added if "max_power" in e.unique_id), None)
    assert max_power is not None

    assert max_power.unique_id == f"{TEST_CHARGER_ID}_max_power"


# =============================================================================
# Load Balancing Current Number Entity Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_load_balancing_current(mock_wellborne_data):
    """Create a mock coordinator with load balancing current set."""
    mock_wellborne_data.load_balancing.max_current = 24  # 24A
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_max_current = AsyncMock()
    coordinator.async_set_delay_time = AsyncMock()
    coordinator.async_set_max_power = AsyncMock()
    coordinator.async_set_load_balancing_current = AsyncMock()
    return coordinator


async def test_load_balancing_current_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing_current,
) -> None:
    """Test load balancing current number shows current setting."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing_current

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the load balancing current number entity
    lb_current = next((e for e in entities_added if "load_balancing_current" in e.unique_id), None)
    assert lb_current is not None

    # Should show the current load balancing current value (24A)
    assert lb_current.native_value == 24


async def test_load_balancing_current_set(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing_current,
) -> None:
    """Test load balancing current number calls API with new value."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing_current

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lb_current = next((e for e in entities_added if "load_balancing_current" in e.unique_id), None)
    assert lb_current is not None

    # Set a new value
    await lb_current.async_set_native_value(28.0)

    # Verify API was called with correct value
    mock_coordinator_with_load_balancing_current.async_set_load_balancing_current.assert_called_once_with(28)


async def test_load_balancing_current_bounds(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing_current,
) -> None:
    """Test load balancing power number respects 1-100 limits."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing_current

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lb_current = next((e for e in entities_added if "load_balancing_current" in e.unique_id), None)
    assert lb_current is not None

    # Name is localized via translation_key (resolved by HA from strings.json)
    assert lb_current.entity_description.translation_key == "load_balancing_current"

    # Check min and max values
    assert lb_current.native_min_value == 1
    assert lb_current.native_max_value == 100


async def test_load_balancing_current_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing_current,
) -> None:
    """Test load balancing current number has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing_current

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    lb_current = next((e for e in entities_added if "load_balancing_current" in e.unique_id), None)
    assert lb_current is not None

    assert lb_current.unique_id == f"{TEST_CHARGER_ID}_load_balancing_current"
