"""Tests for the Wellborne binary sensor platform."""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api.sse import SseLiveSnapshot
from custom_components.wellborne.binary_sensor import async_setup_entry
from custom_components.wellborne.const import DOMAIN

from .conftest import TEST_CHARGER_ID


def _connected_snapshot(*, power_w: float | None = 3680.0) -> SseLiveSnapshot:
    """Build a fresh, connected live snapshot (status>=3) for state-override tests."""
    return SseLiveSnapshot(
        power_w=power_w,
        current_l1=16.0,
        current_l2=16.0,
        current_l3=16.0,
        voltage_l1=230.0,
        voltage_l2=230.0,
        voltage_l3=230.0,
        energy_kwh=10.5,
        duration_seconds=5400,
        duration_minutes=90,
        cost=0.04,
        cost_text="0.04€",
        status=3,
        connected=True,
    )


@pytest.fixture
def mock_coordinator(mock_wellborne_data):
    """Create a mock coordinator (idle: no fresh live snapshot)."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.live_snapshot = None
    # Mock the available property from CoordinatorEntity
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


@pytest.fixture
def mock_coordinator_charging(mock_wellborne_data_charging):
    """Create a mock coordinator with charging active (REST path, no live snapshot)."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_charging
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.live_snapshot = None
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


@pytest.fixture
def mock_coordinator_unavailable(mock_wellborne_data):
    """Create a mock coordinator that is unavailable."""
    coordinator = MagicMock()
    coordinator.data = None
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = False
    coordinator.live_snapshot = None
    type(coordinator).available = PropertyMock(return_value=False)
    return coordinator


async def test_charging_sensor_state_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charging binary sensor shows OFF when not charging."""
    mock_config_entry.add_to_hass(hass)

    # Set up hass.data with the mock coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    # Capture entities added
    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the charging sensor
    charging_sensor = next(
        (e for e in entities_added if "charging" in e.unique_id and "vehicle" not in e.unique_id),
        None,
    )
    assert charging_sensor is not None

    # Check the charging sensor state is OFF
    assert charging_sensor.is_on is False


async def test_charging_sensor_state_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test charging binary sensor shows ON when charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")
    assert charging_sensor.is_on is True


async def test_charging_sensor_updates_when_charging_starts(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data,
) -> None:
    """Test charging binary sensor updates when charging starts."""
    mock_config_entry.add_to_hass(hass)

    # Create a coordinator mock with mutable data
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.live_snapshot = None

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")

    # Initially not charging
    assert charging_sensor.is_on is False

    # Simulate charging starting by updating the data
    coordinator.data.status.is_charging = True

    # Sensor should now be on
    assert charging_sensor.is_on is True


async def test_sensor_unavailable_when_coordinator_fails(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_unavailable,
) -> None:
    """Test sensor shows unavailable when coordinator fails."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_unavailable

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")

    # is_on should return None when data is None
    assert charging_sensor.is_on is None


async def test_binary_sensor_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test binary sensor has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")
    assert charging_sensor.unique_id == f"{TEST_CHARGER_ID}_charging"


async def test_binary_sensor_device_class(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test binary sensor has correct device class."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charging_sensor = next(
        (e for e in entities_added if "charging" in e.unique_id),
        None,
    )
    assert charging_sensor is not None
    assert charging_sensor.device_class.value == "battery_charging"


# =============================================================================
# Phase 1: Vehicle Connected Binary Sensor Tests
# =============================================================================


async def test_vehicle_connected_sensor_on_when_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test vehicle connected sensor shows ON when charging (vehicle must be connected)."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the vehicle connected sensor
    vehicle_connected_sensor = next(
        (e for e in entities_added if "vehicle_connected" in e.unique_id),
        None,
    )
    assert vehicle_connected_sensor is not None
    assert vehicle_connected_sensor.is_on is True
    assert vehicle_connected_sensor.device_class.value == "plug"


