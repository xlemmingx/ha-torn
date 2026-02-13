# Torn City Integration for Home Assistant

A comprehensive Home Assistant integration for [Torn City](https://www.torn.com), providing real-time access to your player stats, finances, stocks, travel status, cooldowns, and more.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/xlemmingx/ha-torn.svg)](https://github.com/xlemmingx/ha-torn/releases)
[![Downloads](https://img.shields.io/endpoint?url=https://vaskivskyi.github.io/ha-custom-analytics/badges/torn/total.json)](https://github.com/xlemmingx/ha-torn)
[![License](https://img.shields.io/github/license/xlemmingx/ha-torn.svg)](LICENSE)

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=xlemmingx&repository=ha-torn&category=integration)

1. Open HACS → Integrations → Custom repositories
2. Add `https://github.com/xlemmingx/ha-torn` as "Integration"
3. Search for "Torn City" and install
4. Restart Home Assistant

### Manual Installation

1. Download from [releases page](https://github.com/xlemmingx/ha-torn/releases)
2. Copy to `config/custom_components/torn/`
3. Restart Home Assistant

## Configuration

1. Settings → Devices & Services → Add Integration
2. Search "Torn City"
3. Enter your [Torn City API key](https://www.torn.com/preferences.php#tab=api) (**Full Access** recommended)
4. Optional: Enable "Throttle API Usage" to reduce API calls if needed
5. Submit

### Customizing API Endpoints

After setup, you can configure which features to enable:

1. Settings → Devices & Services → Torn City → Configure
2. Enable/disable individual features (Money, Travel, Cooldowns, Stats, Skills, Company, Stocks, Refills, Log)
3. Disabled features reduce API usage and remove associated sensors

Profile & Bars are always enabled (core functionality).

## Features

### Player & Stats
- Name, level, status, battle stats (strength, defense, speed, dexterity)

### Bars & Cooldowns
- Energy, Nerve, Happy, Life, Chain with timers
- Chain timeout timer
- Drug, Medical, Booster cooldowns

### Finances
- Wallet, Vault, Banks, Company & Faction funds
- City Bank investments with profit tracking
- Daily networth

### Stocks (All 35 Torn stocks)
- Current prices, market cap, owned shares
- Stock benefit blocks tracking
- Ready-to-claim benefits

### Travel & Activity
- Destination, method, arrival/departure times
- Recent activity log

### Other
- Skills (dynamic sensors)
- Company stats

All sensors prefixed with `sensor.torn_` and `binary_sensor.torn_`.

## API Rate Limiting

The integration uses intelligent caching to minimize API calls:
- High frequency (5s cache): profile, bars, money, travel, log
- Medium frequency (60s cache): cooldowns, stats, company, stocks
- Low frequency (600s cache): skills, refills

**Default usage: ~64 API calls/minute** (64% of the 100/minute limit)

### Reducing API Usage

1. **Disable unused endpoints**: Configure the integration to disable features you don't use (each disabled feature saves 1-2 API calls)
2. **Enable "Throttle API Usage"**: Reduces update frequency by 10x if you're sharing an API key or approaching limits

## Privacy & Security

This integration stores your Torn City API key **locally** in your Home Assistant configuration only.

- No data is sent to external servers
- No data sharing with third parties
- API key is used only for fetching your personal Torn City data
- All data remains on your Home Assistant instance

## Support

- [GitHub Issues](https://github.com/xlemmingx/ha-torn/issues)
- [Torn API Documentation](https://www.torn.com/swagger.php)

## License

MIT License - see LICENSE file for details.

This integration is not affiliated with Torn City Ltd.
