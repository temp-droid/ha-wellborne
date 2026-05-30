"""Tests for the Wellborne Monthly/Yearly statistics sensors."""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.wellborne.api import MonthlyStatistics, WellborneData, YearlyStatistics
from custom_components.wellborne.const import DOMAIN
from custom_components.wellborne.sensor import (
    SENSOR_DESCRIPTIONS,
    WellborneSensor,
    _start_of_month,
    _start_of_year,
    async_setup_entry,
)

from .conftest import TEST_CHARGER_ID

# =============================================================================
# state_class / last_reset correctness tests (Task 1)
# =============================================================================


def _desc(key: str):
    """Return the sensor description for the given key."""
    return next(d for d in SENSOR_DESCRIPTIONS if d.key == key)


def test_last_session_energy_is_measurement_not_total():
    assert _desc("last_session_energy").state_class == SensorStateClass.MEASUREMENT


def test_last_session_duration_is_measurement_not_total():
    assert _desc("last_session_duration").state_class == SensorStateClass.MEASUREMENT


def test_yearly_energy_total_has_last_reset():
    d = _desc("yearly_energy")
    assert d.state_class == SensorStateClass.TOTAL
    assert d.last_reset_fn is not None


def test_start_of_year_is_local_midnight_jan_first():
    result = _start_of_year()
    assert (result.month, result.day) == (1, 1)
    assert (result.hour, result.minute, result.second) == (0, 0, 0)
    assert result.tzinfo is not None


def test_last_reset_property_returns_anchor_for_periodic_sensor():
    coordinator = MagicMock()
    coordinator.charger_id = TEST_CHARGER_ID
    sensor = WellborneSensor(coordinator, _desc("monthly_energy"))
    assert sensor.last_reset == _start_of_month()


def test_last_reset_property_is_none_for_non_periodic_sensor():
    coordinator = MagicMock()
    coordinator.charger_id = TEST_CHARGER_ID
    sensor = WellborneSensor(coordinator, _desc("last_session_energy"))
    assert sensor.last_reset is None


@pytest.fixture
def mock_monthly_statistics() -> MonthlyStatistics:
    """Create mock monthly statistics."""
    return MonthlyStatistics(
        total_energy=125.5,
        session_count=12,
        month="2024-01",
    )


@pytest.fixture
def mock_yearly_statistics() -> YearlyStatistics:
    """Create mock yearly statistics."""
    return YearlyStatistics(
        total_energy=1250.75,
        session_count=120,
        year="2024",
    )


@pytest.fixture
def mock_coordinator_with_statistics(
    mock_wellborne_data: WellborneData,
    mock_monthly_statistics: MonthlyStatistics,
    mock_yearly_statistics: YearlyStatistics,
):
    """Create a mock coordinator with statistics data."""
    mock_wellborne_data.monthly_statistics = mock_monthly_statistics
    mock_wellborne_data.yearly_statistics = mock_yearly_statistics
    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data
    coordinator.charger_id = TEST_CHARGER_ID
    coordinator.last_update_success = True
    type(coordinator).available = PropertyMock(return_value=True)
    return coordinator


# =============================================================================
# Monthly Energy Statistics Tests
# =============================================================================


async def test_monthly_energy_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test monthly energy sensor reflects the total energy for current month."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    monthly_energy = next(e for e in entities_added if e.entity_description.key == "monthly_energy")
    assert monthly_energy.native_value == 125.5


async def test_monthly_energy_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test monthly energy sensor has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    monthly_energy = next(e for e in entities_added if e.entity_description.key == "monthly_energy")
    assert monthly_energy.unique_id == f"{TEST_CHARGER_ID}_monthly_energy"


async def test_monthly_energy_attributes(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test monthly energy sensor has correct device class and unit."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    monthly_energy = next(e for e in entities_added if e.entity_description.key == "monthly_energy")
    assert monthly_energy.device_class == SensorDeviceClass.ENERGY
    assert monthly_energy.native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR
    assert monthly_energy.state_class == SensorStateClass.TOTAL


async def test_monthly_energy_none_when_no_statistics(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test monthly energy sensor returns None when no statistics data."""
    mock_config_entry.add_to_hass(hass)

    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data  # No statistics set
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

    monthly_energy = next(e for e in entities_added if e.entity_description.key == "monthly_energy")
    assert monthly_energy.native_value is None


# =============================================================================
# Yearly Energy Statistics Tests
# =============================================================================


async def test_yearly_energy_state(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test yearly energy sensor reflects the total energy for current year."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    yearly_energy = next(e for e in entities_added if e.entity_description.key == "yearly_energy")
    assert yearly_energy.native_value == 1250.75


async def test_yearly_energy_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test yearly energy sensor has correct unique ID."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    yearly_energy = next(e for e in entities_added if e.entity_description.key == "yearly_energy")
    assert yearly_energy.unique_id == f"{TEST_CHARGER_ID}_yearly_energy"


async def test_yearly_energy_attributes(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_coordinator_with_statistics,
) -> None:
    """Test yearly energy sensor has correct device class and unit."""
    mock_config_entry.add_to_hass(hass)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][mock_config_entry.entry_id] = mock_coordinator_with_statistics

    entities_added = []

    def capture_entities(entities):
        entities_added.extend(entities)

    await async_setup_entry(hass, mock_config_entry, capture_entities)
    await hass.async_block_till_done()

    yearly_energy = next(e for e in entities_added if e.entity_description.key == "yearly_energy")
    assert yearly_energy.device_class == SensorDeviceClass.ENERGY
    assert yearly_energy.native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR
    assert yearly_energy.state_class == SensorStateClass.TOTAL


async def test_yearly_energy_none_when_no_statistics(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_wellborne_data: WellborneData,
) -> None:
    """Test yearly energy sensor returns None when no statistics data."""
    mock_config_entry.add_to_hass(hass)

    coordinator = MagicMock()
    coordinator.data = mock_wellborne_data  # No statistics set
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

    yearly_energy = next(e for e in entities_added if e.entity_description.key == "yearly_energy")
    assert yearly_energy.native_value is None
