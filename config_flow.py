"""Config flow for Torn City integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DOMAIN, CONF_API_KEY, CONF_UPDATE_INTERVAL, API_BASE_URL, API_TIMEOUT, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=3600)
        ),
    }
)


async def validate_api_key(api_key: str, session: aiohttp.ClientSession) -> dict[str, Any]:
    """Validate the API key by making a test request."""
    url = f"{API_BASE_URL}/user/basic?key={api_key}"

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)) as response:
            if response.status == 200:
                data = await response.json()
                if "error" in data:
                    return {"error": data["error"]["error"]}
                profile = data.get("profile", {})
                return {"title": profile.get("name", "Torn City"), "user_id": profile.get("id")}
            return {"error": f"HTTP {response.status}"}
    except aiohttp.ClientError as err:
        _LOGGER.error("Error connecting to Torn API: %s", err)
        return {"error": "cannot_connect"}
    except Exception as err:
        _LOGGER.exception("Unexpected error: %s", err)
        return {"error": "unknown"}


class TornConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Torn City."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_create_clientsession(self.hass)
            result = await validate_api_key(user_input[CONF_API_KEY], session)

            if "error" in result:
                errors["base"] = result["error"]
            else:
                # Create a unique ID based on user ID
                await self.async_set_unique_id(str(result["user_id"]))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=result["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
