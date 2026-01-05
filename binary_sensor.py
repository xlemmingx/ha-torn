"""Binary sensor platform for Torn City integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from .const import DOMAIN
from .coordinator import TornDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Torn City binary sensors from a config entry."""
    coordinator: TornDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    # Create binary sensor entities
    entities: list[BinarySensorEntity] = [
        TornEnergyRefillUsedSensor(coordinator, entry),
        TornNerveRefillUsedSensor(coordinator, entry),
        TornTokenRefillUsedSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class TornBinarySensor(CoordinatorEntity[TornDataUpdateCoordinator], BinarySensorEntity):
    """Base class for Torn City binary sensors."""

    def __init__(
        self,
        coordinator: TornDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entry = entry

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name="Torn City",
            manufacturer="Torn City",
            entry_type=DeviceEntryType.SERVICE,
        )


class TornEnergyRefillUsedSensor(TornBinarySensor):
    """Binary sensor for energy refill used status."""

    _attr_icon = "mdi:lightning-bolt"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_energy_refill_used"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Energy Refill Used"

    @property
    def is_on(self) -> bool | None:
        """Return true if energy refill has been used today."""
        if self.coordinator.data:
            return self.coordinator.data.get("refills", {}).get("energy_refill_used")
        return None


class TornNerveRefillUsedSensor(TornBinarySensor):
    """Binary sensor for nerve refill used status."""

    _attr_icon = "mdi:brain"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_nerve_refill_used"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Nerve Refill Used"

    @property
    def is_on(self) -> bool | None:
        """Return true if nerve refill has been used today."""
        if self.coordinator.data:
            return self.coordinator.data.get("refills", {}).get("nerve_refill_used")
        return None


class TornTokenRefillUsedSensor(TornBinarySensor):
    """Binary sensor for token refill used status."""

    _attr_icon = "mdi:poker-chip"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_token_refill_used"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Token Refill Used"

    @property
    def is_on(self) -> bool | None:
        """Return true if token refill has been used today."""
        if self.coordinator.data:
            return self.coordinator.data.get("refills", {}).get("token_refill_used")
        return None
