"""Tests for the Wellborne sensor platform."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import MagicMock, PropertyMock

from freezegun import freeze_time
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import WifiInfo
from custom_components.wellborne.api.sse import SseLiveSnapshot
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.sensor import async_setup_entry

from .conftest import TEST_CHARGER_ID


def _charging_snapshot(*, duration_minutes: int = 90) -> SseLiveSnapshot:
    """Build a fresh, connected live snapshot mirroring mock_meter_values.

    Values match the REST mock_meter_values fixture (power 3680 W, voltage 230 V, current 16 A,
    energy 10.5 kWh) so the live-path assertions stay readable.
    """
    return SseLiveSnapshot(
        power_w=3680.0,
        current_l1=16.0,
        current_l2=16.0,
        current_l3=16.0,
        voltage_l1=230.0,
        voltage_l2=230.0,
        voltage_l3=230.0,
        energy_kwh=10.5,
        duration_seconds=duration_minutes * 60,
        duration_minutes=duration_minutes,
        cost=0.04,
        cost_text="0.04€",
        status=3,
        connected=True,
    )


@pytest.fixture
def mock_coordinator(mock_wellborne_data, mock_config_entry):
    """Create a mock coordinator (idle: no fresh live snapshot)."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.config_entry = mock_config_entry
    coordinator.live_snapshot = None
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


@pytest.fixture
def mock_coordinator_charging(mock_wellborne_data_charging, mock_config_entry):
    """Create a mock coordinator with active charging and a fresh live snapshot."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_charging
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.config_entry = mock_config_entry
    coordinator.live_snapshot = _charging_snapshot()
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


async def test_power_sensor(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test power sensor shows charging power."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the power sensor
    power_sensor = next((e for e in entities_added if "power" in e.unique_id), None)
    assert power_sensor is not None
    assert power_sensor.native_value == 3680.0  # From mock_meter_values
    assert power_sensor.device_class == SensorDeviceClass.POWER
    assert power_sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert power_sensor.state_class == SensorStateClass.MEASUREMENT


async def test_energy_sensor(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test energy sensor shows energy delivered."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the energy sensor
    energy_sensor = next((e for e in entities_added if "energy" in e.unique_id), None)
    assert energy_sensor is not None
    assert energy_sensor.native_value == 10.5  # From mock_meter_values
    assert energy_sensor.device_class == SensorDeviceClass.ENERGY
    assert energy_sensor.native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR
    assert energy_sensor.state_class == SensorStateClass.TOTAL_INCREASING


async def test_voltage_sensor(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test voltage sensor shows L1 voltage."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the voltage sensor (L1)
    voltage_sensor = next(
        (e for e in entities_added if "voltage" in e.unique_id and "l2" not in e.unique_id and "l3" not in e.unique_id),
        None,
    )
    assert voltage_sensor is not None
    assert voltage_sensor.native_value == 230.0  # From mock_meter_values
    assert voltage_sensor.device_class == SensorDeviceClass.VOLTAGE
    assert voltage_sensor.native_unit_of_measurement == UnitOfElectricPotential.VOLT


async def test_current_sensor(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test current sensor shows L1 current."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the current sensor (L1)
    current_sensor = next(
        (
            e
            for e in entities_added
            if "current" in e.unique_id
            and "l2" not in e.unique_id
            and "l3" not in e.unique_id
            and "max" not in e.unique_id
        ),
        None,
    )
    assert current_sensor is not None
    assert current_sensor.native_value == 16.0  # From mock_meter_values
    assert current_sensor.device_class == SensorDeviceClass.CURRENT
    assert current_sensor.native_unit_of_measurement == UnitOfElectricCurrent.AMPERE


async def test_sensors_unavailable_when_not_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test meter sensors return None when not charging (no meter values)."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the power sensor
    power_sensor = next((e for e in entities_added if "power" in e.unique_id), None)
    assert power_sensor is not None
    # Should be None when not charging (no meter values)
    assert power_sensor.native_value is None


async def test_max_current_sensor(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test max current sensor shows configured max current."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the max current sensor
    max_current_sensor = next((e for e in entities_added if "max_current" in e.unique_id), None)
    assert max_current_sensor is not None
    assert max_current_sensor.native_value == 16.0  # From mock_charger_status
    assert max_current_sensor.device_class == SensorDeviceClass.CURRENT
    assert max_current_sensor.native_unit_of_measurement == UnitOfElectricCurrent.AMPERE


async def test_sensor_unique_ids(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test sensors have correct unique IDs."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Check that all entities have unique IDs starting with the charger ID
    for entity in entities_added:
        assert entity.unique_id.startswith(TEST_CHARGER_ID)


# =============================================================================
# Phase 1: Session Duration Sensor Tests
# =============================================================================


async def test_session_duration_sensor_from_live_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Session duration comes from the live snapshot (charingTimeText), NOT now - start.

    Regression guard for the 177h bug: the value is read from the fresh SSE snapshot's
    duration_minutes (parsed from charingTimeText), independent of any wall clock.
    """
    mock_coordinator_charging.live_snapshot = _charging_snapshot(duration_minutes=42)

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    # A wildly different wall clock must NOT affect the duration (proves it is snapshot-driven).
    with freeze_time(datetime(2030, 1, 1, 0, 0, 0, tzinfo=UTC)):
        await async_setup_entry(hass, mock_config_entry, capture_entities)
        await hass.async_block_till_done()

        session_duration_sensor = next(
            (e for e in entities_added if "session_duration" in e.unique_id),
            None,
        )
        assert session_duration_sensor is not None
        assert session_duration_sensor.native_value == 42
        assert session_duration_sensor.device_class == SensorDeviceClass.DURATION
        assert session_duration_sensor.native_unit_of_measurement == "min"


