"""Sensor platform for Torn City integration."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
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
        TornProfileStatusDescriptionSensor(coordinator, entry),
        TornProfileStatusDetailsSensor(coordinator, entry),
        TornProfileStatusUntilSensor(coordinator, entry),
        # Battle stats sensors
        TornBattleStatsStrengthSensor(coordinator, entry),
        TornBattleStatsDefenseSensor(coordinator, entry),
        TornBattleStatsSpeedSensor(coordinator, entry),
        TornBattleStatsDexteritySensor(coordinator, entry),
        TornBattleStatsTotalSensor(coordinator, entry),
        # Bars sensors
        TornBarsEnergySensor(coordinator, entry),
        TornBarsNerveSensor(coordinator, entry),
        TornBarsHappySensor(coordinator, entry),
        TornBarsLifeSensor(coordinator, entry),
        TornBarsChainSensor(coordinator, entry),
        TornBarsChainTimeoutSensor(coordinator, entry),
        # Cooldowns sensors
        TornCooldownsDrugSensor(coordinator, entry),
        TornCooldownsMedicalSensor(coordinator, entry),
        TornCooldownsBoosterSensor(coordinator, entry),
        # Money sensors
        TornMoneyPointsSensor(coordinator, entry),
        TornMoneyWalletSensor(coordinator, entry),
        TornMoneyCompanySensor(coordinator, entry),
        TornMoneyVaultSensor(coordinator, entry),
        TornMoneyCaymanBankSensor(coordinator, entry),
        TornMoneyCityBankSensor(coordinator, entry),
        TornMoneyCityBankProfitSensor(coordinator, entry),
        TornMoneyCityBankDurationSensor(coordinator, entry),
        TornMoneyCityBankInterestRateSensor(coordinator, entry),
        TornMoneyCityBankUntilSensor(coordinator, entry),
        TornMoneyCityBankInvestedAtSensor(coordinator, entry),
        TornMoneyFactionSensor(coordinator, entry),
        TornMoneyFactionPointsSensor(coordinator, entry),
        TornMoneyDailyNetworthSensor(coordinator, entry),
        # Travel sensors
        TornTravelDestinationSensor(coordinator, entry),
        TornTravelMethodSensor(coordinator, entry),
        TornTravelDepartedAtSensor(coordinator, entry),
        TornTravelArrivalAtSensor(coordinator, entry),
        TornTravelTimeLeftSensor(coordinator, entry),
        # Log sensor
        TornLogLatestSensor(coordinator, entry),
        # Company sensors
        TornCompanyFundsSensor(coordinator, entry),
        TornCompanyPopularitySensor(coordinator, entry),
        TornCompanyEfficiencySensor(coordinator, entry),
        TornCompanyEnvironmentSensor(coordinator, entry),
        TornCompanyTrainsAvailableSensor(coordinator, entry),
        TornCompanyAdvertisingBudgetSensor(coordinator, entry),
        TornCompanyRatingSensor(coordinator, entry),
        TornCompanyNameSensor(coordinator, entry),
        TornCompanyDailyIncomeSensor(coordinator, entry),
        TornCompanyWeeklyIncomeSensor(coordinator, entry),
    ]

    # Add dynamic skill sensors
    if coordinator.data and "skills" in coordinator.data:
        skills = coordinator.data["skills"]
        if skills and isinstance(skills, list):
            for skill in skills:
                entities.append(TornSkillSensor(coordinator, entry, skill))

    # Add dynamic stock sensors (all 35 stocks)
    if coordinator.data and "torn_stocks" in coordinator.data:
        torn_stocks = coordinator.data["torn_stocks"]
        _LOGGER.info(f"Creating stock sensors. Found {len(torn_stocks) if torn_stocks else 0} stocks in torn_stocks")
        if torn_stocks and isinstance(torn_stocks, dict):
            for stock_id, stock_data in torn_stocks.items():
                _LOGGER.debug(f"Creating TornStockSensor for stock_id={stock_id}, name={stock_data.get('name', 'Unknown')}")
                entities.append(TornStockSensor(coordinator, entry, stock_id, stock_data))
            _LOGGER.info(f"Created {len([e for e in entities if isinstance(e, TornStockSensor)])} stock sensors")
    else:
        _LOGGER.warning(f"No torn_stocks data found. coordinator.data keys: {list(coordinator.data.keys()) if coordinator.data else 'None'}")

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

        # Set up device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Torn",
            manufacturer="Torn City",
            model="Player Account",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None


# ============================================================================
# Profile Sensors
# ============================================================================


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
            if isinstance(status, dict):
                return status.get("state") or status.get("description")
            return str(status)
        return None


class TornProfileStatusDescriptionSensor(TornSensor):
    """Sensor for player status description."""

    _attr_icon = "mdi:text"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_status_description"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Status Description"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            status = self.coordinator.data.get("profile", {}).get("status", {})
            return status.get("description")
        return None


class TornProfileStatusDetailsSensor(TornSensor):
    """Sensor for player status details (e.g., hospital reason)."""

    _attr_icon = "mdi:text-box"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_status_details"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Status Details"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            status = self.coordinator.data.get("profile", {}).get("status", {})
            return status.get("details")
        return None


class TornProfileStatusUntilSensor(TornSensor):
    """Sensor for player status until timestamp."""

    _attr_icon = "mdi:clock-end"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_profile_status_until"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Profile Status Until"

    @property
    def native_value(self) -> datetime | None:
        """Return the state."""
        if self.coordinator.data:
            status = self.coordinator.data.get("profile", {}).get("status", {})
            until = status.get("until")
            if until and until > 0:
                return datetime.fromtimestamp(until, tz=timezone.utc)
        return None


# ============================================================================
# Battle Stats Sensors
# ============================================================================


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


# ============================================================================
# Bars Sensors
# ============================================================================


class TornBarsEnergySensor(TornSensor):
    """Sensor for energy bar."""

    _attr_icon = "mdi:lightning-bolt"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_energy"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Energy"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            energy = self.coordinator.data.get("bars", {}).get("energy", {})
            return energy.get("current")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            energy = self.coordinator.data.get("bars", {}).get("energy", {})
            return {
                "current": energy.get("current"),
                "maximum": energy.get("maximum"),
            }
        return {}


class TornBarsNerveSensor(TornSensor):
    """Sensor for nerve bar."""

    _attr_icon = "mdi:brain"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_nerve"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Nerve"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            nerve = self.coordinator.data.get("bars", {}).get("nerve", {})
            return nerve.get("current")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            nerve = self.coordinator.data.get("bars", {}).get("nerve", {})
            return {
                "current": nerve.get("current"),
                "maximum": nerve.get("maximum"),
            }
        return {}


class TornBarsHappySensor(TornSensor):
    """Sensor for happy bar."""

    _attr_icon = "mdi:emoticon-happy"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_happy"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Happy"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            happy = self.coordinator.data.get("bars", {}).get("happy", {})
            return happy.get("current")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            happy = self.coordinator.data.get("bars", {}).get("happy", {})
            return {
                "current": happy.get("current"),
                "maximum": happy.get("maximum"),
            }
        return {}


class TornBarsLifeSensor(TornSensor):
    """Sensor for life bar."""

    _attr_icon = "mdi:heart-pulse"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_life"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Life"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            life = self.coordinator.data.get("bars", {}).get("life", {})
            return life.get("current")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            life = self.coordinator.data.get("bars", {}).get("life", {})
            return {
                "current": life.get("current"),
                "maximum": life.get("maximum"),
            }
        return {}


class TornBarsChainSensor(TornSensor):
    """Sensor for chain bar."""

    _attr_icon = "mdi:link-variant"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_chain"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Chain"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            chain = self.coordinator.data.get("bars", {}).get("chain")
            if chain and isinstance(chain, dict):
                return chain.get("current", 0)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.coordinator.data:
            chain = self.coordinator.data.get("bars", {}).get("chain")
            if chain and isinstance(chain, dict):
                return {
                    "current": chain.get("current"),
                    "maximum": chain.get("maximum"),
                    "timeout": chain.get("timeout"),
                }
        return {}


class TornBarsChainTimeoutSensor(TornSensor):
    """Sensor for chain timeout timer."""

    _attr_icon = "mdi:timer"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_bars_chain_timeout"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Bars Chain Timeout"

    @property
    def native_value(self) -> datetime | None:
        """Return the state as timestamp."""
        if self.coordinator.data:
            chain = self.coordinator.data.get("bars", {}).get("chain")
            if chain and isinstance(chain, dict):
                timeout = chain.get("timeout")
                if timeout and timeout > 0:
                    return datetime.fromtimestamp(timeout, tz=timezone.utc)
        return None


# ============================================================================
# Cooldowns Sensors
# ============================================================================


class TornCooldownsDrugSensor(TornSensor):
    """Sensor for drug cooldown."""

    _attr_icon = "mdi:pill"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_cooldowns_drug"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Cooldowns Drug"

    @property
    def native_value(self) -> datetime | None:
        """Return the state as timestamp."""
        if self.coordinator.data:
            seconds = self.coordinator.data.get("cooldowns", {}).get("drug", 0)
            if seconds > 0:
                return datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=seconds)
        return None


class TornCooldownsMedicalSensor(TornSensor):
    """Sensor for medical cooldown."""

    _attr_icon = "mdi:medical-bag"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_cooldowns_medical"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Cooldowns Medical"

    @property
    def native_value(self) -> datetime | None:
        """Return the state as timestamp."""
        if self.coordinator.data:
            seconds = self.coordinator.data.get("cooldowns", {}).get("medical", 0)
            if seconds > 0:
                return datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=seconds)
        return None


class TornCooldownsBoosterSensor(TornSensor):
    """Sensor for booster cooldown."""

    _attr_icon = "mdi:rocket-launch"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_cooldowns_booster"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Cooldowns Booster"

    @property
    def native_value(self) -> datetime | None:
        """Return the state as timestamp."""
        if self.coordinator.data:
            seconds = self.coordinator.data.get("cooldowns", {}).get("booster", 0)
            if seconds > 0:
                return datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=seconds)
        return None


# ============================================================================
# Money Sensors
# ============================================================================


class TornMoneyPointsSensor(TornSensor):
    """Sensor for points."""

    _attr_icon = "mdi:star-circle"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_points"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Points"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("points")
        return None


class TornMoneyWalletSensor(TornSensor):
    """Sensor for wallet."""

    _attr_icon = "mdi:wallet"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_wallet"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Wallet"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("wallet")
        return None


class TornMoneyCompanySensor(TornSensor):
    """Sensor for company funds."""

    _attr_icon = "mdi:office-building"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_company"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Company"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("company")
        return None


class TornMoneyVaultSensor(TornSensor):
    """Sensor for vault."""

    _attr_icon = "mdi:safe"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_vault"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Vault"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("vault")
        return None


class TornMoneyCaymanBankSensor(TornSensor):
    """Sensor for Cayman bank."""

    _attr_icon = "mdi:bank"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_cayman_bank"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Cayman Bank"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("cayman_bank")
        return None


class TornMoneyCityBankSensor(TornSensor):
    """Sensor for city bank."""

    _attr_icon = "mdi:bank"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                return city_bank.get("amount")
        return None


class TornMoneyFactionSensor(TornSensor):
    """Sensor for faction funds."""

    _attr_icon = "mdi:account-group"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_faction"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Faction"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            faction = self.coordinator.data.get("money", {}).get("faction", {})
            if isinstance(faction, dict):
                return faction.get("money")
        return None


class TornMoneyDailyNetworthSensor(TornSensor):
    """Sensor for daily networth."""

    _attr_icon = "mdi:chart-line"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_daily_networth"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Daily Networth"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("money", {}).get("daily_networth")
        return None


class TornMoneyCityBankProfitSensor(TornSensor):
    """Sensor for city bank profit."""

    _attr_icon = "mdi:cash-plus"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank_profit"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank Profit"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                return city_bank.get("profit")
        return None


class TornMoneyCityBankDurationSensor(TornSensor):
    """Sensor for city bank investment duration."""

    _attr_icon = "mdi:calendar-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "days"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank_duration"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank Duration"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                return city_bank.get("duration")
        return None


class TornMoneyCityBankInterestRateSensor(TornSensor):
    """Sensor for city bank interest rate."""

    _attr_icon = "mdi:percent"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank_interest_rate"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank Interest Rate"

    @property
    def native_value(self) -> float | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                return city_bank.get("interest_rate")
        return None


class TornMoneyCityBankUntilSensor(TornSensor):
    """Sensor for city bank investment end time."""

    _attr_icon = "mdi:clock-end"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank_until"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank Until"

    @property
    def native_value(self) -> datetime | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                until_timestamp = city_bank.get("until")
                if until_timestamp:
                    return datetime.fromtimestamp(until_timestamp, tz=timezone.utc)
        return None


class TornMoneyCityBankInvestedAtSensor(TornSensor):
    """Sensor for city bank investment start time."""

    _attr_icon = "mdi:clock-start"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_city_bank_invested_at"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money City Bank Invested At"

    @property
    def native_value(self) -> datetime | None:
        """Return the state."""
        if self.coordinator.data:
            city_bank = self.coordinator.data.get("money", {}).get("city_bank", {})
            if isinstance(city_bank, dict):
                invested_at = city_bank.get("invested_at")
                if invested_at:
                    return datetime.fromtimestamp(invested_at, tz=timezone.utc)
        return None


class TornMoneyFactionPointsSensor(TornSensor):
    """Sensor for faction points."""

    _attr_icon = "mdi:star-circle"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_money_faction_points"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Money Faction Points"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            faction = self.coordinator.data.get("money", {}).get("faction", {})
            if isinstance(faction, dict):
                return faction.get("points")
        return None


# ============================================================================
# Travel Sensors
# ============================================================================


class TornTravelDestinationSensor(TornSensor):
    """Sensor for travel destination."""

    _attr_icon = "mdi:airplane"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_travel_destination"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Travel Destination"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("travel", {}).get("destination")
        return None


class TornTravelMethodSensor(TornSensor):
    """Sensor for travel method."""

    _attr_icon = "mdi:airplane-takeoff"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_travel_method"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Travel Method"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            method = self.coordinator.data.get("travel", {}).get("method")
            return str(method) if method else None
        return None


class TornTravelDepartedAtSensor(TornSensor):
    """Sensor for travel departed timestamp."""

    _attr_icon = "mdi:clock-start"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_travel_departed_at"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Travel Departed At"

    @property
    def native_value(self) -> datetime | None:
        """Return the state."""
        if self.coordinator.data:
            timestamp = self.coordinator.data.get("travel", {}).get("departed_at")
            if timestamp:
                return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return None


class TornTravelArrivalAtSensor(TornSensor):
    """Sensor for travel arrival timestamp."""

    _attr_icon = "mdi:clock-end"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_travel_arrival_at"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Travel Arrival At"

    @property
    def native_value(self) -> datetime | None:
        """Return the state."""
        if self.coordinator.data:
            timestamp = self.coordinator.data.get("travel", {}).get("arrival_at")
            if timestamp:
                return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return None


class TornTravelTimeLeftSensor(TornSensor):
    """Sensor for travel time left."""

    _attr_icon = "mdi:timer-sand"
    _attr_native_unit_of_measurement = "s"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_travel_time_left"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Travel Time Left"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("travel", {}).get("time_left")
        return None


# ============================================================================
# Skills Sensors (Dynamic)
# ============================================================================


class TornSkillSensor(TornSensor):
    """Sensor for a skill."""

    _attr_icon = "mdi:school"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: TornDataUpdateCoordinator,
        entry: ConfigEntry,
        skill: dict,
    ) -> None:
        """Initialize the skill sensor."""
        super().__init__(coordinator, entry)
        self.skill_slug = skill.get("slug", "")
        self.skill_name = skill.get("name", "")

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_skills_{self.skill_slug}"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return f"Skills {self.skill_name}"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data and "skills" in self.coordinator.data:
            skills = self.coordinator.data["skills"]
            if skills and isinstance(skills, list):
                for skill in skills:
                    if skill.get("slug") == self.skill_slug:
                        return skill.get("level")
        return None


# ============================================================================
# Log Sensor
# ============================================================================


class TornLogLatestSensor(TornSensor):
    """Sensor for latest log entries."""

    _attr_icon = "mdi:text-box-multiple"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_log_latest"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Log Latest"

    @property
    def native_value(self) -> str | None:
        """Return the state (latest log entry)."""
        if self.coordinator.data and "log" in self.coordinator.data:
            logs = self.coordinator.data["log"]
            if logs and isinstance(logs, list) and len(logs) > 0:
                latest = logs[0]
                return latest.get("details", {}).get("title", "")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes with all log entries."""
        if self.coordinator.data and "log" in self.coordinator.data:
            logs = self.coordinator.data["log"]
            if logs and isinstance(logs, list):
                entries = []
                for i, log_entry in enumerate(logs[:5]):  # Latest 5
                    entries.append({
                        "id": log_entry.get("id"),
                        "timestamp": log_entry.get("timestamp"),
                        "title": log_entry.get("details", {}).get("title"),
                        "category": log_entry.get("details", {}).get("category"),
                        "data": log_entry.get("data", {}),
                        "params": log_entry.get("params", {}),
                    })
                return {"entries": entries, "count": len(entries)}
        return {}


