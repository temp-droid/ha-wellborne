"""Tests for the Wellborne sensor platform."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, PropertyMock

from freezegun import freeze_time
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import WifiInfo
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.sensor import async_setup_entry

from .conftest import TEST_CHARGER_ID


@pytest.fixture
def mock_coordinator(mock_wellborne_data, mock_config_entry):
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.config_entry = mock_config_entry
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


@pytest.fixture
def mock_coordinator_charging(mock_wellborne_data_charging, mock_config_entry):
    """Create a mock coordinator with active charging."""
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data_charging
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    coordinator.config_entry = mock_config_entry
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


async def test_session_duration_sensor_shows_minutes_when_charging(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_session_start,
) -> None:
    """Test session duration sensor shows time since session started."""
    frozen_now = datetime(2024, 6, 15, 12, 0, 0, tzinfo=UTC)
    mock_coordinator_with_session_start.data.session_start_time = frozen_now - timedelta(minutes=90)

    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_session_start

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    with freeze_time(frozen_now):
        await async_setup_entry(hass, mock_config_entry, capture_entities)
        await hass.async_block_till_done()

        # Find the session duration sensor
        session_duration_sensor = next(
            (e for e in entities_added if "session_duration" in e.unique_id),
            None,
        )
        assert session_duration_sensor is not None
        # Session started exactly 90 minutes before frozen_now
        assert session_duration_sensor.native_value == 90
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
