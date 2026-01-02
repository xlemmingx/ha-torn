# Torn City Integration for Home Assistant

A comprehensive Home Assistant custom integration for [Torn City](https://www.torn.com), providing real-time access to your player stats, finances, travel status, cooldowns, and activity logs.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/xlemmingx/ha-torn.svg)](https://github.com/xlemmingx/ha-torn/releases)
[![License](https://img.shields.io/github/license/xlemmingx/ha-torn.svg)](LICENSE)

## Features

This integration creates sensors for all your Torn City data:

### Player Information
- Player name, level, and status
- Battle stats (strength, defense, speed, dexterity, total)

### Bars
- Energy, Nerve, Happy, Life, Chain (with current/maximum values)

### Cooldowns
- Drug, Medical, and Booster cooldowns (as timestamps)

### Money & Finances
- Wallet, Vault, Cayman Bank, Company Funds
- City Bank investment details (amount, profit, interest rate, duration, dates)
- Faction balance and points
- Points and daily networth

### Travel
- Current destination, method, departure/arrival times, time remaining

### Activity Log
- Latest activity entries with full details (data and parameters)

### Skills
- Dynamic sensors for each of your character's skills

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/xlemmingx/ha-torn`
6. Select category "Integration"
7. Click "Add"
8. Search for "Torn City" and install
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/xlemmingx/ha-torn/releases)
2. Copy the entire `custom_components/torn` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Torn City"
4. Enter your Torn City API key
   - **Recommended:** Use a [Full Access API key](https://www.torn.com/preferences.php#tab=api?step=addNewKey&title=Home%20Assistant&type=4) for complete functionality
   - You can create or manage API keys at [Torn Preferences](https://www.torn.com/preferences.php#tab=api)
5. Configure the update interval (default: 60 seconds, range: 30-3600 seconds)
6. Click "Submit"

### API Key Permissions

- **Minimal Access:** Basic player information only
- **Limited Access:** Includes cooldowns, money, travel, and logs
- **Full Access:** Recommended - includes all features, especially battle stats

## Sensors

All sensors are prefixed with `sensor.torn_` and grouped by category:

### Profile Sensors
- `sensor.torn_profile_name`
- `sensor.torn_profile_level`
- `sensor.torn_profile_status`

### Battle Stats Sensors
- `sensor.torn_battlestats_strength`
- `sensor.torn_battlestats_defense`
- `sensor.torn_battlestats_speed`
- `sensor.torn_battlestats_dexterity`
- `sensor.torn_battlestats_total`

### Bars Sensors
- `sensor.torn_bars_energy`
- `sensor.torn_bars_nerve`
- `sensor.torn_bars_happy`
- `sensor.torn_bars_life`
- `sensor.torn_bars_chain`

### Cooldowns Sensors (timestamps)
- `sensor.torn_cooldowns_drug`
- `sensor.torn_cooldowns_medical`
- `sensor.torn_cooldowns_booster`

### Money Sensors
- `sensor.torn_money_wallet`
- `sensor.torn_money_vault`
- `sensor.torn_money_cayman_bank`
- `sensor.torn_money_city_bank`
- `sensor.torn_money_city_bank_profit`
- `sensor.torn_money_city_bank_interest_rate`
- `sensor.torn_money_city_bank_duration`
- `sensor.torn_money_city_bank_invested_at`
- `sensor.torn_money_city_bank_until`
- `sensor.torn_money_company`
- `sensor.torn_money_faction`
- `sensor.torn_money_faction_points`
- `sensor.torn_money_points`
- `sensor.torn_money_daily_networth`

### Travel Sensors
- `sensor.torn_travel_destination`
- `sensor.torn_travel_method`
- `sensor.torn_travel_departed_at`
- `sensor.torn_travel_arrival_at`
- `sensor.torn_travel_time_left`

### Log Sensor
- `sensor.torn_log_latest` (includes last 5 activity entries as attributes)

### Skill Sensors
- `sensor.torn_skill_*` (dynamically created based on your skills)

## Example Dashboard

An example dashboard configuration is included in `dashboard.yaml`. Import it via:

1. Go to your Home Assistant dashboard
2. Click the three dots → "Edit Dashboard"
3. Click the three dots again → "Raw configuration editor"
4. Copy the contents of `dashboard.yaml` and paste it

## API Rate Limiting

The integration respects Torn City's API rate limit of 100 requests per minute. With the default update interval of 60 seconds, this integration makes approximately 8 requests per minute, well within the limits.

## Support

- **Issues:** [GitHub Issues](https://github.com/xlemmingx/ha-torn/issues)
- **Torn City API Documentation:** [Torn API](https://www.torn.com/swagger.php)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This integration is not affiliated with, endorsed by, or in any way officially connected with Torn City Ltd. or any of its subsidiaries or affiliates.
