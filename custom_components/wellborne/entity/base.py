"""Base entity for Wellborne integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import ATTRIBUTION, DOMAIN
from ..coordinator import WellborneDataUpdateCoordinator


class WellborneEntity(CoordinatorEntity[WellborneDataUpdateCoordinator]):
    """Base class for Wellborne entities."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: WellborneDataUpdateCoordinator,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._charger_id = coordinator.charger_id

        # Set device info - handle case when data is not yet available
        if coordinator.data is not None:
            name = coordinator.data.charger.alias or f"Wellborne {self._charger_id}"
            model = coordinator.data.charger.model
        else:
            name = f"Wellborne {self._charger_id}"
            model = None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._charger_id)},
            name=name,
            manufacturer="Wellborne/ATESS",
            model=model,
            sw_version=None,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data is not None
