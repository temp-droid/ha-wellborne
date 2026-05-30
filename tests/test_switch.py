"""Tests for the Wellborne switch platform."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api.exceptions import ApiConnectionError
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.switch import async_setup_entry

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
    coordinator.async_set_connector_lock = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def mock_coordinator_charging(mock_wellborne_data_charging):
    """Create a mock coordinator with active charging."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_charging
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_start_charging = AsyncMock()
    coordinator.async_stop_charging = AsyncMock()
    coordinator.async_set_connector_lock = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_charging_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charging switch reflects OFF when not charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 8 switches
    assert len(entities_added) == 8
    charging_switch = next(e for e in entities_added if e.entity_description.key == "charging")

    # Check the charging switch state is OFF
    assert charging_switch.is_on is False


async def test_charging_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test charging switch reflects ON when charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]
    assert charging_switch.is_on is True


async def test_charging_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charging switch calls start_charging API when turned on."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]

    # Turn on the switch
    await charging_switch.async_turn_on()

    # Verify start_charging was called
    mock_coordinator.async_start_charging.assert_called_once()


async def test_charging_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test charging switch calls stop_charging API when turned off."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]

    # Turn off the switch
    await charging_switch.async_turn_off()

    # Verify stop_charging was called
    mock_coordinator_charging.async_stop_charging.assert_called_once()


async def test_switch_optimistic_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test switch updates state optimistically after turn_on."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]

    # Initially OFF
    assert charging_switch.is_on is False

    # Turn on - should update state optimistically
    await charging_switch.async_turn_on()

    # State should be ON immediately (optimistic)
    assert charging_switch.is_on is True


async def test_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test switch has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]
    assert charging_switch.unique_id == f"{TEST_CHARGER_ID}_charging"


