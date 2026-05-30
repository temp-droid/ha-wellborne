"""Select platform for Wellborne EV Charger."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.select import SelectEntity, SelectEntityDescription

from ..api import WellborneData
from ..const import DOMAIN, SOLAR_MODE_API_TO_NAME, SOLAR_MODE_NAME_TO_API
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneSelectEntityDescription(SelectEntityDescription):
    """Describes a Wellborne select entity."""

    value_fn: Callable[[WellborneData], str | None]
    options_map: dict[str, str]


def _get_solar_mode(data: WellborneData) -> str | None:
    """Get the solar mode as display name."""
    return SOLAR_MODE_API_TO_NAME.get(data.status.solar_mode)


SELECT_DESCRIPTIONS: tuple[WellborneSelectEntityDescription, ...] = (
    WellborneSelectEntityDescription(
        key="solar_mode",
        translation_key="solar_mode",
        options=list(SOLAR_MODE_API_TO_NAME.values()),
        value_fn=_get_solar_mode,
        options_map=SOLAR_MODE_NAME_TO_API,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne selects from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneSelect] = [WellborneSelect(coordinator, description) for description in SELECT_DESCRIPTIONS]

    async_add_entities(entities)


class WellborneSelect(WellborneEntity, SelectEntity):
    """Representation of a Wellborne select."""

    entity_description: WellborneSelectEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneSelectEntityDescription,
    ) -> None:
        """Initialize the select."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        api_value = self.entity_description.options_map.get(option)
        if api_value is not None:
            await self.coordinator.async_set_solar_mode(api_value)
