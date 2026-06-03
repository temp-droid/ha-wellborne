"""Sensor platform for Wellborne EV Charger."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfLength,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from ..api import WellborneData
from ..const import CONF_VEHICLE_EFFICIENCY, DEFAULT_VEHICLE_EFFICIENCY, DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneSensorEntityDescription(SensorEntityDescription):
    """Describes a Wellborne sensor entity."""

    value_fn: Callable[[WellborneData], float | int | str | None]
    # Optional: for periodic-total sensors, returns the start of the current
    # accumulation period so the Energy dashboard tracks resets precisely.
    last_reset_fn: Callable[[], datetime] | None = None


def _start_of_month() -> datetime:
    """Return midnight on the 1st of the current month (HA local time)."""
    return dt_util.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _start_of_year() -> datetime:
    """Return midnight on Jan 1 of the current year (HA local time)."""
    return dt_util.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def _get_power(data: WellborneData) -> float | None:
    """Get charging power."""
    if data.meter_values is None:
        return None
    return data.meter_values.power


def _get_energy(data: WellborneData) -> float | None:
    """Get energy delivered."""
    if data.meter_values is None:
        return None
    return data.meter_values.energy


def _get_voltage(data: WellborneData) -> float | None:
    """Get L1 voltage."""
    if data.meter_values is None:
        return None
    return data.meter_values.voltage


def _get_voltage_l2(data: WellborneData) -> float | None:
    """Get L2 voltage."""
    if data.meter_values is None:
        return None
    return data.meter_values.voltage_l2


def _get_voltage_l3(data: WellborneData) -> float | None:
    """Get L3 voltage."""
    if data.meter_values is None:
        return None
    return data.meter_values.voltage_l3


def _get_current(data: WellborneData) -> float | None:
    """Get L1 current."""
    if data.meter_values is None:
        return None
    return data.meter_values.current


def _get_current_l2(data: WellborneData) -> float | None:
    """Get L2 current."""
    if data.meter_values is None:
        return None
    return data.meter_values.current_l2


def _get_current_l3(data: WellborneData) -> float | None:
    """Get L3 current."""
    if data.meter_values is None:
        return None
    return data.meter_values.current_l3


def _get_max_current(data: WellborneData) -> float | None:
    """Get configured max current."""
    return data.status.max_current


def _get_charger_status(data: WellborneData) -> str:
    """Get charger status as a text state."""
    if data.status.is_charging:
        return "charging"
    if data.delayed_charging.enabled or data.scheduled_charging.enabled:
        return "pending"
    return "idle"


# Status options for enum sensor
CHARGER_STATUS_OPTIONS = ["idle", "charging", "pending"]

# Connection status options for the diagnostic enum sensor (order matters; a frontend
# card depends on these exact literals).
CONNECTION_STATUS_OPTIONS = ["online", "charger_offline", "cloud_unreachable"]


def _get_last_session_energy(data: WellborneData) -> float | None:
    """Get energy delivered in last completed session."""
    if data.last_session is None:
        return None
    return data.last_session.energy


def _get_last_session_duration(data: WellborneData) -> int | None:
    """Get duration of last completed session in minutes."""
    if data.last_session is None:
        return None
    return data.last_session.duration_minutes


def _get_monthly_energy(data: WellborneData) -> float | None:
    """Get total energy for current month."""
    if data.monthly_statistics is None:
        return None
    return data.monthly_statistics.total_energy


def _get_yearly_energy(data: WellborneData) -> float | None:
    """Get total energy for current year."""
    if data.yearly_statistics is None:
        return None
    return data.yearly_statistics.total_energy


def _get_wifi_ssid(data: WellborneData) -> str | None:
    """Get WiFi SSID (network name)."""
    if data.wifi_info is None:
        return None
    return data.wifi_info.ssid


# External meter getters (from load balancing Eastron SDM630)
def _get_ext_meter_current_l1(data: WellborneData) -> float | None:
    """Get external meter L1 current."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.current_l1


def _get_ext_meter_current_l2(data: WellborneData) -> float | None:
    """Get external meter L2 current."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.current_l2


def _get_ext_meter_current_l3(data: WellborneData) -> float | None:
    """Get external meter L3 current."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.current_l3


def _get_ext_meter_voltage_l1(data: WellborneData) -> float | None:
    """Get external meter L1 voltage."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.voltage_l1


def _get_ext_meter_voltage_l2(data: WellborneData) -> float | None:
    """Get external meter L2 voltage."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.voltage_l2