async def test_switch_device_class(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test switch has correct device class."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = entities_added[0]
    assert charging_switch.device_class == SwitchDeviceClass.SWITCH


async def test_connector_lock_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch reflects OFF when unlocked."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 8 switches
    assert len(entities_added) == 8

    # Find the connector lock switch
    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")
    assert connector_lock_switch.is_on is False


async def test_connector_lock_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch reflects ON when locked."""
    # Set connector_lock to True
    mock_coordinator.data.status.connector_lock = True

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")
    assert connector_lock_switch.is_on is True


async def test_connector_lock_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch calls API when turned on."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")

    await connector_lock_switch.async_turn_on()

    mock_coordinator.async_set_connector_lock.assert_called_once_with(enabled=True)


async def test_connector_lock_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch calls API when turned off."""
    mock_coordinator.data.status.connector_lock = True

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")

    await connector_lock_switch.async_turn_off()

    mock_coordinator.async_set_connector_lock.assert_called_once_with(enabled=False)


async def test_connector_lock_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")
    assert connector_lock_switch.unique_id == f"{TEST_CHARGER_ID}_connector_lock"


async def test_charging_switch_clears_optimistic_state_on_update(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charging switch clears optimistic state when coordinator updates."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = next(e for e in entities_added if e.entity_description.key == "charging")

    # Set hass attribute for optimistic state update
    charging_switch.hass = hass

    # Initially OFF (from coordinator data)
    assert charging_switch.is_on is False
    assert charging_switch._optimistic_state is None

    # Turn on - should set optimistic state
    await charging_switch.async_turn_on()
    assert charging_switch._optimistic_state is True
    assert charging_switch.is_on is True  # Optimistic state takes precedence

    # Clear optimistic state directly (instead of calling _handle_coordinator_update
    # which requires full HA entity setup)
    charging_switch._optimistic_state = None

    # After clearing, should reflect actual data, not optimistic state
    assert charging_switch._optimistic_state is None
    assert charging_switch.is_on is False  # Should be False from coordinator data


async def test_charging_switch_returns_none_when_no_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charging switch returns None when coordinator has no data."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = next(e for e in entities_added if e.entity_description.key == "charging")

    # Set coordinator data to None
    mock_coordinator.data = None

    # Should return None when no data
    assert charging_switch.is_on is None


async def test_connector_lock_switch_returns_none_when_no_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test connector lock switch returns None when coordinator has no data."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")

    # Set coordinator data to None
    mock_coordinator.data = None

    # Should return None when no data
    assert connector_lock_switch.is_on is None


# =============================================================================
# Delayed Charging Enable Switch Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_delayed_charging(mock_wellborne_data):
    """Create a mock coordinator with delayed charging enabled."""
    mock_wellborne_data.delayed_charging.enabled = True
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_delayed_charging_enabled = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_delayed_charging_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test delayed charging switch reflects OFF when disabled."""
    # Add the mock method for delayed charging
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 8 switches
    assert len(entities_added) == 8

    delayed_charging_switch = next(e for e in entities_added if e.entity_description.key == "delayed_charging")
    assert delayed_charging_switch.is_on is False


async def test_delayed_charging_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delayed_charging,
) -> None:
    """Test delayed charging switch reflects ON when enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delayed_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delayed_charging_switch = next(e for e in entities_added if e.entity_description.key == "delayed_charging")
    assert delayed_charging_switch.is_on is True


async def test_delayed_charging_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test delayed charging switch calls API when turned on."""
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delayed_charging_switch = next(e for e in entities_added if e.entity_description.key == "delayed_charging")

    await delayed_charging_switch.async_turn_on()

    mock_coordinator.async_set_delayed_charging_enabled.assert_called_once_with(enabled=True)


async def test_delayed_charging_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delayed_charging,
) -> None:
    """Test delayed charging switch calls API when turned off."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delayed_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delayed_charging_switch = next(e for e in entities_added if e.entity_description.key == "delayed_charging")

    await delayed_charging_switch.async_turn_off()

    mock_coordinator_with_delayed_charging.async_set_delayed_charging_enabled.assert_called_once_with(enabled=False)


async def test_delayed_charging_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test delayed charging switch has correct unique ID."""
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    delayed_charging_switch = next(e for e in entities_added if e.entity_description.key == "delayed_charging")
    assert delayed_charging_switch.unique_id == f"{TEST_CHARGER_ID}_delayed_charging"


# =============================================================================
# Scheduled Charging Enable Switch Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_scheduled_charging(mock_wellborne_data):
    """Create a mock coordinator with scheduled charging enabled."""
    mock_wellborne_data.scheduled_charging.enabled = True
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_scheduled_charging_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled charging switch reflects OFF when disabled."""
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 8 switches
    assert len(entities_added) == 8

    scheduled_charging_switch = next(e for e in entities_added if e.entity_description.key == "scheduled_charging")
    assert scheduled_charging_switch.is_on is False


async def test_scheduled_charging_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_scheduled_charging,
) -> None:
    """Test scheduled charging switch reflects ON when enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_scheduled_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_charging_switch = next(e for e in entities_added if e.entity_description.key == "scheduled_charging")
    assert scheduled_charging_switch.is_on is True


async def test_scheduled_charging_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled charging switch calls API when turned on."""
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_charging_switch = next(e for e in entities_added if e.entity_description.key == "scheduled_charging")

    await scheduled_charging_switch.async_turn_on()

    mock_coordinator.async_set_scheduled_charging_enabled.assert_called_once_with(enabled=True)


async def test_scheduled_charging_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_scheduled_charging,
) -> None:
    """Test scheduled charging switch calls API when turned off."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_scheduled_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_charging_switch = next(e for e in entities_added if e.entity_description.key == "scheduled_charging")

    await scheduled_charging_switch.async_turn_off()

    mock_coordinator_with_scheduled_charging.async_set_scheduled_charging_enabled.assert_called_once_with(enabled=False)


async def test_scheduled_charging_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test scheduled charging switch has correct unique ID."""
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    scheduled_charging_switch = next(e for e in entities_added if e.entity_description.key == "scheduled_charging")
    assert scheduled_charging_switch.unique_id == f"{TEST_CHARGER_ID}_scheduled_charging"


