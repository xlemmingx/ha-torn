"""DataUpdateCoordinator for Torn City integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from time import time
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, API_ENDPOINTS, API_TIMEOUT, DOMAIN, get_enabled_endpoints

_LOGGER = logging.getLogger(__name__)


class TornDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Torn City data update coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        update_interval: timedelta,
        throttle_api: bool = False,
        enabled_endpoint_options: dict[str, Any] | None = None,
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
        self.throttle_multiplier = 10 if throttle_api else 1
        self._cache: dict[str, Any] = {}  # Cached data per endpoint key
        self.cache_times: dict[str, float] = {}  # Last fetch time per endpoint key (public for sensors)

        # Get enabled endpoints based on options
        self.enabled_endpoints = get_enabled_endpoints(enabled_endpoint_options or {})
        # Build set of enabled data keys for quick lookup
        self.enabled_data_keys = {ep["key"] for ep in self.enabled_endpoints}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Torn City API."""
        combined_data = {}
        errors = []
        current_time = time()

        # Fetch data from enabled endpoints
        for endpoint_config in self.enabled_endpoints:
            path = endpoint_config["path"]
            data_key = endpoint_config["key"]
            params = endpoint_config.get("params", {})
            cache_for = endpoint_config.get("cache_for")

            # Check if we have cached data that's still valid
            if cache_for and data_key in self._cache:
                last_fetch = self.cache_times.get(data_key, 0)
                cache_age = current_time - last_fetch
                effective_cache_duration = cache_for * self.throttle_multiplier

                if cache_age < effective_cache_duration:
                    # Use cached data
                    combined_data[data_key] = self._cache[data_key]
                    _LOGGER.debug(f"Using cached data for {data_key} (age: {cache_age:.0f}s / {effective_cache_duration}s)")
                    continue

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
                        # Use cached data if available as fallback
                        if data_key in self._cache:
                            combined_data[data_key] = self._cache[data_key]
                        continue

                    data = await response.json()

                    if "error" in data:
                        error_msg = f"{data['error'].get('error', 'Unknown error')} on {path}"
                        _LOGGER.warning(f"API error: {error_msg}")
                        errors.append(error_msg)
                        # Use cached data if available as fallback
                        if data_key in self._cache:
                            combined_data[data_key] = self._cache[data_key]
                        continue

                    # Extract the actual data using the configured key
                    # The response structure is typically {"key": {...}}
                    # For endpoints with 'selections' param, the response key is the selection value
                    response_key = params.get("selections", data_key)
                    endpoint_data = data.get(response_key, {})
                    combined_data[data_key] = endpoint_data

                    # Update cache
                    self._cache[data_key] = endpoint_data
                    self.cache_times[data_key] = current_time
                    _LOGGER.debug(f"Fetched and cached {data_key}")

            except aiohttp.ClientError as err:
                error_msg = f"Network error on {path}: {err}"
                _LOGGER.warning(error_msg)
                errors.append(error_msg)
                # Use cached data if available as fallback
                if data_key in self._cache:
                    combined_data[data_key] = self._cache[data_key]
            except Exception as err:
                error_msg = f"Unexpected error on {path}: {err}"
                _LOGGER.warning(error_msg)
                errors.append(error_msg)
                # Use cached data if available as fallback
                if data_key in self._cache:
                    combined_data[data_key] = self._cache[data_key]

        # If no data was retrieved at all, raise UpdateFailed
        if not combined_data:
            raise UpdateFailed(f"Failed to fetch any data. Errors: {', '.join(errors)}")

        # Log summary if there were any errors
        if errors:
            _LOGGER.info(f"Update completed with {len(errors)} endpoint error(s): {', '.join(errors)}")

        return combined_data