async def test_session_duration_sensor_none_when_not_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test session duration sensor returns None when not charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the session duration sensor
    session_duration_sensor = next(
        (e for e in entities_added if "session_duration" in e.unique_id),
        None,
    )
    assert session_duration_sensor is not None
    # Should be None when not charging
    assert session_duration_sensor.native_value is None


# =============================================================================
# Phase 1: Charger Status Text Sensor Tests
# =============================================================================


async def test_status_sensor_shows_charging_when_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test status sensor shows 'charging' when actively charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the status sensor
    status_sensor = next(
        (e for e in entities_added if e.unique_id.endswith("_status")),
        None,
    )
    assert status_sensor is not None
    assert status_sensor.native_value == "charging"
    assert status_sensor.device_class == SensorDeviceClass.ENUM


async def test_status_sensor_shows_idle_when_not_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test status sensor shows 'idle' when not charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the status sensor
    status_sensor = next(
        (e for e in entities_added if e.unique_id.endswith("_status")),
        None,
    )
    assert status_sensor is not None
    assert status_sensor.native_value == "idle"


async def test_status_sensor_charging_from_live_snapshot_when_rest_idle(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """A fresh connected snapshot overrides idle REST data -> status 'charging'."""
    # mock_coordinator wraps mock_wellborne_data (is_charging False) but has a live snapshot.
    mock_coordinator.live_snapshot = _charging_snapshot()

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    status_sensor = next((e for e in entities_added if e.unique_id.endswith("_status")), None)
    assert status_sensor is not None
    assert status_sensor.native_value == "charging"


async def test_status_sensor_charging_from_live_snapshot_power_zero(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """A connected snapshot with power_w=0 (plugged, not drawing) still reads 'charging'."""
    mock_coordinator.live_snapshot = replace(_charging_snapshot(), power_w=0.0)

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    status_sensor = next((e for e in entities_added if e.unique_id.endswith("_status")), None)
    assert status_sensor is not None
    assert status_sensor.native_value == "charging"


async def test_status_sensor_falls_back_to_rest_when_no_snapshot(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """With no live snapshot, status follows REST (idle data -> 'idle')."""
    mock_coordinator.live_snapshot = None

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    status_sensor = next((e for e in entities_added if e.unique_id.endswith("_status")), None)
    assert status_sensor is not None
    assert status_sensor.native_value == "idle"


async def test_status_sensor_shows_pending_when_delayed_charging_enabled(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_delayed_charging,
) -> None:
    """Test status sensor shows 'pending' when delayed charging is enabled."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_delayed_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the status sensor
    status_sensor = next(
        (e for e in entities_added if e.unique_id.endswith("_status")),
        None,
    )
    assert status_sensor is not None
    assert status_sensor.native_value == "pending"


# =============================================================================
# Phase 2: Added Range Sensor Tests
# =============================================================================


async def test_added_range_sensor_calculates_km_from_energy(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test added range sensor calculates km from session energy."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the added range sensor
    added_range_sensor = next(
        (e for e in entities_added if "added_range" in e.unique_id),
        None,
    )
    assert added_range_sensor is not None
    # Energy is 10.5 kWh, default efficiency is 6 km/kWh = 63 km
    assert added_range_sensor.native_value == 63.0
    assert added_range_sensor.device_class == SensorDeviceClass.DISTANCE
    assert added_range_sensor.native_unit_of_measurement == "km"


async def test_added_range_sensor_none_when_not_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test added range sensor returns None when not charging (no meter values)."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the added range sensor
    added_range_sensor = next(
        (e for e in entities_added if "added_range" in e.unique_id),
        None,
    )
    assert added_range_sensor is not None
    # Should be None when not charging (no meter values)
    assert added_range_sensor.native_value is None


# =============================================================================
# Coverage Tests: Sensors returning None when not charging
# =============================================================================


async def test_meter_value_sensors_none_when_not_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator,
) -> None:
    """Test all meter-value-dependent sensors return None when not charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Power sensor should be None
    power_sensor = next(e for e in entities_added if e.entity_description.key == "power")
    assert power_sensor.native_value is None

    # Energy sensor should be None
    energy_sensor = next(e for e in entities_added if e.entity_description.key == "energy")
    assert energy_sensor.native_value is None

    # Voltage sensors should be None
    voltage_sensor = next(e for e in entities_added if e.entity_description.key == "voltage")
    assert voltage_sensor.native_value is None

    voltage_l2_sensor = next(e for e in entities_added if e.entity_description.key == "voltage_l2")
    assert voltage_l2_sensor.native_value is None

    voltage_l3_sensor = next(e for e in entities_added if e.entity_description.key == "voltage_l3")
    assert voltage_l3_sensor.native_value is None

    # Current sensors should be None
    current_sensor = next(e for e in entities_added if e.entity_description.key == "current")
    assert current_sensor.native_value is None

    current_l2_sensor = next(e for e in entities_added if e.entity_description.key == "current_l2")
    assert current_l2_sensor.native_value is None

    current_l3_sensor = next(e for e in entities_added if e.entity_description.key == "current_l3")
    assert current_l3_sensor.native_value is None


# =============================================================================
# WiFi Sensors Tests
# =============================================================================


@pytest.fixture
def mock_coordinator_with_wifi(mock_wellborne_data):
    """Create a mock coordinator with WiFi info."""
    mock_wellborne_data.wifi_info = WifiInfo(ssid="MyHomeNetwork", signal=-65)
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


async def test_wifi_ssid_sensor_value(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_wifi,
) -> None:
    """Test WiFi SSID sensor shows network name."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_wifi

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # Find the WiFi SSID sensor
    wifi_ssid_sensor = next(
        (e for e in entities_added if "wifi_ssid" in e.unique_id),
        None,
    )
    assert wifi_ssid_sensor is not None
    assert wifi_ssid_sensor.native_value == "MyHomeNetwork"


async def test_wifi_ssid_sensor_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_wifi,
) -> None:
    """Test WiFi SSID sensor has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_wifi

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    wifi_ssid_sensor = next(
        (e for e in entities_added if "wifi_ssid" in e.unique_id),
        None,
    )
    assert wifi_ssid_sensor is not None
    assert wifi_ssid_sensor.unique_id == f"{TEST_CHARGER_ID}_wifi_ssid"


# =============================================================================
# L2/L3 Voltage and Current Sensors (non-None branch)
# =============================================================================


# =============================================================================
# Connection Status (diagnostic enum) Sensor Tests
# =============================================================================


def _make_connection_status_coordinator(connection_status: str, *, data) -> MagicMock:
    """Build a mock coordinator exposing a connection_status property."""
    coordinator = MagicMock()
    coordinator.data = data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.connection_status = connection_status
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


async def test_connection_status_sensor_options_and_metadata(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data,
) -> None:
    """Test connection_status sensor exposes the exact options, enum device class and diagnostic category."""
    coordinator = _make_connection_status_coordinator("online", data=mock_wellborne_data)

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    sensor = next((e for e in entities_added if e.entity_description.key == "connection_status"), None)
    assert sensor is not None
    assert sensor.unique_id == f"{TEST_CHARGER_ID}_connection_status"
    assert sensor.device_class == SensorDeviceClass.ENUM
    assert sensor.options == ["online", "charger_offline", "cloud_unreachable"]
    assert sensor.entity_description.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == "online"


@pytest.mark.parametrize(
    "status",
    ["online", "charger_offline", "cloud_unreachable"],
)
async def test_connection_status_sensor_reflects_coordinator_property(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data,
    status: str,
) -> None:
    """Test connection_status sensor reports the coordinator property value."""
    coordinator = _make_connection_status_coordinator(status, data=mock_wellborne_data)

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    sensor = next((e for e in entities_added if e.entity_description.key == "connection_status"), None)
    assert sensor is not None
    assert sensor.native_value == status


async def test_connection_status_sensor_available_without_data(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test connection_status sensor reports its value and stays available even when data is None."""
    coordinator = _make_connection_status_coordinator("cloud_unreachable", data=None)

    mock_config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = coordinator

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    sensor = next((e for e in entities_added if e.entity_description.key == "connection_status"), None)
    assert sensor is not None
    # Value comes from coordinator.connection_status, not coordinator.data
    assert sensor.native_value == "cloud_unreachable"
    # Must stay available even with no data (like charger_online)
    assert sensor.available is True


async def test_l2_l3_sensors_return_values_when_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_charging,
) -> None:
    """Test L2/L3 voltage and current sensors return meter values when charging."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_charging

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    # voltage_l2 — from mock_meter_values.voltage_l2 = 230.0
    voltage_l2 = next(e for e in entities_added if e.entity_description.key == "voltage_l2")
    assert voltage_l2.native_value == 230.0
    assert voltage_l2.device_class == SensorDeviceClass.VOLTAGE
    assert voltage_l2.native_unit_of_measurement == UnitOfElectricPotential.VOLT

    # voltage_l3 — from mock_meter_values.voltage_l3 = 230.0
    voltage_l3 = next(e for e in entities_added if e.entity_description.key == "voltage_l3")
    assert voltage_l3.native_value == 230.0

    # current_l2 — from mock_meter_values.current_l2 = 16.0
    current_l2 = next(e for e in entities_added if e.entity_description.key == "current_l2")
    assert current_l2.native_value == 16.0
    assert current_l2.device_class == SensorDeviceClass.CURRENT
    assert current_l2.native_unit_of_measurement == UnitOfElectricCurrent.AMPERE

    # current_l3 — from mock_meter_values.current_l3 = 16.0
    current_l3 = next(e for e in entities_added if e.entity_description.key == "current_l3")
    assert current_l3.native_value == 16.0
