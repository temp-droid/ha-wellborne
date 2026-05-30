"""Number platform for Wellborne EV Charger."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberEntityDescription, NumberMode
from homeassistant.const import UnitOfElectricCurrent, UnitOfPower, UnitOfTime

from ..api import WellborneData
from ..const import DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneNumberEntityDescription(NumberEntityDescription):
    """Describes a Wellborne number entity."""

    value_fn: Callable[[WellborneData], float | None]
    setter_key: str  # Name of coordinator method to call (without async_ prefix)


def _get_max_current(data: WellborneData) -> float | None:
    """Get the max current value."""
    return data.status.max_current


def _get_delay_time(data: WellborneData) -> float | None:
    """Get the delay time value in minutes.

    Note: The API stores delay_time in seconds, but we display it in minutes
    for better user experience. The conversion happens in async_set_delay_time
    in the coordinator (minutes * 60 = seconds).
    """
    # API stores seconds, we display minutes (divide by 60)
    return float(data.delayed_charging.delay_time) / 60


def _get_max_power(data: WellborneData) -> float | None:
    """Get the max power value in Watts."""
    return float(data.status.max_power)


def _get_load_balancing_current(data: WellborneData) -> float | None:
    """Get the load balancing total domestic power value.

    Note: Despite the function name, this actually returns the total domestic
    power limit in kW, as that's what the API provides for load balancing.
    """
    return float(data.load_balancing.max_current)


NUMBER_DESCRIPTIONS: tuple[WellborneNumberEntityDescription, ...] = (
    WellborneNumberEntityDescription(
        key="max_current",
        translation_key="max_current",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        native_min_value=6,
        native_max_value=32,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=_get_max_current,
        setter_key="set_max_current",
    ),
    WellborneNumberEntityDescription(
        key="delay_time",
        translation_key="delay_time",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        native_min_value=0,
        native_max_value=1440,  # 24 hours
        native_step=1,
        mode=NumberMode.BOX,
        value_fn=_get_delay_time,
        setter_key="set_delay_time",
    ),
    WellborneNumberEntityDescription(
        key="max_power",
        translation_key="max_power",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        native_min_value=0,
        native_max_value=22000,
        native_step=100,
        mode=NumberMode.SLIDER,
        value_fn=_get_max_power,
        setter_key="set_max_power",
    ),
    WellborneNumberEntityDescription(
        key="load_balancing_current",
        translation_key="load_balancing_current",
        device_class=NumberDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=_get_load_balancing_current,
        setter_key="set_load_balancing_current",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne numbers from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneNumber] = [WellborneNumber(coordinator, description) for description in NUMBER_DESCRIPTIONS]

    async_add_entities(entities)


class WellborneNumber(WellborneEntity, NumberEntity):
    """Representation of a Wellborne number."""

    entity_description: WellborneNumberEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneNumberEntityDescription,
    ) -> None:
        """Initialize the number."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        setter_method = getattr(self.coordinator, f"async_{self.entity_description.setter_key}")
        await setter_method(int(value))
