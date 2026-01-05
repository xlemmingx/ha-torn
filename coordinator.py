"""DataUpdateCoordinator for Torn City integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, API_ENDPOINTS, API_TIMEOUT, DOMAIN

_LOGGER = logging.getLogger(__name__)


class TornDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Torn City data update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.session = session
        self.api_key = api_key

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Torn City API."""
        combined_data = {}
        errors = []

        # Fetch data from all configured endpoints
        for endpoint_config in API_ENDPOINTS:
            path = endpoint_config["path"]
            data_key = endpoint_config["key"]
            params = endpoint_config.get("params", {})

            try:
                # Build URL with query parameters
                url = f"{API_BASE_URL}{path}"
                query_params = {"key": self.api_key, **params}

                async with self.session.get(
                    url, params=query_params, timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
                ) as response:
                    if response.status != 200:
                        error_msg = f"HTTP {response.status} on {path}"
                        _LOGGER.warning(error_msg)
                        errors.append(error_msg)
                        continue

                    data = await response.json()

                    if "error" in data:
                        error_msg = f"{data['error'].get('error', 'Unknown error')} on {path}"
                        _LOGGER.warning(f"API error: {error_msg}")
                        errors.append(error_msg)
                        continue

                    # Extract the actual data using the configured key
                    # The response structure is typically {"key": {...}}
                    combined_data[data_key] = data.get(data_key, {})

            except aiohttp.ClientError as err:
                error_msg = f"Network error on {path}: {err}"
                _LOGGER.warning(error_msg)
                errors.append(error_msg)
            except Exception as err:
                error_msg = f"Unexpected error on {path}: {err}"
                _LOGGER.warning(error_msg)
                errors.append(error_msg)

        # If no data was retrieved at all, raise UpdateFailed
        if not combined_data:
            raise UpdateFailed(f"Failed to fetch any data. Errors: {', '.join(errors)}")

        # Log summary if there were any errors
        if errors:
            _LOGGER.info(f"Update completed with {len(errors)} endpoint error(s): {', '.join(errors)}")

        return combined_data
