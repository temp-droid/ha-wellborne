"""Switch platform for Wellborne EV Charger."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity, SwitchEntityDescription

from ..api import WellborneData
from ..const import DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator
from ..entity.base import WellborneEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@dataclass(frozen=True, kw_only=True)
class WellborneSwitchDescription(SwitchEntityDescription):
    """Describes a Wellborne switch entity with on/off methods and value function."""

    turn_on_method: str  # Coordinator method name for turn_on (without async_ prefix)
    turn_off_method: str  # Coordinator method name for turn_off (without async_ prefix)
    value_fn: Callable[[WellborneData], bool | None]


# Switch descriptions with on/off methods and value functions
SWITCH_DESCRIPTIONS: tuple[WellborneSwitchDescription, ...] = (
    WellborneSwitchDescription(
        key="charging",
        translation_key="charging",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="start_charging",
        turn_off_method="stop_charging",
        value_fn=lambda data: data.status.is_charging,
    ),
    # connector_lock is a persistent config toggle (updateConnectorLock); the momentary "unlock now" action is the separate unlock_connector button.
    WellborneSwitchDescription(
        key="connector_lock",
        translation_key="connector_lock",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_connector_lock",
        turn_off_method="set_connector_lock",
        value_fn=lambda data: data.status.connector_lock,
    ),
    WellborneSwitchDescription(
        key="delayed_charging",
        translation_key="delayed_charging",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_delayed_charging_enabled",
        turn_off_method="set_delayed_charging_enabled",
        value_fn=lambda data: data.delayed_charging.enabled,
    ),
    WellborneSwitchDescription(
        key="scheduled_charging",
        translation_key="scheduled_charging",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_scheduled_charging_enabled",
        turn_off_method="set_scheduled_charging_enabled",
        value_fn=lambda data: data.scheduled_charging.enabled,
    ),
    WellborneSwitchDescription(
        key="off_peak",
        translation_key="off_peak",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_off_peak_enabled",
        turn_off_method="set_off_peak_enabled",
        value_fn=lambda data: data.off_peak.enabled,
    ),
    WellborneSwitchDescription(
        key="lcd_enabled",
        translation_key="lcd_enabled",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_lcd_enabled",
        turn_off_method="set_lcd_enabled",
        value_fn=lambda data: data.status.lcd_enabled,
    ),
    WellborneSwitchDescription(
        key="low_power_reserve",
        translation_key="low_power_reserve",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_low_power_reserve_enabled",
        turn_off_method="set_low_power_reserve_enabled",
        value_fn=lambda data: data.status.low_power_reserve,
    ),
    WellborneSwitchDescription(
        key="load_balancing",
        translation_key="load_balancing",
        device_class=SwitchDeviceClass.SWITCH,
        turn_on_method="set_load_balancing_enabled",
        turn_off_method="set_load_balancing_enabled",
        value_fn=lambda data: data.load_balancing.enabled,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wellborne switches from a config entry."""
    coordinator: WellborneDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[WellborneSwitch] = [WellborneSwitch(coordinator, description) for description in SWITCH_DESCRIPTIONS]

    async_add_entities(entities)


class WellborneSwitch(WellborneEntity, SwitchEntity):
    """Representation of a Wellborne switch with optimistic state support."""

    entity_description: WellborneSwitchDescription

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
        description: WellborneSwitchDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.charger_id}_{description.key}"
        # Optimistic state for immediate UI feedback before API response
        self._optimistic_state: bool | None = None

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Clear optimistic state when coordinator updates with fresh data
        self._optimistic_state = None
        super()._handle_coordinator_update()

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        # Return optimistic state if set (for immediate UI feedback)
        if self._optimistic_state is not None:
            return self._optimistic_state

        if self.coordinator.data is None:
            return None

        return self.entity_description.value_fn(self.coordinator.data)

    async def async_turn_on(self, **_kwargs: Any) -> None:
        """Turn on the switch."""
        previous = self._optimistic_state
        self._optimistic_state = True
        # Only write state if entity is properly added to HA
        if self.hass is not None and self.platform is not None:
            self.async_write_ha_state()

        # Get the turn_on method from coordinator
        method_name = f"async_{self.entity_description.turn_on_method}"
        method = getattr(self.coordinator, method_name)

        try:
            # For methods that take enabled=True/False, pass enabled=True
            if self.entity_description.turn_on_method == self.entity_description.turn_off_method:
                await method(enabled=True)
            else:
                await method()
        except Exception:
            self._optimistic_state = previous
            if self.hass is not None and self.platform is not None:
                self.async_write_ha_state()
            raise

    async def async_turn_off(self, **_kwargs: Any) -> None:
        """Turn off the switch."""
        previous = self._optimistic_state
        self._optimistic_state = False
        # Only write state if entity is properly added to HA
        if self.hass is not None and self.platform is not None:
            self.async_write_ha_state()

        # Get the turn_off method from coordinator
        method_name = f"async_{self.entity_description.turn_off_method}"
        method = getattr(self.coordinator, method_name)

        try:
            # For methods that take enabled=True/False, pass enabled=False
            if self.entity_description.turn_on_method == self.entity_description.turn_off_method:
                await method(enabled=False)
            else:
                await method()
        except Exception:
            self._optimistic_state = previous
            if self.hass is not None and self.platform is not None:
                self.async_write_ha_state()
            raise
