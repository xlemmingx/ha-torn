"""Sensor platform for Torn City integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_API_KEY, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import TornDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Torn City sensors from a config entry."""
    coordinator: TornDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    # Create grouped sensor entities
    entities: list[SensorEntity] = [
        TornProfileSensor(coordinator, entry),
        TornBattleStatsSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class TornSensor(CoordinatorEntity[TornDataUpdateCoordinator], SensorEntity):
    """Base class for Torn City sensors."""

    def __init__(
        self,
        coordinator: TornDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None


class TornProfileSensor(TornSensor):
    """Sensor for player profile information."""

    _attr_icon = "mdi:account"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile"

    @property
    def native_value(self) -> str | None:
        """Return the state (player name)."""
        if self.coordinator.data:
            return self.coordinator.data.get("profile", {}).get("name")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        profile = self.coordinator.data.get("profile", {})
        status = profile.get("status", {})

        # Handle status - can be dict or string
        status_text = None
        if isinstance(status, dict):
            status_text = status.get("state") or status.get("description")
        else:
            status_text = str(status)

        return {
            "id": profile.get("id"),
            "name": profile.get("name"),
            "level": profile.get("level"),
            "gender": profile.get("gender"),
            "status": status_text,
        }


class TornBattleStatsSensor(TornSensor):
    """Sensor for battle statistics."""

    _attr_icon = "mdi:sword-cross"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battle_stats"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Battle Stats"

    @property
    def native_value(self) -> int | None:
        """Return the state (total battle stats)."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("total")
            )
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        battle_stats = self.coordinator.data.get("personalstats", {}).get("battle_stats", {})

        return {
            "strength": battle_stats.get("strength"),
            "defense": battle_stats.get("defense"),
            "speed": battle_stats.get("speed"),
            "dexterity": battle_stats.get("dexterity"),
            "total": battle_stats.get("total"),
        }