async def test_vehicle_connected_sensor_unknown_when_idle(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test vehicle connected sensor shows Unknown when idle (not charging).

    The REST API doesn't expose connector status, so we can't reliably determine
    if a vehicle is plugged in when not actively charging. Return None (Unknown).
    """
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the vehicle connected sensor
    vehicle_connected_sensor = next(
        (e for e in entities_added if "vehicle_connected" in e.unique_id),
        None,
    )
    assert vehicle_connected_sensor is not None
    # Returns None (Unknown) when not charging - API limitation
    assert vehicle_connected_sensor.is_on is None


# =============================================================================
# Bluetooth Enabled Binary Sensor Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_bluetooth(mock_wellborne_data):
    """Create a mock coordinator with Bluetooth enabled."""
    mock_wellborne_data.charger.bluetooth_enabled = True
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


async def test_bluetooth_enabled_sensor_on(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_bluetooth,
) -> None:
    """Test Bluetooth enabled sensor shows ON when Bluetooth is enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_bluetooth

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Should have 4 binary sensors now (including charger_online)
    assert len(entities_added) == 4

    # Find the Bluetooth enabled sensor
    bluetooth_sensor = next(
        (e for e in entities_added if "bluetooth_enabled" in e.unique_id),
        None,
    )
    assert bluetooth_sensor is not None
    assert bluetooth_sensor.is_on is True


async def test_bluetooth_enabled_sensor_off(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test Bluetooth enabled sensor shows OFF when Bluetooth is disabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the Bluetooth enabled sensor
    bluetooth_sensor = next(
        (e for e in entities_added if "bluetooth_enabled" in e.unique_id),
        None,
    )
    assert bluetooth_sensor is not None
    # Default mock_wellborne_data has bluetooth_enabled = False
    assert bluetooth_sensor.is_on is False


async def test_bluetooth_enabled_sensor_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_bluetooth,
) -> None:
    """Test Bluetooth enabled sensor has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_bluetooth

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    bluetooth_sensor = next(
        (e for e in entities_added if "bluetooth_enabled" in e.unique_id),
        None,
    )
    assert bluetooth_sensor is not None
    assert bluetooth_sensor.unique_id == f"{TEST_CHARGER_ID}_bluetooth_enabled"


# =============================================================================
# Charger Online Binary Sensor Tests
# =============================================================================


async def test_charger_online_sensor_is_on_when_coordinator_online(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charger_online sensor is_on follows coordinator.is_online when True."""
    mock_coordinator.is_online = True

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charger_online_sensor = next(
        (e for e in entities_added if e.entity_description.key == "charger_online"),
        None,
    )
    assert charger_online_sensor is not None
    assert charger_online_sensor.is_on is True


async def test_charger_online_sensor_is_off_when_coordinator_offline(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test charger_online sensor is_on follows coordinator.is_online when False."""
    mock_coordinator.is_online = False

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charger_online_sensor = next(
        (e for e in entities_added if e.entity_description.key == "charger_online"),
        None,
    )
    assert charger_online_sensor is not None
    assert charger_online_sensor.is_on is False


async def test_charger_online_sensor_does_not_depend_on_coordinator_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_unavailable,
) -> None:
    """Test charger_online reads coordinator.is_online even when data is None."""
    # coordinator_unavailable has data=None; we set is_online explicitly
    mock_coordinator_unavailable.is_online = True

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_unavailable

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    charger_online_sensor = next(
        (e for e in entities_added if e.entity_description.key == "charger_online"),
        None,
    )
    assert charger_online_sensor is not None
    # is_online=True regardless of data=None (special case in is_on property)
    assert charger_online_sensor.is_on is True


# =============================================================================
# Live SSE snapshot overrides REST for charging / vehicle_connected state
# =============================================================================


async def _setup_binary_sensors(hass, mock_config_entry, coordinator):
    """Set up the binary sensors with the given coordinator and return them."""
    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()
    return entities_added


async def test_charging_sensor_on_from_live_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Charging is ON from a fresh connected snapshot even when REST reports not charging."""
    # REST data says idle (mock_wellborne_data is not charging), live snapshot says connected.
    mock_coordinator.live_snapshot = _connected_snapshot()

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")
    assert charging_sensor.is_on is True


async def test_charging_sensor_on_from_live_snapshot_power_zero(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """A connected snapshot with power_w=0 (plugged, not drawing) still reads as charging."""
    mock_coordinator.live_snapshot = _connected_snapshot(power_w=0.0)

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")
    assert charging_sensor.is_on is True


async def test_charging_sensor_falls_back_to_rest_when_no_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """With no live snapshot, charging follows REST is_charging (idle -> off)."""
    mock_coordinator.live_snapshot = None

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    charging_sensor = next(e for e in entities_added if e.entity_description.key == "charging")
    assert charging_sensor.is_on is False


async def test_vehicle_connected_on_from_live_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Vehicle connected is ON from a fresh connected snapshot even when REST is idle."""
    mock_coordinator.live_snapshot = _connected_snapshot()

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    vehicle_connected = next(e for e in entities_added if e.entity_description.key == "vehicle_connected")
    assert vehicle_connected.is_on is True


async def test_vehicle_connected_on_from_live_snapshot_power_zero(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """A connected snapshot with power_w=0 still reports the vehicle as connected."""
    mock_coordinator.live_snapshot = _connected_snapshot(power_w=0.0)

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    vehicle_connected = next(e for e in entities_added if e.entity_description.key == "vehicle_connected")
    assert vehicle_connected.is_on is True


async def test_vehicle_connected_none_when_idle_and_no_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Without a live snapshot and idle REST, vehicle_connected stays Unknown (None)."""
    mock_coordinator.live_snapshot = None

    entities_added = await _setup_binary_sensors(hass, mock_config_entry, mock_coordinator)

    vehicle_connected = next(e for e in entities_added if e.entity_description.key == "vehicle_connected")
    assert vehicle_connected.is_on is None
