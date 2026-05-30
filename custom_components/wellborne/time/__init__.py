"""Time platform for Wellborne EV Charger."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from datetime import time
from typing import TYPE_CHECKING, Any

from homeassistant.components.time import TimeEntity, TimeEntityDescription

from ..api import WellborneData
from ..const import DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


def _parse_time(time_str: str) -> time | None:
    """Parse a time string (HH:MM) to a time object."""
    if not time_str:
        return None
    try:
        parts = time_str.split(":")
        return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


@dataclass(frozen=True, kw_only=True)
class WellborneTimeEntityDescription(TimeEntityDescription):
    """Describes a Wellborne time entity."""

    value_fn: Callable[[WellborneData], str]
    # Setter function that takes coordinator and time string, returns coroutine
    setter_fn: Callable[[WellborneDataUpdateCoordinator, str], Coroutine[Any, Any, None]]


async def _set_off_peak_weekday_start(coordinator: WellborneDataUpdateCoordinator, time_str: str) -> None:
    """Set off-peak weekday start time."""
    await coordinator.async_set_off_peak_time(weekday_start=time_str)


async def _set_off_peak_weekday_end(coordinator: WellborneDataUpdateCoordinator, time_str: str) -> None:
    """Set off-peak weekday end time."""
    await coordinator.async_set_off_peak_time(weekday_end=time_str)


async def _set_scheduled_time(coordinator: WellborneDataUpdateCoordinator, time_str: str) -> None:
    """Set scheduled charging start time."""
    await coordinator.async_set_scheduled_time(cycle_time=time_str)


TIME_DESCRIPTIONS: tuple[WellborneTimeEntityDescription, ...] = (
    WellborneTimeEntityDescription(
        key="off_peak_weekday_start",
        translation_key="off_peak_weekday_start",
        value_fn=lambda data: data.off_peak.weekday_start,
        setter_fn=_set_off_peak_weekday_start,
    ),
    WellborneTimeEntityDescription(
        key="off_peak_weekday_end",
        translation_key="off_peak_weekday_end",
        value_fn=lambda data: data.off_peak.weekday_end,
        setter_fn=_set_off_peak_weekday_end,
    ),
    WellborneTimeEntityDescription(
        key="scheduled_start_time",
        translation_key="scheduled_start_time",
        value_fn=lambda data: data.scheduled_charging.cycle_time,
        setter_fn=_set_scheduled_time,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne time entities from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneTimeEntity] = [
        WellborneTimeEntity(coordinator, description) for description in TIME_DESCRIPTIONS
    ]

    async_add_entities(entities)


class WellborneTimeEntity(WellborneEntity, TimeEntity):
    """Representation of a Wellborne time entity."""

    entity_description: WellborneTimeEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneTimeEntityDescription,
    ) -> None:
        """Initialize the time entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    @property
    def native_value(self) -> time | None:
        """Return the current time value."""
        if self.coordinator.data is None:
            return None

        time_str = self.entity_description.value_fn(self.coordinator.data)
        return _parse_time(time_str)

    async def async_set_value(self, value: time) -> None:
        """Set the time value."""
        time_str = value.strftime("%H:%M")
        await self.entity_description.setter_fn(self.coordinator, time_str)