class TornCompanyFundsSensor(TornSensor):
    """Sensor for company funds."""

    _attr_icon = "mdi:cash-multiple"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_funds"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Funds"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("company_funds")
        return None


class TornCompanyPopularitySensor(TornSensor):
    """Sensor for company popularity."""

    _attr_icon = "mdi:star"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_popularity"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Popularity"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("popularity")
        return None


class TornCompanyEfficiencySensor(TornSensor):
    """Sensor for company efficiency."""

    _attr_icon = "mdi:gauge"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_efficiency"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Efficiency"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("efficiency")
        return None


class TornCompanyEnvironmentSensor(TornSensor):
    """Sensor for company environment."""

    _attr_icon = "mdi:flower"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_environment"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Environment"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("environment")
        return None


class TornCompanyTrainsAvailableSensor(TornSensor):
    """Sensor for company trains available."""

    _attr_icon = "mdi:dumbbell"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_trains_available"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Trains Available"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("trains_available")
        return None


class TornCompanyAdvertisingBudgetSensor(TornSensor):
    """Sensor for company advertising budget."""

    _attr_icon = "mdi:bullhorn"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_advertising_budget"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Advertising Budget"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company_detailed", {}).get("advertising_budget")
        return None


class TornCompanyRatingSensor(TornSensor):
    """Sensor for company rating."""

    _attr_icon = "mdi:star-circle"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_rating"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Rating"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company", {}).get("rating")
        return None