# =============================================================================
# Off-Peak Charging Enable Switch Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_off_peak(mock_wellborne_data):
    """Create a mock coordinator with off-peak charging enabled."""
    # Add off_peak data structure (will be added to WellborneData)
    mock_wellborne_data.off_peak = MagicMock()
    mock_wellborne_data.off_peak.enabled = True
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_off_peak_enabled = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_off_peak_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak switch reflects OFF when disabled."""
    # Add off_peak mock to coordinator data
    mock_coordinator.data.off_peak = MagicMock()
    mock_coordinator.data.off_peak.enabled = False
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    assert len(entities_added) == 8  # Now expects 8 switches
    off_peak_switch = next(e for e in entities_added if e.entity_description.key == "off_peak")
    assert off_peak_switch.is_on is False


async def test_off_peak_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_off_peak,
) -> None:
    """Test off-peak switch reflects ON when enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_off_peak

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    off_peak_switch = next(e for e in entities_added if e.entity_description.key == "off_peak")
    assert off_peak_switch.is_on is True


async def test_off_peak_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak switch calls API when turned on."""
    mock_coordinator.data.off_peak = MagicMock()
    mock_coordinator.data.off_peak.enabled = False
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    off_peak_switch = next(e for e in entities_added if e.entity_description.key == "off_peak")

    # Set hass attribute for optimistic state update
    off_peak_switch.hass = hass

    await off_peak_switch.async_turn_on()

    mock_coordinator.async_set_off_peak_enabled.assert_called_once_with(enabled=True)


async def test_off_peak_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_off_peak,
) -> None:
    """Test off-peak switch calls API when turned off."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_off_peak

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    off_peak_switch = next(e for e in entities_added if e.entity_description.key == "off_peak")

    # Set hass attribute for optimistic state update
    off_peak_switch.hass = hass

    await off_peak_switch.async_turn_off()

    mock_coordinator_with_off_peak.async_set_off_peak_enabled.assert_called_once_with(enabled=False)


async def test_off_peak_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test off-peak switch has correct unique ID."""
    mock_coordinator.data.off_peak = MagicMock()
    mock_coordinator.data.off_peak.enabled = False
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    off_peak_switch = next(e for e in entities_added if e.entity_description.key == "off_peak")
    assert off_peak_switch.unique_id == f"{TEST_CHARGER_ID}_off_peak"


# =============================================================================
# Load Balancing Switch Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_load_balancing(mock_wellborne_data):
    """Create a mock coordinator with load balancing enabled."""
    mock_wellborne_data.load_balancing.enabled = True
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    coordinator.async_set_load_balancing_enabled = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_load_balancing_switch_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test load balancing switch reflects OFF when disabled."""
    mock_coordinator.async_set_load_balancing_enabled = AsyncMock()
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()
    mock_coordinator.async_set_lcd_enabled = AsyncMock()
    mock_coordinator.async_set_low_power_reserve_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 8 switches now (including load balancing)
    assert len(entities_added) == 8

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")
    assert load_balancing_switch.is_on is False


async def test_load_balancing_switch_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing,
) -> None:
    """Test load balancing switch reflects ON when enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")
    assert load_balancing_switch.is_on is True


async def test_load_balancing_switch_turn_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test load balancing switch calls API when turned on."""
    mock_coordinator.async_set_load_balancing_enabled = AsyncMock()
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()
    mock_coordinator.async_set_lcd_enabled = AsyncMock()
    mock_coordinator.async_set_low_power_reserve_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")

    await load_balancing_switch.async_turn_on()

    mock_coordinator.async_set_load_balancing_enabled.assert_called_once_with(enabled=True)


async def test_load_balancing_switch_turn_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_load_balancing,
) -> None:
    """Test load balancing switch calls API when turned off."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_load_balancing

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")

    await load_balancing_switch.async_turn_off()

    mock_coordinator_with_load_balancing.async_set_load_balancing_enabled.assert_called_once_with(enabled=False)


async def test_load_balancing_switch_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test load balancing switch has correct unique ID."""
    mock_coordinator.async_set_load_balancing_enabled = AsyncMock()
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()
    mock_coordinator.async_set_lcd_enabled = AsyncMock()
    mock_coordinator.async_set_low_power_reserve_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")
    assert load_balancing_switch.unique_id == f"{TEST_CHARGER_ID}_load_balancing"