def _get_ext_meter_voltage_l3(data: WellborneData) -> float | None:
    """Get external meter L3 voltage."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.voltage_l3


def _get_ext_meter_power(data: WellborneData) -> float | None:
    """Get external meter total power."""
    if data.load_balancing.external_meter is None:
        return None
    return data.load_balancing.external_meter.power


# Maps a sensor key to the live SSE snapshot attribute it should read while a fresh snapshot is
# available. These are the only sensors fed by the live stream; everything else stays on REST.
# `added_range` derives from session energy (handled with the efficiency multiplier separately).
_LIVE_SNAPSHOT_FIELDS: dict[str, str] = {
    "power": "power_w",
    "current": "current_l1",
    "current_l2": "current_l2",
    "current_l3": "current_l3",
    "voltage": "voltage_l1",
    "voltage_l2": "voltage_l2",
    "voltage_l3": "voltage_l3",
    "energy": "energy_kwh",
    "session_duration": "duration_minutes",
    "session_cost": "cost",
}


SENSOR_DESCRIPTIONS: tuple[WellborneSensorEntityDescription, ...] = (
    WellborneSensorEntityDescription(
        key="power",
        translation_key="power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_power,
    ),
    WellborneSensorEntityDescription(
        key="energy",
        translation_key="energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=_get_energy,
    ),
    WellborneSensorEntityDescription(
        key="session_cost",
        translation_key="session_cost",
        # Live-only via the SSE snapshot (the cloud reports the running session cost in EUR).
        # Plain sensor (no monetary device_class) to avoid currency-unit validation; the card
        # formats it. No REST source, so the value_fn fallback is a no-op.
        native_unit_of_measurement="€",
        value_fn=lambda _data: None,
    ),
    WellborneSensorEntityDescription(
        key="voltage",
        translation_key="voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_voltage,
    ),
    WellborneSensorEntityDescription(
        key="voltage_l2",
        translation_key="voltage_l2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_voltage_l2,
    ),
    WellborneSensorEntityDescription(
        key="voltage_l3",
        translation_key="voltage_l3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_voltage_l3,
    ),
    WellborneSensorEntityDescription(
        key="current",
        translation_key="current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_current,
    ),
    WellborneSensorEntityDescription(
        key="current_l2",
        translation_key="current_l2",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_current_l2,
    ),
    WellborneSensorEntityDescription(
        key="current_l3",
        translation_key="current_l3",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_current_l3,
    ),
    WellborneSensorEntityDescription(
        key="max_current",
        translation_key="max_current",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_max_current,
    ),
    WellborneSensorEntityDescription(
        key="session_duration",
        translation_key="session_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        # Live value resolved from the SSE snapshot's charingTimeText in native_value; this
        # fallback intentionally returns None (replaces the old now - session_start_time logic
        # that produced bogus durations, e.g. 177h, from a stale session_start_time).
        value_fn=lambda _data: None,
    ),
    WellborneSensorEntityDescription(
        key="status",
        translation_key="status",
        device_class=SensorDeviceClass.ENUM,
        options=CHARGER_STATUS_OPTIONS,
        value_fn=_get_charger_status,
    ),
    # Diagnostic enum: distinguishes the two charger-unreachable failure modes.
    # Value comes from coordinator.connection_status (special handling in
    # WellborneSensor), not coordinator.data, so it reports even when data is None.
    WellborneSensorEntityDescription(
        key="connection_status",
        translation_key="connection_status",
        device_class=SensorDeviceClass.ENUM,
        options=CONNECTION_STATUS_OPTIONS,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda _data: None,
    ),
    # Note: added_range uses special handling in WellborneSensor for configurable efficiency
    WellborneSensorEntityDescription(
        key="added_range",
        translation_key="added_range",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.meter_values.energy if data.meter_values else None,
    ),
    WellborneSensorEntityDescription(
        key="last_session_energy",
        translation_key="last_session_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        # No state_class: a per-session snapshot is not an accumulating total, and HA
        # rejects measurement+energy. Omitting it keeps the value out of long-term sums.
        value_fn=_get_last_session_energy,
    ),
    WellborneSensorEntityDescription(
        key="last_session_duration",
        translation_key="last_session_duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_last_session_duration,
    ),
    WellborneSensorEntityDescription(
        key="monthly_energy",
        translation_key="monthly_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        value_fn=_get_monthly_energy,
        last_reset_fn=_start_of_month,
    ),
    WellborneSensorEntityDescription(
        key="yearly_energy",
        translation_key="yearly_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL,
        value_fn=_get_yearly_energy,
        last_reset_fn=_start_of_year,
    ),
    WellborneSensorEntityDescription(
        key="wifi_ssid",
        translation_key="wifi_ssid",
        entity_registry_enabled_default=False,
        value_fn=_get_wifi_ssid,
    ),
    # External meter sensors (household power from Eastron SDM630)
    WellborneSensorEntityDescription(
        key="household_power",
        translation_key="household_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_ext_meter_power,
    ),
    WellborneSensorEntityDescription(
        key="household_current_l1",
        translation_key="household_current_l1",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_ext_meter_current_l1,
    ),
    WellborneSensorEntityDescription(
        key="household_current_l2",
        translation_key="household_current_l2",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_ext_meter_current_l2,
    ),
    WellborneSensorEntityDescription(
        key="household_current_l3",
        translation_key="household_current_l3",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_ext_meter_current_l3,
    ),
    WellborneSensorEntityDescription(
        key="household_voltage_l1",
        translation_key="household_voltage_l1",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_ext_meter_voltage_l1,
    ),
    WellborneSensorEntityDescription(
        key="household_voltage_l2",
        translation_key="household_voltage_l2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_ext_meter_voltage_l2,
    ),
    WellborneSensorEntityDescription(
        key="household_voltage_l3",
        translation_key="household_voltage_l3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        value_fn=_get_ext_meter_voltage_l3,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne sensors from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneSensor] = [WellborneSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS]

    async_add_entities(entities)


class WellborneSensor(WellborneEntity, SensorEntity):
    """Representation of a Wellborne sensor."""

    entity_description: WellborneSensorEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    @property
    def last_reset(self) -> datetime | None:
        """Return when a periodic-total sensor last reset (e.g. start of month)."""
        if self.entity_description.last_reset_fn is None:
            return None
        return self.entity_description.last_reset_fn()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # connection_status reports the coordinator's connection state and must stay
        # available even when coordinator.data is None (like the charger_online sensor).
        if self.entity_description.key == "connection_status":
            return CoordinatorEntity.available.fget(self)
        return super().available

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value.

        Live sensors (power, per-phase current/voltage, session energy, session duration and the
        derived added range) read from the coordinator's live SSE snapshot while it is fresh, and
        report None otherwise — never the stale REST live values that produced bogus readings.
        Non-live sensors (statistics, last session, status, etc.) stay on coordinator.data.
        """
        key = self.entity_description.key

        # Special handling for connection_status - doesn't depend on coordinator.data
        if key == "connection_status":
            return self.coordinator.connection_status

        snapshot = self.coordinator.live_snapshot

        # A fresh connected snapshot means a live session is active: the status is "charging"
        # regardless of the slow REST status (which lags ~120s). live_snapshot only returns a
        # value when fresh AND connected, so its presence is the authoritative signal.
        if key == "status" and snapshot is not None:
            return "charging"

        # added_range derives from live session energy with a configurable efficiency.
        if key == "added_range":
            energy = snapshot.energy_kwh if snapshot is not None else None
            if energy is None:
                return None
            efficiency = self.coordinator.config_entry.options.get(CONF_VEHICLE_EFFICIENCY, DEFAULT_VEHICLE_EFFICIENCY)
            return round(energy * efficiency, 1)

        # Live sensors: snapshot when fresh, else None (do not fall back to stale REST values).
        if key in _LIVE_SNAPSHOT_FIELDS:
            if snapshot is None:
                return None
            return getattr(snapshot, _LIVE_SNAPSHOT_FIELDS[key])

        if self.coordinator.data is None:
            return None

        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Expose the precise live session duration in seconds.

        The ``session_duration`` state stays in whole minutes (statistics/energy-dashboard
        friendly), but the dashboard card reads ``duration_seconds`` (parsed live from the
        charger's ``charingTimeText``) to display and tick ``H:MM:SS`` every second.
        """
        if self.entity_description.key != "session_duration":
            return None
        snapshot = self.coordinator.live_snapshot
        if snapshot is None or snapshot.duration_seconds is None:
            return None
        return {"duration_seconds": snapshot.duration_seconds}