class TornCompanyNameSensor(TornSensor):
    """Sensor for company name."""

    _attr_icon = "mdi:office-building"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_name"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Name"

    @property
    def native_value(self) -> str | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company", {}).get("name")
        return None


class TornCompanyDailyIncomeSensor(TornSensor):
    """Sensor for company daily income."""

    _attr_icon = "mdi:cash-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_daily_income"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Daily Income"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company", {}).get("daily_income")
        return None


class TornCompanyWeeklyIncomeSensor(TornSensor):
    """Sensor for company weekly income."""

    _attr_icon = "mdi:calendar-cash"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "$"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_company_weekly_income"

    @property
    def name(self) -> str:
        """Return sensor name."""
        return "Company Weekly Income"

    @property
    def native_value(self) -> int | None:
        """Return the state."""
        if self.coordinator.data:
            return self.coordinator.data.get("company", {}).get("weekly_income")
        return None


# ============================================================================
# Stock Sensors (Dynamic)
# ============================================================================


class TornStockSensor(TornSensor):
    """Sensor for a stock."""

    _attr_icon = "mdi:chart-line"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: TornDataUpdateCoordinator,
        entry: ConfigEntry,
        stock_id: str,
        stock_data: dict,
    ) -> None:
        """Initialize the stock sensor."""
        super().__init__(coordinator, entry)
        self.stock_id = stock_id
        self._stock_data = stock_data

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self.entry.entry_id}_stock_{self.stock_id}"

    @property
    def name(self) -> str:
        """Return sensor name."""
        acronym = self._stock_data.get("acronym", f"Stock {self.stock_id}")
        return f"Stock {acronym}"

    @property
    def native_value(self) -> int | None:
        """Return the state (number of shares owned)."""
        if self.coordinator.data:
            user_stocks = self.coordinator.data.get("user_stocks", {})
            if self.stock_id in user_stocks:
                return user_stocks[self.stock_id].get("total_shares", 0)
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        # Get torn stocks data (market info)
        torn_stocks = self.coordinator.data.get("torn_stocks", {})
        stock_info = torn_stocks.get(self.stock_id, {})

        # Get user stocks data (ownership info)
        user_stocks = self.coordinator.data.get("user_stocks", {})
        user_stock = user_stocks.get(self.stock_id, {})

        # Basic stock information
        current_price = stock_info.get("current_price", 0)
        total_shares_owned = user_stock.get("total_shares", 0)

        attributes = {
            "stock_id": int(self.stock_id),
            "name": stock_info.get("name"),
            "acronym": stock_info.get("acronym"),
            "current_price": current_price,
            "market_cap": stock_info.get("market_cap"),
            "total_shares": stock_info.get("total_shares"),
            "investors": stock_info.get("investors"),
            "total_shares_owned": total_shares_owned,
            "total_value": current_price * total_shares_owned if total_shares_owned else 0,
        }

        # Benefit information from torn stocks
        benefit = stock_info.get("benefit", {})
        if benefit:
            attributes["benefit_type"] = benefit.get("type")
            attributes["benefit_requirement"] = benefit.get("requirement")
            attributes["benefit_description"] = benefit.get("description")
            attributes["benefit_frequency"] = benefit.get("frequency")

        # User-specific benefit/dividend info (only if owned)
        if user_stock:
            # Handle both "benefit" and "dividend" keys
            user_benefit = user_stock.get("benefit") or user_stock.get("dividend", {})
            if user_benefit:
                attributes["blocks_active"] = user_benefit.get("increment", 0)
                attributes["blocks_next_payout_progress"] = user_benefit.get("progress", 0)
                attributes["blocks_ready_to_claim"] = bool(user_benefit.get("ready", 0))

                # Calculate total benefit per payout (increment × benefit amount)
                # Note: benefit_description might need parsing if it's a string like "$50,000,000"
                increment = user_benefit.get("increment", 0)
                if increment > 0:
                    attributes["blocks_next_payout_frequency"] = user_benefit.get("frequency")

        return attributes
