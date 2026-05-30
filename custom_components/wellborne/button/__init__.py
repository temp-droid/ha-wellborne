"""Button platform for Wellborne EV Charger."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from ..const import DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneButtonEntityDescription(ButtonEntityDescription):
    """Describes a Wellborne button entity."""

    press_fn: Callable[[WellborneDataUpdateCoordinator], Awaitable[None]]


async def _start_charging(coordinator: WellborneDataUpdateCoordinator) -> None:
    """Start a charging session."""
    await coordinator.async_start_charging()


async def _stop_charging(coordinator: WellborneDataUpdateCoordinator) -> None:
    """Stop the current charging session."""
    await coordinator.async_stop_charging()


async def _unlock_connector(coordinator: WellborneDataUpdateCoordinator) -> None:
    """Unlock the connector."""
    await coordinator.async_unlock_connector()


async def _prompt_charge(coordinator: WellborneDataUpdateCoordinator) -> None:
    """Start immediate charge (bypasses delayed charging)."""
    await coordinator.async_prompt_charge()


BUTTON_DESCRIPTIONS: tuple[WellborneButtonEntityDescription, ...] = (
    WellborneButtonEntityDescription(
        key="start_charging",
        translation_key="start_charging",
        press_fn=_start_charging,
    ),
    WellborneButtonEntityDescription(
        key="stop_charging",
        translation_key="stop_charging",
        press_fn=_stop_charging,
    ),
    WellborneButtonEntityDescription(
        key="unlock_connector",
        translation_key="unlock_connector",
        press_fn=_unlock_connector,
    ),
    WellborneButtonEntityDescription(
        key="prompt_charge",
        translation_key="prompt_charge",
        press_fn=_prompt_charge,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne buttons from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneButton] = [WellborneButton(coordinator, description) for description in BUTTON_DESCRIPTIONS]

    async_add_entities(entities)


class WellborneButton(WellborneEntity, ButtonEntity):
    """Representation of a Wellborne button."""

    entity_description: WellborneButtonEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.press_fn(self.coordinator)