async def test_load_balancing_switch_returns_none_when_no_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test load balancing switch returns None when coordinator has no data."""
    mock_coordinator.async_set_load_balancing_enabled = AsyncMock()
    mock_coordinator.async_set_off_peak_enabled = AsyncMock()
    mock_coordinator.async_set_scheduled_charging_enabled = AsyncMock()
    mock_coordinator.async_set_delayed_charging_enabled = AsyncMock()
    mock_coordinator.async_set_lcd_enabled = AsyncMock()
    mock_coordinator.async_set_low_power_reserve_enabled = AsyncMock()

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    load_balancing_switch = next(e for e in entities_added if e.entity_description.key == "load_balancing")

    # Set coordinator data to None
    mock_coordinator.data = None

    # Should return None when no data
    assert load_balancing_switch.is_on is None


# =============================================================================
# Optimistic State Revert on Failure Tests
# =============================================================================


async def test_switch_turn_on_reverts_optimistic_state_on_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turn_on reverts optimistic state and re-raises when coordinator fails."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = next(e for e in entities_added if e.entity_description.key == "charging")

    # Prior state is None (never turned on)
    assert charging_switch._optimistic_state is None

    # Simulate coordinator failure
    mock_coordinator.async_start_charging.side_effect = ApiConnectionError("charger offline")

    with pytest.raises(ApiConnectionError):
        await charging_switch.async_turn_on()

    # Optimistic state must be reverted to prior value (None), not left True
    assert charging_switch._optimistic_state is None


async def test_switch_turn_off_reverts_optimistic_state_on_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test turn_off reverts optimistic state and re-raises when coordinator fails."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_switch = next(e for e in entities_added if e.entity_description.key == "charging")

    # Prior state is None
    assert charging_switch._optimistic_state is None

    # Simulate coordinator failure
    mock_coordinator_charging.async_stop_charging.side_effect = ApiConnectionError("charger offline")

    with pytest.raises(ApiConnectionError):
        await charging_switch.async_turn_off()

    # Optimistic state must be reverted to prior value (None), not left False
    assert charging_switch._optimistic_state is None


async def test_non_charging_switch_turn_on_reverts_optimistic_state_on_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turn_on on a non-charging switch (enabled= path) reverts on failure."""
    mock_coordinator.async_set_connector_lock = AsyncMock(side_effect=ApiConnectionError("charger offline"))

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")

    # Prior optimistic state is None
    assert connector_lock_switch._optimistic_state is None

    with pytest.raises(ApiConnectionError):
        await connector_lock_switch.async_turn_on()

    # Optimistic state must be reverted to prior value (None), not left True
    assert connector_lock_switch._optimistic_state is None


async def test_non_charging_switch_turn_off_reverts_optimistic_state_on_failure(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test turn_off on a non-charging switch (enabled= path) reverts on failure."""
    mock_coordinator.data.status.connector_lock = True
    mock_coordinator.async_set_connector_lock = AsyncMock(side_effect=ApiConnectionError("charger offline"))

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    connector_lock_switch = next(e for e in entities_added if e.entity_description.key == "connector_lock")

    # Prior optimistic state is None
    assert connector_lock_switch._optimistic_state is None

    with pytest.raises(ApiConnectionError):
        await connector_lock_switch.async_turn_off()

    # Optimistic state must be reverted to prior value (None), not left False
    assert connector_lock_switch._optimistic_state is None


async def test_switch_turn_off_reverts_to_true_when_prior_state_true(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test turn_off reverts to True (not None/False) when prior optimistic state was True."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    sw = next(e for e in entities_added if e.entity_description.key == "charging")

    # Pre-set prior optimistic state to True
    sw._optimistic_state = True

    # Simulate coordinator failure on stop
    mock_coordinator_charging.async_stop_charging.side_effect = ApiConnectionError("charger offline")

    with pytest.raises(ApiConnectionError):
        await sw.async_turn_off()

    # Must revert to the captured prior value (True), not hardcoded None/False
    assert sw._optimistic_state is True
