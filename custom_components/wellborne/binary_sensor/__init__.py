"""Binary sensor platform for Wellborne EV Charger."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

from ..const import DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Wellborne binary sensor entity."""


BINARY_SENSOR_DESCRIPTIONS: tuple[WellborneBinarySensorEntityDescription, ...] = (
    WellborneBinarySensorEntityDescription(
        key="charger_online",
        translation_key="charger_online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    WellborneBinarySensorEntityDescription(
        key="charging",
        translation_key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    WellborneBinarySensorEntityDescription(
        key="vehicle_connected",
        translation_key="vehicle_connected",
        device_class=BinarySensorDeviceClass.PLUG,
        # Marked as diagnostic because the REST API cannot reliably detect plug status
        # when the charger is idle (not charging). The sensor only shows True when
        # actively charging or has an active session.
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    WellborneBinarySensorEntityDescription(
        key="bluetooth_enabled",
        translation_key="bluetooth_enabled",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne binary sensors from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneBinarySensor] = [
        WellborneBinarySensor(coordinator, description) for description in BINARY_SENSOR_DESCRIPTIONS
    ]

    async_add_entities(entities)


class WellborneBinarySensor(WellborneEntity, BinarySensorEntity):
    """Representation of a Wellborne binary sensor."""

    entity_description: WellborneBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        # Special handling for charger_online - doesn't depend on coordinator.data
        if self.entity_description.key == "charger_online":
            return self.coordinator.is_online

        if self.coordinator.data is None:
            return None

        match self.entity_description.key:
            case "charging":
                return self.coordinator.data.status.is_charging
            case "vehicle_connected":
                # Vehicle is connected if charging or has an active session
                # When idle (not charging), we can't reliably detect if plugged
                # because the REST API doesn't expose connector status
                if self.coordinator.data.status.is_charging:
                    return True  # Definitely connected if charging
                if self.coordinator.data.session_start_time is not None:
                    return True  # Connected if active session
                return None  # Unknown when idle - API limitation
            case "bluetooth_enabled":
                return self.coordinator.data.charger.bluetooth_enabled
            case _:
                return None
