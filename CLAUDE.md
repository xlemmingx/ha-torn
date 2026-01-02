# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant add-on for Torn City (torn.com) game integration.

## Architecture

### Home Assistant Add-on Structure

This follows the standard Home Assistant add-on architecture:

- `config.yaml`: Add-on configuration defining options, schema, ports, and dependencies
- `Dockerfile`: Container image definition for the add-on
- `run.sh`: Main entry point script executed when the add-on starts (uses bashio framework)

### Bashio Framework

The add-on uses bashio (`/usr/bin/with-contenv bashio`), Home Assistant's bash scripting framework for add-ons. Bashio provides:
- Configuration option reading via `bashio::config`
- Logging via `bashio::log.*` functions
- Service availability checks
- Supervisor API interaction

## Development Commands

Since this is a Home Assistant add-on, development typically involves:

**Building the add-on:**
```bash
# Build locally using Home Assistant builder
docker build -t local/ha-torn .
```

**Testing:**
- Install the add-on in Home Assistant (via local add-on repository)
- Check logs in Home Assistant Supervisor
- Use `bashio::log.info`, `bashio::log.warning`, `bashio::log.error` for debugging

**Configuration:**
The `config.yaml` should follow Home Assistant add-on schema with sections:
- `name`, `version`, `slug`, `description`
- `arch`: Supported architectures (amd64, armhf, armv7, aarch64, i386)
- `options`: User-configurable options
- `schema`: JSON schema for option validation

## Key Considerations

### Configuration Management
Use bashio to read config values in run.sh:
```bash
API_KEY=$(bashio::config 'api_key')
INTERVAL=$(bashio::config 'update_interval')
```

### Torn City API Integration
The Torn API requires:
- API key authentication
- Rate limiting awareness (100 requests per minute)
- Proper error handling for API responses
- API endpoint: https://api.torn.com/

### Data Persistence
Home Assistant add-ons should use:
- `/data` directory for persistent storage
- Home Assistant's built-in services for state management where possible
