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
        try:
            combined_data = {}

            # Fetch data from all configured endpoints
            for endpoint_config in API_ENDPOINTS:
                path = endpoint_config["path"]
                data_key = endpoint_config["key"]
                params = endpoint_config.get("params", {})

                # Build URL with query parameters
                url = f"{API_BASE_URL}{path}"
                query_params = {"key": self.api_key, **params}

                async with self.session.get(
                    url, params=query_params, timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
                ) as response:
                    if response.status != 200:
                        raise UpdateFailed(
                            f"Error fetching {path}: HTTP {response.status}"
                        )

                    data = await response.json()

                    if "error" in data:
                        raise UpdateFailed(
                            f"API error on {path}: {data['error'].get('error', 'Unknown error')}"
                        )

                    # Extract the actual data using the configured key
                    # The response structure is typically {"key": {...}}
                    combined_data[data_key] = data.get(data_key, {})

            return combined_data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
