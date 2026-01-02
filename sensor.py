"""Sensor platform for Torn City integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
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

    # Create flat sensor entities
    entities: list[SensorEntity] = [
        # Profile sensors
        TornProfileNameSensor(coordinator, entry),
        TornProfileLevelSensor(coordinator, entry),
        TornProfileStatusSensor(coordinator, entry),
        # Battle stats sensors
        TornBattleStatsStrengthSensor(coordinator, entry),
        TornBattleStatsDefenseSensor(coordinator, entry),
        TornBattleStatsSpeedSensor(coordinator, entry),
        TornBattleStatsDexteritySensor(coordinator, entry),
        TornBattleStatsTotalSensor(coordinator, entry),
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


# Profile Sensors


class TornProfileNameSensor(TornSensor):
    """Sensor for player name."""

    _attr_icon = "mdi:account"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_name"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Name"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("profile", {}).get("name")
        return None


class TornProfileLevelSensor(TornSensor):
    """Sensor for player level."""

    _attr_icon = "mdi:star"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_level"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Level"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("profile", {}).get("level")
        return None


class TornProfileStatusSensor(TornSensor):
    """Sensor for player status."""

    _attr_icon = "mdi:information"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_status"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Status"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            status = self.coordinator.data.get("profile", {}).get("status", {})
            # Status is typically an object with state, description, etc.
            if isinstance(status, dict):
                return status.get("state") or status.get("description")
            return str(status)
        return None


# Battle Stats Sensors


class TornBattleStatsStrengthSensor(TornSensor):
    """Sensor for strength battle stat."""

    _attr_icon = "mdi:arm-flex"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battlestats_strength"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "BattleStats Strength"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("strength")
            )
        return None


class TornBattleStatsDefenseSensor(TornSensor):
    """Sensor for defense battle stat."""

    _attr_icon = "mdi:shield"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battlestats_defense"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "BattleStats Defense"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("defense")
            )
        return None


class TornBattleStatsSpeedSensor(TornSensor):
    """Sensor for speed battle stat."""

    _attr_icon = "mdi:run-fast"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battlestats_speed"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "BattleStats Speed"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("speed")
            )
        return None


class TornBattleStatsDexteritySensor(TornSensor):
    """Sensor for dexterity battle stat."""

    _attr_icon = "mdi:hand-back-right"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battlestats_dexterity"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "BattleStats Dexterity"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("dexterity")
            )
        return None


class TornBattleStatsTotalSensor(TornSensor):
    """Sensor for total battle stats."""

    _attr_icon = "mdi:chart-line"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_battlestats_total"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "BattleStats Total"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return (
                self.coordinator.data.get("personalstats", {})
                .get("battle_stats", {})
                .get("total")
            )
        return None
